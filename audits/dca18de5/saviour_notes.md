# Saviour notes for dca18de5

MetaOthello studies how a small transformer trained on mixed Othello variants organizes shared, rotated, and game-specific board-state representations.

Observation 1: The artifact story is strong: the appendix lists public code, pretrained models and probes, and training data, and says the repository includes the game engine, data generation, model training, probe training, intervention analysis, and checkpoints.

Observation 2: The alpha score is an important methodological detail. It normalizes KL divergence against a random baseline over the full move vocabulary, which matters because DelFlank, NoMidFlip, and Classic have different valid-move branching factors and mixed-game states use posterior-weighted next-move distributions.

Observation 3: The global board-state intervention evidence is scoped by a fixed intervention recipe: probe vectors are added across all eight layers at once with gamma set to 5, and the paper notes this may over-intervene and is not fully optimized. That does not remove the result, but it makes single-layer/circuit-level follow-up important for interpreting causal transfer.
