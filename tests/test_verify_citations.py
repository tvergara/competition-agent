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
    assert result["semantic_scholar_id"] is None
    assert result["match_source"] == "openalex"


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
    assert result["semantic_scholar_id"] is None
    assert result["match_source"] == "openalex"


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
    assert result["semantic_scholar_id"] is None
    assert result["match_source"] == "openalex"


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
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={"total": 0, "offset": 0, "data": []},
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
    assert result["match_source"] == "openalex"


# ---------------------------------------------------------------------------
# no match -> not_found
# ---------------------------------------------------------------------------


def test_resolve_no_match(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={"meta": {"count": 0}, "results": []},
    )
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={"total": 0, "offset": 0, "data": []},
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
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={"total": 0, "offset": 0, "data": []},
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
# disambiguator year tiebreak: two ≥90 candidates, one has matching year
# ---------------------------------------------------------------------------


def test_disambiguator_year_tiebreak(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={
            "meta": {"count": 2},
            "results": [
                {
                    "id": "https://openalex.org/W_match",
                    "display_name": "Common Title Phrase Here",
                    "title": "Common Title Phrase Here",
                    "publication_year": 2020,
                    "authorships": [
                        {"author": {"display_name": "Z. Smith"}}
                    ],
                },
                {
                    "id": "https://openalex.org/W_off",
                    "display_name": "Common Title Phrase Here",
                    "title": "Common Title Phrase Here",
                    "publication_year": 2017,
                    "authorships": [
                        {"author": {"display_name": "Smith Different"}}
                    ],
                },
            ],
        },
    )
    entry = {
        "key": "tiebreak",
        "title": "Common Title Phrase Here",
        "authors": ["Smith, Z."],
        "year": 2020,
        "doi": None,
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "verified"
    assert result["openalex_id"] == "https://openalex.org/W_match"
    assert result["match_source"] == "openalex"


# ---------------------------------------------------------------------------
# S2 lifts a not_found OpenAlex result via title search
# ---------------------------------------------------------------------------


def test_s2_lifts_not_found(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={"meta": {"count": 0}, "results": []},
    )
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={
            "total": 1,
            "offset": 0,
            "data": [
                {
                    "paperId": "abc123",
                    "title": "A Real Lurking Paper",
                    "year": 2022,
                    "authors": [{"name": "Jane Lurker"}],
                }
            ],
        },
    )
    entry = {
        "key": "lurker",
        "title": "A Real Lurking Paper",
        "authors": ["Lurker, Jane"],
        "year": 2022,
        "doi": None,
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
# S2 lifts an ambiguous OpenAlex result to verified
# ---------------------------------------------------------------------------


def test_s2_lifts_ambiguous_to_verified(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={
            "meta": {"count": 2},
            "results": [
                {
                    "id": "https://openalex.org/W1",
                    "display_name": "Shared Title Across Two Works",
                    "title": "Shared Title Across Two Works",
                    "publication_year": 2020,
                    "authorships": [
                        {"author": {"display_name": "Different Author One"}}
                    ],
                },
                {
                    "id": "https://openalex.org/W2",
                    "display_name": "Shared Title Across Two Works",
                    "title": "Shared Title Across Two Works",
                    "publication_year": 2020,
                    "authorships": [
                        {"author": {"display_name": "Different Author Two"}}
                    ],
                },
            ],
        },
    )
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={
            "total": 1,
            "offset": 0,
            "data": [
                {
                    "paperId": "s2id999",
                    "title": "Shared Title Across Two Works",
                    "year": 2020,
                    "authors": [{"name": "John Smith"}],
                }
            ],
        },
    )
    entry = {
        "key": "ambs2",
        "title": "Shared Title Across Two Works",
        "authors": ["Smith, John"],
        "year": 2020,
        "doi": None,
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "verified"
    assert result["match_source"] == "semantic_scholar"
    assert result["semantic_scholar_id"] == "https://www.semanticscholar.org/paper/s2id999"


# ---------------------------------------------------------------------------
# S2 also misses -> stays not_found
# ---------------------------------------------------------------------------


def test_s2_also_not_found(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={"meta": {"count": 0}, "results": []},
    )
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={"total": 0, "offset": 0, "data": []},
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
# S2 is skipped when OpenAlex verifies cleanly
# ---------------------------------------------------------------------------


def test_s2_skipped_when_openalex_verified(httpx_mock):
    httpx_mock.add_response(
        url="https://api.openalex.org/works/doi:10.1000/clean",
        json={
            "id": "https://openalex.org/W_clean",
            "display_name": "Clean Match Paper",
            "title": "Clean Match Paper",
            "publication_year": 2020,
            "authorships": [{"author": {"display_name": "A. Alpha"}}],
        },
    )
    entry = {
        "key": "clean",
        "title": "Clean Match Paper",
        "authors": ["Alpha, A."],
        "year": 2020,
        "doi": "10.1000/clean",
        "arxiv_id": None,
    }
    with httpx.Client() as client:
        result = vc.resolve_entry(client, entry)
    assert result["status"] == "verified"
    assert result["match_source"] == "openalex"
    s2_calls = [
        r for r in httpx_mock.get_requests()
        if "semanticscholar" in str(r.url)
    ]
    assert s2_calls == []


# ---------------------------------------------------------------------------
# end-to-end CLI smoke against the bundled sample.bib fixture
# ---------------------------------------------------------------------------


def test_cli_main_bibfile_smoke(httpx_mock, tmp_path):
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
    # S2 will be consulted for the not_found and metadata_mismatch entries.
    # Both miss -> s2_lifted stays 0.
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.semanticscholar\.org/graph/v1/paper/search\?.*$"),
        json={"total": 0, "offset": 0, "data": []},
        is_reusable=True,
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
    assert summary["s2_consulted"] == 2
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
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={"meta": {"count": 1}, "results": [
            {"id": "https://openalex.org/W1", "display_name": "Real Paper",
             "title": "Real Paper", "publication_year": 2024,
             "authorships": [{"author": {"display_name": "C. Author"}}]}
        ]},
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
    Must still resolve to verified."""
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={"meta": {"count": 0}, "results": []},
    )
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
    should resolve to verified, not ambiguous."""
    httpx_mock.add_response(
        url=re.compile(r"^https://api\.openalex\.org/works\?.*$"),
        json={
            "meta": {"count": 2},
            "results": [
                {
                    "id": "https://openalex.org/W100",
                    "display_name": "Discrete Flow Matching",
                    "title": "Discrete Flow Matching",
                    "publication_year": 2024,
                    "authorships": [{"author": {"display_name": "Itai Gat"}}],
                },
                {
                    "id": "https://openalex.org/W200",
                    "display_name": "Discrete Flow Matching",
                    "title": "Discrete Flow Matching",
                    "publication_year": 2024,
                    "authorships": [{"author": {"display_name": "Itai Gat"}}],
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
    assert result["openalex_id"] == "https://openalex.org/W100"


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
