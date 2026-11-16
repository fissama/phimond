# farm-field-cabbage

Prompt: Pixel-art HD-2D sprite sheet on flat magenta; three distinct 3:2 farm plot tiles, wheat, cabbage, carrot; warm brown earth, ragged grass edges, detailed clustered pixels, no hard rectangle or shadow.

Image source: built-in image_gen. Raw sheet: `raw-01.png`, 1536x1024, SHA256 `79495948b6cfcfbfc307bcf00023583296bf85019e72cd5bb9138e6a43ef8269`.

References (content first, approved style, then two pet anchors):
- `.ai/design/gpt-redo/refs-v1.0.0/05-later/orig-map-city_farm.png` SHA256 `de83a948b76b83bf6a4b1648db49e7e70b1ece3798a07da2e71cf4c9b6f701c8`
- `.ai/design/gpt-redo/refs-v1.0.0/05-later/orig-level3_NongTrai-sprites-x3.png` SHA256 `1e6018ca1af90134384f2075aecfcd141702c839059a1971293b230eafed1420`
- `apps/game-web/art-src/hd2d/batch-01-octopath/grass-floor-01/final.png` SHA256 `792b3a1c25fb3be8671af1a4e119ef7af3bbd5a89dd22e42e14206317697524c`
- `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`

Processing: crop the magenta-keyed sheet cell, binary alpha, nearest-neighbor fit inside 8px safe margin to 384x256 (3x2 world units), median-cut palette to max 48.
