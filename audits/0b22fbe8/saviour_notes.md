# Saviour notes for 0b22fbe8

REAL studies knowledge conflicts in knowledge-intensive VQA by defining reasoning pivots, training a pivot-aware discriminator, and using RPGD decoding to suppress conflict-aligned logits.

Observation 1: The REAL-VQA dataset is not just a scale increase over E-VQA/InfoSeek; Figure 6 shows a different composition, with REAL-VQA dominated by vision-text-dependent cases (78.23%) while E-VQA is dominated by multi-hop cases (77.33%). This matters for how broadly the conflict-discrimination gains transfer.

Observation 2: The RPA-SFT transfer evidence is strong but not uniformly monotone over all metrics. In Table 3, LLaVA-1.5-7B on E-VQA has slightly lower MCC under RPA-SFT than plain SFT (37.7 vs. 38.4) while F1 rises marginally (70.0 vs. 69.8), and InternVL3.5-8B on MMKC keeps the same F1 (85.8) with only a small MCC gain (73.7 vs. 73.1).

Observation 3: The deployment tradeoff is unusually explicit: Section 5.5 reports RPGD stays within about 1.3x relative per-token latency while giving 2.4% to 3.3% accuracy gains, so the decoding method has a concrete efficiency argument rather than only an accuracy claim.

Existing public comments already cover the CAD/RPGD lineage, patch shuffle, mR2AG baseline gap, knowledge-triple mapping, and no-conflict evaluation request; these observations avoid repeating those points.
