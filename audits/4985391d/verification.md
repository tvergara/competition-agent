# Claims checked for "Efficient Analysis of the Distilled Neural Tangent Kernel"

1. ✓ **Theorem 3.3 Scope**: Confirmed. Theorem 3.3 (Section 3.3.2) is explicitly a "One-step smoothness regret bound" for dataset distillation. The full DNTK pipeline described in Section 4 includes additional steps (JL random projection and local-global gradient distillation) which are motivated by the theory but not directly covered by the one-step guarantee.
2. ✓ **Pretraining Dependency (Figure 1)**: Confirmed. The caption of Figure 1 (Section 5.1) explicitly states that while the method works with a distilled-data base model, "performance differs by 10% if only the distilled-data model is available" and results in a "better-conditioned kernel" when using a pretrained model.
3. ✓ **Coverage Gap Quantification (Figure 4)**: Confirmed. Figure 4 (Bottom) and Section 5.3 quantify the local-global "coverage gap" at approximately 12-15% of global variance at the truncation rank. Algorithm 1 (specifically Step 5) is designed to explicitly capture these "gap directions."

# Summary
I checked 3 material claims regarding the theoretical scope, empirical dependencies, and spectral analysis of DNTK. All 3 claims were confirmed. The paper's theoretical guarantees are limited to local updates, and its empirical performance relies heavily on the quality of the base model's feature representation, but it successfully identifies and addresses a significant spectral coverage gap in local-only compression methods.
