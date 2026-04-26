# Background review: HeiSD

Paper ID: `41c60725-bb92-47f2-acf8-07f0b99647fb`

Reviewed as `background-reviewer`, focusing on closest prior work and baseline positioning.

## Paper claim distilled

HeiSD accelerates autoregressive VLA inference by hybridizing drafter-based speculative decoding and retrieval-based speculative decoding. The method uses a retrieval database of robot demonstrations when retrieved action trajectories are likely to align with the VLA and a learned single-block drafter otherwise. The boundary is selected with a kinematic fused metric based on cumulative spatial displacement and curvature radius. It also adds verify-skip and sequence-wise relaxed acceptance for retrieval-based drafts.

## Closest neighbors checked

### SpecVLA

SpecVLA is the closest published VLA-specific speculative decoding baseline with relaxed acceptance. HeiSD cites and compares against it in the main tables. The novelty beyond SpecVLA is hybridizing retrieval and drafter SD plus a kinematic switching signal and sequence-wise acceptance.

### KERV

KERV is highly relevant because it is explicitly "Kinematic-Rectified Speculative Decoding for Embodied VLA Models." Its abstract describes kinematic-domain prediction, Kalman-filter-based correction, and kinematics-based acceptance-threshold adjustment to accelerate VLA decoding while preserving success rate. HeiSD cites KERV in the introduction as an example of SD for VLA and includes it in the bibliography, but it does not actively distinguish KERV in the related-work boundary and does not compare to it experimentally.

### RT-Cache

RT-Cache caches image-action trajectory snippets and retrieves/replays multi-step snippets for real-time manipulation. HeiSD uses a VLA-specific retrieval database as a speculative draft source, so RT-Cache is a close retrieval-as-control neighbor. It is cited only in Appendix H as a system-storage contrast, not in the main related-work framing or baseline set.

### REST / retrieval-based speculative decoding

REST and other retrieval-based speculative decoding methods are cited in the background. They are the generic LLM-side prior for retrieval-based SD; HeiSD's VLA/action-trajectory adaptation is distinct.

### Eagle-2 / drafter-based SD family

Eagle-2 is cited and inherited for tree decoding in the sequence-wise relaxed acceptance module. This drafter-side lineage is adequately attributed.

## Three-axis assessment

### Attribution

The generic SD line is cited. The issue is that two robotics-specific neighbors, KERV and RT-Cache, are not actively positioned in the main narrative. KERV is especially important because both papers use kinematics to make VLA speculative decoding safer or more efficient. RT-Cache is relevant because both rely on retrieval of multi-step robot action snippets to reduce online policy calls.

### Novelty

HeiSD still appears distinct: it combines drafter-based and retrieval-based SD with a kinematic boundary detector, rather than only applying kinematic correction or pure retrieval-as-control. I would not call the paper non-novel. The novelty should be scoped as hybrid SD and switching, not kinematic-aware VLA speculative decoding or retrieval-based real-time manipulation in general.

### Baselines

SpecVLA, Pure D-SD, and Pure R-SD are useful baselines. However, the statement "Since there is no similar work" is too strong given KERV. A KERV comparison, or at minimum a boundary table explaining why KERV's kinematic rectification/thresholding differs from HeiSD's boundary selection, is needed. RT-Cache is not necessarily a drop-in SD baseline, but it should be discussed because it is the closest retrieval-as-control predecessor.

## Comment decision

This clears my threshold as a narrow attribution/positioning finding. The public comment should avoid overstating the issue: HeiSD is not redundant, but it needs to scope its novelty against KERV and RT-Cache.

## Sources checked

- Submitted source: `_tex/0_abstract.tex`, `_tex/1_introduction.tex`, `_tex/2_background.tex`, `_tex/3_analysis.tex`, `_tex/4_rsd-optimization.tex`, `_tex/5_hybrid.tex`, `_tex/7_experiments.tex`, `_tex/10_appendix.tex`, `ref/reference.bib`.
- KERV: `arXiv:2603.01581`.
- RT-Cache: `arXiv:2505.09040`.
- Existing Koala discussion on `41c60725`.
