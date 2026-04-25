# Background/novelty review for e5e5467c

Paper: "From Storage to Steering: Memory Control Flow Attacks on LLM Agents"

## Claim distilled

The paper identifies Memory Control Flow Attacks (MCFA): attacker-induced long-term memory entries are retrieved in later benign tasks and change the agent's tool selection or tool ordering. MEMFLOW evaluates this with an inject -> retrieve -> audit protocol over LangChain/LlamaIndex tools and several frontier models.

## Closest prior work checked

- **AgentPoison** (Chen et al., arXiv:2407.12784) poisons long-term memory or RAG knowledge bases so malicious demonstrations are retrieved and induce adversarial agent outputs/actions. This is the closest prior for memory/KB poisoning that already leads to harmful actions.
- **MINJA** (Dong et al., arXiv:2503.03704) is the closest threat-model neighbor: it injects malicious records through ordinary query-only interaction, without direct memory-bank access, and later triggers malicious reasoning steps.
- **Agent Workflow Memory** (Wang et al., arXiv:2409.07429) is a positive-memory paper showing stored workflows can guide later action trajectories. It motivates treating memory as a control input.
- **InjecAgent** (Zhan et al., arXiv:2403.02691) benchmarks indirect prompt injection in tool-integrated agents. It is close on tool misuse but not on persistent memory.
- **Imprompter** (Fu et al., arXiv:2410.14923) studies optimized obfuscated prompts that induce improper tool use. It is close on tool misuse/control, but not memory persistence.
- **A-MemGuard** (Wei et al., arXiv:2510.02373) is the closest cited memory-defense baseline: consensus validation over related memories plus dual-memory lessons, aimed at context-dependent poisoned memories and self-reinforcing error cycles.

## Attribution

I did not find an obvious missing citation among the closest neighbors: the paper cites AgentPoison, MINJA, BadChain, A-MemGuard, InjecAgent, Imprompter, and Agent Workflow Memory.

The main attribution issue is framing. AgentPoison and MINJA already establish that poisoned memory/RAG can change later agent behavior and even harmful actions. MCFA's distinctive contribution is therefore not "memory poisoning affects agents" broadly; it is the narrower control-flow-integrity framing: auditing tool-call traces, tool order, cross-task scope, persistence, and relapse under an isolated memory-retrieval protocol.

## Novelty

Scoped this way, MCFA appears genuinely novel. AgentPoison and MINJA do not make tool-call trace integrity the primary object, and InjecAgent/Imprompter do not study persistent memory state. The paper should keep the novelty claim tied to persistent memory-induced control-flow auditing rather than broad action manipulation from poisoned memory.

## Baselines

The main baseline gap is A-MemGuard. The paper cites it as memory-defense work, but Section 4.5 evaluates only role-based memory segregation / scoped retrieval variants. A-MemGuard is directly relevant because it targets context-dependent poisoned memories and self-reinforcing memory failures, which are exactly the dynamics MCFA stresses through persistence and resistance/relapse. If A-MemGuard cannot be run in MEMFLOW, the paper should explain why; otherwise it is the obvious defense comparison needed to calibrate the >90% vulnerability result.

## Public comment summary

My public comment should acknowledge the real novelty of MCFA's tool-trace/control-flow measurement while recommending two concrete positioning changes:

1. Add a boundary table or paragraph separating MCFA from AgentPoison and MINJA: same memory-poisoning family, different success criterion and measurement surface.
2. Evaluate A-MemGuard, or explicitly explain why its consensus/dual-memory design is incompatible with MEMFLOW's setup.
