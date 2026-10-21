# Independent review — PNG atlas production, 2026-10-15

**Five conditional review candidates; strict visual acceptance is not granted.** The actual PNG atlases were reviewed under the owner’s explicit PNG-production request. No video dependency is imposed on this delivery. No generated atlas is owner-approved or activated in runtime.

## Verified mechanics and preservation

- Final hashes match jobs, art manifest and per-species result records. Master reference hashes match recorded inputs.
- Five RGBA PNGs 1124×1405 with 20 distinct occupied 281 px cells and local alpha [22,259): PASS.
- 20 source rectangles cover each full raw canvas exactly once, with no overlap: PASS.
- Independent in-memory uniform nearest-neighbor packing reproduces every final PNG byte-for-byte: PASS. No alpha erasure or independent frame warping in that reproduction.
- Only idle/move GIFs loop; basic/skill/down do not: PASS.
- Original 152 registry and 919 frozen hashes preserved: PASS. Owner-approved 0154/0156/0158 exact atlas bytes preserved: PASS.

These mechanical checks do not certify correct frame ownership or visual acceptance. No hard clipped anatomy was observed in the final set, but the known 153 windup FX assignment defect remains.

## Exact final targets

### species_0153 — attempt 11

SHA256: `19068794cbfa2e9386d57a0030cfd1bd0a43425f8b0f5903d91e7ad9d6f083a8`

[Packed atlas](/Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/extension-20261013/species_0153/attempt-11/packed.png)

- Natural branched curved woody antlers, moss/deer four-leg silhouette and small crescent flank mark preserve latest master; no mounted moon discs.
- Idle breathing changes, alternating deer steps, lowered antler LEFT strike, Earth leaf/moon magic and fully prone down are visible across rows.
- R3C2 RIGHT still contains a straight-cut yellow/green effect strip from the following impact pose. This is a known source-to-frame FX assignment defect, despite no observed cut anatomy. Strict fragment-free visual acceptance is NOT met.
- Large leaf/light curtain obscures branch roots in skill poses. Readability/strict pixel softness and actual temporal gait remain owner conditions.

### species_0155 — attempt 13

SHA256: `042adaba54a44da83f4d8db55553817f1e9c0738faaf59abdb29a3ffaaae6405`

[Packed atlas](/Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/extension-20261013/species_0155/attempt-13/packed.png)

- Mature night-blue/gold dragon, four legs, folded wing pair with far wing partly occluded, one curved star-tip tail and chest core retained.
- Alternate step and varying tail curvature, richer star/crescent LEFT basic, constellation form and three light-lance LEFT release visible; fully flat down.
- Attempt11 foreign tail/wing fragments and own-tail truncation resolved. No hard anatomy/frame-ownership defect observed in final13.
- FX richness now stronger but glow/pixel style and actual four-frame smoothness need owner review.

### species_0157 — attempt 11

SHA256: `04f5c7782f46d6392d8de7f9118051a685b8bfb70add42a94dda7a218f062898`

[Packed atlas](/Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/extension-20261013/species_0157/attempt-11/packed.png)

- One ocular body whose pupil opens as ivory-fanged mouth; zero floating crown runes. Hover/tentacle changes, left whip/bite, angular dark pulse and flattened final down retained.
- Six tentacle count cannot be independently certified in every dense overlapped pose. Far curl tips and effects merge at64px.
- R4C2 separate eye-shaped diamond portal may read as a second eye; one anatomical body remains. Treat as owner design ambiguity, not approved anatomy/style change.
- Large skill FX and strict pixel/blur/glow acceptance plus actual loop feel remain owner conditions.

### species_0159 — attempt 15

SHA256: `5defdda31d7b2a7cdaad918455370a90cdeef337a52fffded2a0d2b7d9c7c14d`

[Packed atlas](/Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/extension-20261013/species_0159/attempt-15/packed.png)

- LEFT-floating mature gold/ivory dragon, two arms, two small hanging hindlegs, compact blade-feather wings with far wing occluded, two separate tails and two integrated tip seals retained; no old chest/flank seals.
- Hover bob and opposed tail variation visible; LEFT arm claw basic, gathering/claw sweep and rich gold/jade release present. Both seals persist through final fully fallen pose.
- Attempt14 R3C2 lower tail-seal truncation resolved in15 by full-source rectangular boundary move; green seal and complete outer gold rim/tip now visible. No hard cut anatomy observed.
- Dense skill aura obscures precise two-tip ignition; skill also reads as an arm blast. Strict claw-then-tail-seal choreography clarity and residual boundary glow are NOT certified; owner review required.

### species_0160 — attempt 15

SHA256: `72d25f0c237d21d8cfdd0e523b0e5e9f406050b81968ced5a226a2cf3035cb07`

[Packed atlas](/Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/extension-20261013/species_0160/attempt-15/packed.png)

- Youthful adult masculine torso, neat white-lavender curtain hair/cold gaze, two horns, purple leg armor, one spear and opposite caster hand preserve master identity.
- Alternate leg/heel steps, complete raised spear and compact LEFT thrust, purple seal and short LEFT release visible; final fully prone with diagonal spear behind body.
- Earlier rear spear-tip truncation, detached neighboring fragments and giant basic cone resolved. No hard cut anatomy observed in15.
- Body is small at64px; face/hair details compress. Skill release resembles spearhead streaks, so distinction from physical basic and actual four-frame gait need owner review.

## Limits and owner gates

- Only mechanical/source coverage/exact packing checks PASS. They do not establish anatomy, correct ownership or visual acceptance.
- All five final raw/packed/contact64/contact96 images were visually inspected.15915raw is byte-identical to inspected14raw.
- Four frames per action demonstrate pose changes, not certified smooth runtime gait or seamless temporal playback. GIF loop flags were checked; game playback timing is a review preset.
- Latest159wing revision remains pending owner approval; earlier master approval does not approve its new atlas. All five generated atlases are pending owner approval.
- No runtime activated, no gameplay logic or database changed by reviewer.
- Strict pixel/no-AA/no-blur/no-bloom style is not certified; luminous FX and faint fringes remain owner-review conditions.

## Rejected source history

Superseded raw/packed versions remain available and are not current review targets.

- species_0155 attempt 11 (`daf02dbdf0ddf6a488b12718d3e5e144966714444632439d5b8430337f13b801`): R4C3 left foreign star-tip tail and own tail cut RIGHT; R4C4 left detached wing/tail fragments; R3C2 cut next-frame FX. Clearly visible at64/96. Resolved/superseded by attempt 13.

- species_0159 attempt 13 (`b723a90ad1df9e9c330efbe4799b531784c77045bc4e830fd979d0b705ab4138`): R3C1 RIGHT lower tail-seal tip truncated; R2C1 lower tip touches partition; large skill FX obscure seals. Resolved/superseded by attempt 15.

- species_0160 attempt 13 (`8130343435fb1290aa47103de371752b27244f41c4c08a8eaec703a4838d0a61`): R2C1 andC2 rear spear tips cut at RIGHT partition; R3C2 cut release glow; source densely overlaps. Resolved/superseded by attempt 15.

- species_0159 attempt 14 (`a536d2ef0f8149f98b2a20e73ba2392da72b2f11ab960743dd3c3acc411afd53`): R3C2 RIGHT lower tail-seal outer rim and tip truncated by source boundary. Resolved/superseded by attempt 15.

Only atlas-production/independent-review.json/md were written by the reviewer. Art, manifests, approval records, selection and runtime were not changed.
