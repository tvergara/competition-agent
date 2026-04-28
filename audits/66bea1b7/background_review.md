# Background and Novelty Review: ICA

## Paper Summary
The paper introduces **ICA (Information-Aware Credit Assignment)**, a reinforcement learning framework for long-horizon information-seeking agents. It addresses the signal-to-noise bottleneck in web agents through two main contributions:
1.  **Visual-native search framework**: Webpages are represented as rendered snapshots instead of linearized text, preserving structural and non-textual cues.
2.  **Information-Aware Credit Assignment (ICA)**: A post-hoc, information-centric credit attribution method that estimates the marginal utility of acquired evidence units (atomic evidence units) by their posterior association with successful outcomes in a batch.

The method is integrated with **GRPO** and demonstrates significant improvements over text-based baselines across multiple benchmarks (GAIA, Xbench-DS, BrowseComp, Seal-0).

## Comparison with Prior Works
1.  **IGPO (Wang et al., 2025): "Information gain-based policy optimization"**
    *   *Relationship*: IGPO rewards each turn by the marginal increase in the model's internal probability of the correct answer. ICA shifts this to a posterior, batch-level association between *actual outcomes* and *acquired evidence*.
    *   *Citation*: Correctly cited.
2.  **C-GRPO (Zhang et al., 2026): "Chaining the evidence: Robust RL for Deep Search Agents"**
    *   *Relationship*: C-GRPO uses citation-aware rubric rewards based on question decomposition. ICA uses unstructured evidence (snapshots) and posterior success association, achieving much higher performance (+18.5 on GAIA).
    *   *Citation*: Correctly cited.
3.  **DAPO (Yu et al., 2025): "DAPO: An open-source llm reinforcement learning system"**
    *   *Relationship*: Provides the underlying optimization framework (decoupled clipping and dynamic sampling) used in ICA-GRPO.
    *   *Citation*: Correctly cited.
4.  **Search-o1 (Jin et al., 2025): "Agentic search-enhanced large reasoning models"**
    *   *Relationship*: A strong search agent baseline. ICA outperforms Search-o1 by +7.8 points on GAIA.
    *   *Citation*: Correctly cited.
5.  **SeeClick (Cheng et al., 2024) / WebGUM (Furuta et al., 2023)**:
    *   *Relationship*: Prior works using visual input for web agents. ICA builds on this by using snapshots as persistent information units for post-hoc credit assignment.
    *   *Citation*: Closely related work on visual grounding is cited.

## Three-Axis Assessment
*   **Attribution**: Excellent. The paper is well-grounded in the latest deep search and RL literature (IGPO, C-GRPO, DAPO). It correctly identifies the limitations of action-centric and text-based approaches.
*   **Novelty**: **Clearly very novel**. The conceptual shift from action-centric to **information-centric credit assignment** via batch-level posterior success association is a significant and effective innovation. While the mathematical formulation (Equation 10) is simple, its application to rendered snapshots in a long-horizon setting is a powerful combination that yields state-of-the-art results.
*   **Baselines**: Comprehensive and up-to-date. The comparison spans the latest open-source (C-GRPO, Search-o1) and proprietary (OpenAI o3, DeepResearch) models. The large gains (+18.5 over C-GRPO) strongly validate the method.

## Overall Verdict
**Clearly very novel.** ICA introduces a principled and highly effective framework for addressing the credit assignment problem in information-seeking agents. By decoupling information acquisition from credit estimation and grounding the process in a visual-native modality, the authors achieve a new frontier in web agent performance.
