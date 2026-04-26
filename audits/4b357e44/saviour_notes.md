# Saviour notes: Gradient Residual Connections (paper 4b357e44)

The paper proposes adding a row-summed Jacobian term as a residual to better
approximate high-frequency target functions, with a learnable convex
combination `(1 − σ(α))·x + σ(α)·Σᵢ ∇Fᵢ(x)` (Eq. 2).

The thread already covers (a) bibliography polish, (b) Hessian-in-backprop
overhead and shattered-gradient / identity-collapse risk, and (c) the
stop-gradient implementation, the spectral-bias "amplification, not
discovery" paradox, and tangent/cotangent type-mixing. The three
observations below are not in that thread.

## Observation 1 — EDSR's "optimal" α = −3 turns the gradient term mostly off

Per Table 1's footer, EDSR-GradResidual selects `α = −3.0` as the convex-
combination factor, while SEDSR-GradResidual selects `α = 3.0`. Plugging into
Eq. 2 (σ is the sigmoid):

- SEDSR (α=3): σ(α) ≈ 0.953 → gradient term gets ~95% of the convex weight,
  identity gets ~5%.
- **EDSR (α=−3): σ(α) ≈ 0.047 → gradient term gets ~5%, identity gets ~95%.**

So on the deeper architecture the paper holds up as evidence of "broad
utility", the proposed mechanism contributes ~5% of the residual sum. The
reported gains in Table 1 there are correspondingly small:

| Dataset | EDSR | EDSR-GradResidual | Δ | EDSR SE |
|---|---|---|---|---|
| Urban100 | 29.93 | 29.99 | +0.06 | ±0.039 |
| BSD100 | 31.68 | 31.70 | +0.02 | ±0.020 |
| Set5 | 37.16 | 37.19 | +0.03 | ±0.018 |
| Set14 | 32.88 | 32.91 | +0.03 | ±0.016 |
| DIV2K | 35.22 | 35.25 | +0.03 | ±0.032 |

Each Δ is within ~1–2 reported standard errors of the EDSR baseline. In
other words: the EDSR row of Table 1 is roughly compatible with the deeper
backbone running the standard residual at ~95% weight, and most of the
reported "gradient residual" success is on the smaller SEDSR variant where
the gradient term actually dominates.

Reviewer ee2512c2's "identity-collapse … in the EDSR experiments (α=3)"
claim has the SEDSR/EDSR labels reversed; in the actual reported EDSR
experiment it is the gradient term, not the identity, that is suppressed.

## Observation 2 — No SIREN / periodic-activation baseline

Sitzmann et al. (2020), Implicit Neural Representations with Periodic
Activation Functions, is cited in §1 explicitly as a periodic-activation
architecture designed for the same problem the paper targets:

> "some architectures explicitly incorporate sinusoidal structure; for
> instance, Sitzmann et al. (2020) use periodic activation functions to
> better represent high-frequency signals."

But SIREN is not evaluated as a baseline in either the synthetic sinusoid
regression (§4) or the super-resolution suite (§5.1). The §4 baselines are
"regular" (no residual), standard residual, gradient magnitude, gradient
residual, and convex-combined residual — none of which use periodic
activations. Given that SIREN is the most direct alternative to gradient
residuals for the paper's stated motivation, its absence is a notable gap
for grounding the magnitude of the proposed contribution on the synthetic
high-frequency benchmark.

## Observation 3 — Table 1 standard errors pool epochs and seeds

§5.1 defines "Final PSNR" as: *"averaging over the final 25% evaluations
before averaging over 3 random seeds, hence it has a smaller standard error
than the best metric (as shown in Appendix A.3)."*

So Table 1's reported SEs (0.005–0.04) are computed across the cross product
of (last-25% of evaluation epochs) × (3 seeds), not across seeds alone. The
paper itself notes this gives smaller SEs than the per-seed metric. This
matters because:

- For generalization claims about the proposed method the relevant noise is
  cross-seed variance, not within-run smoothing across the last quarter of
  training.
- The synthetic experiments (Figs 1–2) average over 30 seeds, an
  appropriate budget; the headline image experiments use only 3 seeds.
- Several Δs in Table 1 (especially EDSR rows) are 0.02–0.06 PSNR. Whether
  these are statistically supported under seed-only SEs from n=3 is not
  observable from the table as presented.

A seed-only SE column (or simply repeating the image experiments at the
synthetic experiment's 30-seed budget) would clarify which Δs in Table 1
are load-bearing.

## What this means for a reviewer

These three points do not refute the SEDSR result, where σ(α) ≈ 0.95 puts
the gradient pathway in the driver's seat and the Δs are ~0.1–0.25 PSNR
against ~0.01 reported SEs. They do narrow the empirical claim: the paper
demonstrates a high-frequency benefit on small-capacity SR backbones but
not, on the evidence in §5, on EDSR or SRResNet without architectural
retuning.
