# Background and Novelty Audit: DEL Framework

## Summary of Paper
The paper proposes **DEL**, a framework for differentially private (DP) and communication-efficient LLM split inference. The method uses an encoder-decoder for dimensionality reduction, a stochastic hBcbit quantization mechanism that provides DP guarantees, and server-side soft prompts to restore utility lost due to the DP noise. A key claim is that this is the first work to use soft prompts to improve the privacy-utility trade-off in LLM inference.

## Related Works Comparison
I identified five closely related works to assess the context and novelty of DEL:

1.  **Split-and-Denoise (SnD)** (Mai et al., ICML 2024): Uses local DP and a separate 6-layer Transformer denoiser on the server. DEL improves upon this by using soft prompts (more integrated and lightweight) and quantization (more communication-efficient).
2.  **PrivacyRestore** (Zeng et al., ACL 2025): Uses "restoration vectors" and activation steering to restore information from "privacy spans" (removed tokens). This is functionally very similar to using soft prompts for utility restoration, though the threat model (token removal vs. embedding noise) differs.
3.  **POST: Efficient and Privacy-Preserving Soft Prompt Transfer for LLMs** (Wang et al., ICML 2025): Focuses on private tuning of soft prompts and their transfer between models. While the goal is different (transfer vs. split inference), it establishes the use of soft prompts in private LLM contexts.
4.  **InferDPT** (Tong et al., 2025): Uses discrete token replacement for privacy and requires a local model for denoising/reconstruction. DEL eliminates the need for local models by using server-side soft prompts.
5.  **DP-OPT** (Hong et al., ICLR 2024): Focuses on private offsite prompt tuning. It uses DP ensembles for prompt generation.

## Three-Axis Assessment

### 1. Attribution
The paper provides a good overview of the split inference and DP-LLM literature, citing **SnD** and **InferDPT** as primary baselines. It also correctly cites **QSGD** for the quantization foundations and **Gaussian Differential Privacy (GDP)** for the privacy analysis framework. 

However, there is a notable omission of:
- **PrivacyRestore** (ACL 2025): Given its similar approach of using continuous "restoration vectors" to maintain utility in private inference, it is a critical missing reference.
- **POST** (ICML 2025): Relevant for the use of soft prompts in DP settings.

### 2. Novelty
The claim of being the **"first work that utilizes soft prompt to improve the trade-off between privacy and utility in LLM inference"** (Section 1 and 3) is contested by the existence of **PrivacyRestore** (which uses "restoration vectors" for a similar purpose) and **POST**. While the specific application to split-inference with embedding-level DP noise and quantization is indeed novel, the claim should be more carefully qualified to distinguish DEL from these contemporary works.

The technical contribution of **DP stochastic quantization**—framing stochastic rounding as a standalone DP mechanism in the latent space—is a clever and efficient way to handle the privacy-communication-utility triangle.

### 3. Baselines
The experimental comparison against **SnD** and **InferDPT** is thorough and demonstrates clear advantages in both communication (bits per coordinate) and utility (PPL/Acc/COH). The "Gaussian mechanism + soft prompt" baseline in Section 4.2 is a strong addition that validates the specific benefits of the proposed stochastic quantization over standard additive noise.

The omission of **PrivacyRestore** as a baseline is a gap, as it also addresses utility restoration for private LLM inference, albeit through a different privacy mechanism (token redaction).

## Conclusion
**Verdict: Neutral (Incremental but practical improvement)**
The paper presents a well-engineered framework that solves a real-world problem (local resource constraints in private inference) more effectively than previous methods like SnD and InferDPT. However, the novelty claims are slightly overstated by ignoring contemporary work on restoration vectors and soft prompt DP.

**Key supporting works:**
- Mai et al. (ICML 2024) for the Split-and-Denoise paradigm.
- Zeng et al. (ACL 2025) for "PrivacyRestore" (the missing link).
