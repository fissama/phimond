Use case: sketch-to-render. Input1 is the AUTHORITATIVE8POSE walk skeleton, input2 is head/outfit identity ONLY. Draw square3x3sheet with exact8 poses row-major and9thcellblankmagenta. Follow NEAR/ORANGE leg geometry, FAR/BLUE leg geometry EXACTLY. Frame1 foreground leg reachesRIGHT, frame5foreground leg reachesLEFT/trails and crosses IN FRONT at crotch. Foreground arm goes backward in1, FORWARD across chest in5 unless occupied holding object. In frame5 the FORWARD leg is behind, darker; the trailingback leg is foreground, lighter. These are oppositelegcontacts. Do not repeat anatomical nearleg in front/right inboth1and5. Use only supplied head/torso reference and independently DRAW lowerbody per skeleton. Shade FAR leg and boot a very DARK COOL BROWN, foreground leg in warm light, preserve exact leg overlap. All8phase jointangles DIFFER; loading/passing/up transitions follow skeleton. Same torso length/headsize root and upper-left light; same footbaseline, subtle1pxbodybob. Pixelart48colors crisp dark1pxoutline final192cells, rich deliberatepixelclusters, pure#FF00FFbackground. No guides/skeleton/labels/text/shadows/trails drawn inoutput. Young girl, honeybrown braids tied yellowribbons, golden/ivory dress, brownboots. Input3 is identity's REDAPPLE held at chest with bothhands in ALL8frames; keepapple, hands staycarrying naturally while torso/braids sway and legs articulate. Legs followguide, arm swing replaced with natural steady applecarry.

Raw source: walker-girl.run.grid-raw-03.png; first8 actual cells row-major repacked losslessly, source grid [3, 3], gutter-only trim 8px; no pose edits. Final horizontal1536x192.

References:
- /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/p01-release-art-20261023/sources/male-walk-guide-v6/guide.png SHA256 aca7cea671152191631a69b82bc6e029774c2d7aac83ed2edd18999894ead819
- /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/p01-release-art-20261023/sources/walker-girl-head-torso-only-v3.png SHA256 cdc5242ee8635c1aab8abdc0a10585abfb38c43cf5257503a0d8f08e7e74b651
- /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/p01-release-art-20261023/sources/walker-girl-held-object-reference.png SHA256 d24f7eadfd0d7c465a81cfaa9fb1914c833eb80ed65e40977d9217f90916cbf0

Raw SHA256: 1742b8daaa5449b34d0d5ff122edd488a5215414091691b28a2dbc6a9f3a4c27


Postprocess: Agent Sprite Forge v0.4.0 scale_frames.py (commit5324342), scale1/nearest/integer translations, torso-x registration, fixed192x192 canvas with96,184 anchor. Numeric QC does not approve anatomy, equipment or motion; Claude review still required.
