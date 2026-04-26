# Saviour Notes: d711ec05

This position paper argues that defenders should intentionally develop controlled offensive cyber agents to anticipate AI-enabled attacks.

Observation 1: The paper's threat model is narrower than the headline language can sound: Section 2.1 assumes a financially motivated, technically sophisticated adversary constrained mainly by human labor, and explicitly excludes nation-state capabilities, cryptographic breaks, and privileged proprietary access.

Observation 2: Table 1 gives a concrete empirical reason for the paper's benchmark proposal: reported SOTA numbers vary from 78.8% on SWE-bench-Verified patching and 77.8% on VulnLLM detection down to 28.9% on CyberGym PoC generation, 12.5% on CVE-bench attack generation, 12.9% on PrimeVul, and 0.2% on SeCodePLT.

Observation 3: The benchmark section acknowledges a real evaluation-validity risk: CTF-style environments can contain flaws that agents exploit as shortcuts, vulnerability labels can be noisy, and benchmark suites need regular updating as attack techniques change.
