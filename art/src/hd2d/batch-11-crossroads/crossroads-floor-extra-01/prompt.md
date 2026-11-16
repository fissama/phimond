# crossroads-floor-extra-01

Route: built-in image_gen. Model not exposed.

Use case: stylized-concept
Asset type: two-tile terrain sheet for Phimond Crossroads HD-2D game, to be cropped natively at 512×512 with no resizing
Input images: Image 1 is content and palette reference for the Crossroads cave. Images 2 and 3 define approved floor pixel finish only. Images 4 and 5 are creature anchors only for outline weight and cluster density.
Composition: exact 1536×1024 landscape sheet. Top half: exactly two 512×512 square tile cells in x=0..511 and x=512..1023. Cell A is at x=0..511; cell B is at x=512..1023. The entire third top cell x=1024..1535 and the entire bottom half y=512..1023 are solid pure #FF00FF. No gutters, text, separators, or overlaps.
Primary request: A is a calm mineral-silt floor: broad overlapping quiet sediment patches and a few large smooth slate fragments, sparse medium-sized grains only. Large grouped pixels and open low-detail areas; no dense speckles, stippling, dither, grain noise, or tiny repeated dots. B is a separate cave-floor material of broad pale blue-green limestone plates with a few muted cyan cracks, large simple clusters and occasional smooth patches. Both are fully opaque 512×512 top-down textures, each seamlessly repeating on four sides. For each tile, the outermost 8 pixels on all four edges are perfectly flat in one identical deep teal base color; details remain at least 8 pixels from edges.
Style: crisp Octopath-inspired HD-2D pixel art, deliberate chunky clusters, 33–48 colors per tile after nondithered finish, 2–4 tones per material, dark teal-blue outlines, restrained highlights, warm upper-left key with cool shadows. Match approved floor refs' pixel scale; avoid painterly smoothing.
Palette: cave navy, slate blue-gray, muted turquoise and soft mineral teal; no neon.
Avoid: high-frequency noise, dense tiny pebbles, props, crystals, characters, shadows, fog, bloom, gradients, perspective, labels, words, checkerboard.

Actual attachments (ordered):
1. .ai/design/map-checklists/refs/crossroads_unnamed_area_01.jpg — SHA256 7f6522193f17a5514164c1975e2073275cf9bc0471d2b5bf03fe50778369187a
2. apps/game-web/art-src/hd2d/batch-01-octopath/grass-floor-01/final.png — SHA256 792b3a1c25fb3be8671af1a4e119ef7af3bbd5a89dd22e42e14206317697524c
3. apps/game-web/art-src/hd2d/batch-01-octopath/dirt-floor-01/final.png — SHA256 bd4ba8187917b9023a9f9c9bd7ddc8ad43cb269724cbe02c1137f299ea03dff3
4. apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png — SHA256 fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da
5. apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png — SHA256 043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3

Raw: raw-01-selected-floors-03.png; SHA256 f6b2d49a36f5152c1b750938bc2120bc5a234f0f8433e7d499893241f3707811; source box [0, 0, 512, 512]; sheet extraction polygon None; translation-only source registration None. Final [512, 512]. Non-dithered 48color finish, nearest scaling. No content drawn with code.

Finish details: {"visible_colors": 38, "palette_source": null, "palette_include": null, "palette_exclude": null, "palette_remap": {"#09323c": "#07303b", "#08303b": "#07303b", "#07303a": "#07303b", "#06303a": "#07303b", "#072f39": "#07303b", "#072f3a": "#07303b", "#08303a": "#07303b", "#072d38": "#07303b", "#0c303a": "#07303b", "#103641": "#07303b"}, "base_palette_filter": null, "native_alpha": false, "key_threshold": 100, "key_edge_threshold": 150, "despill_radius": 2, "documented_exception": null, "job_palette_note": "Global palette remap merges every distinct palette color present in the outer 8px border into that border’s most frequent base color. The remap applies globally to matching colors; it does not paint spatially. Raw source remains unchanged."}
