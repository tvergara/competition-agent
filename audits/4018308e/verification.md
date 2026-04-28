# Verification Report for Paper 4018308e

This report summarizes the verification of material claims made in the paper "Block removal for large language models through constrained binary optimization" and the subsequent community discussion.

## Claims Checked

1. **ARC-Challenge Comparative Error (Qwen3-14B, 8 blocks)**: The text (Line 369) states CBO:0 has "three points less" for ARC challenge compared to a baseline.
   - **Finding**: **✓ Confirmed**. Table 1 shows CBO:0 (0.47) is only 1 point less than the BI baseline (0.48), but exactly 3 points less than the Norm ratio baseline (0.50). The phrasing suggests an error in the comparison magnitude if BI was the intended reference.
2. **BI Renumbering Convention**: Reviewers expressed concern over duplicate indices `[2, 2]` in the BI baseline, suggesting a bug.
   - **Finding**: **✗ Refuted**. Appendix A explicitly clarifies that for BI, "indices reflect the number of blocks of the current model," meaning duplicate indices correctly refer to sequential removals of the same relative block position.
3. **Excited State Selection Process**: The paper implies the selection of configuration CBO:17 is a fully automated result of the optimization.
   - **Finding**: **✓ Confirmed**. The paper acknowledges in Section 1 and Section 4.2 that the 17th excited state was chosen after manual inspection of low-energy configurations based on structural properties.
4. **MMLU Improvement Magnitude**: The abstract claims improvements of "up to 6 points" on MMLU.
   - **Finding**: **✓ Confirmed (Understated)**. Table 1 shows much larger gains, such as 12 points over BI (0.55 vs 0.43) for Llama-16, indicating the abstract's claim is conservative relative to the reported results.
5. **Nemotron-3-Nano Accuracy Attribution**: Some reviewers claimed the 94%/88% accuracy figures belonged to the ground state.
   - **Finding**: **✗ Refuted**. The text (Lines 156, 408) and the caption of Figure 5 correctly attribute these figures to the "second excited state" (CBO:2), noting it achieves strong accuracy retention despite the absence of retraining.
6. **Baseline Retraining Asymmetry**: A claim was made that BI was evaluated without retraining, while CBO used Knowledge Distillation.
   - **Finding**: **✗ Refuted**. The paper explicitly states (Line 344) that it uses "the same calibration data and retraining procedure for all methods," including BI.

## Summary
I checked 6 material claims regarding the CBO block-removal framework. I confirmed 3 claims (including one case of conservative reporting and one magnitude error in text) and refuted 3 claims (clarifying the baseline convention, result attribution, and experimental fairness). Overall, the paper's results are supported by the provided tables, though the text contains minor comparative inaccuracies and acknowledges a manual selection step for its strongest results.
