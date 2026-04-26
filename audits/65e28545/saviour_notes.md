# Saviour Notes: 65e28545

This paper proposes a multi-view RGB-D 4D world model for robotic manipulation plus test-time trajectory-latent action inference.

Observation 1: The training recipe deliberately mixes conditioning regimes: with probability 0.5 it replaces the noise region with only the first frame of the first view, with probability 0.5 it uses the full video latent from the first view and masks arbitrary frames, and later gradually masks the trajectory latent with a null token.

Observation 2: The real-robot success-rate protocol is two-stage: for each trial, the authors first verify whether the predicted video completes the task, count incorrect videos as failures, and only then decode/interpolate/execute actions for videos judged correct.

Observation 3: The appendix reports a concrete view-budget tradeoff on RLBench: success improves from 68.6% with 1 view to 72.6% with 3 views, but 4-5 views give only marginal gains (72.9/73.1) while increasing runtime to 1.20x/1.35x relative to 3 views.
