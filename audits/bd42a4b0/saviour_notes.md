# Saviour notes for bd42a4b0

CF-HyperGNNExplainer adapts counterfactual explanation optimization to hypergraph neural networks by learning structural deletion masks over incidence entries or whole hyperedges.

Observation 1: The two variants encode genuinely different intervention granularities: NHP removes individual node-hyperedge incidences, while HP removes whole hyperedges within the target node's neighborhood. Table 1 shows NHP is stronger on Cora/CiteSeer accuracy (0.720/0.727 vs. 0.647/0.613), while HP is slightly stronger on PubMed (0.524 vs. 0.506), so the choice is not merely cosmetic.

Observation 2: The explainer is highly sensitive to optimizer hyperparameters in the ablations. On Cora NHP, Table 3 reports accuracy dropping from 0.720 to 0.453 when the learning rate changes from 0.1 to 0.01, and Table 4 reports a similar drop from 0.720 to 0.454 when momentum changes from 0.9 to 0.

Observation 3: The runtime advantage depends materially on the sparse COO implementation, not just the counterfactual objective. Table 5 reports NHP at 19.630 seconds in the dense implementation versus 3.299 seconds in the sparse one, and HP at 6.282 seconds dense versus 3.190 seconds sparse.

Existing comments already cover the narrow citation-network scope, single HGNN architecture, PubMed degradation, fixed threshold, missing code/artifacts, omitted random baseline, and normalization-coupling concern; the observations above avoid repeating those points.
