# Background Review: VideoAesBench

## Claimed Contributions
The paper introduces **VideoAesBench**, a comprehensive benchmark specifically designed to evaluate the video aesthetics perception capabilities of Large Multimodal Models (LMMs). Key contributions include:
- A dataset of 1,804 videos from 5 diverse sources (UGC, AIGC, RGC, Compression, Gaming).
- 12 fine-grained aesthetics dimensions categorized into three aspects: Visual Form, Visual Style, and Visual Affectiveness.
- Multiple question formats, including the introduction of **Multiple Choice Questions (MC)** for video aesthetics, which require models to identify all relevant aesthetic issues.
- A comprehensive benchmark of 23 state-of-the-art open-source and closed-source LMMs.

## Closest Prior Works and Relations

1. **Q-Bench-Video: Benchmarking the Video Quality Understanding of LMMs** (Zhang et al., 2024)
   - **Relation**: Directly related as it also benchmarks LMMs on video quality.
   - **Comparison**: While Q-Bench-Video includes an "Aesthetic" dimension, it is one of only 4 broad categories (Technical, Aesthetic, Temporal, AIGC). VideoAesBench significantly increases the granularity with 12 specific aesthetic dimensions.
   - **Citation**: Correctly cited as a key predecessor.

2. **AesBench: An Expert Benchmark for Multimodal Large Language Models on Image Aesthetics Perception** (Huang et al., 2024)
   - **Relation**: The image-domain counterpart to the proposed work.
   - **Comparison**: AesBench focuses on image aesthetics with 8 dimensions/perspectives. VideoAesBench extends this to the video domain, introducing temporal-aware dimensions and a more complex MC question format.
   - **Citation**: Correctly cited.

3. **Exploring Video Quality Assessment on User Generated Contents from Aesthetic and Technical Perspectives (DIVIDE-3K)** (Wu et al., 2023)
   - **Relation**: A foundational dataset that established the disentangled aesthetic and technical axes for video quality.
   - **Comparison**: DIVIDE-3K is a human-scored dataset used for training/evaluating traditional VQA models. VideoAesBench uses it as a source of videos but pivots to evaluate the **explainable** perception capabilities of LMMs via QA.
   - **Citation**: Correctly cited.

4. **VADB: A Large-Scale Video Aesthetic Database with Professional and Multi-Dimensional Annotations** (Qiao et al., 2025)
   - **Relation**: A recent large-scale database (10K+ videos) for video aesthetics.
   - **Comparison**: VADB focuses on score regression and language comments for traditional models. VideoAesBench builds upon the multi-dimensional annotation idea but creates a specific benchmark for LMMs with diverse question types.
   - **Citation**: Correctly cited.

5. **Video-Bench: A Comprehensive Benchmark and Toolkit for Evaluating Video-based Large Language Models** (Ning et al., 2023)
   - **Relation**: A foundational general benchmark for video LMMs.
   - **Comparison**: Video-Bench evaluates general understanding and reasoning but lacks a specific focus on low-level perceptual or high-level aesthetic quality.
   - **Citation**: **Not cited**. While VideoMME and MVBench are cited as general benchmarks, Video-Bench is a notable omission from the "Video LMM Benchmarking" lineage.

## Three-Axis Assessment

### 1. Attribution
The paper provides an excellent mapping of its work within the context of recent "Quality/Aesthetics" benchmarks for LMMs (Q-Bench, AesBench, Q-Bench-Video). It correctly identifies the gap between general perceptual quality (distortions) and high-level aesthetics. The omission of `Video-Bench` is minor given the citation of other general benchmarks like `MVBench` and `VideoMME`.

### 2. Novelty
The work is **clearly very novel** in its specific focus and granularity. While `Q-Bench-Video` introduced aesthetics as one of its dimensions, `VideoAesBench` is the first to provide a 12-dimension rubric specifically for video aesthetics in LMMs. The introduction of the **Multiple Choice** format for this task is a significant contribution, as it forces models to demonstrate a more complete understanding of overlapping aesthetic issues rather than just picking a single correct answer.

### 3. Baselines
The paper benchmarks a comprehensive set of 23 LMMs, including the latest models like Qwen3-VL, GPT-5.2, and O3. This scale of evaluation provides a clear picture of the current state of the field. A minor weakness is the **lack of a human baseline** on the final benchmark set, which would help quantify the "room for improvement" mentioned by the authors.

## Overall Verdict
**Very Novel.** VideoAesBench fills a clear and significant gap in the evaluation of Large Multimodal Models by providing the first fine-grained, multi-dimensional benchmark for video aesthetics. Its holistic approach and challenging question formats make it a valuable resource for the community.
