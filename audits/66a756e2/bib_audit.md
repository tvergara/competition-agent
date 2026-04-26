# Bibliography Audit for TIMI

Paper ID: 66a756e2-c084-495f-b9d8-3f0ac4332cea
Title: TIMI: Training-Free Image-to-3D Multi-Instance Generation with Spatial Fidelity

## Audit Results

I performed a structural audit of the `example_paper.bib` and `example_paper_full.bib` files and identified the following issues:

### Non-Standard Cite Keys
The bibliography uses descriptive and inconsistent cite keys instead of the standard `authorYEAR` or `authorYEARtitle` format. Examples include:
- `midi`
- `real-data`
- `DPA`
- `dit`
- `dreamfusion`
- `Magic3D`
- `zero123`
- `lgm`
- `trellis`
- `reparo`
- `sing3d`
- `gen3dsr`
- `CAST`
- `3dfront`
- `flux`
- `kerbl3Dgaussians`
- `CLIP`
- `dino`
- `DreamView`

### Messy Author Data
- **Entry `flux`**: The author `Black Forest Labs` is listed as `Labs, Black Forest`, which is an incorrect inversion of a corporate/lab name.
- **Entry `hunyuan3d`**: The author is listed as `Tencent Hunyuan3D Team`. While acceptable for preprints, corporate authors often require special wrapping (e.g., `{{Tencent Hunyuan3D Team}}`) to prevent BibTeX from parsing "Team" as a surname and "Tencent Hunyuan3D" as first names.

### File Redundancy
The project contains two nearly identical bibliography files (`example_paper.bib` and `example_paper_full.bib`). The only difference between them is the inclusion of "Proceedings of the" in the `booktitle` fields of the `full` version. This redundancy can lead to maintenance issues if only one file is updated.

## Audit Methodology
The audit was performed using a custom Python script and manual inspection of the `.bib` files. The checks included:
1. Verification of cite key conventions.
2. Structural integrity of author names.
3. Analysis of project file redundancy.
4. Standard checks for missing fields and duplicate entries.
