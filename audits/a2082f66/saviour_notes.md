This paper builds a large molecule-to-language description dataset by extending OPSIN metadata and using LLM generation plus hybrid validation.

Observation 1: The strongest positive evidence not yet foregrounded in the discussion is the metadata ablation in `data_validation.tex`: with enriched metadata and atom-match passing, precision is 1925/1953 (98.6%), while removing metadata but keeping atom-match passing gives 1761/1871 (94.1%); the hard split drops from 178/185 (96.2%) to 142/172 (82.6%).

Observation 2: The dataset scope is narrower than "PubChem at scale": construction starts from 200,000 sampled PubChem molecules, then excludes entries without IUPAC names, disconnected components, OPSIN warnings/errors, and OPSIN-vs-PubChem SMILES mismatches before generation, leaving 167,416 candidates.

Observation 3: The headline 98.6% precision is explicitly conditional on samples that pass the atom-count filter; the ablation reports that 97.7% pass this filter, while the filtered-out 47/2000 subset has only 13/47 valid descriptions (27.7%), so the filter is doing substantial quality control rather than merely a bookkeeping check.
