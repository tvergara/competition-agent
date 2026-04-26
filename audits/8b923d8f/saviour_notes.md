# Saviour notes for 8b923d8f

The paper proposes BFS-PO, an RL fine-tuning method that searches for progressively shorter correct reasoning traces by expanding high-entropy points on the current shortest correct path.

**Observation 1:** A useful strength is that the evaluation is not only in-domain: after MATH-500 training, the paper tests transfer to MMLU-STEM, AIME'25, and MINERVA-MATH, and it repeats AIME'25 32 times because the benchmark has only 30 questions.

**Observation 2:** The only BFS-specific hyperparameter is the number of expansions K; the paper ablates K only on GSM8K with Qwen2.5-3B-Instruct, selects K=3, and then keeps it fixed for all other models, datasets, and token budgets.

**Observation 3:** The accuracy improvement is not uniform even when AES improves: in Table 3, BFS-PO is slightly below DAPO on Llama-3.1-8B MATH-500 accuracy (50.6 vs. 50.8) and Qwen2.5-7B MMLU-STEM accuracy (80.7 vs. 80.9), so some gains come from the length side of the trade-off.
