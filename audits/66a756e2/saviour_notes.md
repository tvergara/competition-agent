# Saviour Notes: TIMI (66a756e2)

This paper proposes TIMI, a training-free framework for Image-to-3D multi-instance generation that uses inference-time guidance (ISG and SGU) to disentangle objects while preserving global layout.

### Observations

1. **Inference Efficiency:** TIMI introduces only a ~9% computational overhead compared to its base model, Hunyuan3D 2.0 (59.2s vs. 54.2s per scene), as reported in Table 1. This is significantly more efficient than the nearest training-based baseline, MIDI, which incurs a ~66% overhead (90.1s), or compositional methods like DPA which take over 10x longer (783s). This confirms the framework's suitability as a lightweight plug-in for existing I23D models.

2. **Cross-Attention Layer Sensitivity:** While the paper defaults to guiding the first four layers ( \le 4$), the ablation in Table 3 reveals a notable trade-off: restricting guidance to just the first layer (=1$) actually yields a higher local F-Score (0.372 vs. 0.353), suggesting better individual object quality, albeit with a lower separation success rate (0.772 vs. 0.809). This indicates the module can be tuned depending on whether instance distinctiveness or geometric fidelity is the primary priority.

3. **Dynamic Gradient Scaling:** The Spatial-stabilized Geometry-adaptive Update (SGU) module adaptively scales gradients using the standard deviation of the current latent features ($\sigma_{\mathbf{z}_t}$) in Equation 9. By tying the "separation force" to the global feature energy at each timestep, the update remains relative to the denoising state. This statistical anchoring likely explains why TIMI avoids the structural breakage often associated with naive inference-time optimization.
