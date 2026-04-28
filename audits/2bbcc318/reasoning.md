# Citation Integrity Audit: 2bbcc318

I ran an automated citation audit on the bibliography of this paper using Semantic Scholar and OpenAlex. Out of 169 entries, 153 were verified, but I identified several clear hallucinations that appear to be leftover placeholders from a LaTeX template.

## Confirmed Hallucinations

The following entries use classic placeholder names (e.g., "Alpher", "Gamow", "FirstName LastName") and titles (e.g., "Frobnication", "The frobnicatable foo filter") typical of the CVPR/ICCV LaTeX style guides. These are not real academic publications:

- **Authors14**: *The frobnicatable foo filter* (FirstName LastName; 2014)
- **Authors14b**: *Frobnication tutorial* (FirstName LastName; 2014)
- **Alpher02**: *Frobnication* (FirstName Alpher; 2002)
- **Alpher03**: *Frobnication revisited* (FirstName Alpher, FirstName Fotheringham-Smythe; 2003)
- **Alpher04**: *Can a machine frobnicate?* (FirstName Alpher, FirstName Fotheringham-Smythe, FirstName Gamow; 2004)
- **Alpher05**: *Can a computer frobnicate?* (FirstName Alpher, FirstName Gamow; 2005)

These placeholder citations indicate that the final bibliography was not properly cleaned before submission.

Full audit data: [citation_audit.json](./citation_audit.json)
