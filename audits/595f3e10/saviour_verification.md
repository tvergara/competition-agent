# Saviour Verification: SSR (595f3e10)

## Investigated Claims

### 1. Technical Incongruity: Grassmannian Manifold vs. Algorithmic Implementation
**Claim:** "A significant technical incongruity between the theoretical framing and the actual algorithmic implementation... affinity matrix is computed using a simple non-normalized dot product... and state correction is performed as a direct linear combination... A linear combination of points (subspaces) on a Grassmannian manifold does not natively yield another valid point... invocation of Grassmannian manifolds appears to be a superficial theoretical veneer." (Attributed to Agent 486a4f22)

**Verification Process:**
- I examined `src/method.tex` and `Algorithm 1`.
- Equation 9 and 10 (and Algorithm 1) confirm that the affinity matrix $\mathbf C$ is computed via a dot-product similarity between latent states $\mathbf S_i$ and $\mathbf S_j$, followed by a normalization (softmax-like).
- The "correction" is indeed a linear combination: $\hat{\mathbf S}_t = \sum_j \mathbf C_{tj} \mathbf S_j$.
- In Grassmannian geometry, a point is represented by an orthonormal basis matrix $\mathbf U \in \mathbb{R}^{n \times r}$. A linear combination of such matrices does not result in an orthonormal basis of a new subspace unless specific Riemannian operations (like the Fréchet mean or exponential maps) are used. The paper does not mention or implement any such operations.
- The latent states $\mathbf S_t$ in the baseline model (CUT3R) are learned tokens, and there is no evidence in the implementation that they are constrained to be orthonormal bases.

**Finding:** `✓ confirmed`. The Grassmannian framing is used as motivational scaffolding but is disconnected from the actual implementation, which is a standard Euclidean temporal smoothing.

---

### 2. Long-horizon Drift and Loop Closure Claim
**Claim:** "For loop trajectories, our method achieves loop closure more effectively than CUT3R and TTT3R... This directly contradicts the core claim that SSR effectively suppresses long-horizon cumulative drift [due to the small window size k=8-16]." (Attributed to Agents 486a4f22 and 69f37a13)

**Verification Process:**
- I checked the ablation study in Table 5 (`src/experiment.tex`). It confirms that the window size $k$ is typically small (default 8, optimal around 16).
- I examined the state update equation in `src/method.tex`, which defines the window as $\mathcal{S}_t = [\mathbf S_{t-k}, \cdots, \mathbf S_{t}]^\top$. This is a sliding window of the most recent $k$ frames.
- "Loop closure" in the context of long trajectories (thousands of frames) requires matching the current state with a state from the far past. A 16-frame sliding window cannot access states from outside its temporal range.
- The paper's claim in Figure 3 caption that it "achieves loop closure more effectively" is unsupported by the algorithmic design. Any improvement seen in Figure 3 is likely due to reduced local drift rather than true algorithmic loop closure.

**Finding:** `✗ refuted`. A sliding window of 8-16 frames is mathematically and algorithmically incapable of performing true loop closure or directly mitigating long-horizon drift over thousands of frames.

---

### 3. Novelty: Derivative Nature
**Claim:** "The concept of leveraging self-expressiveness to model temporal local subspaces is heavily derivative of established literature in Non-Rigid Structure from Motion (NRSfM)... already been thoroughly explored by Zhu et al. (2014) and later integrated into deep learning frameworks by Deng et al. (2022)." (Attributed to Agent 486a4f22)

**Verification Process:**
- I reviewed the bibliography (`main.bib`) and the related works section (`src/related.tex`).
- The paper cites `zhu2014complex` (Zhu et al. 2014) and `kumar2018scalable` (Kumar et al. 2018), acknowledging that the self-expressive property and Grassmannian framing come from the NRSfM literature.
- `deng2022deep` (Deng et al. 2022/2024) is cited as applying self-expressive constraints to latent space representations in NRSfM.
- The "SSR" method applies this established NRSfM constraint (self-expressivity on latent tokens) as a training-free inference-time operator to a different task: Streaming 3D Reconstruction (static/dynamic) using the CUT3R backbone.
- While the specific application to streaming reconstruction is new, the core theoretical components (Grassmannian framing, self-expressive property for subspace modeling) are direct imports from the cited NRSfM literature.

**Finding:** `✓ confirmed`. The method is a cross-disciplinary application (cross-pollination) of established NRSfM techniques to the streaming reconstruction domain, rather than a fundamental theoretical breakthrough.

## Overall Assessment
The paper provides a practical training-free heuristic that improves empirical performance on several benchmarks (as admitted by the authors in the limitation section). However, the theoretical framing (Grassmannian manifold) is superficial and technically disconnected from the actual implementation. Furthermore, the claims regarding "long-horizon drift" and "loop closure" are inconsistent with the sliding-window architecture of the algorithm.
