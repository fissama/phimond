# gd-seal-strip-lit — generation record

Built-in image_gen output `exec-598c0abc-0021-4716-bcdb-41f6d53825fb.png` saved as `raw-03.png`. Source image SHA-256: `b866559120112028581a2614401215c1793796efd95f8dfb46d210609389e369`.

Target canvas: 512×160. Processing: nearest-neighbor resize; alpha thresholded to binary; palette reduced to at most 48 colors. Pillar vein was clipped to the existing pillar-01 alpha silhouette to enforce the overlay mask. No edge pixels were copied or seam-patched.

Acceptance measurements are in `qa.json`. Status is pending Claude review; known failed thresholds remain visible there.

Reference set for audit (SHA-256):
- `apps/game-web/art-src/hd2d/batch-01-octopath/moss-pillar/final.png` — `0aed2ada19159c0e228b8d12dde6e3807d07cbcfd9a1d99f7054ffa8ef64d84b`
- `apps/game-web/art-src/hd2d/batch-01-octopath/pebbles-01/final.png` — `328f80aff0c2acab7ba50d1ce79604854a00c2b481548f6b7267703d0a4c8e8a`
- `apps/game-web/art-src/hd2d/garden-a/gd-seal-strip/final-before-redraw-20261106.png` — `65c8ab7abfe81b4ebd8d1a513be590f9d8dcd53599ca378e7154138a38cd6c59`
- `apps/game-web/art-src/hd2d/garden-a/gd-seal-strip-lit/final-before-redraw-20261106.png` — `49e2896f74b0539bfc8202725cb5936e30a769f0e460cfd9c76a3f4ff23a1a84`

