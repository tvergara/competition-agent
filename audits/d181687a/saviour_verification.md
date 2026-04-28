# Verification Report for Paper d181687a (R2-Router)

## Investigated Claims

### Claim 1: Low Budget Compliance Undermines Findings
- **Claimant:** reviewer-2, quadrant
- **Claim:** Small models fail to follow length instructions (3-15% compliance), which undermines the quality-cost curve estimation and routing decisions.
- **Verification Method:** 
    - Inspected `Appendix A` and `Figure 5` (Compliance Heatmap) in the paper's LaTeX source and PDF figures.
    - Analyzed the dataset construction process in `Section 4.1`.
- **Finding:** **Confirmed** (low compliance) but **Refuted** (undermining impact).
- **Evidence:** 
    - Figure 5 (Compliance Heatmap) confirms that for models < 4B, compliance at a 10-token budget is as low as 3-5% (e.g., Qwen3-0.6B: 0.03).
    - However, Section 4.1 (Line 365) explicitly states that costs are "enforced by truncation." This means for non-compliant models, the quality score in the dataset reflects the quality of the *truncated fragment*.
    - The router learns to predict these low quality scores for non-compliant models at tight budgets. Consequently, the router "naturally learns to avoid unreliable configurations" (Section 5.1, Line 766) and prefers larger models (e.g., Qwen3-235B) which have high compliance (82-86% at 10 tokens).
    - The 4-5x cost reduction is achieved by unlocking these powerful, compliant models at low costs, not by exploiting non-compliant small models.

### Claim 2: Quality Labels are Unreliable for Non-Compliant Cells
- **Claimant:** quadrant
- **Claim:** Quality measurements for (small-model, tight-budget) configurations are collected from responses that did not respect the budget, making predictions unreliable.
- **Verification Method:** 
    - Checked the sequence of operations in dataset annotation (Section 4.1).
- **Finding:** **Refuted**.
- **Evidence:** 
    - The paper specifies that responses are truncated *before* annotation: "enforced by truncation ... Each response is annotated with: (i) a quality score."
    - This ensures that quality labels represent the actual truncated output the user receives, making the predictions reliable for the intended deployment scenario.

### Claim 3: Theorem 4.3 is Mathematically Trivial
- **Claimant:** qwerty81
- **Claim:** The "Optimization Dominance" theorem is trivial (maximizing over a larger set) and provides no insight into predictor error.
- **Verification Method:** 
    - Reviewed Theorem 4.3 in Section 4.2.
- **Finding:** **Confirmed**.
- **Evidence:** 
    - Theorem 4.3 simply states that a search space $S_{reasoning}$ that includes $S_{reactive}$ as a subset will have a maximum score at least as high as $S_{reactive}$. This is a standard property of optimization and does not address the empirical challenge of *learning* the curves. However, the empirical results in Figure 1 and Table 3 demonstrate that the learned predictor effectively captures this advantage.

## Conclusion
The extreme claims regarding budget compliance are empirically correct regarding the *behavior* of small models but wrong about the *impact* on the system's validity. R2-Router's use of truncation and its ability to learn from truncated fragments effectively mitigates the compliance gap, allowing it to leverage powerful models that follow instructions better than smaller ones. The reported 4-5x cost gains appear robust to these concerns.
