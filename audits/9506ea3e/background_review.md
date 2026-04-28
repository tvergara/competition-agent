# Background & Novelty Audit: Robust and Efficient Zeroth-Order LLM Fine-Tuning via Adaptive Bayesian Subspace Optimizer (BSZO)

## Paper Summary
This paper introduces **BSZO**, a zeroth-order (ZO) optimization framework for fine-tuning Large Language Models (LLMs) that operates in a low-dimensional subspace. The primary contribution is the use of **Kalman filtering** and **Bayesian inference** to aggregate finite-difference measurements from multiple perturbation directions within a single batch. This approach aims to reduce the high variance of ZO gradient estimates and improve robustness to low-precision (fp16/bf16) training environments. The authors claim state-of-the-art performance on various LLM benchmarks (OPT, Mistral, RoBERTa) while maintaining inference-level memory efficiency.

## 5 Most Similar Prior Works
1.  **MeZO (Malladi et al., 2023)**: The foundational work for memory-efficient LLM fine-tuning using zeroth-order optimization with a single random perturbation. BSZO directly builds on this by extending the perturbation to a hBcdimensional subspace.
2.  **SubZero (Yu et al., 2024)**: Introduces random subspace zeroth-order optimization for LLMs. This work established the viability of using low-dimensional subspaces to stabilize ZO training, which BSZO also employs. (**Omitted in BSZO**).
3.  **P-GAP (Mi et al., 2025)**: "Towards Fast LLM Fine-tuning through Zeroth-Order Optimization with Projected Gradient-Aligned Perturbations." This method also uses projected gradients in a low-dimensional space to reduce variance. (**Omitted in BSZO**).
4.  **AGZO (Lin et al., 2026)**: "Activation-Guided Zeroth-Order Optimization for LLM Fine-Tuning." A very recent work that uses activation structures to guide the subspace selection on the fly. (**Omitted in BSZO**).
5.  **LOREN (Seung et al., 2025)**: "Low-Rank Curvature for Zeroth-Order Optimization in LLM Fine-Tuning." Uses a low-rank block diagonal preconditioner to capture curvature information, similar in spirit to BSZO's goal of improving convergence via adaptive noise/curvature modeling. (**Omitted in BSZO**).

## Three-Axis Assessment

### Attribution
The paper has significant gaps in its attribution of prior work on subspace-based zeroth-order optimization for LLMs. Specifically:
-   **SubZero (Yu et al., 2024)** and **P-GAP (Mi et al., 2025)** are direct precursors that established the subspace/low-dimensional perturbation paradigm in this specific domain.
-   The claim in the Introduction that "existing methods essentially perform updates in a one-dimensional space" is factually incorrect as it ignores these published subspace methods.
-   **AGZO (Lin et al., 2026)** is highly relevant as it addresses the same problem (variance reduction in ZO-LLM) using more sophisticated subspace selection techniques (activation-guided vs random).

### Novelty
BSZO's genuine novelty lies in the **Bayesian formulation** of the gradient estimation problem. While using subspaces for ZO is known, treating directional derivatives as noisy observations and using **Kalman filtering** for their fusion is a novel and principled way to aggregate information within a batch. This allows for explicit uncertainty quantification and adaptive noise modulation via residuals, which appears to be a distinct contribution from the simple projection or averaging used in earlier subspace works. However, the overall novelty is tempered by the fact that the "subspace" framing is already a competitive area with multiple existing solutions.

### Baselines
The experimental evaluation is incomplete. While BSZO compares against the foundational MeZO and some recent variants like HiZOO and LOZO, it lacks comparisons with the more directly relevant subspace/low-rank methods:
-   **P-GAP** and **AGZO** are the most critical missing baselines, as they also attempt to solve the ZO variance problem by restricting updates to low-dimensional spaces. Without these comparisons, it is difficult to assess whether the Bayesian aggregation in BSZO provides a material advantage over other subspace projection strategies.

## Overall Verdict
**Not Novel / Attribution Issues.** While the Bayesian/Kalman filter approach is technically interesting and potentially effective, the paper fails to cite and compare against the core body of literature on subspace-based ZO optimization for LLMs (SubZero, P-GAP, AGZO). The central claim of moving beyond 1D updates is presented as a new observation, whereas it has been the focus of multiple recent works.
