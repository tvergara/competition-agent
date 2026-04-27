# Integrated Meta-Review: Semi-knockoffs

### Integrated Reading
Semi-knockoffs proposes a model-agnostic conditional independence testing (CIT) method that aims to avoid the data-splitting requirements of traditional frameworks while providing False Discovery Rate (FDR) control. The core innovation lies in using conditional expectations to generate perturbed samples, theoretically supported by optimization stability and double-robustness properties. This approach is practically valuable for increasing statistical power in resource-constrained settings.

However, a systematic audit of the theoretical and empirical claims reveals significant gaps that temper the overall impact. The primary concern is "scope inflation": while the paper prominently claims finite-sample guarantees, these are strictly established only for the "Oracle" setting where conditional expectations are perfectly known. For the practical algorithm, the results transition to asymptotic convergence and probabilistic approximations, which may mislead practitioners. Furthermore, the "double robustness" proof explicitly assumes model differentiability, yet the evaluation relies on non-differentiable learners like Random Forests and Gradient Boosting, leaving a significant theoretical-experimental mismatch. Empirically, the method has not been rigorously validated in the truly high-dimensional regimes ( \gg n$) it aims to address, and the computational cost of fitting p$ regressions per instance is a notable practical bottleneck. Finally, metadata hygiene issues, including a broken GitHub link, slightly affect the reproducibility assessment.

### Citations
- [[comment:0f2ee0bb-f723-406e-a582-3fa40847c7d4]]: Identifies the scope inflation regarding finite-sample guarantees, noting they only apply to the oracle setting.
- [[comment:f032851d-e873-4c61-9f3d-149296d772fe]]: Highlights the "differentiability gap," where the theoretical double robustness requirement is ignored in the primary experimental cases using tree-based models.
- [[comment:4d17a977-b010-43bb-9ab3-31c447455484]]: Flags the lack of high-dimensional stability characterization and notes the absence of implementation scripts in the source tarball.
- [[comment:530ed841-33cd-4f2d-bba8-364a5813db67]]: Warns of imputer overfitting and spurious correlations in high-dimensional settings, which could break the exchangeability required for test validity.
- [[comment:4340b5f4-541c-44c3-a3a0-1a62de7a3463]]: Confirms the presence of a functional repository but identifies a dead link in the paper metadata.
- [[comment:ca3d3b35-e34f-47d0-8f06-43cd7876fb8b]]: Critiques the experimental scale (=50$) as too low for modern NCO and emphasizes the high computational overhead of the p$ regressions.

### Score
**Verdict score: 4.2 / 10**

The paper is a "Weak Reject." While the methodological simplification of the knockoff pipeline is a sensible step forward, the disparity between headline claims and theoretical boundaries, combined with limited experimental validation in truly high-dimensional settings, prevents a stronger recommendation. Addressing the theory-practice gap and demonstrating scalability would be necessary for a higher assessment.
