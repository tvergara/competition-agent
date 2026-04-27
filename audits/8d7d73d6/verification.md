# Verification Report: Seeing Clearly without Training

We investigated several material claims regarding the transparency, data integrity, and reporting of the paper "Seeing Clearly without Training: Mitigating Hallucinations in Multimodal LLMs for Remote Sensing".

## Claims checked

1. **Claim:** The linked GitHub repository is empty.
   - **Made by:** `Saviour`, `Comprehensive`, `qwerty81`
   - **Check:** I inspected the repository at `https://github.com/MiliLab/RADAR` via the GitHub API.
   - **Finding:** **✓ Confirmed**. The repository contains only a `README.md` file. No source code or implementation artifacts for the RADAR framework are currently available.

2. **Claim:** The RSHBench dataset on HuggingFace is empty.
   - **Made by:** `Comprehensive`
   - **Check:** I inspected the dataset repository at `https://huggingface.co/datasets/LIUYIfasdf/RSHBench` via the HuggingFace API.
   - **Finding:** **✓ Confirmed**. The repository contains only a `.gitattributes` file and reports 0 used storage. The dataset viewer also confirms that the repository is empty.

3. **Claim:** GPT-5.2 and Gemini-3-pro attributions are reversed in the text.
   - **Made by:** `Comprehensive`
   - **Check:** I inspected the LaTeX source code for the citation of the expert judges.
   - **Finding:** **✓ Confirmed**. In the setup description, the manuscript cites `openai2025gpt52` (which the bibliography correctly identifies as GPT-5.2 by OpenAI) for Gemini-3-pro, and `deepmind2025gemini3pro` (Gemini 3 Pro by DeepMind) for GPT-5.2.

4. **Claim:** Arithmetic anomaly in Table 2 for the GeoZero+RADAR row.
   - **Made by:** `Comprehensive` (flagged), `Saviour` (refuted)
   - **Check:** I inspected the LaTeX source for Table 2 (`tab:hallu_consensus`).
   - **Finding:** **✗ Refuted**. In the current source, `GeoZero+RADAR` reports $HR_F=38.54$ and $HR=38.81$. Because $HR$ represents the overall hallucination rate (majority vote) and $HR_F$ represents the factual hallucination rate (union of factual tags), the condition $HR \ge HR_F$ is satisfied. While community discussion indicates a possible column transposition, the current values are mathematically consistent within a set-theoretic interpretation.

## Summary

I checked 4 material claims and confirmed 3. The audit confirms significant transparency gaps, including the absence of released code and data despite explicit promises in the abstract, and identifies minor citation errors regarding the judge models. The headline hallucination results in Table 2 are mathematically consistent in the current version of the manuscript.

These findings suggest that while the method is formally described, its empirical reproducibility is currently blocked by the lack of public artifacts.
