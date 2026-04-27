# Background and Novelty Review: SDM (Formalizing the Sampling Design Space...)

## Summary of Contribution
The paper proposes SDM, a framework for optimizing diffusion sampling through two main components: (i) Curvature-based solver allocation, which switches between Euler (1st order) and Heun (2nd order) solvers based on a cache-based curvature proxy to save NFE; and (ii) Wasserstein-bounded adaptive scheduling, which derives optimal timesteps by bounding the local discretization error in Wasserstein distance.

## Three-Axis Assessment

### 1. Attribution
The paper provides good attribution for standard diffusion solvers (EDM, DPM-Solver++, UniPC) and properly acknowledges **AdaFlow** (Hu et al., 2024) as the source for the Wasserstein-bounded scheduling proofs. However, there is a significant missing citation:
- **FSampler: Training Free Acceleration of Diffusion Sampling via Epsilon Extrapolation** (Vladimir, 2025; arXiv:2511.09180). 

### 2. Novelty
Contribution (i), the use of a cache-based curvature proxy to adaptively select the approximation order, is highly similar to the mechanism introduced in **FSampler**. FSampler maintains a history (cache) of denoising signals to estimate local trajectory dynamics and adaptively selects the order of its predictors (up to 4th order). FSampler's "gradient estimation stabilizer" specifically addresses local curvature to correct drift, functionally overlapping with SDM's curvature-based switching. Presentation of this mechanism as a novel contribution without reference to FSampler overstates the work's original impact.

### 3. Baselines
The empirical evaluation compares SDM against EDM and COS (Williams et al., 2024). However:
- **FSampler** should have been included as a baseline, as it also provides a training-free, cache-efficient method for reducing NFE based on local trajectory geometry. Given that FSampler allows for 0-NFE steps through extrapolation, it represents a strong competitor for the efficiency gains claimed by SDM.

## Decision Rule
**Comment recommended.** The failure to cite and compare against **FSampler** (Vladimir 2025) is a significant oversight, as FSampler established the core idea of using cached signal history for curvature-aware adaptive sampling orders several months prior to this work.
