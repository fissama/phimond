# Batch 4 — Pirate Ship & Shared Markers (Octopath HD-2D)

Total 21 individual assets covering:
- Pirate ship hardware: `cannon`, `helm-wheel`, `rum-barrel`, `rope-coil`
- Rigging & sway props: `mast-trunk`, `sail-cloth`, `pirate-flag`, `teleport-pillar-high`
- Shared world interaction markers: `target-ring`, `touch-ring`, `quest-new`, `quest-complete`, `talk-mark`, `nest-marker`
- Animated lights & indicators: `storm-lantern` (4 frames), `exit-arrow-up`, `exit-arrow-right`, `exit-arrow-down`, `exit-arrow-left` (4 pulse frames each)
- Terrain & backdrop: `ship-deck-tile` (512x512 seamless xy), `ship-hull-backdrop` (1024x384 seamless x)

## Mechanical QA Summary
- Total assets: 21
- Pass: 21
- Fail: 0
- Color palette: harmonized under `phimond-octopath-ship` palette (max 48 colors).
- Alpha hygiene: clean >= 8px margins on all isolated props and decals.
- Raw integrity: byte-identical raw inputs preserved in each asset directory.
