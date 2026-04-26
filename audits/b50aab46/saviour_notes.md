# Saviour notes for b50aab46

Draft-Conditioned Constrained Decoding proposes a two-stage, training-free structured generation method: first sample an unconstrained semantic draft, then generate a valid output under hard constraints while conditioning on that draft.

Observation 1: The empirical suite is broader than the GSM8K headline: the paper evaluates GSM8K, MATH500, GSM-Symbolic, and FOLIO with JSON schemas, expression grammars, and first-order-logic grammars, and counts success only when the answer is both semantically correct and structurally valid.

Observation 2: The test-time scaling comparison uses different units of repeated sampling: constrained decoding votes over multiple independently generated structured outputs, while DCCD votes over multiple unconstrained drafts and then runs a single constrained projection on the selected draft. The paper reports DCCD improving from 78% to 83% on GSM8K and 42% to 47% on MATH500 as n grows from 1 to 13, with gains saturating around n=7.

Observation 3: The appendix includes a non-verifiable TL;DR compression experiment under a 256-token budget. DCCD is judged against constrained decoding by Qwen2.5-14B-Instruct across overall quality, coverage, and faithfulness, with reported win rates of 78-80.5%; this is useful breadth, but it rests on a single-model LLM-as-judge protocol.
