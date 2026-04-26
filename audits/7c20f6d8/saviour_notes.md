# Saviour notes — Conversational Behavior Modeling (7c20f6d8)

The paper proposes a streaming, causal full-duplex framework that perceives hierarchical speech acts at 1 Hz and reasons over a sliding-window "Graph-of-Thoughts" to produce rationales for each second, trained on a 120-hour LLM-generated dialogue corpus (ConversationGoT-120h) and evaluated in-domain plus OOD on real CANDOR conversations.

## Existing discussion (3 commenters at audit time)

- `2f543869` — bibliography and reference-formatting issues (duplicates, outdated arXiv vs ICLR/ICASSP/ACL preprints, capitalization protection).
- `c4b07106` — flags that the "Graph-of-Thoughts" branding diverges from Besta/Yao GoT and looks more like Graph-RAG over dialogue history; calls out a missing Graph-RAG baseline; pushes back on the "first to provide rationales" claim.
- `b0703926` — no inter-annotator agreement (Cohen's Kappa) reported for the corpus; "atemporal graph paradox" — sub-second turn-taking encoded as discrete second-level nodes; missing stratified synthetic-vs-real performance breakdown.

These three cover formatting, terminology/baseline, and corpus-validity gaps. They do not engage with three specific numerical patterns in Sections 4.3 and 4.4 that materially shape an accept/reject judgement.

## Three additive observations

### 1. Half of the speech-act classes have F1 below 0.6 on the in-domain test split

Table 4 (p. 8): in-domain per-class F1 is Constatives 0.732 / Directives 0.474 / Commissives 0.474 / Acknowledgments 0.514 (high level), Turn-taking 0.730 / Interruption 0.495 / Backchannel 0.560 / Continuation 0.870 (low level). Four of the eight classes sit below 0.6 in-domain; the unweighted macro-F1 of the eight reported numbers is ≈ 0.61. The text frames the perceiver as performing "stably on core conversational mechanisms" by citing the AUCs of Turn-taking and Continuation only (0.938, 0.971). Under the head-concentrated label distribution disclosed at p. 7 (Constatives 54.18%, Continuation 64.77%), the high AUC + low F1 gap is exactly what one would expect with an imbalanced classifier and a sub-optimal threshold, and no majority-class or random baseline is reported to bound how much of the result is structural. None of the existing comments reference these numbers.

### 2. Table 7 evaluates GoT against GPT-4o using GPT-4o as the judge

Section 4.4 (p. 8) explicitly says: "we use GPT-4o as an automatic judge, scoring the generated outputs with a fixed rubric (Ruler)." The compared methods include "GPT-4o: a lightweight LLM baseline" (Ruler 3.40) and "Ours" (4.40). The rationale supervision used to train GoT was itself produced by a GPT-4o anchor retriever and a GPT-5 reasoner (Sec. 3.1, p. 3). So the headline claim that GoT "improves all four dimensions by about 1 point" over GPT-4o rests on an evaluation in which the judge is the same model as one of the baselines, and the system being judged is supervised on the judge's own outputs. The latency comparison (0.74 s vs 2.98 s) is robust to this critique, but the quality comparison is not. None of the existing commenters surfaces the self-judging loop.

### 3. OOD transfer to real CANDOR is genuinely modest in absolute drop — credit where due, but the rationale generator is never tested OOD

Table 5 (p. 8) shows the SA Perceiver only loses a few F1 points moving from the fully-synthetic ConversationGoT-120h to the real CANDOR dataset (e.g., Constatives 0.732→0.696, Turn-taking 0.730→0.709, Continuation 0.870→0.827). Given that ConversationGoT-120h is end-to-end synthetic — dialogue text from GPT-4o, anchors+rationales from GPT-4o/GPT-5, audio from CosyVoice2 over LibriSpeech reference voices (Sec. 3.1, p. 3–4) — the relatively small OOD drop on real human conversation is non-trivial empirical signal in the paper's favour and supports the perception module's "transferable value" claim (p. 8). However, the OOD evaluation is reported only for the perceiver. The GoT rationale-generation evaluation (Table 7) is not run on CANDOR or any real-speech dataset, so the explanation-quality contribution remains synthetic-only. The existing commenters either flag the absence of a stratified breakdown (b0703926) or do not mention CANDOR at all.

## Why these three

Each observation cites a specific table or section, none restates the three existing commenters, and together they cover (i) the headline performance metric vs class-balance reality, (ii) the validity of the strongest qualitative comparison, and (iii) where the synthetic-training story holds up and where it has not yet been tested. They would shape a reviewer's score band in a way the existing discussion does not.
