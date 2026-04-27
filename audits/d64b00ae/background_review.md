# Background and Novelty Review: Rel-MOSS

This review focuses on the attribution, methodological novelty, and experimental rigor of the **Rel-MOSS** framework for imbalanced entity classification on relational databases (RDB).

## 1. Attribution and Prior Work

The manuscript correctly identifies **Relational Deep Learning (RDL)** as a recently formalized subfield (Fey et al., 2024) and positions its contribution at the intersection of RDL and class-imbalanced learning. It provides citations for foundational graph over-sampling methods such as **GraphSMOTE** (Zhao et al., 2021) and **GraphSHA** (Li et al., 2023).

However, there is a notable gap in the empirical comparison with the state-of-the-art (SOTA). While the paper cites **LTE4G** (Yun et al., 2022) and **GraphSR** (Zhou & Gong, 2023) in the bibliography, it fails to include them as baselines in the main evaluation (Table 1). **LTE4G** specifically addresses class and degree imbalance in GNNs via an expert-student architecture and knowledge distillation, representing a more modern and potentially stronger baseline than the included classic SMOTE variants. Similarly, **GraphSR** introduces a data augmentation algorithm that leverages reinforcement learning to select and label unlabelled nodes, which is a more advanced approach to imbalance than the linear interpolation employed in Rel-MOSS.

## 2. Methodological Novelty

The primary novelty claim of Rel-MOSS is that it is the first to investigate the class imbalance problem specifically within the context of RDL. While this application domain is novel, the individual components of the framework represent incremental combinations of established techniques:

- **Rel-Gate (Relation-wise Gating Controller):** This module uses an attention-based mechanism to weight neighborhood messages from different relations. While the motivation is to prioritize minority-leaning relations, the technical formulation (Eq. 9) is conceptually similar to relation-specific attention in **Heterogeneous Graph Transformers (HGT)** (Hu et al., 2020), albeit simplified to a relation-level scalar.
- **Rel-Syn (Relation-guided Minority Synthesizer):** The use of "relational signatures" (entity type histograms and fan-in/fan-out distributions) to guide over-sampling is a practical extension of SMOTE for heterogeneous graphs. However, the use of basic structural features to enhance graph representation learning is well-established in graph mining literature.

## 3. Experimental Rigor and Result Interpretation

I have identified a discrepancy in the reporting of improvements in Table 1, specifically for the **amazon-user-churn** dataset:

- For the **Balanced Accuracy (B-Acc)** metric, the best baseline is underlined as **RDL (0.6309)**.
- However, the reported score for **GraphSHA (0.6347)** on the same dataset is materially higher and should have been identified as the best baseline.
- The "Improvement" row for this dataset (0.86%) appears to be calculated relative to **RDL** (`(0.6363 - 0.6309) / 0.6309 = 0.855%`), which inflates the reported gain. If calculated against the actual best baseline (**GraphSHA**), the improvement would be only **0.25%** (`(0.6363 - 0.6347) / 0.6347`).

Furthermore, for several datasets (e.g., **f1-driver-dnf**), the reported improvements are within the range of one standard deviation of the best baseline, suggesting that the performance gains may not be statistically significant in all cases.

## Conclusion

While Rel-MOSS provides a practical integration of gating and signature-based over-sampling for RDL, its novelty is constrained by the existence of more advanced imbalanced GNN methods (e.g., LTE4G, GraphSR) which were not included in the head-to-head comparison. The misidentification of the best baseline for the amazon-user-churn dataset further necessitates a more nuanced framing of the empirical results.
