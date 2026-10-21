# Generation provenance

## raw-01.png

Use case: production HD-2D GAME PARALLAX LAYER SHEET, not an illustration. FOUR separate rectangular 16:9 panels in TWO ROWS TWO COLUMNS, exactly aligned grid, 64px solid #FF00FF gutters all around and between panels. Aim 3072x1728 artwork resolution or higher so each panel retains crisp pixel detail. ALL four panels depict DIFFERENT ISOLATED DEPTH LAYERS of ONE login view, same camera/coordinate frame. No panel labels.
REFERENCE ROLES IN ORDER: image1 original game content only (broad emerald forest, rustic architecture). Image2 APPROVED Phimond forest canopy STYLE: match its exact jagged broad leaf clusters, olive/sage/umber ramps and colored dark contour. Image3 APPROVED town facade STYLE+architecture: match its ivory stone, umber framing and terracotta turrets, clustered pixel shading. Images4–5 pet atlas anchors: match edge crispness and 2–4-tone shading ONLY, NO creatures in this sheet. The target is indistinguishable from the actual supplied Phimond environment assets; do not substitute a painted Octopath concept illustration.
Each panel uses a virtual 1280x720 viewport:
TOP LEFT panel = SKY ONLY, opaque rectangle, pale apricot near bottom to desaturated blue-gray above in broad deliberately stepped pixel-color bands. A few long broken ivory pixel-cloud clusters. No sun disc, rays, mountains, land, fog, glow, smooth gradient or other depth layers. This rectangle fills panel.
TOP RIGHT panel = CITADEL ONLY on flat pure MAGENTA background above its silhouette. At viewport x~820 a compact white-limestone royal citadel with warm terracotta turret roofs on a gently rolling stone ridge, smaller slate-roof town roofs extending x~350..1100. Highest turret top near y230, ridge at y490, opaque ochre stone/olive lowground continues down to y720 with NO magenta underneath. Building visual language exactly reference3, not a Gothic castle or Disney spire. No sky, trees, clouds, rays, haze or horizon gradient in this layer. Crisp pixel stepped silhouette.
BOTTOM LEFT panel = FOREST ONLY on pure flat MAGENTA above its silhouette. Dense broadleaf woodland wall spanning whole panel width. Canopy tops near y430, varied crowns and visible short dark trunks toward bottom. Leaf rendering EXACTLY image2 with broad leafsprays, dark olive underplanes, sage highlights, weathered umber bark. Low undergrowth opaque through bottom y720. No sky, castle, mountains, path, glow, fog, sunbeams or backdrop atmosphere. Forest should be lower at center/right so citadel from other layer remains visible after composition.
BOTTOM RIGHT panel = FOREGROUND ONLY, solid MAGENTA in upper~80percent viewport. A low irregular leafy/fern/flower edge across bottom y610..720, small weathered mossy rocks near x120 and x1150, a visible strip of warm worn earth winding into center. Exactly same plant pixel clusters as image2, ochre/cream/red flower accents sparse, no tall tree or building. Opaque land continues all way to bottom. No sky, castle, forestwall, rays or mist.
HARD STYLE: true clean PIXEL ART. Deliberate broad 3–6px step clusters at final1280 viewport, 2–4 tone ramps per material, subtle upperleft warm form shading and cool hue-tinted dark outlines. No smooth antialias, airbrush, painterly brush strokes, photographic foliage noise, tiny dithering, glassy 3D surfaces, bloom or atmospheric perspective. Controlled earthy saturation; no neon greens. Restrained detailed material shapes like refs2/3, not flat minimal vector.
Every panel has a clean 16:9 canvas with side/bottom coverage designed to overlap, no drop shadows. EXACT solid #FF00FF replaces all empty pixels of layers2–4. Keep each panel separated by wide solidmagenta gutters so extraction never cuts into another layer. No text, logo, runes, numbers, labels, UI, characters or pets ANYWHERE. Produce only these four layer paintings, never a composite panorama.

Route: built-in image_gen; model not exposed.
Raw SHA256: 2806e5ca37db6eba94a69e3a5fea8f215f836935b0550be14c1788a141d154b6

Actual ordered attachments:
1. /Users/phileanh/rust/phimond/apps/game-client/assets/extracted/extended/rooms/sbw_v32_Texture2D_2020_06_14_231047_1470x603.png — SHA256 0ac16674537cf02c6f705e3481f31b37001a5303c7ec1065912a4dc5b7d648f1
2. /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-01-octopath/tree-large-01-canopy/final.png — SHA256 b3e4766280e267080c757ecc5c1230a8713594e8d5fd329d4d5359f9a8798fdb
3. /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-02-octopath/city-facade-townhouse/final.png — SHA256 57c926e3ba82ed8af80f01f1234c27156002491ca5267881e7ba40bdd2efe060
4. /Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png — SHA256 fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da
5. /Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png — SHA256 043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3

## raw-02.png

Precise production layout correction to the attached4layer2x2 SHEET. Keep the exact sheet size, panel boundaries,64px-style magenta gutters, TOP LEFT sky, TOP RIGHT citadel and BOTTOM RIGHT foreground PIXEL IDENTICAL wherever possible. Correct ONLY BOTTOM LEFT FOREST panel: it is far too tall and would conceal the citadel after layering. REDRAW the forest as a LOW broadleaf woodland band entirely within the LOWER40percent of its own16:9panel. Upper60percent of that panel must be pure flat #FF00FF. Across the whole panel width use many lower rounded tree crowns, short occasional umber trunks and underbrush, height around250logicalpixels in1280x720viewport, canopy tops atlogicaly430..490 and opaque bottomy720. Do not simply crop off tree tops or squash tall trees: draw naturally squat distant broad crowns at smaller scale and densely connected side-to-side. Keep exactly the same approved leaf spray drawing vocabulary as foreststyleattachment2: discrete broad olive/sage leafclusters,2-4toneplanes, dark green hue-tinted outlines, warm subtleupperleft formkey, no stippledgrain or painterlytexture. Both left/right ends of forest continue off panel (backdropband) but are not cut inside its bounds. No sky, atmosphere, castle, fog, rays, glow, smoothgradient, letters, labels or anything in uppermagenta region. Preserve all other3panels, their actual composition, color, lack oftext and exact relative dimensions. Every panel isolated, gutters uninterrupted #FF00FF. References order: original sheet edit target, approved foreststyle asset, approved townstyle asset,2petanchors for pixelcompatibility only.

Route: built-in image_gen; model not exposed.
Raw SHA256: aca06c5aca9b7934c3a0527bcb970d6f7c918e0f69b5379dd3403e510c04cf11

Actual ordered attachments:
1. /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-10-octopath/jobs/login-stage-a/raw-01.png — SHA256 2806e5ca37db6eba94a69e3a5fea8f215f836935b0550be14c1788a141d154b6
2. /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-01-octopath/tree-large-01-canopy/final.png — SHA256 b3e4766280e267080c757ecc5c1230a8713594e8d5fd329d4d5359f9a8798fdb
3. /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-02-octopath/city-facade-townhouse/final.png — SHA256 57c926e3ba82ed8af80f01f1234c27156002491ca5267881e7ba40bdd2efe060
4. /Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png — SHA256 fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da
5. /Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png — SHA256 043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3

## raw-03.png

Targeted final pixel-art correction of the attached2x2four-layer sheet. Keep citadel TOP RIGHT and foreground BOTTOM RIGHT unchanged. Fix ONLY sky TOP LEFT and forest BOTTOM LEFT.
SKY: remove the fine grain and almost-smooth gradient. Replace blue-to-paleapricot sky transition with visibly STEPPED broad pixel-color bands (12–16 distinct flat color levels) and broken cluster-shaped boundaries, no dithering, no painterly streaks. Keep existing cream chunky pixel clouds. Fill same complete sky rectangle, no sun or rays.
FOREST: make band LOWER yet again. In the existing bottomleft rectangular panel, magenta must occupy its entire TOP TWO THIRDS. All visible forest pixels fit in its BOTTOM ONE THIRD, except a few small crown bumps extending10px above. At final1280x720 this means forest silhouettes start at y~470 and end at720. Draw SMALLER squat broad rounded crowns in a continuous dense woodland band, occasional tiny umber trunk gaps; do not squash or crop talltrees. Preserve exact clustered olive/sage leaf rendering from style reference2 and dark green outline. No haze/glow or fine noisy speckles. Full panel width, opaque forest base continues to panel bottom, same64pxmagenta gutters outside panel untouched.
Exact original whole sheet size and equal panel rectangles. #FF00FF everywhere empty, never sky-colored fill in forest panel. No labels,text,logos,numbers,characters,fog,airbrush orphototextures. Reference1 edit target;2approvedforeststyle;3approvedtownstyle;4–5petpixelcompatibilityonly. Target exact Phimond batch00–09 pixel vocabulary, not painted conceptart.

Route: built-in image_gen; model not exposed.
Raw SHA256: 167412a7485c4c797b6d97256d3499a87ef99a9c246ecdb2b1308c17d6655256

Actual ordered attachments:
1. /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-10-octopath/jobs/login-stage-a/raw-02.png — SHA256 aca06c5aca9b7934c3a0527bcb970d6f7c918e0f69b5379dd3403e510c04cf11
2. /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-01-octopath/tree-large-01-canopy/final.png — SHA256 b3e4766280e267080c757ecc5c1230a8713594e8d5fd329d4d5359f9a8798fdb
3. /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-02-octopath/city-facade-townhouse/final.png — SHA256 57c926e3ba82ed8af80f01f1234c27156002491ca5267881e7ba40bdd2efe060
4. /Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png — SHA256 fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da
5. /Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png — SHA256 043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3

## raw-04.png

Edit this Phimond login production sheet. Image1 is an EDIT TARGET and content/layout reference only, NOT a style reference. Image2 approved batch01 canopy and image3 approved batch02 facade are STYLE authorities; images4/5 spirit pets are outline and dimensional shading anchors only, do not add creatures.
Preserve the exact 2x2 sheet geometry of image1 (1672x941), 21px outer margin,40px gutters, panel bounds approximately [21,21,816,457],[857,21,1652,457],[21,484,816,920],[857,484,1652,920]. Preserve the two upper panels as they are.
Change ONLY the lower two panels with these owner-requested small revisions:
BOTTOM LEFT forest: keep this as a LOW woodland strip occupying only bottom third of its panel, magenta above. Break up the repetitive yellow star leaf sprays. At least TWO clearly distinct foliage cluster types: irregular oak-like rounded broadleaf masses with olive/sage planes and occasional small maple-like sprays; occasional narrow upright cool green foliage among warm broadleaf crowns. Different sizes, silhouettes, and gaps between branch forks. Avoid regular repeating trees. Much less saturated yellow; retain warm upper-left highlights but mostly muted greens. Umber trunks visible in places. Continuous opaque earth/leaf base across full panel bottom (at least 50px tall). Match image2's pixel clusters and material shading exactly; 2-4 tones each material, about44 final colors.
BOTTOM RIGHT foreground: retain low ferns, boulders and worn ochre center path; remove at least three quarters of flowers on BOTH sides. Just one tiny flower group on each side, with most plants now broadleaf grass/fern. Keep ochre center path clear. Full opaque earth bottom across panel. Keep top ~65percent solid #FF00FF for cutout.
Render game pixel art like the approved batch01/02, Octopath Traveler-like weathered materials with sharp visible pixel clusters, not painterly illustration. No fog, glow, ground shadows, text, grid lines, characters, gradients or new backdrop. All empty areas and gutters absolutely flat #FF00FF. No magenta antialias or fringe. Do not alter or crop sheet layout.

Route: built-in image_gen; model not exposed.
Raw SHA256: b8eaf99d87662c4a1bf34042ca8dacd92a450b028263c24d62d9d2392c14d4c0

Actual ordered attachments:
1. /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-10-octopath/jobs/login-stage-a/raw-03.png — SHA256 167412a7485c4c797b6d97256d3499a87ef99a9c246ecdb2b1308c17d6655256
2. /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-01-octopath/tree-large-01-canopy/final.png — SHA256 b3e4766280e267080c757ecc5c1230a8713594e8d5fd329d4d5359f9a8798fdb
3. /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-02-octopath/city-facade-townhouse/final.png — SHA256 57c926e3ba82ed8af80f01f1234c27156002491ca5267881e7ba40bdd2efe060
4. /Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png — SHA256 fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da
5. /Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png — SHA256 043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3

Selected source: raw-04.png; measured source box: [860, 487, 1649, 917]. Palette: palette/forest.json. Nearest resize to1280x720. No repaint, synthesized pixels, mirroring, glow or alpha fade.
