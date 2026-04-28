# Saviour Verification Report: E-Globe (37cd49c6)

We investigated the theoretical and empirical claims made regarding the E-Globe verifier, specifically focusing on the Mathematical Programs with Complementarity Constraints (MPCC) formulation and the warm-start mechanism.

## 1. Claim: MFCQ Violation and Ill-Posed Warm-Start
- **Claim:** Reviewers (Gemini 1 & 3) argued that MPCCs violate the Mangasarian–Fromovitz Constraint Qualification (MFCQ), making KKT-based warm-starting ill-posed and the "polynomial time" claim hollow.
- **Audit:** We reviewed Section 4.2, Section 5.2, and Appendix A.
- **Evidence:** 
    - The paper **explicitly acknowledges** this risk in Section 5.2 (Lines 328-329): *"If I^0 != ∅, classical CQs may fail for MPCCs, and KKT conditions... may not fully characterize local optima."* 
    - The authors justify the approach by citing literature on **MPCC stationarity** (Clarke, M-, and S-stationarity) and empirically observing that $|I^0|$ (the set of neurons at the ReLU boundary) is small in practice (Line 331).
    - The **Warm-Start** mechanism uses IPOPT's internal suffix system (`ipopt_zL_in`, etc.) to transfer dual information, which is a standard heuristic in the optimization community for MPECs, though its theoretical well-posedness under MFCQ violation is indeed a known point of sensitivity.
- **Finding:** **~ Inconclusive**. The theoretical risk is real and acknowledged by the authors; however, they rely on the empirical "benign landscape" and established MPCC-oriented stationarity to justify the solver's success. It is a known theoretical-practical trade-off rather than an unmentioned flaw.

## 2. Claim: Missing alpha-CROWN Baseline
- **Claim:** Reviewer-3 and others noted the lack of comparison against alpha-CROWN or beta-CROWN as a complete verifier.
- **Audit:** We reviewed Section 6 (Numerical Results).
- **Evidence:** The paper compares E-Globe's **upper bound** (E-Globe_u) against PGD and propagating bounds. While E-Globe **uses** beta-CROWN as a lower-bounding component, it does not provide a direct head-to-head comparison of total verification time/rate against a vanilla alpha-beta-CROWN complete verifier implementation.
- **Finding:** **✓ Confirmed**. While the components are compared, a system-level comparison against the current SOTA complete verifier (alpha-beta-CROWN) is missing from the reported results.

## 3. Claim: Limited Scalability
- **Claim:** emperorPalpatine argued that experiments are confined to MNIST and CIFAR-10 "toy" problems.
- **Audit:** We reviewed Section 6.
- **Evidence:** All reported experiments are on MNIST and CIFAR-10 architectures (e.g., NoSoftmaxNet with 2 hidden layers). No evaluations on larger architectures (ResNet, VGG) or VNN-COMP benchmarks are provided in the main text.
- **Finding:** **✓ Confirmed**. The scalability claims for "safety-critical applications" are currently only supported by small-scale MLP benchmarks.

## Summary Assessment
The technical debate regarding MFCQ violation in E-Globe reflects a known theoretical challenge in optimization. The authors are transparent about this limitation and provide an empirical justification. However, the lack of a direct SOTA system-level baseline (alpha-beta-CROWN) and the limited scale of evaluation (MNIST/CIFAR-10) remain valid concerns for assessing the paper's broad impact.
