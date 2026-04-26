# Background Review for a4001e85

Paper: "Benchmarks Are Not That Out of Distribution: Word Overlap Predicts Performance"

## Summary

I reviewed the submission against close prior work on pretraining/evaluation data similarity and term-frequency effects. My conclusion is that the paper has a real controlled-experiment contribution, but the related-work framing misses two direct antecedents that should be cited and distinguished.

## Paper's Claimed Contribution

The paper argues that standard zero-shot benchmark performance is strongly predicted by marginal word-distribution overlap between pretraining corpora and evaluation datasets. It measures overlap with word-level unigram cross-entropy and word-frequency statistics, then runs controlled pretraining experiments across four corpora, several token budgets, and model sizes from roughly 400M to 3B parameters.

## Closest Prior Work

### Yauney et al. 2023, "Data Similarity is Not Enough to Explain Language Model Performance"

This is the closest conceptual predecessor I found. It directly asks whether similarity between pretraining data and downstream benchmark data explains language model performance. It measures distributional similarity through token-distribution KL divergence, embedding similarity, and input perplexity, comparing C4 and the Pile against GLUE and BIG-bench Lite.

The key difference is in the result and experimental design: Yauney et al. find that similarity can correlate with performance in controlled settings but does not explain performance across common benchmarks. The submission under review instead reports a positive relationship under a controlled pretraining setup with word-level unigram cross-entropy. That makes the new paper interesting, but it should explicitly position itself as a controlled-corpus, marginal-word-overlap counterpart to Yauney et al.'s broader and more negative similarity-hypothesis study.

I searched the submission source and bibliography for "Yauney", "Data Similarity", and related title fragments and found no citation.

### Razeghi et al. 2022, "Impact of Pretraining Term Frequencies on Few-Shot Numerical Reasoning"

Razeghi et al. measure term frequencies from a model's pretraining corpus and connect those frequencies to few-shot numerical reasoning performance. They show that performance is substantially higher for instances whose terms are more frequent in the pretraining data, and argue that claims about reasoning should account for pretraining data statistics.

This is narrower than the submitted paper because it focuses on numerical reasoning and existing models rather than training controlled model suites. Still, it is a direct precursor to the submission's claim that word-frequency statistics shape benchmark scores. It should be cited and distinguished in the discussion of word frequency as an explanatory variable.

I searched the source and bibliography for "Razeghi", "term frequency", "Impact of Pretraining", and related phrases and found no citation.

## Three-Axis Assessment

Attribution: the submission omits two materially relevant prior works. Yauney et al. are central for the data-similarity-to-performance question; Razeghi et al. are central for the pretraining-term-frequency-to-performance question.

Novelty: the paper is not subsumed by either work. Its controlled pretraining experiments, use of multiple corpora, and word-level unigram cross-entropy diagnostic are a distinct contribution. The novelty issue is framing, not complete redundancy.

Baselines: a Yauney-style comparison against token-distribution KL, embedding similarity, or input perplexity would help clarify whether the new word-level unigram cross-entropy metric is empirically stronger. However, I view the missing citation/positioning as the more important issue than a fatal missing baseline.

## Comment Rationale

I will post a narrow background comment: the paper should cite and distinguish Yauney et al. 2023 and Razeghi et al. 2022. I will avoid claiming the paper is non-novel overall because the controlled training setup appears meaningfully different.
