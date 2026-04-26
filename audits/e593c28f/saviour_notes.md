# Saviour notes for e593c28f

CLAA proposes cross-layer attention-score aggregation to stabilize token selection for long-context LLM prefill pruning.

Observation 1: The long-context evidence is not only LongBench averages: the paper also evaluates Needle-in-a-Haystack and RULER at 64K context, where CLAA improves the RULER average over FastKV at 40% keep rate (82.01 vs. 81.28) while still trailing FullKV (83.78).

Observation 2: The gain over FastKV is not uniform across model sizes and budgets. In Table 2, FastKV slightly beats CLAA on Mistral-Nemo-12B at 20% and 40% keep rates, and the Llama-3.2-3B 40% setting is effectively tied (44.17 FastKV vs. 44.15 CLAA).

Observation 3: The headline TTFT result is scoped to a specific systems setting: Llama-3.1-8B on one A100 80GB, 10k prompt tokens, 32 generated tokens, HuggingFace Transformers, and FlashAttention-2. The reported 39% TTFT reduction is useful, but it is not yet a deployment-wide latency claim.
