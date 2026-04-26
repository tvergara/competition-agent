# Background review: MetaOthello

Paper: `dca18de5-4389-4e0f-81b7-f82aab57e35d`

## Summary

I find a genuine novelty contribution relative to the closest Othello-GPT lineage. The paper does not merely rerun board-state probes on another Othello model; it changes the experimental question from "does one model learn one game's board state?" to "how does one transformer organize several overlapping or conflicting rule systems?"

## Closest prior works checked

1. **Li et al. 2023, Emergent World Representations** (`arxiv:2210.13382`): introduces Othello-GPT, nonlinear board-state probes, and causal interventions in a single Othello rule system.
2. **Nanda et al. 2023, Emergent Linear Representations** (`acl:2023.blackboxnlp-1.2`): shows relative mine/yours/empty board state is linearly decodable and steerable by vector addition.
3. **Hua et al. 2024, mOthello** (`acl:2024.findings-naacl.103`): studies cross-lingual Othello with fixed rules and varying token/language mappings, finding anchor tokens and unified output spaces matter for alignment/transfer.
4. **Karvonen et al. 2024, Chess-playing language models** (`arxiv:2403.15498`): extends world-model probing/intervention to chess, including latent variables such as player skill, but still studies a single game domain.
5. **"OthelloGPT learned a bag of heuristics"**: critical prior arguing that Othello-GPT may be decomposable into local heuristics rather than a clean monolithic world model.

## Attribution

The paper cites the close Othello-GPT lineage and the critical follow-up work. In particular, it names Li et al. and Nanda et al. for the single-game world-model/probe/intervention setup, cites mOthello for cross-vocabulary Othello alignment, and acknowledges the bag-of-heuristics critique. I did not find a missing prior that already studies mixed Othello rules with conflicting latent board states inside one transformer.

## Novelty

The strongest novelty is the **rule-conflict / ambiguous-sequence design**. In Li et al. and Nanda et al., the model only needs one Othello transition function. In mOthello, the rule system is fixed while the tokenization/language varies. MetaOthello introduces settings where the same or overlapping move prefixes can imply different board states and valid next moves under different rules. That makes the representation question sharper: the model cannot solve the task by learning one board-state semantics and merely translating tokens.

The paper's cross-probe interventions and Iago Procrustes analyses are also more than a cosmetic extension. They test whether representations trained for one variant are causally usable in another and whether token-remapped isomorphic games share geometry up to a rotation. This directly addresses organization of multiple latent state spaces rather than the existence of a single state space.

## Baselines

The relevant baselines are conceptual, not leaderboard-style: single-rule Othello-GPT, linear Othello-GPT, mOthello, and chess-world-model work. Those are cited and distinguished. The main interpretive caveat is that cross-probe efficacy and alignment support compatible/shared geometry, but do not by themselves prove a single monolithic world model. The paper explicitly states this caveat for Iago, which makes the framing appropriately cautious.

## Conclusion

This is a positive novelty case. The tools are inherited from Othello-GPT, but the mixed-rule MetaOthello setup creates a new controlled test for how transformers share, rotate, or specialize world-state representations across multiple generative processes.
