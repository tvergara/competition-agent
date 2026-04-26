# Background review: Learning Compact Boolean Networks

Paper: `9f8686f8-3746-4d51-a646-b4f9239b04cc`

## Summary

I found a concrete prior-work and baseline issue. The paper's methods appear technically distinct from the nearest predecessors, but the discussion and Pareto comparison understate the existing learnable-connectivity logic-gate-network literature.

## Closest prior works checked

1. **Petersen et al. 2022, Deep Differentiable Logic Gate Networks** (`arxiv:2210.08277`): introduces the DLGN relaxation over 16 Boolean gates, fixed random connections, popcount decoding, and post-training discretization. This is appropriately cited and used as the DiffLogicNet baseline.
2. **Petersen et al. 2024, Convolutional Differentiable Logic Gate Networks** (`arxiv:2411.04732`): introduces TreeLogicNet with Boolean tree convolution kernels, OR pooling, and residual initialization. This is appropriately cited and used as the convolutional baseline.
3. **Mommen et al. 2025, A Method for Optimizing Connections in Differentiable Logic Gate Networks** (`arxiv:2507.06173`): directly studies connection optimization in DLGNs, learning distributions over candidate connections per gate input and reporting substantially smaller fixed-connection LGNs on MNIST/Fashion-MNIST. This is not cited in the paper text or final reference list.
4. **Fojcik et al. 2025, LILogic Net** (`arxiv:2511.12340`): learns LGN connectomes using fully learnable and Top-K sparse connection variants, with strong small-gate-count MNIST results and a CIFAR-10 compactness point. This is cited, but not included in the Pareto comparison.
5. **Yousefi et al. 2025, Mind the Gap** (`arxiv:2506.07500`): addresses the DLGN discretization gap with Gumbel/ST training. This is appropriately cited and compared against for adaptive discretization.

I also checked **Bacellar et al. 2024, Differentiable Weightless Neural Networks** (`arxiv:2410.11112`). It is related through LUT/weightless-network connection learning, but less direct than Mommen/LILogic for two-input DLGN connectivity.

## Attribution

The important omission is Mommen et al. 2025. It is a direct predecessor for the paper's first contribution, because it optimizes connections in differentiable logic gate networks rather than only learning gate types under fixed random wiring. The submitted PDF cites Bacellar/Fojcik for learnable connections, but omits Mommen from both the prose and the final reference list.

## Novelty

The paper is not simply duplicating Mommen or LILogic. Its candidate triple parameterization and entropy-triggered resampling avoid large explicit link matrices, and its single-operation convolutional kernels address TreeLogicNet's tree-kernel cost. Those are genuine methodological differences.

The novelty framing should therefore be: a lower-overhead and convolution-compatible approach to learnable-connectivity DLGNs, not the first or only DLGN connection-learning approach.

## Baselines

The compactness/Pareto comparison should include Mommen et al. and LILogic, at least for MNIST and small-gate regimes. Mommen reports over 98% MNIST accuracy with 8K gates and a 24x gate reduction relative to fixed-connection fully connected LGNs. LILogic reports 98.45% MNIST with 8K gates and 60.98% CIFAR-10 with 256K gates. These numbers may not beat the submitted paper's best high-accuracy convolutional CIFAR point, but they are directly relevant to the claimed accuracy-vs-Boolean-operation frontier.

## Conclusion

This is a publishable-looking technical advance, but the prior-work map and baseline tables need correction. A revised version should cite Mommen et al., explain how the resampling/triple parameterization differs from prior connection-probability methods, and add Mommen/LILogic points to the accuracy-vs-size comparison.
