# Saviour notes for 8a0d16b0

The paper proposes INSES, a GraphRAG-style method that combines LLM-guided KG traversal, query-time similarity expansion, and a router between naive RAG and graph reasoning.

**Observation 1:** The main MuSiQue/2Wiki/HotpotQA experiments say they use a "standard pipeline" to construct KGs and store them in Neo4j, but the paper does not specify the extraction pipeline used for those KGs; this is more explicit for the MINE benchmark, where KGGEN, GraphRAG, and OpenIE are named.

**Observation 2:** The router is important to the reported system, especially on HotpotQA, where Figure 2 routes about 86% of queries to naive RAG; however Algorithm 2 and Appendix G rely on a multi-hop classifier plus a self-reported confidence threshold without reporting the threshold value or calibration procedure.

**Observation 3:** A useful positive detail in Appendix A is that the MINE robustness setting is not just another aggregate QA table: it quantifies graph topology differences, including OpenIE averaging 189 nodes and 265 edges versus GraphRAG averaging 14 nodes and 13 edges, which supports the claim that INSES is tested across very different KG density regimes.
