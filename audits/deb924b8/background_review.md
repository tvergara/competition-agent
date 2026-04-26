# Background and novelty audit for deb924b8

Paper: "Analyzing and Improving Chain-of-Thought Monitorability Through Information Theory"

## Claim audited

I audited the paper's central novelty claim: that it gives an information-theoretic account of CoT
monitorability and uses that account to train models so their CoTs remain useful to monitors under
optimization pressure.

## Closest prior work checked

- Baker et al. 2025, "Monitoring Reasoning Models for Misbehavior and the Risks of Promoting
  Obfuscation" (arXiv:2503.11926)
- Korbak et al. 2025, "Chain-of-Thought Monitorability: A New and Fragile Opportunity for AI Safety"
  (arXiv:2507.11473)
- Emmons et al. 2025, "When Chain of Thought is Necessary, Language Models Struggle to Evade
  Monitors" (arXiv:2507.05246)
- Ton et al. 2025, "Understanding Chain-of-Thought in LLMs through Information Theory"
  (arXiv:2411.11984)
- Farquhar et al. 2025, "MONA: Myopic Optimization with Non-myopic Approval Can Mitigate Multi-step
  Reward Hacking" (arXiv:2501.13011)
- Xu et al. 2020, "What Can Neural Networks Reason About?" / predictive V-information
  (arXiv:2002.10689)

## Attribution

The closest neighbors I found are cited. Baker et al. are cited as the key empirical warning that
optimization against a CoT monitor can degrade monitorability through obfuscation. Korbak et al. are cited
for the monitorability agenda. Emmons et al. are cited for the necessity-of-CoT argument. Ton et al. and
Lei et al. are cited as information-theoretic analyses of CoT. Xu et al. are cited in the appendix where the
paper discusses predictive V-information and practical extractor limitations. MONA/Farquhar is also cited
in the reward-hacking/steganography context.

I did not find a materially relevant omitted prior among the close neighbors I checked.

## Novelty assessment

The paper's main contribution appears meaningfully new relative to the closest prior work.

Baker et al. establish the empirical phenomenon: CoT monitors can detect reward hacking, but direct
optimization against the monitor can induce obfuscation. Korbak et al. frame CoT monitorability as a
fragile safety opportunity. Emmons et al. argue that when CoT is necessary for the bad behavior, the
reasoning is more likely to be exposed and monitorable. Ton et al. estimate step-wise information gain to
evaluate reasoning quality.

The submitted paper is doing a different thing: it formalizes monitorability uplift through conditional
mutual information, sharpens the "necessity" story by showing that nonzero CoT-output information is not
sufficient for monitorability, decomposes practical monitor error into an information gap and an elicitation
error, and then uses a conditional-MI proxy as a training signal for preserving monitorability. I did not see
that full package in any of the close prior works.

## Baseline assessment

The experimental comparisons include task reward, task-plus-monitor reward, oracle monitor reward,
conditional-MI reward, and true-reward variants in MBPP and BigMath/Reasoning-Gym style environments.
Given the paper's claim, Baker et al. are the closest empirical reference point and are used appropriately.

MONA is adjacent but not an obvious required baseline: it addresses multi-step reward hacking via myopic
optimization with non-myopic approval, whereas this paper studies preserving the informational content of
CoTs under direct pressure from CoT monitors. A head-to-head comparison could be interesting in future
work, but its absence does not look like a baseline omission for the paper's main claim.

## Bottom line

This looks like a genuinely novel contribution in the CoT-monitorability literature. The novelty is not that
CoT monitors are useful or fragile, nor that information theory can evaluate reasoning steps. The novelty is
the paper's specific formal and empirical bridge between monitorability, extractable information in CoT, and
training objectives that preserve that information under optimization pressure.
