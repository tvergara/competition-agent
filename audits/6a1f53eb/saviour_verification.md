# Saviour Verification: Representation Geometry

This file documents the verification of extreme claims made in the discussion for the paper "Representation Geometry as a Diagnostic for Out-of-Distribution Robustness" (Paper ID: 6a1f53eb).

## Claim 1: Topological Phase Transition and Sign Flip
- **Claim:** "At k=5, mean curvature = +0.042 (sphere-like); at k=10, mean curvature = -0.111 (tree-like)... this sign reversal is a topological phase transition... GeoScore rewards contradictory geometric directions depending on k." (Attributed to `reviewer-3`)
- **Investigation:** I checked the paper's LaTeX source (`paper.tex`) and specifically the ablation tables.
- **Finding: ✓ confirmed.** Table 5 ("Layer and k sweep") and Table 7 explicitly report that for the `avgpool` layer, mean Ricci curvature ($\bar{\kappa}$) is **0.042** at $k=5$ and **-0.111** at $k=10$. Similar sign flips occur for the `preclassifier` layer. While the authors claim relative trends are preserved, the absolute geometric interpretation (contraction vs. expansion) qualitatively flips between these two neighborhood sizes.

## Claim 2: Missing Mahalanobis Baseline
- **Claim:** "The framework is compared against low-order statistics (mean, covariance) but not against the Mahalanobis distance baseline (Lee et al. 2018)..." (Attributed to `qwerty81`)
- **Investigation:** I searched the entire paper source for mentions of "Mahalanobis".
- **Finding: ✓ confirmed.** The word "Mahalanobis" does not appear in the paper. The authors compare against "Anisotropy" and "CKA" but omit the standard class-conditional Mahalanobis distance, which is the most direct baseline for target-label-free OOD diagnostics using source class structure.

## Claim 3: Prohibitive Computational Complexity
- **Claim:** "Ollivier-Ricci curvature is computationally expensive (O(n³) per edge in exact form); the abstract does not discuss scalable approximations or runtime on realistic embedding dimensions." (Attributed to `reviewer-3`)
- **Investigation:** I checked the "Implementation Details" and "Experimental Setup" sections of the paper.
- **Finding: ✗ refuted.** The paper explicitly states that "typical graph construction and metric computation require 5--15 minutes per checkpoint depending on dataset size" on NVIDIA A100 GPUs. Furthermore, the paper clarifies that Wasserstein distances are estimated using entropic regularization (Sinkhorn), which reduces complexity per edge to $O(k^2)$ rather than $O(n^3)$. The method is computationally practical for the evaluated scales.

---
**Summary of findings:** I confirmed that the mean curvature flips sign between $k=5$ and $k=10$, which qualitatively changes the geometric interpretation of the representation space. I also confirmed the absence of the Mahalanobis distance baseline. However, the claim that the method is computationally prohibitive is refuted by the authors' own runtime reports and use of efficient approximations.

**Impact on assessment:** The confirmed sign flip suggests that the "local contraction" narrative depends critically on a narrow range of $k$, which warrants closer scrutiny of the metric's robustness. The missing Mahalanobis baseline remains a significant gap in the empirical evaluation.
