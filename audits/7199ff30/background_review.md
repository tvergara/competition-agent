# Background Review: Loss Knows Best

Paper: `7199ff30-a65c-4d84-bca6-0cc49e9ad373`

## Scope

I reviewed the paper against five close prior works on training-dynamics and loss-based label-error detection:

- Dataset Cartography: Mapping and Diagnosing Datasets with Training Dynamics
- Identifying Mislabeled Data using the Area Under the Margin Ranking
- An Empirical Study of Example Forgetting during Deep Neural Network Learning
- Deep Learning on a Data Diet: Finding Important Examples Early in Training
- Learning Discriminative Dynamics with Label Corruption for Noisy Label Detection

The submission proposes Cumulative Sample Loss (CSL): average per-frame loss over saved checkpoints, used as a post-hoc signal for detecting mislabeled or temporally disordered video annotations.

## Attribution

The attribution is partial. The paper cites Dataset Cartography, Confident Learning, Data Diet/EL2N, and DynaCor-style discriminative dynamics. However, it does not cite AUM or example forgetting, both of which are central training-dynamics methods for identifying mislabeled or noisy examples.

AUM is especially close: it computes an epoch-aggregated margin statistic and uses it to flag mislabeled examples. Example forgetting is also relevant because it established that noisy labels are concentrated among frequently forgotten examples. These are not peripheral references for this paper; they are part of the direct methodological lineage behind using per-example training trajectories as a data-quality signal.

## Novelty

The video-specific contribution appears useful but scoped. CSL adapts a training-dynamics idea to dense frame annotations, then adds temporal smoothing/interpretation for semantic mislabeling and phase disordering. That is materially different from static-image or text classification label cleaning.

The broad principle, however, is not new: model behavior across training can diagnose hard, ambiguous, or mislabeled examples. Dataset Cartography, AUM, forgetting events, EL2N/GraNd, and DynaCor all establish variants of that idea.

## Baselines

The main weakness is the baseline set. The experiments compare LossFormer mainly against video anomaly or procedural error detectors: HF2-VAD, SSPCAB, S3R, and EgoPED. Those are reasonable task-adjacent baselines, but they are not the closest baselines for the paper's central mechanism, which is loss/training-dynamics-based annotation error detection.

For semantic mislabeling, the paper should adapt at least a few direct training-dynamics baselines to frame-level scores:

- AUM: average assigned-label margin over checkpoints.
- Dataset Cartography: confidence and variability across checkpoints.
- DynaCor: learned/clustering-based training-dynamics representations.
- A simple early-loss or EL2N-style score.
- Optionally, a forgetting-event count over frame predictions.

For temporal disordering, the authors can fairly argue that direct prior baselines are less obvious; still, the semantic-mislabeling portion is close enough to existing noisy-label detection that the current SOTA claim is not well supported without these comparisons.

## Conclusion

I would not frame this as clearly non-novel. The video dense-annotation and disordering setting is a meaningful specialization. But the paper currently overstates the distinctiveness of CSL and the strength of its empirical comparison by omitting the most direct loss/training-dynamics label-error baselines.
