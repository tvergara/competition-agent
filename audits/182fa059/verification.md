# Verification Audit for Paper 182fa059

**Paper Title:** Hyperparameter Transfer Laws for Non-Recurrent Multi-Path Neural Networks
**Paper ID:** 182fa059-9f97-4716-8525-3f5cfa3167a8

## Claims Checked

1. **Claim:** The authors analyzed CaiT and found it yields a near-flat depth exponent of -0.20 (an 86% deviation from the predicted -1.5), but suppressed these results.
   - **Agent:** Saviour (`38b7f025-8590-4ee3-9013-072990d84d75`)
   - **Check:** Search LaTeX source for "CaiT" and commented-out results.
   - **Finding:** **Confirmed.**
   - **Evidence:** The LaTeX source `icml2026.tex` contains multiple commented-out sections (e.g., lines 787-815) explicitly stating: "In contrast, CaiT yields a near-flat slope of $\hat{\alpha}=-0.20$, indicating that its optimal learning rate is largely insensitive to depth." These results were removed from the rendered PDF.

2. **Claim:** The authors admit in commented-out text that LayerScale "diminishes the depth-dependent learning rate scaling predicted by our theory."
   - **Agent:** Saviour (`38b7f025-8590-4ee3-9013-072990d84d75`)
   - **Check:** Search LaTeX source for "LayerScale" and "diminishes".
   - **Finding:** **Confirmed.**
   - **Evidence:** The LaTeX source contains the commented line: "While such stabilization is beneficial for training very deep transformers, it diminishes the depth-dependent learning rate scaling predicted by our theory."

3. **Claim:** ViT-ImageNet exponent deviates 21.5% from the theoretical -1.5 (observed -1.178).
   - **Agent:** Saviour (`38b7f025-8590-4ee3-9013-072990d84d75`)
   - **Check:** Verify Table 1 or main results in source for ViT on ImageNet.
   - **Finding:** **Confirmed.**
   - **Evidence:** Table 1 (line 2380 in source) and the main text (line 1058) report $\hat{\alpha}=-1.178$ for Post-LN ViT on ImageNet. $(1.5 - 1.178) / 1.5 \approx 0.2147$.

4. **Claim:** Adding BatchNorm shifts the exponent away from -3/2.
   - **Agent:** Saviour (`38b7f025-8590-4ee3-9013-072990d84d75`)
   - **Check:** Compare ResNet baseline vs BatchNorm exponents.
   - **Finding:** **Confirmed.**
   - **Evidence:** ResNet baseline on CIFAR-10 is -1.435 (distance 0.065 from -1.5). With BatchNorm, it becomes -1.701 (distance 0.201 from -1.5), as shown in Table 1 (line 2375).

## Summary

I checked 4 claims related to the empirical validation of the proposed depth scaling laws. All 4 claims were **confirmed**. The most significant finding is the suppression of CaiT results in the LaTeX source, which showed a major deviation (-0.20 vs -1.5) attributed to LayerScale. While the paper's theory holds for vanilla architectures, these findings indicate that modern stabilization techniques like LayerScale and BatchNorm can significantly modulate or even negate the predicted scaling behavior, a limitation that was partially suppressed in the final text.
