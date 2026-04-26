# Saviour notes for 06374772

This paper proposes MoVE, a shared token-indexed value-embedding bank that adds parametric memory to autoregressive transformers and evaluates it on text generation, image generation, and an MLA variant.

Observation 1: The text-generation gains are consistent but parameter-heavy; at D32, MoVE x2 adds about 4.33B parameters to a 1.88B baseline for a 0.016 BPB gain, and the discussion explicitly acknowledges lower performance gain per added parameter than dense scaling.

Observation 2: The image-generation evidence is metric-specific. On GPT-L, MoVE improves FID from 3.47 to 3.10 and recall from 0.51 to 0.53, but has lower IS than the standard model (281.4 vs 291.2) and lower precision than LaVE (0.84 vs 0.86); the planned GPT-XXL evaluation was not completed because checkpoint storage failed.

Observation 3: The ablation usefully separates global memory from standard-path gating. Global+gated MoVE is best in all four D12/D20 settings, but some margins over gated LaVE are small, e.g. 0.8124 vs 0.8128 on D12 x2 and 0.7440 vs 0.7462 on D20 x2.
