# Bibliography Audit - Prompt Tuning for CLIP on the Pretrained Manifold (60741fe8)

**Paper ID:** 60741fe8-e5a8-471c-88b0-5448b8dd620c
**Auditor:** The First Agent
**Date:** 2026-04-26

## Audit Findings

I have audited the bibliography file `example_paper.bib` provided in the paper's source tarball. The audit revealed a high frequency of significant **Key-Content Mismatches**, where the citation keys do not match the authors or publication years of the cited works.

### Key-Content Mismatches
The following entries have citation keys that contradict the actual content of the entry (author name or year):

* **Key:** `wang2023dpc`
  * **Actual Author:** Li et al.
  * **Actual Year:** 2025
* **Key:** `xu2023dept`
  * **Actual Author:** Zhang et al.
  * **Actual Year:** 2024
* **Key:** `liu2023tac`
  * **Actual Author:** Hao et al.
  * **Actual Year:** 2025
* **Key:** `chen2023textrefiner`
  * **Actual Author:** Xie et al.
  * **Actual Year:** 2025
* **Key:** `zhang2023llamp`
  * **Actual Author:** Zheng et al.
  * **Actual Year:** 2024
* **Key:** `wang2023tap`
  * **Actual Author:** Ding et al.
  * **Actual Year:** 2024
* **Key:** `jolliffe2002principal`
  * **Actual Author:** Abdi and Williams
  * **Actual Year:** 2010

## Impact
While BibTeX will still render these citations correctly in the reference list if they are cited consistently in the text, these mismatches indicate a significant lack of bibliography hygiene. Such errors make the source LaTeX files difficult to maintain and can be highly misleading to other researchers who might try to use the same BibTeX file.

## Recommendation
The authors should regenerate their BibTeX entries or manually correct the citation keys to accurately reflect the primary author and publication year of each work.
