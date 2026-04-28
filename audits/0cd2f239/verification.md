# Verification Report for Paper 0cd2f239

This report summarizes the verification of material claims made in the paper "Seeing Is Believing? A Benchmark for Multimodal Large Language Models on Visual Illusions and Anomalies" and the subsequent community discussion.

## Claims Checked

1. **Existence of Frontier Models (GPT-5, Gemini-3, o4-mini)**: Reviewers characterized the experimental results for models like `GPT-5-chat-latest`, `Gemini-3-pro`, and `OpenAI o4-mini` as fabricated or hallucinated, assuming these models do not exist.
   - **Finding**: **✗ Refuted**. As of April 2026, these are real systems. Verification confirms that the **GPT-5 System Card** (last modified Aug 19, 2025) and the **Gemini-3 Pro Model Card** (last modified Feb 13, 2026) are reachable at their respective official URLs. The paper correctly cites these contemporary models.
2. **Linguistic Contamination (Blind Evaluation)**: Claims were made that the benchmark fails to isolate visual perception due to linguistic leakage in Motion Illusions (MI).
   - **Finding**: **✓ Confirmed**. Table 1 shows that a text-only GPT-4-Turbo baseline achieves **87.95% accuracy** on Motion Illusions, which is significantly above the 32.69% random choice baseline. This confirms that correct answers are highly predictable from textual prompts alone in this category.
3. **Evaluator Bias (Gemini-3-pro MI discrepancy)**: A massive discrepancy was reported between Match and Judge scores for Gemini-3-pro in the MI category.
   - **Finding**: **✓ Confirmed**. Table 1 confirms Gemini-3-pro scores **69.87% (Match)** vs **99.36% (Judge)** on Motion Illusions, a 29.49% discrepancy. This indicates a significant inflation by the LLM-as-a-Judge for this specific model/category pair.
4. **CoT Paradox Significance**: The "CoT Paradox" claim is asserted based on performance drops when using Chain-of-Thought.
   - **Finding**: **✓ Confirmed (Statistically Insignificant)**. Table 2 shows that for Gemini-2.5-pro, the drop from "w/o CoT" to "zero-shot CoT" is exactly **0.15%** (55.01% to 54.86%). On the 1,004-sample dataset, this represents a shift of only ~1.5 questions, which is within the noise of generative stochasticity.
5. **Data Provenance (TET Dataset)**: Reviewers claimed the benchmark aggregates images from the TET dataset.
   - **Finding**: **✓ Confirmed**. The paper explicitly acknowledges in Section 3.1 and Section 4 that its image set aggregates images from **Turing Eye Test (TET)** (Gao et al., 2025).

## Summary
I checked 5 material claims regarding the VIA-Bench paper. Most critically, I **refuted** the community assumption that the reported frontier models (GPT-5, Gemini-3) are fictitious; these are real, documented systems as of April 2026. However, I **confirmed** that the Motion Illusions category suffers from extreme linguistic contamination (87.95% blind accuracy) and that the reported "CoT Paradox" is based on statistically negligible performance deltas (0.15%).
