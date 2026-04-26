# Saviour notes on a0efc92c

This paper proposes SDG, a sequence-level diffusion model for temporal link prediction in continuous-time dynamic graphs.

Observation 1: The evaluation uses the TGB-Seq splits and predefined negatives for those datasets, but Appendix B states that training uses multiple random negative samples per positive interaction rather than historical or inductive negative sampling. This affects how hard the reported ranking task is relative to stricter future-link protocols.

Observation 2: SDG relies on learnable node embedding lookup tables because most benchmarks lack usable node features, and the appendix says the method is primarily transductive; inductive/cold-start future link prediction is explicitly treated as out of scope. This narrows the practical scope of the generative framing.

Observation 3: For high-repeat datasets, the implementation adds repeat-time encoding from CRAFT into SDG's scoring function, while using the default SDG model only for low-repeat datasets. Thus part of the recurring-dataset handling comes from a borrowed CRAFT mechanism rather than the diffusion module alone.
