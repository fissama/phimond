Use case: precise-object-edit. Image1 EDIT TARGET is an eight pose walking sprite source, image2 IDENTITY AND HELD PROP reference only. Restore the missing wooden walking cane held in his anatomical LEFT hand, at screen RIGHT, extending from hand down to ground in ALL EIGHT poses. Preserve exact eight distinct leg poses, face/hair/outfit, body scale, lighting, composition and direction from image1. Hands must actually grip object; occupied arms hold it instead of pumping. Direction TOWARD viewer, front view. Exactly 3x3 equal cells, eight full figures row-major, bottom-right cell EMPTY. Keep all bodies and props wholly inside own cell, generous margins, common root/baseline. Flat #FF00FF background, no grid/labels/shadows. Crisp pixel art matching references, dark outline, upper-left warm light, cool shadows, shared <=48 colors. NO extra figures, no mirroring, no new equipment. Do not replace animation with identical idle poses. Final delivery will be eight 192x192 frames with feet at96,184.

Raw source: walker-elder.run-down.grid-props-v6.png; first8 actual cells row-major repacked losslessly, source grid [3, 3], gutter-only trim 0px; no pose edits. Final horizontal1536x192.

References:
- /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/p01-release-art-20261023/sources/walker-elder.run-down.grid-raw-02.png SHA256 a2e68b1d96e52e3df6d8fc2492e085f925e091c6a2e7ddb4ac2ea759bd49a693
- /Users/phileanh/rust/phimond/apps/client/public/hd2d/walker-elder.png SHA256 6036fb6ca92298f7dfb07f4028a637d240fedfce3afa57a094ce8a47cdb84a3f

Raw SHA256: 9336838cc06a187c43b452e927af29e8e8a3be58ed43880b4933da55fb841b9f


Postprocess: Agent Sprite Forge v0.4.0 scale_frames.py (commit5324342), scale1/nearest/integer translations, torso-x registration, fixed192x192 canvas with96,184 anchor. Numeric QC does not approve anatomy, equipment or motion; Claude review still required.
