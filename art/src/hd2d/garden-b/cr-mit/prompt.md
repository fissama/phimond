# cr-mit — ImageGen prompts and provenance

C08 Mít: shy tan pangolin spirit with jackfruit-like olive spikes, cream face, golden inner fruit. Eight outputs raw-01…raw-08 retained. Selected raw-06 SHA-256 `668c00a3c4d3ba33fbff90e0fbff8c1ba7ad06fef351ac20b3b2f37bd9567e79`; packed final SHA-256 `adac16db15b03c5cdc48b2f0799fdd649eb5f28ee77cd0abb93e3785ed2c82bc`. Style references: Bạc Hà `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`, Mộc Nhĩ `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`. raw-07 referenced extracted sprout image; no pixel edits.


## Plant f4 repair prompts — 2026-11-12

- New ImageGen raw outputs retained: raw-09.png, raw-10.png, raw-11.png, raw-12.png.
- Reference used: `reference-sprout-f1.png` SHA-256 `ba3a8c9d2a091324ea15817b50eef89186cad6381c2b7bc177e2e3d52660f352`.
- Prompt invariant: edit only plant f4; reproduce packed sprout f1 silhouette, pose, proportions and pivot; change face only; preserve remaining atlas frames; retain pure magenta key and crisp HD-2D pixel style.

## Selected repair source — 2026-11-13

Repacked from `raw-10.png` (SHA-256 `6e575c079088aea411143a09ed5a40d8e755e52971740732c444d47ae9aa0136`) with the existing pipeline v3: fixed-pivot component packing, edge-only defringe, shared palette reduction, and measured using `tools/measure_atlas.py`. No manual pixel edits. Latest gate result: 9/10; purple edge count 7108→2711. h=.6799; edge 7108→2711.
- Plant f4 reference used: `reference-sprout-f1.png` — SHA-256 `ba3a8c9d2a091324ea15817b50eef89186cad6381c2b7bc177e2e3d52660f352`.

## 2026-11-16 targeted attempts
raw-13–16: built-in ImageGen, sprout reference and selected sheet, plant f4 match silhouette with facial change. Reference SHA-256 ba3a8c9d2a091324ea15817b50eef89186cad6381c2b7bc177e2e3d52660f352.

### 2026-11-16 bounded plant-row redraw
Selected `raw-22.png` from six outputs `raw-17..22`. Plant sequence is seed → crack → sprout → sprout; h=0.9014. Current final still fails f on sprout height 76 px and max width 151 px. See review.md.
