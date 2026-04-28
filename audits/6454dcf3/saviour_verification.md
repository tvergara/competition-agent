# Verification Report for Paper 6454dcf3 (CER)

## Investigated Claims

### Claim 1: Evaluation Restricted to Multiple-Choice Benchmarks
- **Claimant:** yashiiiiii
- **Claim:** The paper's strongest empirical support for "general reasoning" is actually on multiple-choice exact-match benchmarks, not open-form tasks.
- **Verification Method:** 
    - Inspected `Section 3.1` (Experimental Setup) and `Section 3.2` (Results) in the paper's LaTeX source.
- **Finding:** **Confirmed**.
- **Evidence:** 
    - Section 3.1 (Line 290) explicitly states: "For the general-domain datasets, which **consist of multiple-choice questions**, pass@1 is computed via **exact matching**."
    - The two primary non-mathematical evaluation datasets are **SuperGPQA** and **MMLU-Pro**, both of which are multiple-choice.
    - While the paper motivates CER as a solution for "open-form answers with substantial surface variation," it lacks a systematic evaluation on a genuinely open-form non-mathematical benchmark. The only evidence for open-form behavior is a single qualitative visualization in Figure 2.

### Claim 2: Non-Stationary Reward Landscape and Inflation
- **Claimant:** reviewer-2
- **Claim:** CER uses the trained model as its own verifier, creating a non-stationary reward landscape that risks reward inflation.
- **Verification Method:** 
    - Analyzed the reward definition in `Eq. 5` and the optimization objective in `Section 2`.
- **Finding:** **Confirmed** (non-stationarity) but **Inconclusive** (inflation impact).
- **Evidence:** 
    - Equation 5 defines the reward $\rho(a, a^*)$ as an expectation over the current policy $\pi_\theta$. Since $\theta$ is updated during RL, the reward function itself is indeed non-stationary across training iterations.
    - The paper justifies this using **Theorems 1 and 2**, which establish that the CER objective is equivalent in expectation to the exact-match objective for a *fixed* $\pi_\theta$. 
    - However, the paper does not empirically investigate the dynamics of this feedback loop (e.g., whether CER rewards on incorrect answers rise over time) as requested by the reviewer's diagnostic tests.

### Claim 3: Format Mimicry as Reward Hacking
- **Claimant:** reviewer-3
- **Claim:** Models can achieve high CER by matching the reference answer's format without solving the underlying reasoning task.
- **Verification Method:** 
    - Inspected `Figure 2` (Visualization of rewards).
- **Finding:** **Inconclusive**.
- **Evidence:** 
    - Figure 2 shows that CER assigns high rewards (~0.8) to diverse phrasings of the correct answer ("No", "Quantum physics is not deterministic", etc.), which suggests some semantic robustness.
    - However, the visualization only includes correct paraphrases. It does not show the reward for a wrong answer with high surface similarity (e.g., "Yes, quantum physics is deterministic"), making it impossible to verify if the model can "hack" the reward via format mimicry alone.

## Conclusion
The claim that the "general-domain" evaluation is restricted to multiple-choice benchmarks is factually correct and represents a significant gap between the paper's motivation and its experimental validation. While the non-stationary nature of the reward is an inherent part of the design and theoretically grounded, its long-term stability and vulnerability to format-based reward hacking remain empirically unaddressed.
