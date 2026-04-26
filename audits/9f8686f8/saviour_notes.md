# Saviour notes for 9f8686f8

This paper proposes compact Boolean networks using learned connection triples, a single-operation convolutional Boolean architecture, and adaptive discretization.

Observation 1: Beyond the single-run main tables, the appendix reports random-seed statistics for both connection learning and convolution experiments on MNIST and CIFAR-10. The reported means keep the same ordering as the headline results, which strengthens the empirical claim.

Observation 2: The TreeLogicNet comparison is necessarily approximate. The paper states that the official TreeLogicNet implementation was unavailable, so it uses a community ConvLogic implementation and validates it in Appendix Table 6; this is a reasonable effort, but the main Pareto claim still depends on a proxy baseline.

Observation 3: The efficiency metric is circuit-size focused. The experiments report accuracy, neuron count, and pruned Boolean operation count on MNIST/CIFAR-10, but do not measure hardware latency, energy, memory bandwidth, or post-synthesis area, even though the motivation is resource-constrained inference.
