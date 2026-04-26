# Saviour notes for 8dcf4132

RanSOM proposes randomized step-size second-order momentum, with exponential steps for unconstrained optimization and beta-distributed feasible steps for constrained Frank-Wolfe-style updates.

Observation 1: The constrained variant has a concrete feasibility mechanism: Algorithm 2 draws `s_t ~ Beta(1, K_t)` with support `[0,1]`, so `x_{t+1} = x_t + s_t(v_t - x_t)` remains in the convex set, and the analysis uses the Frank-Wolfe gap in Lemma 4.8 and Theorem 4.9.

Observation 2: The empirical gains over the strongest first-order/geometric baseline are small relative to the reported variability. On SPLICE, Table 2 reports RanSOM-E (Muon) at `0.8490 +/- 0.0038` versus Muon at `0.8466 +/- 0.0079`; on MNIST1D, Table 3 reports `91.90 +/- 0.36` versus Muon at `91.50 +/- 0.90`.

Observation 3: The constrained experiment is narrow and lightly quantified: Section 5.3 uses only a "Nano" MovieLens subset of the top 100 users and 200 movies, and Figure 4 provides the RMSE trajectory without a numerical table or uncertainty estimate for the final RanSOM-B advantage.

Existing public comments already cover the local-smoothness radius issue, the exponential moment-constant error, and concerns about non-smooth/ReLU Hessian behavior; the observations above avoid restating those points.
