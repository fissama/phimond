# Prompt & provenance — cr-dia-hoang

- Brief: Đơn 15 v2, crop #5 Địa Hoàng; pipeline and acceptance: Đơn 16.
- Character: hardworking mole-root spirit; swollen cream/brown medicinal root body, wrinkled olive rosette, pink-purple bell flowers, tiny pink nose and round eyes. Ripe motion sniffs while bells wobble. Keep face gentle, root pivot fixed, 4×5 animation with blinks in loop rows and friendly harvest fade.
- Generation tool: built-in ImageGen. Eight sheets retained as `raw-01.png`…`raw-08.png`; selected `raw-08.png` SHA-256 `850186687deae1c33d0fea2dea15cc06d361a6d69e09cf39588f7d2e85835850`.
- Final candidate `final.png`, SHA-256 `128977398c0a9b3ff2f7474e1e81fc5a19c72716161bd1afb6ddde4dfb5fc468`.
- Image reference attached: approved `cr-moc-nhi/final.png`, SHA-256 `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51` (style and atlas scale).
- QA after attempt 8: 9/10. h fails: plant f4 vs sprout f1 IoU 0.6767 (threshold ≥0.80). All other applicable checks pass; see `qa.json` and `review.md`.
- Packing used connected-component extraction, common nearest-neighbor scale, pivot alignment, quantization and magenta key only. No pixel painting, clipping, flipping or mirroring.
