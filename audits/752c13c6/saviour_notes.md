# Saviour notes for 752c13c6

This paper argues that frozen modern vision foundation model features plus a linear classifier are a stronger default for AI-generated image detection than specialized forensic detector designs.

Observation 1: The claimed simplicity is backed by a genuinely minimal training protocol: all modern VFM baselines use only GenImage Stable Diffusion v1.4 training data, freeze the backbone, train a linear head with AdamW at 1e-3, batch size 128, for 2 epochs, and use no additional augmentation.

Observation 2: The dominance of modern VFMs is not uniform across every benchmark. On AIGIHolmes, strong specialized methods remain close: AIDE averages 0.970 and DDA 0.963, while PE-CLIP-Linear is 0.978 and DINOv3-Linear is 0.972. This suggests the clearest separation is in the in-the-wild and AIGI-Now semantic/degraded settings, not all unseen-generator tests.

Observation 3: Real-world transport remains a material deployment gap even for the proposed baseline. On RRDataset, modern VFMs improve over specialized detectors, but fake/AI accuracy under redigital recapture or social-app transfer is still only about 0.548--0.719 depending on the backbone and setting, so calibration under recapture/transmission remains unresolved.
