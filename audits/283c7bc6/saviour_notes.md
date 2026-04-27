# Factual Observations for NEXUS: Bit-Exact ANN-to-SNN Equivalence

- **Bit-Exact Equivalence**: NEXUS is designed to achieve mathematically identical outputs between ANNs and SNNs by constructing arithmetic operations from pure IF neuron logic gates that implement IEEE-754 compliant floating-point arithmetic.
- **Leakage Immunity**: The framework's single-timestep spatial bit encoding makes it inherently immune to membrane potential leakage, maintaining 100% accuracy across all decay factors $β \in [0.1, 1.0]$.
- **Hardware Efficiency**: Empirical results show a 27--168,000x energy reduction on neuromorphic hardware compared to standard ANNs, while maintaining machine-precision accuracy.
