# Background Review: 13cb28c8

Paper: STEP: Scientific Time-Series Encoder Pretraining via Cross-Domain Distillation

## Scope

I reviewed the submission as a background-and-novelty reviewer, focusing only on whether the closest prior work is cited and whether the baseline set isolates the claimed contribution. I did not re-litigate public-thread concerns about WBCIC, BrainOmni, frequency mismatch, distillation table presentation, or sample accounting.

## Submission Claim

The paper proposes STEP, a scientific time-series encoder with learnable adaptive patching, statistics compensation, and cross-domain distillation from audio, general time-series, and neural foundation models. The empirical claim is that STEP is an effective unified encoder/pretraining paradigm for heterogeneous scientific time series.

## Closest Prior Work Checked

### MOMENT: A Family of Open Time-series Foundation Models

MOMENT (ICML 2024; arXiv:2402.03885) is a family of open-source time-series foundation models pretrained on a large Time Series Pile. It explicitly targets general-purpose time-series analysis across forecasting, imputation, classification, and anomaly detection, including limited-supervision transfer.

This is a close neighbor because STEP's downstream suite is mostly classification-style scientific-signal tasks, not just forecasting. MOMENT is therefore a more direct baseline for "general-purpose transferable time-series representation" than decoder-only forecasting models alone. I did not find MOMENT in the active LaTeX source or bibliography.

### UniTS: A Unified Multi-Task Time Series Model

UniTS (NeurIPS 2024; arXiv:2403.00131) proposes a unified multi-task time-series model spanning forecasting, classification, anomaly detection, and imputation across heterogeneous multi-domain datasets. Its abstract and experiments emphasize transfer across varied temporal scales, sampling rates, and task specifications.

This is also a close neighbor for STEP's "unified encoder" framing. It is not a scientific-only model, but it is directly relevant as a general-purpose multi-task time-series foundation baseline. I did not find UniTS in the active source or bibliography.

### Cited Neighbors

The paper does cite/evaluate several relevant models:

- SciTS / TimeOmni is cited and discussed as scientific time-series context, including router-based patch sizing.
- Time-MoE and Moirai are cited and evaluated as general time-series foundation models.
- CBraMod and BrainOmni are cited as neural-signal foundation models.
- SPEAR and Whisper are cited as audio foundation models.

Those citations make the missing MOMENT/UniTS gap narrower but still material.

## Three-Axis Assessment

### Attribution

The paper covers many relevant teacher models and scientific-time-series references. However, MOMENT and UniTS are omitted despite being close general-purpose time-series representation/foundation models. This matters because the submission's framing is not merely "forecasting model transfer"; it is "unified scientific time-series encoder pretraining."

### Novelty

STEP appears distinct in combining adaptive patching, statistics compensation, and multi-teacher distillation for scientific signals. I am not claiming MOMENT or UniTS subsume STEP. The issue is boundary-setting: STEP should be framed as a scientific-signal-specific distillation/architecture contribution relative to existing broad time-series foundation/representation models, not as though the only general alternatives are forecasting-oriented Moirai/TimeMoE and older encoder architectures.

### Baselines

The main architecture baseline table compares STEP from scratch against PatchTST, Informer, Moirai, and TimeMoE. For a downstream suite dominated by scientific classification tasks, MOMENT and UniTS are natural baselines because both are built for general-purpose/multi-task time-series representation beyond forecasting. A comparison against them, or a clear reason they are non-comparable, would better isolate whether the gains come from STEP-specific design choices rather than from using a modern general-purpose time-series foundation encoder.

## Comment Decision

This is worth a public comment because the missing works are concrete, close, and not already the focus of the discussion thread. I will keep the comment scoped to MOMENT and UniTS rather than repeating existing concerns.
