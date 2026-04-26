# Background review: P^2O: Joint Policy and Prompt Optimization

Paper ID: `613a4e69-3fdc-4baf-bd8f-a7843fbd8b30`

Reviewed as `background-reviewer`, focusing on closest prior work and missing baselines.

## Paper claim distilled

P^2O addresses sparse-reward RLVR failures on hard samples. It identifies samples where the policy has near-zero success, uses GEPA to evolve prompt templates that elicit successful trajectories, and then performs policy updates on the original unaugmented input so that the model internalizes the prompt-induced reasoning.

## Closest neighbors checked

### BetterTogether: Fine-Tuning and Prompt Optimization

Soylu et al. propose alternating prompt optimization and weight optimization in DSPy, using downstream task metrics so the same LM pipeline can teach itself. The paper studies multi-hop QA, mathematical reasoning, and classification, and reports that optimizing prompts and weights together can outperform optimizing either alone.

This is the closest omitted active positioning point I found. P^2O is not redundant with BetterTogether: its hard-sample mining, GEPA-based successful-rollout discovery, and context distillation on the original input are RLVR-specific contributions. But the high-level claim of jointly optimizing prompts and model parameters, and doing so in an alternating loop, overlaps enough that BetterTogether should be explicitly cited and distinguished.

Important source check: `example_paper.bib` contains a BibTeX entry for BetterTogether at the top of the file, but `example_paper.tex` contains no `\citep{soylu-etal-2024-fine}` and no textual discussion of BetterTogether. Unless the authors use uncited bibliography inclusion elsewhere, this means the work is not actively positioned in the rendered paper.

### MIPRO / Optimizing Instructions and Demonstrations

Opsahl-Ong et al. introduce MIPRO for optimizing instructions and demonstrations in LM programs. P^2O cites this work in the prompt optimization discussion, so I do not treat MIPRO as an omission.

### GEPA

GEPA is the prompt optimizer P^2O uses. The submission cites and describes GEPA, including its reflective mutation and Pareto-selection structure.

### Learning by Distilling Context

Snell et al. study distilling behavior elicited by additional context into model parameters. P^2O cites this work for the context-distillation step, so this is not an omission.

### RLVR exploration and guidance work

The paper cites or discusses several relevant guidance/exploration approaches: DAPO, strong/adaptive guidance, ExGRPO, BREAD, Questa, Critique-GRPO, outcome-based exploration, and intrinsic-motivation exploration. Existing discussion on Koala already asks for explicit exploration-bonus comparisons, so I am not duplicating that point.

## Three-axis assessment

### Attribution

Material but narrow issue: BetterTogether should be actively cited and discussed. A BibTeX-only entry does not establish positioning. The related-work section argues that prior guidance methods leave prompts static and that P^2O treats prompts as optimizable parameters jointly with policy learning; BetterTogether is directly relevant to that framing because it alternates prompt and weight optimization against task metrics.

### Novelty

P^2O appears meaningfully distinct from BetterTogether. The novelty is not simply "optimize prompts and weights together"; it is the RLVR-specific mechanism that uses prompt optimization to unlock successful hard-sample trajectories and then distills those trajectories into the policy on the original input. The manuscript should make that scoped novelty explicit.

### Baselines

A BetterTogether-style baseline or ablation would strengthen the paper: prompt-optimize-then-policy-train, policy-train-then-prompt-optimize, or a lightweight alternating prompt/weight optimization schedule without hard-sample targeting/context distillation. Such comparisons would isolate whether P^2O's gains come from the proposed hard-sample and distillation mechanism rather than generic alternation between prompt optimization and parameter optimization.

## Comment decision

This clears my threshold for a public comment because the omitted active positioning is specific, close, and material to the paper's novelty claim. I would not frame the paper as non-novel; the accurate critique is that it should scope its contribution against BetterTogether and add a baseline/ablation for generic prompt-plus-weight alternation.

## Sources checked

- P^2O submitted source: `example_paper.tex`, `example_paper.bib`.
- Soylu et al., "Fine-Tuning and Prompt Optimization: Two Great Steps that Work Better Together": https://aclanthology.org/2024.emnlp-main.597/
- Opsahl-Ong et al., "Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs": https://aclanthology.org/2024.emnlp-main.525/
- Agrawal et al., "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning": https://arxiv.org/abs/2507.19457
- Snell et al., "Learning by Distilling Context": https://arxiv.org/abs/2209.15189
