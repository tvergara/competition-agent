# Saviour notes for c45a4598

This paper proposes Controllable Information Production (CIP), an intrinsic motivation objective defined as the gap between open-loop and closed-loop Kolmogorov-Sinai entropy and implemented with an iCEM/MPC controller.

Observation 1: The experimental evidence in Section 5 is qualitative: the paper shows trajectories and a CIP curve for single pendulum, cart pole, and double pendulum, but does not report success rates, seeds, returns, runtimes, or numerical comparisons against empowerment, curiosity, DIAYN, or reward-based MPC baselines.

Observation 2: The method is intentionally scoped to low-dimensional model-based control. Section 5 uses MuJoCo-MJX with random-sampling MPC, and the limitations section states that this controller does not scale well to high-dimensional or long-horizon tasks.

Observation 3: The reproducibility signal is mixed. The paper states that code is provided at an anonymous 4open URL, but the Koala metadata lists no GitHub URLs, the submitted source tarball contains only LaTeX/figures, and the linked `readme.md` retrieved during review contained only the title.
