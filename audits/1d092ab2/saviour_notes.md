# Saviour notes for 1d092ab2

The paper studies parameter-space noise for RLVR, using PSN-GRPO to improve large-budget pass@k on math reasoning while adding truncated importance sampling and adaptive noise control.

Observation 1: The Qwen3-4B-Base appendix result supports generalization but with a small average effect: pass@256 rises from 72.0% to 72.5%, while pass@1 falls from 33.8% to 31.9% and pass@2 falls from 41.5% to 40.5%; the larger gains are concentrated on AIME24 and AIME25.

Observation 2: The appendix does quantify the adaptive scheduler's compute cost: Variant II uses two probe generations per query with G=8 rollouts, estimates a naive 17% slowdown, and reports an observed per-iteration throughput reduction of about 8% relative to fixed-sigma PSN under identical hardware and batch settings.

Observation 3: The detailed adaptive-noise table is not uniformly favorable at low budgets: on AIME 24, PSN Var-II has lower pass@2 and pass@4 than GRPO Train (28.1% vs 30.9%, and 37.1% vs 39.3%) while still improving pass@256 substantially (81.7% vs 72.6%).
