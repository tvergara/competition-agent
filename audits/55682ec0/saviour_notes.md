# Saviour notes for 55682ec0

This paper proposes a twelve-metric reliability profile for AI agents across consistency, robustness, predictability, and operational safety, evaluated on GAIA and a cleaned tau-bench airline subset.

Observation 1: The tau-bench experiment uses the SABER-verified 26-task subset after citing that 24 of the original 50 airline tasks have label, answer-key, or ambiguity errors; the paper also compares full vs clean results and reports that predictability and safety improve almost universally on the cleaned subset.

Observation 2: The core multi-run consistency protocol executes each task K = 5 times at temperature 0 for non-reasoning models, while reasoning models keep provider defaults; this isolates non-sampling nondeterminism, but the paper's own limitation notes that accuracy-maximizing nonzero-temperature deployments may be less reliable.

Observation 3: Predictability is measured through post-hoc self-assessed confidence from the evaluated agent, and safety/compliance severity is judged with GPT-4o over traces; this is practical for frontier APIs, but makes two important reliability axes depend on elicitation and judge behavior rather than direct ground-truth instrumentation alone.
