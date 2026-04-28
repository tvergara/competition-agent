# Background and Novelty Review

## Paper Summary
The paper "Stop Preaching and Start Practising Data Frugality for Responsible Development of AI" argues for the adoption of data frugality (subset selection) to reduce the environmental impact of machine learning. It provides an aggregate estimation of the energy use and carbon emissions associated with the downstream use of ImageNet-1K, estimating approximately 5.46 GWh of energy and 2429 tCO2e of emissions for model training between 2017 and 2025. The paper also demonstrates that state-of-the-art (SOTA) coreset selection methods (Dyn-Unc, InfoMax) can prune 25-35% of ImageNet-1K without performance loss, yielding significant energy savings. Finally, it uses a toy Colored MNIST example to show that coreset selection can mitigate dataset bias and provides a "Call to Action" for stakeholders.

## Comparison with Prior Works
1. **Paul et al. (2025): "Core Tokensets for Data-efficient Sequential Training of Transformers"**
   - *Relationship:* Provides a recent example of applying coreset/tokenset selection to modern architectures (Transformers).
   - *Citation:* Correctly cited.
2. **Dharmasiri et al. (2025): "The Impact of Coreset Selection on Spurious Correlations and Group Robustness"**
   - *Relationship:* A comprehensive study on how coreset selection affects bias and robustness in real-world datasets.
   - *Citation:* Cited in Section 5 (Alternative Views) regarding the risk of removing rare samples, but its findings on bias mitigation are not integrated into the main bias discussion (Section 4.3).
3. **Jin Cui et al. (2025): "FAST: Topology-Aware Frequency-Domain Distribution Matching for Coreset Selection"**
   - *Relationship:* A very recent (Nov 2025) coreset paper that explicitly targets power consumption and energy efficiency, reporting a 96.57% reduction in power consumption and 2.2x speedup.
   - *Citation:* **Missing.** This paper directly challenges the claim that coreset methods rarely evaluate energy savings.
4. **Nagaraj et al. (2025): "Coresets from Trajectories: Selecting Data via Correlation of Loss Differences"**
   - *Relationship:* Proposes the CLD metric for efficient coreset selection and explicitly mentions inherent bias reduction via per-class validation alignment.
   - *Citation:* **Missing.** Highly relevant to both the efficiency and bias mitigation arguments.
5. **Yang et al. (2023): "Chasing Low-Carbon Electricity for Practical and Sustainable DNN Training"**
   - *Relationship:* Specifically measures the carbon footprint of training ResNet-50 on ImageNet (achieving a 13.6% reduction).
   - *Citation:* **Missing.** Provides an important empirical anchor for the ImageNet-specific carbon footprints discussed in Section 3.1.

## Three-Axis Assessment

### 1. Attribution
The paper identifies an important reporting gap in the coreset literature ("preaching vs. practising") but misses several recent works that have already begun to bridge this gap. Specifically, the omission of **FAST (Jin Cui et al., 2025)** is significant because that work centers energy efficiency as its primary metric, contradicting the claim that "only one evaluates energy savings" in a representative sample. Furthermore, **CLD (Nagaraj et al., 2025)** and **Chase (Yang et al., 2023)** are relevant neighbors for coreset-driven bias mitigation and ImageNet-specific carbon footprinting, respectively, which would have strengthened the paper's grounding.

### 2. Novelty
The paper's primary novelty lies in its **community-wide aggregate estimation** of the environmental cost of a canonical dataset (ImageNet-1K) and its **rhetorical positioning** of data frugality as a core tenet of responsible AI. The technical demonstrations (Section 4) are largely illustrative of existing SOTA methods (Dyn-Unc, InfoMax) or standard techniques (balanced sampling). While the "preach vs. practice" framing is compelling, the paper's claim that such practices are almost non-existent is slightly undermined by the very recent literature (FAST, CLD) that it omits.

### 3. Baselines
The paper correctly identifies and uses SOTA coreset methods (Dyn-Unc, InfoMax) as references for ImageNet pruning. However, the **bias mitigation baseline** (Section 4.3) is limited to a toy dataset (Colored MNIST) and a simple balanced sampling technique. The discussion would have benefited from engaging with the more rigorous analysis of coreset bias and group robustness found in **Dharmasiri et al. (2025)** or the inherent bias reduction properties of **CLD (Nagaraj et al., 2025)**.

## Overall Verdict
**Neutral.** The paper provides a valuable and timely "Call to Action" backed by a novel aggregate impact estimation for ImageNet. However, its characterization of the current state of coreset reporting ("only one evaluates energy") is arguably too narrow and fails to account for very recent SOTA works (e.g., FAST) that explicitly prioritize energy and power metrics. The technical contribution on bias is also relatively thin compared to the cited and omitted neighbors.
