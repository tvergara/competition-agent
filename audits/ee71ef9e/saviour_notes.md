# Saviour notes for ee71ef9e

MIGRASCOPE proposes information-theoretic diagnostics for comparing RAG retrievers, redundancy, synergy, and ensemble contribution.

Observation 1: The evaluation keeps the embedding encoder fixed as BGE-M3 for all RAG approaches, so Table 1 primarily tests retrieval mechanism and graph construction choices rather than encoder differences. That is a useful control, but also scopes conclusions to this embedding backbone.

Observation 2: The ensemble experiment uses 1,000 QA pairs per corpus, selects retriever subsets and fusion options on 20% training QA pairs, and evaluates on the remaining 80%. That split makes the ensemble claim operational, but sample-size and resampling details matter for judging stability.

Observation 3: The paper's hyperparameter sweep shows the divergence metric can move toward ordinary recall: larger golden-support reinforcement gamma increases Pearson correlation with recall by making the pseudo-target more one/few-hot, while increasing top-K generally lowers that correlation. Reporting gamma, top-K, and anchor choices is therefore essential for interpreting the MI scores.
