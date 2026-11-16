# crossroads-edge-02

Route: built-in image_gen (`host_image`); model not exposed.

Prompt: Top-down horizontally repeating cave-floor edge strip, 512x128 final. Transition: dark cave gravel into emerald mossy stone; irregular natural edge, no large props, full-coverage tile strip, left/right endpoints join seamlessly. Damp underground cave palette, crisp Octopath-like pixel clusters, 33–48 discrete colors, 2–4 tones, no haze/blur/glow/gradient/text. Actual image output is cropped only to a naturally matching 4:1 segment; no pixel drawing or mirroring.

Actual attached references and SHA256:
- `.ai/design/map-checklists/refs/crossroads_unnamed_area_01.jpg` — `7f6522193f17a5514164c1975e2073275cf9bc0471d2b5bf03fe50778369187a`
- `apps/game-web/art-src/hd2d/batch-01-octopath/edge-grass-dirt/final.png` — `cea364b6f8306a6a2db0561b36b846d0e1252cf9b9c75f383a8f97a86a2c417d`
- `apps/game-web/art-src/hd2d/batch-01-octopath/edge-grass-roots/final.png` — `7bf3e3700ef71963c08b435e2bc1a717799e46acef74ca018b27122d4541aab8`
- `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`
- raw-01.png — `c8fc6488ec86f011a6a6ddd352e014e26189b7e46e8e3e32008a4ed1ec94d779`

Selected source crop `84,328,1620,712` of `2059x764`; nearest-scale to 512×128, nondithered 48-color finish, alpha set opaque by threshold (all source alpha >127).
