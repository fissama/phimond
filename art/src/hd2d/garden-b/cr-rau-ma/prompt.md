# Prompt & provenance — cr-rau-ma (C01)

- Brief: `.ai/design/gpt-redo/20-batch-C01-prompt.md`, roster #2 Rau Má; criteria: Đơn 16.
- Built-in ImageGen first made standalone sprout f1 (`raw-01.png`, SHA-256 `499e9e3e754fa702f710b660f84df00f195c33b2af3d5c38f61997381cf8ffd1`). The full 4×5 atlas generation used that sprite as primary design reference; pilot references attached: Bạc Hà `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`, Mộc Nhĩ `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`.
- For plant f4, attached packed sprout f1 `reference-sprout-f1.png` (SHA-256 `3bc3665390d6870f0ec73370a0426c6753abe5bd3d76c1670819de2492157636`) to single-frame ImageGen. Selected packed atlas source `raw-06.png`, SHA-256 `65027cbcaae37a6139598814bcecda0f7c5030346cbe34388cc9797c3cad4386`.
- Final SHA-256 `a82a72e52b424f3b54893c8b976d8c154d5abd0cf2392d723ad84eb65af008bb`. Attempts: 5 ImageGen calls (standalone sprout, atlas redraws, targeted f4); every raw retained.
- QA 10/10. H IoU 0.9575; f heights 74 / 100 / 125–127 px; max width 139; j minimum 0.8536. Remains `approved:false`.
- Packing: connected components, one common nearest-neighbor scale, pivot alignment, magenta key and palette reduction only; no hand-painted pixels or clipping.
