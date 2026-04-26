# Saviour Notes: 6008e765

This paper derives a data-limited language-model scaling exponent from conditional-entropy decay and token-correlation decay in natural-language corpora.

Observation 1: The conditional-entropy exponent gamma is not estimated from raw n-gram counts; the paper says direct count estimation is infeasible at the vocabulary sizes and horizons used, so it estimates gamma from trained autoregressive model losses treated as increasingly tight upper bounds.

Observation 2: The empirical scope is controlled but small relative to frontier scaling: all experiments use TinyStories and WikiText-103 tokenized with BPE vocabulary 8192; GPT-2-style runs use a 98M base model and up to 600M parameters for WikiText, while LLaMA-style runs use reduced LLaMA-3.2-1B variants.

Observation 3: The training appendix reports real tuning effort but not exhaustive search at the largest data sizes: it grid-searches learning rate, weight decay, epochs, and batch size where feasible, then aims for local optimality because exhaustive tuning becomes too costly.
