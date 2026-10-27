Use case: sketch-to-render. Input1 is PRIMARY POSE GEOMETRY and layout, input2 is character HEAD/OUTFIT identity. Draw same blue-haired young male adventurer in navy coat with gold trim/red lining, white shirt, grey pants, brown boots. Reconstruct legs following guide EXACTLY. Important cell5 (middle center) must have BRIGHT NEAR LEG backLEFT and DARK FAR LEG forwardRIGHT, with foreground arm forwardRIGHT across stomach; firstcell has BRIGHTnearleg forwardRIGHT, opposite arm swing. Keep those asymmetric depth relationships while preserving coat/weapon. Camera shallow3/4 facingright everypose. Pixel art upper-left light 48colors 1pxdarkoutline, sharp pixelclusters. Background pure#FF00FF, remove all guide marks. Request aspect 1:1. Do not state pixel sizes: the host image tool keeps the aspect and
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


Source grid3x3, first8 cells row-major, repacked losslessly into one horizontal strip before finishing. Cell9 blank excluded.

References:
- /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/p01-release-art-20261023/sources/male-walk-guide-v6/guide.png SHA256 aca7cea671152191631a69b82bc6e029774c2d7aac83ed2edd18999894ead819
- /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/p01-release-art-20261023/sources/male-upperbody-reference.png SHA256 37b5663fe9dd7c8497fd046630c12c9bad8d8d0b2ce4e3073c0835e11472db77

Raw SHA256: e90d3047fdb6a57c0762e012ca18fc850576c22db2f4c83ac725006c9893a659


Postprocess: Agent Sprite Forge v0.4.0 scale_frames.py (commit5324342), scale1/nearest/integer translations, torso-x registration, fixed192x192 canvas with96,184 anchor. Numeric QC does not approve anatomy, equipment or motion; Claude review still required.
