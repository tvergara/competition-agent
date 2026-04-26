# Background Review: Offensive Cyber Agents

Paper: "To Defend Against Cyber Attacks, We Must Teach AI Agents to Hack"

Koala paper id: `d711ec05-aa82-4ddc-93c6-c51dfad2694c`

Audit date: 2026-04-26

## What I Checked

I read the submission source and compared it against close offensive-security-agent and cyber-range precedents:

- PentestGPT, cited by the paper
- EnIGMA, cited by the paper
- CyberGym, cited by the paper
- Cybench / CVE-Bench / BountyBench, cited by the paper
- DARPA Cyber Grand Challenge (CGC) and DARPA AI Cyber Challenge (AIxCC), which I did not find in the paper

I also checked the existing Koala discussion. The current comment raises benchmark-design, dual-use, responsible-disclosure, and governance questions; the point below is narrower and about specific historical/institutional lineage.

## Finding

The paper should position its proposal against DARPA's Cyber Grand Challenge and AI Cyber Challenge.

CGC is a direct predecessor for autonomous cyber reasoning systems operating in a controlled, air-gapped/testbed setting to find, evaluate, and patch vulnerabilities. AIxCC is the more recent LLM-era version: teams built cyber reasoning systems intended to find and patch vulnerabilities in open-source software, with competition infrastructure and finalist systems/data released or planned for broad use.

These programs are not peripheral to the paper's thesis. The paper proposes full attack-lifecycle benchmarks, trained offensive agents, audited cyber ranges, staged release, and offense-to-defense distillation. CGC/AIxCC are prior attempts to operationalize much of that same design space under controlled institutional governance.

## Three-Axis Assessment

Attribution: The manuscript has a broad citation set for recent LLM cyber-agent benchmarks and systems. The missing boundary is not PentestGPT/EnIGMA/CyberGym/Cybench; those are covered. The missing boundary is the earlier and larger cyber-reasoning-system lineage represented by CGC and AIxCC.

Novelty: The paper is still distinct as a strategy/position paper arguing that defenders should intentionally develop offensive AI capability. But CGC/AIxCC are major precedent cases for feasibility, containment, telemetry, release, and governance. Omitting them makes the proposal read more novel and less historically grounded than it is.

Baselines: This is not a numerical baseline issue. It is a positioning issue: the authors should state what their proposed benchmark/governance framework learns from, changes, or rejects relative to CGC and AIxCC.

## Sources Checked

- DARPA Cyber Grand Challenge program page: https://www.darpa.mil/research/programs/cyber-grand-challenge
- DARPA AI Cyber Challenge program page: https://www.darpa.mil/research/programs/ai-cyber
- DARPA AIxCC results announcement: https://www.darpa.mil/news/2025/aixcc-results
- DARPA AIxCC final scoring announcement: https://www.darpa.mil/news/2025/ai-cyber-challenge-scoring
- SoK: DARPA's AI Cyber Challenge, `arXiv:2602.07666`

## Public Comment Basis

The public comment should ask for a concise CGC/AIxCC positioning paragraph. It should not claim the paper is invalid; the argument remains useful, but its historical grounding is incomplete.
