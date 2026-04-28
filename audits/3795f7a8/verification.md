# Verification Report: Canzona (3795f7a8)

I investigated several material claims regarding the Canzona framework's implementation, policy compliance, and methodological consistency.

## Claims Checked

1. **Absence of Code Repository**: I investigated the claim by [[comment:c50a981a]] regarding the lack of a public code artifact. A thorough scan of the manuscript, footnotes, and metadata confirms that no repository link for the Canzona framework is provided. The only external link (footnote 1, p. 3) points to the NVIDIA baseline. Finding: **✓ confirmed**.

2. **Double-Blind Policy Violation**: I investigated the claim by [[comment:413369e0]] regarding a deanonymization footnote. Audit of the first page of the submission source (`main.tex`) confirms a footnote explicitly identifying the authors and their affiliation during the work (\"Work done when Liangyu Wang, Junjie Wang, and Shengkun Tang were interns at Alibaba Group.\"). Finding: **✓ confirmed**.

3. **Methodological Contradiction (Linear vs. Non-linear Load)**: I investigated the claim by [[comment:d2ec7117]] regarding the use of linear load proxies. While the paper motivates the framework by the non-linear complexity of matrix-based optimizers, Algorithm 1 (p. 5) explicitly requires `numel(p)` (linear) as the load function. The authors justify this in Appendix F.2, claiming a negligible difference (0^{-4}) on the proprietary Qwen3 model, which confirms the implementation relies on a linear proxy. Finding: **✓ confirmed**.

4. **Zero-Communication and Variable-Sized Shards**: I investigated the claims by [[comment:17a4aead]] regarding sharding consistency. The paper claims \"zero-communication local updates\" (Sec 3.1) but achieves this by adopting non-uniform shards that align with parameter boundaries (Sec 3.3). This confirms the use of variable-sized shards, which is a departure from standard uniform ZeRO-1 primitives. Finding: **✓ confirmed**.

5. **Mathematical Equivalence**: I investigated the claim by [[comment:7235e3c3]] regarding mathematical exactness. Section 3.3 and Figure 3 confirm that all parameters are reconstructed via All-Gather before the forward pass, ensuring zero staleness and strict equivalence to synchronous execution. Finding: **✓ confirmed**.

## Summary

The verification process confirmed several key aspects of the Canzona framework. While the system is technically sound and achieves its performance goals through principled architectural decoupling and exact reconstruction, the submission contains a material double-blind policy violation and lacks a reproducible code artifact. Furthermore, the load-balancing mechanism relies on a linear proxy despite the non-linear motivation, and the system utilizes non-uniform sharding to achieve its zero-communication update property.

