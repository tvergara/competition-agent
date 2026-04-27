# Background Review: Sparse Autoencoders are Capable LLM Jailbreak Mitigators

## Paper Summary
The paper proposes **Context-Conditioned Delta Steering (CC-Delta)**, an inference-time defense against jailbreak attacks using Sparse Autoencoders (SAEs). The method identifies jailbreak-relevant features by comparing SAE latent representations of harmful requests in two contexts: a plain (harmful) context and a jailbreak-wrapped context. By using token-level matching to compare the *exact same* tokens of the harmful request across these contexts, and applying a Wilcoxon signed-rank test with FDR correction, the authors select a sparse set of features for mean-shift steering in SAE space. The authors claim that this approach achieves better safety-utility tradeoffs and superior out-of-distribution (OOD) generalization compared to dense-space steering methods like CAA and other baselines like Circuit Breakers.

## Comparison with Prior Work

### 1. [O'Brien et al. 2024] Steering Language Model Refusal with Sparse Autoencoders
- **Relation:** Foundational work for SAE-based safety steering.
- **Comparison:** O'Brien et al. identify features associated with general refusal. CC-Delta specifically targets jailbreak-induced changes in harmful request representations. CC-Delta claims better utility preservation (e.g., MMLU) by using more targeted feature selection.
- **Citation:** Correctly cited and distinguished.

### 2. [Bhargav & Zhu 2025] Feature-Guided SAE Steering for Refusal-Rate Control using Contrasting Prompts (arXiv:2511.00029)
- **Relation:** Highly similar method using "contrasting prompts" to select SAE features for refusal control.
- **Comparison:** Bhargav & Zhu use (harmful vs harmless) contrast pairs and a composite score (magnitude + consistency) to select features. CC-Delta uses (harmful vs jailbroken) contrast and token-level matching. CC-Delta is more specific to jailbreak defense, whereas Bhargav & Zhu is more general for refusal control.
- **Citation:** **MISSING.** This is a significant omitted prior work given the similarity in using contrasting prompts for SAE steering.

### 3. [Yeon et al. 2025] GSAE: Graph-Regularized Sparse Autoencoders for Robust LLM Safety Steering (arXiv:2512.06655)
- **Relation:** Another recent work on SAE-based safety steering.
- **Comparison:** GSAE uses graph regularization to find distributed safety representations and a two-stage gating mechanism.
- **Citation:** **MISSING.** Relevant for the discussion of how safety features are represented and steered in SAE space.

### 4. [Rimsky et al. 2024] Steering Llama 2 with Contrastive Activation Addition (CAA)
- **Relation:** Primary baseline for activation steering.
- **Comparison:** CAA operates in dense activation space. CC-Delta moves this to sparse SAE space and uses more specific token-level selection.
- **Citation:** Correctly cited and used as a baseline.

### 5. [Rimsky et al. 2024] One-shot Optimized Steering Vectors Mediate Safety-relevant Behaviors in LLMs (arXiv:2502.18862)
- **Relation:** Investigates steering generalization from single examples.
- **Comparison:** Relevant for the "delta" approach which can be seen as a form of one-shot or small-sample optimization.
- **Citation:** **MISSING.**

## Three-Axis Assessment

### 1. Attribution
The paper identifies the foundational work of O'Brien et al. (2024) but fails to cite very recent and highly relevant neighbors from late 2025: **Bhargav & Zhu (2025)** and **Yeon et al. (2025)**. These works also explore SAE-based safety steering and "contrasting prompt" selection, which are central to the paper's claims of novelty.

### 2. Novelty
The core novelty—**Context-Conditioned Delta Steering** with **token-level matching**—is a well-motivated and likely novel specific refinement for the jailbreak setting. By comparing the same tokens in different contexts, the method isolates the "jailbreak vector" more precisely than broader contrastive methods. The use of rigorous statistical filtering (Wilcoxon + FDR) also adds to the technical contribution. However, the claim to be the first to apply activation steering in SAE space for safety should be bounded against Bhargav & Zhu (2025) and O'Brien et al. (2024).

### 3. Baselines
The experimental comparison is strong against dense steering methods (CAA, LinearAcT) and architectural methods (Circuit Breakers, LAT). However, it lacks a direct empirical comparison against **contemporary SAE-based safety steering methods** like those in Bhargav & Zhu (2025) or GSAE (Yeon et al. 2025). Including at least one of these as a baseline would significantly strengthen the claim that CC-Delta's specific feature selection is superior to other SAE-based selection methods.

## Overall Verdict
**Neutral.** The paper presents a technically sound and effective method with strong empirical results in a difficult setting (jailbreak defense). However, the omission of very close prior works (Bhargav & Zhu, GSAE) and the lack of comparison against them weakens the novelty claim. The "Context-Conditioned" approach is a valuable specific insight that deserves recognition, but its contribution should be more clearly positioned relative to the emerging field of SAE safety steering.
