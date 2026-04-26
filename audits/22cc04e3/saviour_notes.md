# Saviour Notes: VETime (22cc04e3)

This paper proposes VETime, a multi-modal foundation model for zero-shot time-series anomaly detection that unifies 1D temporal and 2D visual representations.

### Observation 1: Parameter-Efficient Asymmetric Tuning
The architecture employs a dual-encoder setup where the vision encoder (MAE ViT-Base) remains completely frozen, while the time-series encoder (based on Time-RCD) is fine-tuned using Low-Rank Adaptation (LoRA) with rank 8 and alpha 16 (Section 5.4, Appendix C4). This asymmetric strategy allows the model to preserve general visual features while specializing the temporal pathway for the detection task.

### Observation 2: Auxiliary Reconstruction Performance Driver
The model incorporates a dedicated reconstruction head and an associated MSE loss term as an auxiliary task. According to the ablation study in Table 7, removing this reconstruction component results in a consistent performance degradation across multiple datasets (e.g., Affiliation-F1 drops by ~1.6% on NAB). This confirms that learning to reconstruct the original sequence is a vital regularizer that enhances the primary anomaly classification task.

### Observation 3: Scaling Plateau for Vision Backbones
Experimental results in Table 6 indicate an "efficiency plateau" for the visual modality. Moving from an MAE (Base) to an MAE (Large) encoder—a 3.5x increase in parameters—yields only marginal gains and even results in performance degradation on certain datasets like YAHOO. This suggests that the bottleneck for vision-based anomaly detection may reside more in the image conversion and temporal alignment stages than in the capacity of the visual feature extractor itself.
