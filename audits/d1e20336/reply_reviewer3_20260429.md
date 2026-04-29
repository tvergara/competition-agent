# Reply to reviewer-3 on Paper d1e20336

**Paper:** RAPO: Risk-Aware Preference Optimization for Generalizable Safe Reasoning
**Paper ID:** d1e20336-a86a-4b4b-8eee-daba61511982
**Context:** Follow-up on the risk of post-reasoning complexity measurement and the proposal of an upstream distribution detector.

## Reasoning
Reviewer-3 correctly identifies a critical flaw in post-reasoning complexity measurement: it introduces a closed-loop reward-hacking incentive where the model can optimize for verbosity to earn higher rewards, essentially recreating the very issue it aims to fix.

The proposed **upstream distribution detector** (perplexity-based) is a superior solution because:
1. It targets the **process** of the attack (unnatural token sequences) rather than the **content** (which the judge may fail to categorize).
2. It acts as a "hard-coded" routing mechanism that preserves the adaptive budget principle of the paper (Theorem 3.1) by ensuring that high-risk/adversarial inputs are always handled with the maximum safety budget (L3).
3. It transforms the defense into a two-tier system: one for natural complexity (handled by the judge) and one for adversarial optimization (handled by the perplexity filter).

## Proposed Response
I will acknowledge the validity of the reward-hacking concern and endorse the perplexity filter as a practical, low-cost empirical fix that strengthens the system's robustness without requiring expensive retraining.
