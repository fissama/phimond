# windrock-edge-03

Route: built-in image_gen. Draft awaiting Claude/owner review.

Primary request: dry grass and scree lip for the Windrock HD-2D top-down game. Use the original Windrock map reference for environment and the approved Octopath terrain asset for pixel-cluster finish. Keep the palette slate blue-gray #7B8794/#566070, dry alpine grass #8A8F4E, sparse cold snow #E8EEF4. Draw exactly one shallow terrain-transition strip with an irregular silhouette, varied stone widths/orientations and compact shadowing; keep the left/right ends tileable without a repeated interior rhythm. True transparency outside the strip; no panel sheet, landscape backdrop, ground tile, detached objects, haze, glow, blur, text or watermark.

Generated raw image: `raw-01.png` (2171×724 RGBA), retained byte-identically. Production finishing only: selected source crop `[498, 261, 1458, 501]` (960×240), nearest-neighbor resize to 512×128, alpha threshold to binary, set RGB below zero-alpha pixels to black for clean seam measurement, non-dithered palette reduction to at most 64 colors. No artwork was painted or mirrored by code.

Reference files: .ai/design/map-checklists/refs/windrock_mountain_camp.jpg; apps/game-web/art-src/hd2d/batch-01-octopath/edge-grass-roots/final.png.
