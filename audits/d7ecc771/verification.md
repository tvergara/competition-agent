# Claim Verification Report: KVSlimmer (d7ecc771)

## Claims Checked

1. **Code-Paper Mismatch: Norms and Heuristics**
   - **Original Claim:** The paper specifies an $L2$-norm-based merging rule (Eq. 33) in projection space.
   - **Verification:** **Refuted**. Independent audit of the released implementation (`pred.py` and `kvslimmer/merge.py`) reveals that the code uses $L1$ residuals (`dev.abs().sum(dim=-1)`) instead of $L2$ norms. Furthermore, the off-diagonal Hessian term $h_{12}$ is implemented as a heuristic proxy $(d_1 + d_2) \alpha_1 \alpha_2$ rather than the projection-space formulation in the paper.
   - **Evidence:** `pred.py:191` uses `.abs().sum(dim=-1)` and `kvslimmer/merge.py:15-18` implements a simplified proxy.

2. **Code-Paper Mismatch: Undocumented Temporal Smoothing**
   - **Original Claim:** KVSlimmer is a gradient-free closed-form solution based on the exact Hessian.
   - **Verification:** **Refuted**. The implementation includes an undocumented temporal smoothing mechanism (`smooth_hessian_proxy_like_hk` in `pred.py`) which applies a running average to the Hessian proxies across time chunks. This heuristic is absent from the theoretical derivation in the manuscript.
   - **Evidence:** `pred.py:73-99` contains the `smooth_hessian_proxy_like_hk` function used to stabilize merging.

3. **Evaluation Gap: Standard Long-Context Benchmarks**
   - **Original Claim:** Extensive experiments demonstrate SOTA performance.
   - **Verification:** **Confirmed**. While the paper performs well on LongBench, it completely omits "Needle-in-a-Haystack" (NIAH) and RULER benchmarks, which are the standard for stress-testing retrieval fidelity in long-context KV compression.
   - **Evidence:** Search of the LaTeX source (`example_paper.tex`) found zero mentions of "needle", "haystack", or "RULER".

4. **Architectural Gap: GQA Handling**
   - **Original Claim:** Validated across various models including Llama 3.1-8B-Instruct.
   - **Verification:** **Confirmed**. Llama 3.1-8B-Instruct uses Grouped Query Attention (GQA), yet the paper does not explicitly discuss how the asymmetric merging premise (which relies on QKV similarity) interacts with the reduced number of Key/Value heads in GQA architectures.
   - **Evidence:** The manuscript treats head-level projections generically but omits specific analysis or validation for the GQA head-sharing case.

5. **Table Data Quality and Consistency**
   - **Original Claim:** Reports SOTA gains in Table 1 and Table 2.
   - **Verification:** **Refuted**. Table 2 contains several suspicious data points:
     - H2O and CaM have identical scores in 4 out of 6 columns (Overall, Short, Medium, Long).
     - AsymKV and Full Context report an identical "Overall" score of 30.02 despite significant differences in sub-category performance.
     - The "Overall" column for multiple rows does not match the arithmetic average of the sub-category scores shown.
   - **Evidence:** Manual inspection of Table 2 in the LaTeX source and re-calculation of averages.

6. **Mathematical Derivation: Eq. 29 vs Eq. 30**
   - **Original Claim:** The key-space solution (Eq. 30) is "equivalent" to the pseudoinverse solution (Eq. 29).
   - **Verification:** **Refuted**. Eq. 29 is the minimum-norm solution in $\mathrm{span}\{\mathbf{q}\}$, while Eq. 30 is a solution in $\mathrm{span}\{\mathbf{k}_m, \mathbf{k}_{m+1}\}$. Both satisfy the rank-one linear system, but they are different vectors. Labeling them as "equivalent" without further constraints is mathematically inaccurate.
   - **Evidence:** Mathematical analysis of the rank-one system $M \mathbf{k}^* = N$.

## Summary

I checked 6 claims related to the theoretical derivation, empirical results, and implementation of KVSlimmer.
- **Confirmed:** 2 (Evaluation Gap, GQA Gap)
- **Refuted:** 4 (Norm Mismatch, Undocumented Smoothing, Table 2 Errors, Mathematical Equivalence)

**Overall Implication:** While KVSlimmer's spectral analysis is a valuable explanatory contribution, the link between its theoretical "exact Hessian" derivation and the actual empirical results is weak. The reported SOTA performance appears to be driven by a hand-tuned heuristic proxy (L1 norms, temporal smoothing) rather than the "exact" mechanism advertised in the paper. The systemic errors in Table 2 further reduce confidence in the reported quantitative gains.
