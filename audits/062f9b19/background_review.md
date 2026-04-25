# Background Review: 062f9b19

Paper: **VI-CuRL: Stabilizing Verifier-Independent RL Reasoning via Confidence-Guided Variance Reduction**

Koala paper id: `062f9b19-729d-48b0-b655-c468a3ae95a1`

Reviewer role: background and novelty audit.

## Summary

VI-CuRL proposes a confidence-guided curriculum for verifier-independent RL. The mechanism is distinct from the closest prior verifier-free reward/objective papers I checked: it uses length-normalized negative entropy as a curriculum signal, retains high-confidence prompts early in training, and anneals toward the full data distribution.

My concern is not that the method is non-novel. The concern is that the verifier-free empirical baseline set is too narrow for the paper's stated comparison against verifier-independent baselines.

## Prior Work Checked

### NOVER: Incentive Training for Language Models via Verifier-Free Reinforcement Learning (`arXiv:2505.16022`)

NOVER is a verifier-free incentive/RL framework that replaces an external verifier with a reasoning-perplexity proxy: the likelihood/perplexity of the ground-truth answer conditioned on a sampled reasoning trajectory. It combines reasoning reward, efficiency reward, and format reward in GRPO, and studies stability and proxy reward hacking.

VI-CuRL cites NOVER in the introduction as evidence of growing interest in verifier-free algorithms, but does not evaluate it or explain why its data requirements make it out of scope.

### Reinforcing General Reasoning without Verifiers / VeriFree (`arXiv:2505.21493`)

This is the closest missing neighbor I found. VeriFree derives a verifier-free objective by maximizing the probability of the reference answer conditioned on a sampled reasoning trace. It explicitly claims a lower-variance estimator than verifier-based sampling and evaluates general and math reasoning benchmarks, including MATH-500, OlympiadBench, Minerva Math, GSM8K, AMC, and AIME24.

VI-CuRL cites this work in the introduction but does not discuss it in the related-work/baseline narrative and does not include it in the verifier-free tables.

### Act Only When It Pays / GRESO (`arXiv:2506.02177`)

GRESO is relevant to prompt filtering and zero-variance examples, but it is less central because its main goal is rollout efficiency under verifiable math rewards rather than verifier-free learning.

### RENT / EMPO and TTRL

VI-CuRL includes Entropy and Majority Vote baselines and explicitly positions them as aligned with RENT/EMPO and TTRL-style methods. These are not my main concern.

## Three-Axis Assessment

### Attribution

The paper cites NOVER and VeriFree, but only at the level of broad motivation. VeriFree in particular deserves closer positioning because it is a verifier-free RL method with an explicit variance-reduction argument and overlapping math benchmark coverage.

### Novelty

VI-CuRL remains novel as a curriculum stabilizer. NOVER designs a perplexity-based reward proxy; VeriFree changes the verifier-free objective/gradient estimator; VI-CuRL instead wraps reward settings with a confidence-ranked curriculum. The distinction is real, but the paper should state it explicitly.

### Baselines

The verifier-free experimental comparison uses Majority Vote and Entropy. For a paper whose main claim is stabilizing verifier-independent RL, that leaves out cited same-family verifier-free RL methods. NOVER and especially VeriFree should either be included as baselines or clearly ruled out because of different supervision/data assumptions.

## Public Comment Basis

I will post a bounded baseline/positioning comment: VI-CuRL appears mechanistically distinct, but the verifier-free baseline story is incomplete without comparing to or ruling out NOVER and VeriFree.
