# Background Review: SynthSAEBench

Paper: `2116346c-4e22-4110-a553-dabf5ecb8750`

Title: SynthSAEBench: Evaluating Sparse Autoencoders on Scalable Realistic Synthetic Data

## Claim Distillation

The paper introduces SynthSAEBench, a scalable synthetic-data toolkit and standard 16k-feature benchmark for sparse autoencoder evaluation. Its main contribution is a known-ground-truth feature generator with configurable superposition, feature correlation, hierarchy, Zipfian firing rates, and firing magnitudes. This lets SAE architectures be compared on direct feature-recovery metrics, not only LLM proxy metrics. The strongest paper-specific empirical finding is that Matching Pursuit SAEs can improve reconstruction by exploiting superposition noise while degrading ground-truth feature recovery.

## Closest Neighbors Checked

1. Korznikov et al. 2026, "Sanity Checks for Sparse Autoencoders: Do SAEs Beat Random Baselines?", arXiv:2602.14111.
   - This is the closest omitted neighbor I found. It also studies SAE feature recovery on synthetic data with known ground-truth feature directions, reports a reconstruction-vs-feature-recovery mismatch, and adds random/frozen decoder or encoder sanity baselines on real activations.
   - Its synthetic setup is simpler than SynthSAEBench: 100-dimensional inputs, 3200 ground-truth features, constant and heavy-tailed firing regimes, and no integrated hierarchy/correlation/superposition benchmark artifact. Still, the research question overlaps directly.
   - It also reports that plain TopK behaves differently from BatchTopK, JumpReLU, and Matryoshka on its synthetic setup, making plain TopK a relevant baseline or at least a baseline to explicitly rule out.

2. Karvonen et al. 2025, "SAEBench: A Comprehensive Benchmark for Sparse Autoencoders in Language Model Interpretability", arXiv:2503.09532.
   - Cited and used appropriately as the main LLM-activation benchmark motivation. SynthSAEBench is positioned as complementary because SAEBench lacks true feature ground truth.

3. Elhage et al. 2022, "Toy Models of Superposition", arXiv:2209.10652.
   - Cited. This is the foundational synthetic superposition model; SynthSAEBench extends this line from small toy settings toward a reusable large-scale benchmark.

4. Chanin et al. 2025, "Feature Hedging: Correlated Features Break Narrow Sparse Autoencoders", arXiv:2505.11756.
   - Cited. This is directly relevant to correlation and hierarchy failure modes in SAEs. SynthSAEBench incorporates related phenomena at a larger benchmark scale.

5. Chanin and Garriga-Alonso 2025, "Sparse but Wrong: Incorrect L0 Leads to Incorrect Features in Sparse Autoencoders", arXiv:2508.16560.
   - Cited. This work uses known-feature toy models to show incorrect L0 can induce feature mixing; SynthSAEBench extends the known-feature benchmark setting but does not simply duplicate this contribution.

6. Costa et al. 2025, "From Flat to Hierarchical: Extracting Sparse Representations with Matching Pursuit", arXiv:2506.03093.
   - Cited as the MP-SAE source. SynthSAEBench's MP-SAE overfitting result is a useful counterpoint rather than a restatement.

## Three-Axis Assessment

### Attribution

The main attribution gap is Korznikov et al. 2026. It is materially relevant because it already asks whether SAEs recover known synthetic ground-truth features and shows that strong reconstruction can coexist with poor feature recovery. It also proposes random/frozen component baselines that are natural sanity checks for a benchmark intended to validate SAE architecture improvements.

The rest of the close prior-work map is mostly well covered: SAEBench, Toy Models of Superposition, Feature Hedging, Sparse but Wrong, and MP-SAE are cited and usually positioned correctly.

### Novelty

SynthSAEBench remains novel if scoped to the scalable and configurable benchmark artifact: 16k known features, realistic hidden dimension, controllable superposition/correlation/hierarchy, Zipfian firing, direct feature-recovery metrics, and a specific MP-SAE superposition-noise finding. Those aspects go beyond the closer prior.

The broad framing that synthetic known-feature data reveals a reconstruction-vs-feature-recovery mismatch should be softened, because Korznikov et al. already makes that point in a simpler but directly comparable synthetic setting.

### Baselines

The most important missing baseline/context is not another LLM benchmark but a close sanity-check family:

- Compare against or explicitly discuss Korznikov et al.'s synthetic setup and frozen/random baselines.
- Add plain TopK SAE or explain why BatchTopK/JumpReLU/Matryoshka/MP/L1 are sufficient, because the closest omitted work found TopK can behave differently in known-feature synthetic recovery.
- If frozen/random baselines are too expensive or not meaningful for all SynthSAEBench metrics, the paper should at least state which metrics require learned feature directions and which could be partially satisfied by random overcomplete dictionaries.

## Bottom Line

I would not call SynthSAEBench non-novel overall. The benchmark construction and MP-SAE superposition-noise diagnosis look like real contributions. But the related-work boundary is missing a very close known-feature SAE sanity-check paper, and the baseline set would be stronger with either a direct comparison to that setup or an explicit explanation of why its TopK and frozen/random baselines are not comparable.
