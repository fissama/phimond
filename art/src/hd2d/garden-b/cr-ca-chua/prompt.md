# Prompt & provenance — cr-ca-chua (C01)

- Brief: `.ai/design/gpt-redo/20-batch-C01-prompt.md`, roster #7 Cà Chua; criteria: Đơn 16.
- Built-in ImageGen first made standalone sprout f1 (`raw-01.png`, SHA-256 `d4d56f6904fab107d0df67b687380bb5e1063f6da753c054465d1f239a303ddb`). Atlas generations used it as the primary design reference; Bạc Hà (`8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`) and Mộc Nhĩ (`2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`) were attached as style references.
- Plant f4 single-frame ImageGen used packed sprout f1 `reference-sprout-f1.png` (SHA-256 `192fa06ec9916d01e63e6af8ebb8795405aa46aa5c88b59a10cf9b203b643438`). Selected packing source `raw-06.png`, SHA-256 `42c6e254da8064e4440e0b5d5d86ef7b82224f8862aad86c3e4509ff25ee762b`.
- Final SHA-256 `2585b1e031583bee174b110390cdf179eab8eb8daf55af9aa1a99db4802c877f`. Five ImageGen calls used; all raw sources retained.
- QA 10/10. H IoU 0.9612; f heights 73 / 111–112 / 132–133 px; max width 112; j minimum 0.9217. Remains `approved:false`.
- Packing: connected components, common nearest-neighbor scale, pivot alignment, magenta key and palette reduction only; no hand-painted pixels or clipping.
