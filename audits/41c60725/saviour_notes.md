# Saviour notes for 41c60725

The paper proposes HeiSD, a hybrid speculative-decoding system for autoregressive VLA robot policies that switches between retrieval-based and drafter-based drafts using kinematic signals.

**Observation 1:** The retrieval component is unusually concrete: Appendix database details report 273,465 timestep vectors across 40 task-specific Qdrant collections, a 6.5 GB total footprint, and 5.13 ms average query latency, which supports the practical feasibility of the retrieval side of the system.

**Observation 2:** That same design is partly task-routed: the appendix says retrieval uses task-level sharding and searches within a pre-specified task collection, so the reported retrieval quality assumes that the correct task collection is known at inference time.

**Observation 3:** The speedup tables focus on online inference, but the setup cost is nontrivial: Section 7 says the single-LLaMA-block drafter is trained for 8 hours on 2 NVIDIA A100 GPUs, and the real-world appendix says about 300 episodes per task type are collected for later fine-tuning.
