"""Tests for tools/verify_citations.py — citation verification CLI/module."""
from __future__ import annotations

import json
import re
from pathlib import Path

import httpx

import verify_citations as vc

FIXTURES = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# parse_bib
# ---------------------------------------------------------------------------


def test_parse_bib_basic(tmp_path):
    bib = tmp_path / "x.bib"
    bib.write_text(
        """@article{withdoi,
  title = {Doi Paper},
  author = {Alpha, A.},
  year = {2020},
  doi = {10.1000/xyz}
}
@inproceedings{witharxiv,
  title = {Arxiv Paper},
  author = {Beta, B.},
  year = {2021},
  eprint = {2103.00001},
  archivePrefix = {arXiv}
}
@article{titleonly,
  title = {Title Only Paper},
  author = {Gamma, C. and Delta, D.},
  year = {2019}
}
"""
    )
    entries = vc.parse_bib_file(bib)
    assert len(entries) == 3
    by_key = {e["key"]: e for e in entries}
    assert by_key["withdoi"]["doi"] == "10.1000/xyz"
    assert by_key["witharxiv"]["arxiv_id"] == "2103.00001"
    assert by_key["titleonly"]["doi"] is None
    assert by_key["titleonly"]["arxiv_id"] is None
    assert by_key["titleonly"]["title"] == "Title Only Paper"
    assert by_key["titleonly"]["authors"] == ["Gamma, C.", "Delta, D."]
    assert by_key["titleonly"]["year"] == 2019


# ---------------------------------------------------------------------------
# resolution by DOI
# ---------------------------------------------------------------------------


def test_resolve_by_doi(httpx_mock):
    httpx_mock.add_response(
        url="https://api.openalex.org/works/doi:10.1000/xyz",
        json={
            "id": "https://openalex.org/W9",
            "display_name": "Doi Paper",
            "title": "Doi Paper",
            "publication_year": 2020,
            "authorships": [{"author": {"display_name": "A. Alpha"}}],
        },
    )
    entry = {
        "key": "withdoi",
        "title": "Doi Paper",
        "authors": ["Alpha, A."],
        "year": 2020,
        "doi": "10.1000/xyz",
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "verified"
    assert result["openalex_id"] == "https://openalex.org/W9"
    assert result["best_match"]["year"] == 2020


# ---------------------------------------------------------------------------
# resolution by arXiv id
# ---------------------------------------------------------------------------


def test_resolve_by_arxiv(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*search=arxiv\+2103\.00001.*$"),
        json={
            "meta": {"count": 1},
            "results": [
                {
                    "id": "https://openalex.org/W42",
                    "display_name": "Arxiv Paper",
                    "title": "Arxiv Paper",
                    "publication_year": 2021,
                    "authorships": [{"author": {"display_name": "B. Beta"}}],
                }
            ],
        },
    )
    entry = {
        "key": "witharxiv",
        "title": "Arxiv Paper",
        "authors": ["Beta, B."],
        "year": 2021,
        "doi": None,
        "arxiv_id": "2103.00001",
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "verified"
    assert result["openalex_id"] == "https://openalex.org/W42"


# ---------------------------------------------------------------------------
# resolution by title + author
# ---------------------------------------------------------------------------


def test_resolve_by_title_match(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={
            "meta": {"count": 1},
            "results": [
                {
                    "id": "https://openalex.org/W7",
                    "display_name": "Title Only Paper",
                    "title": "Title Only Paper",
                    "publication_year": 2019,
                    "authorships": [
                        {"author": {"display_name": "C. Gamma"}},
                        {"author": {"display_name": "D. Delta"}},
                    ],
                }
            ],
        },
    )
    entry = {
        "key": "titleonly",
        "title": "Title Only Paper",
        "authors": ["Gamma, C.", "Delta, D."],
        "year": 2019,
        "doi": None,
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "verified"
    assert result["openalex_id"] == "https://openalex.org/W7"
    assert result["title_similarity"] >= 0.9


# ---------------------------------------------------------------------------
# year off by two -> metadata_mismatch
# ---------------------------------------------------------------------------


def test_resolve_title_year_off_by_two(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={
            "meta": {"count": 1},
            "results": [
                {
                    "id": "https://openalex.org/W11",
                    "display_name": "Off By Two Years Sample Paper",
                    "title": "Off By Two Years Sample Paper",
                    "publication_year": 2020,
                    "authorships": [{"author": {"display_name": "Hana Kim"}}],
                }
            ],
        },
    )
    entry = {
        "key": "kim2018wrongyear",
        "title": "Off By Two Years Sample Paper",
        "authors": ["Kim, Hana"],
        "year": 2018,
        "doi": None,
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "metadata_mismatch"
    assert "year" in result["mismatches"]


# ---------------------------------------------------------------------------
# no match -> not_found
# ---------------------------------------------------------------------------


def test_resolve_no_match(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={"meta": {"count": 0}, "results": []},
    )
    entry = {
        "key": "fab",
        "title": "A Wholly Fabricated Title That Does Not Exist Anywhere",
        "authors": ["Nguyen, Imaginary"],
        "year": 2099,
        "doi": None,
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "not_found"
    assert result["openalex_id"] is None


# ---------------------------------------------------------------------------
# ambiguous: two candidates >= 0.9 with different authors
# ---------------------------------------------------------------------------


def test_resolve_ambiguous(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={
            "meta": {"count": 2},
            "results": [
                {
                    "id": "https://openalex.org/W1",
                    "display_name": "Common Title Phrase Here",
                    "title": "Common Title Phrase Here",
                    "publication_year": 2020,
                    "authorships": [
                        {"author": {"display_name": "Different Author One"}}
                    ],
                },
                {
                    "id": "https://openalex.org/W2",
                    "display_name": "Common Title Phrase Here",
                    "title": "Common Title Phrase Here",
                    "publication_year": 2021,
                    "authorships": [
                        {"author": {"display_name": "Different Author Two"}}
                    ],
                },
            ],
        },
    )
    entry = {
        "key": "amb",
        "title": "Common Title Phrase Here",
        "authors": ["Smith, Z."],
        "year": 2020,
        "doi": None,
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "ambiguous"


# ---------------------------------------------------------------------------
# network error -> status: error, no crash
# ---------------------------------------------------------------------------


def test_resolve_network_error(httpx_mock):
    httpx_mock.add_exception(httpx.ConnectError("boom"))
    entry = {
        "key": "neterr",
        "title": "Some Paper",
        "authors": ["Doe, J."],
        "year": 2020,
        "doi": None,
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "error"
    assert result["error"]


# ---------------------------------------------------------------------------
# end-to-end CLI smoke against the bundled sample.bib fixture
# ---------------------------------------------------------------------------


def test_cli_main_bibfile_smoke(httpx_mock, tmp_path, monkeypatch):
    monkeypatch.setattr(vc, "POLITE_SLEEP_SECONDS", 0.0)

    httpx_mock.add_response(
        url=re.compile(
            r"^https://api\.openalex\.org/works\?.*search=Resolvable\+Sample\+Paper\+on\+Things.*$"
        ),
        json=json.loads((FIXTURES / "openalex_resolvable.json").read_text()),
    )
    httpx_mock.add_response(
        url=re.compile(
            r"^https://api\.openalex\.org/works\?.*search=A\+Wholly\+Fabricated\+Title.*$"
        ),
        json=json.loads((FIXTURES / "openalex_empty.json").read_text()),
    )
    httpx_mock.add_response(
        url=re.compile(
            r"^https://api\.openalex\.org/works\?.*search=Off\+By\+Two\+Years\+Sample\+Paper.*$"
        ),
        json=json.loads((FIXTURES / "openalex_wrongyear.json").read_text()),
    )

    out = tmp_path / "report.json"
    rc = vc.main([
        "--bibfile",
        str(FIXTURES / "sample.bib"),
        "--out",
        str(out),
    ])
    assert rc == 0
    summary = json.loads(out.read_text())
    assert summary["total"] == 3
    assert summary["verified"] == 1
    assert summary["missing"] == 1
    assert summary["mismatch"] == 1
