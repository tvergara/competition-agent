# Background Review: EnterpriseLab

Paper: `45341e1a-1269-40fa-805e-1aef13c24e60`

This audit focuses only on closest-neighbor attribution and novelty boundaries. I read EnterpriseLab together with the following nearby prior works:

- WorkArena, arXiv:2403.07718
- WorkArena++, arXiv:2407.05291
- AgentInstruct, arXiv:2407.03502
- ToolACE, arXiv:2409.00920
- TheAgentCompany, arXiv:2412.14161
- Graph2Eval, arXiv:2510.00507

## Paper Claim Being Audited

EnterpriseLab claims a closed-loop platform for enterprise agents: MCP-backed enterprise tool integration, automated trajectory synthesis from environment schemas, model training through SFT/DPO/Agentic GRPO, and continuous evaluation/adaptation. EnterpriseArena instantiates this platform with 15 MCP servers and 140+ tools across enterprise domains.

## Neighbor Comparisons

### WorkArena and WorkArena++

EnterpriseLab cites WorkArena and correctly identifies one important difference: WorkArena is centered on ServiceNow UI tasks, while EnterpriseArena is a multi-application MCP/tool environment. However, the paper does not cite WorkArena++, which is the more relevant successor for the "complex enterprise workflow" claim. WorkArena++ expands WorkArena from 33 tasks to 682 compositional enterprise tasks requiring planning, retrieval, logical/arithmetic reasoning, data-driven decisions, and infeasibility detection. It also describes a mechanism for generating new workflows by composing lower-level oracle/validator functions.

This does not erase EnterpriseLab's contribution, because EnterpriseLab's MCP/API setting and trainable trajectory synthesis are different from WorkArena++'s browser/UI benchmark. But WorkArena++ is close enough that a novelty discussion should compare against it directly.

### AgentInstruct

AgentInstruct is not cited. It is not an enterprise-environment paper, but it is a close antecedent for the synthetic-data part of EnterpriseLab. AgentInstruct uses agentic flows to create post-training data across skills, including tool/API-use flows that synthesize API lists from code or API descriptions and then generate single- and multi-API tasks.

EnterpriseLab's stronger distinction is that it generates tasks from executable environment-exposed MCP schemas and can feed those trajectories into environment-specific training. The manuscript should make that distinction explicitly rather than presenting schema/API-driven tool-use data synthesis as if the closest antecedents were only ToolACE and Graph2Eval.

### ToolACE and Graph2Eval

Both are cited. ToolACE is also used as a baseline. The paper's distinction from ToolACE is plausible: ToolACE builds a broad function-calling dataset from an API pool with self-guided complexity and dual-layer verification, whereas EnterpriseLab grounds generation in a deployable enterprise environment. Graph2Eval is relevant for automated agent-task generation from structured graphs, but is less enterprise-specific than WorkArena++ or TheAgentCompany.

### TheAgentCompany

TheAgentCompany is cited and appears in Table 7, but the comparison under-characterizes it. TheAgentCompany is a self-contained workplace benchmark with internal web services and data, simulated coworkers through RocketChat, GitLab/project-management/file-storage style workflows, long-horizon professional tasks, and execution/checkpoint-based evaluation. It therefore already covers several properties that EnterpriseArena presents as distinctive: workplace realism, multiple services, cross-platform workflows, and enterprise-style communication.

The real distinction is not simply that EnterpriseArena is "multi-application enterprise orchestration"; it is that EnterpriseArena exposes these workflows through MCP/tool APIs and couples them to automatic trajectory synthesis and training. The paper would be stronger if Table 7 and the related work framed this narrower distinction.

## Three-Axis Assessment

Attribution: WorkArena, ToolACE, Graph2Eval, EnterpriseBench, CRMArena, tau-Bench, and TheAgentCompany are cited. WorkArena++ and AgentInstruct are missing. TheAgentCompany is cited but not compared at the right level of detail.

Novelty: EnterpriseLab is not a simple restatement of one prior work. The platform integration is meaningful. However, the manuscript overstates the novelty boundary if read as claiming unique multi-application enterprise orchestration or unique schema-driven tool-use data synthesis. Those pieces have close antecedents.

Baselines: I do not think WorkArena++ or TheAgentCompany must be direct numerical baselines, because the interaction interfaces differ. But they are necessary design comparisons. AgentInstruct should be discussed as a synthesis antecedent, even if it is not directly runnable as a benchmark baseline.

## Public Comment Basis

The public comment should focus narrowly on:

1. Add WorkArena++ to the related work and explain how EnterpriseArena differs from compositional ServiceNow enterprise workflows.
2. Add AgentInstruct to the synthesis discussion and clarify what is new about environment-exposed MCP schema generation.
3. Revise the TheAgentCompany comparison so the novelty claim centers on MCP/tool-based trainable synthesis, not merely multi-application workplace orchestration.
