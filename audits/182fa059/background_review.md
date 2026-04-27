# Background and Novelty Review: Hyperparameter Transfer Laws for Non-Recurrent Multi-Path Neural Networks

This review evaluates the manuscript "Hyperparameter Transfer Laws for Non-Recurrent Multi-Path Neural Networks" with a focus on its theoretical unification of depth scaling across modern architectures and its relationship to established scaling laws.

## 1. Attribution and Scholarly Context
The manuscript provides a robust contextualization of its contributions within the evolving landscape of maximal update parameterization (μP) and depth-wise scaling.

- **Foundational Scaling Laws:** The paper correctly identifies the ^{-3/2}$ power law previously established for sequential ReLU MLPs by **Jelassi et al. (2023)**. It also acknowledges the recent empirical work on depth transfer in ResNets and ViTs by **Bordelon & Pehlevan (2025)**.
- **Multi-Path Interpretation:** The choice of "effective depth" as the minimal path length is grounded in the "unraveled view" of residual networks proposed by **Veit et al. (2016)**, which suggests that shorter paths dominate the gradient flow at initialization. This work successfully formalizes that architectural insight into a predictive hyperparameter-transfer law.

## 2. Novelty and Theoretical Contribution
The primary novelty of this work lies in the **unification** and **formalization** of depth-scaling laws for non-recurrent architectures.

- **Effective Depth Framework:** By defining a graph-based "effective depth unit," the authors provide a consistent metric that applies across heterogeneous architectures (CNNs, ResNets, Transformers). This is a significant improvement over treating depth as a simple layer count, which often breaks down in residual or multi-branch models.
- **AM-μP (Arithmetic-Mean μP):** The introduction of a network-wide update-energy budget is a principled extension of the classical per-layer μP constraint. This allows for update reallocation across heterogeneous paths while maintaining width-robustness and predictable depth scaling.
- **Proof of Universality:** The manuscript provides the first unified proof that the -3/2 law holds for a broad class of multi-path graphs, bridging the gap between sequential-MLP theory and modern parallel-structured architectures.

## 3. Empirical Baselines and Rigor
The experimental section is thorough, spanning multiple datasets (CIFAR-10/100, ImageNet) and architectures.

- **Superiority over PathSum:** The comparison against **PathSum (Chen et al. 2024)** is particularly informative. The results demonstrate that while PathSum provides architecture-aware scaling, it deviates from the empirical optima as depth increases, whereas the proposed AM-μP law remains consistent. This validates the importance of the -3/2 exponent and the effective depth metric.
- **Zero-Shot Transfer:** The demonstration of reliable zero-shot transfer across both depth and width validates the practical utility of the framework for large-scale model training.

## Conclusion
The manuscript presents a strong theoretical and empirical case for a universal depth-scaling law. By synthesizing insights from path-based ResNet analysis and maximal-update theory, it provides a unified and practical framework for hyperparameter transfer in modern non-recurrent architectures.
