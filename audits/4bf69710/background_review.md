# Background review: SpreadsheetArena

Paper: `4bf69710-879e-49f9-be08-6f7450bcb304`

## Summary

I see this as a positive novelty case relative to the closest spreadsheet and preference-evaluation literature. The paper is not merely another spreadsheet manipulation benchmark or another Chatbot Arena clone; it changes both the artifact being evaluated and the evaluation signal.

## Closest prior works checked

1. **SpreadsheetBench** (`arxiv:2406.14991`): a real-world spreadsheet manipulation benchmark with OJ-style evaluation across multiple spreadsheet test cases. It evaluates whether agents transform existing spreadsheets correctly.
2. **SheetAgent / SheetRM** (`arxiv:2403.03636`): an LLM spreadsheet agent and benchmark for long-horizon spreadsheet reasoning/manipulation with checklist-style procedure evaluation.
3. **SpreadsheetCoder** (`ICML 2021`): formula prediction from semi-structured context around a target spreadsheet cell.
4. **NL2Formula** (`arxiv:2402.14853`): natural-language-to-spreadsheet-formula generation with table context.
5. **Chatbot Arena / LMArena** (`arxiv:2403.04132`): blind pairwise preference evaluation and Bradley-Terry/Elo ranking for conversational LLMs.
6. **AI Spreadsheet Benchmark** (`Rows HQ 2025`): an adjacent industry technical benchmark comparing production spreadsheet assistants using Pass@1, Pass@3, dynamic output rate, and latency.

## Attribution

The paper cites the main academic neighbors: SpreadsheetCoder, NL2Formula, SpreadsheetBench, SheetAgent/SheetRM, TableLlama, JSONSchemaBench, Chatbot Arena, and SEAL Showdown. I did not find an academic prior that already combines end-to-end workbook generation with blind pairwise preference voting and feature/expert decomposition.

The one adjacent work I would add is the Rows AI Spreadsheet Benchmark. It is not a peer-reviewed academic baseline, but it is a public 2025 technical benchmark for spreadsheet-native AI assistants and dynamic outputs. It is close enough to deserve a related-work mention, especially because SpreadsheetArena also cares about usable spreadsheet artifacts rather than text-only answers.

## Novelty

The novelty is the combination:

- Compared with SpreadsheetBench and SheetRM, SpreadsheetArena evaluates generated workbook artifacts rather than manipulation of existing workbooks under exact/checklist metrics.
- Compared with SpreadsheetCoder and NL2Formula, it moves from formula-level generation to whole-workbook generation with layout, formatting, formulas, and multi-sheet structure.
- Compared with Chatbot Arena and SEAL-style preference analyses, it applies pairwise preference evaluation to a structured artifact whose spreadsheet-specific features can be extracted and modeled.
- The finance expert study adds a domain-validity check showing that crowd preference and professional spreadsheet standards only partially align.

## Baselines

I do not see a missing academic baseline that makes the contribution redundant. The closest possible addition is contextual rather than fatal: cite or discuss AI Spreadsheet Benchmark and SheetBench-style workflow evaluations to make clear how SpreadsheetArena differs from spreadsheet-assistant/product benchmarks.

## Conclusion

This is a real new evaluation setting. Its closest neighbors each cover one component -- spreadsheet manipulation, formula generation, or arena-style preference ranking -- but not the same combination of end-to-end workbook generation, human preference, feature decomposition, and domain-expert validation.
