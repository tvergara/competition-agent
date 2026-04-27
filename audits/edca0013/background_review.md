# Background and Novelty Review: SAME

## Claimed Contributions
The paper identifies two primary failure modes in Multimodal Continual Instruction Tuning (MCIT) for Mixture-of-Experts (MoE) models: **router drift** (expert selection becomes inconsistent) and **expert drift** (shared experts are overwritten). It proposes the **SAME** (StAbilized Mixture-of-Experts) framework, which introduces three mechanisms:
1. **Spectral-aware Routing**: Stabilizes expert selection by decomposing routing dynamics into orthogonal subspaces and updating only task-relevant directions.
2. **Curvature-aware Scaling**: Regulates expert updates using historical input covariance to bound functional deviation.
3. **Adaptive Expert Activation**: A task-level mechanism to freeze experts with low current utility but high historical importance.

## Prior Work Comparison

1. **Gradient Projection Memory (GPM; Saha et al., 2021)**: GPM uses SVD to find the signal subspace of activations and constrains updates to the orthogonal null space. **SAME's Spectral-aware Routing** is a direct application of GPM/OWM to the gating network of an MoE module.
2. **Natural Gradient Descent (Amari, 1998)**: Scaling updates by the inverse of the Fisher Information Matrix (often approximated by input covariance). **SAME's Curvature-aware Scaling** (Eq. 14) is an application of Natural Gradient (or EWC-style regularization) to MoE experts.
3. **MoELoRA (Luo et al., 2024)**: The primary architecture baseline. SAME extends MoELoRA by adding the stability mechanisms.
4. **XSMoE: Efficient Multimodal Streaming Recommendation via Expandable Side Mixture-of-Experts (Qu et al., 2025)**: A close neighbor that addresses drift in MoE-based multimodal systems using expandable experts and utilization-based pruning. SAME fails to cite this relevant work on MoE drift management.
5. **TalkLoRA: Communication-Aware Mixture of Low-Rank Adaptation (Mu et al., 2026)**: A very recent neighbor that stabilizes MoE-LoRA routing via expert communication. SAME does not position its routing stabilization against this concurrent approach.

## Three-Axis Assessment

### Attribution
The paper correctly cites the foundational GPM and MoELoRA papers but fails to position its "router drift" and "expert drift" framing against existing work on MoE stability and expansion, such as **XSMoE (Qu et al., 2025)**. The "curvature-aware scaling" is presented as a "Riemannian manifold metric" approach, which under-attributes its direct heritage to **Natural Gradient (Amari, 1998)** and its variants in continual learning (e.g., EWC, K-FAC).

### Novelty
The novelty is **incremental**. The core idea of using orthogonal subspace projections (GPM) and covariance-based scaling (Natural Gradient) for stability is well-established in the continual learning literature. Applying these specifically to the router and experts of an MoE model is a logical extension rather than a fundamental breakthrough. The "Adaptive Expert Activation" is a sensible but relatively straightforward heuristic based on utilization.

### Baselines
The paper omits a direct comparison with a standard GPM-protected LoRA or a vanilla Natural Gradient baseline, which would have isolated whether the MoE-specific components of SAME provide gains beyond general continual learning stabilizers. It also omits **XSMoE (Qu et al., 2025)** as a relevant drift-mitigation baseline for MoE.

## Technical Soundness
There is a **major technical flaw** in Equation 11:
2250488\Delta W_{G}^{t} = \Delta W_{||}^{t} + \Delta W_{\perp}^{t}2250488
The paper claims that $\Delta W_{\perp}^{t}$ preserves old-task knowledge by being in the null space. However, $\Delta W_{||}^{t}$ is explicitly in the **signal space** of the router inputs (which includes old tasks). By summing the two, the final update $\Delta W_{G}^{t}$ is no longer orthogonal to the old-task subspace. Since old inputs ^{old}$ lie primarily in {||}$, the update $\Delta W_{||}^{t}$ will explicitly and destructively alter the router's outputs for old tasks, negating the "preservation" claim of the orthogonal decomposition.

## Verdict
**Clearly not novel and mathematically flawed.** The paper rebrands existing continual learning techniques (GPM, Natural Gradient) for MoE architectures and introduces a summation update (Eq. 11) that negates the very stability property it claims to provide.
