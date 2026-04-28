# Background and Novelty Review: f0da4b35

## Paper's Claimed Contribution
The paper "Stop Preaching and Start Practising Data Frugality for Responsible Development of AI" argues for a shift in the machine learning community towards "data frugality"—minimizing data usage to reduce environmental and social impacts. Its primary contributions are:
1. A conceptual distinction between "data frugality" and "model frugality."
2. An aggregate estimation of the downstream environmental cost (energy and carbon) of the ImageNet-1K dataset (estimated at 5.46 GWh for training from 2017-2025).
3. Empirical evidence that coreset-based data pruning can reduce training energy by approximately 30% with minimal accuracy loss.
4. Actionable recommendations for individuals, platforms, and policy-makers to institutionalize data frugality.

## Closest Prior Works
1. **Strubell et al. (2019) "Energy and Policy Considerations for Deep Learning in NLP"**: This foundational work quantified the carbon footprint of training large NLP models and neural architecture search (NAS), bringing environmental concerns to the forefront of the ML community.
2. **Patterson et al. (2021) "Carbon Emissions and Large Neural Network Training"**: This work updated previous emission estimates and highlighted that choice of hardware, datacenter efficiency (PUE), and geographic location (energy mix) can reduce emissions by 100-1000x.
3. **Lacoste et al. (2019) "Quantifying the Carbon Emissions of Machine Learning"**: This seminal paper introduced the Machine Learning Emissions Calculator, providing the methodology and data for many subsequent emission-tracking tools.
4. **Schwartz et al. (2020) "Green AI"**: This position paper advocated for efficiency as a primary evaluation criterion in AI research, coining the term "Green AI" to describe research that yields novel results without increasing computational cost.
5. **Mirzasoleiman et al. (2020) "Coresets for Data-efficient Training of Machine Learning Models" (CRAIG)**: This work introduced a rigorous method for selecting weighted subsets (coresets) that approximate the full dataset's gradient, achieving significant speedups in training deep neural networks.

## Three-Axis Assessment

### 1. Attribution
The paper provides a comprehensive overview of the literature on ML efficiency and environmental impact. However, it **fails to cite Lacoste et al. (2019)**, which is the seminal work that introduced the first widely used tool for quantifying ML emissions and established the methodology for the "Carbon tracker" and "CodeCarbon" tools the authors reference. This is a significant omission given the paper's focus on "practising" quantification.

### 2. Novelty
The paper's most significant novelty is the **shift from model-centric to dataset-centric environmental analysis**. While prior work (Strubell, Patterson, Luccioni) focuses on the footprint of training specific models (e.g., BERT, GPT-3, BLOOM), this paper estimates the aggregate downstream footprint of a *dataset* (ImageNet-1K) across its entire community of users. The estimate of 5.46 GWh for ImageNet training is a novel and valuable data point for understanding the cumulative impact of shared research infrastructure.

### 3. Baselines
In the empirical section (Section 4), the paper demonstrates energy savings using a "25% pruned subset sampled uniformly at random." While this shows the *potential* for savings, the paper **neglects the computational cost of coreset construction**. As noted in Mirzasoleiman et al. (2020), selecting informative coresets for deep networks can require periodic re-selection (e.g., every few epochs), which introduces an overhead that may offset some of the training energy gains. By only measuring random pruning in Table 1, the authors may be overstating the "data frugality" benefits achievable by accuracy-preserving methods without providing a full cost-benefit analysis that includes the construction phase.

## Overall Verdict: Very Novel
Despite the attribution and baseline issues, the paper's aggregate quantification of a major dataset's environmental impact represents a distinct and important new direction in the "Green AI" literature.
