# Saviour Notes: 75c4a4bd

This paper proposes PENCIL, a BERT-style Transformer over sampled link-centric subgraphs for link prediction.

Observation 1: The appendix ablation shows that the method is not just input encoding plus a plain encoder: removing the multiplicative residual drops Cora MRR from 42.23 to 34.64, PubMed MRR from 38.28 to 21.49, and ogbl-collab H@50 from 66.88 to 53.43.

Observation 2: The HeaRT result on ogbl-ppa has a special evaluation caveat: because customized negatives per positive edge are computationally prohibitive, the paper uses one negative link per positive link and reuses the optimal checkpoint from the original benchmark setting.

Observation 3: The runtime appendix is more nuanced than the batching-efficiency framing: with identical sampling, GAT is faster than PENCIL on PubMed, while PENCIL is comparable on ogbl-collab despite using roughly 7-8x more parameters.
