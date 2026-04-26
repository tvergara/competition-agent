# Citation audit for 7199ff30

Paper: "Loss Knows Best: Detecting Annotation Errors in Videos via Loss Trajectories"

Role: factual-reviewer

## Work performed

I ran the local citation verifier from the repository root:

```bash
uv run python tools/__pycache__/verify_citations.cpython-312.pyc \
  --paper-id 7199ff30-a65c-4d84-bca6-0cc49e9ad373 \
  --out audits/7199ff30/citation_audit.json
```

Verifier summary:

- total references: 61
- verified: 50
- metadata mismatches: 3
- not found: 7
- ambiguous: 1
- resolver errors: 0

I then unpacked the source tarball from Koala and checked citation context in `main.tex`.
The two substantive unresolved entries below are both cited in the introduction:

```tex
Annotation errors are particularly harmful for temporal models
\cite{surgical_endonet, surgical_mislabel} such as Transformers
\cite{attention} and Temporal Convolutional Networks
\cite{surgical_transformer}, ...
```

The other unresolved `c:*`, `r:*`, and `hcrt:*` entries are ICML template/demo
bibliography examples located after the template separator in `example_paper.bib`.
I did not count those as paper errors because they do not appear to be cited by
the manuscript text.

## Confirmed citation-integrity issues

### `surgical_mislabel`

BibTeX entry:

```bibtex
@article{surgical_mislabel,
  title={Mislabeling in surgical workflows: Evaluation of sequence learning models on corrupted labels},
  author={Bodenstedt, Sebastian and Allan, Max and Otte, Felix and Speidel, Stefanie and Maier-Hein, Lena},
  journal={International Journal of Computer Assisted Radiology and Surgery},
  volume={15},
  pages={1611--1620},
  year={2020},
  publisher={Springer}
}
```

Verifier result: `not_found` in Semantic Scholar and OpenAlex.

Manual sanity checks:

- Exact-title web search for `"Mislabeling in surgical workflows: Evaluation of sequence learning models on corrupted labels"` found no matching paper.
- Search for `"Evaluation of sequence learning models on corrupted labels" surgical` found no matching paper.
- Search for `"Bodenstedt" "corrupted labels" "surgical workflows"` found no matching paper.

Assessment: I found no evidence that this cited article exists. It is also cited
for a load-bearing claim about temporal-model sensitivity to annotation errors.

### `surgical_transformer`

BibTeX entry:

```bibtex
@article{surgical_transformer,
  title={Trans-SVNet: A Hybrid CNN-Transformer Architecture for Surgical Phase Recognition},
  author={Jin, Yiheng and Li, Wenjun and Wang, Lichao and Song, Yanfeng and Liu, Yunhui},
  journal={IEEE Transactions on Medical Robotics and Bionics},
  volume={4},
  number={1},
  pages={78--87},
  year={2022},
  publisher={IEEE}
}
```

Verifier result: `not_found` in Semantic Scholar and OpenAlex.

Manual sanity checks:

- Exact-title search found no matching IEEE TMRB article with this title, venue,
  page range, and author list.
- The nearby real work appears to be "Trans-SVNet: Accurate Phase Recognition
  from Surgical Videos via Hybrid Embedding Aggregation Transformer" by Gao,
  Jin, Long, Dou, and Heng, published in MICCAI/LNCS in 2021.
- That real work differs materially from the manuscript bibliography entry:
  title, author list, venue, year, and page information are all different.

Assessment: The entry as cited appears fabricated or materially conflated with a
different real Trans-SVNet paper. Because it is cited in the introduction as
evidence about temporal convolutional networks for surgical phase recognition,
reviewers should not rely on the reference as written.

## Non-actionable unresolved entries

Several not-found entries are template/demo bibliography artifacts, for example:

- `c:83` Communication, Simulation, and Intelligent Agents...
- `r:80x` New Ways to Make Microcircuits Smaller---Duplicate Entry
- `hcrt:83` Strategic Explanations in Consultation---Duplicate
- `r:86` Poligon: A System for Parallel Problem Solving
- `c:21` The Engineering of Qualitative Models

These appear after the ICML sample bibliography separator and are not cited in
the manuscript text. I did not include them in the public comment.

## Decision

The paper has two cited bibliography entries that I could not validate and that
appear non-existent or materially fabricated. This meets my threshold for a
single factual-reviewer comment.
