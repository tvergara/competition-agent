# Background Review: REAL

Paper: "REAL: Resolving Knowledge Conflicts in Knowledge-Intensive Visual Question Answering via Reasoning-Pivot Alignment"

Koala paper id: `0b22fbe8-5ab4-4944-8081-40e9cbf49de8`

Audit date: 2026-04-26

## What I Checked

I read the REAL submission source/PDF and compared it against five close retrieval-augmented or knowledge-intensive VQA neighbors:

- EchoSight, "Advancing visual-language models with Wiki knowledge" (`arXiv:2407.12735`)
- RoRA-VLM, "Robust retrieval-augmented vision language models" (`arXiv:2410.08876`)
- mR2AG, "Multimodal Retrieval-Reflection-Augmented Generation for Knowledge-Based VQA" (`arXiv:2411.15041`)
- mKG-RAG, "Multimodal Knowledge Graph-Enhanced RAG for Visual Question Answering" (`arXiv:2508.05318`)
- VLM-PRF, "Knowledge-based Visual Question Answer with Multimodal Processing, Retrieval and Filtering" (`arXiv:2510.14605`)

I also checked the existing Koala discussion and avoided duplicating the separate comment about CAD/RPGD lineage and patch-shuffle construction.

## Finding

The main related-work/baseline gap I found is mR2AG. REAL's `references.bib` includes mR2AG as `zhang2024mr`, but I did not find an active citation to that work in the LaTeX body or a corresponding row in the main E-VQA/InfoSeek comparison table.

This matters because mR2AG is not just a broad-topic neighbor. It is a retrieval-augmented knowledge-based VQA method that introduces retrieval-reflection and relevance-reflection to decide whether retrieval is needed and to select useful evidence from retrieved Wikipedia entries. Its paper reports results on InfoSeek and Encyclopedic-VQA under retrieved-knowledge settings, which are the same benchmark family REAL uses for its core KI-VQA evaluation.

## Three-Axis Assessment

Attribution: EchoSight, RoRA-VLM, mKG-RAG, and VLM-PRF are cited and/or evaluated. mR2AG is present in the BibTeX but appears absent from the active manuscript discussion, so the boundary to this close prior work is not explained.

Novelty: I do not think REAL is simply a restatement of mR2AG. REAL focuses on explicit reasoning-pivot conflicts and a geometric decoding intervention, while mR2AG focuses on adaptive retrieval and relevance reflection. The novelty concern is therefore about missing positioning, not duplication.

Baselines: mR2AG looks like an obvious baseline or at least a necessary context point for claims about robust use of retrieved knowledge on InfoSeek/Enc-VQA. If the authors believe it is not comparable because of retriever, split, model, or task differences, that exclusion should be stated explicitly.

## Public Comment Basis

The public comment should be narrow: ask the authors to cite/position mR2AG and either include it in the comparison or explain why it is not comparable. I would not characterize REAL as non-novel based on this alone.
