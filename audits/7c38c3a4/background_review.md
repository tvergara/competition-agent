# Background Review: TAB-PO

Paper: `7c38c3a4-4ee3-4436-a93d-56f4a163fb5e`

Title: TAB-PO: Preference Optimization with a Token-Level Adaptive Barrier for Token-Critical Structured Generation

## Claim I Checked

TAB-PO argues that standard sequence-level DPO is brittle for token-critical structured generation, especially when chosen and rejected completions differ in only a few semantically decisive tokens. Its method combines token-weighted, reference-adjusted preference advantages with a confidence-gated preferred-token barrier. The reported preference baselines are DPO, IPO/psiPO, SimPO, Cal-DPO, and DPO-Positive/Smaug.

In the paper source, the authors state that the compared recent DPO-style variants "remain sequence-level" and do not target token-critical supervision for structured extraction. I checked the source with `rg` and found no matches for `TDPO`, `TIS-DPO`, `Token-Importance`, `Selective Preference`, or `T-REG`.

## Closest Prior Work

1. **TDPO: Token-level Direct Preference Optimization** (`arXiv:2404.11999`)

   TDPO is a direct prior on token-level DPO. It reformulates preference optimization over autoregressive generation with token-level rewards, a token-level Bradley-Terry/regret formulation, and sequential KL terms. It is not a structured-extraction method and does not use TAB-PO's semantic Code/Sub-code/Span weights or confidence barrier, but it is a necessary related-work boundary for any broad "token-level DPO" framing.

2. **TIS-DPO: Token-level Importance Sampling for Direct Preference Optimization With Estimated Weights** (`arXiv:2410.04350`, ICLR 2025)

   TIS-DPO is the closest missing baseline for the token-importance part. It explicitly argues that DPO treats the whole response as one arm and ignores token-importance differences, then assigns per-token importance weights estimated from contrastive LLMs. TAB-PO differs by using task-defined semantic field weights and a preferred-token barrier, but TIS-DPO is directly relevant to whether token weighting, rather than the barrier or structured data construction, drives the gain.

3. **SePO: Selective Preference Optimization via Token-Level Reward Function Estimation** (`arXiv:2408.13518`, EMNLP 2025)

   SePO estimates token-level rewards and selects key tokens for preference optimization. It differs from TAB-PO because it learns/selects key tokens with an oracle model and uses a reference-free contrastive objective rather than schema-defined weights. Still, it is a close neighbor for the claim that fine-grained token selection improves preference optimization.

4. **T-REG: Preference Optimization with Token-Level Reward Regularization** (`arXiv:2412.02685`, ACL 2025)

   T-REG uses token-level reward regularization to distribute sparse sequence-level preference signal over tokens. It is a general instruction-following method rather than a structured medical extraction method, but it is relevant background for token-level credit assignment in preference optimization.

5. **TI-DPO: Token-Importance Guided Direct Preference Optimization** (`arXiv:2505.19653`)

   TI-DPO explicitly targets DPO's failure to account for differential token importance, using gradient-attribution token-importance weights and a triplet loss. It is another strong missing baseline or boundary condition for TAB-PO's weighted-token component.

## Three-Axis Assessment

**Attribution.** The paper should cite and position at least TDPO and TIS-DPO, and likely SePO/T-REG/TI-DPO. The current related-work framing discusses only sequence-level DPO variants after DPO itself, which makes the token-level contribution look less contextualized than it is.

**Novelty.** I do not think these priors make TAB-PO redundant. TAB-PO's specific combination remains distinct: structured medical annotation, low-edit-distance confusion-aware pairs, hand/task-defined semantic token weights for Code/Sub-code/Span fields, reference-adjusted advantages, and a confidence-gated preferred-token barrier. The novelty should be scoped to that combination rather than to token-level preference optimization broadly.

**Baselines.** TIS-DPO and TI-DPO are the clearest missing baselines or explicit boundary conditions. TDPO should at minimum be in related work. If implementation cost is high, the authors should still explain why these token-level methods are not comparable for PV-Miner.

## Public Comment Summary

I will comment that TAB-PO appears distinct, but its baseline/related-work set omits several direct token-level DPO and token-importance preference optimization neighbors. The main recommendation is to add TDPO/TIS-DPO/TI-DPO positioning and, ideally, at least a TIS-DPO or TI-DPO comparison to isolate how much of TAB-PO's gain comes from token weighting versus the adaptive barrier and structured preference construction.
