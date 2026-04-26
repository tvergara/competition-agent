# Saviour notes for 65af1f63

This paper proposes RAD, a training-free retrieval-based multi-class anomaly detector that stores anomaly-free DINOv3 features and scores test patches through global-then-local multi-level retrieval.

Observation 1: The standard MUAD table shows RAD's strongest contribution is pixel-level localization. It ties Dinomaly on MVTec image-level metrics and is below Dinomaly on VisA image-level AUROC/AP/F1, while winning the pixel-level columns on MVTec, VisA, and Real-IAD.

Observation 2: The training-free claim is operationally tied to the frozen representation and input resolution. RAD uses DINOv3 ViT-B/16 with layers 4/7/10/12 and 512-to-448 preprocessing, and the appendix reports that stronger ImageNet representations and higher resolution raise P-AUPRO.

Observation 3: The ablation supports the architecture rather than only the backbone. On MVTec-AD, multi-layer memory raises P-AP/P-F1 by 3.3/3.4 points, adding global retrieval gives another 1.0/0.8, and spatial conditioning adds 0.6/0.5 on the strongest variant.
