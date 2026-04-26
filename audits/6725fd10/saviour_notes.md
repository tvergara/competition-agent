# Saviour Notes: 6725fd10

This paper proposes NextMem, a latent factual-memory autoencoder for storing, reconstructing, using, and retrieving agent memories.

Observation 1: The main compression setting is concrete: NextMem-Dense and NextMem-Sparse generate 15 latent tokens from a Qwen3-8B backbone, use maximum encode/output length 1024, and train progressive substitution in 15 steps with block size 16; the ICAE baseline uses a public 128-token Mistral-7B checkpoint.

Observation 2: The contextual-generation table separates direct latent use from decompressed use. ICAE is best in all four compression columns, while NextMem's best results are mainly in the decompression columns, so its utilization advantage is clearest after reconstructing text rather than from direct latent conditioning.

Observation 3: The dataset processing narrows several benchmarks: HotpotQA uses only easy-level samples and supporting-fact sentences, SQuAD filters out unanswerable questions, LoCoMo selects only categories 1 and 5, and LongMemEval uses the cleaned LongMemEval-S split primarily for testing/evaluation.
