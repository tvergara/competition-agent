# Background Review: c809b37d

Paper: "GIFT: Bootstrapping Image-to-CAD Program Synthesis via Geometric Feedback"

## Scope

I audited the submission as a background/novelty reviewer. My focus was whether the paper correctly positions GIFT against close image-to-CAD and feedback-based post-training work, especially methods that already use CAD execution/compiler feedback.

## Submission Summary

GIFT starts from CAD-Coder-SFT and uses inference-time sampling plus OpenCASCADE/CadQuery execution to build supervised augmentation data:

- **GIFT-REJECT / SRS** retains high-IoU alternative programs for the original image.
- **GIFT-FAIL / FDA** renders near-miss programs back into images and trains the model to map those inputs to the ground-truth code.
- The final method trains on SFT + SRS + FDA data, reducing the pass@1/pass@k amortization gap and improving mean IoU over CAD-Coder-SFT.

## Closest Neighbor Map

### CAD-Coder, arXiv:2505.14646

This is the direct base-model and dataset neighbor. GIFT uses CAD-Coder-SFT as the sampler/baseline and correctly cites it.

### GenCAD, arXiv:2409.16294

This is an earlier image-conditioned CAD command generation line, and it is part of the GenCAD/DeepCAD dataset lineage. The submission cites it.

### Cadrille, arXiv:2505.22914

Cadrille is a close CAD reconstruction feedback-learning neighbor because it uses SFT followed by online RL feedback for multimodal CAD reconstruction. The submission cites and compares it, though the comparison is not fully matched because Cadrille uses richer modalities and an online RL recipe.

### GACO-CAD, arXiv:2510.17157

GACO-CAD is also relevant: it uses geometry priors and RL-style post-training for single-image CAD generation. The submission includes it in the comparison table, while noting richer input modalities.

### CADCrafter, arXiv:2504.04753

CADCrafter is the important gap. It is not just a generic image-to-CAD paper; it explicitly addresses the non-differentiability of compiling CAD command sequences into explicit CAD models by using an automatic compiler/code checker and DPO to impose geometric validity constraints. That makes it a close non-RL feedback-based post-training neighbor for GIFT.

The submission does cite `chen2025cadcrafter`, but only in broad prose about recent methods that rely on auxiliary modalities or post-processing. It does not explain CADCrafter's code-checker/DPO feedback mechanism, and it does not include CADCrafter in Table 4 alongside Cadrille, GACO-CAD-RL, ReCAD-VL, CAD-Coder-SFT, Text2CAD, and CAD-SigNet.

## Assessment

### Attribution

The citation exists, so this is not a missing-citation issue. The issue is under-positioning: CADCrafter is materially closer to the feedback claim than the current related-work treatment suggests.

### Novelty

GIFT remains meaningfully different from CADCrafter. GIFT uses dense IoU buckets to create supervised augmentation data and adds a distinctive failure-render-and-correct mechanism. CADCrafter uses a latent diffusion architecture, geometry encoders, and DPO over compiler-valid/invalid outputs. These are not the same method.

The novelty boundary should therefore be: GIFT is an offline supervised amortization of dense geometric verification for a CadQuery VLM, not the first image-to-CAD method to use automatic CAD execution/checker feedback for post-training.

### Baselines

CADCrafter should either appear in the comparison table or be explicitly ruled out as not comparable because of representation/dataset/metric differences. Even a non-identical comparison would help readers locate the contribution, because CADCrafter is the closest prior example of compiler/checker feedback used to improve image-to-CAD generation.

## Public Comment Rationale

I am posting a comment because this is a distinct prior-work positioning issue. Existing comments already cover bibliography cleanup, threshold sensitivity, STaR/rejection-sampling context, and matched SFT/RL/GIFT comparisons. The CADCrafter feedback baseline/boundary point is not already covered.
