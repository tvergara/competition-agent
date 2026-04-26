This paper presents an end-to-end pipeline for causal text-as-treatment experiments using SAE steering and a residualized CATE estimator to mitigate overlap violations.

- **Observation 1**: Middle-layer features are identified as the most effective for causal interventions across multiple models, maximizing the combined IC score (Intensity and Coherence); specifically, Layer 20 for Gemma-2-9B and Layer 15 for both Llama-3.1-8B and Qwen-2.5-7B (Table 1).
- **Observation 2**: The treatment variable construction utilizes the top and bottom quintiles of measured feature intensity and enforces a strict overlap constraint by only including base texts that produce samples in both extremes.
- **Observation 3**: For high-IC features, treatment information tends to concentrate in the first principal component of the text embeddings, suggesting that dropping the first PC is a viable simplified residualization strategy for well-behaved SAE features (Section 9.3).
