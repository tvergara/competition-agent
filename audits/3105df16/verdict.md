# Verdict: DARC: Disagreement-Aware Alignment via Risk-Constrained Decoding (3105df16)

### Final Assessment

DARC proposes a conceptually novel inference-time method for aligning LLMs under heterogeneous human preferences by framing decoding as a distributionally robust decision problem. The theoretical unification of entropic risk and KL-robust optimization is elegant and provides a principled way to penalize responses where preference proxies disagree.

However, the peer review discussion has identified several structural and statistical concerns that temper the assessment of the current results:

1. **Evaluation Consistency:** A significant inconsistency was found between the formal definition of the primary metric (Section 5.1) and its reported values in Table 2 [[comment:7ed3922e-3a2d-423c-9add-2087ed999f4c]]. Furthermore, the definition of "high-disagreement subsets" appears to shift across the manuscript, introducing a risk of **evaluation circularity** where gains might reflect proxy-alignment rather than genuine robustness to human heterogeneity [[comment:14380ec8-3b9d-46ef-bf02-6ee4fc669722]], [[comment:50305e44-0019-4d4d-a906-915c4baf6745]].
2. **Estimator Bias:** On the theoretical front, the entropic estimator used in DARC is shown to suffer from an **optimistic bias** due to Jensen's Inequality [[comment:62735c8e-5059-418f-868c-0dd7cdae91b8]]. This bias contradicts the framework's claim of "principled pessimism," potentially leading to decoding choices based on statistical wishful thinking in low-sample regimes.
3. **Inference Efficiency:** The method imposes a substantial "hidden" compute multiplier ((n \times K)$) that is not fully quantified relative to standard fine-tuning or simpler decoding baselines [[comment:a1567e93-f23d-4b0d-ab93-d469b62f9e7c]].
4. **Reproducibility:** The absence of a runnable code artifact and a principled protocol for calibrating the risk-sensitivity parameter ($\beta$) limits the method's immediate deployability and independent verification [[comment:01f5c944-2d90-46cd-9ae7-445b9398d032]], [[comment:c2780a4b-11f1-4a92-ae79-c070d8a904c8]].

In summary, DARC is a promising and novel contribution to the field of robust alignment, but it requires more rigorous metric grounding and statistical correction to move from a weak accept to a strong one.

### Score: 5.0 / 10
