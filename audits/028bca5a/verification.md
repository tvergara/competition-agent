# Verification Report for MOTIFLOW (028bca5a)

I have verified several material claims regarding the methodology, performance, and comparative positioning of MOTIFLOW.

## Claims Checked

1. **Atom Stability (GEOM-Drugs)**: **Confirmed**.
   - **Claim:** Surpassing state-of-the-art in atom stability on GEOM-Drugs.
   - **Evidence:** Table 2 in Section 5.1 reports MOTIFLOW at 95.0% atom stability, compared to 87.2% for the strongest atom-based baseline, END.
2. **Generation Steps**: **Confirmed**.
   - **Claim:** 2x to 10x reduction in generation steps compared to atom-based methods.
   - **Evidence:** Table 2 and Table 1 show MOTIFLOW using 100 steps while baselines like GeoLDM, GeoBFN, and END use 1000 steps (10x) or 250 steps (2.5x).
3. **Compression Factor**: **Confirmed** (with minor discrepancy).
   - **Claim:** 3.5x compression in molecular representations.
   - **Evidence:** The abstract claims 3.5x compression, while Section 3.2 in contents/method.tex specifies 3.4x for all-atom representations on the QMUGS dataset.
4. **Fragmentation Threshold**: **Confirmed**.
   - **Claim:** Default pruning threshold of alpha = 0.1% in the fragmentation scheme.
   - **Evidence:** Section 3.1 in contents/method.tex confirms the use of alpha=0.1% as the default threshold.
5. **Dummy Atoms**: **Confirmed**.
   - **Claim:** Use of "dummy atoms" to resolve the orientation of collinear and isolated fragments.
   - **Evidence:** Section 3.1 in contents/method.tex explicitly describes adding dummy atoms at a unit distance to lock the SE(3) frame orientation.
6. **HierDiff Comparison**: **Confirmed**.
   - **Claim:** HierDiff is a relevant fragment-based 3D generator that should be compared against.
   - **Evidence:** HierDiff is cited in the Related Work section (Section 4), but it is absent from the quantitative comparison tables (Tables 1 and 2), confirming the observation that a direct numerical comparison is missing.

## Summary

We checked 6 material claims and confirmed all 6 (with a minor 0.1x discrepancy noted in the compression factor). The audit confirms that MOTIFLOW achieves significant improvements in atom stability and generation efficiency by leveraging a rigid-motif representation. While the methodology is technically sound and well-cited, the superior stability results are partly a consequence of the rigid-motif design which preserves internal bond stability by definition.
