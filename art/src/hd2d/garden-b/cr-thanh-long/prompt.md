# Prompt & provenance — cr-thanh-long

- Brief: `.ai/design/gpt-redo/20-batch-C09-prompt.md`; contract: `.ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md`.
- Source: built-in ImageGen, `raw-02.png` SHA-256 `19cc280b430d11f158bf05b8948bc7a91a7ea0bf83fe34e61705132a850262ad`.
- References:
- `cr-bac-ha/final.png` SHA-256 `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`
- `cr-moc-nhi/final.png` SHA-256 `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`
- Packed final SHA-256 `99364a33f60dbe7a94c2e3861de4adc78a7d99c73c8b61a4957b2a0756ffab3f`. Pack command: `tools/pack_atlas.py --id cr-thanh-long --kind crop --raw raw-02.png`.

Cute proud baby dragon-fruit spirit, restrained pink fruit body, green scales, cream face. Sheet layout: 4×5, rows sprout/grow/ripe/harvest/plant; plant f4 repeats sprout f1 silhouette; rows 1–3 blink at frame 3. No effects baked.


## Selected source correction

Packed source: `raw-07.png`. Source SHA256: `1fef8452f0e95e5ed15b4a7a0fb3e35103cd74b3a6cc86a3d9cecf3cf4d7dd8c`. Final SHA256: `167c2b3256b541acb09fa44b4b0729b55b6841c2fbdc911de4db7840d194721f`.


## Plant f4 repair prompts — 2026-11-12

- New ImageGen raw outputs retained: raw-09.png.
- Reference used: `reference-sprout-f1.png` SHA-256 `29279fcb3b637bcd747b422f6b4b554ed2503554ab0d7ae4ea92faa18b2d62ed`.
- Prompt invariant: edit only plant f4; reproduce packed sprout f1 silhouette, pose, proportions and pivot; change face only; preserve remaining atlas frames; retain pure magenta key and crisp HD-2D pixel style.

## Selected repair source — 2026-11-13

Repacked from `raw-09.png` (SHA-256 `10b4956583bb6ec1fb62b6540db6191d2ecb3cdf12dfb12b51d71c7228524cc6`) with the existing pipeline v3: fixed-pivot component packing, edge-only defringe, shared palette reduction, and measured using `tools/measure_atlas.py`. No manual pixel edits. Latest gate result: 10/10; purple edge count 6809→612. h=.9803; edge 6809→612.
- Plant f4 reference used: `reference-sprout-f1.png` — SHA-256 `29279fcb3b637bcd747b422f6b4b554ed2503554ab0d7ae4ea92faa18b2d62ed`.
