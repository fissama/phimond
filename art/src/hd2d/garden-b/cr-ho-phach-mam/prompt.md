# Hổ Phách Mầm — generation record

Built-in ImageGen; outputs `raw-01.png` through `raw-03.png` retained. Selected source: `raw-03.png`. Candidate concept follows C10: friendly amber fossil-bug seedling, amber shell and warm core, olive leaves; rows are sprout, grow, ripe, harvest, plant. Prompt explicitly requested pixel art, a uniform 4×5 sheet, #FF00FF background, blink frames and no purple/violet/pink subject pixels.

Style references attached by request: garden-b/cr-bac-ha/final.png and garden-b/cr-moc-nhi/final.png.

## Reference hashes

- `cr-bac-ha/final.png` SHA256 `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`
- `cr-moc-nhi/final.png` SHA256 `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`
- `cr-ho-phach-mam/raw-05.png` SHA256 `b9425e77203733f40c5297431b266f6c4ecff6b3d023b510348e757dc61ee861`


## Plant f4 repair prompts — 2026-11-12

- New ImageGen raw outputs retained: raw-09.png, raw-10.png, raw-11.png, raw-12.png.
- Reference used: `reference-sprout-f1.png` SHA-256 `ebfdfea6e96d9131735a14bb95bb1fbc660275eefa362825f6d9ee98891900d8`.
- Prompt invariant: edit only plant f4; reproduce packed sprout f1 silhouette, pose, proportions and pivot; change face only; preserve remaining atlas frames; retain pure magenta key and crisp HD-2D pixel style.

## Selected repair source — 2026-11-13

Repacked from `raw-10.png` (SHA-256 `1686097a947c0953a5f2a5836f777c8bb5c8a5f61175932f030af9852f5df6ce`) with the existing pipeline v3: fixed-pivot component packing, edge-only defringe, shared palette reduction, and measured using `tools/measure_atlas.py`. No manual pixel edits. Latest gate result: 9/10; purple edge count 6533→0. h=.6041; edge 6533→0.
- Plant f4 reference used: `reference-sprout-f1.png` — SHA-256 `ebfdfea6e96d9131735a14bb95bb1fbc660275eefa362825f6d9ee98891900d8`.

## 2026-11-16 targeted attempts
raw-13–16 from built-in ImageGen with sprout reference; selected raw-16. Reference SHA-256 ebfdfea6e96d9131735a14bb95bb1fbc660275eefa362825f6d9ee98891900d8.

### 2026-11-16 grow/ripe redraw
Selected `raw-21.png`; current packed final passed a–j (58 colors; h=.8953; loop IoU=.9547). Visual review is recorded in review.md.
