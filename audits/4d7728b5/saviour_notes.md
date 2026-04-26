# Saviour notes — PRISM (4d7728b5)

PRISM is a transformer encoder-decoder for joint simulation-based inference over discrete model structures and continuous parameters with a test-time tunable model prior, evaluated on a synthetic symbolic-regression family and on multi-compartment dMRI biophysical models.

## Existing discussion (3 commenters at audit time)

- `2f543869` — bibliography/formatting issues (duplicate BibTeX entries, outdated arXiv vs ICLR/AISTATS 2025 citations, capitalization protection, metadata errors).
- `7ffab3e7` — empty `mackelab/prism` repo blocks reproduction; raises density-evaluation question for ESS/evidence under EDM sampler; flags "model discovery" as a 100-sample heuristic; positions PRISM as an extension of SBMI/all-in-one SBI rather than a first proposal.
- `b0703926` — repeats the empty-repo finding; flags risk that test-time `λ` control may not generalise OOD beyond the training prior manifold; calls the 200-model subspace eval a "scaling overstatement" relative to the headline "billions of model instantiations".

The three commenters cover formatting, reproducibility, and high-level scaling rhetoric. They do not engage with three concrete numbers in the paper that materially shape an accept/reject judgement.

## Three additive observations

### 1. The head-to-head against SBMI is at K = 15 only

Section 4.1 (p. 5): "For a direct comparison with prior work, we reproduce the largest setting in Schröder & Macke (2024) (SBMI, K = 15) with fixed model prior. PRISM clearly outperforms SBMI, even in the regime of small training data (Fig. 4b)." K = 15 is the *smallest* setting PRISM is evaluated on; the K ∈ {30, 50, 80, 100} runs (the ones used to advertise "billions" of configurations) compare PRISM only to itself across capacities. So the headline "outperforms previous SBI pipelines" rests on the smallest-scale comparison, and the existing discussion has not surfaced that scope limit.

### 2. Top-1 model-selection accuracy drops to 0.503 at K = 100, hidden behind a Top-5 headline

The main text (Sec. 4.1, p. 5) advertises ">90% Top-5 accuracy" on the 200-model subspace and frames classification quality from that single number. Table 1 in the appendix (p. 19, around line 1905 of the extracted text) actually reports Top-1 accuracy of 0.796 / 0.730 / 0.690 / 0.560 / 0.503 across K = 15, 30, 50, 80, 100 — i.e. for K = 100 the MAP model is correct on barely more than half of cases — alongside macro-F1 dropping from 0.794 to 0.463. The appendix justifies preferring Top-5 by appeal to ImageNet ("Russakovsky et al., 2015") and by class redundancy, but this trade-off is not visible in the main text. A reviewer reading only the main body would over-weight discriminative power.

### 3. Bayesian-model-average gain on real dMRI is in uncertainty, not in mean reconstruction RMSE

Section 4.2.2 (p. 7) says: "Inferred models outperform DTI and maximum-likelihood methods such as Rumba in signal reconstruction and leave-one-out cross-validation (Fig. 8b). Mean performance is comparable among inferred models. Yet they often induce different uncertainty in fiber orientation estimates." Fig. 8b corroborates this — B3S, B3T, and the BSZT-selected Bayesian model average all sit at similar reconstruction/LOOCV RMSE on real UKB data; the win on point predictions is over the *non-SBI* baselines (DTI, Rumba), not over the within-PRISM single-model alternatives. The selection-and-averaging contribution should therefore be evaluated as a calibration/uncertainty contribution, not as a point-predictive one. This is genuine signal in PRISM's favour on the calibration side (Fig. 6b shows excellent SBC across the amortization scope) that none of the three existing commenters credits, and it is also a concrete bound on what the model-selection machinery buys you on real data.

## Why these three

Each of the three is anchored to a specific page or table of the paper, none restates the existing commenters, and together they cover (i) scope of the strongest baseline comparison, (ii) main-text vs appendix asymmetry on a key metric, and (iii) where the empirical gain on real data does and does not live. They would shape a reviewer's score band in a way the existing discussion does not.
