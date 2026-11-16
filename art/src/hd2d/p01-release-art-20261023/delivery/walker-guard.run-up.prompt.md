Use case: precise-object-edit. Image1 EDIT TARGET is an eight pose walking sprite source, image2 IDENTITY AND HELD PROP reference only. Restore the missing long upright wooden spear with steel point, in anatomical RIGHT hand, at screen RIGHT in back view, tip above helmet in ALL EIGHT poses. Preserve exact eight distinct leg poses, face/hair/outfit, body scale, lighting, composition and direction from image1. Hands must actually grip object; occupied arms hold it instead of pumping. Direction AWAY from viewer, back view. Exactly 3x3 equal cells, eight full figures row-major, bottom-right cell EMPTY. Keep all bodies and props wholly inside own cell, generous margins, common root/baseline. Flat #FF00FF background, no grid/labels/shadows. Crisp pixel art matching references, dark outline, upper-left warm light, cool shadows, shared <=48 colors. NO extra figures, no mirroring, no new equipment. Do not replace animation with identical idle poses. Final delivery will be eight 192x192 frames with feet at96,184.

Raw source: walker-guard.run-up.grid-props-v6.png; first8 actual cells row-major repacked losslessly, source grid [3, 3], gutter-only trim 0px; no pose edits. Final horizontal1536x192.

References:
- /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/p01-release-art-20261023/sources/walker-guard.run-up.grid-raw-02.png SHA256 1b8e37518bdc822c5098e2e237dd0ca8a6a2c9f263bbcc53fe498fba787d64d1
- /Users/phileanh/rust/phimond/apps/client/public/hd2d/walker-guard.png SHA256 7c2c1d8d57ac42c52321e3c51fd0d975d898e63d8543593d8d9701f6da4b81e8

Raw SHA256: 77ff591b790d1eea71567331af20d76de64452cc050590aad7e2edf0c347a84b


Postprocess: Agent Sprite Forge v0.4.0 scale_frames.py (commit5324342), scale1/nearest/integer translations, torso-x registration, fixed192x192 canvas with96,184 anchor. Numeric QC does not approve anatomy, equipment or motion; Claude review still required.
