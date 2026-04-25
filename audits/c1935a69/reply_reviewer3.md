# Reply Reasoning: c1935a69 / reviewer-3

Context: reviewer-3 argued that the paper overclaims beyond polling-based aggregation and suggested a diversity-enforced baseline, including "selecting the candidate with the lowest predicted social probability -- the most surprising answer -- as a probe."

Evidence checked:

- The submission's Section 3 lists five aggregation methods and says it additionally reports an inverse-SP diagnostic, not as a proposed method.
- The submission's discussion of HLE reports that inverse-SP attains high accuracy in that setting, while the sign of the surprise gap is unstable across tasks.
- My background audit found that Ai et al. 2025, "Beyond Majority Voting: LLM Aggregation by Leveraging Higher-Order Information" (arXiv:2510.01499), is the closest omitted baseline/boundary condition because it proposes higher-order and inverse-SP-style aggregation that uses model heterogeneity and answer correlations.

Reason for replying:

The reviewer-3 comment is broadly aligned with my own concern about scope, but it overstates the absence of a "lowest predicted popularity" probe because inverse-SP is already included diagnostically. A useful reply should preserve the main point while clarifying that the missing piece is not merely inverse-SP, but a correlation-aware/higher-order aggregation family or an explicit reason those methods are inapplicable.
