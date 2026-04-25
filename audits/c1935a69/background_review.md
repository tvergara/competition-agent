# Background and Novelty Audit: c1935a69

Paper: "Consensus is Not Verification: Why Crowd Wisdom Strategies Fail for LLM Truthfulness"

I audited the submission against five close neighbors:

- Wang et al. 2023, "Self-Consistency Improves Chain of Thought Reasoning in Language Models" (arXiv:2203.11171)
- Schoenegger et al. 2024, "Wisdom of the Silicon Crowd" (arXiv:2402.19379)
- Kim et al. 2025, "Correlated Errors in Large Language Models" (arXiv:2506.07962)
- Goel et al. 2025, "Great Models Think Alike and this Undermines AI Oversight" (arXiv:2502.04313)
- Ai et al. 2025, "Beyond Majority Voting: LLM Aggregation by Leveraging Higher-Order Information" (arXiv:2510.01499)

## Claimed Contribution

The paper argues that inference-time aggregation helps when an external verifier exists, but does not reliably scale truthfulness in verifier-absent domains. It tests majority vote, confidence-based voting, predicted-popularity weighting, and Surprisingly Popular (SP) on binary factual/commonsense/expert/forecasting tasks, then diagnoses failure through correlated errors, confidence/consensus misalignment, and a random-string no-truth control.

## Neighbor Comparisons

### Wang et al. 2023: Self-consistency

Wang et al. sample multiple reasoning paths from a single model and majority-vote final answers, obtaining large gains on arithmetic, commonsense, symbolic, and some NLP tasks. The submission cites this correctly as a positive test-time scaling result in structured/verifiable reasoning. I do not see an attribution issue here: the submission's novelty is testing where this intuition stops applying.

### Schoenegger et al. 2024: LLM crowd forecasting

Schoenegger et al. is the closest positive prior result for the paper's forecasting angle. It aggregates forecasts from twelve LLMs on real-time Metaculus binary forecasting questions and reports that the LLM crowd beats a no-information baseline and is not statistically different from a human crowd under Brier score. This is not identical to the submission's binary forced-choice Predict-the-Future setup, but it directly addresses whether LLM ensembles can realize a wisdom-of-crowds effect in forecasting.

The submission's `references.bib` includes this work, but I found no main-text citation or discussion. Because the submitted paper reports a negative result for LLM aggregation on forecasting questions, it should explicitly contrast its protocol and conclusions with this positive prior result. Otherwise readers are left without the most relevant boundary condition: probabilistic forecasting aggregation over diverse LLMs can look useful in one setting, while forced-choice truthfulness polling fails here.

### Kim et al. 2025: Correlated LLM errors

Kim et al. measure whether different LLMs choose the same wrong answer when they err, across hundreds of models and several downstream settings. The submission cites this directly and uses it appropriately to motivate the correlated-error mechanism. The current paper adds a different contribution: showing how this correlation limits verifier-absent truthfulness aggregation and adding the random-string no-truth control.

### Goel et al. 2025: Similar mistakes in AI oversight

Goel et al. introduce a chance-adjusted probabilistic agreement metric over mistakes and show that more capable models can make more similar mistakes, with consequences for AI oversight. The submission cites it correctly for the claim that error correlation grows with capability and training similarity.

### Ai et al. 2025: Higher-order LLM aggregation

Ai et al. is directly relevant to the baseline set. It studies multi-agent LLM aggregation under model heterogeneity and correlation, arguing that majority voting ignores first-order expected accuracy and second-order answer correlations. It proposes Optimal Weight and Inverse Surprising Popularity (ISP), and reports improvements over majority voting on UltraFeedback, MMLU, and ARMMAN.

The submission's `references.bib` includes this paper, but I found no main-text citation or discussion. This matters because the submission says its five aggregation rules "exhaust common internal selection signals." Higher-order/correlation-aware aggregation is a plausible internal-selection family. It may require calibration data, pseudo-label assumptions, or repeated-question distributions that are unavailable in the submitted evaluation; if so, that should be stated as an exclusion. If applicable, ISP/OW-style methods are the natural missing baseline.

## Three-Axis Assessment

Attribution: The paper handles Wang et al., Kim et al., and Goel et al. appropriately. The main attribution gap is that Schoenegger et al. 2024 and Ai et al. 2025 are present in the bibliography but not integrated into the argument, despite being highly relevant to the forecasting and aggregation claims.

Novelty: The paper is not merely restating prior work. Its combination of verifier-absent truthfulness tasks, confidence/predicted-popularity/SP diagnostics, and random-string no-truth control is genuinely new relative to the five neighbors. The novelty is strongest if scoped as a negative result for tested polling-style endogenous aggregation under binary protocols.

Baselines: Ai et al.'s ISP/OW-style higher-order aggregation is the clearest omitted baseline or explicit boundary condition. Schoenegger et al. is not a direct answer-selection baseline, but it is an essential forecasting comparator that should be discussed when interpreting the Predict-the-Future result.

## Bottom Line

My recommendation is not that the paper lacks novelty. Rather, it has a real contribution but should tighten its related-work and baseline framing. In particular, it should explain why its negative forecasting result differs from Schoenegger et al.'s positive LLM-crowd forecasting result, and it should either evaluate or explicitly exclude Ai et al.'s higher-order correlation-aware aggregation family.
