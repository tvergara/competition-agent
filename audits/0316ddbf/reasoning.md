# Citation Integrity Audit: 0316ddbf

Paper: Self-Attribution Bias: When AI Monitors Go Easy on Themselves

Audited at: 2026-04-25T22:50Z

Verifier command:

```bash
uv run python tools/verify_citations.py \
  --paper-id 0316ddbf-c5a0-4cbe-8a86-9d6f31c58041 \
  --out audits/0316ddbf/citation_audit.json
```

Report summary:

- Total bibliography entries: 59
- Verified: 31
- Not found in both Semantic Scholar and OpenAlex: 14
- Metadata mismatch: 6
- Ambiguous: 3
- Skipped non-academic/source entries: 5
- Tool errors: 0

The public comment should not flag model cards, company launch posts, Hugging Face datasets, or old psychology papers merely because academic indices miss them. I excluded entries such as Anthropic/OpenAI/Google model-card style citations, `mather2000choice`, and dataset-like records from the fabrication count.

## Confirmed fabrication candidates

I treated the following four references as confidently fabricated enough to surface:

1. `li2024`
   - Raw title: "Systematic Biases in LLM-as-a-Judge Evaluations"
   - Raw authors: Ming Li, Wei Zhang, Xinyi Chen, others
   - Year: 2024
   - Verifier status: `not_found`
   - Reasoning: neither Semantic Scholar nor OpenAlex found a matching work. Exact web search for the title plus the named author combination did not locate an independent paper record. The title and placeholder-style author list resemble a generic invented LLM-as-judge citation.

2. `wang2024a`
   - Raw title: "Position Bias in Large Language Model Evaluations"
   - Raw authors: Zhen Wang, Yan Liu, Rahul Kumar, others
   - Year: 2024
   - Verifier status: `not_found`
   - Reasoning: neither Semantic Scholar nor OpenAlex found a matching work. Exact web search for the title plus the named author combination did not locate an independent record. There are real papers on position bias in LLM judges, but not this title-author combination.

3. `koo2023`
   - Raw title: "Do Language Models Rate Their Own Outputs More Favorably? Measuring Self-Bias in LLM Evaluation"
   - Raw authors: Jiyoung Koo, Sungho Park, Hyunji Kim, others
   - Year: 2023
   - Verifier status: `not_found`
   - Reasoning: neither Semantic Scholar nor OpenAlex found a matching work. Exact web search surfaced this submission's own PDF/reference context rather than an independent publication. The cited arXiv-like reference shown in the paper context appears placeholder-style, not a resolvable paper.

4. `liu2023b`
   - Raw title: "Self-Preference in Large Language Models: When Models Favor Their Own Outputs"
   - Raw authors: Zihan Liu, Yiming Zhao, Hao Chen, others
   - Year: 2023
   - Verifier status: `not_found`
   - Reasoning: neither Semantic Scholar nor OpenAlex found a matching work. Exact title/author web search did not locate an independent publication. The subject overlaps real self-preference work, but this specific title-author tuple appears unsupported.

## Borderline entries not surfaced

- `sharma2025understandingsycophancylanguagemodels`: real work found with year metadata drift around arXiv 2310.13548; not a fabrication.
- `anthropic2024claude35haiku`, `anthropic2025claude4`, `anthropic2025claude41opus`, `openai2025gptoss`, `openai2025gpt5`, `openai2025gpt5developers`, `gemini2024family`, `gemini2025technical`: product/model-card style citations; the verifier is not well calibrated for company web pages and model cards.
- `mather2000choice`: real psychology paper, likely missed due to title punctuation or index coverage.
- `agentlans2023redditethics`, `noddybear2024unanswerable`, `noddybear2025computeruse`: dataset-like records; not reliable fabrication signals.
- `hubinger2024scheming`, `carlsmith2023collusion`, `kenton2021alignment`, `bowman2022failure`: broad AI-safety/blog-report style entries where absence from academic indices is not sufficient for a public fabrication claim without more checking.

Decision: post one comment because at least four entries meet the confirmed-fabrication threshold.
