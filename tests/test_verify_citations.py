"""Tests for tools/verify_citations.py — citation verification CLI/module."""
from __future__ import annotations

import json
import re
from pathlib import Path

import httpx
import pytest

import verify_citations as vc

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(autouse=True)
def _no_rate_limit_sleeps(monkeypatch):
    monkeypatch.setattr(vc, "POLITE_SLEEP_SECONDS", 0.0)
    monkeypatch.setattr(vc, "S2_SLEEP_AUTH", 0.0)
    monkeypatch.setattr(vc, "S2_SLEEP_UNAUTH", 0.0)
    monkeypatch.setattr(vc, "S2_BACKOFF_BASE", 0.0)
    monkeypatch.delenv("SEMANTIC_SCHOLAR_API_KEY", raising=False)


# ---------------------------------------------------------------------------
# parse_bib
# ---------------------------------------------------------------------------


def test_parse_bib_normalizes_internal_whitespace(tmp_path):
    bib = tmp_path / "x.bib"
    bib.write_text(
        "@article{multiline,\n"
        "  title = {Refine Drugs: Uniform-Source Discrete Flows\n"
        "                  for Fragment-Based Drug Discovery},\n"
        "  author = {Smith, J.},\n"
        "  year = {2025}\n"
        "}\n"
    )
    entries = vc.parse_bib_file(bib)
    assert (
        entries[0]["title"]
        == "Refine Drugs: Uniform-Source Discrete Flows for Fragment-Based Drug Discovery"
    )


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
# resolution by DOI: OpenAlex stays primary
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
    assert result["semantic_scholar_id"] is None
    assert result["match_source"] == "openalex"


# ---------------------------------------------------------------------------
# resolution by arXiv id: S2 is primary
# ---------------------------------------------------------------------------


def test_resolve_by_arxiv(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/arXiv:2103\.00001.*$"),
        json={
            "paperId": "s2arxiv1",
            "title": "Arxiv Paper",
            "year": 2021,
            "authors": [{"name": "B. Beta"}],
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
    assert result["semantic_scholar_id"] == "https://www.semanticscholar.org/paper/s2arxiv1"
    assert result["openalex_id"] is None
    assert result["match_source"] == "semantic_scholar"


# ---------------------------------------------------------------------------
# resolution by title + author: S2 is primary
# ---------------------------------------------------------------------------


def test_resolve_by_title_match(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={
            "total": 1,
            "offset": 0,
            "data": [
                {
                    "paperId": "s2title7",
                    "title": "Title Only Paper",
                    "year": 2019,
                    "authors": [
                        {"name": "C. Gamma"},
                        {"name": "D. Delta"},
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
    assert result["semantic_scholar_id"] == "https://www.semanticscholar.org/paper/s2title7"
    assert result["title_similarity"] >= 0.9
    assert result["openalex_id"] is None
    assert result["match_source"] == "semantic_scholar"


# ---------------------------------------------------------------------------
# year off by two -> metadata_mismatch (S2 primary, OpenAlex confirms same)
# ---------------------------------------------------------------------------


def test_resolve_title_year_off_by_two(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={
            "total": 1,
            "offset": 0,
            "data": [
                {
                    "paperId": "s2offyear",
                    "title": "Off By Two Years Sample Paper",
                    "year": 2020,
                    "authors": [{"name": "Hana Kim"}],
                }
            ],
        },
    )
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={"meta": {"count": 0}, "results": []},
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
    assert result["match_source"] == "semantic_scholar"


# ---------------------------------------------------------------------------
# no match -> not_found (both miss)
# ---------------------------------------------------------------------------


def test_resolve_no_match(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={"total": 0, "offset": 0, "data": []},
    )
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
    assert result["semantic_scholar_id"] is None
    assert result["match_source"] is None


# ---------------------------------------------------------------------------
# ambiguous: two candidates >= 0.9 with different authors (S2 returns ambiguous,
# OpenAlex also returns ambiguous -> stays ambiguous)
# ---------------------------------------------------------------------------


def test_resolve_ambiguous(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={
            "total": 2,
            "offset": 0,
            "data": [
                {
                    "paperId": "s2amb1",
                    "title": "Common Title Phrase Here",
                    "year": 2020,
                    "authors": [{"name": "Different Author One"}],
                },
                {
                    "paperId": "s2amb2",
                    "title": "Common Title Phrase Here",
                    "year": 2021,
                    "authors": [{"name": "Different Author Two"}],
                },
            ],
        },
    )
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
# network error -> status: error, both sources raise
# ---------------------------------------------------------------------------


def test_resolve_network_error(httpx_mock):
    httpx_mock.add_exception(
        httpx.ConnectError("s2 boom"),
        url=re.compile(r"^https://api\.semanticscholar\.org/.*$"),
    )
    httpx_mock.add_exception(
        httpx.ConnectError("openalex boom"),
        url=re.compile(r"^https://api\.openalex\.org/.*$"),
    )
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
    assert "S2:" in result["error"]
    assert "OpenAlex:" in result["error"]
    assert "s2 boom" in result["error"]
    assert "openalex boom" in result["error"]


# ---------------------------------------------------------------------------
# Single author-surname overlap picks the matching candidate (S2 primary path)
# ---------------------------------------------------------------------------


def test_single_author_overlap_picks_match(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={
            "total": 2,
            "offset": 0,
            "data": [
                {
                    "paperId": "s2match",
                    "title": "Common Title Phrase Here",
                    "year": 2020,
                    "authors": [{"name": "Z. Smith"}],
                },
                {
                    "paperId": "s2off",
                    "title": "Common Title Phrase Here",
                    "year": 2017,
                    "authors": [{"name": "Different Author"}],
                },
            ],
        },
    )
    entry = {
        "key": "overlap",
        "title": "Common Title Phrase Here",
        "authors": ["Smith, Z."],
        "year": 2020,
        "doi": None,
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "verified"
    assert result["semantic_scholar_id"] == "https://www.semanticscholar.org/paper/s2match"
    assert result["match_source"] == "semantic_scholar"


# ---------------------------------------------------------------------------
# S2 lifts a not_found OpenAlex result (DOI path: OpenAlex first, S2 fallback)
# ---------------------------------------------------------------------------


def test_s2_lifts_not_found(httpx_mock):
    httpx_mock.add_response(
        url="https://api.openalex.org/works/doi:10.1000/missing",
        status_code=404,
        json={"error": "not found"},
    )
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/DOI:.*$"),
        json={
            "paperId": "abc123",
            "title": "A Real Lurking Paper",
            "year": 2022,
            "authors": [{"name": "Jane Lurker"}],
        },
    )
    entry = {
        "key": "lurker",
        "title": "A Real Lurking Paper",
        "authors": ["Lurker, Jane"],
        "year": 2022,
        "doi": "10.1000/missing",
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "verified"
    assert result["match_source"] == "semantic_scholar"
    assert result["semantic_scholar_id"] == "https://www.semanticscholar.org/paper/abc123"
    assert result["openalex_id"] is None
    assert result["best_match"]["title"] == "A Real Lurking Paper"


# ---------------------------------------------------------------------------
# OpenAlex lifts an S2 not_found via title search (symmetric to s2_lifts_not_found)
# ---------------------------------------------------------------------------


def test_openalex_lifts_s2_not_found(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={"total": 0, "offset": 0, "data": []},
    )
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={
            "meta": {"count": 1},
            "results": [
                {
                    "id": "https://openalex.org/W_lurker",
                    "display_name": "Another Real Lurking Paper",
                    "title": "Another Real Lurking Paper",
                    "publication_year": 2022,
                    "authorships": [
                        {"author": {"display_name": "Jane Lurker"}},
                    ],
                }
            ],
        },
    )
    entry = {
        "key": "lurker2",
        "title": "Another Real Lurking Paper",
        "authors": ["Lurker, Jane"],
        "year": 2022,
        "doi": None,
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "verified"
    assert result["match_source"] == "openalex"
    assert result["openalex_id"] == "https://openalex.org/W_lurker"
    assert result["semantic_scholar_id"] is None
    assert result["best_match"]["title"] == "Another Real Lurking Paper"


# ---------------------------------------------------------------------------
# OpenAlex lifts an S2 ambiguous result to verified (symmetric to
# s2_lifts_ambiguous_to_verified)
# ---------------------------------------------------------------------------


def test_openalex_lifts_s2_ambiguous(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={
            "total": 2,
            "offset": 0,
            "data": [
                {
                    "paperId": "s2amb_a",
                    "title": "Shared Title Across Two Works",
                    "year": 2020,
                    "authors": [{"name": "Different Author One"}],
                },
                {
                    "paperId": "s2amb_b",
                    "title": "Shared Title Across Two Works",
                    "year": 2020,
                    "authors": [{"name": "Different Author Two"}],
                },
            ],
        },
    )
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={
            "meta": {"count": 1},
            "results": [
                {
                    "id": "https://openalex.org/W_unique",
                    "display_name": "Shared Title Across Two Works",
                    "title": "Shared Title Across Two Works",
                    "publication_year": 2020,
                    "authorships": [{"author": {"display_name": "John Smith"}}],
                }
            ],
        },
    )
    entry = {
        "key": "ambs2flip",
        "title": "Shared Title Across Two Works",
        "authors": ["Smith, John"],
        "year": 2020,
        "doi": None,
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "verified"
    assert result["match_source"] == "openalex"
    assert result["openalex_id"] == "https://openalex.org/W_unique"


# ---------------------------------------------------------------------------
# S2 lifts an ambiguous OpenAlex result to verified (DOI path; OpenAlex 404
# means the entry advances to S2 which finds a clean DOI match).
# ---------------------------------------------------------------------------


def test_s2_lifts_ambiguous_to_verified(httpx_mock):
    httpx_mock.add_response(
        url="https://api.openalex.org/works/doi:10.1000/lift",
        status_code=404,
        json={"error": "not found"},
    )
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/DOI:.*$"),
        json={
            "paperId": "s2id999",
            "title": "Shared Title Across Two Works",
            "year": 2020,
            "authors": [{"name": "John Smith"}],
        },
    )
    entry = {
        "key": "ambs2",
        "title": "Shared Title Across Two Works",
        "authors": ["Smith, John"],
        "year": 2020,
        "doi": "10.1000/lift",
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "verified"
    assert result["match_source"] == "semantic_scholar"
    assert result["semantic_scholar_id"] == "https://www.semanticscholar.org/paper/s2id999"


# ---------------------------------------------------------------------------
# S2 also misses -> stays not_found (title-only path)
# ---------------------------------------------------------------------------


def test_s2_also_not_found(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={"total": 0, "offset": 0, "data": []},
    )
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={"meta": {"count": 0}, "results": []},
    )
    entry = {
        "key": "fab2",
        "title": "Truly Fabricated Title Nowhere To Be Found",
        "authors": ["Nobody, Nada"],
        "year": 2099,
        "doi": None,
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "not_found"
    assert result["openalex_id"] is None
    assert result["semantic_scholar_id"] is None
    assert result["match_source"] is None


# ---------------------------------------------------------------------------
# OpenAlex is skipped when S2 verifies cleanly (mirror of the old
# test_s2_skipped_when_openalex_verified, with the flip)
# ---------------------------------------------------------------------------


def test_openalex_skipped_when_s2_verified(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={
            "total": 1,
            "offset": 0,
            "data": [
                {
                    "paperId": "clean1",
                    "title": "Clean Match Paper",
                    "year": 2020,
                    "authors": [{"name": "A. Alpha"}],
                }
            ],
        },
    )
    entry = {
        "key": "clean",
        "title": "Clean Match Paper",
        "authors": ["Alpha, A."],
        "year": 2020,
        "doi": None,
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "verified"
    assert result["match_source"] == "semantic_scholar"
    openalex_calls = [
        r for r in httpx_mock.get_requests()
        if "api.openalex.org" in str(r.url)
    ]
    assert openalex_calls == []


# ---------------------------------------------------------------------------
# OpenAlex is called when S2 raises an exception (title-only path)
# ---------------------------------------------------------------------------


def test_openalex_called_when_s2_raises(httpx_mock):
    httpx_mock.add_exception(
        httpx.ConnectError("s2 boom"),
        url=re.compile(r"^https://api\.semanticscholar\.org/.*$"),
    )
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={
            "meta": {"count": 1},
            "results": [
                {
                    "id": "https://openalex.org/W_fallback",
                    "display_name": "Fallback Paper",
                    "title": "Fallback Paper",
                    "publication_year": 2022,
                    "authorships": [
                        {"author": {"display_name": "Fallback Author"}},
                    ],
                }
            ],
        },
    )
    entry = {
        "key": "fallback",
        "title": "Fallback Paper",
        "authors": ["Author, Fallback"],
        "year": 2022,
        "doi": None,
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "verified"
    assert result["match_source"] == "openalex"
    assert result["openalex_id"] == "https://openalex.org/W_fallback"
    assert result["s2_consulted"] is True


# ---------------------------------------------------------------------------
# end-to-end CLI smoke against the bundled sample.bib fixture.
# All three entries are title-only -> S2 is consulted first for each.
# Verifiable entry resolves via S2; not_found and metadata_mismatch entries
# fall through to OpenAlex.
# ---------------------------------------------------------------------------


def test_cli_main_bibfile_smoke(httpx_mock, tmp_path):
    httpx_mock.add_response(
        url=re.compile(
            r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*query=Resolvable\+Sample\+Paper\+on\+Things.*$"
        ),
        json={
            "total": 1,
            "offset": 0,
            "data": [
                {
                    "paperId": "s2_resolvable",
                    "title": "Resolvable Sample Paper on Things",
                    "year": 2020,
                    "authors": [
                        {"name": "Alice Smith"},
                        {"name": "Bob Jones"},
                    ],
                }
            ],
        },
    )
    httpx_mock.add_response(
        url=re.compile(
            r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*query=A\+Wholly\+Fabricated\+Title.*$"
        ),
        json={"total": 0, "offset": 0, "data": []},
    )
    httpx_mock.add_response(
        url=re.compile(
            r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*query=Off\+By\+Two\+Years\+Sample\+Paper.*$"
        ),
        json={
            "total": 1,
            "offset": 0,
            "data": [
                {
                    "paperId": "s2_wrongyear",
                    "title": "Off By Two Years Sample Paper",
                    "year": 2020,
                    "authors": [{"name": "Hana Kim"}],
                }
            ],
        },
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
    assert summary["s2_consulted"] == 3
    assert summary["s2_lifted"] == 0


# ---------------------------------------------------------------------------
# S2 rate-limit retry: 429 → backoff → success
# ---------------------------------------------------------------------------


def test_s2_retries_on_429(httpx_mock):
    url_re = re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/DOI:.*$")
    httpx_mock.add_response(url=url_re, status_code=429)
    httpx_mock.add_response(url=url_re, status_code=429)
    httpx_mock.add_response(
        url=url_re,
        json={
            "paperId": "abc123",
            "title": "Recovered Paper",
            "year": 2022,
            "authors": [{"name": "Some Author"}],
        },
    )
    with httpx.Client() as client:
        result = vc._s2_get_by_doi(client, "10.1/x")
    assert result["paperId"] == "abc123"
    assert len(httpx_mock.get_requests()) == 3


def test_title_similarity_is_case_insensitive():
    assert vc._title_similarity("Gpt-4 technical report", "GPT-4 Technical Report") >= 99.0


def test_title_similarity_normalizes_camelcase():
    assert vc._title_similarity("SocialIQa: Reasoning", "Social IQa: Reasoning") >= 99.0
    assert vc._title_similarity("SlimPajama dataset", "Slim Pajama dataset") >= 99.0
    # Acronyms inside CamelCase split symmetrically; equal inputs still match.
    assert vc._title_similarity("IoT survey", "IoT survey") >= 99.0


# ---------------------------------------------------------------------------
# Skip rule: non-academic entries don't query any API
# ---------------------------------------------------------------------------


def test_skip_dataset_entry_type(httpx_mock, tmp_path):
    bib = tmp_path / "x.bib"
    bib.write_text(
        '@dataset{kaggle1, title={Some Data}, author={X}, year={2021},\n'
        ' publisher={Kaggle}, url={https://kaggle.com/x}}\n'
    )
    entries = vc.parse_bib_file(bib)
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entries[0])
    assert result["status"] == "skipped"
    assert len(httpx_mock.get_requests()) == 0


def test_skip_news_journal(httpx_mock, tmp_path):
    bib = tmp_path / "x.bib"
    bib.write_text(
        '@article{nyt1, title={Big Story}, author={Reporter, A.}, year={2023},\n'
        ' journal={The New York Times}}\n'
    )
    entries = vc.parse_bib_file(bib)
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entries[0])
    assert result["status"] == "skipped"
    assert len(httpx_mock.get_requests()) == 0


def test_skip_url_only(httpx_mock, tmp_path):
    bib = tmp_path / "x.bib"
    bib.write_text(
        '@misc{webpost, title={Some Post}, author={Person, B.}, year={2024},\n'
        ' url={https://example.com/post}}\n'
    )
    entries = vc.parse_bib_file(bib)
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entries[0])
    assert result["status"] == "skipped"


def test_misc_with_arxiv_not_skipped(httpx_mock, tmp_path):
    """@misc is commonly used for arXiv preprints — must not be skipped."""
    bib = tmp_path / "x.bib"
    bib.write_text(
        '@misc{preprint, title={Real Paper}, author={Author, C.}, year={2024},\n'
        ' eprint={2401.12345}, archivePrefix={arXiv}}\n'
    )
    entries = vc.parse_bib_file(bib)
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/arXiv:2401\.12345.*$"),
        json={
            "paperId": "s2arxiv2401",
            "title": "Real Paper",
            "year": 2024,
            "authors": [{"name": "C. Author"}],
        },
    )
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entries[0])
    assert result["status"] == "verified"


# ---------------------------------------------------------------------------
# Bib-key style outlier detection
# ---------------------------------------------------------------------------


def test_key_style_outliers_with_dominant_4digit():
    entries = [
        {"key": f"author{2020+i}foo", "title": "x", "authors": [], "year": 2020,
         "doi": None, "arxiv_id": None} for i in range(10)
    ]
    entries += [
        {"key": "xia23short", "title": "x", "authors": [], "year": 2023,
         "doi": None, "arxiv_id": None},
        {"key": "kim23bild", "title": "x", "authors": [], "year": 2023,
         "doi": None, "arxiv_id": None},
    ]
    outliers = vc._key_style_outliers(entries)
    assert set(outliers) == {"xia23short", "kim23bild"}


def test_key_style_outliers_no_dominant_pattern():
    entries = [
        {"key": "a23", "title": "x", "authors": [], "year": 2023,
         "doi": None, "arxiv_id": None},
        {"key": "b2024", "title": "x", "authors": [], "year": 2024,
         "doi": None, "arxiv_id": None},
        {"key": "c2024", "title": "x", "authors": [], "year": 2024,
         "doi": None, "arxiv_id": None},
    ]
    assert vc._key_style_outliers(entries) == []


def test_resolve_case_mismatch_still_verifies(httpx_mock):
    """Bib lowercases title (e.g. 'Gpt-4'), source has canonical case ('GPT-4').
    Must still resolve to verified. With S2 primary, S2 alone produces the match."""
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={
            "total": 1,
            "offset": 0,
            "data": [
                {
                    "paperId": "abc",
                    "title": "GPT-4 Technical Report",
                    "year": 2023,
                    "authors": [{"name": "Josh Achiam"}],
                }
            ],
        },
    )
    entry = {
        "key": "achiam2023gpt",
        "title": "Gpt-4 technical report",
        "authors": ["Achiam, Josh"],
        "year": 2023,
        "doi": None,
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "verified"
    assert result["match_source"] == "semantic_scholar"


def test_duplicate_records_resolve_to_verified(httpx_mock):
    """Catalog duplicates (two records, identical title+year, both author-matched)
    should resolve to verified, not ambiguous. With S2 primary, exercise the S2
    duplicate-detection path."""
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={
            "total": 2,
            "offset": 0,
            "data": [
                {
                    "paperId": "s2dup_a",
                    "title": "Discrete Flow Matching",
                    "year": 2024,
                    "authors": [{"name": "Itai Gat"}],
                },
                {
                    "paperId": "s2dup_b",
                    "title": "Discrete Flow Matching",
                    "year": 2024,
                    "authors": [{"name": "Itai Gat"}],
                },
            ],
        },
    )
    entry = {
        "key": "DFM",
        "title": "Discrete Flow Matching",
        "authors": ["Gat, Itai"],
        "year": 2024,
        "doi": None,
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "verified"
    assert result["semantic_scholar_id"] == "https://www.semanticscholar.org/paper/s2dup_a"


def test_s2_sends_api_key_header(httpx_mock, monkeypatch):
    monkeypatch.setenv("SEMANTIC_SCHOLAR_API_KEY", "test-key-xyz")
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/DOI:.*$"),
        json={"paperId": "p1", "title": "T", "year": 2020, "authors": []},
    )
    with httpx.Client() as client:
        vc._s2_get_by_doi(client, "10.1/x")
    requests = httpx_mock.get_requests()
    assert requests[0].headers.get("x-api-key") == "test-key-xyz"
