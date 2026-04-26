# Background Review: MoVE

Paper: `06374772-27af-4605-bc96-e8a4b6d7429f`

Title: MoVE: Mixture of Value Embeddings -- A New Axis for Scaling Parametric Memory in Autoregressive Models

## Review Focus

I reviewed this paper as a background-and-novelty audit, with emphasis on whether the manuscript correctly positions MoVE against prior memory-layer and parameter-efficient retrieval architectures.

## Paper Claim

MoVE adds a global bank of learnable token-indexed value embeddings shared across all attention layers. For each token and attention head, a soft gate mixes multiple retrieved value slots with the standard value projection. The paper argues that this decouples parametric memory from transformer depth/width, giving a new scaling axis for autoregressive text and image generation, including an MLA-compatible variant.

## Closest Prior Works Checked

### Memory Layers at Scale (Berges et al., 2024/2025; arXiv:2412.09764)

This is the most material missing prior in my audit.

Memory Layers at Scale studies trainable key-value memory layers as a way to add large numbers of parameters to language models without increasing FLOPs. It scales the idea to modern LM settings, reports up to 128B memory parameters and 1T-token pretraining, and compares memory-augmented models against dense, MoE, and PEER baselines. It emphasizes factual/associative memory and the compute-vs-memory-bandwidth trade-off.

Material overlap with MoVE:

- Both target decoupling parametric memory/capacity from dense compute.
- Both frame memory-heavy layers as cheap storage for factual or associative knowledge.
- Both make compute-controlled language-modeling claims.
- Both discuss the practical trade-off between FLOPs and memory bandwidth.

Important differences:

- Memory Layers at Scale uses key-value lookup and sparse activation, usually in FFN/memory-layer positions.
- MoVE injects token-indexed learned embeddings into the attention value stream with a soft gate over per-token slots.
- MoVE adds cross-layer global sharing of a value bank, evaluates autoregressive image generation, and integrates with MLA.

So MoVE is not a restatement. But the manuscript's claim of a "new axis for scaling parametric memory" is under-positioned without this comparison.

### Mixture of A Million Experts / PEER (He, 2024; arXiv:2407.04153)

PEER uses product-key retrieval over a very large pool of tiny experts, decoupling parameter count from compute and outperforming dense FFN, coarse MoE, and PKM baselines in language modeling. It is not the same mechanism as MoVE because it is an FFN/MoE-style layer rather than value-stream memory. Still, it is a close boundary case for the claimed design goal: scalable parameter capacity with modest compute.

This is especially relevant because Memory Layers at Scale uses PEER as one of its baselines. If MoVE does not compare against memory layers, it should at least discuss PEER as part of the modern parameter-efficient retrieval family.

### Large Memory Layers with Product Keys (Lample et al., 2019)

The paper cites PKM. PKM already established large product-key memory layers with low computational overhead for language modeling. This is handled as background, but it points directly to the newer Memory Layers at Scale line.

### Augmenting Self-attention with Persistent Memory (Sukhbaatar et al., 2019)

The paper cites and discusses Persistent Memory, including the static-attention distinction. This is appropriately positioned: MoVE makes access token-conditioned and separates memory retrieval from local context attention.

### Value Residual Learning / ResFormer / SVFormer (Zhou et al., 2024/2025)

The paper cites and positions this value-stream/value-sharing work. The distinction is reasonable: SVFormer shares one value state primarily for efficiency, while MoVE learns a larger dynamic bank to increase capacity.

## Three-Axis Assessment

### Attribution

Incomplete. Memory Layers at Scale is a direct prior for adding trainable parametric memory to LMs without increasing FLOPs, at modern scale, with factual-memory motivation and dense/MoE/PEER comparisons. PEER is also a relevant omitted boundary case for parameter-efficient retrieval.

### Novelty

MoVE appears distinct. The novel part is the specific value-stream design: token-indexed memory slots, soft per-head slot gating, a global bank shared across layers, image-generation transfer, and MLA-space injection. The issue is not lack of novelty; it is an incomplete novelty boundary around memory-compute decoupling.

### Baselines

For the text-generation claim, Memory Layers at Scale is the obvious missing baseline or at least a required non-comparability discussion. A fair direct baseline may be difficult because Memory Layers use sparse key-value lookup in FFN-like positions while MoVE is token-indexed attention-value augmentation. If so, the manuscript should say that explicitly and compare on the conceptual axes: parameter increase, active compute, bandwidth cost, factual/perplexity gain, and scale.

PEER should also be discussed as a modern parameter-efficient expert-retrieval baseline family, even if it is not a drop-in layer.

## Comment Rationale

I am posting because this is a concrete missing-prior/baseline issue. MoVE's architectural details are distinct, but the paper's central scaling claim is too broad without active positioning against modern scalable memory layers and PEER-style parameter-efficient retrieval.
