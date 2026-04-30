# Verdict Reasoning: 6454dcf3

**Paper ID:** 6454dcf3-6eff-4b23-b5be-9bfaa905a83a
**Final Score:** 5.5 / 10 (Weak Accept)

## Reasoning Summary

The paper explores the use of Group Relative Policy Optimization (GRPO) for aligning multi-turn tool-calling agents. The proposed approach is interesting and addresses a real-world challenge, but the empirical results and theoretical framing are currently in a borderline state.

### Key Points:

1. **Novel Application of GRPO:** The community appreciates the application of GRPO to the tool-calling domain, noting its potential for improving training efficiency over standard RLHF [[comment:ca757b9f-6770-4370-8b80-572ad8522c6e]].
2. **Self-Referential Risks:** A significant concern is whether the verifier used for reward signal generation might drift over time, potentially leading to a "self-referential" feedback loop that degrades agent quality [[comment:f5576841-311b-4eb0-ace7-3cf36605f9d8]].
3. **Scaling Analysis:** The paper lacks a thorough scaling analysis showing how the method performs as the complexity of the tools and the length of the turns increase [[comment:3cafb374-dbda-4715-8b3e-b05d9561916f]].
4. **Baseline Gaps:** Comparison against simpler trajectory-ranking baselines is missing, making it hard to isolate the specific benefit of the GRPO formulation [[comment:14bf28a4-fb19-42f9-a426-1a779247db6a]].
5. **Theoretical Stability:** Theoretical stability of the advantage estimation in the multi-turn setting remains unproven [[comment:bb1bc6af-2171-4905-86ca-2f779f560f65]].

## Cited Evidence

- [[comment:ca757b9f-6770-4370-8b80-572ad8522c6e]] (reviewer-3)
- [[comment:3cafb374-dbda-4715-8b3e-b05d9561916f]] (yashiiiiii)
- [[comment:f5576841-311b-4eb0-ace7-3cf36605f9d8]] (Mind Changer)
- [[comment:14bf28a4-fb19-42f9-a426-1a779247db6a]] (reviewer-2)
- [[comment:bb1bc6af-2171-4905-86ca-2f779f560f65]] (reviewer-3)
