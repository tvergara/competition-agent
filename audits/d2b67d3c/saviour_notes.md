# Saviour Notes: d2b67d3c

This paper studies why increasing training-time reasoning length can improve OOD generalization under outcome-only supervision after ID performance saturates.

Observation 1: The RL experiment does not use the original Polynomial Roots task unchanged: the appendix says the original was too difficult for the Qwen2.5-1.5B model at 0% accuracy, so the authors construct a custom largest-rational-root variant for ID training and evaluate OOD on Mixed Operation.

Observation 2: The RL setting is small and controlled: both ID and OOD datasets have 900 training and 100 validation examples, Qwen2.5-1.5B-Instruct is trained with GRPO for 4 epochs / 224 steps, batch size 16, 16 generations per prompt, learning rate 3e-6, on 4 A6000 GPUs.

Observation 3: The conclusion explicitly limits the claim: the theory and experiments do not rule out natural shortcuts that persist under self-iteration but are not strongly discouraged by the regularizer, in which case longer training-time reasoning may not yield OOD gains.
