# Bibliography Audit - e43f049b

I audited the bibliography for the paper "Attention Deficits in Language Models: Causal Explanations for Procedural Hallucinations" (id: e43f049b).

## Methodology
I extracted the paper source and parsed `references.bib`. I checked for:
- Missing required BibTeX fields
- Duplicate cite keys
- Placeholder entries (TODO, FIXME, etc.)
- Year anomalies
- Key-content mismatches (e.g., year in key vs. year field)

## Findings
I found the following issue:

- **Key-Year Mismatch**: 
  - Entry: `wu2024retrieval`
  - Issue: The cite key contains `2024`, but the `year` field is set to `2025`.
  - Content: `title={Retrieval Head Mechanistically Explains Long-Context Factuality}`, `booktitle={International Conference on Learning Representations}`, `year={2025}`.

This mismatch can lead to confusion in citations and might indicate an incomplete update of the bibliographic entry.
