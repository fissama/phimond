# Prompt/provenance — cr-dua-hau

## Asset brief
Dưa Hấu — bé dưa sọc xanh, cười lộ ruột đỏ và phì hạt tinh nghịch.

## Contract
- 4×5 sheet, pure #FF00FF backing, packed by garden-b/tools/pack_atlas.py; 768×960 RGBA atlas.
- HD-2D Octopath pixel art, hard pixel clusters, same-tone outlines, no baked shadow/glow/text.
- Crop: visible cute face; distinct sprout/grow/ripe sizes; loop rows blink; harvest and plant are one-shot.

## Source provenance
- Selected packed source: `raw-09.png` (sha256 `d70232cf09c3457439daab95d00f69b82c04a5222baf5d1fdff708500f9bde65`).
- ImageGen generations in this continuation: 8 outputs (`raw-02.png` through `raw-09.png`); all retained. Their prompts requested only plant-row repair, while the generator re-rendered the complete sheet.
- Current final is checked in `qa.json`; review findings are in `review.md`.

## Current task — plant row 5 redraw

Plant f1 must begin as a tiny watermelon seed in a small soil mound; f2 cracks/sprouts; f3 grows slightly; f4 matches the extracted sprout f1 silhouette (IoU >=0.80). Never start with a mature plant. Only row 5 may change.

ImageGen reference attached: `reference-sprout-f1.png` (cropped directly from packed sprout f1); sha256 `83dd38c22a1c3d9d5f97e5e6f9a595a10444f4364d2d568f8ed3d04da7e9e762`.

The initial request before this continuation had been rejected with HTTP 429; after reset, eight ImageGen outputs were produced and packed. Final gate failures and the current final hash are in `review.md` and `qa.json`.


## Plant f4 repair prompts — 2026-11-12

- New ImageGen raw outputs retained: raw-09.png, raw-10.png, raw-11.png, raw-12.png, raw-13.png.
- Reference used: `reference-sprout-f1.png` SHA-256 `83dd38c22a1c3d9d5f97e5e6f9a595a10444f4364d2d568f8ed3d04da7e9e762`.
- Prompt invariant: edit only plant f4; reproduce packed sprout f1 silhouette, pose, proportions and pivot; change face only; preserve remaining atlas frames; retain pure magenta key and crisp HD-2D pixel style.

## Selected repair source — 2026-11-13

Repacked from `raw-09.png` (SHA-256 `d70232cf09c3457439daab95d00f69b82c04a5222baf5d1fdff708500f9bde65`) with the existing pipeline v3: fixed-pivot component packing, edge-only defringe, shared palette reduction, and measured using `tools/measure_atlas.py`. No manual pixel edits. Latest gate result: 8/10; purple edge count 8020→4642. h=.5710; j=.8458; edge 8020→4642.
- Plant f4 reference used: `reference-sprout-f1.png` — SHA-256 `83dd38c22a1c3d9d5f97e5e6f9a595a10444f4364d2d568f8ed3d04da7e9e762`.

## Retry log — 2026-11-13

Three new built-in ImageGen sheet outputs are retained as `raw-11.png` through `raw-13.png`; their SHA-256 values: 0c98056dde9e55dc5680b96c63598833c6f4492fa11e9f7c525eaebfb0cdda72, d74dda9727b1c99ab99f0f03a4b051df176d356ee7c448486a229a52ce52ff94, 249583badd962ff5f832f7ded4de85bbdbd88ef99477ddc1bfffa742f531535d. `raw-11` and `raw-12` did not satisfy the localized-edit/plant-match target. Latest packed candidate is `raw-13.png` (SHA-256 `249583badd962ff5f832f7ded4de85bbdbd88ef99477ddc1bfffa742f531535d`); measured h=.7891, j=.8524. ImageGen returned HTTP 429 after this third output; reset at 2026-11-13 11:50:38 +07. Resume with attempt 4/6 from this state.

## Targeted plant f4 repair — 2026-11-13

Six built-in ImageGen attempts retained as raw-11 through raw-16, using the packed sprout f1 reference. Latest selected source raw-16; h=.5822, j=.8690. Six-output allowance exhausted; no manual pixel patching.

## Targeted plant f4 repair — 2026-11-16

Six new built-in ImageGen outputs retained. Latest packed source `raw-16.png`; h=0.5822, j=0.8690. Six-output allowance exhausted.
