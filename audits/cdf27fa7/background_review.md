# Background Review: StiefAttention

Paper: "Don't be so Stief! Learning KV Cache low-rank approximation over the Stiefel manifold" (`cdf27fa7-5108-4a4d-abfc-46f554fb3f52`)

## Summary

StiefAttention is a distinct contribution within hidden-dimension KV-cache compression: it learns orthonormal key/value projection bases that minimize decoder-layer output reconstruction error, rather than fitting bases to reconstruct K/V, `[K;Q]`, or another intermediate attention quantity. The paper's diagnostic that proxy objectives can preserve the wrong quantity is plausible and useful.

The concern is not missing citation. The paper cites the relevant family. The concern is that the empirical baseline set is too narrow for the main claim: the only quantitative baseline is EigenAttention, while two closer stress tests are cited but not evaluated.

## Closest Prior Work Checked

1. **EigenAttention** (Saxena et al., Findings EMNLP 2024). This is cited and evaluated. It is a reasonable baseline because it compresses KV feature dimension using low-rank bases and a `[K;Q]` SVD objective.

2. **KQ-SVD** (Lesens et al., arXiv:2512.05916). This is cited but not evaluated. It is very close to the paper's motivating argument: it already criticizes K-only and EigenAttention-style objectives as suboptimal proxies and instead optimizes a closed-form low-rank approximation to the attention interaction `KQ^T`, with an analogous value/output treatment. If StiefAttention's advantage is that attention-level proxies still miss full decoder-layer behavior, KQ-SVD is the natural baseline to show that.

3. **MatryoshkaKV** (Lin et al., ICLR 2025). This is cited but not evaluated. It directly trains orthogonal projection matrices for KV feature-dimension compression with a distillation objective so compressed-cache model outputs stay close to full-cache outputs. It also uses adaptive layer/head compression budgets. That makes it a close conceptual predecessor to StiefAttention, even though StiefAttention is distinct in optimizing per-layer decoder-output reconstruction from activation statistics rather than global output distillation.

4. **TALE** (Lee et al., TACL 2025). This is cited but not evaluated. TALE is less central to the novelty claim, but it is a practical low-rank KV-cache compression boundary because it uses token-adaptive ranks, lazy approximation, and reconstruction elimination, reporting high compression and latency gains.

5. **Palu** (Chang et al., ICLR 2025). This is cited as earlier low-rank projection work. It is a foundational hidden-dimension compression baseline and relevant to practical speed/memory claims, although less directly tied to StiefAttention's decoder-output objective.

## Three-Axis Assessment

**Attribution.** The paper cites the close neighbors I would expect: EigenAttention, Palu, KQ-SVD, TALE, MatryoshkaKV, and related SVD/low-rank KV-cache methods. I do not see a clean uncited-prior failure.

**Novelty.** StiefAttention is not a restatement of EigenAttention or Palu. It also differs from KQ-SVD and MatryoshkaKV: KQ-SVD targets attention-interaction fidelity, and MatryoshkaKV uses output-preserving distillation of orthogonal projections, while StiefAttention optimizes a per-layer decoder-output criterion and builds bases from lightweight activation statistics. The novelty is real, but its boundary is narrower than a comparison to EigenAttention alone establishes.

**Baselines.** KQ-SVD and MatryoshkaKV are the key missing head-to-heads or explicit non-comparability cases. TALE and Palu are also useful practical boundaries for compression ratio and latency. The paper's current EigenAttention-only evaluation supports "better than this SVD-style baseline," but not the stronger implication that decoder-layer-output optimization is superior to the best nearby proxy/objective alternatives.

## Comment Decision

I recommend posting a public comment because the issue is specific and material: StiefAttention may be a valid contribution, but reviewers need the KQ-SVD and MatryoshkaKV boundary to interpret the claimed novelty and empirical strength.
