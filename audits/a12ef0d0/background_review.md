# Background and Novelty Audit: Learning to Share (LTS) for Parallel Agentic Systems

## 1. Attribution and Prior Work
The paper correctly identifies the current state-of-the-art in parallel agentic execution, specifically **M1-Parallel (Zhang et al., 2025)**, as the primary baseline. It also acknowledges the growing body of work on LLM-based memory management, including **Memory-r1 (Yan et al., 2025)** and **G-Memory (Zhang et al., 2025b)**.

However, the distinction between LTS and **Memory-r1** could be sharpened. While LTS focuses on "ephemeral" per-task shared memory for parallel teams, Memory-r1 also employs a reinforcement learning framework to manage and utilize memories. A more explicit comparison of the "usage-aware credit assignment" (LTS) versus the RL objectives used in Memory-r1 would help clarify the methodological novelty.

## 2. Novelty and Technical Contribution
The framing of "ephemeral shared memory for parallel teams" is a distinct and practical contribution to the field of multi-agent coordination. Most existing work on parallel LLM agents focuses on independent exploration followed by final aggregation; LTS correctly identifies the redundancy in this approach and proposes a mechanism for intermediate information reuse.

The **usage-aware credit assignment** ( = A_{base} + \beta \cdot \mathbb{I}(\text{used})$) is a sensible application of hindsight-style reward shaping to the memory admission problem, ensuring that only memories that actually contributed to a successful outcome are reinforced.

## 3. Omitted Baselines (Critical Concern)
The primary weakness in the empirical evaluation is the omission of a **similarity-based deduplication baseline**. 

Given that parallel teams often explore overlapping paths (e.g., executing the same web search or parsing the same snippet), a simple, non-learned heuristic such as **embedding similarity thresholding** (admit step $ only if $\text{sim}(s, M) < \tau$) would likely capture a significant portion of the "redundancy reduction" gains. Without this baseline, it is difficult to determine whether the 0.6B-parameter RL-trained controller is providing value beyond simple deduplication.

Furthermore, the paper provides an ablation on its RL objectives but does not compare against other standard unlearned memory admission heuristics (e.g., admission by recency or importance scores from a frozen model).

## 4. Reporting Gaps
The hyperparameters $\beta$ (usage bonus) and $\lambda_{sparse}$ (sparsity penalty) are introduced in Section 3.3 but their specific values used in the experiments are not reported in the main text or the implementation details section, which hinders reproducibility.

