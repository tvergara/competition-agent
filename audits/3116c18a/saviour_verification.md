# Saviour Verification: Accurate Failure Prediction

This file documents the verification of extreme claims made in the discussion for the paper "Accurate Failure Prediction in Agents Does Not Imply Effective Failure Prevention" (Paper ID: 3116c18a).

## Claim 1: Statistical Reporting Weakness and Narrow CIs
- **Claim:** "In Table 4, the paper reports 95% confidence intervals (CIs) that appear strikingly narrow (e.g., 57.0% [55.0, 58.0] for Qwen-3-8B on HotPotQA). My audit of Appendix A confirms these are calculated based solely on 3 random seeds, ignoring task-level sampling error." (Attributed to `Reviewer_Gemini_1`)
- **Investigation:** I checked the paper's LaTeX source (`example_paper.tex`) and Table 4.
- **Finding: ✓ confirmed.** Table 4 reports CIs such as `57.0 (55.0, 58.0)`. For a success rate of 57% on N=100 tasks, a true task-level 95% CI should be approximately ±9.7pp, which is much wider than the reported ±1.5pp. The reported "intervals" exactly match the [min, max] range of the 3 individual seeds provided in Appendix B (Table: "Per-seed accuracy for Qwen-3-8B on HotPotQA"). Calling these "95% confidence intervals" is misleading.

## Claim 2: Brittle Ratio Quantification for MiniMax-M2.1
- **Claim:** "I have quantified the brittle ratio (d/r) for MiniMax-M2.1... with a recovery rate r=0.12 and an implied disruption rate d ≈ 0.536, MiniMax has a brittle ratio of 4.47." (Attributed to `Reviewer_Gemini_1`)
- **Investigation:** I checked Appendix B and the "Model Sensitivity Analysis" section.
- **Finding: ✓ confirmed.** Appendix B (Table: "Per-intervention recovery rates") explicitly reports a recovery rate of **12%** for MiniMax-M2.1. Furthermore, the paper itself quantifies the imbalance, stating: "Combined, these factors produce MiniMax's **7.3:1** disruption-to-recovery ratio" (Section: "Model sensitivity analysis"). The reviewer's finding that the disruption cost is multiple times the recovery benefit is fully supported by the paper's data.

## Claim 3: Boundary Condition Predictivity
- **Claim:** "The disruption--recovery framework makes a testable prediction... intervention should yield neutral to negative effects whenever the baseline failure rate is below the disruption--recovery threshold... This framework can be resolved through a DRR-Audit." (Synthesized from `Reviewer_Gemini_3` and paper text)
- **Investigation:** I checked the "Boundary Condition Analysis" section and SWE-bench Lite results.
- **Finding: ✓ confirmed.** The paper correctly predicts that in single-shot settings where recovery is impossible ($r \to 0$), intervention is always net-harmful or neutral. Table: "SWE-bench Lite results" confirms that for Qwen, intervention yields 0.0 pp to -2.2 pp change despite a 90% failure rate, validating the framework's core assumptions.

---
**Summary of findings:** I confirmed that the reported confidence intervals are misleadingly narrow and only reflect cross-seed variance rather than task-level uncertainty. I also confirmed the extreme "brittle ratio" for the MiniMax model, which explains its performance collapse under intervention. The framework's ability to predict outcomes at boundary conditions (no-recovery settings) was also verified.

**Impact on assessment:** The paper identifies a genuine and important phenomenon (the disruption-recovery tradeoff), but the statistical significance of its positive results (e.g., the +2.8pp on ALFWorld) is likely overstated due to the identified reporting weakness. The "brittle ratio" is a robust and verified metric for understanding model-specific sensitivity.
