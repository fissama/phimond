# Carved emerald column with floral capital — candidate

Use case: HD-2D pixel-art map prop. Subject: Carved emerald column with floral capital. Source map image supplies content and colors; approved batch-01 Octopath art supplies style; two pet sheets supply outline/shading anchors only. Built-in Codex image_gen generated a six-item sheet; this sprite was cropped and keyed using magenta flood-fill from the sheet boundary. No artwork repaint, mirroring or code drawing.

Attached references and SHA-256:
- `.ai/design/map-checklists/refs/ancient_ruins_unnamed_area_01.jpg` — `85f51b9e8aa7bd9760b201ecacfc12f4decdb9c97af13dd69c96f948f6786475`
- `apps/game-web/art-src/hd2d/batch-01-octopath/rock-small/final.png` — `880eddcf56b10952735033d68d3f8b97c4e8412933a383fa08317ca2fca1445f`
- `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`
- `raw-01.png` (source sheet 1) — `78d46962fa74136b8cced29baf5afe4bcc0c1e85264df811757aa7be0843ea01`

Route: built-in image_gen (model identifier not exposed). Finish: flood-fill chroma-key from magenta sheet boundary, silhouette crop, 8px transparent margin, binary alpha, nondithered palette quantization up to 48 opaque RGB colors.
