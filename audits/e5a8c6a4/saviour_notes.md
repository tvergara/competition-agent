# Saviour notes for e5a8c6a4

This paper introduces ATM-Bench, a multimodal, multi-source personal memory QA benchmark with schema-guided memory representations and evaluations of memory-agent and RAG systems.

Observation 1: The headline ATM-Bench-Hard result should be read with its split size in mind: the appendix reports only 25 hard questions, with 6 number, 12 list-recall, and 7 open-ended items, though those hard questions average 6.3 evidence items.

Observation 2: Oracle retrieval still leaves a substantial answer-generation bottleneck. With gold evidence, GPT-5 reaches 74.7 QS on ATM-Bench-Hard, while Qwen3-VL-8B reaches 47.3, showing that hard cases are not only retrieval failures.

Observation 3: The retrieval ablation is notable for multimodal memory: Qwen3-VL-Embedding-2B performs much worse than text-based embedding over SGM memory (31.3 QS and 40.1 R@10 versus MiniLM's 51.0 QS and 68.7 R@10), which supports the paper's explanation that high-resolution visual tokens can dilute timestamp/location metadata.
