# Image generation provenance

Route: host_image / built-in image_gen
Model: not exposed by tool
Source job: forest-a-sheet

## Attempt 1

Use case: stylized-concept. Asset type: isolated production game sprite sheet for Phimond HD-2D. Reference image 1 is CONTENT only: original emerald forest. Images 2 and 3 are STYLE only: approved pets, match hard pixel clusters, colored dark outline and 2–4 shade ramps, no smooth painting. Create exactly SIX separate sprites in a regular 3 column x 2 row grid on a 1536x1024 genuinely transparent canvas. Each cell 512x512, centered horizontally, baseline y=480 within cell, at least 32px clear space inside every cell. Top row: large full broadleaf emerald forest tree (whole trunk AND foliage, total height 410 pixels), round bush (height 145 pixels), upright grass clump (height 65 pixels). Bottom row: small yellow wildflower cluster (height 80px), pink wildflower cluster (height 80px), fern grass clump (height 80px). Tree crown full and rounded, roots visible; warm olive highlights, emerald mids, cool dark teal shade, earthy umber trunk, source's pink and yellow accents. Front billboard view seen slightly from above 24 degrees. Large crisp pixel blocks, 2px logical pixels, hue tinted outline. This is variant A, faithful warm lush original palette. All six independent, no shared ground, no shadows on ground, no scenery, no fog, no glow, no text, no labels, no borders. Export image to disk and return output path.

## Attempt 2

Edit the first input image ONLY to remove ALL colored haze, glow, fog and background surrounding its six sprites. Preserve the tree, shrub, grass and three flower/fern sprites pixel-for-pixel in design and palette. Put each complete object on completely empty TRANSPARENT alpha=0 background, the solid interior of every object must be fully opaque alpha=255. No colored atmospheric clouds, no gradients outside objects, no ground cast shadows whatsoever. Keep all six objects distinct with wide gaps; enlarge canvas margins if necessary to preserve the entire tree silhouette. Do not add text, labels or frames. These are cutout production pixel sprites, not a presentation poster.

## Attempt 3

Use case: stylized-concept. Create a PRODUCTION CUTOUT SPRITE PACK on a completely flat pure #FF00FF magenta background. NO transparency effect, NO gradient, NO glow or haze, NO cast shadows. Exactly six separate isolated forest objects, no overlaps, no ground patches, no labels: one full large broadleaf forest tree on left taking full height with a clear margin; at upper right one rounded bush; at lower right four small separate clumps: grass blades, yellow wildflowers, pink wildflowers, fern. Each silhouette completely contained and separated by wide blank magenta gaps. First reference is original forest content (brown trunk, lime/emerald foliage, pink and yellow flowers). Next two references are approved pet pixel style only. Crisp clean PIXEL ART, visible square pixel clusters and dark hue-tinted outlines, only 4 tones per material and 40 total solid colors per prop, NO antialiasing. Warm light upper left, cooler shade. Standing front billboards, seen slightly from above about 24 degrees. This is variant A: rich warm emerald and yellow-green. Flat key background must remain EXACTLY pure solid magenta up to the hard opaque object boundary, no painted lighting on background. Empty space on all four sides of every object. Do not paint any pixels resembling shadow underneath.

## Ordered source references (first generation)

- /Users/phileanh/Downloads/Phimond-P12-Review/map-images/emerald_forest_main_woods.png — sha256 8dd000bbab532d975e304b17374effa743a80f2bb6c28a27a231b2db84683cef
- /Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png — sha256 fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da
- /Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png — sha256 043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3

Image-edit attempts use the previous raw as their edit target, as recorded in generation-jobs.json.

## Raw SHA256

- raw-01.png: 61e8f35a527adefbad4827624eb1e2f9920c39e16deb807439bcb30db9384e0f
- raw-02.png: af94f8842830ee4e0d5e3a7af46b69feed53999cdd306e7a1c6108fdcf736e58
- raw-03.png: 8cccde45bcd91b0853e8fe895dd79f86557216c62fd655eee6a377899f5af1ba
