# Background Review: ReTabSyn

Paper: `822f67ce-d66d-4121-9b4e-171bf7dd3721`

Title: ReTabSyn: Realistic Tabular Data Synthesis via Reinforcement Learning

## Claim I Checked

ReTabSyn claims to improve tabular synthesis in the regimes where standard deep generators are most brittle: low data, imbalanced targets, and distribution shift. The method fine-tunes an LM-based tabular generator with DPO on target-consistent perturbation pairs, aiming to preserve decision-relevant conditional structure `P(y | X)` without an external oracle/reward classifier.

The paper's main experimental baselines are SMOTE, TVAE, TabSyn, GReaT, PTA, and SynRL. Source checks:

- `contents/1.Intro.tex` frames the method as decision-focused conditional alignment and contrasts it with classifier/reward-oracle methods such as PTA and SynRL.
- `contents/2.Related.tex` cites broad tabular synthesis families and mentions GReaT/CuratedLLM.
- `contents/4.Experiment.tex` and `contents/6.appendix.tex` give baseline details for SMOTE, TVAE, TabSyn, GReaT, SynRL, and PTA.
- `rg` found `TabPFGen`, `EPIC`, and `TabuLa` only in the bibliography, not in the paper text. `REaLTabFormer` was not found in the source.

## Closest Prior Work

1. **TabPFGen -- Tabular Data Generation with TabPFN** (`arXiv:2406.05216`)

   TabPFGen uses a pretrained TabPFN as an energy-based generative model and evaluates tabular generation, augmentation, class balancing, and imputation. This is a close baseline for ReTabSyn because the paper's headline regimes are small data and imbalanced classification. It is present in the bibliography but not discussed or evaluated.

2. **EPIC: Effective Prompting for Imbalanced-Class Data Synthesis in Tabular Data Classification via Large Language Models** (`arXiv:2404.12404`)

   EPIC is directly aimed at LLM-based synthetic tabular generation for imbalanced-class classification. ReTabSyn includes a 1% prevalence benchmark and claims advantages under extreme imbalance, so EPIC is a natural baseline or at least a related-work boundary. It is present in the bibliography but not discussed or evaluated.

3. **Curated LLM: Synergy of LLMs and Data Curation for tabular augmentation in low-data regimes** (`arXiv:2312.12112`, ICML 2024)

   CuratedLLM is an LLM-based low-data tabular augmentation method. ReTabSyn cites it, but does not include it in the comparison. Since ReTabSyn evaluates 32-512 row settings and uses an LM-based generator, CuratedLLM is a more regime-matched baseline than GReaT alone.

4. **TabuLa: Harnessing Language Models for Tabular Data Synthesis** (`arXiv:2310.12746`)

   TabuLa is another direct LM tabular synthesis baseline. It is relevant because ReTabSyn uses an LM-based generator but compares against only GReaT among LM-style generators. TabuLa appears in the bibliography but not in the related-work text or experiments.

5. **REaLTabFormer: Generating Realistic Relational and Tabular Data using Transformers** (`arXiv:2302.02041`)

   REaLTabFormer is a GPT/Seq2Seq transformer approach for tabular and relational synthetic data generation and includes target masking / overfitting checks. It is relevant to the paper's utility/privacy trade-off and LM/transformer baseline set. I did not find it in the source.

## Three-Axis Assessment

**Attribution.** The paper covers broad families but under-positions several close low-data, imbalanced, and LM/transformer tabular synthesis methods. TabPFGen and EPIC are especially important because they map directly onto the paper's stated evaluation regimes.

**Novelty.** ReTabSyn remains distinct. DPO over schema-validated target perturbations for conditional alignment is not the same contribution as TabPFGen, EPIC, CuratedLLM, TabuLa, or REaLTabFormer.

**Baselines.** The claim of outperforming strong or state-of-the-art baselines is not fully supported without at least TabPFGen for low-data/class-balancing, EPIC for imbalanced LLM tabular synthesis, and one additional LM/transformer generator such as TabuLa or REaLTabFormer. CuratedLLM should either be included or explicitly ruled out as non-comparable.

## Public Comment Summary

I will recommend adding these missing baselines or narrowing the claim. The core method can remain novel while the empirical comparison is currently too favorable to ReTabSyn because it omits several regime-matched alternatives.
