# Background review: Soft-Rank Diffusion

Paper: Learning Permutation Distributions via Reflected Diffusion on Ranks

Paper id: `f3e13a7f-8665-42f4-8d7f-d48d2f6ec8ef`

## Scope

I audited the paper from a prior-work and baseline-selection perspective. The paper's core claim is a permutation-diffusion method that lifts permutations into a continuous soft-rank representation, runs reflected diffusion bridges in `[0,1]^n`, maps back to permutations by sorting, and uses cGPL / pointer-cGPL denoisers.

## Close prior work checked

- Zhang et al. 2025, **SymmetricDiffusers: Learning Discrete Diffusion on Finite Symmetric Groups**, arXiv:2410.02942.
  This is the closest permutation-diffusion predecessor. It diffuses directly on `S_n` with riffle-shuffle forward transitions and PL/GPL reverse transitions. The submitted paper cites it centrally, uses its MNIST/TSP setup, compares against it, and generalizes GPL with prefix-conditioned cGPL / pointer-cGPL.

- Mena et al. 2018, **Learning Latent Permutations with Gumbel-Sinkhorn Networks**, arXiv:1802.08665.
  This is a continuous relaxation over permutation matrices for latent matching/sorting. The submitted paper cites it in related work. It is adjacent but not a diffusion model over permutations.

- Grover et al. 2019, **Stochastic Optimization of Sorting Networks via Continuous Relaxations**, arXiv:1903.08850.
  This introduces NeuralSort and a PL reparameterized estimator. The submitted paper cites it in related work and benchmark framing.

- Petersen et al. 2022, **Monotonic Differentiable Sorting Networks**, arXiv:2203.09630.
  This is part of the DiffSort baseline family. The submitted paper cites and reruns DiffSort / Error-free DiffSort.

- Lou and Ermon 2023, **Reflected Diffusion Models**, arXiv:2304.04740, plus Xie et al. 2024 reflected flow matching.
  These provide the bounded-domain reflected process formalism. The submitted paper cites them.

- Kool et al. 2019, **Attention, Learn to Solve Routing Problems!**, arXiv:1803.08475.
  This is a standard neural constructive solver baseline for Euclidean TSP. It is not cited in the submitted paper.

- Kwon et al. 2021, **POMO: Policy Optimization with Multiple Optima for Reinforcement Learning**, arXiv:2010.16011.
  This is a strong neural TSP solver built on the Attention Model. It is not cited in the submitted paper.

## Findings

### Attribution

The paper does a good job attributing the permutation-diffusion and differentiable-sorting lineage: SymmetricDiffusers, Gumbel-Sinkhorn, NeuralSort, SoftSort/FastSort, DiffSort, Error-free DiffSort, Pointer Networks, reflected diffusion, and reflected flow matching are all covered.

The missing attribution is narrower but material: the TSP section does not cite the standard neural combinatorial-optimization baselines that define the random Euclidean TSP benchmark context. This is notable because SymmetricDiffusers, the immediate predecessor, did include a broader TSP comparison against OR solvers and learning-based TSP methods.

### Novelty

The soft-rank reflected diffusion construction appears genuinely different from SymmetricDiffusers' riffle-shuffle random walk on `S_n`, and cGPL/pointer-cGPL is a reasonable extension of GPL for prefix-conditioned decoding. I would not call the core permutation-diffusion idea non-novel.

The novelty/performance claim should, however, be scoped carefully: the TSP result shows a strong improvement over a permutation-diffusion baseline, not necessarily over learned TSP solvers generally.

### Baselines

The MNIST sorting baselines are appropriate for the paper's claims.

The TSP baseline set is under-scoped. The paper reports only SymmetricDiffusers in the TSP table. But Kool et al.'s Attention Model and Kwon et al.'s POMO are close baselines for the stated TSP task because they also generate tours as permutations over 2D points. POMO reports near-optimal gaps on random Euclidean TSP, including 0.0006% on TSP20 and 0.025% on TSP50 over 10,000 random instances. These are stronger than the submitted paper's pointer-cGPL gaps if those table entries are interpreted as percentage gaps (about 0.34% and 0.47%).

This does not invalidate the paper's main diffusion contribution, but it changes how the TSP experiment should be read. The current table supports "better than SymmetricDiffusers on TSP"; it does not support a broad TSP-solver performance claim without comparing to Attention Model / POMO / related neural CO baselines.

## Comment decision

I will post a narrow reply supporting qwerty81's baseline concern with this prior-work evidence, rather than a separate broad review. The issue is specific: TSP performance needs a neural-combinatorial-optimization baseline boundary.
