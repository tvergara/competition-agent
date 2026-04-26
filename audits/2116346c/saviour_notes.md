# Saviour notes for 2116346c

The paper introduces SynthSAEBench, a synthetic known-feature benchmark and toolkit for evaluating sparse autoencoder architectures under controlled superposition, hierarchy, and correlation.

Observation 1: The benchmark artifact is quite concrete: SynthSAEBench-16k has 16,384 ground-truth features in a 768-dimensional hidden space, uses 200M training samples per SAE, and the authors report 15-20 minutes per width-4096 SAE on a single H100; the sampler runs at about 300K samples/sec for the 16k model.

Observation 2: Some architecture comparisons use deliberately modified training recipes rather than off-the-shelf variants: JumpReLU uses zero encoder-bias initialization, initial threshold and latent norm 0.5 rather than 0.1, and a TopK auxiliary loss; Matryoshka uses a per-prefix auxiliary loss designed to reduce dead latents at low L0.

Observation 3: The correlation ablation is presented as a weaker signal than the headline superposition result: increasing correlation scale mostly raises explained variance, gives slight F1 decreases, mixed MCC changes, and the authors state that correlation effects are likely overshadowed by superposition noise and hierarchy.
