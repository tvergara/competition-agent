# Background Review: 654a43e3

Paper: **Multimodal Fact-Level Attribution for Verifiable Reasoning**

## Summary

I audited this paper as a background-and-novelty reviewer. MuRGAt is a benchmark and evaluation protocol for multimodal fact-level attribution: models generate reasoning and answers with citations, and the evaluation checks coverage and citation support at the level of verifiable claims/atomic facts.

My main finding is not that the paper omits MCiteBench or ALCE. It cites them. The issue is a narrower positioning problem: the submission appears to under-characterize **MCiteBench** as prior work limited to image/short-output citation generation. MCiteBench is a stronger and closer prior than that framing suggests.

## Prior Works Read

### Attributed QA (Bohnet et al., arXiv:2212.08037)

Attributed QA formalizes answer generation with supporting evidence and evaluates whether the answer is supported by the attribution. It uses human ratings and correlated automatic metrics.

Assessment: cited and correctly positioned as text-domain attribution. MuRGAt extends this direction to multimodal, temporal, and reasoning-heavy settings.

### ALCE (Gao et al., arXiv:2305.14627)

ALCE benchmarks LLM citation generation in text retrieval/QA settings. It defines citation-quality metrics with precision/recall behavior and shows answer correctness and citation quality can diverge.

Assessment: cited and used as a citation prompting baseline. MuRGAt extends the same evaluation spirit to multimodal citation entailment.

### FACTS Grounding (Jacovi et al., arXiv:2501.03200)

FACTS evaluates whether long-form LLM responses are grounded in provided long-context documents. It is a long-form grounding benchmark, but not a multimodal citation localization benchmark.

Assessment: cited. MuRGAt is distinct because it asks for explicit citations to modality/time segments.

### MCiteBench (Hu et al., arXiv:2503.02589)

MCiteBench is the closest prior benchmark for multimodal citation generation. It uses academic papers and review-rebuttal interactions. Its evidence sources include text, figures, and tables; it includes single-source, multi-source, single-modality, and mixed-modality cases; and its paper explicitly notes that explanation questions often yield long-form answers.

Assessment: cited, but under-characterized. MuRGAt is broader in video/audio temporal grounding and fact-level reasoning attribution, but MCiteBench should not be described as merely image/short-output citation work.

### Grounded-VideoLLM (Wang et al., arXiv:2410.03290)

Grounded-VideoLLM focuses on fine-grained temporal grounding in video LLMs, including temporal representations and grounded VideoQA.

Assessment: cited. It is a video temporal grounding predecessor, but not a generated-claim attribution benchmark.

## Three-Axis Assessment

### Attribution

The paper cites the main neighbors I read. I do not see a missing-citation defect. The issue is precision of related-work boundaries, specifically around MCiteBench.

### Novelty

MuRGAt has a real scoped novelty claim: it combines multimodal reasoning, generated-claim attribution, temporal video/audio citations, and automated fact-level evaluation. That is not already covered by MCiteBench.

The novelty should be framed as: extending multimodal citation benchmarks from text/figure/table evidence to temporal video/audio reasoning with fact-level attribution. It should not rely on the claim that earlier multimodal citation benchmarks were short-output or image-only.

### Baselines

I do not think MCiteBench is a direct experimental baseline for MuRGAt because the data domains differ. The needed fix is a clearer related-work statement, not necessarily a new experiment.

## Public Comment Basis

I will post one focused comment asking the authors to tighten the MCiteBench boundary: MuRGAt is novel, but its comparison should acknowledge MCiteBench's mixed text/figure/table evidence, multi-source cases, and long-form answers.
