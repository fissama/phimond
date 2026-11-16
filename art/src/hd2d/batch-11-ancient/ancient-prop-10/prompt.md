# Tall emerald crystal on carved foot — four-frame crystal pulse candidate

Use case: 4-frame HD-2D game prop animation. Source Ancient map image defines content and palette; approved Octopath pixels and pet sheets set style/outline. Built-in image_gen produced the 4x3 source sheet. Each row was sliced into four frame cells and assembled horizontally with bottom-center registration; no artwork painted or mirrored.

Attached references and SHA-256:
- `.ai/design/map-checklists/refs/ancient_ruins_unnamed_area_03.jpg` — `421da2e3338eec7f89e10c18bd2b603ea815b83462dc37fe015321cf3a14229c`
- `apps/game-web/art-src/hd2d/batch-01-octopath/rock-small/final.png` — `880eddcf56b10952735033d68d3f8b97c4e8412933a383fa08317ca2fca1445f`
- `apps/game-web/art-src/hd2d/batch-11-ancient/raw-prop-sheet-02.png` — `7ebb4f923cbb2e1a312cdfa27f9a408b3e17e712a630241d577b4d39cbc75687`
- `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`
- `raw-01.png` original static source — `7ebb4f923cbb2e1a312cdfa27f9a408b3e17e712a630241d577b4d39cbc75687`
- `raw-02.png` generated 4x3 animation sheet — `dff3575750573ddb7d34b23e604df227781b3e45604d27e84b65821a76cb202c`

Route: built-in image_gen (model identifier not exposed). Finish: magenta boundary flood-fill, frame cell extraction, binary alpha, shared nondithered palette up to 48 opaque RGB colors. Frame layout: four frames horizontal, frame size 171x323, bottom-center aligned.
