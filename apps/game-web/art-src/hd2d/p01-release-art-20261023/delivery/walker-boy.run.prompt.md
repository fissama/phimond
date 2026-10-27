Use case: sketch-to-render. Input1 is the AUTHORITATIVE8POSE walk skeleton, input2 is head/outfit identity ONLY. Draw square3x3sheet with exact8 poses row-major and9thcellblankmagenta. Follow NEAR/ORANGE leg geometry, FAR/BLUE leg geometry EXACTLY. Frame1 foreground leg reachesRIGHT, frame5foreground leg reachesLEFT/trails and crosses IN FRONT at crotch. Foreground arm goes backward in1, FORWARD across chest in5 unless occupied holding object. In frame5 the FORWARD leg is behind, darker; the trailingback leg is foreground, lighter. These are oppositelegcontacts. Do not repeat anatomical nearleg in front/right inboth1and5. Use only supplied head/torso reference and independently DRAW lowerbody per skeleton. Shade FAR leg and boot a very DARK COOL BROWN, foreground leg in warm light, preserve exact leg overlap. All8phase jointangles DIFFER; loading/passing/up transitions follow skeleton. Same torso length/headsize root and upper-left light; same footbaseline, subtle1pxbodybob. Pixelart48colors crisp dark1pxoutline final192cells, rich deliberatepixelclusters, pure#FF00FFbackground. No guides/skeleton/labels/text/shadows/trails drawn inoutput. Young boy, short brown spiky hair, ivory shirt brownvest, tan shorts and darkbrownboots. Arms exchange as skeleton.

Raw source: walker-boy.run.grid-raw-03.png; first8 actual cells row-major repacked losslessly, source grid [3, 3], gutter-only trim 8px; no pose edits. Final horizontal1536x192.

References:
- /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/p01-release-art-20261023/sources/male-walk-guide-v6/guide.png SHA256 aca7cea671152191631a69b82bc6e029774c2d7aac83ed2edd18999894ead819
- /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/p01-release-art-20261023/sources/walker-boy-head-torso-only-v3.png SHA256 66ebb57df925c22d021619b6672ef63d29837d8c9e394129732541ca9cb8a41e

Raw SHA256: facc75672e980b2d27219a768af2ad4deb34d56409d6b32799350c172d6ef6e3


Postprocess: Agent Sprite Forge v0.4.0 scale_frames.py (commit5324342), scale1/nearest/integer translations, torso-x registration, fixed192x192 canvas with96,184 anchor. Numeric QC does not approve anatomy, equipment or motion; Claude review still required.
