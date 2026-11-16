# tomb-tile-edge-decal — redraw 03

Route: built-in image_gen. Prompt: “Create a single dark blue-gray crypt slate texture tile. Use very small broken slate chips embedded in a nearly uniform dark substrate; each chip should be only a tiny mark, not a whole recognizable stone, so tiling does not reveal repeated large forms. Add sparse moss-green pixels and restrained subtle texture. Calm, evenly distributed surface with no focal point. Treat the image as wraparound: left/right and top/bottom edges must match continuously. Pixelated clustered shapes, low contrast, 33–48 colors. Avoid large stones, boulders, cobbles, pavers, slabs, mortar grid, brick rows, large cracks, bands, photographic grain, blur, shadows, gradients, text or watermark.”

Raw: `raw-02.png` (the original `raw-01.png` and prior selected output are preserved). Processing: center-square crop `0,0,1254,1254`, nearest resize to 512×512, nondithered median-cut palette to 48 colors. No painting, mirroring, edge synthesis or manual pixel edits.

Raw SHA256: `8de22edb2f93808dbef30c0e99ea7330f00d52898c45f232f77cf352706567f8`
Final SHA256: `592e8bcdc6c84e37542632901802cb44079412dee345ede44d21fed88a221179`
QA: 48 colors; seam mean X=3.585, Y=5.775; both within the 6 threshold. Viewed 4× dark/checker and 3×3 repeat. Candidate remains `approved:false` pending owner review.
