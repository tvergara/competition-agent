# Spec: Flip Semantic Scholar to primary, OpenAlex to fallback

## Goal
Make Semantic Scholar the primary citation lookup in `tools/verify_citations.py`,
with OpenAlex as the secondary fallback. Today's order is the reverse, and
OpenAlex's `/works?search=` endpoint is being IP-throttled (HTTP 429) on Mila
compute nodes regardless of mailto, which currently bricks `factual-reviewer`.

## Context
- `tools/verify_citations.py:resolve_entry` orchestrates a per-entry resolution.
  Today it calls `_resolve_openalex` first and only consults `_resolve_s2` when
  the OpenAlex outcome is `not_found`, `ambiguous`, or `metadata_mismatch`.
- The two resolvers are largely symmetric — each handles DOI / arXiv / title
  search and classifies against the candidate. The merge step
  (`_apply_s2_result`) is currently asymmetric: it overlays S2 onto an existing
  OpenAlex result.
- The factual-reviewer agent runs an ad-hoc `curl` probe of OpenAlex search at
  the start of every loop iteration (`agent_configs/factual-reviewer/cluster.*.out`).
  When that probe returns 429 it idles for the rest of the iteration without
  ever invoking `verify_citations.py`. Even after we flip the primary, the agent
  will keep short-circuiting unless the prompt is updated.
- Existing test suite (`tests/test_verify_citations.py`) hard-codes
  `match_source == "openalex"` for the happy paths (DOI, arXiv, title-only,
  ambiguous, year-mismatch, etc.), and only mocks OpenAlex in those cases. Those
  expectations flip too.

## Requirements
1. **`resolve_entry` order flip — only for the search-based path.** The order
   depends on which lookup the entry needs:
   - **DOI present:** call OpenAlex (`/works/doi:`) first. This endpoint is
     keyed, reliable, and not subject to the IP throttling we're routing
     around. If OpenAlex returns 404 or raises, fall through to S2
     (`/paper/DOI:`).
   - **arXiv id present (no DOI):** call S2 (`/paper/arXiv:`) first — also a
     keyed lookup. If S2 misses or raises, fall through to OpenAlex's
     search-based arxiv path.
   - **Title-only (no DOI, no arXiv):** call S2 search first. If S2 returns
     `verified` or `skipped`, do not call OpenAlex. Otherwise (`not_found`,
     `ambiguous`, `metadata_mismatch`, or raise) fall through to OpenAlex
     search and apply the priority-based merge.
   If both sources raise, return `status: error` with both error strings
   concatenated (e.g. `"S2: ConnectError: ... | OpenAlex: ConnectError: ..."`).
2. **Symmetric merge.** Generalize `_apply_s2_result` so it works in both
   directions. The "lower-priority result is upgraded if the secondary returns
   a higher-priority status" rule is unchanged; only the orientation flips.
   Concretely: the result dict still tracks both `openalex_id` and
   `semantic_scholar_id` independently, and `match_source` reflects whichever
   source supplied `best_match`/`title_similarity`/`mismatches`.
3. **Counters preserved.** Names (`s2_consulted`, `s2_lifted`) and JSON keys
   are unchanged — committed audit JSONs and the skill doc reference them.
   New semantics:
   - `s2_consulted` increments whenever S2 was called for an entry. With the
     order flip, this is *most* non-skipped entries: every title-only and
     every arXiv entry, plus DOI entries where OpenAlex missed.
   - `s2_lifted` keeps its current meaning: the entry's final status is better
     than what the *first-consulted* source would have returned alone. For
     DOI entries with OpenAlex first, this means S2 lifted an OpenAlex miss.
     For title-only with S2 first, this means OpenAlex lifted an S2 miss.
   Add no new counters.
4. **Tests rewritten, not skipped.** Every existing test that asserted
   `match_source == "openalex"` for a happy path now asserts S2 was called and
   the match came from S2 (or OpenAlex if S2 was mocked to miss). The S2
   `429-retry` test stays as-is. The CLI smoke test (`test_cli_main_bibfile_smoke`)
   is updated to mock S2 first and OpenAlex as the fallback. **No test gets
   `@pytest.mark.skip` or deletion** — every behavior the test was guarding
   should be re-expressed under the new ordering.
5. **Skill doc updated.** `agent_definition/skills/citation_verification.md`
   reflects the new ordering ("Semantic Scholar primary, OpenAlex fallback") and
   the corresponding interpretation of `not_found` (now: both indices missed,
   same evidence as today, just reached in the opposite order). Update the
   prose explaining `s2_consulted` / `s2_lifted`.
6. **Drop the curl probe in factual-reviewer.** Edit
   `agent_configs/factual-reviewer/system_prompt.md` to instruct the agent not
   to run ad-hoc liveness probes against OpenAlex / S2. The right behavior is
   to call `python tools/verify_citations.py --paper-id <id>` and act on the
   report; per-entry `error` statuses indicate transient failures, not a reason
   to halt the whole pass.

## Constraints
- **Must not change** the CLI surface (`--paper-id` / `--tarball` /
  `--bibfile` / `--out` / `--openalex-mailto`). The env var
  `OPENALEX_MAILTO` still feeds the OpenAlex polite pool.
- **Must not change** the `entries[*]` JSON shape. Reasoning files / commits
  written by past audits should still parse.
- **Must not change** the `STATUS_PRIORITY` ordering or the per-status
  classifier behavior — only the dispatch order.
- **Must not change** the `S2_*` rate-limit constants or the `_s2_get`
  retry/backoff logic.
- The `OPENALEX_MAILTO` env wiring (added in `.env` and `cli/reva/launch_script.py`
  earlier this session) stays. The flip is independent of throttling status —
  S2 stays primary even when OpenAlex recovers.

## Test Plan
File: `tests/test_verify_citations.py`.

- **Rewrite** existing happy-path tests so each one mocks S2 (success case) and
  asserts `match_source == "semantic_scholar"`. The OpenAlex-only mocks become
  S2-only mocks for those tests.
- **Add** `test_openalex_lifts_s2_not_found` — symmetric to today's
  `test_s2_lifts_not_found`. S2 returns empty, OpenAlex returns a verified
  candidate, final `match_source == "openalex"`.
- **Add** `test_openalex_lifts_s2_ambiguous` — symmetric to today's
  `test_s2_lifts_ambiguous_to_verified`.
- **Update** `test_s2_skipped_when_openalex_verified` →
  `test_openalex_skipped_when_s2_verified` (mirror image: S2 verifies, no
  OpenAlex call is made).
- **Add** `test_openalex_called_when_s2_raises` — mock S2 to raise
  `httpx.ConnectError`, mock OpenAlex to return a verified candidate, assert
  result is verified via OpenAlex and `s2_consulted == True`.
- **Update** `test_resolve_network_error` so it covers *both* sources raising,
  with the resulting `status: error` containing both error fingerprints.
- **Update** `test_cli_main_bibfile_smoke` so the fixture's three entries are
  resolved against S2 first; OpenAlex fallback fires for the not_found and
  metadata_mismatch entries. Final `s2_consulted == 3`, `s2_lifted == 0`.

## Acceptance Criteria
- [ ] `uv run pytest tests/test_verify_citations.py -q` passes with 0 skipped
      and ≥ the current count of test functions plus the two new symmetric
      "OpenAlex lifts S2" tests.
- [ ] Manual trace: in `resolve_entry`, the first network call for a non-skipped
      entry without DOI is to `api.semanticscholar.org/graph/v1/paper/search`,
      not `api.openalex.org/works?search=`.
- [ ] When S2 returns a clean `verified`, no request to `api.openalex.org` is
      made for that entry (verified by `httpx_mock.get_requests()` filter in the
      updated `test_openalex_skipped_when_s2_verified`).
- [ ] `agent_definition/skills/citation_verification.md` no longer claims
      OpenAlex is the primary; the word "primary" appears at most once and
      refers to Semantic Scholar.
- [ ] `agent_configs/factual-reviewer/system_prompt.md` contains an explicit
      instruction not to probe OpenAlex/S2 with ad-hoc curl before running
      `verify_citations.py`. Existing factual-reviewer behavior loop is
      otherwise unchanged.
- [ ] No file outside the four listed in Requirements is modified.
