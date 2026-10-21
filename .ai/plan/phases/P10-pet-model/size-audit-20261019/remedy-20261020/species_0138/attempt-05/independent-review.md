# Independent exact-candidate review — species_0138 attempt-05

Decision: **Conditional PASS: inspected static art/registration requirements pass; direct temporal playback not independently exercised.** No remaining blocking static-art finding. Owner approval and runtime validation remain separate and pending.

Exact candidate: `apps/game-client/assets/pets/redraws/size-remedy-20261020/species_0138/attempt-05/packed.png`.
SHA-256: `bc83d0b2cdaa05b3ee3668e867b8309e02d2b765e38a623346c54ff2f9b6f487` (matches metadata and checker).
Compared with the same pinned before atlas and Linh Tiên species_0144 attempt-01 baseline used for attempt-04 review. Reviewed all 20 exact packed poses at native 281px cells and supplied fixed-cell 96/192px comparisons. Also inspected alpha-support mask for detached residuals. This is a new-hash review and does not change the failed disposition for attempt-04.

## Registration fix

The attempt-04 blocker is resolved. Exclusive opaque bottom y at alpha ≥128:

| Row | F1 | F2 | F3 | F4 |
| --- | --- | --- | --- | --- |
| Idle | 210 | 210 | 210 | 210 |
| Movement | 209 | 210 | 209 | 209 |
| Basic | 209 | 210 | 211 | 210 |
| Skill | 209 | 211 | 210 | 210 |
| Hurt/down | 211 | 210 | 211 | 209 |

R3F4 and R4F4 now recover on the idle ground; R5F4 rests on that same ground. Two-pixel total variation is ordinary pixel/pose variation, unlike attempt-04's 30px drift. Opaque contact, rather than faint alpha bounds, supports this conclusion. Numerical destination pivot is [140,210]. Packing records 20 rectangles and one common scale 0.7094339622641508. Packed raw source hash is `b06fa2fc97924e02c81c8e71c6a964886238b5f31e5272bdca7005604c4cad6c`, matching raw bytes.

## All-pose findings

- R1F1–F4: recognizable squat lava-rock brute, consistent two arms/two legs and large fists, orange fissures, dark red/brown stones. Different idle poses; no visible scale pumping. Mean opaque idle height 155.5px versus before 63.5px and reference 162.75px. Broad torso/fists make the slightly shorter silhouette substantial; it is not being enlarged by its effects. At equal 96px, body and bright face remain legible.
- R2F1–F4: leg/knee/foot and arm poses differ materially. They read as heavy locomotion rather than static-image translation. The foreground bent-leg action dominates; frame-by-frame inspection does not establish the opposite half-stride or 4→1 timing as clearly as playback would. No added/missing limb found. No registration blocker.
- R3F1–F4: ready/anticipation, cross-body wind-up, screen-left punch/impact, recovery. R3F2 rounded upper rear shoulder and lower rear fist remain readable as one shoulder/arm assembly, not a third arm. F3 impact points left; compact effect leaves the body readable. Recovery ground matches idle.
- R4F1–F4: gather, form, release three compact lava projectiles to screen-left, dissipate/recover. Face and torso stay visible. Recovery ground matches idle.
- R5F1–F4: stagger, weakened kneel, collapse, genuinely prone fully-down final pose; no upright-stun substitution. The final resting body matches the common ground. No visible anatomical regression from attempt-04.

Native outlines and hard colored clusters remain legible at equal 96/192 previews. No visible rectangular haze, full-body bloom, text, border, background, definite neighboring anatomical fragment, or definite hallucinated limb found in these 20 frames.

## Residuals and limitations

Alpha-support diagnostic still shows near-transparent detached specks, particularly above R2F2/F3 and R5F1/F2/F3. These were already present in the shared raw image. They are not visible foreign anatomical pieces in the normal images examined; no blocking neighboring-fragment finding is established. Do not count these specks as body height or intentional design detail, and do not erase alpha to claim containment. Preserving the raw source remains appropriate.

Mechanical command `python3 tools/assets/check_p10_atlas.py <candidate>` returned exit 0 / PASS: RGBA PNG 1124×1405; 20 occupied/distinct cells; every alpha >0 pixel contained in [22,259).

Temporal playback was not independently exercised by this reviewer. A final all-gates visual PASS still needs direct review of idle/move loops and one-shot/hold behavior, especially the movement 4→1 rhythm. Parent self-review playback evidence may satisfy its own review, but must not be described as this reviewer having watched it. In-game scale/camera/UI verification remains pending. No selection, runtime activation, or owner approval is granted.
