# Prompt & provenance — cr-huong-co

- Brief: Đơn 15 v2, crop #6 Hương Cô; pipeline and acceptance: Đơn 16.
- Character: gentle shiitake cook spirit, spotted brown cap shaped like a chef hat, cream stem body, tiny friendly face, green root/leaf base. Ripe animation pretends to stir an imaginary pot using short arms. No actual pot or extra prop. Sleepy sprout, curious grow, proud ripe, friendly harvest wave into sparse pixels, plant f4 echoing sprout f1.
- Generation tool: built-in ImageGen. Eight sheets retained as `raw-01.png`…`raw-08.png`; selected `raw-08.png` SHA-256 `6d61007e7d21a96c298c42510b889098f58241c7d7b86faba2f8e7f29e27df26`.
- Final candidate `final.png`, SHA-256 `a72786344ac72eb07fddfba2ffd94ea5c35872836a1224b20431085b5a2cefba`.
- Image reference attached: approved `cr-moc-nhi/final.png`, SHA-256 `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51` (style and atlas scale).
- QA after attempt 8: 9/10. h fails: plant f4 vs sprout f1 IoU 0.7158 (threshold ≥0.80). All other applicable checks pass; see `qa.json` and `review.md`.
- Packing used connected-component extraction, common nearest-neighbor scale, pivot alignment, quantization and magenta key only. No pixel painting, clipping, flipping or mirroring.

## Targeted plant f4 redraw — 2026-11-10

- Generated a standalone plant f4 frame with built-in ImageGen using `reference-sprout-f1.png` as the primary attached reference (SHA-256 `eb583f9a05c4a43117e7194238a58c41ef3eb02275d9abe0f13c2653c1e2e5a0`).
- Target frame `raw-09.png` retained; final packing sheet `raw-10.png`, SHA-256 `acd6dd88021a2ae59886081ed37eea309d347d7fc130d11ad3dced0031630378`.
- New `final.png` SHA-256 `abe51f8cbb9ac028a839eea10aab4fb46fbfd1abb8a2e954bb7ddac6c72c7c1a`.
- QA after repack: 10/10; plant f4/sprout f1 IoU 0.9505. Candidate remains `approved:false`.
