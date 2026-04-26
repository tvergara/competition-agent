# Saviour notes for 27ee28cc

The paper proposes anytime-valid watermark detection based on e-processes and evaluates it on synthetic two-token settings and MarkMyWords long-form generation.

Observation 1: The real-data setup is specific: the experiments watermark Llama2-7B-chat at temperature 0.7, use Phi-3-mini-128k-instruct as the anchor model, evaluate on 300 MarkMyWords outputs across book summarization, creative writing, and news article generation, and report detection size as median tokens over private keys and perturbations at alpha=0.02.

Observation 2: The additional experiments fix generation hyperparameters inherited from the SEAL/Huang comparison setting, namely K=20, |Omega_h|=2, and delta=0.3; the synthetic verification is limited to two-token Bernoulli cases using CLARABEL for log-growth and stopping-time simulations over selected p values.

Observation 3: The temperature table shows a real tradeoff rather than uniform dominance: the method has the best detection size at all three tested temperatures, but quality is 0.909 versus inverse-transform's 0.910 at temperature 0.3, tied at 0.919 at 0.7, and 0.902 versus 0.917 at 1.0.
