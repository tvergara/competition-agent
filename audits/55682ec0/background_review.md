# Background Review: AI Agent Reliability

Paper: "Towards a Science of AI Agent Reliability"

Koala paper id: `55682ec0-bf7c-4867-a7ea-45f80255f45e`

Audit date: 2026-04-26

## What I Checked

I read the submission source and compared it against five close agent-evaluation neighbors:

- Holistic Agent Leaderboard (`arXiv:2510.11977`)
- tau-bench (`arXiv:2406.12045`)
- "When Agents Disagree With Themselves: Measuring Behavioral Consistency in LLM-Based Agents" (`arXiv:2602.11619`)
- RUPBench (`arXiv:2406.11020`)
- AgentHarm (`arXiv:2410.09024`)

I also checked the existing Koala discussion. The current public comment raises metric redundancy, trajectory-distance semantics, safety aggregation, and scaffold invariance; it does not cover the consistency-prior issue below.

## Finding

The main related-work gap I found is Mehta (2026), "When Agents Disagree With Themselves." I could not find this work in the active text or bibliography.

This is a close neighbor for the paper's consistency pillar. It repeatedly runs ReAct-style agents on identical HotpotQA tasks and measures unique action-sequence diversity, step-count variance, and first-divergence points. Its central empirical finding is that repeated-run behavioral consistency predicts correctness, and that early trajectory divergence is a major source of downstream failure.

## Three-Axis Assessment

Attribution: The paper cites tau-bench for pass^k, HAL for holistic infrastructure, RUPBench for perturbation robustness, and AgentHarm for agent safety. It also cites broader consistency/reproducibility work. But Mehta (2026) is agent-specific and directly overlaps with outcome/trajectory/resource consistency, so it should be cited and positioned.

Novelty: The reliability paper is broader than Mehta (2026). It adds robustness, predictability, safety, a safety-critical engineering framing, and experiments over GAIA and tau-bench. The missing citation does not make the paper a duplicate.

Baselines: This is not necessarily a missing numerical baseline because Mehta's setup is a HotpotQA/ReAct study rather than the paper's GAIA/tau-bench evaluation. It is a missing boundary comparison: the authors should explain how their trajectory consistency metrics extend or differ from unique action-sequence diversity, first-divergence analysis, and consistency-as-confidence-signal findings.

## Public Comment Basis

The public comment should be narrow: cite and position Mehta (2026) in the consistency section. The paper's broader framework remains distinct.
