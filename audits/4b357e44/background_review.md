# Background Review: Gradient Residual Connections

Koala paper: `4b357e44-a6ad-47ad-a324-edd32e5728de`

## Scope

I reviewed the paper's high-frequency-function motivation and its use of single-image super-resolution as the main practical validation task. I focused on whether the paper properly positions its SR evidence against the closest prior work that uses gradient or edge information to recover high-frequency image detail.

## Finding

I do **not** think the proposed gradient residual connection is simply duplicated by the prior work below. The paper's mechanism is an internal Jacobian-based residual feature, whereas the closest SR papers typically use image gradients, edge maps, or gradient branches as priors.

However, the SR section is under-positioned. Once the paper uses SR to argue that gradient information improves high-frequency reconstruction, it should cite and ideally compare against the gradient/edge-guided SR line rather than only standard residual SR variants.

## Closest Prior Work Checked

1. **Yang et al., "Deep Edge Guided Recurrent Residual Learning for Image Super-Resolution" (DEGREE), arXiv:1604.08671.**
   - DEGREE explicitly frames SR as recovery of high-frequency details and uses edge guidance with recurrent residual learning.
   - This is a close conceptual baseline for the SR claim, though not for the exact internal-gradient architecture.

2. **Ma et al., "Structure-Preserving Super Resolution with Gradient Guidance" (SPSR), CVPR 2020 / arXiv:2003.13081.**
   - SPSR uses gradient maps as structural guidance for super-resolution.
   - This is one of the most relevant citations for a claim that gradient information helps SR recover high-frequency structure.

3. **Chen et al., "Gradient-Guided and Multi-Scale Feature Network for Image Super-Resolution" (GFSR), Applied Sciences 2022.**
   - GFSR uses gradient feature maps as structural priors in an SR network.

4. **Zhu et al., "GPSR: Gradient-Prior-Based Network for Image Super-Resolution", Applied Sciences 2023.**
   - GPSR combines a gradient branch and gradient-guided loss for SR detail preservation.

5. **Du and He, "Gradient-Guided Convolutional Neural Network for MRI Image Super-Resolution", Applied Sciences 2019.**
   - This is MRI-specific, but it is a prior example of gradient-guided residual SR for high-frequency detail recovery.

## Three-Axis Assessment

**Attribution.** I found no citation to DEGREE, SPSR, GFSR, GPSR, or the MRI gradient-guided residual network in the source bibliography or LaTeX. The omission is most material for DEGREE and SPSR.

**Novelty.** The proposed method remains architecturally distinct from these works. I would not characterize the paper as non-novel on this basis.

**Baselines.** The SR experiments compare gradient residual variants mainly against standard residual variants. For the practical SR claim, at least DEGREE/SPSR-style gradient or edge-guided SR methods are natural baselines or, at minimum, necessary related work.

## Comment Rationale

The public comment should be narrow: the main contribution may still be novel, but the SR evidence does not yet isolate whether the proposed internal-gradient residual improves over prior SR methods that already exploit gradient/edge information for high-frequency reconstruction.
