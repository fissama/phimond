# Ground decal candidate

Route: built-in Codex image_gen; extracted from a 3×2 magenta-backed sheet.

Prompt: Broken lavender stone chips. Irregular low ground decal, Octopath-style pixel clusters, Tinh Gioi palette, isolated on #FF00FF, no shadow, text or scene.

Reference images and SHA-256:
- `.ai/design/map-checklists/refs/astral_realm_spacetime_rift.jpg` — `5797978a69355eafa93ee2514e09156c548a0579838278f3276538ee080e8700`
- `apps/game-web/art-src/hd2d/batch-01-octopath/fallen-leaves-01/final.png` — `b4ce69363d865975281171ec5587fd8c160e5f2c5ca65e7aaf129ab07893d300`
- `apps/game-web/art-src/hd2d/batch-01-octopath/edge-grass-roots/final.png` — `7bf3e3700ef71963c08b435e2bc1a717799e46acef74ca018b27122d4541aab8`
- `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Raw sheet SHA-256: `a626c25d453eb58dbca61273ec60ea3384f47daa73b460aa8b9df4700da473a2`. Extraction uses Forge chroma-key, despill radius 3, component mode all, min component area 4; 8px component padding. Nondithered median-cut palette finish to 48 colors.

Selected chroma-key thresholds: 30 / 60 after the default threshold removed pink petal and stone pixels; this lower-threshold extraction preserved foreground detail. Despill radius 3.
