# Saviour Notes for 8e32c11f

This paper proposes Semi-knockoffs, a conditional independence testing framework that uses two residual-resampling populations to compare loss changes from a pretrained model.

Observation 1: The method is not just a p-value test: Section 3 gives finite-sample type-I control through paired nonparametric tests, while Section 3.3 adapts the knockoff threshold for direct FDR control, avoiding reliance on BH-style dependence assumptions for that FDR route.

Observation 2: The empirical high-dimensional evidence is narrower than the wording suggests. The main simulations are repeated 50 times with n=300 and p=50, and the appendix higher-dimensional double-robustness check also uses p=50 rather than a p much larger than n regime.

Observation 3: The real-data experiment on Wisconsin Diagnostic Breast Cancer is a useful sanity check but not a direct ground-truth feature-selection benchmark: because true important features are unknown, the paper estimates type-I error by adding an artificial null feature correlated at 0.6 with the original inputs.
