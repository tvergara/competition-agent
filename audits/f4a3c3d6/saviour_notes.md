# Saviour notes for f4a3c3d6

This paper argues that closed-form OLS/RRR autoregressive anomaly scores are strong, efficient baselines for univariate and multivariate time-series anomaly detection.

Observation 1: The evaluation is stronger than a plain point-adjusted Best-F1 table. Section 4 reports F1, B-F-5, and E-F-5, and the appendix explicitly motivates the delay-aware/event-level metrics as guards against Best-F1 inflation.

Observation 2: The RRR setup has a dataset-specific tuning burden. Appendix Figure 6 and its text state that optimal RRR rank and window size vary by dataset, with MSL/SMAP preferring lower ranks while SMD/SWAT benefit from higher ranks.

Observation 3: The artifact link in Koala metadata points to `https://github.com/huggingface/candle`, whose GitHub API description is "Minimalist ML framework for Rust"; the submitted tarball contains manuscript source and figures, so I did not find paper-specific experiment code through the platform artifact.
