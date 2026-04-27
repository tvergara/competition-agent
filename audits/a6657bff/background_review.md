# Background and Novelty Assessment: Solving the Offline and Online Min-Max Problem of Non-smooth Submodular-Concave Functions...

## Claimed Contributions
The paper introduces a **zeroth-order approach** to solving min-max and max-min problems where the objective function is submodular with respect to the minimizer and concave with respect to the maximizer. The proposed algorithm, **ZO-EG**, leverages the **Lovász extension** to handle the submodular component and **Gaussian smoothing** to handle the potentially non-smooth concave component.

Key contributions include:
1.  A zeroth-order framework based on the extragradient method that requires only function evaluations.
2.  Theoretical proof of convergence to an $\epsilon$-saddle point in the offline setting with $O(m^2 \epsilon^{-2})$ complexity.
3.  Dynamic regret (duality gap) bounds of $O(\sqrt{N \bar{P}_N})$ for the online setting.
4.  Demonstrated application in online adversarial image segmentation, outperforming standard U-Net baselines.

## Comparison with Closest Neighbors

1.  **Minimisation of Submodular Functions Using Gaussian Zeroth-Order Random Oracles** (Farzin et al., Oct 2025):
    - *Relationship*: Direct predecessor by the same authors that established the zeroth-order submodular minimization framework.
    - *Citation*: Cited.
    - *Assessment*: This paper is a logical and substantial extension of the previous work to the min-max and online min-max regimes.

2.  **Submodular + Concave** (Mitra et al., 2021):
    - *Relationship*: The first work to formally study the maximization of functions of the form $G(x) + C(x)$ (DR-submodular + concave).
    - *Citation*: **Not cited.**
    - *Assessment*: Mitra et al. provide essential context for the "submodular-concave" function class. While their focus was on maximization and this paper is on min-max, the structural insights into this class are highly relevant and should have been acknowledged.

3.  **Polyhedral aspects of Submodularity, Convexity and Concavity** (Iyer & Bilmes, 2015):
    - *Relationship*: Foundational work exploring the relationships between submodularity and concavity/convexity.
    - *Citation*: **Not cited.**
    - *Assessment*: This paper provides the mathematical background for the very connections the current paper exploits.

4.  **Minimax Optimization with Convex-Submodular Objective Functions** (Adibi et al., 2022):
    - *Relationship*: Recent work on min-max problems with a related function class (convex-submodular).
    - *Citation*: Cited and discussed.
    - *Assessment*: The paper correctly differentiates itself by handling the submodular-concave class and using a zeroth-order approach.

5.  **Learning with Submodular Functions: A Convex Optimization Perspective** (Bach, 2013):
    - *Relationship*: Foundational reference for the Lovász extension and submodular minimization as convex optimization.
    - *Citation*: Cited.

## Three-Axis Assessment

*   **Attribution**: The paper is well-grounded in classical theory and the authors' recent work. However, it omits key "middle-ground" literature like **Mitra et al. (2021)** and **Iyer & Bilmes (2015)**, which established the importance and properties of the submodular-concave class.
*   **Novelty**: The novelty is **moderate to high**. Extending zeroth-order submodular optimization to the min-max setting is a non-trivial theoretical achievement with clear practical utility in robust and adversarial settings. The proofs for both offline and online settings add significant value.
*   **Baselines**: The application to image segmentation is interesting, but the paper **lacks a comparison against other optimization-based baselines**. A comparison with first-order methods (to show the ZO gap) or with other combinatorial min-max solvers would have better contextualized the performance of ZO-EG.

## Overall Verdict
**Neutral.** The paper presents a solid theoretical contribution and fills an important gap in the intersection of zeroth-order and submodular optimization. Its main strength is the rigorous convergence analysis in both offline and online settings. Its impact would be improved by better positioning within the broader submodular-concave literature and more diverse algorithmic baselines.
