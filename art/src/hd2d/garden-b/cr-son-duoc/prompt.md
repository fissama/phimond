# Prompt & provenance — cr-son-duoc Sơn Dược

- Brief: Đơn 15 v2, crop #2; pipeline/criteria: Đơn 16.
- Character: gentle sleepy baby snake formed from a coiled heart-leaf vine around a short stake; plump cream yam-root belly as face; no fangs or scary tongue. Ripe motion: lazy head yawn and gentle tail swish.
- Atlas prompt: exact 4×5 sheet on flat #FF00FF, HD-2D pixel clusters, face and blush, fixed root pivot (96,168), sprout/grow/ripe loop rows with blink, friendly wave-to-light harvest, plant f4 echo of sprout f1. Max 60 colors and safe packed bounds.
- Selected packed source: `raw-08.png`; SHA-256 `8bf443566b25035a554f516e0417b84e16f5489cd572140b0684afa912b897bb`.
- Final candidate SHA-256: `978a8fc5afbf067a123da754c74117df87a13566d5ddf7c46ad4abd03cbaf9b1`.
- Image references used on initial generation: approved `cr-bac-ha/final.png` SHA-256 `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`; approved `cr-moc-nhi/final.png` SHA-256 `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`; `gd-roots-hang-04/final.png` SHA-256 `9a23c7f7861ecd61f8b8f1ead09ef96005b650f31cdfad2498dc59b047d837e6`; `DocDangNu/sprites.png` SHA-256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`; `DaoThienDuong/sprites.png` SHA-256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`.
- Attempt count: 8/8. Latest QA: 9/10, only h fails at 0.7950. Candidate remains unapproved.
- Packing: `tools/pack_atlas.py` connected-component extraction, common nearest-neighbor scale, pivot alignment; no hand-painted pixels or clipping. The generated target frame was placed into the atlas source as a layout/packing operation.

## Targeted plant f4 redraw — 2026-11-10

- Generated a standalone plant f4 frame with built-in ImageGen, attaching `reference-sprout-f1.png` as the primary image reference (SHA-256 `80f130d28d7d33d6153d0c170d2002084902621113f3a5a85668cf75f88eaab6`). The first whole-sheet edit `raw-09.png` changed unrelated frames and was discarded.
- Targeted frame source: `raw-10.png` (single ImageGen frame; retained). Final packing sheet: `raw-11.png`, SHA-256 `adb2f1ba653c44d4a692117d402309c12fe30db609ca057cecffe6d74c621bc7`.
- New `final.png` SHA-256 `3dd38fcf34ecd5f49ae4a154f954db9a1a6f0d8ca49137cf27ccd00270bae3ec`.
- QA after repack: 10/10; plant f4/sprout f1 IoU 0.9480. Candidate remains `approved:false`.
