# cr-tam-that — ImageGen prompts and provenance

Tam Thất (Lv54): quick, friendly little chick spirit with a red berry crest, palmate green foliage and three-leaf tail. Eight successful ImageGen atlas outputs retained as raw-01.png…raw-08.png. Selected candidate raw-07 SHA-256 `4b87146a97f5a2d3013c888b9e791e37e09f17759901646fd2992d2a558aae80`; packed final SHA-256 `ab78f5ac3a436eedb58517431d3fd002335d4313a252bd94b71c09f5cfce87bc`.

Style reference hashes:
- cr-bac-ha/final.png `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`
- cr-moc-nhi/final.png `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`

No pixel retouching. Pipeline used: connected-component pivot packing, common scale, nearest-neighbor.


## Plant f4 repair prompts — 2026-11-12

- New ImageGen raw outputs retained: raw-09.png, raw-10.png, raw-11.png, raw-12.png.
- Reference used: `reference-sprout-f1.png` SHA-256 `403de7eec1ea9c88284afd5efcfea554471f1aa3617df1cb8ab32edd658af811`.
- Prompt invariant: edit only plant f4; reproduce packed sprout f1 silhouette, pose, proportions and pivot; change face only; preserve remaining atlas frames; retain pure magenta key and crisp HD-2D pixel style.

## Selected repair source — 2026-11-13

Repacked from `raw-10.png` (SHA-256 `a86f532802cd17c63cdd16e2e1e656ce3968b0b029f766a4e00c317173577535`) with the existing pipeline v3: fixed-pivot component packing, edge-only defringe, shared palette reduction, and measured using `tools/measure_atlas.py`. No manual pixel edits. Latest gate result: 9/10; purple edge count 5369→389. h=.6798; j=.8593; edge 5369→389.
- Plant f4 reference used: `reference-sprout-f1.png` — SHA-256 `403de7eec1ea9c88284afd5efcfea554471f1aa3617df1cb8ab32edd658af811`.

## 2026-11-16 targeted attempts
raw-13–18: built-in ImageGen, sprout reference and existing sheet; request plant f4 match sprout silhouette, then remove fringe. Selected raw-17. Reference SHA-256 403de7eec1ea9c88284afd5efcfea554471f1aa3617df1cb8ab32edd658af811.
