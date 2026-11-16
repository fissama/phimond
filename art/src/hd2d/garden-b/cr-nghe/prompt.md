# Prompt & provenance — cr-nghe

- Source: built-in Codex `image_gen`; one standalone sprout reference and eight atlas sheets retained. This exceeded the per-asset 8-output allowance by one; no further image calls were made.
- Selected sheet: `raw-05.png`; SHA-256 `653e9d3519bd8e63e3e9be74900538718be92e02d2d88a38137355157aea7558`.
- Final atlas: `final.png`; SHA-256 `fc252b6fcaa30176912ebb4aedb71142ebd2f8d8362daec214e13f3c9461069a`; packed by `tools/pack_atlas.py`, nearest-neighbor common scale recorded in `qa.json`.
- Sprout reference: `reference-sprout-f1.png`; SHA-256 `e8f915bdb4ee42d0ef5b7240b33aebc7942d14e3a7f6f16915e5181573181056`.
- Style refs attached: `cr-bac-ha/final.png` `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`; `cr-moc-nhi/final.png` `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`; `DocDangNu/sprites.png` `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`; `DaoThienDuong/sprites.png` `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e`.

Brief: orange turmeric-root tiger cub with cream muzzle/belly, dark turmeric stripes, small white-pink flower bud and green leaves. 4×5 pixel atlas, 192px cells; row1 sprout, row2 grow, row3 brave ripe roar, row4 friendly wave/harvest, row5 seed to sprout. Plant frame4 should match sprout frame1. Target heights 45–75 / 85–112 / 120–150px, width ≤140px; rows1–3 blink; no text, glow, baked shadow, fog or blur. Atlas style and all raw generations are recorded in this folder.


## Plant f4 repair prompts — 2026-11-12

- New ImageGen raw outputs retained: raw-09.png, raw-10.png, raw-11.png, raw-12.png.
- Reference used: `reference-sprout-f1.png` SHA-256 `e8f915bdb4ee42d0ef5b7240b33aebc7942d14e3a7f6f16915e5181573181056`.
- Prompt invariant: edit only plant f4; reproduce packed sprout f1 silhouette, pose, proportions and pivot; change face only; preserve remaining atlas frames; retain pure magenta key and crisp HD-2D pixel style.

## Selected repair source — 2026-11-13

Repacked from `raw-05.png` (SHA-256 `653e9d3519bd8e63e3e9be74900538718be92e02d2d88a38137355157aea7558`) with the existing pipeline v3: fixed-pivot component packing, edge-only defringe, shared palette reduction, and measured using `tools/measure_atlas.py`. No manual pixel edits. Latest gate result: 9/10; purple edge count 6681→0. h=.7640; edge 6681→0.
- Plant f4 reference used: `reference-sprout-f1.png` — SHA-256 `e8f915bdb4ee42d0ef5b7240b33aebc7942d14e3a7f6f16915e5181573181056`.

## Targeted plant f4 repair — 2026-11-16

Six new built-in ImageGen outputs retained. Latest packed source `raw-18.png`; h=0.5673, j=0.9192. Six-output allowance exhausted.


## Plant f4 repair — 2026-11-16

One built-in ImageGen edit output saved as raw-19.png. Reference order: raw-18.png atlas edit target; reference-sprout-f1-tight.png for the exact plant f1 silhouette. Prompt constrained changes to plant f4 only, matching its outer shape/pose/scale to sprout f1 and changing expression.

### 2026-11-16 bounded repair
Selected `raw-29.png` from six outputs `raw-25..30`; h=0.6717 under current >=0.75 criterion. Attempt budget exhausted; see review.md.
