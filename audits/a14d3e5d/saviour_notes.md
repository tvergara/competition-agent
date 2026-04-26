# Saviour Notes: a14d3e5d

This paper uses a FlyWire-derived whole-brain fruit-fly connectome as the fixed graph topology of a message-passing policy for flybody locomotion tasks.

Observation 1: The appendix explicitly says walking and flight share the same graph topology but not the same controller interface or hyperparameters: walking uses 1,253-dimensional observations, 59-dimensional actions, visual augmentation, learning rate 1e-4, and a 512-512-512-512 expert, while flight uses 104-dimensional observations, 12-dimensional actions, learning rate 1e-5, and a 256-256-256 expert.

Observation 2: The imitation dataset is constructed from rollouts of pretrained domain-specific MLP controllers and filters for successful episodes longer than 100 steps. This helps explain the IL curves as fitting curated successful expert behavior, not learning from the full distribution of failed or short rollouts.

Observation 3: The neural-representation figure is useful but exploratory: activity is compressed to a scalar by PCA over channels, clipped to the 5th-95th percentile range, min-max normalized, stratified/downsampled because class sizes are highly imbalanced, and reordered by a spectral method with alpha set to 0.7.
