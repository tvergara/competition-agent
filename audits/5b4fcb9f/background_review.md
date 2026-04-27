# Background and Novelty Review: Soft Forward-Backward Representations (SFB)

## 1. Attribution and Prior Work
The paper correctly identifies the limitations of the standard **Forward-Backward (FB) Representations (Touati & Ollivier, 2021)** in handling non-linear reinforcement learning problems. It also provides a comprehensive background on RL with **General Utilities (Kumar et al., 2022; Zahavy et al., 2021)** and correctly positions SFB as a scalable, zero-shot solution for this problem class.

The citation of very recent work such as **Temporal Difference Flows (Farebrother et al., 2025)** and **Behavioral Foundation Models (Pirotta et al., 2024)** demonstrates a high degree of grounding in the current state-of-the-art for foundation model RL.

## 2. Novelty and Technical Contribution
The primary contribution is the introduction of a maximum entropy (soft) variant of the FB algorithm. This is a technically sound and logical extension that allows the framework to retrieve a richer class of stochastic policies, which is essential for optimizing general utilities (e.g., pure exploration or constrained RL). 

The theoretical result (Theorem 4.2) establishing that Soft FB captures $\epsilonhBcoptimal solutions for any differentiable function of occupancy measures is a valuable contribution that provides a principled justification for the method. The hBcreparameterization to a bounded hypersphere is also a practical improvement for test-time optimization.

## 3. Omitted Baselines and Comparative Context
While the paper compares SFB against standard FB, it omits a critical comparison with the **Mixture of Deterministic Policies** approach established by **Zahavy et al. (2021)**. 

Zahavy et al. proved that any convex MDP objective (a subset of general utilities) can be optimized by a mixture of deterministic policies. Since the standard FB framework already retrieves a family of deterministic policies, a natural baseline would be to mix the deterministic policies captured by FB and compare this mixture against the single Markov policy produced by Soft FB. 

Demonstrating that a single Markov policy from SFB is superior to, or more practical than, a non-Markovian mixture of FB policies would significantly strengthen the paper\"s claims regarding the necessity of the soft variant.

Furthermore, the quantitative evaluation on didactic environments (Table 1) would benefit from comparisons against established general utility algorithms, such as those proposed by **Kumar et al. (2022)** or **Mutti et al. (2023)**, to establish a broader context for the zero-shot performance.

