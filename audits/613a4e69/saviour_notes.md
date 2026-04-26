# Saviour Notes: 613a4e69

This paper proposes P2O, an RLVR framework that alternates policy updates with GEPA prompt evolution for near-zero-success hard reasoning samples.

Observation 1: The experimental protocol uses two 5,000-sample training sets, DeepScaler-5K and DeepMath-5K, Qwen3-4B as the backbone, five training epochs, temperature 0.6, six rollouts per prompt during training, and a strict binary reward requiring both boxed format and exact answer match.

Observation 2: The reflection source is not uniformly beneficial: Teacher-Ref with Kimi-K2 is best on DeepScaler-5K (65.2 average), while Self-Ref is better on DeepMath-5K (61.7 vs 57.9), suggesting the external teacher is task-dependent rather than uniformly stronger.

Observation 3: The ablation table isolates context distillation as the main load-bearing component: removing it drops the DeepScaler-5K average from 65.2 to 55.6, below the GRPO baseline, while using the same template within a rollout group drops only to 64.2.
