Use case: precise-object-edit. Image1 EDIT TARGET is an eight pose walking sprite source, image2 IDENTITY AND HELD PROP reference only. Restore the missing one red apple held in both hands in front of chest, like idle reference in ALL EIGHT poses. Preserve exact eight distinct leg poses, face/hair/outfit, body scale, lighting, composition and direction from image1. Hands must actually grip object; occupied arms hold it instead of pumping. Direction TOWARD viewer, front view. Exactly 3x3 equal cells, eight full figures row-major, bottom-right cell EMPTY. Keep all bodies and props wholly inside own cell, generous margins, common root/baseline. Flat #FF00FF background, no grid/labels/shadows. Crisp pixel art matching references, dark outline, upper-left warm light, cool shadows, shared <=48 colors. NO extra figures, no mirroring, no new equipment. Do not replace animation with identical idle poses. Final delivery will be eight 192x192 frames with feet at96,184.

Raw source: walker-girl.run-down.grid-props-v6.png; first8 actual cells row-major repacked losslessly, source grid [3, 3], gutter-only trim 0px; no pose edits. Final horizontal1536x192.

References:
- /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/p01-release-art-20261023/sources/walker-girl.run-down.grid-raw-02.png SHA256 91e3f5c9e46f22560a9233a72f78f696a7b6f2138424f4aa75d163e42d350110
- /Users/phileanh/rust/phimond/apps/client/public/hd2d/walker-girl.png SHA256 c4bcce6724b529d9729563ba944dccb46552a418b28ddc4da7a73987bdcf0621

Raw SHA256: ae895a81f6df1d04e977f0aa0d456eeba11c374f57b141a19f6a4e53b0d9a901


Postprocess: Agent Sprite Forge v0.4.0 scale_frames.py (commit5324342), scale1/nearest/integer translations, torso-x registration, fixed192x192 canvas with96,184 anchor. Numeric QC does not approve anatomy, equipment or motion; Claude review still required.
