dnaHNet proposes a tokenizer-free autoregressive genomic foundation model using differentiable dynamic chunking to handle long DNA contexts efficiently.

- **Observation 1 (Inference Latency)**: The model achieves a >3x inference speedup compared to standard Transformers on genomic sequences, as its recursive chunking mechanism yields quadratic FLOP reductions (Abstract).
- **Observation 2 (Pretraining Focus)**: Pretraining is performed on a massive prokaryotic corpus (GTDB release 10, >700k bacterial/archaeal genomes), grounding its capability in bacterial and archaeal genomics (Abstract, Background Notes).
- **Observation 3 (Learned Boundaries)**: The differentiable chunking mechanism enables the discovery of hierarchical biological structures without explicit supervision, with learned boundaries aligning with codons, promoters, and intergenic regions (Abstract, Background Notes).
