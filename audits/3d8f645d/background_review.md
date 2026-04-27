# Background and Novelty Assessment: Super Research (3d8f645d)

## Summary of Findings
While the **Super Research** benchmark introduces a promising "high-ceiling" evaluation framework for autonomous agents, its claim to address a "largely unexplored" complexity tier is weakened by the omission of key contemporary benchmarks. Additionally, the core technical contribution—the graph-anchored auditing protocol—lacks essential human cross-validation.

## 1. Omission of Expert-Level Benchmarks
The manuscript claims that current evaluation paradigms are ill-suited for super-complex inquiry. However, it fails to position itself against or compare with:
- **BrowseComp (OpenAI, 2024)**: Evaluates autonomous web research and long-horizon retrieval for verifiable questions.
- **Humanity's Last Exam (HLE, 2025)**: Targets expert-level reasoning and retrieval across diverse domains.
Without a comparative analysis or a clear explanation of what specific difficulty class Super Research surfaces that these benchmarks do not, the "novel complexity tier" claim remains unsupported.

## 2. Unvalidated Auditing Protocol
The proposed **graph-anchored auditing protocol** is the primary methodological innovation for evaluating open-ended reports. However:
- The protocol relies on an LLM judge to map generated claims onto an expert-curated Research Graph. 
- The reliability of this automated auditor is not validated against human expert ratings (e.g., via Cohen's κ). 
Without establishing inter-rater agreement between the auditor and human experts, the metric's validity as a proxy for research quality is an untested assumption.

## 3. Undisclosed Construction Protocol
The benchmark's representativeness as a "powerful proxy for general research competence" depends on the diversity and calibration of the 300 questions. The manuscript lacks disclosure regarding:
- The selection criteria for the "experts" who wrote the questions.
- The inter-expert agreement on difficulty categorization.
- The distribution of question types (e.g., factual synthesis vs. reasoning under conflicting evidence).

## Conclusion
We recommend the authors integrate BrowseComp and HLE into their related work and comparative results. Furthermore, validating the graph-anchored auditor against human experts and disclosing the question-construction protocol would significantly strengthen the benchmark's standing as a reliable ceiling evaluation for LLMs.
