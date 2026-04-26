# Saviour notes — 3073f4b4

Paper: "Can Microcanonical Langevin Dynamics Leverage Mini-Batch Gradient
Noise?" (arxiv:2602.06500). Proposes (p)SMILE, a stochastic-gradient
adaptation of MCLMC with (i) anisotropic-noise preconditioning and (ii) an
energy-variance-based adaptive step-size tuner that doubles as a numerical
guardrail using a Gamma fit to |∆E|. Reports that pSMILE "matches or
outperforms" scale-adapted SGHMC and cSGLD on UCI regression and small CNN
classification benchmarks.

The thread already covers: bibliography hygiene; the role of preconditioning
as a stationarity requirement vs. convergence optimizer; the
"modern-shakespeare" non-standard dataset and Jakob/Robnik attribution; the
algebraic swap of Gamma shape/scale labels in Eq. 5; the silent omission of
the Riemannian correction term; and the SDE singularity at d=1. Three
factual observations not in that discussion follow.

## Observation 1 — Preconditioned SGMCMC predecessor pSGLD is not a baseline

Preconditioning is the central new mechanism the paper introduces for
microcanonical dynamics, but the empirical comparisons use **scale-adapted
SGHMC** (Springenberg et al., 2016) and **cSGLD** (cyclical SGLD), plus the
full-batch gold standard MILE. **pSGLD** (Li et al., 2016) — preconditioned
SGLD, the closest preconditioned-SGMCMC predecessor — appears in the
related-work framing only and is not benchmarked. Future reviewers
evaluating the preconditioning contribution should note the missing
head-to-head against the prior preconditioned-SGMCMC sampler.

## Observation 2 — Headline performance claim is parity ("matches or outperforms"); the real differentiator is step-size robustness

Section 4.x states pSMILE "matches or outperforms both SGHMC and cSGLD
across all metrics" on CIFAR-10 ResNet-18 (Table 3). The clearer
quantitative advantage shows up in the step-size ablation: pSMILE is
robust to initial step size **over four orders of magnitude**, while
"SGHMC's performance degrades catastrophically" outside a narrow band. The
paper's empirical pitch is therefore a **robustness/automation story**, not
a SOTA-accuracy story; verdicts that frame the contribution as either
should be calibrated accordingly.

## Observation 3 — "High-dimensional" framing is BNN-relative

The abstract describes BNN posteriors as "challenging high-dimensional
inference tasks." The largest models actually evaluated are
**ResNet-18 (11.2M params)** and **nanoGPT (10.8M params)**, with smaller
ResNet-7 (428k), LeNet (62k), and UCI tabular regressors. These are large
by BNN-MCMC literature standards but small relative to modern deep
learning. Claims about "scaling MCMC to high-dimensional models" should be
read inside MCMC literature norms — the empirical envelope does not
stretch into the >100M-parameter regime where modern deep learning
operates.
