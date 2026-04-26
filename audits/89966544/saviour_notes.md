# Saviour notes on 89966544

VideoAfford proposes VIDA, a video-conditioned 3D affordance grounding benchmark, and a Video-LLaVA-based baseline that predicts 3D affordance masks from HOI videos and point clouds.

Observation 1: The main-result margins are positive but modest in absolute mIoU. Table 1 reports VideoAfford at 28.20 mIoU on Seen versus GREAT at 23.62, and 10.95 on Unseen versus GREAT at 8.22; this supports a real improvement, but also shows the harder Unseen setting remains very low in absolute segmentation overlap.

Observation 2: The ablation table indicates the spatial loss contributes more mIoU than the action encoder when each is added alone. From the no-module baseline, action-only gives 20.16 to 21.49 Seen and 7.120 to 8.010 Unseen, while spatial-only gives 20.16 to 24.58 Seen and 7.120 to 9.520 Unseen. This qualifies the paper's emphasis on dynamic video/action modeling.

Observation 3: The comparison protocol explicitly excludes the closest video-affordance baseline, EGO-SAG, because code is unavailable, and instead adapts image/3D affordance methods by sampling video frames and fusing embeddings. This makes the benchmark useful but means the strongest comparison is against adapted static-image pipelines rather than an independently reproduced video-affordance method.
