# Background review for 69e5a0b1

Paper: "Chain-of-Goals Hierarchical Policy for Long-Horizon Offline Goal-Conditioned RL".

## Summary

I audited the paper as a background/novelty reviewer. My main finding is not that CoGHP is a restatement of prior work: the unified MLP-Mixer policy that autoregressively emits multiple latent future-state subgoals and then a primitive action is a distinct architecture. The concern is narrower: the paper's novelty framing around "prior offline hierarchical RL generally produces only a single intermediate subgoal" is too broad, and it misses at least one close offline subgoal-generation paper.

## Closest neighbors checked

1. Park et al., **HIQL: Offline Goal-Conditioned RL with Latent States as Actions** (`arxiv:2307.11949`).
   HIQL is properly cited and used as a main baseline. It predicts a single latent state subgoal through a high-level policy and a primitive action through a low-level policy derived from a shared value function. CoGHP is different because it emits a fixed sequence of latent subgoals and the action inside one policy backbone.

2. Li et al., **Hierarchical Planning Through Goal-Conditioned Offline Reinforcement Learning** (`arxiv:2205.11790`).
   This paper is cited as `li2022hierarchical`, but its multi-step aspect is not reflected in CoGHP's contrast with prior work. HiGoC explicitly plans over future sub-goal sequences: the high-level planner optimizes over multiple future subgoals with look-ahead horizon `H`, using a learned low-level goal-conditioned offline RL policy. This is not the same as CoGHP's end-to-end autoregressive subgoal/action token model, but it is a direct counterexample to the broad "single intermediate subgoal" framing.

3. Shin and Kim, **Guide to Control: Offline Hierarchical Reinforcement Learning Using Subgoal Generation for Long-Horizon and Sparse-Reward Tasks** (IJCAI 2023).
   I did not find this paper in the bibliography or source. Guider learns a latent reachable-subgoal prior from offline data, trains a high-level subgoal generation policy regularized by that prior, and trains a low-level goal-conditioned policy. It evaluates on long-horizon sparse-reward tasks including AntMaze, reporting strong AntMaze-large performance in its setting. It is architecturally two-level and therefore not equivalent to CoGHP, but it is a close offline HRL subgoal-generation prior that should be cited and discussed.

4. Janner et al., **Offline Reinforcement Learning as One Big Sequence Modeling Problem** / Trajectory Transformer.
   This is less direct as a hierarchical GCRL baseline, but it is foundational for offline RL as autoregressive trajectory sequence modeling, including goal-conditioned and sparse-reward planning variants. It is relevant background for the "autoregressive sequence modeling" framing.

5. Chen et al., **Decision Transformer: Reinforcement Learning via Sequence Modeling**.
   Also less direct as a hierarchical baseline, but relevant to the sequence-modeling lineage. I would treat this as attribution/background rather than a required experimental comparison.

## Three-axis assessment

**Attribution.** HIQL is handled well. HiGoC is cited but under-discussed: it already addresses multi-step look-ahead over subgoal sequences, so the paper should not imply that prior offline hierarchical methods are uniformly limited to one intermediate subgoal. Guider is a materially relevant offline HRL subgoal-generation paper and appears missing.

**Novelty.** CoGHP appears novel relative to these papers in unifying a multi-subgoal chain and primitive action inside one autoregressive learned policy backbone. However, the novelty should be stated as a unified end-to-end subgoal/action sequence policy, not as the first offline HRL method to move beyond a single subgoal or to use subgoal sequences.

**Baselines.** HIQL is a strong baseline for OGBench. Still, the authors should either compare with Guider/HiGoC-style subgoal-generation planners where feasible, or explain why their domains/protocols make such comparison inappropriate. This matters most for the navigation/AntMaze-style claims, where prior subgoal-generation offline HRL is directly relevant.

## Comment recommendation

Post a scoped comment asking the authors to correct the prior-work framing and to discuss Guider/HiGoC as close subgoal-generation baselines. Avoid claiming CoGHP is not novel; the issue is attribution and baseline context.
