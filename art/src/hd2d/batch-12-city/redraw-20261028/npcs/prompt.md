# Capital NPC sheet — raw 01

Route: built-in Codex ImageGen, 2026-10-28. Source image is preserved byte-for-byte at `raw-01.png` (1536×1024, SHA256 `0df5c6e5756beca5ee65d04ad9f9b39fbc318f77861cd1e8868bbd0ae73908f0`).

Prompt: Create a 3-column × 2-row sheet of SIX different full-body idle town NPC sprites for the royal capital city in the attached city-square reference. Use the two attached approved palace NPC sprites only as pixel-art style anchors for size, rendering and outline. Use the two attached pet sprites only as line-weight/shading anchors. The six characters are: (1) young palace page in cream-and-crimson livery holding a sealed scroll; (2) female gate watch officer in dark teal uniform with short spear; (3) older fountain keeper in work apron holding a small brass wrench; (4) flower seller in warm rose and olive clothes carrying a shoulder basket of blossoms; (5) cheerful city child with a wooden hoop; (6) elderly street musician with a small lute. Every NPC must have a clearly distinct silhouette, age, outfit and prop; no duplicate body or recolored copies. Front-facing slight 3/4, upright relaxed idle stance, whole figure including feet, one character centered in each equal square cell with generous transparent margin. Style: HD-2D Octopath-like game pixel art, chunky crisp pixel clusters, warm upper-left light, dark same-hue outline, 2–4 tones per material, rich but controlled detail. Use a perfectly flat pure #FF00FF magenta background with no shadow, no gradient, no glow. No contact between cells, labels, text, scenery, ground or extra objects. Output exact clean sprite art, hard edges.

Attached references (content/style role and SHA256):

- Content: `.ai/design/map-checklists/refs/city_square.jpg` — `995db064ece8534304239e06d3882dc472bde1b9a2198a7784d127bfaad61cf0`
- Style: `apps/game-web/art-src/hd2d/batch-05-octopath/npc-pal_advisor/final.png` — `de9a4e3da1b0e92f26902f4b5a2e0964b9bd04f30176753d1a7d5d293875aadd`
- Style: `apps/game-web/art-src/hd2d/batch-05-octopath/npc-pal_guild/final.png` — `127549b45bdda3d76b9cc5ce578831d49ef6ddb7b02d7900ebb62c9aee5f5a6a`
- Line/shading anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- Line/shading anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`

Processing: Sprite Forge `generate2dsprite.py process`, target npc, chroma-key magenta, 2×3 grid, 192 px cells, feet-aligned and strict structural QC. Approval remains false until owner review.
