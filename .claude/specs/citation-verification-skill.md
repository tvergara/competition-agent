# Spec: Citation Verification Skill (v1: existence + metadata)

## Goal

Ship a reusable "citation verification" skill that lets reviewer agents
deterministically detect **fabricated** or **metadata-mismatched** references in
ICML 2026 submissions on Koala by parsing each paper's `.bib` file and
resolving every entry against OpenAlex. v1 covers existence checking only;
misattribution / claim-vs-abstract NLI is deferred to a follow-up spec.

## Context

### How agents read papers today

- Koala's `get_paper` MCP tool returns `pdf_url` and a `tarball_url` pointing at
  `https://koala.science/storage/tarballs/<paper_id>.tar.gz`.
- The example paper (`59386b0e-204c-4c09-986a-109be4967508`) ships a clean LaTeX
  source tree with `ref.bib` at the top level. Verified manually: 704 lines of
  standard BibTeX, fields are mostly `author/title/booktitle/year` (no DOI or
  arXiv ID). This means **OpenAlex resolution will be title+author search** for
  the majority of refs, not DOI lookup.
- ICML uses `icml202X.bst`; we should not assume any single bibliography
  driver, but `.bib` files are the dominant format.

### How prompts are assembled

- `cli/reva/prompt.py` concatenates: `GLOBAL_RULES.md` + `platform_skills.md` +
  `agent_configs/<name>/system_prompt.md`. There is **no auto-include
  mechanism for skills** — the agent only sees what's in those three files.
- The agent (codex) runs from `agent_configs/<name>/` with shell access via
  `--dangerously-bypass-approvals-and-sandbox`. It can read any file in the
  repo and run any script.

### How the agent posts findings

- Comments require `github_file_url` pointing at a file in the agent's GitHub
  fork on a per-paper branch (`agent-reasoning/<agent>/<paper-id-prefix>`).
- The agent commits its reasoning file to that branch before posting the
  comment that references it.

### Existing consumers

- `factual-reviewer` (codex backend, scaffolded; default system prompt).
- Future reviewer agents that opt in.

## Requirements

1. **CLI: `tools/verify_citations.py`** (new top-level `tools/` directory,
   sibling to `cli/`).

   Inputs (mutually exclusive, exactly one required):
   - `--paper-id <uuid>` — fetches `https://koala.science/storage/tarballs/<id>.tar.gz`,
     extracts to a temp dir, parses every `.bib` file found.
   - `--tarball <path>` — same but reads a local tarball (for offline / test).
   - `--bibfile <path>` — parses a single `.bib` file directly (smallest unit
     for testing).

   Optional flags:
   - `--out <path>` — write JSON report to this path; default stdout.
   - `--openalex-mailto <email>` — passed in OpenAlex `?mailto=` query param to
     get the polite-pool rate limit (10 req/s vs. shared 10 req/s pool). Defaults
     to the env var `OPENALEX_MAILTO` if set, else omitted.

   Behaviour:
   - Parse the `.bib` with [`bibtexparser`](https://pypi.org/project/bibtexparser/) v2.
   - For each entry, build a resolution query in this priority:
     1. DOI → `GET https://api.openalex.org/works/doi:<doi>`
     2. arXiv ID (regex `arxiv\.org/abs/(\d{4}\.\d{4,5})` in any field, or
        `eprint = {…}` with `archivePrefix = {arXiv}`) →
        `GET https://api.openalex.org/works?search=arxiv+<id>`, falling back
        to title search if no result. (OpenAlex has no direct arXiv-ID lookup
        endpoint, so search is the only path.)
     3. Title + first author surname → `GET https://api.openalex.org/works?search=<title>&per_page=5`,
        fuzzy-match candidates.
   - Fuzzy match (rapidfuzz `token_set_ratio`):
     - Title similarity ≥ 90 → candidate accepted.
     - Then check ≥1 author surname appears in OpenAlex `authorships[*].author.display_name`
       (case-insensitive substring after ASCII-folding).
     - Year disagreement of ±1 is `metadata_mismatch`, ±0 is exact, > ±1 is also `metadata_mismatch`.
   - Per entry, emit:
     ```json
     {
       "key": "<bibtex key>",
       "raw": {"title": "...", "authors": [...], "year": 2024, "doi": null, "arxiv_id": null},
       "status": "verified" | "metadata_mismatch" | "not_found" | "ambiguous" | "error",
       "openalex_id": "https://openalex.org/W..." | null,
       "best_match": {"title": "...", "year": ..., "authors": [...]},
       "title_similarity": 0.0–1.0,
       "mismatches": ["year"|"authors"|"venue"],
       "error": "<message if status=error>"
     }
     ```
   - On network failure for an individual entry, emit `status: "error"` and
     continue. Top-level exit code 0 unless argument parsing or tarball
     download fails.
   - Add a top-level summary block:
     ```json
     {
       "paper_id": "...",
       "total": 42, "verified": 35, "mismatch": 4, "missing": 2, "ambiguous": 1, "error": 0,
       "entries": [...]
     }
     ```

2. **Skill doc: `agent_definition/skills/citation_verification.md`**

   New file (and new `skills/` subdir under `agent_definition/`). Contents:
   - Purpose: detect fabricated and mismatched citations, pre-comment.
   - When to run: once per paper, before forming the verdict; before posting
     any comment that makes a citation-related claim.
   - How to invoke:
     ```bash
     python tools/verify_citations.py --paper-id <paper_id> \
       --out agent-reasoning/<agent_name>/<paper-id-prefix>/citation_audit.json
     ```
   - How to interpret each `status`:
     - `verified` — do not surface; no value in commenting.
     - `metadata_mismatch` — surface only when the mismatch is meaningful
       (wrong author, wrong year by > 1, wrong venue). Year-off-by-one is
       common preprint-vs-conference noise; do **not** flag.
     - `not_found` — likely fabricated; investigate before flagging (try a
       Google Scholar search yourself). If you can't find the work, post a
       comment.
     - `ambiguous` — multiple candidates; usually not worth a public flag.
     - `error` — re-run; don't comment on tool errors.
   - Comment format template (markdown), with the rule that **the
     `citation_audit.json` MUST be committed to the agent's reasoning branch
     and linked as `github_file_url`** so the claim is auditable.
   - Cost reminder: at 1.0 karma for the first comment + 0.1 each, do not
     post more than ~3 citation-related comments per paper; bundle multiple
     issues into one comment when possible.

3. **Agent integration: `agent_configs/factual-reviewer/system_prompt.md`**

   Replace the TODO template with:
   - One-paragraph persona: "factual reviewer focused on the integrity of a
     paper's references and quantitative claims."
   - Pointer to the skill: instruction to read
     `agent_definition/skills/citation_verification.md` and run the audit
     before commenting on any paper.
   - Leave room for future skills (a `## Skills` section listing one item
     today, ready to grow).

4. **Tests: `tests/test_verify_citations.py`**

   Following the project's `test_*.py` convention. Mock all HTTP via
   `pytest-httpx` (preferred) or `responses`. No live network calls in unit
   tests.

   Cases:
   - `parse_bib_basic` — three entries (one with DOI, one with arXiv, one
     title-only) parse correctly.
   - `resolve_by_doi` — DOI present → OpenAlex `/works/doi:...` path is hit
     once and the work is returned.
   - `resolve_by_arxiv` — arXiv ID present → search path with `arxiv+<id>` is
     hit; fallback verified.
   - `resolve_by_title_match` — title similarity ≥ 90 + author surname overlap
     → `verified`.
   - `resolve_title_year_off_by_two` → `metadata_mismatch` with
     `mismatches=["year"]`.
   - `resolve_no_match` — search returns 0 results → `not_found`.
   - `resolve_ambiguous` — two candidates ≥ 90 with different authors → `ambiguous`.
   - `resolve_network_error` — httpx mock raises → `status: "error"`, CLI
     exit 0.
   - `cli_main_bibfile_smoke` — runs `tools/verify_citations.py
     --bibfile tests/fixtures/sample.bib` end-to-end against mocked HTTP and
     asserts the summary block (`verified=1, missing=1, mismatch=1`).

   Fixtures: `tests/fixtures/sample.bib` with three seeded entries
   (one resolvable, one fabricated, one wrong year). Mocked OpenAlex
   responses stored as `tests/fixtures/openalex_*.json`.

5. **Manual demo on the example paper** (not automated)

   Run:
   ```bash
   python tools/verify_citations.py --paper-id 59386b0e-204c-4c09-986a-109be4967508
   ```
   Record the summary line (counts) in a comment at the bottom of this spec
   file after implementation. This is a sanity gate, not a pass/fail test.

## Constraints

- **No new credentials.** OpenAlex is keyless; `OPENALEX_MAILTO` is optional.
  `.env.template` does not change.
- **Network errors must not crash the agent.** Per-entry errors are captured
  in the JSON; the CLI always exits 0 on data-level failures.
- **Dependencies.** Add `bibtexparser>=2.0.0`, `rapidfuzz>=3.0`, `httpx>=0.27`,
  and `pytest-httpx>=0.30` to `pyproject.toml` via `uv add`. No GROBID, no
  Java, no PDF parsing.
- **Performance.** Sequential resolution is fine for v1. Add a single 0.1s
  sleep between requests to stay polite; do not parallelize.
- **Scope.** Existence + metadata only. Do not implement claim-vs-abstract
  NLI or LLM-judging; that's a separate v2 spec.
- **No changes to `prompt.py`.** The skill is opt-in via a reference inside
  the agent's `system_prompt.md`. Auto-inclusion of skills is a separate spec
  later.
- **Backwards compatibility.** Existing 172 tests must still pass clean.

## Test Plan

- Unit tests in `tests/test_verify_citations.py` using `pytest-httpx` to mock
  every OpenAlex call.
- Three `.bib` fixtures under `tests/fixtures/`, three OpenAlex JSON fixtures.
- Integration smoke run on the example paper, executed manually post-merge.

## Acceptance Criteria

- [ ] `uv run pytest tests/test_verify_citations.py` passes with at least 9
      test cases.
- [ ] `uv run pytest` passes overall (existing 172 + new ones, all green).
- [ ] `python tools/verify_citations.py --bibfile tests/fixtures/sample.bib`
      produces a JSON summary with exactly one `verified`, one `not_found`,
      one `metadata_mismatch` against the seeded fixture HTTP mocks.
- [ ] `python tools/verify_citations.py --paper-id 59386b0e-204c-4c09-986a-109be4967508`
      runs end-to-end against live Koala + OpenAlex, exits 0, and prints a
      JSON summary with non-zero `total`.
- [ ] `agent_definition/skills/citation_verification.md` exists and explains:
      when to run, how to invoke, how to interpret each `status`, how to
      format the comment, where to commit the audit JSON.
- [ ] `agent_configs/factual-reviewer/system_prompt.md` no longer contains
      the TODO marker and references the skill file.
- [ ] `.env.template` is unchanged (no new credentials).
- [ ] `pyproject.toml` lists the new deps; `uv.lock` is updated.

## Out of scope (explicit)

- Claim-vs-abstract entailment / NLI / LLM-judge → v2 spec.
- Citation intent classification (background vs. method vs. result) → v2.
- PDF parsing fallback when no `.bib` exists in the tarball → v2 (fail with a
  clear message in v1).
- Self-consistency checks on the agent's own citations → separate concern.

## Manual demo result

`python tools/verify_citations.py --paper-id 59386b0e-204c-4c09-986a-109be4967508`
on 2026-04-25:

- exit code: 0
- summary: `total=52, verified=28, mismatch=0, missing=5, ambiguous=19, error=0`
