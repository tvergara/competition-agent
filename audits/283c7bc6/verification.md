# Verification Report: NEXUS: Bit-Exact ANN-to-SNN Equivalence via Neuromorphic Gate Circuits with Surrogate-Free Training

I identified and investigated three verifiable claims regarding the paper "NEXUS" (ID: 283c7bc6-c3d4-43d7-86a5-48e1f99ab266).

## Claims Checked

1. **Energy Efficiency and Reduction Claim**
   - **Original Claim:** The abstract and Section 4.4 claim a 27--168,000x energy reduction on neuromorphic hardware (Loihi) compared to GPU.
   - **Verification Process:** Cross-referenced the reported energy values in Table 10 with the paper's own energy formula (Eq. 8: {\text{op}} = N_{\text{active\_spikes}} \times 23.6\,\text{pJ}$) and reported spike counts.
   - **Finding:** **✗ Refuted**. Table 10 is internally inconsistent with Eq. 8 by exactly 1000x. For a Transformer Block, the paper reports 30.7M active spikes and 724 nJ Loihi energy. However, 0.7 \times 10^6 \times 23.6 \times 10^{-12} \text{ J} = 724,520 \text{ nJ}$ (or 724 $\mu). When using the correct Loihi energy derived from the paper's formula, the SNN consumes $\sim 17\times$ MORE energy than the GPU (724 $\mu vs 42 $\mu), reversing the signs of the headline efficiency claim.
   - **Evidence:** Table 10 ("Transformer Block" row) and Equation 8 in Section 4.4.

2. **Bit-Exact IEEE-754 Equivalence**
   - **Original Claim:** NEXUS is the first to achieve bit-exact equivalence between ANNs and SNNs using gate-level implementation.
   - **Verification Process:** Reviewed the methodology and compared against cited and un-cited prior art.
   - **Finding:** **✓ Confirmed** (Technical Implementation). The use of IF neurons to build digital logic gates (AND, OR, XOR) is a mathematically sound way to replicate IEEE-754 arithmetic. However, the "first to be lossless" claim is weakened by prior works (e.g., Bu et al. 2023, You et al. 2024) that already report lossless or zero-error conversion using different mechanisms.
   - **Evidence:** Section 3.1 and 3.2 detailing the gate constructions.

3. **Immunity to LIF Membrane Leakage**
   - **Original Claim:** Spatial bit encoding is inherently immune to membrane potential leakage ($\beta < 1$) because it operates in a single timestep.
   - **Verification Process:** Audited the theoretical basis and results in Table 7 (Appendix).
   - **Finding:** **✓ Confirmed**. Since each bit is processed in parallel across spatial channels in one timestep, there is no temporal accumulation, making the mechanism robust to information decay over time.
   - **Evidence:** Appendix B Table 7 showing 100% accuracy for all $\beta \in [0.1, 1.0]$.

## Summary

I verified three material claims for the NEXUS paper. I confirmed that the energy reduction claim is based on a 1000x arithmetic error in Table 10; under the paper's own formula and data, the proposed SNN is significantly less energy-efficient than a GPU. The bit-exact equivalence and LIF leakage immunity were confirmed as technically sound properties of the spatial bit encoding, although the novelty of lossless conversion is shared with prior literature. These findings indicate a critical failure in the paper's headline empirical result regarding hardware efficiency.
