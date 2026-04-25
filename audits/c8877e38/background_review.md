# Background Review: DIVE

Paper: `c8877e38-1784-4b7f-a23a-a79a154ba733`

This audit focuses on closest-neighbor attribution for DIVE's claim about diverse, verifiable, executable task synthesis for tool-using agents. I read DIVE alongside:

- APIGen, arXiv:2406.18518
- APIGen-MT, arXiv:2504.03601
- ToolACE, arXiv:2409.00920
- AgentInstruct, arXiv:2407.03502
- EnvScaler, arXiv:2601.05808
- WebExplorer, arXiv:2509.06501

## Paper Claim Being Audited

DIVE argues that current agentic synthesis pipelines do not scale structural diversity while preserving executability and verifiability. Its proposed solution is evidence-first synthesis: sample a heterogeneous real-tool set, execute tools to collect grounded evidence, then reverse-derive query-answer tasks strictly entailed by those traces. The resulting data trains Qwen3-8B through SFT and RL and improves generalization across L2/L3 tool-use benchmarks.

## Neighbor Comparisons

### APIGen

APIGen is not cited, but it is a direct antecedent for the broad framing of "diverse, verifiable function-calling datasets." APIGen collects 3,673 executable APIs across 21 categories and verifies generated data through format checking, actual function execution, and semantic verification. It also explicitly treats query-style diversity, API sampling diversity, and API-category diversity as central ingredients for robust function-calling training.

DIVE is still distinct: APIGen is query-first and verifies generated function calls after generation, whereas DIVE executes tools first and derives tasks from observed traces. That distinction is important and should be made explicitly.

### APIGen-MT

APIGen-MT is also not cited. It is close to DIVE on verifiable multi-turn agent data: it first constructs task blueprints with ground-truth actions, validates executability, and then generates complete human-agent-environment trajectories through simulated interplay. It also trains the xLAM-2-fc-r model family.

DIVE differs by scaling broader tool-pool diversity and by using evidence-first trace collection rather than blueprint-first simulation, but APIGen-MT is close enough that it should appear in the related work and baseline discussion.

### ToolACE

ToolACE is not cited. This is the closest missing prior for the "diversity scaling" part of DIVE. ToolACE synthesizes a large API pool, generates function-calling dialogs through a self-guided multi-agent process, and uses dual-layer verification. It explicitly studies how API diversity, data complexity, and verification affect tool-use performance. In particular, its diversity ablations are directly relevant to DIVE's claim that structural diversity improves generalization.

DIVE's stronger novelty is not simply "diverse and verified tool-use data"; it is the evidence-first inversion over real tool executions and the reverse derivation of tasks from traces.

### AgentInstruct, EnvScaler, and WebExplorer

These are cited by DIVE. AgentInstruct is a broad antecedent for agentic synthetic post-training data. EnvScaler is cited and used as a generalizable synthesized-environment baseline. WebExplorer is cited and used as a specialist web-agent baseline. These comparisons are appropriate, but they do not substitute for APIGen/APIGen-MT/ToolACE, which are closer to the verifiable function-calling and tool-use data synthesis claim.

## Three-Axis Assessment

Attribution: APIGen, APIGen-MT, and ToolACE are material omissions. AgentInstruct, EnvScaler, and WebExplorer are properly included.

Novelty: DIVE has a real novelty boundary: evidence-first collection followed by reverse task derivation from real tool traces. The manuscript should narrow its novelty language to that mechanism, because diverse/verifiable function-calling synthesis and diversity/verification ablations already appear in APIGen and ToolACE.

Baselines: EnvScaler and WebExplorer are reasonable baselines for the L2/L3 benchmark setup. ToolACE and APIGen/xLAM may not be directly runnable across DIVE's benchmark protocols, but they should be discussed as close synthesis antecedents. If feasible, the authors should report whether their trained models can be evaluated under the compatible function-calling subsets, or explain why not.

## Public Comment Basis

The public comment should be narrow and additive: it should corroborate the missing ToolACE/APIGen-family gap, but emphasize the precise novelty distinction rather than repeating broad evaluation concerns already raised by another reviewer.
