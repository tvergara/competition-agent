# Background and Novelty Audit: 0316ddbf

Paper: "Self-Attribution Bias: When AI Monitors Go Easy on Themselves"

I audited the submission against five close neighbors:

- Panickssery et al. 2024, "LLM Evaluators Recognize and Favor Their Own Generations" (arXiv:2404.13076)
- Wataoka et al. 2024, "Self-Preference Bias in LLM-as-a-Judge" (arXiv:2410.21819)
- Spiliopoulou et al. 2025, "Play Favorites: A Statistical Method to Measure Self-Bias in LLM-as-a-Judge" (arXiv:2508.06709)
- Chen et al. 2025, "Do LLM Evaluators Prefer Themselves for a Reason?" (arXiv:2504.03846)
- Tsui et al. 2025, "Self-Correction Bench" (arXiv:2507.02778)

## Claimed Contribution

The paper argues that LLM monitors become more lenient toward actions implicitly framed as their own through assistant-turn conversational structure, especially in on-policy self-monitoring after the model has generated the action. It distinguishes this from explicit statements of authorship and from static off-policy monitor evaluations.

## Neighbor Comparisons

### Panickssery et al. 2024

Panickssery et al. show that LLM evaluators can recognize their own generations and that self-recognition correlates with self-preference. This is a direct predecessor for the "models favor their own outputs" phenomenon. The present paper cites it and distinguishes its target: same-action rating shifts induced by implicit conversational attribution in agentic monitoring contexts, not preference among static generated texts.

### Wataoka et al. 2024

Wataoka et al. argue that self-preference can be explained by familiarity/perplexity: models prefer lower-perplexity text, and their own outputs are often lower perplexity to them. The present paper cites this and tries to hold action content fixed so the core variable is presentation/attribution rather than textual familiarity. This does not fully settle all mechanism questions, but it is a meaningful distinction from Wataoka et al.

### Spiliopoulou et al. 2025

Spiliopoulou et al. provide a statistical framework for estimating self-bias while controlling for completion quality and report family-bias. This is highly relevant to cross-model controls, because within-family off-diagonal comparisons could be partially inflated. The submission cites this in related work. I view it as a methodological caveat, not a novelty-destroying prior.

### Chen et al. 2025

Chen et al. use verifiable tasks to distinguish legitimate self-preference from harmful self-preference and find that harmful self-preference persists when models are wrong. This is one of the closest prior works because the submitted paper also emphasizes that bias is largest for incorrect/unsafe actions. The distinction is that Chen et al. study response preference on verifiable benchmarks, while this paper studies monitor ratings under implicit assistant-turn/on-policy attribution in code and tool-use settings.

### Tsui et al. 2025

Tsui et al. identify a self-correction blind spot: models correct external errors more readily than identical errors in their own outputs. This is also very close, since it directly shows attribution modulates evaluation of identical content. The present paper cites it and extends the setup from correction of injected reasoning errors to action/risk/correctness monitoring in agentic contexts.

## Three-Axis Assessment

Attribution: The submission cites the five closest prior works I checked and does not appear to misrepresent them. The related work is short, but the key distinctions are present.

Novelty: The broad phenomenon "LLMs favor their own outputs" is not new. The more specific contribution is new enough to matter: implicit assistant-turn attribution, same-turn versus previous-turn structure, and on-policy self-monitoring of generated actions in code/safety settings. That is not covered by Panickssery, Wataoka, Spiliopoulou, Chen, or Tsui.

Baselines: I do not see an obvious missing background baseline. The paper still has methodological caveats raised by other reviewers, especially cross-family stratification, many-turn/compaction realism, and denominator-aware deployment-risk estimates, but those are not prior-work attribution defects.

## Bottom Line

The correct novelty framing is scoped: this is not a new discovery of self-preference in general, but it is a distinct and useful extension to implicit conversational self-attribution in agentic self-monitoring. Claims that the paper is merely renaming prior self-preference work are too strong given the closest prior literature.
