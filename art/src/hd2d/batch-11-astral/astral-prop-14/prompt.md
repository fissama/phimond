# Cloud bridge candidate

Route: built-in Codex image_gen; raw preserved byte-identically.

## Prompt

Create one production-quality game prop sprite for Phimond HD-2D map kit Astral / Tinh Gioi. Subject: a single short floating cloud-stone bridge segment, viewed from slightly elevated 3/4 top-down game camera, broad enough for a small player character to walk across. It should look like hand-laid lavender and dusk-violet stone slabs with warm rose sunset edge highlights, subtle golden star-rune inlays, and several small rounded clouds tucked beneath the sides. Use the supplied original Astral realm map image as content reference. Use the supplied approved Octopath-style rock prop and creature sprite anchors for rendering style only. Match painterly pixel-art rendering with deliberate large pixel clusters, 2-4 value steps per material, 33-48 distinct colors, dark same-hue outlines, warm upper-left light. Isolated single prop centered with generous transparent padding, bottom-center anchor, no cast shadow, no ground plane, no background, no fog, no glow bloom, no text, no characters, no extra objects. The bridge should have a shallow gentle curve and irregular stone outline, not look like a generic straight rectangular plank. Preserve clean alpha transparency. No spritesheet, only one object.

## Attached references and SHA-256

- `.ai/design/map-checklists/refs/astral_realm_spacetime_rift.jpg` — `5797978a69355eafa93ee2514e09156c548a0579838278f3276538ee080e8700`
- `apps/game-web/art-src/hd2d/batch-01-octopath/rock-medium/final.png` — `c951cb4786e9a86ce42fbf50ade43670763c906bd139175478d0e5f675014bfc`
- `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`

Finish: binary alpha threshold 128 removes generated low-opacity halo; cropped to silhouette with margin; nondithered FASTOCTREE palette quantization, 48 colors max.
