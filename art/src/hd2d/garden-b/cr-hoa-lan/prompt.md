# Prompt & provenance — cr-hoa-lan

- Built-in ImageGen; eight total outputs including one standalone sprout reference.
- Selected source: `raw-06.png`. Pipeline v3 pack and measure; no pixel editing.
- Design: elegant orchid butterfly spirit, cream-white/violet petals, gold center, muted green body.

## Reference SHA-256
- Bac Ha style reference: `cr-bac-ha/final.png` — `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`
- Moc Nhi style reference: `cr-moc-nhi/final.png` — `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`
- standalone orchid sprout reference: `cr-hoa-lan/sprout-reference.png` — `23c2e3ebab558503286e7d167ef7783cb7d87bc1c8da8c33e84628193197fba0`
- Selected raw SHA-256: `9648ed61a65a5e01c0bb06aa297955324d69ff10d0a2a14c2580286ebe613498`
- Final SHA-256: `4431e713d5d4a5d58d07e4b8fea9bdd4dd688db892839641516a5c5927f98db8`


## Plant f4 repair prompts — 2026-11-12

- New ImageGen raw outputs retained: raw-09.png, raw-10.png.
- Reference used: `reference-sprout-f1.png` SHA-256 `0ff9a3bfb79dd3df9cc383031c89173f39766c969c36bd639b8aeacdd6187b31`.
- Prompt invariant: edit only plant f4; reproduce packed sprout f1 silhouette, pose, proportions and pivot; change face only; preserve remaining atlas frames; retain pure magenta key and crisp HD-2D pixel style.

## Selected repair source — 2026-11-13

Repacked from `raw-10.png` (SHA-256 `580b4c901c135b5e03b4303404b91d8b82b4d0ccbe31ceb7228de0aa7aab4be6`) with the existing pipeline v3: fixed-pivot component packing, edge-only defringe, shared palette reduction, and measured using `tools/measure_atlas.py`. No manual pixel edits. Latest gate result: 10/10; purple edge count 10362→7631. h=.8078; edge 10362→7631.
- Plant f4 reference used: `reference-sprout-f1.png` — SHA-256 `0ff9a3bfb79dd3df9cc383031c89173f39766c969c36bd639b8aeacdd6187b31`.
