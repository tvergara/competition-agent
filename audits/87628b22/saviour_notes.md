SoMA is a real-to-sim neural simulator for soft-body manipulation that uses action-conditioned Gaussian Splatting to model dynamics.

- **Gravity Orientation Logic**: The simulator resolves gravity sign ambiguity by aligning the direction with the camera viewing vector $\mathbf{v}_c$ and supporting plane normal $\mathbf{n}_{\Pi}$ using the formula $\mathbf{g} = -\operatorname{sign}(\mathbf{n}_{\Pi} \cdot \mathbf{v}_c)\,\mathbf{n}_{\Pi}$ (Section 4.2.1).
- **Occlusion-Robust Color Initialization**: For the T-shirt folding task, all Gaussian splat colors are initialized to blue to maintain appearance consistency for occluded or weakly observed regions, such as the back side of the fabric (Appendix B.1).
- **H200 Hardware Benchmarks**: The system was trained on NVIDIA H200 GPUs, with the initial training stage requiring 24 hours on a 4-GPU setup and achieving an inference rate of approximately 12 FPS on a single unit (Appendix B.2).
