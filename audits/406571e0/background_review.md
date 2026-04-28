# Background and Novelty Review: VEQ (arXiv:2602.01037)

## Paper Summary
The paper introduces **VEQ (Visual Expert Quantization)**, a post-training quantization (PTQ) framework specifically tailored for Mixture-of-Experts (MoE) Vision-Language Models (VLMs). The authors identify that existing quantization methods fail to account for two types of heterogeneity: (1) **Modality Heterogeneity** (text tokens are more sensitive to error than vision tokens) and (2) **Expert Heterogeneity** (experts are specialized for different modalities and have different activation frequencies). VEQ addresses these by introducing a joint modality-expert importance weighting for grid-search optimization and an affinity-aware Hessian matrix for error minimization.

## Comparison with Prior Works
1. **VLMQ (Xue et al., 2025): "VLMQ: Token Saliency-Driven Post-Training Quantization for Vision-language Models"**
   - *Relationship:* VLMQ introduced gradient-driven importance factors to handle the modality gap in dense VLMs. VEQ extends this logic to MoE architectures by incorporating expert activation patterns.
   - *Citation:* Correctly cited.
2. **MoEQuant (Hu et al., 2025): "MoEQuant: Enhancing Quantization for Mixture-of-Experts Large Language Models via Expert-Balanced Sampling and Affinity Guidance"**
   - *Relationship:* MoEQuant introduced affinity-guided quantization for MoE LLMs (text-only). VEQ integrates modality sensitivity into the affinity weighting.
   - *Citation:* Correctly cited.
3. **MQuant (Yu et al., 2025): "MQuant: Unleashing the Inference Potential of Multimodal Large Language Models via Full Static Quantization"**
   - *Relationship:* Proposes modality-specific static scales. VEQ offers a more fine-grained expert-level weighting.
   - *Citation:* Correctly cited.
4. **MBQ (Li et al., 2025): "Mbq: Modality-balanced quantization for large vision-language models"**
   - *Relationship:* Uses gradient-based sensitivity to balance modalities. VEQ applies this to the sparse MoE setting.
   - *Citation:* Correctly cited.
5. **DynaMo (Zheng et al., 2025): "DynaMo: Runtime Switchable Quantization for MoE with Cross-Dataset Adaptation"**
   - *Relationship:* Focuses on expert dynamics across datasets. VEQ focuses on cross-modal expert specialization.
   - *Citation:* Correctly cited.

## Three-Axis Assessment
- **Attribution:** The paper is exceptionally well-attributed. It clearly identifies the two lines of research it synthesizes (VLM-specific and MoE-specific quantization) and cites the most recent SOTA in both fields (VLMQ, MoEQuant, etc.). It correctly positions its contribution as addressing the intersection of these two areas.
- **Novelty:** **High.** While the individual components (modality weighting and affinity weighting) have been explored in isolation, their joint formulation for MoE VLMs is novel and well-motivated. The observation that experts spontaneously specialize in modality-specific clusters is used to derive a principled importance metric that combines quantity (activation frequency) and quality (gradient sensitivity).
- **Baselines:** **Comprehensive.** The paper compares against both modality-aware (VLMQ, MBQ, MQuant) and MoE-aware (MoEQuant, MoQa) baselines, demonstrating superior performance across multiple benchmarks (2.04% - 3.09% accuracy gains).

## Overall Verdict
**Very Novel.** The paper successfully addresses a specific and timely challenge at the intersection of two complex architectures. The proposed dual-aware quantization framework is technically sound, empirically effective, and fills a clear gap in the existing literature.
