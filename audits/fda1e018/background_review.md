# Background and Novelty Assessment: StableQAT

## Claimed Contributions
The paper proposes **StableQAT**, a framework designed to stabilize Quantization-Aware Training (QAT) at ultra-low bitwidths (2-4 bits). Its central contribution is the **Rotated Damped Fourier Surrogate (RDFS)**, a smooth, analytically grounded surrogate for backpropagation derived from a discrete Fourier analysis of the rounding operator. By rotating the coordinate system, the paper transforms the non-periodic rounding staircase into a periodic triangle wave, which is then approximated via Fourier series. This approach aims to provide bounded and stable gradients, resolving the forward-backward mismatch inherent in standard Straight-Through Estimator (STE) based QAT.

## Comparison with 5 Most Similar Prior Works

1.  **STE: Straight-Through Estimator (Bengio et al., 2013)**:
    - *Relationship*: The foundational surrogate for discrete operators. StableQAT identifies STE as a special case of its RDFS (where amplitude $A=0$) and claims to generalize it with richer structural information.
    - *Citation*: Correctly cited as the primary baseline.
2.  **LSQ: Learned Step-size Quantization (Esser et al., 2019)**:
    - *Relationship*: A landmark QAT method that introduced learnable quantization parameters. StableQAT builds on this lineage by focusing on the gradient surrogate itself to improve stability.
    - *Citation*: Correctly cited.
3.  **DSQ: Differentiable Soft Quantization (Gong et al., 2019)**:
    - *Relationship*: A canonical soft-rounding approach that uses sigmoids to bridge full-precision and low-bit values. StableQAT uses DSQ as a primary baseline and theoretically proves that DSQ's gradient variance diverges as it sharpens, whereas RDFS remains bounded.
    - *Citation*: Correctly cited and used as a key baseline.
4.  **Smooth Approximations of the Rounding Function (Semenov, 2025)**:
    - *Relationship*: Recent work focusing on sigmoid-based smooth approximations. StableQAT's Fourier-based approach provides a more mathematically principled, periodic surrogate that avoids the saturation issues of sigmoids.
    - *Citation*: Correctly cited.
5.  **Gaussian Weight Sampling for Stable PQT (Ahn & Yoo, 2025)**:
    - *Relationship*: Contemporary work focusing on stabilization through noise injection. StableQAT addresses stability through a deterministic, analytically derived surrogate gradient, offering an alternative paradigm.
    - *Citation*: Correctly cited (as "Differentiable, Stable and Efficient Floating-Point Quantization").

## Three-Axis Assessment

- **Attribution**: **Excellent.** The paper meticulously maps the landscape of QAT, from the original STE to the most recent SOTA methods like ParetoQ (2025). It correctly identifies and differentiates its contribution from both deterministic surrogates and stochastic relaxations.
- **Novelty**: **Clearly very novel.** The derivation of a gradient surrogate via a 45-degree coordinate rotation and Fourier series expansion is a highly original geometric and spectral insight. It elegantly reconciles the non-periodic nature of rounding with the periodic strengths of Fourier analysis. The theoretical proof of bounded gradient variance compared to DSQ provides a strong justification for the method's stability.
- **Baselines**: **Strong.** The comparison against ParetoQ (SOTA STE-based) and DSQ (canonical soft-surrogate) is rigorous. Evaluating on LLaMA-3.2 models (1B and 3B) at 2-4 bits using standard benchmarks (ARC, Hellaswag, etc.) demonstrates significant empirical gains (up to 6.88% at 3 bits).

## Overall Verdict
**Clearly very novel.** StableQAT introduces a theoretically elegant and practically effective surrogate for QAT that generalizes the standard STE. Its unique information-theoretic grounding in Fourier analysis addresses long-standing stability issues in low-bit quantization in a principled way. The method is "fusion-friendly" and matches the efficiency of STE while delivering superior performance.

**Primary Supporting Works**: Bengio et al. (2013), Gong et al. (2019), and Semenov (2025).
