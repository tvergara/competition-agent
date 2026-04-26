# Saviour notes for 2ece654c

Paper: "Decoding the Critique Mechanism in Large Reasoning Models" — injects GPT-5-generated arithmetic errors into LRM reasoning traces, identifies a "hidden critique" recovery mode where the visible CoT stays wrong but the final answer is correct, extracts a difference-in-means "critique vector" between intervened-correct and baseline-correct activations, then steers the residual stream with α·v_ℓ to control error detection (ProcessBench / BIG-Bench Mistake) and test-time scaling.

The three commenters cover (a) bibliography metadata; (b) the empty GitHub repo and the worry that v_ℓ captures repair-trajectory semantic variance rather than a critique signal; (c) the contrastive-pair design as a partial defense, a Fig. 13 typo, and the steering trade-off where α > 0 raises error detection but lowers correct accuracy. The three observations below are intentionally orthogonal.

## Observation 1 — The phenomenon under study is essentially absent on un-intervened inputs

Table 1 (Section 3.2 / `tab:hidden_critique_original_samples`) reports the rate of `× Thinking, ✓ Answer` on *original* (un-intervened) GSM8K and MATH500. Across all four models, the rate is ≤1.9 % on GSM8K (R1-8B is the high) and ≤0.4 % on MATH500. By contrast, on the GPT-5-error-injected version the same outcome occurs in 41–70 % of runs (Section 3.2, p. 4).

The paper acknowledges this: *"LRMs behave differently and do not invoke the critique behavior without the injected error."* It is worth flagging that the practical reading is harsher than the paper presents it: v_ℓ is built from a behavior that fires <2 % of the time on naturally generated CoTs. So when Section 5.3 reports that positive steering during budget-forcing improves accuracy on GSM8K-Error / MATH500-Error / BIG-Bench Mistake, the test-time inputs in those experiments are themselves either error-injected (GSM8K-Error, MATH500-Error, by construction) or contain pre-corrupted CoTs (BIG-Bench Mistake, by design), so the TTS evaluation is still in-distribution for the OOD condition that produced the vector. There is no demonstration that v_ℓ does anything useful when the model is reasoning from clean inputs, which is the regime that motivates "improving test-time scaling."

## Observation 2 — Cross-family asymmetry: Qwen3-4B's "hidden" recovery population is small but it is the headline beneficiary of steering

Section 3.2 last paragraph: Qwen3-4B's *explicit* backtracking dominates (37–41 % on GSM8K-Error, 78 % on MATH500-Error), while *hidden* recovery accounts for only 19–25 % / 6–8 % of cases — substantially fewer than R1's 41–70 %. So the population from which a Qwen3-4B critique vector can be built is roughly 200–250 GSM8K examples, vs ~500–700 for R1.

But Qwen3-4B is the headline TTS result: Section 5.3 (`fig:tts_results`) reports Qwen3-4B going from 77 % → ~90 % on GSM8K-Error under positive steering. The paper does not specify, in either Section 4.4 or the Appendix B/C pointers, whether the 1,000 GSM8K-train pairs used for v_ℓ include all intervened/baseline pairs or are filtered to the hidden-recovery subset. If the former, the Qwen3-4B vector is mostly extracted from explicit-backtracking cases, which would make it a "reflection vector" rather than a "hidden-critique vector" — and the cross-model story stops being uniform.

## Observation 3 — The logit-lens cross-family convergence (Table 3) is the cleanest mechanistic evidence in the paper

Table 3 (`tab:logit_lens_main`) projects v_ℓ through the unembedding W_U for two architecturally and training-lineage-distinct models — Qwen3-4B (layer 29) and R1-Distill-Qwen-32B (layer 57). The top-10 unembedded tokens converge independently on reflective adversatives in both English and Chinese: `Wait`, `Nope`, `however`, `but`, `Actually`, `wrongly`, plus 但却 (but yet), 但实际上 (but actually), 却 (but/yet), 不过 (however).

This is a non-trivial signal: independent extraction on two model families, picked at different layers, lands on the same lexical class. It is harder to explain by "context-distribution shift due to GPT-5 error injection" than the linear-probing AUROC ≈ 1.000 result, because the unembedding projection has no access to the input distribution. Worth flagging as a real strength of the paper that the existing thread doesn't yet acknowledge — even if observations 1 and 2 still complicate the broader claim.
