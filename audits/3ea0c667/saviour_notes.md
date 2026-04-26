# Saviour notes on 3ea0c667

This paper proposes SymPlex, an RL-trained structure-aware Transformer for discovering symbolic PDE solutions from PDE and boundary-condition residuals.

Observation 1: The non-smooth Hamilton-Jacobi cases are not trained with the same generic residual as the other PDEs; Appendix B replaces the PDE loss for Burgers and Eikonal equations with an implicit characteristic-based loss adapted from Park et al. to bias recovery toward viscosity solutions.

Observation 2: The baseline protocol is stronger than a single-run comparison: SSDE, FEX, and PINN+DSR are each run for 20 independent seeds with the best-MSE expression selected, and the KAN baseline is physics-informed with Adam then L-BFGS on shared collocation/constraint points.

Observation 3: The curriculum is staged and rule-based: Stage 1 excludes time and parameters, Stage 2 adds time with parameters fixed to 1, Stage 3 adds parametric variables, with up to 500 epochs per stage and early progression when reward exceeds 0.99 or after 200 epochs. The appendix visualizes the curriculum-vs-single-stage comparison only for the two parametric PDE examples.
