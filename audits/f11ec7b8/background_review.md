# Background Review: DUEL

Paper: `f11ec7b8-9229-4dba-a0b6-f7515cfde172`

## Claim Checked

The submission argues that a pretrained masked diffusion denoiser plus a deterministic unmasking rule defines a concrete test-time generative distribution. Since the position policy is deterministic, likelihood evaluation for a given sequence follows the single induced unmasking path rather than marginalizing over all possible ordered partitions. This yields an exact likelihood/perplexity for deterministic MDM samplers.

## Prior Work Read

- Hoogeboom et al., **Autoregressive Diffusion Models** (`arXiv:2110.02037`): establishes the ARDM/AO-ARM bridge and likelihood-bound perspective for arbitrary-order generation.
- Ou et al., **Your Absorbing Discrete Diffusion Secretly Models the Conditional Distributions of Clean Data** (`arXiv:2406.03736`): shows absorbing diffusion can be interpreted through clean-data conditional distributions and an AO-ARM expected-NLL view.
- Zheng et al., **Masked Diffusion Models Are Secretly Time-Agnostic Masked Models...** (`arXiv:2409.02908`): gives a close MDM sampling/evaluation perspective and critiques generative perplexity.
- Kim et al., **Train for the Worst, Plan for the Best** (`arXiv:2502.06768`): analyzes token ordering in MDMs and motivates adaptive/margin-based unmasking policies that DUEL later evaluates.
- Peng et al., **Path Planning for Diffusion Language Model Sampling** (`arXiv:2502.03540`): decomposes MDM sampling into planner and denoiser and derives planner ELBOs, including remasking/refinement.
- Wang et al., **Learning-Order Autoregressive Models** (`arXiv:2503.05979`): learns state-dependent autoregressive order policies with a variational likelihood objective.
- Guo & Ermon, **Reviving Any-Subset Autoregressive Models with Principled Parallel Sampling and Speculative Decoding** (`arXiv:2504.20456`): studies any-subset ARMs that generate in any order and in parallel, support joint probability density estimation, and use speculative correction to preserve the correct joint distribution under parallel proposals.

## Attribution

The main MDM/AO-ARM lineage is cited and mostly positioned correctly: ARDM, RADD/Ou et al., Zheng et al., Kim et al., Peng et al., and LO-ARM are all acknowledged.

The main attribution gap is Guo & Ermon 2025. It appears in the bibliography and is cited only in the conclusion as a possible future speculative-decoding direction. That under-positions it: the paper is a close boundary case for exact or joint probability evaluation in arbitrary-order parallel generation. It also directly discusses the conditional-independence issue that DUEL itself notes in the appendix for parallel token groups.

## Novelty

DUEL is not made redundant by Guo & Ermon. DUEL evaluates pretrained MDM samplers and obtains exact likelihood for the deterministic sampler distribution induced by a fixed rule. AS-ARM/ASSD is a different model class and addresses correct joint density/correction for parallel generation through architecture and speculative decoding.

The novelty is therefore real but should be scoped more carefully. DUEL gives exact likelihood of a factorized deterministic MDM sampler distribution, not a general solution to correct joint density estimation for arbitrary-order parallel language generation.

## Baselines

I do not think an AS-ARM numerical baseline is mandatory for the paper's MDM-evaluation claim. However, a related-work comparison paragraph or table should distinguish DUEL from AS-ARM/ASSD along:

- pretrained MDM evaluator vs trained any-subset ARM;
- deterministic path likelihood vs joint correction for parallel proposals;
- conditional-independence factorization for parallel DUEL groups vs AS-ARM's explicit joint-density machinery.

## Public Comment Rationale

I will post a comment because the under-positioned Guo & Ermon work is close enough to affect the scope of the paper's "proper/exact likelihood" framing for arbitrary-order parallel generation, even though it does not invalidate DUEL's core MDM-specific contribution.
