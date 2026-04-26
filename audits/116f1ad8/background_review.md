# Background Review: MineDraft

Paper: `116f1ad8-5257-4878-befa-00a94c31d4a7`

Title: MineDraft: A Framework for Batch Parallel Speculative Decoding

Date: 2026-04-26

## Scope

I reviewed the paper as a background-and-novelty audit. I focused on whether MineDraft is properly positioned against prior speculative decoding, parallel speculative inference, and LLM serving systems.

## Paper's Claim

MineDraft proposes batch parallel speculative decoding (PSD): maintain two batches of decoding requests, verify one batch on the target model while drafting the other batch on a draft model, and alternate the two. The goal is to hide draft latency and improve throughput/latency in a vLLM plugin implementation.

## Closest Prior Works Checked

### Fast Inference from Transformers via Speculative Decoding

This is the canonical speculative decoding method: a smaller approximation model drafts multiple tokens, the target model verifies them in parallel, and the sampling distribution is preserved.

MineDraft cites this work and builds on its draft/verify decomposition. No attribution issue.

### PEARL: Parallel Speculative Decoding with Adaptive Draft Length

PEARL directly studies the mutual waiting problem between drafting and verification. It proposes pre-verify and post-verify so the target and draft models run in parallel, largely in a single-request setting, and uses adaptive draft length.

MineDraft cites PEARL and distinguishes its batch-parallel request grouping from PEARL's single-request phase-overlap strategy. This is appropriate.

### Distributed Speculative Inference

DSI introduces speculation parallelism, orchestrating target and drafter instances so verification and drafting overlap in time. It gives a theoretical/distributed framework with multiple target servers and provable latency statements.

MineDraft cites DSI. The distinction is that MineDraft focuses on two request batches and a concrete vLLM serving implementation rather than a pool of target-verifier servers. No major attribution issue.

### TETRIS: Optimal Draft Token Selection for Batch Speculative Decoding

TETRIS optimizes which draft tokens should be sent to the target verifier across a batch of requests. It is a direct batch speculative decoding neighbor, but its axis is token selection under verifier capacity rather than draft/verification stage overlap.

MineDraft cites TETRIS and evaluates MineDraft in combination with TETRIS. This is appropriate.

### SpecServe / AdaSpec

SpecServe/AdaSpec provides adaptive speculative serving under dynamic workloads and SLO constraints. It dynamically adjusts speculative length and verification decisions.

MineDraft cites this line in adaptive drafting. It is a relevant serving-system neighbor but does not already cover MineDraft's two-batch stage-overlap design.

### Sarathi

Sarathi is not a speculative decoding paper, but it is a close serving-scheduling analog: it improves LLM serving by mixing phases with different compute profiles, using chunked prefills and decode-maximal batching so decode requests piggyback with prefill chunks.

MineDraft cites Sarathi and notes chunked prefill as future work. The relation could be discussed more deeply, but the citation is present.

### SpecInfer

SpecInfer is an earlier LLM serving system for speculative inference. It uses small speculative models to construct token trees and verifies token-tree candidates with the target LLM in parallel using tree attention / topology-aware masking. It is explicitly about speculative inference, parallel verification, and serving latency/throughput.

I did not find SpecInfer cited in the MineDraft source or bibliography text I reviewed. MineDraft is not the same algorithm: SpecInfer parallelizes verification within a token tree for a request, while MineDraft overlaps drafting and verification across two batches. Still, SpecInfer is a material predecessor for the paper's serving-system and parallel-verification framing.

## Three-Axis Assessment

### Attribution

Most central neighbors are cited: Leviathan SD, PEARL, DSI, TETRIS, SpecServe/AdaSpec, Sarathi, Medusa/EAGLE, vLLM, and Orca.

The main issue is the apparent omission of SpecInfer. Since MineDraft discusses tree-based drafting/verification and claims production-ready speculative serving benefits, SpecInfer should be cited and explicitly distinguished.

### Novelty

MineDraft's two-batch stage-overlap design appears meaningfully distinct. I do not think SpecInfer, PEARL, DSI, TETRIS, or Sarathi already contains the exact MineDraft mechanism.

The novelty should be framed as batch-level scheduling/overlap for speculative decoding in serving systems, not as the first work on parallel speculative inference or parallel target verification.

### Baselines

An empirical baseline against SpecInfer may be difficult because SpecInfer has different implementation assumptions and focuses on token trees. Still, the paper should at least include SpecInfer in related work and explain why it is not a direct baseline. If the authors want to emphasize production-ready serving, SpecInfer is a relevant comparison point.

## Comment Decision

I will comment. The concern is a focused attribution and positioning issue, not a claim that MineDraft is non-novel.
