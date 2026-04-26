# Bibliography Audit for RIGA-Fold

Paper ID: 5c5508af-25ee-4319-9a93-522ef57d7f87
Title: RIGA-Fold: A General Framework for Protein Inverse Folding via Recurrent Interaction and Geometric Awareness

## Audit Results

I performed a structural audit of the `references.bib` file and identified the following issues:

### Duplicate Cite Keys
The following keys appear multiple times in the bibliography, which can lead to citation ambiguity:
- `kipf2016semi`
- `velivckovic2017graph`
- `alexey2020image`
- `rong2019dropedge`
- `zhao2019pairnorm`
- `topping2021understanding`

### Missing Required Fields
- **Entry `singh2025effects`**: Missing `journal` field for an `@article` entry.

### Key-Year Mismatches
The following entries have a cite key that encodes a year different from the `year` field, which might indicate a miscitation or an updated reference that was not fully renamed:
- `jing2020learning`: Key has 2020, but `year` field is 2021.
- `gao2022pifold`: Key has 2022, but `year` field is 2023.
- `alon2020bottleneck`: Key has 2020, but `year` field is 2021.
- `mao2023novo`: Key has 2023, but `year` field is 2024.

## Audit Methodology
The audit was performed using a custom Python script that parses the `.bib` files using `bibtexparser` and checks for:
1. Missing required fields for standard entry types (`@article`, `@inproceedings`, `@book`).
2. Duplicate cite keys.
3. Placeholder entries (e.g., "todo", "fixme").
4. Year anomalies (years in the far future or far past).
5. Heuristic mismatches between the cite key and the `year` field.
