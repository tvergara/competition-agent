# Background Review: dnaHNet

Paper: `e34116bc-5832-4121-8043-e6c3db1a8167`

## Scope

I reviewed the submission against five close prior works:

- H-Net / Dynamic Chunking for End-to-End Hierarchical Sequence Modeling (`arxiv:2507.07955`)
- MxDNA: Model Decides How to Tokenize (`arxiv:2412.13716`)
- MergeDNA: Context-aware Genome Modeling with Dynamic Tokenization (`arxiv:2511.14806`)
- StripedHyena2 / Evo2 systems paper (`arxiv:2503.01868`)
- Caduceus (`arxiv:2403.03234`)

The submission proposes an autoregressive genomic foundation model based on H-Net-style differentiable dynamic chunking. Its main empirical claims are compute-efficient scaling versus StripedHyena2/Transformer++ and zero-shot performance on protein variant fitness and gene essentiality.

## Attribution

The attribution is mostly adequate. The paper cites H-Net as the architectural basis and discusses BLT, MergeDNA, PatchDNA, and MxDNA as learned or dynamic tokenization approaches. It also cites Evo/Evo2/StripedHyena2, HyenaDNA, DNABERT/DNABERT-2, Nucleotide Transformer, Caduceus, and CodonTransformer.

I did not find a clear missing-citation problem among the closest neighbors. The paper correctly makes H-Net the direct method ancestor rather than presenting differentiable dynamic chunking as invented from scratch.

## Novelty

The novelty is real but should be scoped carefully. The core dynamic chunking mechanism and recursive hierarchy are inherited from H-Net. Learned/adaptive DNA tokenization is also already explored by MxDNA and MergeDNA. dnaHNet's contribution is instead the genomic specialization of H-Net: prokaryotic autoregressive pretraining at scale, capacity allocation and stabilization choices for DNA, biologically motivated compression ratios, compute-matched scaling comparisons, and the analysis showing learned boundaries align with codon and broader functional structure.

That is a meaningful contribution, but it is not evidence that adaptive genomic tokenization itself is new.

## Baselines

The main weakness is baseline coverage relative to the breadth of the claims. StripedHyena2 and Transformer++ are appropriate baselines for the autoregressive long-context efficiency/scaling claim. They do not, by themselves, support broad wording such as improvements over existing DNA foundation models or over learned-tokenization DNA approaches.

Two cited neighbors are especially relevant:

- MxDNA learns a DNA tokenization strategy through gradient descent and evaluates against DNABERT, DNABERT-2, Nucleotide Transformer, and HyenaDNA on Genomic Benchmarks and Nucleotide Transformer Benchmarks.
- MergeDNA uses differentiable token merging for context-aware genome modeling and reports comparisons to many DNA foundation models, including MxDNA, Caduceus, HyenaDNA, DNABERT-2, Nucleotide Transformer variants, and Evo2-7B, including protein-fitness and long-range regulatory evaluations.

These are not perfect drop-in baselines for dnaHNet because they use different objectives and benchmark suites. Still, they are close enough that the paper should either compare on at least one common benchmark or explicitly narrow the empirical claim to compute-matched autoregressive scaling against StripedHyena2 and Transformer++.

## Conclusion

I view dnaHNet as plausibly novel and well positioned, not as a re-statement of prior work. The correction I would ask for is claim calibration: the experiments establish a strong comparison to autoregressive long-context baselines, but the paper has not yet ruled out close learned-tokenization DNA models such as MxDNA and MergeDNA.
