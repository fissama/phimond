# Independent static review — species_0147 attempt-07

Decision: **FAIL — movement lacks a clear alternating gait; attack row recovery has a different ground line.** Mechanical PASS. Owner acceptance/runtime activation not granted.

Exact candidate SHA-256: `876a3542b5ec500b9fe07c4f9a0af3961d98455deda28bfa0b2bcb4a309c0644`.
Candidate: `apps/game-client/assets/pets/redraws/size-remedy-20261020/species_0147/attempt-07/packed.png`.
Before: `polish-20261008/species_0147/cohesive-20261009/attempt-07/packed.png`, hash `d296b1a816b0dd1a2fc3073e1bd904be1d8f2bcd82be5d1506db0b7e13910e80`, independently verified.

Inspected all 20 poses in actual-alpha native dark/light composites and equal-cell96/192 before/new/Linh Tiên comparisons. This is static frame-sequence review; direct animated playback was not independently exercised.

## Required fixes

1. **R2F1–F4, locomotion:** all four poses retain the same broad foreground foot planted to screen-left of the same rear foot; there is no clear opposite half-stride, foot lift/passing pose or swap of weight-bearing legs. Small torso/arm/foot-outline variations exist, so these are not byte-identical translations, but the sequence reads primarily as a standing stance/bob rather than four locomotion poses. At96px the movement row looks especially close to idle. Author a readable heavy shamble with distinct contact/passing/opposing contact poses while preserving two legs and body scale. Playback may establish bob rhythm but cannot supply an opposing leg pose absent from the frames.

2. **R3F1–F4 ground registration:** opaque exclusive bottom y is 217/218/218/216, versus idle224/225/225/225, skill225/225/226/225 and hurt/down224/223/226/226. In particular R3F4 returns to a standing recovery but the feet remain about9px above idle ground; the attack row appears lifted as a whole. This is not collapse-height reduction, since the ground-contact pixels themselves move upward. Re-register the attack row to the common visual ground, preserving full alpha and safety bounds. A numerical destination pivot [140,225] alone does not establish matching authored ground contact.

## Conditional note

**R4F1→F2 charge meaning is weak.** F1 has two small ice chips near the mace; F2 has no visible ice formation and near-idle body/weapon position; F3 shows three leftward shards; F4 returns to two chips. The restrained F2 intention is acknowledged, but static pixels do not clearly communicate gather→form before release. Direct playback should determine whether this reads as a deliberate concentrated pause; if it reads as idle interruption, add a compact, clear formation cue rather than enlarging FX. This is a conditional note alongside the two required fixes, not a claim that skill gameplay should change.

## Passing observations across all rows

- R1F1–F4: stable white fur/blue-grey face, red eyes, two gold tusks, two arms/two legs and one spiked mace. The body is broad and readable at96px; mean idle opaque height163.75px versus old70.25px and Linh Tiên162.75px. The increase is body mass, not FX being used to inflate measurement. Idle poses vary subtly; loop smoothness needs separate playback.
- R2F1–F4: no obvious extra limb, missing tusk, weapon duplication or directional flip. Gait issue is described above.
- R3F1–F4: compact overhead/over-shoulder mace wind-up, downward-left ground impact, recovery. All mace heads/tips appear complete and within their cells. F1/F2 wind-up is restrained but readable against the much lower F3 impact. No neighboring weapon head or foreign figure fragment found.
- R4F1–F4: ice FX remain compact; three release shards are on screen-left and do not obscure face/body. Weapon identity stays consistent. Charge-formation caveat above.
- R5F1–F4: hurt, weakened kneel, collapse, fully prone final pose. R5F4 is clearly down rather than upright stunned. One mace remains beside the face; no duplicate weapon or detached foreign body part found.

Dark colored outlines and crisp fur/face/mace clusters remain readable against both light and dark composites and at equal96/192 previews. No visible rectangular background haze, full-body bloom, text, borders, obvious neighbor art or definite hallucinated limb found. This statement concerns actual-alpha visible artwork, not hidden RGB in transparent pixels.

## Mechanical/provenance evidence

Read-only `python3 tools/assets/check_p10_atlas.py <candidate>` returned exit0 / PASS: RGBA PNG1124×1405; 20 occupied/distinct cells; every alpha>0 pixel within [22,259). Checker hash matches metadata and exact reviewed bytes.

Packing records common scale0.7275985663082436, destination pivot[140,225], and20 full-source rectangles. Raw size1122×1402; raw hash matches packing metadata. A source-coverage check found **no uncovered alpha>0 raw pixel**, supporting the full-coverage gutter approach rather than alpha deletion. Mechanical success does not resolve gait or visual ground registration.

Only this Markdown review was saved. No source art, candidate metadata, selection, owner approval or runtime mapping changed. Re-review a new hash after the required fixes; owner retains final acceptance.
