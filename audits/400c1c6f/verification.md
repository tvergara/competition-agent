# Claim Verification for Paper 400c1c6f

I have verified several material claims regarding the mechanics and diagnostics of "anti-grokking" presented in the paper.

## Claims checked

1. **L-infinity Confound** (✓ **confirmed**): Appendix G (Theorem 1, line 1083) explicitly proves that a single large weight entry $|W_{i,j}|$ satisfies a sufficient condition to trigger a "Correlation Trap" in randomized matrices. This confirms that the trap signal is a mathematical consequence of the $\ell_\infty$ norm growth.
2. **Diagnostic Inconsistency** (✓ **confirmed**): Cross-referencing Table 1 (MLP) and Table 6 (Modular Addition) confirms that the $\alpha$ exponent behaves inconsistently across tasks. In the MLP, average $\alpha$ drops from .9$ to .1$ (below 2.0) during collapse, while in Modular Addition, it rises from .02$ to .89$.
3. **Concurrency vs. Prediction** (✓ **confirmed**): Although the paper claims "early warning" (line 551), the text later acknowledges that the $\alpha$ drop occurs "just after the significant drop in test accuracy" (line 546) and that traps are "immediately detected" (line 571) rather than predictive.
4. **Prior Work Overlap** (✓ **confirmed**): The paper's bibliography (line 2185) cites `prakash2025grokking` (arXiv:2506.04434), which is explicitly acknowledged as a prior version of this work describing the anti-grokking phenomenon.
5. **Missing Citation** (✓ **confirmed**): A review of `references.bib` confirms that Doshi et al. (2024, "To Grok or Not to Grok"), which demonstrated multi-phase training dynamics, is not cited or differentiated.
6. **LLM Pathologies** (✓ **confirmed**): Section 6 (line 725) and Figure 16 (line 739) provide data showing that production-quality LLMs (GPT-20B and 120B) exhibit an unusually large number of layers with $\alpha < 2$, supporting the claim of observable pathologies in large-scale models.

## Summary

We checked 6 claims and confirmed all 6. The audit confirms that while the mechanistic evidence for prototype memorization is visually grounded, the proposed spectral diagnostics are mathematically tied to simple weight norms, behave inconsistently across different architectures, and act as concurrent detectors rather than predictive early-warning systems. Furthermore, the work extends prior findings by the same authors and omits relevant concurrent literature on multi-phase grokking dynamics.

Full evidence derived from the manuscript source and bibliography.
