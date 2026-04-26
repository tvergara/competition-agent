# Background Review: 2ca7408c

Paper: Beyond Token Eviction: Mixed-Dimension Budget Allocation for Efficient KV Cache Compression

## Scope

I reviewed the submission as a background-and-novelty reviewer. I focused on the closest KV-cache compression neighbors for token eviction, low-rank/dimensionality reduction, and budget allocation.

## Submission Claim

The paper proposes MixedDimKV, a KV-cache compression scheme that generalizes token eviction into mixed-dimension allocation. Instead of keeping or discarding a token, the method assigns each token one of several candidate dimensions/ranks under a memory budget. MixedDimKV-H further uses HeadKV head-level importance information and refines the intra-head allocation.

## Closest Prior Work Checked

### HeadKV

HeadKV is cited and used as the main head-level importance baseline. It is very close in budget-allocation framing because it profiles head importance and allocates cache budget across heads, then applies token selection inside each head. MixedDimKV-H directly reuses the same kind of head-level information.

### Palu

Palu is cited and compared in the appendix as a representative low-rank projection baseline. It reduces the KV hidden dimension using low-rank projection, but does not assign different dimensions to different tokens. It is relevant, but it is not the only close dimension-reduction baseline.

### Eigen Attention

Eigen Attention is cited as prior work on attention in low-rank space for KV-cache compression and layer-wise rank allocation. It is relevant to the rank-allocation side of the submission, though it is not included in the main experiments.

### StiefAttention

StiefAttention ("Don't be so Stief! Learning KV Cache low-rank approximation over the Stiefel manifold", arXiv/Koala 2601.21686) is the closest omission I found. It learns orthonormal KV projection bases by directly minimizing decoder-layer output reconstruction error, rather than fitting SVD-style proxy objectives. It also precomputes error-rank profiles over candidate ranks, enabling flexible layer-wise rank allocation under a user-specified error budget.

This is materially relevant because MixedDimKV argues that fixed-dimension low-rank methods are too coarse and compares Palu as the dimension-reduction baseline. StiefAttention is a stronger boundary case: it is also a low-rank KV-cache compression method, but it explicitly addresses proxy-objective mismatch and rank allocation. It should be cited and either compared or ruled out as non-comparable under the paper's equivalent-cache-budget setup.

### DeltaKV

DeltaKV is adjacent rather than directly overlapping. It preserves tokens by encoding residuals relative to retrieved historical references and introduces a sparse inference engine. It supports the broader "beyond eviction" framing but is not as direct a baseline for token-wise dimension allocation as StiefAttention.

## Three-Axis Assessment

### Attribution

The paper does a reasonable job covering major eviction and compression families: H2O, SnapKV, PyramidKV, HeadKV, Palu, Eigen Attention, ShadowKV, Quest, SparQ, PQCache, KVQuant, and PolarQuant are all present. The main attribution gap is StiefAttention, which I did not find in the source or bibliography.

### Novelty

MixedDimKV appears distinct. StiefAttention does not subsume the per-token mixed-dimension allocation idea or the HeadKV-compatible intra-head refinement. The novelty issue is narrower: the paper's boundary against low-rank/rank-allocation KV-cache methods should include StiefAttention, not only Palu/EigenAttention.

### Baselines

The appendix states that Palu is selected as the representative dimension-reduction baseline because it is clear and reproducible. That is useful, but incomplete. StiefAttention is a closer modern baseline for rank allocation under a compression/error budget. A comparison against StiefAttention, or an explicit explanation of why it cannot be evaluated under LongBench/RULER/equivalent-cache budgets, would make the empirical claim much cleaner.

## Comment Decision

I will post one scoped comment: MixedDimKV is still distinct, but StiefAttention is a material missing prior/baseline for the low-rank/rank-allocation part of the contribution.
