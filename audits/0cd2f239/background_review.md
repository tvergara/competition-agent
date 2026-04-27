# Background and Novelty Review: VIA-Bench

## Claimed Contributions
The paper introduces **VIA-Bench**, a diagnostic benchmark designed to probe Multimodal Large Language Models (MLLMs) on six categories of visual illusions and anomalies. It claims to be a pioneering effort to systematically evaluate how machine perception diverges from human perception in scenarios that defy common-sense priors.

## Prior Work Comparison
1. **HallusionBench (Guan et al., 2024)**: A comprehensive diagnostic suite for image-context reasoning and visual illusions. HallusionBench already covers many of the failure modes (hallucination vs. illusion) that VIA-Bench targets.
2. **TET: Turing Eye Test (Gao et al., 2025)**: A primary data source for VIA-Bench. TET already provides high-resolution perceptual datasets for evaluating model vision. VIA-Bench's contribution is largely an aggregation of TET samples with new QA pairs.
3. **GVIL (Zhang et al., 2023)**: Probed color and geometric illusions in vision models. VIA-Bench expands the taxonomy but covers similar ground.
4. **Illusory VQA (Rostamkhani et al., 2025)**: Another recent benchmark focusing on visual illusions.
5. **MMMU (Yue et al., 2024)**: While broader in scope, MMMU includes complex reasoning tasks that often involve high-level visual interpretation.

## Three-Axis Assessment

### Attribution
The paper cites **HallusionBench** and **GVIL** but fails to clearly state that the majority of its images are sourced from existing datasets like **TET (Gao et al., 2025)**. The "Related Works" section acknowledges prior benchmarks but does not sufficiently distinguish VIA-Bench's novelty beyond taxonomic expansion.

### Novelty
**Incremental and Derivative.** The work is primarily an aggregation effort. While the 1,004 curated QA pairs add value, the images themselves and the core research question (MLLM failure on visual illusions) are well-established in the literature. The "CoT Paradox" claim—that reasoning degrades performance—is supported by statistically insignificant margins (e.g., 0.15% drop), rendering this "novel" finding highly questionable.

### Baselines
The evaluation includes a text-only baseline (GPT-4-Turbo), which reveals a significant flaw: the model achieves high accuracy (87.95% on Motion Illusions) without seeing the images. This confirms that the benchmark is heavily influenced by linguistic priors, contradicting the claim that it measures "visual intelligence rather than linguistic bias."

## Verdict
**Clearly not novel.** VIA-Bench is a derivative aggregation of existing perceptual datasets (TET) and benchmarks (HallusionBench, GVIL). Its primary scientific claims are either already well-known or based on statistically insignificant data.
