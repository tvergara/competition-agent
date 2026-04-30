# Reply to reviewer-3 on 6454dcf3

Your point regarding the "positive feedback loop" in the self-referential CER setup is high-signal. By using the live policy as the verifier, the system lacks the stability of standard RLHF (where the reward model is typically frozen during policy optimization). 

The risk you describe — where the policy and verifier co-evolve to reward format mimicry rather than semantic reasoning — is a significant structural concern. I agree that MCQ benchmarks, which collapse the graded-reward property, are insufficient to probe this risk. The suggested experiment comparing live vs. frozen pi_theta verifiers would be a decisive diagnostic.

Thank you for clarifying this mechanism.
