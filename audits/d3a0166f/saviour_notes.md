C-kNN-LSH is a nearest-neighbor framework for sequential counterfactual inference, applied here to Long COVID recovery trajectories.

- **Observational Frequency**: In the 13,511-participant RECOVER cohort, each individual contributes between 4 and 8 intermittent PASC severity measurements over a 6-month follow-up period (Section 5.1).
- **Multivalued Treatment Definition**: The treatment variable {i,t}$ is modeled as the cumulative number of vaccine doses received (ranging from 0 to 6) prior to the outcome measurement, rather than a binary indicator (Section 5.2).
- **Baseline Feature Engineering**: The Outcome Regression (OR) baseline uses TF-IDF features extracted from serialized structured textual history representations to perform its conditional mean estimations (Section 5.4).
