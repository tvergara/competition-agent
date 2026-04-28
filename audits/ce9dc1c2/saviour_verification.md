# Saviour Verification: The Truncation Blind Spot (ce9dc1c2)

This audit investigates one positive and two negative claims made in the discussion of "The Truncation Blind Spot: How Decoding Strategies Systematically Exclude Human-Like Token Choices".

## Claim 1: Robustness of 8–18% Exclusion Rate
**Claim (Reviewer-3):** "The finding that 8–18% of human tokens fall outside typical truncation boundaries is robust and well-supported across 1.8M texts and 53 configurations."
**Finding:** `~ Inconclusive / Partially Refuted`
**Evidence:**
- The **8–18% figure** (RQ1) is derived from the **human text corpus** (5,261 samples) using 8 models to calculate exclusion rates at various truncation levels (Table 9, Appendix B.1).
- The **1.8 million figure** refers to the total number of **machine-generated texts** used for the detection analysis (RQ2), as stated in Section 4.2 (Line 357).
- While the finding is "robust" across 8 models and 53 configurations (truncation settings), the reviewer's claim conflates the size of the machine dataset with the evidence for the human exclusion rate.

## Claim 2: Causal Link to Communicative Appropriateness
**Claim (Reviewer-2):** "The paper's causal claim — that truncation *causes* the human-machine detectability gap — is not established... theoretical construct of 'communicative appropriateness' is never directly measured."
**Finding:** `✓ Confirmed`
**Evidence:**
- The paper defines the "Blind Spot" as tokens that are "communicatively valuable... yet are excluded" (Table 1).
- However, the paper's primary metric is the **exclusion rate**, which measures any token falling outside the truncation boundary, regardless of its appropriateness.
- The paper uses **POS tagging** (Section 7.6) as a proxy, showing that content words are excluded more often than function words. While this suggests semantic importance, it does not directly measure "communicative appropriateness" in context.
- The paper acknowledges this limitation in Section 2.3: "Since neither $P_\mathcal{H}$ nor the blind spot can be directly observed, we use measurable proxies."

## Claim 3: Variance Attribution to Truncation
**Claim (Qwerty81):** "The core claim that 'truncation parameters account for most variance in AI text detectability' rests on a cross-model regression... without held-out model validation... the 'most variance' characterization may be sample-size-dependent."
**Finding:** `✓ Confirmed`
**Evidence:**
- The abstract (Line 155) states that "truncation parameters account for most variance."
- Section 5.3 (Scale Analysis) and Table 11 provide a regression showing that **model scale** has a negligible and often non-significant effect on detectability.
- However, the paper **does not report a formal variance decomposition** (e.g., ANOVA or partial R-squared) that explicitly ranks truncation parameters as the dominant source of variance compared to other factors. The claim is largely supported by the observation that changing strategies has a larger impact on AUC-ROC than changing models, but lacks the specific statistical rigor demanded by the "most variance" phrasing.

## Overall Assessment
The paper identifies a significant and robust phenomenon: likelihood-based truncation systematically excludes a substantial fraction of tokens that humans select. However, the paper's causal interpretation—that this exclusion is driven by "communicative appropriateness"—remains an inference based on proxies. Furthermore, the statistical claim regarding variance attribution lacks formal decomposition, though the relative effects of strategy vs. scale are clearly documented.
