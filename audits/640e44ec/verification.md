# Verification Report: Tool-Genesis: A Task-Driven Tool Creation Benchmark for Self-Evolving Language Agent

I have verified several key claims regarding this paper's methodology, metrics, and benchmarks:

1. **Utility Metric Formula (Eq. 15):** ✓ **Confirmed**. Equation 15 (Line 1018 in the LaTeX) defines the Oracle-Normalized Success Rate as  = \frac{1 - s^{gt}_j}{1 - s^{gen}_j + \epsilon}$. This formula is mathematically problematic: if the ground-truth oracle is perfect (^{gt}_j = 1.0$), the score for any generated tool becomes 0, regardless of its performance.
2. **Fixed Proxy Agent:** ✓ **Confirmed**. Appendix A.4 (Line 1007) states that Level 4 downstream utility is evaluated using a fixed proxy agent based on **Qwen3-14B-instruct**.
3. **Metric Composition (Layer 3 FC):** ✓ **Confirmed**. Equation 12 (Line 991) defines the Level 3 Functional Correctness (UT) score as an equal-weight combination (1/2 each) of structured JSON key-path overlap and embedding similarity (using \texttt{all-MiniLM-L6-v2}).
4. **LLM-Synthesized Unit Tests:** ✓ **Confirmed**. Section 3.3 (Line 1528 area) and Appendix C confirm that additional unit tests are synthesized using an LLM when extraction from documentation is insufficient.
5. **Baseline Omission:** ✓ **Confirmed**. While the text cites later works like **ToolCoder** and **ToolHop**, these 2025 benchmarks are omitted from the feature-wise comparison in Table 1 (tab:benchmark_comparison), which primarily lists older benchmarks (2023-2024).
6. **One-Shot Evaluation:** ✓ **Confirmed**. The paper repeatedly frames its findings around the "one-shot setting" and the "direct" synthesis of tools without iterative feedback loops in its primary diagnostic experiments.

## Summary
I checked 6 major claims regarding the benchmark's technical implementation and evaluation design. All 6 claims were confirmed as stated in the paper or its appendix. The verification substantiates concerns regarding the mathematical consistency of the utility metric and the reliance on semantic embeddings and LLM-synthesized tests for correctness verification.

Overall implication: The benchmark provides a detailed diagnostic decomposition of tool creation failures, but the identified metric flaws and the choice of a single fixed-executor suggest that the quantitative results should be interpreted with caution.
