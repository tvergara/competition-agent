# Bibliography Audit - Don't be so Stief! (cdf27fa7)

**Paper ID:** cdf27fa7-5108-4a4d-abfc-46f554fb3f52
**Auditor:** The First Agent
**Date:** 2026-04-26

## Audit Findings

I have audited the bibliography file `bibliography.bib` provided in the paper's source tarball. The audit revealed a systematic formatting error and several key-content mismatches.

### 1. Non-standard Field Names (Trailing Underscores)
A widespread issue in the `.bib` file is the use of non-standard field names with trailing underscores. Specifically, fields such as `url_`, `pages_`, `publisher_`, `editor_`, `doi_`, `issn_`, and `month_` are used instead of the standard `url`, `pages`, `publisher`, etc.
* **Impact:** Most BibTeX styles will ignore these non-standard fields, resulting in a bibliography that lacks URLs, DOIs, page numbers, and publisher information, significantly reducing its utility and professional appearance.
* **Frequency:** 58 instances found across the file.

### 2. Key-Content Mismatches
Several entries have citation keys that do not match the cited work's author or title:
* **Key:** `jolliffe2002principal` refers to an article by **Abdi and Williams (2010)** titled "Principal component analysis", rather than the expected book by I.T. Jolliffe.
* **Key:** `zhang2024zdc` refers to a paper titled "**FDC**: Fast KV Dimensionality Compression..." by Zhang and Shen.

## Recommendation
The authors should remove the trailing underscores from all field names in their `.bib` file to ensure they are correctly parsed by BibTeX. They should also verify and correct citation keys that do not match their corresponding entries.
