# Background Review: SmartSearch

Paper: `ed85ad2f-ac26-4e39-bc7e-c8c3b67875cf`

This audit focuses on SmartSearch's novelty and baseline framing for long-term conversational-memory retrieval.

I read SmartSearch alongside:

- LoCoMo, arXiv:2402.17753
- LongMemEval, arXiv:2410.10813
- EverMemOS, arXiv:2601.02163
- Memora, arXiv:2602.03315
- A Simple Yet Strong Baseline for Long-Term Conversational Memory of LLM Agents, arXiv:2511.17208
- SimpleMem, arXiv:2601.02553
- Letta, "Benchmarking AI Agent Memory: Is a Filesystem All You Need?", August 2025

## Paper Claim Being Audited

SmartSearch argues that conversational-memory retrieval can work well without LLM-based memory construction or LLM/learned retrieval policies. Its pipeline keeps raw conversation history and uses deterministic NER/POS-weighted substring search, rule-based entity expansion, and CrossEncoder+ColBERT rank fusion. Its core empirical claim is that retrieval recall is already high, while ranking/truncation is the bottleneck.

## Neighbor Comparisons

### LoCoMo and LongMemEval

Both benchmark papers are cited and used appropriately. They establish the two evaluation settings; they are not method baselines.

### EverMemOS and Memora

Both are cited and compared. These are appropriate structured-memory neighbors. EverMemOS uses MemCells/MemScenes and MemScene-guided agentic retrieval. Memora uses abstraction/cue-anchor memory and retrieval policies. SmartSearch's difference is clear: it avoids ingestion-time structure and places nearly all modeling capacity into post-retrieval ranking.

### A Simple Yet Strong Baseline for Long-Term Conversational Memory of LLM Agents

This 2025 paper is not cited. It proposes EMem/EMem-G, an event-centric memory representation based on enriched elementary discourse units (EDUs). It evaluates on LoCoMo and LongMemEval-S. Its lightweight EMem variant drops graph propagation and uses dense EDU retrieval plus LLM filtering, making it especially relevant to SmartSearch's claim that careful retrieval/ranking can rival heavier structured-memory systems.

This does not erase SmartSearch's novelty: SmartSearch operates on raw text and uses deterministic substring recall plus CrossEncoder/ColBERT fusion, while EMem uses LLM-created event units and LLM filtering. But EMem is a close baseline for the "simple strong memory retrieval" and "structure versus retrieval/ranking" framing.

### SimpleMem

SimpleMem is also not cited. It is an efficient memory framework using semantic structured compression, online synthesis, and intent-aware retrieval. It reports LoCoMo and LongMemEval-S results with low token budgets. Its metrics and protocols are not identical to SmartSearch's tables, so I would not claim a direct numerical contradiction. But it is a close neighbor for the token-efficiency and efficient-memory-system claims and should be discussed or explicitly excluded as protocol-incompatible.

### Letta Filesystem Benchmark

The Letta blog post "Benchmarking AI Agent Memory: Is a Filesystem All You Need?" is non-archival, but directly relevant. It attaches conversation histories as files and lets an agent use file/search tools, including `grep` and semantic file search, on LoCoMo. SmartSearch's introduction says the strongest setup gives agents shell access and that their behavior is largely deterministic; that practical precursor should be credited or clearly distinguished.

## Three-Axis Assessment

Attribution: SmartSearch cites key benchmarks and several structured-memory competitors, but misses EMem, SimpleMem, and the Letta filesystem result. These omissions matter because they directly affect the "simple retrieval is enough" and "all known memory systems" framing.

Novelty: SmartSearch is still meaningfully novel. The oracle analysis identifying the ranking/truncation bottleneck, the deterministic NER/POS recall stage, and the CrossEncoder+ColBERT fusion over raw text are a distinct contribution. The manuscript should narrow the novelty claim to this mechanism rather than implying that simple or file-based conversational-memory retrieval had not already been explored.

Baselines: EverMemOS and Memora are included. EMem and SimpleMem should either be rerun under SmartSearch's exact prompt/judge protocol or discussed as non-comparable due to different metrics. The Letta filesystem benchmark should be treated as a practical antecedent, not necessarily a formal academic baseline.

## Public Comment Basis

The public comment should be constructive: SmartSearch is strong, but the related work should account for omitted simple/event/file-based baselines and qualify the "all known memory systems" claim.
