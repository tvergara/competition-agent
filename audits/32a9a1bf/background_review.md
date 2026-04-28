# Background and Novelty Review: Stochastic Gradient Variational Inference with Price's Gradient Estimator from Bures-Wasserstein to Parameter Space

## Summary of Contributions
The paper investigates the relationship between Wasserstein Variational Inference (WVI) and Black-Box Variational Inference (BBVI). Its main claims are:
1. It closes the gap in iteration complexity between WVI and BBVI by showing that both can achieve identical state-of-the-art guarantees ($O(d \kappa \epsilon^{-1})$) when using a Hessian-based gradient estimator, which the authors call "Price's gradient."
2. It provides a refined convergence analysis for WVI, improving upon the results of Diao et al. (2023) by a factor of $\kappa$ and removing a logarithmic factor.
3. It demonstrates that the observed superiority of WVI in previous work was largely due to the use of second-order information (Price's gradient) rather than the Bures-Wasserstein geometry itself.
4. It shows that WVI can also be implemented using the first-order reparametrization gradient, making it more widely applicable, though less efficient than the Hessian-based version.

## Prior Works and Relationship
1. **Diao et al. (2023): "Forward-Backward Gaussian Variational Inference via JKO in the Bures-Wasserstein Space"**
   - *Relationship:* The primary theoretical baseline for WVI. The current paper improves their complexity results and uses their estimator as a starting point.
   - *Citation:* Correctly cited and used as a benchmark.
2. **Kim et al. (2023) / Domke et al. (2023): "On the Convergence of Black-Box Variational Inference" / "Provable Convergence Guarantees for Black-Box Variational Inference"**
   - *Relationship:* The primary theoretical baselines for BBVI with reparametrization gradients. The current paper uses their results to show the "gap" that it eventually closes.
   - *Citation:* Correctly cited.
3. **Yi & Liu (2023): "Bridging the Gap between Variational Inference and Wasserstein Gradient Flows"**
   - *Relationship:* A conceptual predecessor that suggested the recast of Bures-Wasserstein gradient flows as Euclidean flows.
   - *Citation:* Cited as providing the conceptual intuition, while the current paper claims to provide the first non-asymptotic discrete-time analysis.
4. **Fan et al. (2015): "Fast Second Order Stochastic Backpropagation for Variational Inference"**
   - *Relationship:* A key methodological predecessor that proposed using second-order information (Hessians) via Gaussian backpropagation (equivalent to Price's theorem) to improve BBVI convergence.
   - *Citation:* **Omitted in the main text.** While present in the bibliography, it is not cited in the discussion of second-order BBVI, which is a significant attribution oversight given its direct relevance to the paper's core mechanism.
5. **Lambert et al. (2022): "Variational Inference via Wasserstein Gradient Flows"**
   - *Relationship:* Foundation of modern parametric WVI.
   - *Citation:* Correctly cited.

## Three-Axis Assessment

### 1. Attribution
The paper is generally well-grounded in recent WVI literature (Diao, Chewi, Lambert). However, it has a significant attribution gap regarding the use of second-order information in BBVI. Specifically, **Fan et al. (2015)** is not cited in the main text despite proposing the exact second-order methodology that the authors "identify" as the source of BBVI's potential improvement. Furthermore, while the authors cite Price (1958) and Stein (1981), they downplay the long history of "Variational Gaussian Approximation" (VGA) methods (e.g., Opper & Archambeau, 2009; Salimans & Knowles, 2013) that have utilized these identities for decades.

### 2. Novelty
The novelty is **High** on the theoretical axis. Refining the iteration complexity for WVI to remove the $\log \epsilon^{-1}$ factor and some $\kappa$ dependencies is a valuable technical contribution. More importantly, the proof that BBVI achieves the *exact same* rate as WVI when equipped with the same estimator is a strong result that clarifies the relative importance of geometry vs. estimator quality in VI. The empirical demonstration that WVI can use reparametrization gradients (and performs similarly poorly to BBVI in that case) effectively isolates the "Hessian advantage."

### 3. Baselines
The experimental design is excellent, covering the full 2x2 matrix of (WVI vs. BBVI) and (Reparametrization vs. Price/Hessian). This directly addresses the paper's core hypothesis. The inclusion of NGVI as a reference point in the discussion and some experiments adds further context, although the theoretical comparison to NGVI is correctly identified as an open challenge.

## Overall Verdict: Very Novel
The paper provides a significant theoretical unification of two seemingly different approaches to variational inference. By showing that the "Wasserstein advantage" is primarily an "estimator advantage," it shifts the focus of the field toward the choice of gradient estimators. The refinement of WVI rates is a solid technical achievement. Despite the missing attribution to Fan et al. (2015) in the main text, the theoretical contribution is sufficiently distinct and rigorous to warrant a positive assessment.
