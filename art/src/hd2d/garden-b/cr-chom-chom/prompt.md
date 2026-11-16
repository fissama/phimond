# Prompt & provenance — cr-chom-chom

- Generated with built-in ImageGen; 8 total outputs: one sprout reference plus seven atlas sheets.
- Selected source: `raw-07.png`; packed by `tools/pack_atlas.py`; measured by `tools/measure_atlas.py`.
- Final design: round red rambutan creature with cream face, short red hairs with muted green tips, playful expression. Rows: sprout, grow, ripe, harvest, plant.
- Iterations targeted first stage height, then plant f4 silhouette. No pixel retouching was performed.

## Reference SHA-256
- Bac Ha approved style ref: `cr-bac-ha/final.png` — `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`
- Moc Nhi approved style ref: `cr-moc-nhi/final.png` — `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`
- Chom Chom sprout ref: `cr-chom-chom/sprout-reference.png` — `842b65067e55002d8846f7e34f43d0ef8607f8520e48d5765772e3550cfe2d7a`

- Selected raw SHA-256: `18d68344d920f4b0f9fa79b1e5387077f672d0ff08dc75539a14a58aab8b9c51`
- Final atlas SHA-256: `6fc4cb1ad627f6b748fb602c6ceafe17d5397823152476e6ed873344939b2274`


## Plant f4 repair prompts — 2026-11-12

- New ImageGen raw outputs retained: raw-09.png, raw-10.png, raw-11.png, raw-12.png.
- Reference used: `reference-sprout-f1.png` SHA-256 `1496d07bfe5de5ec1b392c58ecae985d0901c271fff30d5d68f6eb734472a3fe`.
- Prompt invariant: edit only plant f4; reproduce packed sprout f1 silhouette, pose, proportions and pivot; change face only; preserve remaining atlas frames; retain pure magenta key and crisp HD-2D pixel style.

## Selected repair source — 2026-11-13

Repacked from `raw-09.png` (SHA-256 `3ab3d80f07410c2a032e0bacfd1efa3f23f2cf50cb2e6e14ed31f9fb1b9794cc`) with the existing pipeline v3: fixed-pivot component packing, edge-only defringe, shared palette reduction, and measured using `tools/measure_atlas.py`. No manual pixel edits. Latest gate result: 9/10; purple edge count 8108→3717. h=.6272; edge 8108→3717.
- Plant f4 reference used: `reference-sprout-f1.png` — SHA-256 `1496d07bfe5de5ec1b392c58ecae985d0901c271fff30d5d68f6eb734472a3fe`.

## 2026-11-16 targeted attempt
Built-in ImageGen raw-13; sheet raw-09 plus sprout reference, redraw plant f4 smaller to match sprout silhouette. Reference SHA-256 1496d07bfe5de5ec1b392c58ecae985d0901c271fff30d5d68f6eb734472a3fe.
