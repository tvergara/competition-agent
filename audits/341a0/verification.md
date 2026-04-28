# Verification Report for Paper 341a0a9e

## Claims Checked

1. **Table 1 Arithmetic Inconsistencies**
   - **Original Claim**: Headline results in Table 1 are inconsistent with test set sizes in Table 7. LLaMA results are transposed and Opus-4.5 results are cyclically shifted.
   - **Agent**: Saviour
   - **Check**: Compared `tab:main_results` (Table 1) and `tab:rl_split` (Table 7) in `example_paper.tex`.
   - **Finding**: ✓ **confirmed**. 
     - Table 7 shows Miss Param has 22 samples and Long Context has 23. 
     - LLaMA "Ours" results: Miss Param says 60.87% (14/23) and Long Context says 54.54% (12/22). The denominators are swapped.
     - Opus-4.5 results: Miss Func says 65.22% (15/23), Miss Param says 64.71% (11/17), and Long Context says 59.09% (13/22). The categories are cyclically shifted.

2. **Algorithm Efficacy on SFT Initialization**
   - **Original Claim**: Adding RC-GRPO to a standard SFT model yields negligible or negative gains.
   - **Agent**: Saviour
   - **Check**: Verified Table \ref{tab:ablation_rctp_init}(A) in `example_paper.tex`.
   - **Finding**: ✓ **confirmed**. LLaMA shows 0.00% change (35.00% -> 35.00%) and Qwen shows -2.50% change (48.75% -> 46.25%) when adding RC to SFT-based GRPO.

## Summary

Out of 2 claims checked, 2 were confirmed. The arithmetic errors in the main results table are significant and suggest a copy-paste or calculation error in the final manuscript preparation. Furthermore, the ablation results confirm that the primary driver of performance in this paper is the RCTP-FT initialization stage rather than the RC-GRPO algorithm itself when starting from standard supervised fine-tuning.

