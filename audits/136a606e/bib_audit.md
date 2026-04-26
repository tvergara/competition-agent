# Bibliography Audit - Paper 136a606e

**Paper Title:** Learning with Differentiable Combinatorial Sampling Layers
**Paper ID:** 136a606e-c591-4eca-a248-70822da51479
**Auditor:** The First Agent (Bibliography Auditor)

## Audit Overview
I performed an automated and manual audit of the BibTeX file(s) found in the paper's source tarball.

## Findings

### 1. Information Leakage (Local File Paths)
The majority of entries in the bibliography contain absolute local file paths in the `file` field. These paths leak information about the local machine's directory structure and the user's name (e.g., `/Users/gvivier/...`). This is a common byproduct of uncleaned exports from reference managers like Zotero.

Examples of affected entries include:
- `mensch_differentiable_2018`
- `berthet_learning_2020`
- `blondel_learning_2020`
- `vlastelica_differentiation_2020`
- ... and many others (almost every entry in the file).

### 2. Improper Entry Types for Published Works
Many entries are defined using the `@misc` type, even though the `annote` or `note` fields explicitly mention that they were published in major venues. Using `@misc` instead of `@inproceedings` or `@article` often results in missing information (like volume, number, or booktitle) in the rendered bibliography.

Examples:
- `blondel_learning_2020`: Note mentions "In Journal of Machine Learning Research, volume 21" (should be `@article`).
- `sahoo_backpropagation_2023`: Note mentions "ICLR 2023 conference paper" (should be `@inproceedings`).
- `amos_optnet_2021`: Note mentions "ICML 2017" (should be `@inproceedings`).
- `ahmed_simple_2024`: Note mentions "ICLR 2023" (should be `@inproceedings`).
- `niepert_implicit_2021`: Note mentions "NeurIPS 2021" (should be `@inproceedings`).

## Conclusion
The bibliography needs significant cleaning to remove local file paths and to use the correct entry types for published peer-reviewed works. This will improve both the privacy and the professional quality of the paper's references.
