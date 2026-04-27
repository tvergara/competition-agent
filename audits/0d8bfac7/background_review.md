# Background and Novelty Assessment: CUP-FL (0d8bfac7)

## Summary of Findings
While the proposed **Cumulative Utility Parity (CUP)** principle is a well-motivated extension of fairness to intermittent participation settings, the manuscript suffers from significant baseline omissions in its empirical evaluation and a fundamental theoretical error in its selection-frequency proof.

## 1. Experimental Baseline Omissions
The empirical evaluation (Table 2) compares against q-FFL and PHP-FL but omits several foundational and highly relevant baselines that are cited in the Related Work:
- **FedAvg (McMahan et al., 2017)**: The standard baseline for any FL method. Without it, the absolute performance of the proposed method cannot be calibrated.
- **Ditto (Li et al., 2021)**: The primary baseline for personalization-based fairness in heterogeneous FL.
- **FairFedCS (2023)**: A direct competitor that also addresses fairness at the client selection stage using historical participation (reputation scores).
The absence of these benchmarks makes it difficult to determine if the reported gains are due to the CUP principle or simply to better model training.

## 2. Theoretical Flaw (Lemma 2)
Lemma 2 claims that inverse-availability sampling equalizes long-run selection frequency to /N$. However, the proof (Eq. 13-17) invalidly replaces the random denominator with its limit $ inside the expectation. This step assumes independence that does not hold for the stated sampling rule, as demonstrated by simple counterexamples (e.g., a 2-client case with heterogeneous $\pi_k$). Consequently, the asymptotic equality claim is not formally established.

## 3. Algorithm-Theory Mismatch
The theoretical analysis of selection fairness assumes a randomized sampling rule proportional to (t)$, whereas the implementation described in Section 3.2 and Algorithm 1 utilizes a deterministic **top-K** selection mechanism based on availability and missed-round counts. This mismatch further disconnects the theoretical guarantees from the actual behavior of the system.

## Conclusion
We recommend the authors include standard FL and personalized FL baselines (FedAvg, Ditto) and a direct participation-aware competitor (FairFedCS) in their experimental results. Additionally, the proof of Lemma 2 should be corrected to account for the stochasticity of the available set, or the algorithm should be aligned with the randomized sampling assumption.
