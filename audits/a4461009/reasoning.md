# Citation Integrity Audit: a4461009

I ran an automated citation audit on the bibliography of this paper. Out of 82 entries, 61 were verified. I identified one confirmed fabrication/hallucination where a real paper title was assigned to incorrect authors.

## Confirmed Hallucination

- **Mills01021993**: *A mixture-of-experts model for cognitive flexibility* (Mark Mills, Stephen D. D’Souza, Bradley R. Postle; 1993).
  - **Reason**: The paper with this exact title was written by **Robert A. Jacobs** and **Michael I. Jordan** in 1993 (often cited as a technical report or conference paper from that year). While Bradley R. Postle is a real neuroscientist, I could not find any record of this specific collaboration or publication in 1993. This appears to be a hallucinated attribution.

## Suspicious Entries

- **openai2025gpt5systemcard**: *Openai gpt-5 system card* (Singh, Aaditya, et al.; 2025).
  - **Note**: While GPT-5 is a real entity in the 2025-2026 timeline, the author list for this entry is strictly alphabetical by first name (Aaditya, Adam, Adam, Adam, Adi, Ahmed, Aidan, Aiden, AJ, Akhila), which is highly anomalous for an official system card and suggests an automated or placeholder author list.

Full audit data: [citation_audit.json](./citation_audit.json)
