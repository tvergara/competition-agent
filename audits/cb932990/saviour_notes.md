# Saviour Notes for cb932990

SurrogateSHAP proposes a training-free proxy game plus a GBDT/TreeSHAP estimator for contributor attribution in text-to-image diffusion models.

Observation 1: The baseline coverage is broad: the paper compares against similarity heuristics, IF/TRAK variants, Journey-TRAK, D-TRAK, DAS, LOO, and sparsified-FT Shapley in the LDS tables, and the background audit found no material missing direct citation among the closest checked neighbors.

Observation 2: The proxy-fidelity evidence is much stronger on CIFAR-20 than on the larger T2I settings: appendix results report proxy-vs-retraining Spearman correlations of 0.984 for CIFAR FID and 0.942 for CIFAR IS, but only 0.589 for ArtBench aesthetic score and 0.443/0.495 for Fashion LPIPS/diversity.

Observation 3: The estimator validation with exact Shapley ground truth is limited to synthetic games with N in {10,11}, while the real contributor sets include 258 ArtBench artists and 100 Fashion brands, so the TreeSHAP estimator's high-player regime is supported indirectly rather than by exact-ground-truth scaling tests.
