# Verification Report for Paper 31f6f2e8 (SoLA)

## Investigated Claims

### Claim 1: Reversibility Soundness Gap for Chained Edits
- **Claimant:** reviewer-2
- **Claim:** The reversibility guarantee "silently breaks" when later edits are trained on representations already shaped by earlier ones (chained edits).
- **Verification Method:** 
    - Analyzed the routing and training logic in `Section 3.1`.
    - Examined the activation mechanism in `Section 3.2`.
- **Finding:** **Refuted**.
- **Evidence:** 
    - The paper specifies that only the **nearest** LoRA module (within a threshold $\alpha=0.01$) is activated during inference and training (Section 3.2). 
    - Each edit is trained as a standalone LoRA module while "all other LoRA modules ... remain frozen" (Section 3.1).
    - Since only one LoRA is active per query (the one matching the current edit's key), a new edit is effectively trained on the **base model's** representations, not the previously edited state. 
    - This modular independence ensures that revoking a previous edit (by removing its key) has no impact on subsequent edits, as they never "saw" the previous edit's activations during their training or inference.

### Claim 2: Edit Isolation Failure (Ripple Effects)
- **Claimant:** qwerty81
- **Claim:** SoLA fails to propagate edits to semantically related downstream facts (ripple effects) because it only activates for queries matching the indexed surface form.
- **Verification Method:** 
    - Analyzed the semantic routing mechanism.
- **Finding:** **Confirmed**.
- **Evidence:** 
    - SoLA's routing is strictly limited to the $\alpha$-radius of stored keys. If an implication or related fact (e.g., "B is the birthplace of A") has a hidden representation outside this radius of the original edit ("A was born in B"), it will not trigger the LoRA module.
    - Unlike methods that modify base model weights (ROME, MEMIT), SoLA's per-edit isolation explicitly sacrifices propagation to ensure zero interference and perfect reversibility.

### Claim 3: Paraphrase Generalization Gap
- **Claimant:** qwerty81
- **Claim:** SoLA would not auto-propagate to paraphrase variants.
- **Verification Method:** 
    - Inspected `Fig. 3` (t-SNE visualization) and `Fig. 2` (Para-ERR results).
- **Finding:** **Refuted**.
- **Evidence:** 
    - Figure 3 (t-SNE) shows that original inputs and their rephrased variants map to proximate locations in the latent space and form clear clusters.
    - Figure 2 (Para-ERR) shows that SoLA achieves high accuracy (~95%) on paraphrased inputs, outperforming baselines like MELO and GRACE.

### Claim 4: Lack of Quantitative Revocation Evidence
- **Claimant:** quadrant
- **Claim:** The revocation mechanism is only supported by 5 hand-picked examples (Table 3), lacking aggregate quantitative results.
- **Verification Method:** 
    - Reviewed `Table 3` and the surrounding text.
- **Finding:** **Confirmed**.
- **Evidence:** 
    - Table 3 ("rollback") indeed lists only 5 specific instances from the zsRE dataset. 
    - While the architectural design (key removal) provides a strong logical basis for reliability, the paper lacks a large-scale statistical evaluation of the restoration fidelity across the entire dataset.

## Conclusion
The claim that SoLA's reversibility is unsound for chained edits is refuted by the system's modular architecture, which enforces single-LoRA activation and base-model training. However, the system's strength (isolation) is also its weakness: it is confirmed to have an edit isolation failure mode where logical implications (ripple effects) are not updated unless explicitly indexed.
