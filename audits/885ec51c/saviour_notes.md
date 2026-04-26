# Saviour notes for 885ec51c

CAFE proposes a geometry-ordered autoregressive rollout for reconstructing high-density biosignal channel montages from sparse low-density observations.

Observation 1: The evaluation is broader than the headline "six datasets" suggests: the dataset appendix states that for each dataset and SR factor, results are averaged over four predefined low-density channel layouts, and the main table spans SEED, Localize-MI, AJILE12, sEMG1, sEMG2, and CPSC2018.

Observation 2: The autoregressive benefit is not uniform across modalities. In Table 1, CPSC2018 ECG shows only small or zero NMSE improvements from adding AR to the Conv, MLP, and Transformer backbones: 0.41 to 0.41, 0.49 to 0.47, and 0.48 to 0.47, respectively. The paper attributes this to ECG leads being voltage differences with weaker and less consistent spatial coupling.

Observation 3: The rollout-depth ablation supports a limited form of sequential generation rather than simply making the rollout finer. The paper reports that the default three-step schedule with split boundaries 1/6 and 1/2 is best on ECoG and Localize-MI, while deeper rollouts can degrade because accumulated prediction errors offset the extra conditioning.
