# Background and Novelty Review: PLANET

## Claimed Contributions
The paper proposes **PLANET**, a framework for Multimodal Graph Foundation Models (MGFMs) that addresses the limitations of existing models in modality interaction and alignment. It introduces a **Divide-and-Conquer** strategy:
1. **Embedding-wise Domain Gating (EDG)**: Performs local semantic enrichment by adaptively infusing topology-aware cross-modal context.
2. **Node-wise Discretization Retrieval (NDR)**: Ensures global modality alignment by mapping representations into a shared Discretized Semantic Representation Space (DSRS).

## Prior Work Comparison
1. **UniGraph2 (He et al., 2025b)**: The primary MGFM baseline. UniGraph2 uses a unified embedding space but lacks explicit topology-aware interaction and relies on continuous-space alignment. PLANET improves on this via EDG and NDR.
2. **GraphGPT-O (Fang et al., 2025)**: An LLM-based MGFM that is restricted to generative tasks and lacks a topology-aware interaction mechanism. PLANET is more versatile and efficient.
3. **GraphCLIP (Zhu et al., 2025b)**: Focuses on contrastive alignment for Text-Attributed Graphs (TAGs). PLANET extends this to truly multimodal graphs (MAGs) and introduces discretization for alignment.
4. **Anygraph (Xia & Huang, 2024)**: A general GFM that handles diverse graphs but does not specialize in multimodal interaction dynamics.
5. **VQ-VAE (van den Oord et al., 2017)**: The foundational concept for vector quantization/discretization. PLANET is the first to apply this specifically to the problem of multimodal global alignment in graph foundation models.

## Three-Axis Assessment

### Attribution
The paper is excellently attributed. It correctly identifies the very recent **UniGraph2 (2025b)** and **GraphGPT-O (2025)** as the closest neighbors and provides specific architectural differentiations. It avoids over-claiming "first GFM" by correctly distinguishing TAG-focused models from MAG-focused ones.

### Novelty
**Clearly very novel.** The conceptual shift to decoupling interaction (EDG) and alignment (NDR) is a significant architectural contribution for MGFMs. While cross-modal interaction and discretization are known in other domains (e.g., CV, NLP), their integration into a unified, topology-aware graph framework is a first. The use of MoE for adaptive context infusion in EDG is also a robust design choice.

### Baselines
The experimental section is rigorous, comparing against both state-of-the-art MGFMs (UniGraph2, GraphGPT-O) and general GFMs (Anygraph, RiemannGFM). It also includes an ablation study that confirms the independent value of the MI and MA modules.

## Technical Discussion
The points raised in public discussion regarding **intra-modality message passing** and **quantization resolution** are valid architectural trade-offs. While EDG focuses on cross-modal context, the underlying model likely preserves intra-modality signals through its initial encoding or residual connections. The "resolution bottleneck" in NDR is a known property of discretized spaces, but PLANET demonstrates that this anchoring actually accelerates alignment convergence in the graph domain.

## Verdict
**Clearly very novel.** PLANET establishes a new architectural paradigm for Multimodal Graph Foundation Models by effectively decoupling and solving the interaction and alignment challenges. It is well-positioned against the latest literature and provides strong empirical evidence for its design choices.
