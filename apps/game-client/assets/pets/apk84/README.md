# APK 8.4 — accepted species art

152 Species IDs match `data/pets/roster_apk84.json`. Each folder contains:

- `portrait.png`: original source Sprite, unchanged pixels.
- `sprites.png`: original animation Sprites packed without scaling, aligned by
  the source pivot; only transparent padding is added.
- `frames.tres`: Godot SpriteFrames with idle/run/die/attack/magic, source loop
  flags and decoded discrete-keyframe durations. `speed = 1` makes frame duration
  values seconds. Set the renderer's texture filter to nearest for pixel art.

`manifest.json` records Sprite/Animator/AnimationClip source IDs, pivots,
pixels-per-unit, regions, durations and PNG hashes. Actor mapping uses the unique
case-insensitive source Species ID. One source spelling alias is explicit:
`QuaiVatNhamThach` → `QUAIVATNHAMTHAC`.

These are reusable resources for the current Godot project. They do not replace
the legacy gameplay catalog or create stats/spawns/save migration. Animator state
transitions, world scale, flip rules and event synchronization remain renderer
responsibilities; clip extraction does not claim complete Unity behavior parity.

Rebuild from the workspace root:

```sh
rtk proxy tools/.cache/asset-venv/bin/python tools/assets/import_p10_roster.py \
  '/path/Spirit Beast World 8.4 (1).xapk' .
```
