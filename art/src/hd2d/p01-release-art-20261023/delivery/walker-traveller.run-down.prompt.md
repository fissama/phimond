Use case: precise-object-edit. Image1 EDIT TARGET is an eight pose walking sprite source, image2 IDENTITY AND HELD PROP reference only. Restore the missing wooden travelling staff held in anatomical LEFT hand, at screen RIGHT, hand to ground; preserve backpack, bedroll and bags in ALL EIGHT poses. Preserve exact eight distinct leg poses, face/hair/outfit, body scale, lighting, composition and direction from image1. Hands must actually grip object; occupied arms hold it instead of pumping. Direction TOWARD viewer, front view. Exactly 3x3 equal cells, eight full figures row-major, bottom-right cell EMPTY. Keep all bodies and props wholly inside own cell, generous margins, common root/baseline. Flat #FF00FF background, no grid/labels/shadows. Crisp pixel art matching references, dark outline, upper-left warm light, cool shadows, shared <=48 colors. NO extra figures, no mirroring, no new equipment. Do not replace animation with identical idle poses. Final delivery will be eight 192x192 frames with feet at96,184.

Raw source: walker-traveller.run-down.grid-props-v6.png; first8 actual cells row-major repacked losslessly, source grid [3, 3], gutter-only trim 0px; no pose edits. Final horizontal1536x192.

References:
- /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/p01-release-art-20261023/sources/walker-traveller.run-down.grid-raw-02.png SHA256 1ee8b123c1684cfedc8a63dae48762a8e7479ed0460f2cf8aede4cbf0671f88b
- /Users/phileanh/rust/phimond/apps/client/public/hd2d/walker-traveller.png SHA256 f617ecc0e416f3d380d24fd12ba8f99a729bbdafb867a330875a5ec7d965c5c0

Raw SHA256: 74a134507edc45a9d9893197ed6edcbcdd52d6cfefcb5f978479cc3bf749c0ef


Postprocess: Agent Sprite Forge v0.4.0 scale_frames.py (commit5324342), scale1/nearest/integer translations, torso-x registration, fixed192x192 canvas with96,184 anchor. Numeric QC does not approve anatomy, equipment or motion; Claude review still required.
