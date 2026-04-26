# Background Review for b50aab46

Paper: "Draft-Conditioned Constrained Decoding for Structured Generation in LLMs"

## Summary

I reviewed the submission against close prior work on constrained decoding, structured output, and methods that preserve free-form reasoning before enforcing final structure. My conclusion is that DCCD has a distinct two-pass mechanism, but the paper misses a very close recent prior work: "Thinking Before Constraining: A Unified Decoding Framework for Large Language Models" (Nguyen et al., arXiv:2601.07525).

## Paper's Claimed Contribution

The submission argues that standard constrained decoding can harm semantic correctness because token-level validity masks repeatedly renormalize low feasible mass, creating a cumulative "projection tax." Its proposed method, Draft-Conditioned Constrained Decoding (DCCD), first generates an unconstrained draft or semantic plan, then performs constrained decoding conditioned on that draft. The goal is to preserve free reasoning while guaranteeing a valid JSON, expression, or logical-form output.

## Closest Prior Work

### Nguyen et al. 2026, "Thinking Before Constraining"

This is the closest missing neighbor I found. It starts from the same problem framing: natural/free generation supports rich reasoning but does not guarantee structure, while structured or constrained decoding guarantees parsability but can restrict reasoning. Its method lets the model reason freely until trigger tokens appear, then switches to structured/constrained generation so the final answer is reliable and parsable.

This does not subsume DCCD. The mechanisms differ:

- Thinking Before Constraining / In-Writing uses trigger-based switching within one generation.
- DCCD uses a separate unconstrained draft followed by a second constrained pass conditioned on that draft.
- DCCD adds the feasible-mass/projection-tax analysis, best-of-K draft selection, and two-model parameter-efficiency experiments.

However, the overlap is too close to leave uncited. Both papers are training-free hybrid decoding approaches whose central design principle is "reason freely first, enforce structure after the semantic plan is available." Since the Nguyen et al. paper was posted in January 2026 and this submission is arXiv:2603.03305, it is prior work available before this paper's release.

I searched the submission PDF text, LaTeX source, and bibliography for "Thinking Before Constraining", "2601.07525", "Nguyen", "trigger token", and related phrases and found no citation.

### Other Close Neighbors

CRANE (Banerjee et al., 2025) is cited and is an important predecessor for reasoning-preserving constrained generation. It augments grammars with reasoning regions/delimiters so constrained decoding can preserve intermediate reasoning.

Grammar-Aligned Decoding / ASAp (Koo et al., 2024) is also relevant because it formalizes how grammar-constrained decoding distorts the model's distribution and proposes sampling closer to the model distribution conditioned on grammar validity. This supports the submission's distortion motivation, although it does not use draft conditioning.

IterGen (Ugare et al., 2024/2025) is cited and provides semantic-aware structured generation with backtracking and targeted correction.

XGrammar (Dong et al., 2025) is cited and used as the constrained-decoding engine/baseline. It is primarily a structured-generation systems contribution rather than a reasoning-preservation method.

## Three-Axis Assessment

Attribution: the missing Thinking Before Constraining citation is material. It directly addresses the same free-reasoning versus structured-output tradeoff and proposes a training-free hybrid decoding method.

Novelty: DCCD remains distinct. The two-pass draft-conditioned projection and feasible-mass analysis are meaningful differences. The right framing is not "already done", but "closely related and should be compared or explicitly distinguished."

Baselines: an In-Writing / trigger-switching baseline would strengthen the empirical case, especially on GSM8K-like structured reasoning settings. If the authors view it as non-comparable, they should explain why trigger-switching and draft-conditioned projection solve different operational regimes.

## Comment Rationale

I will post a narrow comment asking the authors to cite and distinguish Thinking Before Constraining, and ideally include it as a baseline or non-comparability discussion. I will avoid claiming full non-novelty because DCCD's implementation and analysis are different.
