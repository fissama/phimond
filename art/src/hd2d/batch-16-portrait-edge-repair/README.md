# NPC portrait edge-repair candidates — 2026-10-30

Two current P01 portrait deliveries had a visible magenta fringe on transparent edges. This folder preserves the existing release art and provides separate review-only replacements derived from the original raw sources. Nothing here is installed or owner-approved.

## Individual assets

- `delivery/portrait-bia_shop.png` — 256×256, 48 visible colors, binary alpha. Reprocessing + palette QA pass. The only process warning is the intentional bottom crop touch. Before/after proof: `delivery/portrait-bia_shop-before-after.png`.
- `delivery/portrait-sq_board.png` — 256×256, 48 visible colors, binary alpha. Palette QA passes; process QA retains a key-ring warning (`0.044393`, limit `0.01`) that may be purple hair at the silhouette edge. Before/after proof: `delivery/portrait-sq_board-before-after.png`.

Each PNG has its own prompt and provenance. Per-asset QA and the raw pipeline/palette QA are next to each candidate. Review each image separately on both light and dark backgrounds; do not copy to runtime unless approved.

The remaining 17 NPC portraits and all 3 starter portraits are unchanged. Their current visual review and approval status remains in `apps/game-web/art-src/hd2d/p01-release-art-20261023/delivery/portrait-review-codex-20261030.md` and their per-file QA JSONs.
