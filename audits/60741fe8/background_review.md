# Background and Novelty Audit: ManiPT

Paper: `60741fe8-e5a8-471c-88b0-5448b8dd620c`

Title: Prompt Tuning for CLIP on the Pretrained Manifold

Audit date: 2026-04-26

## Scope

I read the submission and compared it with the following close neighbors:

- CoOp (`arXiv:2109.01134`)
- CoCoOp (`arXiv:2203.05557`)
- MaPLe (`arXiv:2210.03117`)
- PromptSRC (`arXiv:2307.06948`)
- CoPrompt (`arXiv:2306.01195`)
- ProGrad (`arXiv:2205.14865`)
- KgCoOp (`arXiv:2303.13283`)
- LASP (`arXiv:2210.01115`)

## Summary Finding

ManiPT has a distinct mechanism: it constrains prompt tuning with dual-modality cosine consistency, uses LLM-derived text anchors, and applies normalized additive fusion between frozen CLIP features and prompt-adapted features. I do not view the paper as a direct restatement of CoOp, MaPLe, PromptSRC, or CoPrompt.

The gap is in prior-work positioning. The paper frames its contribution around preventing prompt tuning from leaving the pretrained CLIP manifold or forgetting transferable/general knowledge. Several older prompt-tuning methods address essentially that failure mode, but are not cited or used as baselines.

## Attribution

The paper cites and benchmarks many important prompt-learning methods: CoOp, CoCoOp, MaPLe, PromptSRC, CoPrompt, TAC, TAP, and LLaMP. That is a strong modern baseline set.

However, three direct predecessors are absent:

- ProGrad explicitly prevents prompt tuning from forgetting the general knowledge learned by CLIP by only applying prompt updates whose gradients are aligned with the zero-shot/general prompt direction. It evaluates few-shot, base-to-new, cross-dataset, and domain-generalization settings, which largely overlap with ManiPT.
- KgCoOp directly regularizes learned textual prompt embeddings toward hand-crafted CLIP prompt embeddings to preserve general textual knowledge and improve unseen-class generalization. This is close to ManiPT's text-side anchoring motivation.
- LASP addresses base-class overfitting in soft prompt learning by adding a text-to-text objective that keeps learned prompts close to hand-engineered textual prompts, and it also discusses visual-language misalignment.

These omissions matter because the paper's central motivation is not merely "better CLIP prompt tuning", but specifically preserving pretrained geometry/general knowledge under few-shot adaptation.

## Novelty

The novelty should be scoped as follows: ManiPT contributes a geometric manifold interpretation and a multimodal/fused-feature constraint for preserving pretrained support during prompt tuning. The broader goal of constraining prompt updates so that CLIP's general knowledge is not forgotten is already present in ProGrad, KgCoOp, and LASP.

## Baselines

The experiments include several strong recent baselines, but ProGrad and KgCoOp are especially natural comparisons for the stated failure mode. If the authors believe those methods are not comparable because ManiPT uses deep dual-modality prompting or LLM semantic anchors, the paper should say so explicitly. Otherwise, including them would make the empirical claim much cleaner.

LASP is also a relevant text-side regularization comparison because it directly addresses base-class overfitting by keeping learned prompts close to hand-crafted text prompts.

## Public Comment Rationale

This is worth posting because the missing works are not peripheral citations. They are directly tied to the paper's main explanation of why prompt tuning overfits and what kind of constraint prevents it.
