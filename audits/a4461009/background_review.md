# Background and Novelty Review: A Neuropsychologically Grounded Evaluation of LLM Cognitive Abilities

## Paper Contribution Summary
The paper introduces the **NeuroCognition benchmark**, which adapts three classic neuropsychological tests to evaluate Large Language Models (LLMs) and Multimodal Large Language Models (MLLMs): **Raven's Progressive Matrices (RPM)** for abstract relational reasoning, **Spatial Working Memory (SWM)** for maintenance and systematic search, and the **Wisconsin Card Sorting Test (WCST)** for cognitive flexibility. The authors evaluate 156 models and perform an exploratory factor analysis (EFA), claiming the existence of a single "general factor" of capability across 10 standard benchmarks. The study finds that while models perform well on text-based versions of these tests, their performance significantly degrades in multimodal (image-based) settings and with increased task complexity.

## Closest Prior Works
1.  **Hao et al. 2025 (arXiv:2505.22112)**: "Visual Large Language Models Exhibit Human-Level Cognitive Flexibility in the Wisconsin Card Sorting Test". This work evaluates VLLMs on WCST in both text and image modalities, finding that models can achieve human-level set-shifting but are sensitive to modality.
2.  **De Langis et al. 2025 (arXiv:2504.02789)**: "A Framework for Robust Cognitive Evaluation of LLMs" (CognitivEval). This paper introduces a suite of 5 neuropsychological tests, including WCST and Working Memory (N-back), focusing on text-based robust evaluation.
3.  **Zhang et al. 2024 (arXiv:2403.04732)**: "How Far Are We from Intelligent Visual Deductive Reasoning?". This work evaluates LMMs on RPM (using the RAVEN dataset) and highlights perception and reasoning gaps in visual settings.
4.  **Karamcheti et al. 2024 (arXiv:2401.12117)**: "The Curious Case of Nonverbal Abstract Reasoning with Multi-Modal Large Language Models". This paper assesses MLLMs on RPM and abstract reasoning tasks, identifying critical perception limitations.
5.  **Burnell et al. 2023 (arXiv:2306.10062)**: "Revealing the structure of language model capabilities". This paper performs a factor analysis on LLM benchmarks and identifies three distinct factors (Reasoning, Comprehension, Core LM) rather than a single general factor.

## Three-Axis Assessment

### 1. Attribution
The paper has significant attribution gaps regarding recent work that applies neuropsychological suites and specific abstract reasoning tests to LLMs:
*   **Omission of CognitivEval (De Langis et al. 2025)**: The paper claims that previous attempts to apply neuropsychological tests to LLMs are "limited to a single task" (p. 1). However, De Langis et al. 2025 introduced a suite of 5 different tasks (including WCST and Working Memory) specifically for LLM cognitive profiling.
*   **Omission of Zhang et al. 2024 and Karamcheti et al. 2024**: Both papers evaluated LMMs on the RAVEN (RPM) dataset and performed detailed analysis of visual reasoning failures. The paper under review uses the same RAVEN dataset for its RPM component but does not cite these precursors or position its findings against theirs.
*   **Mischaracterization of Hao et al. 2025**: The paper claims prior work is "limited to a single... modality" (p. 1). However, Hao et al. 2025 explicitly compared text-based vs. image-based WCST performance, which is one of the core modalities investigated here.

### 2. Novelty
The paper's claim of being the first to provide a comprehensive, multi-task, multimodal neuropsychological benchmark is overstated given the existence of CognitivEval (multi-task) and the multimodal work by Hao et al. and Zhang et al. 
*   The **genuinely novel aspect** is the specific combination of these three tasks (RPM, SWM, WCST) in a single multimodal framework and the large-scale evaluation of 156 models.
*   The finding of a **unified general factor (g-factor)** across 156 models is a significant and novel contrast to the three-factor structure identified by Burnell et al. 2023.

### 3. Baselines
The paper fails to use relevant prior benchmarks as baselines:
*   **Missing Baseline Comparisons**: Despite evaluating WCST and RPM, the paper does not compare its performance results or error distributions with those reported in Hao et al. 2025 (WCST) or Zhang et al. 2024 (RPM).
*   **Methodological Positioning**: The paper does not discuss how its specific SWM (CANTAB-style) implementation compares with other working memory assessments like N-back used in previous LLM studies (e.g., De Langis et al., Gong et al.).

## Overall Verdict
**Not Novel / Misrepresenting Prior Work**. While the scale of evaluation and the g-factor analysis are valuable, the paper's core novelty claim (being the first multi-task/multimodal neuropsychological suite) is built on an inaccurate characterization and omission of several highly relevant prior works (De Langis et al. 2025, Zhang et al. 2024). The paper fails to cite these closest neighbors and does not use them as comparative baselines.
