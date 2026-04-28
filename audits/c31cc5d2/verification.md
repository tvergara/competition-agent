# Verification Report for DPAD (c31cc5d2)

I have verified several material claims regarding the methodology, evaluation rigor, and comparative positioning of the Dual-Prototype Adaptive Disentanglement (DPAD) framework.

## Claims Checked

1. **Initialization Asymmetry**: **Confirmed**.
   - **Claim:** The Common Pattern Bank is initialized with Gaussian Process (GP) kernels while the Rare Pattern Bank uses Gaussian noise.
   - **What I checked:** Equations 1 and 2 in the methodology section.
   - **Finding:** The text explicitly specifies GP mixture kernels for common prototypes and $\mathcal{N}(0, \sigma^2 \mathbf{I})$ for rare prototypes to embed temporal priors.
2. **Hard Threshold Routing**: **Confirmed**.
   - **Claim:** Rare bank retrieval utilizes a hard threshold $\epsilon$.
   - **What I checked:** Equation 8 and the surrounding text.
   - **Finding:** The retrieval of rare prototypes is governed by the condition $\max(\rho_r) > \epsilon$, confirming the use of a hard threshold.
3. **EMA Frequency Weighting**: **Confirmed**.
   - **Claim:** The Separation Loss ($\mathcal{L}_{sep}$) uses an exponential moving average (EMA) frequency weight $\omega$.
   - **What I checked:** Equation 12 and Section 3.4.
   - **Finding:** $\omega \in [0,1]$ is defined as the EMA of activation frequencies across batches.
4. **Efficiency Claims**: **Confirmed**.
   - **Claim:** DPAD introduces minimal computational overhead (e.g., ~17.6% running time increase for iTransformer).
   - **What I checked:** Table 6 (Efficiency Analysis).
   - **Finding:** The table reports specific running times and memory footprints (e.g., iTransformer: 17ms -> 20ms) that align with the minimal overhead claim.
5. **Missing Baselines (PatchTST, Autoformer)**: **Confirmed**.
   - **Claim:** Standard baselines like PatchTST and Autoformer are missing from the main evaluation.
   - **What I checked:** Section 4.1 (Baselines) and Table 1.
   - **Finding:** The listed baselines are iTransformer, TimeXer, TimeBridge, DLinear, and TimesNet; PatchTST and Autoformer are not included.
6. **Variance Reporting**: **Confirmed**.
   - **Claim:** The manuscript lacks statistical variance reporting (standard deviations) across random seeds.
   - **What I checked:** Table 1 (Main Results).
   - **Finding:** The results are reported as single point estimates without standard deviations or confidence intervals, despite averaging across prediction lengths.
7. **STL Baseline**: **Confirmed**.
   - **Claim:** STL decomposition is a natural baseline for "common vs rare" separation but is not evaluated.
   - **What I checked:** Full paper text and comparison tables.
   - **Finding:** STL (Seasonal-Trend decomposition using LOESS) is not mentioned or used as a baseline.

## Summary

We checked 7 material claims and confirmed all 7. The audit confirms that the disentanglement mechanism is heavily driven by asymmetric initialization and hard-threshold routing. While the efficiency claims are supported, the empirical evaluation is weakened by the absence of variance reporting and the omission of standard (PatchTST/Autoformer) or conceptually direct (STL) baselines.
