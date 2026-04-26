# Saviour Notes: 116f1ad8

This paper proposes MineDraft, a batch-parallel speculative decoding system that overlaps drafting for one request batch with verification for another.

Observation 1: The default experimental setup is specific: PyTorch 2.7.0, Transformers 4.53.3, vLLM 0.9.2, temperature 1.0, one sequence per request, 256 generated tokens while ignoring EOS, target tensor parallelism 4, draft tensor parallelism 1, and one extra GPU relative to standard SD.

Observation 2: The vLLM integration depends on a scheduler/KV-memory patch, not only an outer scheduling policy: during batch parallelism the default vLLM scheduler would allocate KV blocks for all running requests, so MineDraft tracks deferred request IDs and skips allocations for draft-batch decoding requests.

Observation 3: The appendix reports a concrete draft-size failure mode: with Qwen3-8B as the draft model, latency is best at only 1-2 draft tokens per step, more than two draft tokens degrades performance, TETRIS gives no additional latency reduction, and standard SD does not run due to VRAM constraints.
