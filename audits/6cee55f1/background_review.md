# Background and Novelty Review: Partial Optimality in the Preordering Problem

## Summary of Contribution
The paper introduces new partial optimality conditions (persistency) for the Maximum Value Preordering Problem, generalizing existing conditions from clustering (multicut) and comparability editing. Specifically, it provides directed-graph/dicut versions of the criteria introduced by Lange et al. (2019) and generalizes the state-of-the-art preordering persistency rules from Böcker et al. (2009).

## Three-Axis Assessment

### 1. Attribution
The paper accurately identifies and cites the foundational works in the field, including Wakabayashi (1998) for the problem statement, Böcker et al. (2009) for the previous state-of-the-art in partial optimality, and Shekhovtsov (2013; 2014) for the "improving maps" technique. It also correctly positions itself relative to the authors' own recent work on linear ordering (Stein & Andres, 2024).

### 2. Novelty
The theoretical extension from undirected multicut criteria (Lange et al., 2019) to directed preordering (Theorems 6.2 and 6.6) is a non-trivial contribution. The authors also provide a strict generalization of the conditions from Böcker et al. (2009) via a new fixation condition (Theorem 6.7). The work represents a clear step forward for the preordering problem.

### 3. Baselines
The paper compares its new conditions against the generalized conditions of Böcker et al. (2009) (formulated as Theorem 6.9). However, there is a notable omission in the empirical evaluation on social network data (Section 8.2):
- The social network instances (Twitter/Google+) are constructed with unit costs ({ab} \in \{-1, 1\}$), making them instances of the **Transitivity Editing** problem.
- The authors explicitly cite **Weller et al. (2012)** ("On making directed graphs transitive") for establishing "additional conditions specific to this problem" (transitivity editing).
- Despite this citation, the authors do not include Weller's specific data reduction rules as baselines in their evaluation of the social network benchmarks. Since these benchmarks fall exactly into the discrete domain where Weller's rules apply, they constitute an obvious and necessary baseline for assessing the added value of the new generalized conditions in this specific application.

## Decision Rule
**Comment recommended.** The omission of the Weller et al. (2012) baseline in the social network experiments—despite its explicit mention in the related work as being specific to that problem class—is a significant oversight in an otherwise strong empirical evaluation.
