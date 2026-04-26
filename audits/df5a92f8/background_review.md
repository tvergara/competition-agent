# Background Review: DeltaKV

Paper: "DeltaKV: Residual-Based KV Cache Compression via Long-Range Similarity"

Koala paper ID: `df5a92f8-3301-4ffe-966e-984eb26589ba`

Audited at: 2026-04-26T02:46:49-04:00

## Summary

I read DeltaKV against five close KV-cache compression / selection neighbors:

- R-KV: Redundancy-aware KV Cache Compression for Reasoning Models (`arxiv:2505.24133`)
- ClusterKV: Manipulating LLM KV Cache in Semantic Space for Recallable Compression (`arxiv:2412.03213`)
- Chelsea: Efficient Long-Context LLM Inference via KV Cache Clustering (`arxiv:2506.11418`)
- Palu: KV-Cache Compression with Low-Rank Projection (`arxiv:2407.21118`)
- MiniCache: KV Cache Compression in Depth Dimension for Large Language Models (`arxiv:2405.14366`)

My conclusion is narrow: DeltaKV looks technically distinct from these neighbors, but its reasoning/AIME claim has a material missing prior/baseline. R-KV directly studies redundancy-aware KV-cache compression for reasoning-model decoding and evaluates on AIME 2024, yet DeltaKV does not cite or discuss it in the compiled text and does not include it in the AIME comparison.

## Attribution

The clearest issue is R-KV. The DeltaKV source contains a `cai2025rkv` bibliography entry for "R-KV: Redundancy-aware KV Cache Compression for Training-Free Reasoning Models Acceleration," but I could not find a corresponding citation in the paper text or compiled bibliography. DeltaKV's AIME table compares Full, SnapKV, OmniKV, and DeltaKV, while the surrounding text uses AIME to support applicability to reasoning-oriented models.

R-KV is materially relevant to that claim. It focuses on long reasoning-model generations, argues that chain-of-thought outputs create redundant KV entries, combines attention importance with semantic redundancy estimated from key-vector similarity, and reports AIME 2024 results for DeepSeek-R1 distilled models. This does not subsume DeltaKV's residual-compression mechanism, but it is the most direct prior I found for "reasoning-model KV redundancy" and should be cited and positioned.

For the other neighbors, DeltaKV's attribution is mostly reasonable:

- ClusterKV is cited and discussed as semantic-cluster recall with CPU/offload-oriented structures.
- Chelsea is cited and used as the local-similarity clustering contrast.
- Palu is cited and compared as the closest hidden-dimension compression baseline.
- MiniCache is relevant as similarity-based KV compression across depth, but less directly tied to DeltaKV's token-history residualization; I would not treat its absence as a major attribution problem.

## Novelty

DeltaKV appears novel relative to the five neighbors I checked. Palu compresses hidden dimensions via low-rank projection; Chelsea and ClusterKV merge or recall semantically similar token groups; MiniCache exploits adjacent-layer similarity; R-KV selects important and non-redundant generated tokens for reasoning models. DeltaKV's contribution is different: keep strided reference tokens, retrieve globally similar references, encode per-token residuals in a compressed latent space, then reconstruct only selected tokens inside a sparse-attention serving path.

I would therefore not characterize the whole paper as a restatement of prior work.

## Baselines

The general long-context baseline set is reasonable: static eviction, dynamic sparsity, and Palu cover much of the expected comparison space.

The AIME/reasoning baseline set is incomplete. Since R-KV was designed for redundant reasoning traces and reports AIME 2024 behavior under KV-cache budgets, DeltaKV should either compare against it in the AIME setting or explain why its problem setting is out of scope. Without that, the AIME evidence risks overstating the reasoning-specific contribution relative to the closest available baseline.

## Public Comment Basis

The public comment should be framed as a targeted baseline/attribution concern, not as a broad novelty rejection. The strongest defensible statement is:

DeltaKV's residual reference mechanism appears distinct, but the AIME/reasoning evaluation should cite and discuss R-KV and should ideally compare against it or justify why it is not comparable.
