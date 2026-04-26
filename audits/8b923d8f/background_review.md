# Background/Novelty Review: BFS-PO

Paper: `8b923d8f-5d39-4b5a-8d70-1ed0cd54ad4c`

I audited BFS-PO against nearby work on RL-based efficient reasoning and tree-search training. My main finding is a missing close prior/baseline rather than a claim that the paper is non-novel.

## Paper Claim

BFS-PO fine-tunes a reasoning model by constructing a search tree during RL training. It selects the shortest correct complete solution found so far, chooses a high-entropy token on that path as a backtracking point, samples continuations from that prefix, and trains with a branch-level advantage. At inference, it uses ordinary single-chain sampling. The goal is to reduce overthinking while maintaining or improving accuracy.

## Prior Work Checked

### TreeRL: LLM Reinforcement Learning with On-Policy Tree Search (arXiv:2506.11902)

TreeRL is the closest tree-search RL neighbor I found. It performs on-policy tree search for RL training, forks from high-uncertainty intermediate steps, and computes process supervision from local and global advantages over tree nodes. BFS-PO cites TreeRL and distinguishes itself by using shortest-correct best-first selection, entropy-based backtracking on the selected path, and a sibling branch advantage. The paper does not run a direct TreeRL baseline, but it does include a "w/o BFS" variant that the authors explicitly relate to TreeRL. I consider the attribution mostly adequate here.

### ShorterBetter (arXiv:2504.21370)

ShorterBetter defines Sample Optimal Length as the length of the shortest correct response among sampled generations and uses that as a dynamic reward signal in GRPO. This is directly relevant to BFS-PO's "shortest correct solution" target. BFS-PO cites ShorterBetter and notes that its penalty is computed relative to the current shortest positive answer. The distinction is that BFS-PO conditions new exploration on prefixes of the current best path and trains over a tree rather than only reweighting independent group samples.

### Concise Reasoning via Reinforcement Learning (arXiv:2504.05185)

This paper analyzes PPO/GRPO length dynamics and argues that verbosity can arise from RL loss optimization, then proposes a later RL phase on solvable problems to enforce concision. BFS-PO cites it for the length-accuracy relation and GRPO/PPO overthinking dynamics. It is important background but less mechanistically close than TreeRL, ShorterBetter, or S-GRPO.

### S-GRPO: Early Exit via Reinforcement Learning (arXiv:2505.07686)

This is the missing neighbor that seems material. S-GRPO replaces GRPO's parallel group of independent full CoTs with a serial group built from one reasoning path. It samples early-exit paths from different positions in the trajectory, has the model answer from those prefixes, and assigns larger rewards to earlier correct exits. It reports 35.4%-61.1% sequence-length reductions while improving accuracy on GSM8K, AIME 2024, AMC 2023, MATH-500, and GPQA Diamond.

S-GRPO is not identical to BFS-PO: it trains early exits from serial prefixes, while BFS-PO branches from high-entropy points on the shortest correct solution and uses branch advantages. But it is close enough that it should be cited and either compared against or explicitly scoped out. Both works use verifier-based RL to make shorter correct reasoning trajectories more likely, and both move beyond a static global length penalty.

### TokenSkip (arXiv:2502.12067)

TokenSkip constructs compressed CoT training data by pruning lower-importance tokens and fine-tunes models to produce controllably compressed reasoning. BFS-PO cites TokenSkip, follows its experimental protocol, and compares against its reported results. The distinction is clear: TokenSkip is SFT over compressed CoTs; BFS-PO is on-policy RL with search-tree exploration.

## Three-Axis Assessment

Attribution: Mostly adequate for TreeRL, ShorterBetter, Concise RL, TokenSkip, DAPO, and First Finish Search. The gap is S-GRPO, which appears absent despite being a close RL-based efficient-reasoning method with overlapping benchmarks and a verifier-based shorter-correct reward structure.

Novelty: BFS-PO appears to contribute a distinct combination of shortest-correct best-first tree expansion, entropy backtracking on that selected trajectory, and sibling branch advantage. I would not characterize the method as simply duplicating TreeRL, ShorterBetter, or S-GRPO.

Baselines: S-GRPO is an obvious missing comparator, or at minimum a method that should be discussed. The paper's statement that CoT-shortening methods typically sacrifice accuracy should also be qualified, because S-GRPO reports simultaneous length reduction and accuracy gains.

## Bottom Line

I would ask the authors to add S-GRPO to related work and clarify whether a direct comparison is feasible. If a direct run is not feasible because of model/checkpoint/protocol differences, the paper should still explain why the comparison is excluded and narrow the empirical claim accordingly.
