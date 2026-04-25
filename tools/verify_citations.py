"""Resolve every BibTeX entry in a paper against OpenAlex."""
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
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import bibtexparser
import httpx
from rapidfuzz import fuzz


OPENALEX_BASE = "https://api.openalex.org"
KOALA_TARBALL_TEMPLATE = "https://koala.science/storage/tarballs/{paper_id}.tar.gz"
TITLE_SIMILARITY_THRESHOLD = 90
POLITE_SLEEP_SECONDS = 0.1
ARXIV_RE = re.compile(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", re.IGNORECASE)


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
        title = re.sub(r"[{}]", "", title_raw).strip() if title_raw else ""
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
            }
        )
    return out


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


def _title_similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return float(fuzz.token_set_ratio(a, b))


def _classify_against_candidate(
    raw: dict, candidate: dict
) -> tuple[str, list[str]]:
    mismatches: list[str] = []
    raw_year = raw["year"]
    cand_year = candidate.get("publication_year")
    if raw_year and cand_year and abs(int(raw_year) - int(cand_year)) > 1:
        mismatches.append("year")
    if not _author_surname_overlap(raw["authors"], _candidate_author_names(candidate)):
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
    return result


def _set_ambiguous(result: dict, top: tuple[float, dict]) -> dict:
    sim, work = top
    result["status"] = "ambiguous"
    result["openalex_id"] = work.get("id")
    result["best_match"] = _build_best_match(work)
    result["title_similarity"] = sim / 100.0
    return result


# ---- Resolution ------------------------------------------------------------


def resolve_entry(
    client: httpx.Client, entry: dict, mailto: str | None = None
) -> dict:
    """Resolve a single bib entry to OpenAlex; never raises."""
    result = _empty_result(entry)
    try:
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

        author_matches = [
            (sim, w)
            for sim, w in scored
            if _author_surname_overlap(entry["authors"], _candidate_author_names(w))
        ]
        if len(author_matches) == 1:
            return _finalize_match(result, author_matches[0][1], entry)
        if author_matches:
            return _set_ambiguous(result, author_matches[0])
        if len(scored) >= 2:
            return _set_ambiguous(result, scored[0])
        if len(scored) == 1:
            return _finalize_match(result, scored[0][1], entry)
        return result
    except Exception as exc:
        result["status"] = "error"
        result["error"] = f"{type(exc).__name__}: {exc}"
        return result


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

    def add(self, status: str) -> None:
        self.total += 1
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
            counts.add(res["status"])
            results.append(res)
            time.sleep(POLITE_SLEEP_SECONDS)
    return {
        "paper_id": paper_id,
        "total": counts.total,
        "verified": counts.verified,
        "mismatch": counts.mismatch,
        "missing": counts.missing,
        "ambiguous": counts.ambiguous,
        "error": counts.error,
        "entries": results,
    }


# ---- CLI -------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="verify_citations",
        description="Resolve a paper's bibliography against OpenAlex.",
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
