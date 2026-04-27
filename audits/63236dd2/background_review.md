# Background and Novelty Review: CAETC for Counterfactual Estimation over Time

## 1. Attribution and Prior Work
The paper provides a clear and accurate mapping of the field, tracing the development of temporal counterfactual estimation from **CRN (Bica et al., 2020)** and **CT (Melnychuk et al., 2022)** to the more recent **CCPC (Bouchattaoui et al., 2024)**. 

The authors correctly identify **CCPC** as the closest neighbor that addresses representation invertibility. However, the manuscript characterizing CCPC's InfoMax principle as an \"implicit\" version of CAETC's \"explicit\" autoencoding. Given this close relationship, the absence of CCPC as an experimental baseline is a significant omission that hinders the verification of the paper's primary claims.

## 2. Novelty and Technical Contribution
The primary architectural novelty is the integration of **FiLM (Feature-wise Linear Modulation)** for treatment conditioning. While FiLM is an established technique in computer vision, its application as a more expressive alternative to treatment-representation concatenation in causal inference is a meaningful and well-motivated design choice.

The **explicit partial autoencoding** framework provides a principled way to enforce representation richness and invertibility, which is a known challenge in adversarial representation balancing.

## 3. Omitted Baselines (Critical Concern)
The manuscript fails to compare against the most recent and relevant baselines cited in its own related work:
- **CCPC (Bouchattaoui et al., 2024)**: As the closest work addressing invertibility via InfoMax, CCPC is a mandatory baseline for substantiating the benefits of the proposed explicit autoencoding approach.
- **Mamba-CDSP (Wang et al., 2024)**: Cited as a recent architecture-specific method that decorrelates history with planned treatment, it should be included to establishing the relative performance of CAETC.

## 4. Theory-Method Alignment
Theorem 2 provides a valuable error bound based on the generalized Jensen-Shannon divergence (JSD). However, the theorem explicitly assumes that the representation function $\Phi$ is **invertible**. In practice, the paper utilizes a **bottleneck autoencoder** where the representation dimension is smaller than the history dimension ($\text{dim}(\Phi(H)) < \text{dim}(H)$), which fundamentally violates the invertibility assumption. This gap between the theoretical prerequisite (diffeomorphism) and the practical implementation (bottleneck) should be clearly disclosed as a limitation, as the provided bound does not directly cover the primary architectural instantiation.

