# Background and Novelty Audit: FlowConsist (6e607765)

## Claimed Contributions
The paper identifies two main issues in current fast flow models:
1. **Trajectory Drift:** Caused by using conditional velocities (derived from random noise-data pairs) as a surrogate for marginal velocities in training.
2. **Error Accumulation:** Propagated approximation errors over large time spans.

The proposed solution, **FlowConsist**, replaces conditional velocities with self-predicted marginal velocities and introduces a **trajectory rectification strategy** that aligns marginal distributions at every time step along the ODE path.

## 5 Closest Prior Works
1. **Rectified Flow** (Liu et al., 2022/2023): Foundational work on straightening ODE paths for one-step generation.
2. **MeanFlow** (Geng et al., 2025): The primary framework upon which this work builds, using average velocity for one-step mapping.
3. **Improved Mean Flows (iMF)** (Geng et al., 2025b): Concurrent work that also replaces conditional velocity with self-predicted marginal velocity to stabilize training.
4. **Distribution Matching Distillation (DMD)** (Yin et al., 2024): Inspired the distributional alignment strategy, though DMD typically only aligns at the endpoints.
5. **Stable Velocity** (Yang et al., 2026): A nearly concurrent work (posted Feb 5, 2026) that identifies the "variance" caused by conditional velocity surrogates as the primary cause of instability in Flow Matching.

## Three-Axis Assessment

### 1. Attribution
The paper provides excellent coverage of the fast-flow lineage (Consistency Models, MeanFlow, etc.). However, it omits two key neighbors:
- **PeRFlow** (Yan et al., 2024): A significant work on piecewise straightening of flow trajectories which is directly relevant to the "trajectory consistency" theme.
- **Stable Velocity** (Yang et al., 2026, `2602.05435`): This paper was posted on arXiv just one day before FlowConsist. It addresses the exact same issue: the gap/variance between conditional and marginal velocities. While it may be a true concurrent collision, its absence leaves the "previously overlooked" claim vulnerable.

### 2. Novelty
- **Trajectory Drift Theory:** The formalization of the conditional-marginal gap as "trajectory drift" (Theorems 1 and 2) is elegant and provides a deeper mathematical grounding than the "standard regression form" motivation in iMF. However, the *problem itself* (variance in FM training targets) and the *solution* (using marginal/self-predicted velocity) are concurrently addressed in **Stable Velocity** and **iMF**.
- **Trajectory Rectification:** The extension of DMD's distribution matching to *every* time step along the trajectory (Eq 11) is a non-trivial and novel technical contribution. Most distillation methods (like DMD or DMD2) focus on the endpoint $t=0$, whereas this method enforces consistency throughout the path.

### 3. Baselines
The paper compares against the standard state-of-the-art suite (iMF, MeanFlow, sCM, etc.).
- **Missing Baseline:** It does not compare against **PeRFlow** or **Stable Velocity**. Given that Stable Velocity achieved very strong results (though primarily on multi-step), its performance in the 1-NFE regime would have been a valuable comparison for the "trajectory consistency" claim.

## Verdict
**Novel with minor attribution gaps.** The paper's strength lies in its "trajectory rectification" extension and its formal mathematical analysis of the drift phenomenon. The novelty of the drift identification is slightly overstated given concurrent work, but the overall framework is technically sound and achieves superior empirical results (1.52 FID).

**Key Supporting Works:**
- **Stable Velocity** (Yang et al., 2026) for the variance/drift analysis.
- **iMF** (Geng et al., 2025b) for the implementation of self-predicted marginal velocity.
- **DMD** (Yin et al., 2024) for the distributional alignment strategy.
