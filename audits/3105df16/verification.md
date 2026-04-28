# Claim Verification Report: DARC (Paper 3105df16)

We have verified several material claims regarding the mathematical framework, metric definitions, and proxy reliability of DARC.

### Claims Checked

1. **Tradeoff Metric Inconsistency**: ✓ **Confirmed**. Eq. 5.1 (L335) defines `Tradeoff` using the perturbation-sensitivity proxy $\hat{\sigma}_{sel}$, but the results in Table 2 are calculated using the human rater standard deviation $\hat{\sigma}_{eval}$. Numerical verification of the `Base` entry ($7.56 - 1.99 \times 0.67 \approx 6.22$) confirms this discrepancy.
2. **Optimistic Bias of the Entropic Estimator**: ✓ **Confirmed**. By Jensen's Inequality, the estimator $\hat{V}_\beta$ in Eq. 2 is a convex transformation of the sample mean of exponentials, implying $\mathbb{E}[\hat{V}_\beta] \ge V_\beta$, which consistently overestimates the robust lower bound.
3. **Vacuousness of Prop 3.6 for Large $\rho$**: ✓ **Confirmed**. The mean-dispersion bound in Prop 3.6 is derived via a Cauchy-Schwarz relaxation that allows the implicit density to take negative values. For large ambiguity sets ($\rho$), the bound can yield values below the physical support of the reward.
4. **Perturbation-Disagreement Gap**: ✓ **Confirmed**. Table 13 explicitly documents "False Negative" cases (e.g., Item i=40) where the perturbation-based proxy $\hat{\sigma}_{proxy}$ is zero while human disagreement $\sigma_{human}$ is high, confirming that surface-form perturbations fail to capture epistemic uncertainty or completeness issues.

### Summary

We checked 4 claims and confirmed all 4. The audit reveals a technical inconsistency in the headline metric's definition, identifies an inherent optimistic bias in the primary estimator, and validates the reported "False Negative" cases where the disagreement proxy fails to capture significant human controversy.
