# Background and Novelty Audit: Tabula RASA (2f23edaf)

**Claimed Contribution:**
The paper proposes RASA (Relation-Aware Sparse Attention), a Transformer modification featuring sparse adjacency masking and learnable edge-type biases to improve multi-hop relational reasoning. It motivates this using circuit complexity ($\TC^0$) results showing Transformers need $\Omega(k)$ layers for $k$-hop reasoning.

**Prior Work Comparison:**
1. **A Generalization of Transformer Networks to Graphs** (Dwivedi & Bresson, 2020): Introduced Sparse Graph Transformers using adjacency matrix masking to restrict attention to local neighborhoods. RASA's sparse masking is essentially a re-implementation of this.
2. **Do Transformers Really Perform Bad for Graph Representation?** (Graphormer, Ying et al., 2021): Introduced edge encodings/biases to attention. RASA's edge-type bias is a simplified version of this (1-hop vs multi-hop encodings).
3. **The Parallelism Tradeoff: Limitations of Log-Precision Transformers** (Merrill & Sabharwal, 2023): Established the $\TC^0$ completeness of Transformers.
4. **Representational Strengths and Limitations of Transformers** (Sanford et al., 2023): Proved that constant-depth Transformers cannot solve graph connectivity, establishing the $\Omega(k)$ depth requirement for $k$-hop reasoning.
5. **Neural State Machine for Reasoning** (NSM, Zhang et al., 2021): A strong baseline for MetaQA. The RASA paper includes NSM in its results table (98.9% on 3-hop) but ignores it in the abstract and conclusion to claim "outperforming EmbedKGQA (94.8%)" as a significant result.
6. **TransferNet** (Shi et al., 2021): Achieved 100% accuracy on MetaQA 3-hop (Vanilla). RASA (97.7%) fails to reach this SOTA established five years prior.

**Three-Axis Assessment:**
- **Attribution:** While the paper cites the complexity-theoretic works (Sanford/Merrill), it presents the analysis in Section 3 as its own core contribution ("We analyze this limitation through circuit complexity..."). More importantly, it fails to acknowledge that "Sparse Graph Transformer" (Dwivedi, 2020) already pioneered adjacency masking for sparsity.
- **Novelty:** Low. RASA is a combination of known graph transformer techniques (adjacency masking, edge bias). The theoretical motivation identifies a bottleneck that RASA itself admits it does not solve (it still requires $\Omega(k)$ layers). The "reduction in search space" argument is a standard justification for sparse attention.
- **Baselines:** Major concerns. The paper selectively highlights EmbedKGQA (a 2020 model) as the baseline to outperform in the abstract, while its own table shows it is inferior to NSM (2021). It completely omits TransferNet (2021), which solved the 3-hop task with 100% accuracy. Furthermore, RASA's 1-hop results (85.6%) are 12 points lower than the 2020 baseline, suggesting the architectural "fix" significantly degrades basic entity representation.

**Conclusion:**
RASA appears to be an incremental application of established graph transformer techniques to an old benchmark (MetaQA) where it fails to reach state-of-the-art performance. The theoretical analysis is derivative of recent complexity-theoretic work and does not lead to a circumvention of the identified depth limits.

**Final Verdict:** Not Novel / Incremental.
