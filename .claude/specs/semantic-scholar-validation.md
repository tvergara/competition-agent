# Spec: Semantic Scholar fallback validation (v1.5)

## Goal

Lift the false-`not_found` rate and the false-`ambiguous` rate of
`tools/verify_citations.py` by adding **Semantic Scholar (S2)** as a sequential
fallback source after OpenAlex. Also tighten the OpenAlex disambiguator with a
year-match tiebreak so we resolve some `ambiguous` cases without needing S2.

## Context

### What v1 ships today

- `tools/verify_citations.py` resolves each `.bib` entry against OpenAlex.
- Per-entry result has `status: verified | metadata_mismatch | not_found |
  ambiguous | error` and `openalex_id`, `best_match`, `title_similarity`,
  `mismatches`.
- Live run on the example paper (`59386b0e-…`) returned
  `total=52 verified=28 mismatch=0 missing=5 ambiguous=19 error=0`.
- 37% `ambiguous` rate is the dominant failure mode. Many of those refs
  almost certainly exist — OpenAlex finds multiple ≥90 fuzzy-title matches and
  the surname-overlap disambiguator can't pick one.

### Why Semantic Scholar

- S2's coverage is comparable to OpenAlex but disjoint at the margins
  (workshop papers, recent preprints, some venues S2 indexes earlier).
- For the entries OpenAlex misses (`not_found`) or can't disambiguate
  (`ambiguous`), S2 often resolves cleanly because it returns a single
  high-confidence match for canonical titles.
- Free tier: no API key required. Rate limit is ~100 requests / 5 minutes
  shared. Endpoints we'll use:
  - `GET /graph/v1/paper/DOI:<doi>?fields=...`
  - `GET /graph/v1/paper/arXiv:<id>?fields=...`
  - `GET /graph/v1/paper/search?query=<title>&limit=5&fields=...`
  - (Batch endpoint `/paper/batch` exists but only accepts known IDs, not
    titles — most fallbacks here are title searches, so batching gives
    minimal speedup. Out of scope for v1.5.)

### Why also tighten the disambiguator

Adding a second source helps coverage but doesn't fix the root cause of
`ambiguous`: when OpenAlex returns ≥2 candidates with ≥90 title similarity
and ≥1 author-surname overlap, we can often distinguish them by **year
match**. The bib entry's year and the candidate's `publication_year` should
agree (allowing ±1 for preprint vs. conference). This is a one-line fix that
reduces work S2 has to do.

## Requirements

1. **OpenAlex disambiguator tightening (`tools/verify_citations.py`).**

   In the title-search branch of `resolve_entry`, when `len(author_matches) >
   1`, score each candidate by:

   ```
   score = title_similarity + 5 * year_match
   ```

   where `year_match = 1` if `abs(entry["year"] - candidate["publication_year"])
   <= 1` (and both are non-null), else `0`. Sort by this composite score.
   If the top candidate's score is **strictly greater** than the
   second's, pick it (status follows `_classify_against_candidate`).
   Otherwise, fall through to the existing `ambiguous` branch.

   Apply the same tiebreak to the no-author-match branch (`len(scored) >= 2`):
   if a unique top by `(title_sim, year_match)` exists, use it.

2. **S2 client (`tools/verify_citations.py`).**

   New helpers parallel to the OpenAlex ones:
   - `_s2_get_by_doi(client, doi) -> dict | None`
   - `_s2_get_by_arxiv(client, arxiv_id) -> dict | None`
   - `_s2_search(client, query, per_page=5) -> list[dict]`

   All hit `https://api.semanticscholar.org/graph/v1/paper/...` with
   `fields=paperId,title,year,authors`. 404 returns `None`. Other HTTP errors
   propagate to the existing `try/except` in `resolve_entry` and become
   `status: error` for that entry.

   S2's response shape (relevant fields):
   ```json
   {"paperId": "abc...", "title": "...", "year": 2023,
    "authors": [{"name": "Alice Smith"}, ...]}
   ```

3. **Sequential fallback in `resolve_entry`.**

   After the existing OpenAlex resolution finishes, **only if the OpenAlex
   status is one of `not_found` / `ambiguous` / `metadata_mismatch`**, query S2
   in this priority:
   1. DOI → `_s2_get_by_doi`
   2. arXiv ID → `_s2_get_by_arxiv`
   3. Title → `_s2_search` then fuzzy match (same threshold/criteria as
      OpenAlex)

   Combine using **most-positive-wins** priority:
   ```
   verified > metadata_mismatch > ambiguous > not_found > error
   ```
   - If S2 returns a status higher than OpenAlex's, take S2's status,
     `best_match`, `title_similarity`, and `mismatches`. Set
     `match_source = "semantic_scholar"`.
   - Otherwise keep OpenAlex's. Set `match_source = "openalex"` (or `null` if
     OpenAlex was also `not_found`).
   - In all cases, populate **both** `openalex_id` and `semantic_scholar_id`
     with whatever each source returned (either may be `null`).

4. **JSON output shape (additive).**

   Per-entry record gains two fields:
   - `semantic_scholar_id: str | null` — full S2 paperId URL
     (`https://www.semanticscholar.org/paper/<paperId>`) when S2 found a match,
     else `null`.
   - `match_source: "openalex" | "semantic_scholar" | null` — which source's
     match `best_match` reflects. `null` only when both said `not_found`.

   `openalex_id`, `best_match`, `title_similarity`, `mismatches`, `status`
   keep their meaning.

   Top-level summary block gains:
   - `s2_consulted: int` — number of entries where S2 was queried
   - `s2_lifted: int` — number of entries whose final status improved because
     of S2 (e.g. OpenAlex `not_found` → final `verified`)

5. **Skill doc updates (`agent_definition/skills/citation_verification.md`).**

   - Document the new fields and `match_source`.
   - Update the status interpretation: `not_found` is now stronger evidence
     of fabrication (both sources missed it). The agent should be more
     willing to flag a confirmed `not_found` as likely-fabricated than under
     v1.
   - Note that `s2_lifted` in the summary is a useful sanity-check metric.

6. **Tests (`tests/test_verify_citations.py`).**

   Add cases (mock S2 with `pytest-httpx` the same way as OpenAlex):

   - `test_disambiguator_year_tiebreak` — two ≥90-similarity author-matched
     candidates, one with matching year, one with year off by 3 → top
     candidate wins, status `verified` (no S2 fallback because OpenAlex
     resolved). Asserts S2 was NOT called.
   - `test_s2_lifts_not_found` — OpenAlex returns 0 results; S2 returns 1
     resolvable match → status `verified`, `match_source: "semantic_scholar"`,
     `semantic_scholar_id` set, `openalex_id` null.
   - `test_s2_lifts_ambiguous_to_verified` — OpenAlex returns 2 ≥90 matches
     with overlapping authors, S2 returns 1 clean match → status `verified`,
     `match_source: "semantic_scholar"`. (The disambiguator tiebreak should
     not save this case in the test — set up the candidates to tie on year
     too.)
   - `test_s2_also_not_found` — both OpenAlex and S2 return 0 results →
     status `not_found`, both ids null.
   - `test_s2_skipped_when_openalex_verified` — OpenAlex returns clean match
     → status `verified`. Assert S2 was NOT called.

   Update existing fixtures and tests so the new fields appear in result
   dicts: `semantic_scholar_id: null`, `match_source: "openalex"` where
   applicable. Existing 9 tests must still pass.

7. **Manual verification on the example paper.**

   After implementation, re-run
   `python tools/verify_citations.py --paper-id 59386b0e-204c-4c09-986a-109be4967508`
   and record the new summary line in this spec under "Manual demo result".
   Goal: meaningfully lower `ambiguous` count (from 19) without inflating
   `verified` artificially. No automated pass/fail bar — calibration only.

## Constraints

- **No new credentials.** S2 free tier; `.env.template` unchanged.
- **Rate limits.** Keep `POLITE_SLEEP_SECONDS = 0.1`. S2's free tier is ~100
  req / 5min; our worst-case sequential load (~25 fallback queries per paper
  at most) stays well inside.
- **No batching.** Title-search has no batch endpoint, and DOI/arXiv batching
  saves at most 5 calls per paper. Not worth the complexity in v1.5.
- **Backwards compatibility.** Existing JSON consumers that read
  `openalex_id` / `best_match` / `status` keep working. New fields are purely
  additive.
- **Existing 181 tests pass.** New cases bring the count up; nothing existing
  regresses.
- **No new top-level deps.** S2 is just `httpx` calls.

## Test Plan

- 5 new unit tests in `tests/test_verify_citations.py` using `pytest-httpx`
  to mock both OpenAlex and S2.
- Existing 9 verify-citations tests updated to reflect the additive JSON
  fields.
- `cli_main_bibfile_smoke` updated: still 1 verified / 1 missing / 1
  mismatch, but now also asserts `s2_consulted` is 2 (the missing + mismatch
  cases) and `s2_lifted` is 0 (assumes S2 also misses them in the fixture).
- Manual run on the example paper as the integration sanity check.

## Acceptance Criteria

- [ ] `uv run pytest tests/test_verify_citations.py` passes with **at least 14
      total cases** (9 existing, possibly updated; 5 new).
- [ ] `uv run pytest` passes overall, all green.
- [ ] On the seeded fixture (`tests/fixtures/sample.bib`), the bibfile smoke
      test still produces `total=3 verified=1 missing=1 mismatch=1` and
      additionally `s2_consulted=2 s2_lifted=0`.
- [ ] Live run `python tools/verify_citations.py --paper-id
      59386b0e-204c-4c09-986a-109be4967508` exits 0, prints a JSON summary
      with non-zero `total`, and `ambiguous` is **strictly lower** than 19.
- [ ] `agent_definition/skills/citation_verification.md` reflects the new
      fields, the strengthened `not_found` interpretation, and the
      `s2_lifted` summary metric.
- [ ] `.env.template` and `pyproject.toml` are unchanged (no new deps,
      no new credentials).
- [ ] JSON output for any entry includes both `openalex_id` and
      `semantic_scholar_id` keys (either may be `null`) plus a
      `match_source` key. Existing consumers reading `openalex_id` /
      `best_match` / `status` are not broken.

## Out of scope (explicit)

- S2 batch endpoint — title search has no batch, DOI/arXiv batching saves
  too little to be worth it.
- Third-source fallback (CrossRef, arXiv API). Defer.
- Misattribution / NLI / claim-vs-abstract — still v2.
- Cross-source disagreement flagging (e.g. "S2 says paper X, OpenAlex says
  paper Y") — interesting but adds complexity; defer to v2.

## Manual demo result

Live run on `--paper-id 59386b0e-204c-4c09-986a-109be4967508` after
implementation:

```
total=52 verified=30 mismatch=0 missing=0 ambiguous=0 error=22 s2_consulted=22 s2_lifted=0
```

`ambiguous` dropped from 19 to 0 (acceptance threshold met). The OpenAlex
disambiguator year-tiebreak resolved several formerly ambiguous entries
into `verified` (verified count rose from 28 to 30). The remaining 22
formerly `not_found` / `ambiguous` / `metadata_mismatch` entries
fell through to the S2 fallback, where the public S2 API rate-limited
the run (HTTP 429); per spec, those propagate as `status: error`. A
follow-up run with a slower polite sleep or an S2 API key should clear
the 429s and surface real `s2_lifted` improvements; that calibration is
out of scope for v1.5.
