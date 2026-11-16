Create a SQUARE3x3 equal-cell animation source:8 FULL-BODY poses read row-major, ninthcell EMPTYmagenta. This is one8frame looping WALK action, not8idlevariants. Pure#FF00FF background throughout, no captions/grid/numbers/shadows/trails. Same identity/costume as supplied reference, no added objects. Crisp production pixel art, upperleftlight,48colorpalette, one shared body scale and head size, 1pxdarkoutline at192finalscale, no antialias. Each pose fullycontained in cell with generous margin; constant root and baseline; subtle2px bob max, full person168px in final192cell. Final packaging will be8cells in one horizontal1536x192strip. Each phase independently drawn, do not repeat/mirror halfcycle. Input1 controls geometry EXACTLY, input2 head/costume. ORANGE guide limbs are NEAR foreground, BLUE are FAR background; guidecolors are not clothing colors! Brown boots on BOTH legs, actual costume on bothlegs, farleg only a darker shade. Contactframe1NEARleg forwardRIGHT; contactframe5NEARleg trailsLEFT drawn IN FRONT while FARleg leadsRIGHT. Neararm swings BACK inframe1 and FORWARD across torso inframe5. Preserve near/far OCCLUSION so halves truly exchange legs. Request aspect 1:1. Do not state pixel sizes: the host image tool keeps the aspect and
returns about 1254x1254 for it (area about 1,572,864 px).
Attach guide.png as a layout and pose reference only. Do not draw any of its lines, boxes, colours,
grey bands or stick figures.
- 8 poses in 3 rows x 3 columns, read left to right, top row first; leave the last 1 cell(s) empty.
- The grey band around every cell is empty gutter: no pixel of the character may enter it.
- Keep the whole character (ears, tail, both feet, held items) inside the blue safe box of its cell.
- The black line is the ground and the tick is the fixed root: one body scale and one root in every cell.
- The character faces RIGHT in every cell.
- Match each cell's stick pose. ORANGE limbs are NEAR limbs (viewer side): normal brightness, drawn in
  front. BLUE limbs are FAR limbs (away side): one shade darker, partly hidden behind the body.
Poses (NEAR/FAR, never left/right):
0 contact: NEAR leg reaches forward, heel on the ground line; FAR leg trails, heel lifted.
1 down: NEAR leg under the body, knee bent, carrying the weight; FAR leg folds up behind.
2 passing: NEAR leg pushes off behind; FAR knee swings forward past it.
3 up: NEAR leg straightens under the body (highest hip); FAR foot swings forward, just clear of the ground.
4 contact: FAR leg reaches forward, heel on the ground line; NEAR leg trails, heel lifted.
5 down: FAR leg under the body, knee bent, carrying the weight; NEAR leg folds up behind.
6 passing: FAR leg pushes off behind; NEAR knee swings forward past it.
7 up: FAR leg straightens under the body (highest hip); NEAR foot swings forward, just clear of the ground.
Frames 4-7 must not repeat frames 0-3: the leg drawn in front swaps between NEAR and FAR.
Background: real transparency, or one flat chroma colour absent from the character.
No text, labels, numbers, grid lines, shadows, dust or checkerboard.

After generation: run sheet_qc.py spill on the raw sheet, then sheet_qc.py frames --cycle walk.
If the leading-leg test reports a duplicated half-cycle, regenerate only the second half,
attaching the first half and this guide.
 Follow guide EXACTLY especially middlecenter frame5. Near arm FORWARD and near leg BACK, do not keep near arm backward in both contacts. Pose geometry overrides reference stance.

Raw source: player-female.run.grid-raw-03.png; first8 cells of3x3 row-major repacked losslessly, no pose edits. Final horizontal1536x192.

References:
- /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/p01-release-art-20261023/sources/male-walk-guide-v6/guide.png SHA256 aca7cea671152191631a69b82bc6e029774c2d7aac83ed2edd18999894ead819
- /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/p01-release-art-20261023/sources/player-female-upperbody-reference.png SHA256 733eec530ccffe41ffcc8e69a76d039048603941c5de97ec761598496fbe4482

Raw SHA256: 206f470d9142af3e6413f84dbecc641cda8fa7aa0ac45e8d56b13e25cd53b3c9


Postprocess: Agent Sprite Forge v0.4.0 scale_frames.py (commit5324342), scale1/nearest/integer translations, torso-x registration, fixed192x192 canvas with96,184 anchor. Numeric QC does not approve anatomy, equipment or motion; Claude review still required.
