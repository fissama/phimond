# Independent static review — species_0147 attempt-09

Decision: **PASS for inspected static art requirements and mechanical geometry**, with one minor residual-speck note. Both attempt-07 blockers are resolved. Direct playback is reviewed separately by the lead; owner and runtime acceptance remain pending. This is not an all-gates animation or owner approval.

Exact reviewed SHA-256: `d5a7dcc4955deff1db4608104d8f5ffd5472bb213600c0e46dc0b041e0123cff`.
Candidate: `apps/game-client/assets/pets/redraws/size-remedy-20261020/species_0147/attempt-09/packed.png`.

Inspected all20 exact poses in native-dark.jpg/native-light.jpg actual-alpha composites and fixed-cell96/192 before/new/Linh Tiên comparisons. Mechanical checker was run on the exact packed PNG; hash agrees with metadata.

## Previously blocking issues

- **Locomotion resolved:** R2F2 visibly raises the forward foot with the opposite leg bearing weight; R2F4 visibly lifts the rear/opposing foot while the forward foot supports the body. F1/F3 provide contact/spread poses. The sequence now contains real leg-pose changes and opposing passing actions, rather than the prior same-foot planted stance bob. It remains a deliberately heavy shamble. Temporal 4→1 smoothness is separate playback verification.
- **Attack registration resolved:** exclusive opaque bottom y is idle224/224/225/225; movement224/222/225/225; attack226/226/227/224; skill224/224/226/224; down224/224/225/225. R3F4 recovery now returns to the idle visual ground; remaining2–3px contact variation fits the pose differences and does not recreate the prior9px attack-row lift.
- **Skill formation clarified:** R4F2 now has a compact blue ice crown/ring around the mace head, between F1 gathering chips and F3 three leftward shards. The previous near-idle interruption is no longer the only visible reading. F4 dissipating chips remain compact.

## All20 static observations

- R1F1–F4: subtle idle variation, consistent white fur, grey-blue face, red eyes, two gold tusks, two arms/two legs and one short spiked mace. Broad body is readable at equal96px; mean idle opaque height170px versus old70.25px and reference162.75px. Size comes from body, not FX.
- R2F1–F4: distinct heavy contact/passing foot poses as above. Weapon remains in the same hand, tusks/face/scale stay consistent; no duplicated or missing foot found. Opposite raised feet are now distinguishable at96px.
- R3F1–F4: compact overhead mace anticipation/wind-up, lowered leftward ground impact, upright recovery. Mace tips and handle appear complete; single mace throughout. Impact no longer leaves visible white pieces in neighboring cells. F1/F2 differ subtly, but their higher weapon position contrasts clearly with F3 impact.
- R4F1–F4: gather chips, formed crown at mace, three compact leftward ice shards, dissipating chips. Face/body stay visible; no enlarged full-body aura or second weapon.
- R5F1–F4: hurt, weak kneel, collapse, fully prone final pose. Final frame is genuinely down, with one mace retained beside the face and both tusks belonging to the same head. Contact returns to the common ground.

Dark outlines and fur/face/mace clusters remain readable on light and dark backgrounds and fixed96/192 previews. No visible rectangular background haze, full-body bloom, text, border, definite neighboring anatomy, missing mace tip or definite hallucinated limb found.

## Minor nonblocking residual

R2F2 has an isolated **three-pixel dark speck** at cell-local x243,y118–120. Its RGBA values are (18,11,10,175), (9,4,4,215), (8,6,4,211). It appears as a tiny dark vertical dot on the native light background and does not identify a foreign limb/weapon or affect the96/192 pose reading. This is a cosmetic residual, not a blocking anatomical fragment finding. Record honestly rather than describing the candidate as having zero detached pixels. If cleaned later, preserve source history and re-review the resulting hash; do not silently alter accepted pixels.

## Mechanical/provenance evidence

Read-only `python3 tools/assets/check_p10_atlas.py <candidate>` returned exit0 / PASS: RGBA PNG1124×1405; all20 cells occupied/distinct; every alpha>0 pixel within [22,259). Source coverage over all20 declared packing rectangles found no uncovered alpha>0 raw pixel. Actual raw hash matches packing metadata. This verifies packing coverage of the current edited raw; it does not claim edited raw bytes equal earlier attempts.

Only this Markdown review was saved. No source art, candidate metadata, selection, runtime mapping or owner status changed. Playback/loop duration and live world/battle camera/UI checks remain separate. Owner retains final art acceptance.
