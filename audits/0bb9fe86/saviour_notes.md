# Saviour notes on 0bb9fe86

This paper audits whether simple code-generation baselines can match more elaborate code-evolution systems across mathematical bounds, agentic scaffolds, and MLE-bench competitions.

Observation 1: In the math-bounds appendix, the authors state that ShinkaEvolve was slightly hyperparameter-tuned because default settings were not competitive; the final setup used a 1024-token thinking budget, 5 islands instead of 2, and 2 archive programs instead of 4 to reduce API cost. This matters because the comparison is not just against an untouched default implementation.

Observation 2: The OpenEvolve appendix is a useful scope caveat: Gemini runs often crashed with `None` results and lacked thinking-budget/API-budget controls, so the paper reports a partial 300-generation GPT-5.2/GPT-5-mini comparison where OpenEvolve ran successfully on six problems and averaged rank 3.08 against the baselines and ShinkaEvolve.

Observation 3: The MLE-bench baselines are deliberately less minimal than the math/scaffold baselines: the appendix says zero-shot generated programs almost never run, so both baselines iteratively debug each generated solution until it runs successfully, preserving textual feedback while omitting AIDE's explicit fitness selection and full memory.
