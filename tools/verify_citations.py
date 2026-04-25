"""Resolve every BibTeX entry in a paper against Semantic Scholar (with OpenAlex fallback)."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tarfile
import tempfile
import time
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import bibtexparser
import httpx
from rapidfuzz import fuzz


OPENALEX_BASE = "https://api.openalex.org"
S2_BASE = "https://api.semanticscholar.org/graph/v1"
S2_FIELDS = "paperId,title,year,authors"
S2_PAPER_URL_PREFIX = "https://www.semanticscholar.org/paper/"
KOALA_TARBALL_TEMPLATE = "https://koala.science/storage/tarballs/{paper_id}.tar.gz"
TITLE_SIMILARITY_THRESHOLD = 90
POLITE_SLEEP_SECONDS = 0.1
S2_SLEEP_AUTH = 1.0
S2_SLEEP_UNAUTH = 3.0
S2_BACKOFF_BASE = 4.0
S2_MAX_RETRIES = 3
ARXIV_RE = re.compile(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", re.IGNORECASE)

STATUS_PRIORITY = {
    "skipped": 5,
    "verified": 4,
    "metadata_mismatch": 3,
    "ambiguous": 2,
    "not_found": 1,
    "error": 0,
}

NON_ACADEMIC_ENTRY_TYPES = {
    "online", "dataset", "software", "manual", "electronic",
    "www", "webpage", "booklet",
}

NEWS_OUTLET_KEYWORDS = [
    "new york times", "washington post", "wall street journal",
    "tech policy press", "bloomberg", "reuters", "bbc", "cnn",
    "forbes", "wired", "techcrunch", "the verge", "the guardian",
    "financial times", "wikipedia", "wikimedia",
]

NON_ACADEMIC_PUBLISHERS = ["kaggle", "wikimedia", "github"]


# ---- Bib parsing -----------------------------------------------------------


def _entry_field(entry, name: str) -> str | None:
    for f in entry.fields:
        if f.key.lower() == name.lower():
            return str(f.value).strip()
    return None


def _split_bib_authors(raw: str | None) -> list[str]:
    if not raw:
        return []
    parts = re.split(r"\s+and\s+", raw.strip(), flags=re.IGNORECASE)
    return [p.strip() for p in parts if p.strip()]


def _extract_arxiv_id(entry) -> str | None:
    eprint = _entry_field(entry, "eprint")
    archive = _entry_field(entry, "archivePrefix")
    if eprint and (
        (archive and "arxiv" in archive.lower())
        or re.match(r"^\d{4}\.\d{4,5}$", eprint)
    ):
        m = re.search(r"\d{4}\.\d{4,5}", eprint)
        if m:
            return m.group(0)
    for f in entry.fields:
        m = ARXIV_RE.search(str(f.value))
        if m:
            return m.group(1)
    return None


def _coerce_year(raw: str) -> int | None:
    m = re.search(r"\d{4}", raw)
    return int(m.group(0)) if m else None


def parse_bib_file(path: Path) -> list[dict[str, Any]]:
    """Parse a BibTeX file into a list of normalized entry dicts."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    library = bibtexparser.parse_string(text)
    out: list[dict[str, Any]] = []
    for entry in library.entries:
        title_raw = _entry_field(entry, "title")
        title = re.sub(r"\s+", " ", re.sub(r"[{}]", "", title_raw)).strip() if title_raw else ""
        year_raw = _entry_field(entry, "year")
        out.append(
            {
                "key": entry.key,
                "entry_type": entry.entry_type,
                "title": title,
                "authors": _split_bib_authors(_entry_field(entry, "author")),
                "year": _coerce_year(year_raw) if year_raw else None,
                "doi": _entry_field(entry, "doi"),
                "arxiv_id": _extract_arxiv_id(entry),
                "journal": _entry_field(entry, "journal"),
                "publisher": _entry_field(entry, "publisher"),
                "url": _entry_field(entry, "url"),
            }
        )
    return out


def _should_skip(entry: dict) -> bool:
    """Return True for non-academic sources we don't try to resolve.

    Reads optional bib fields (``publisher``, ``journal``, ``url``) which
    ``parse_bib_file`` always sets (to ``None`` when missing). Tests that
    construct entries directly may omit them; ``.get`` keeps that boundary
    permissive so the function works on both shapes.
    """
    if entry.get("entry_type", "").lower() in NON_ACADEMIC_ENTRY_TYPES:
        return True
    publisher = entry.get("publisher") or ""
    if any(p in publisher.lower() for p in NON_ACADEMIC_PUBLISHERS):
        return True
    journal = entry.get("journal") or ""
    if any(k in journal.lower() for k in NEWS_OUTLET_KEYWORDS):
        return True
    if entry.get("url") and not entry.get("doi") and not entry.get("arxiv_id"):
        return True
    return False


def _key_style_outliers(entries: list[dict]) -> list[str]:
    """Flag bib keys whose embedded year-digit count differs from the dominant one.

    LLM-fabricated citations sometimes cluster on a different key style than the
    rest of the bibliography (e.g. 2-digit-year keys against a 4-digit-year
    majority). Returns [] if no dominant pattern exists (≥70% share).
    """
    digit_counts = []
    for e in entries:
        m = re.search(r"\d+", e["key"])
        if m:
            digit_counts.append(len(m.group(0)))
    if not digit_counts:
        return []
    most_common, cnt = Counter(digit_counts).most_common(1)[0]
    if cnt < 0.7 * len(digit_counts):
        return []
    outliers = []
    for e in entries:
        m = re.search(r"\d+", e["key"])
        if m and len(m.group(0)) != most_common:
            outliers.append(e["key"])
    return outliers


# ---- OpenAlex calls --------------------------------------------------------


def _maybe_mailto(params: dict[str, str], mailto: str | None) -> dict[str, str]:
    if mailto:
        params = dict(params)
        params["mailto"] = mailto
    return params


def _get_by_doi(client: httpx.Client, doi: str, mailto: str | None) -> dict | None:
    url = f"{OPENALEX_BASE}/works/doi:{doi}"
    resp = client.get(url, params=_maybe_mailto({}, mailto), timeout=20.0)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def _search_works(
    client: httpx.Client, query: str, mailto: str | None, per_page: int = 5
) -> list[dict]:
    params = _maybe_mailto({"search": query, "per_page": str(per_page)}, mailto)
    resp = client.get(f"{OPENALEX_BASE}/works", params=params, timeout=20.0)
    resp.raise_for_status()
    return resp.json()["results"]


# ---- Semantic Scholar calls ------------------------------------------------


def _s2_get(
    client: httpx.Client, url: str, params: dict[str, str]
) -> httpx.Response:
    """GET with a polite pre-call sleep and exponential backoff on 429.

    With ``SEMANTIC_SCHOLAR_API_KEY`` set, sends ``x-api-key`` and sleeps
    ``S2_SLEEP_AUTH`` (1s, the authenticated rate limit). Without a key,
    sleeps ``S2_SLEEP_UNAUTH`` (3s) on the shared free pool. On 429, retries
    up to ``S2_MAX_RETRIES`` times waiting ``S2_BACKOFF_BASE * 2**attempt``.
    """
    api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    headers = {"x-api-key": api_key} if api_key else {}
    time.sleep(S2_SLEEP_AUTH if api_key else S2_SLEEP_UNAUTH)
    for attempt in range(S2_MAX_RETRIES + 1):
        resp = client.get(url, params=params, headers=headers, timeout=20.0)
        if resp.status_code != 429:
            return resp
        if attempt < S2_MAX_RETRIES:
            time.sleep(S2_BACKOFF_BASE * (2 ** attempt))
    return resp


def _s2_get_by_doi(client: httpx.Client, doi: str) -> dict | None:
    resp = _s2_get(client, f"{S2_BASE}/paper/DOI:{doi}", {"fields": S2_FIELDS})
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def _s2_get_by_arxiv(client: httpx.Client, arxiv_id: str) -> dict | None:
    resp = _s2_get(client, f"{S2_BASE}/paper/arXiv:{arxiv_id}", {"fields": S2_FIELDS})
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def _s2_search(
    client: httpx.Client, query: str, per_page: int = 5
) -> list[dict]:
    params = {"query": query, "limit": str(per_page), "fields": S2_FIELDS}
    resp = _s2_get(client, f"{S2_BASE}/paper/search", params)
    resp.raise_for_status()
    return resp.json().get("data", [])


# ---- Matching helpers ------------------------------------------------------


def _strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)
    )


def _surname_from_bibtex(name: str) -> str:
    if "," in name:
        return name.split(",", 1)[0].strip().lower()
    return name.strip().split()[-1].lower()


def _candidate_author_names(work: dict) -> list[str]:
    return [a["author"]["display_name"] for a in work["authorships"]]


def _s2_author_names(work: dict) -> list[str]:
    return [a["name"] for a in work["authors"]]


def _author_surname_overlap(
    raw_authors: Iterable[str], candidate_authors: Iterable[str]
) -> bool:
    raw_surnames = {_strip_accents(_surname_from_bibtex(n)) for n in raw_authors if n}
    if not raw_surnames:
        return False
    candidate_blob = " ".join(_strip_accents(n).lower() for n in candidate_authors)
    return any(sn and sn in candidate_blob for sn in raw_surnames)


def _candidate_title(work: dict) -> str:
    return work["display_name"].strip()


def _s2_candidate_title(work: dict) -> str:
    return work["title"].strip()


def _normalize_for_match(s: str) -> str:
    return re.sub(r"([a-z])([A-Z])", r"\1 \2", s).lower()


def _title_similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return float(fuzz.token_set_ratio(_normalize_for_match(a), _normalize_for_match(b)))


def _year_match(raw_year: int | None, cand_year: int | None) -> int:
    if raw_year is None or cand_year is None:
        return 0
    return 1 if abs(raw_year - cand_year) <= 1 else 0


def _classify_against_candidate(
    raw: dict, candidate: dict
) -> tuple[str, list[str]]:
    mismatches: list[str] = []
    raw_year = raw["year"]
    cand_year = candidate.get("publication_year")
    if raw_year and cand_year and abs(raw_year - cand_year) > 1:
        mismatches.append("year")
    if not _author_surname_overlap(raw["authors"], _candidate_author_names(candidate)):
        mismatches.append("authors")
    if mismatches:
        return "metadata_mismatch", mismatches
    return "verified", mismatches


def _classify_against_s2_candidate(
    raw: dict, candidate: dict
) -> tuple[str, list[str]]:
    mismatches: list[str] = []
    raw_year = raw["year"]
    cand_year = candidate.get("year")
    if raw_year and cand_year and abs(raw_year - cand_year) > 1:
        mismatches.append("year")
    if not _author_surname_overlap(raw["authors"], _s2_author_names(candidate)):
        mismatches.append("authors")
    if mismatches:
        return "metadata_mismatch", mismatches
    return "verified", mismatches


def _build_best_match(work: dict) -> dict:
    return {
        "title": _candidate_title(work),
        "year": work.get("publication_year"),
        "authors": _candidate_author_names(work),
    }


def _build_s2_best_match(work: dict) -> dict:
    return {
        "title": _s2_candidate_title(work),
        "year": work.get("year"),
        "authors": _s2_author_names(work),
    }


def _empty_result(entry: dict) -> dict:
    return {
        "key": entry["key"],
        "raw": {
            "title": entry["title"],
            "authors": entry["authors"],
            "year": entry["year"],
            "doi": entry["doi"],
            "arxiv_id": entry["arxiv_id"],
        },
        "status": "not_found",
        "openalex_id": None,
        "semantic_scholar_id": None,
        "match_source": None,
        "best_match": None,
        "title_similarity": 0.0,
        "mismatches": [],
        "error": None,
    }


def _finalize_match(result: dict, work: dict, entry: dict) -> dict:
    sim = _title_similarity(entry["title"], _candidate_title(work))
    result["openalex_id"] = work.get("id")
    result["best_match"] = _build_best_match(work)
    result["title_similarity"] = sim / 100.0
    status, mismatches = _classify_against_candidate(entry, work)
    result["status"] = status
    result["mismatches"] = mismatches
    result["match_source"] = "openalex"
    return result


def _set_ambiguous(result: dict, top: tuple[float, dict]) -> dict:
    sim, work = top
    result["status"] = "ambiguous"
    result["openalex_id"] = work.get("id")
    result["best_match"] = _build_best_match(work)
    result["title_similarity"] = sim / 100.0
    result["match_source"] = "openalex"
    return result


def _finalize_s2_match(result: dict, work: dict, entry: dict) -> dict:
    sim = _title_similarity(entry["title"], _s2_candidate_title(work))
    result["semantic_scholar_id"] = _s2_id_url(work)
    result["best_match"] = _build_s2_best_match(work)
    result["title_similarity"] = sim / 100.0
    status, mismatches = _classify_against_s2_candidate(entry, work)
    result["status"] = status
    result["mismatches"] = mismatches
    result["match_source"] = "semantic_scholar"
    return result


def _set_s2_ambiguous(result: dict, top: tuple[float, dict]) -> dict:
    sim, work = top
    result["status"] = "ambiguous"
    result["semantic_scholar_id"] = _s2_id_url(work)
    result["best_match"] = _build_s2_best_match(work)
    result["title_similarity"] = sim / 100.0
    result["match_source"] = "semantic_scholar"
    return result


# ---- Resolution ------------------------------------------------------------


def _resolve_openalex(
    client: httpx.Client, entry: dict, mailto: str | None
) -> dict:
    """Run only the OpenAlex resolution stage. Mutates and returns a fresh result dict."""
    result = _empty_result(entry)
    if entry["doi"]:
        work = _get_by_doi(client, entry["doi"], mailto)
        return _finalize_match(result, work, entry) if work else result

    if entry["arxiv_id"]:
        results = _search_works(
            client, f"arxiv {entry['arxiv_id']}", mailto, per_page=5
        )
        if not results and entry["title"]:
            results = _search_works(client, entry["title"], mailto)
        return _finalize_match(result, results[0], entry) if results else result

    if not entry["title"]:
        return result

    results = _search_works(client, entry["title"], mailto, per_page=5)
    scored = [
        (_title_similarity(entry["title"], _candidate_title(w)), w) for w in results
    ]
    scored = [(sim, w) for sim, w in scored if sim >= TITLE_SIMILARITY_THRESHOLD]
    scored.sort(key=lambda pair: pair[0], reverse=True)

    raw_year = entry["year"]
    author_matches = [
        (sim, w)
        for sim, w in scored
        if _author_surname_overlap(entry["authors"], _candidate_author_names(w))
    ]
    if len(author_matches) == 1:
        return _finalize_match(result, author_matches[0][1], entry)
    if len(author_matches) > 1:
        composite = sorted(
            author_matches,
            key=lambda pair: pair[0] + 5 * _year_match(raw_year, pair[1].get("publication_year")),
            reverse=True,
        )
        top_sim, top_work = composite[0]
        top_year_match = _year_match(raw_year, top_work.get("publication_year"))
        if top_sim >= 99 and top_year_match:
            return _finalize_match(result, top_work, entry)
        top_score = top_sim + 5 * top_year_match
        second_score = composite[1][0] + 5 * _year_match(
            raw_year, composite[1][1].get("publication_year")
        )
        if top_score > second_score:
            return _finalize_match(result, top_work, entry)
        return _set_ambiguous(result, author_matches[0])
    if len(scored) >= 2:
        composite = sorted(
            scored,
            key=lambda pair: (
                pair[0] + 5 * _year_match(raw_year, pair[1].get("publication_year"))
            ),
            reverse=True,
        )
        top_score = composite[0][0] + 5 * _year_match(
            raw_year, composite[0][1].get("publication_year")
        )
        second_score = composite[1][0] + 5 * _year_match(
            raw_year, composite[1][1].get("publication_year")
        )
        if top_score > second_score:
            return _finalize_match(result, composite[0][1], entry)
        return _set_ambiguous(result, scored[0])
    if len(scored) == 1:
        return _finalize_match(result, scored[0][1], entry)
    return result


def _resolve_s2(client: httpx.Client, entry: dict) -> dict:
    """Run only the Semantic Scholar resolution stage. Returns a fresh result dict."""
    result = _empty_result(entry)
    if entry["doi"]:
        work = _s2_get_by_doi(client, entry["doi"])
        return _finalize_s2_match(result, work, entry) if work else result

    if entry["arxiv_id"]:
        work = _s2_get_by_arxiv(client, entry["arxiv_id"])
        return _finalize_s2_match(result, work, entry) if work else result

    if not entry["title"]:
        return result

    results = _s2_search(client, entry["title"], per_page=5)
    scored = [
        (_title_similarity(entry["title"], _s2_candidate_title(w)), w) for w in results
    ]
    scored = [(sim, w) for sim, w in scored if sim >= TITLE_SIMILARITY_THRESHOLD]
    scored.sort(key=lambda pair: pair[0], reverse=True)

    if not scored:
        return result

    author_matches = [
        (sim, w)
        for sim, w in scored
        if _author_surname_overlap(entry["authors"], _s2_author_names(w))
    ]
    if len(author_matches) == 1:
        return _finalize_s2_match(result, author_matches[0][1], entry)
    if len(author_matches) > 1:
        top_sim, top_work = author_matches[0]
        if top_sim >= 99 and _year_match(entry["year"], top_work.get("year")):
            return _finalize_s2_match(result, top_work, entry)
        return _set_s2_ambiguous(result, author_matches[0])
    if len(scored) >= 2:
        return _set_s2_ambiguous(result, scored[0])
    return _finalize_s2_match(result, scored[0][1], entry)


def _s2_id_url(work: dict) -> str:
    return f"{S2_PAPER_URL_PREFIX}{work['paperId']}"


def _merge_secondary(primary: dict, secondary: dict) -> bool:
    """Merge ``secondary`` resolver result into ``primary`` in-place.

    Carries over the secondary's index id always (so both id fields are populated
    independently when both sources matched). Promotes ``primary`` to the
    secondary's outcome when the secondary has a strictly higher status priority.
    Returns True iff the merge raised the primary's status.
    """
    if secondary["openalex_id"]:
        primary["openalex_id"] = secondary["openalex_id"]
    if secondary["semantic_scholar_id"]:
        primary["semantic_scholar_id"] = secondary["semantic_scholar_id"]

    primary_priority = STATUS_PRIORITY[primary["status"]]
    secondary_priority = STATUS_PRIORITY[secondary["status"]]
    if secondary_priority > primary_priority:
        primary["status"] = secondary["status"]
        primary["match_source"] = secondary["match_source"]
        primary["mismatches"] = secondary["mismatches"]
        primary["best_match"] = secondary["best_match"]
        primary["title_similarity"] = secondary["title_similarity"]
        return True
    return False


def _format_error(exc: Exception) -> str:
    return f"{type(exc).__name__}: {exc}"


def resolve_entry(
    client: httpx.Client, entry: dict, mailto: str | None = None
) -> dict:
    """Resolve a single bib entry; never raises.

    Dispatch order:
      - **DOI present:** OpenAlex (`/works/doi:`) first, S2 (`/paper/DOI:`) fallback.
        Both endpoints are keyed lookups and not subject to search throttling.
      - **arXiv id present (no DOI):** S2 (`/paper/arXiv:`) first, OpenAlex
        search-based arxiv path as fallback.
      - **Title-only:** S2 search first, OpenAlex search as fallback.

    The secondary is consulted whenever the primary returns ``not_found``,
    ``ambiguous``, ``metadata_mismatch``, or raises. ``s2_consulted`` is True
    whenever S2 was called (whether as primary or as fallback). ``s2_lifted`` is
    True when the secondary raised the final status above what the primary
    alone would have returned.
    """
    if _should_skip(entry):
        result = _empty_result(entry)
        result["status"] = "skipped"
        return result

    primary_is_s2 = entry["doi"] is None

    primary_error: Exception | None = None
    try:
        if primary_is_s2:
            primary_result = _resolve_s2(client, entry)
        else:
            primary_result = _resolve_openalex(client, entry, mailto)
    except Exception as exc:
        primary_error = exc
        primary_result = _empty_result(entry)

    if primary_error is None and primary_result["status"] not in {
        "not_found", "ambiguous", "metadata_mismatch"
    }:
        if primary_is_s2:
            primary_result["s2_consulted"] = True
        return primary_result

    secondary_error: Exception | None = None
    secondary_result: dict | None = None
    try:
        if primary_is_s2:
            secondary_result = _resolve_openalex(client, entry, mailto)
        else:
            secondary_result = _resolve_s2(client, entry)
    except Exception as exc:
        secondary_error = exc

    if primary_error is not None and secondary_error is not None:
        result = _empty_result(entry)
        result["status"] = "error"
        s2_err = primary_error if primary_is_s2 else secondary_error
        oa_err = secondary_error if primary_is_s2 else primary_error
        result["error"] = (
            f"S2: {_format_error(s2_err)} | OpenAlex: {_format_error(oa_err)}"
        )
        result["s2_consulted"] = True
        return result

    if primary_error is not None:
        secondary_result["s2_consulted"] = True
        secondary_result["s2_lifted"] = True
        return secondary_result

    if secondary_error is not None:
        primary_result["s2_consulted"] = True
        return primary_result

    lifted = _merge_secondary(primary_result, secondary_result)
    primary_result["s2_consulted"] = True
    primary_result["s2_lifted"] = lifted
    return primary_result


# ---- Tarball + multi-bib handling ------------------------------------------


def _collect_bib_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.bib"))


def _extract_tarball(tarball: Path, dest: Path) -> None:
    with tarfile.open(tarball, "r:*") as tar:
        tar.extractall(dest, filter="data")


def _download_tarball(paper_id: str, dest: Path) -> Path:
    url = KOALA_TARBALL_TEMPLATE.format(paper_id=paper_id)
    out = dest / f"{paper_id}.tar.gz"
    with httpx.Client(timeout=60.0, follow_redirects=True) as client:
        with client.stream("GET", url) as resp:
            resp.raise_for_status()
            with out.open("wb") as fh:
                for chunk in resp.iter_bytes():
                    fh.write(chunk)
    return out


# ---- Top-level orchestration -----------------------------------------------


@dataclass
class _Counts:
    total: int = 0
    verified: int = 0
    mismatch: int = 0
    missing: int = 0
    ambiguous: int = 0
    error: int = 0
    skipped: int = 0
    s2_consulted: int = 0
    s2_lifted: int = 0

    def add(self, result: dict) -> None:
        self.total += 1
        status = result["status"]
        if status == "verified":
            self.verified += 1
        elif status == "metadata_mismatch":
            self.mismatch += 1
        elif status == "not_found":
            self.missing += 1
        elif status == "ambiguous":
            self.ambiguous += 1
        elif status == "error":
            self.error += 1
        elif status == "skipped":
            self.skipped += 1
        if result.get("s2_consulted"):
            self.s2_consulted += 1
        if result.get("s2_lifted"):
            self.s2_lifted += 1


def _strip_internal_fields(result: dict) -> dict:
    out = dict(result)
    out.pop("s2_consulted", None)
    out.pop("s2_lifted", None)
    return out


def verify_bib_files(
    bib_paths: list[Path], mailto: str | None, paper_id: str | None
) -> dict:
    entries: list[dict] = []
    for path in bib_paths:
        entries.extend(parse_bib_file(path))
    counts = _Counts()
    results: list[dict] = []
    with httpx.Client() as client:
        for entry in entries:
            res = resolve_entry(client, entry, mailto=mailto)
            counts.add(res)
            results.append(_strip_internal_fields(res))
            if res["status"] != "skipped":
                time.sleep(POLITE_SLEEP_SECONDS)
    return {
        "paper_id": paper_id,
        "total": counts.total,
        "verified": counts.verified,
        "mismatch": counts.mismatch,
        "missing": counts.missing,
        "ambiguous": counts.ambiguous,
        "error": counts.error,
        "skipped": counts.skipped,
        "s2_consulted": counts.s2_consulted,
        "s2_lifted": counts.s2_lifted,
        "key_style_outliers": _key_style_outliers(entries),
        "entries": results,
    }


# ---- CLI -------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="verify_citations",
        description="Resolve a paper's bibliography against Semantic Scholar (with OpenAlex fallback).",
    )
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--paper-id", help="Koala paper UUID")
    src.add_argument("--tarball", help="Path to local paper tarball")
    src.add_argument("--bibfile", help="Path to a single .bib file")
    p.add_argument("--out", help="Write JSON report here (default: stdout)")
    p.add_argument(
        "--openalex-mailto",
        default=os.environ.get("OPENALEX_MAILTO"),
        help="Email passed via ?mailto= to OpenAlex (polite pool).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.bibfile:
        bib_paths = [Path(args.bibfile)]
        if not bib_paths[0].exists():
            print(f"bibfile not found: {bib_paths[0]}", file=sys.stderr)
            return 2
        report = verify_bib_files(bib_paths, args.openalex_mailto, paper_id=None)
    elif args.tarball:
        tarball = Path(args.tarball)
        if not tarball.exists():
            print(f"tarball not found: {tarball}", file=sys.stderr)
            return 2
        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            _extract_tarball(tarball, tdp)
            bibs = _collect_bib_files(tdp)
            if not bibs:
                print(
                    f"No .bib files in tarball {tarball}. "
                    "PDF-only papers are out of scope for v1.",
                    file=sys.stderr,
                )
                return 3
            report = verify_bib_files(bibs, args.openalex_mailto, paper_id=None)
    else:
        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            try:
                tar_path = _download_tarball(args.paper_id, tdp)
            except httpx.HTTPError as exc:
                print(
                    f"Failed to download tarball for {args.paper_id}: {exc}",
                    file=sys.stderr,
                )
                return 4
            extracted = tdp / "extracted"
            extracted.mkdir()
            _extract_tarball(tar_path, extracted)
            bibs = _collect_bib_files(extracted)
            if not bibs:
                print(
                    f"No .bib files in tarball for paper {args.paper_id}. "
                    "PDF-only papers are out of scope for v1.",
                    file=sys.stderr,
                )
                return 3
            report = verify_bib_files(
                bibs, args.openalex_mailto, paper_id=args.paper_id
            )

    payload = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
