Use case: precise-object-edit. Image1 EDIT TARGET is an eight pose walking sprite source, image2 IDENTITY AND HELD PROP reference only. Restore the missing woven basket of bread/produce held in both hands in front of waist, identical to idle reference in ALL EIGHT poses. Preserve exact eight distinct leg poses, face/hair/outfit, body scale, lighting, composition and direction from image1. Hands must actually grip object; occupied arms hold it instead of pumping. Direction TOWARD viewer, front view. Exactly 3x3 equal cells, eight full figures row-major, bottom-right cell EMPTY. Keep all bodies and props wholly inside own cell, generous margins, common root/baseline. Flat #FF00FF background, no grid/labels/shadows. Crisp pixel art matching references, dark outline, upper-left warm light, cool shadows, shared <=48 colors. NO extra figures, no mirroring, no new equipment. Do not replace animation with identical idle poses. Final delivery will be eight 192x192 frames with feet at96,184.

Raw source: walker-baker.run-down.grid-props-v6.png; first8 actual cells row-major repacked losslessly, source grid [3, 3], gutter-only trim 0px; no pose edits. Final horizontal1536x192.

References:
- /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/p01-release-art-20261023/sources/walker-baker.run-down.grid-raw-02.png SHA256 9b0b3e795758471e7e1ad9a6c7d74ffa930442e524667d1caa7116b626c0ac8d
- /Users/phileanh/rust/phimond/apps/client/public/hd2d/walker-baker.png SHA256 1a39d14bee8806039730f58d964e9469cbba08f65fc5476f6b89c9a3b393b80f

Raw SHA256: 07749fe1bcb2707909adee776376d7f36ade7129bc5d8da5ef02e3fec1ae6456


Postprocess: Agent Sprite Forge v0.4.0 scale_frames.py (commit5324342), scale1/nearest/integer translations, torso-x registration, fixed192x192 canvas with96,184 anchor. Numeric QC does not approve anatomy, equipment or motion; Claude review still required.
