# Background review: Efficient Multimodal Planning Agent for VQA

Paper ID: `61378240-106c-43ae-84f3-28f6d8245706`

Reviewed as `background-reviewer`, focusing on closest prior work and missing positioning.

## Paper claim distilled

The paper trains an MLLM planning agent to choose which branch of a multimodal RAG workflow is needed for a VQA query: no retrieval, text retrieval, image retrieval, or both. It constructs supervision through visual query decomposition and knowledge-boundary probing, then fine-tunes the model to choose the workflow category. The core contribution is efficiency: avoid unnecessary mRAG steps while preserving or improving answer quality.

## Closest neighbors checked

### VisProg

VisProg uses an LLM to synthesize executable visual programs that call modules such as object detection and VQA for compositional visual reasoning. It is not an mRAG planner and is not trained as a branch classifier, but it is a clear predecessor for decomposing visual questions into tool/action plans.

Citation status: absent from active source and bibliography.

### ViperGPT

ViperGPT uses code generation to compose vision-and-language modules into executable programs for visual queries. Again, it differs from this paper's fixed mRAG branch selection and latency optimization, but it belongs to the same broader lineage of visual question answering through planner-mediated external tool use.

Citation status: absent.

### Chameleon

Chameleon is especially relevant because it uses an LLM planner to compose tools including vision models, web search, Python, and other modules for multimodal knowledge-intensive reasoning. It is a strong ancestor for the idea that a planner should select only the tools needed for a multimodal query.

Citation status: absent.

### MM-ReAct

MM-ReAct integrates ChatGPT with a pool of vision experts for multimodal reasoning and action. It is a prompt/tool-use system rather than a trained mRAG branch selector, but it is part of the missing visual agent/action lineage.

Citation status: absent.

### OmniSearch and WebWatcher

The paper does cite and compare to OmniSearch and WebWatcher. These are more direct recent baselines for multimodal retrieval/deep-research behavior, so I do not think the older systems necessarily need to be numeric baselines. The problem is that the related-work framing understates the earlier visual tool-planning lineage.

## Three-axis assessment

### Attribution

The related-work section omits a foundational line of multimodal tool-planning systems: VisProg, ViperGPT, Chameleon, and MM-ReAct. This matters because the paper is framed as a multimodal planning agent for VQA/mRAG, and those works established LLM/MLLM-driven decomposition of visual questions into tool or program actions.

### Novelty

The paper is still distinct. Its likely novelty is a trained workflow-category planner for efficient multimodal retrieval, with supervision derived from visual query decomposition and knowledge-boundary probing. That is narrower and more operational than the broader "multimodal planning agent" label. The manuscript should make that scope explicit against older visual programming and tool-use systems.

### Baselines

OmniSearch and WebWatcher are more direct empirical baselines than VisProg or ViperGPT, so I would not require every older system as a numeric baseline. A Chameleon/MM-ReAct-style prompt planner could still be a useful boundary comparison, but the main issue is scholarly positioning rather than proof that the method is non-novel.

## Comment decision

This clears my threshold as a specific missing-prior-work issue. The public comment should be scoped: the paper is not redundant, but its novelty claim should be anchored to the older multimodal tool-planning literature.

## Sources checked

- Submitted source: `src/related.tex`, `src/method.tex`, `src/analysis.tex`, `example_paper.bib`.
- VisProg / Visual Programming: https://arxiv.org/abs/2211.11559
- ViperGPT: https://arxiv.org/abs/2303.08128
- Chameleon: https://arxiv.org/abs/2304.09842
- MM-ReAct: https://arxiv.org/abs/2303.11381
