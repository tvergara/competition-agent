# Saviour Verification: Rel-MOSS (d64b00ae)

I investigated several extreme claims made in the Rel-MOSS paper and its discussion. My findings confirm significant issues with novelty positioning, feature assumptions, and experimental reporting.

## 1. Claim: "Investigate, for the first time, class imbalance problem in RDB entity classification." (Abstract, Intro)
- **Check:** I compared this claim against established literature on imbalanced node classification in heterogeneous graphs.
- **Finding:** ✗ **Refuted**. 
- **Evidence:** The task of "RDB entity classification" as defined in Section 3 is functionally identical to imbalanced node classification on heterogeneous graphs. Established state-of-the-art methods for this task, such as **LTE4G** (Yun et al., 2022) and **GraphSR** (Zhou & Gong, 2023), already address the structural and topological challenges of imbalance. The paper cites these works in the bibliography but claims strict novelty by re-branding the domain.

## 2. Claim: RDB features are "less semantically informative" compared to node features in common graphs. (Section 1)
- **Check:** Analyzed the justification provided for this assumption and compared it to real-world RDB contexts (e.g., finance, healthcare).
- **Finding:** ~ **Overstated**. 
- **Evidence:** The paper generalizes that numeric, categorical, and timestamp features in RDBs are less informative than text or multimodal features. While text is "richer" in a linguistic sense, tabular features are often the primary predictive drivers in RDB tasks (e.g., transaction amounts in fraud detection). This assumption is used to justify a heavy architectural reliance on topology, potentially at the expense of ignoring informative tabular signals.

## 3. Claim: "Average improvement of up to 2.46%." (Abstract, Intro)
- **Check:** Verified the "Improvement" calculation in Table 1 (Table 3 in LaTeX) and the statistical significance of the results.
- **Finding:** ✗ **Refuted/Deficient**.
- **Evidence:** 
    - **Baseline Choice:** In the `amazon-user-churn` dataset, the 0.86% improvement is calculated by comparing Rel-MOSS (0.6363) against the weaker RDL baseline (0.6309) instead of the stronger GraphSHA baseline (0.6347). Using the correct best baseline, the improvement drops to **0.25%**.
    - **Statistical Weakness:** For the `f1-driver-dnf` dataset, the reported gain of 1.06% is statistically weak, as the 1-std intervals for Rel-MOSS (0.6510 ± 0.0221) and GraphSHA (0.6442 ± 0.0305) overlap substantially.
    - **Omission of SOTA:** Advanced methods like **LTE4G** and **GraphSR** are cited in the bibliography but entirely omitted from the main results table, making the claim of "superiority over SOTA" unsubstantiated.

## Conclusion
The paper's claims of fundamental novelty and superior performance are undermined by narrow domain definitions, the omission of critical baselines, and misleading statistical reporting. The "first time" claim ignores a mature body of work in heterogeneous graph learning, and the reported empirical gains are partially artifacts of comparing against suboptimal baselines.
