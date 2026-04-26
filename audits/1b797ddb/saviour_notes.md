# Saviour notes for 1b797ddb

The paper proposes DDP-WM, a sparse/disentangled latent world model for robotic MPC that focuses heavy prediction on localized primary dynamics and updates background tokens cheaply.

Observation 1: The main performance table is broader than the Push-T headline: against DINO-WM, DDP-WM reports 100% vs 98% on PointMaze, 98% vs 90% on Push-T, 98% vs 96% on Wall, and lower Chamfer distance on Rope and Granular (0.31 vs 0.41 and 0.24 vs 0.26).

Observation 2: The efficiency numbers mix several measurement types and hardware contexts: FLOPs are reported only for Push-T and Wall, single-step throughput uses one NVIDIA 2080 Ti with batch size 128, and full MPC decision-loop latency uses one NVIDIA A5880.

Observation 3: The high-precision localization mechanism is a major quantitative component: on Push-T it raises mask IoU from 0.3446 to 0.8935 and recall from 0.5172 to 0.9845, and it cuts 5-step pixel error both without LRM (788 to 427) and with LRM (468 to 361).
