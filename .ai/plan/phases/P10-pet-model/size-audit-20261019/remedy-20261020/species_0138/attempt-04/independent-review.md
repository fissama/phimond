# Independent exact-candidate review — species_0138 attempt-04

Decision: **FAIL — stable ground/pivot across animation rows.** Mechanical PASS. Size/readability remedy is successful; owner acceptance remains pending. This review grants no selection or runtime approval.

Candidate SHA-256: `62752ce7b279e1827962c90ab4b063262a7abed7714d8f3e2c7ea600653df759`.
Before SHA-256 verified: `25b0741369caea0f2c8fe547068fc31359297f38641bc18ff8881ed36ba9e3a8`.
Linh Tiên baseline SHA-256 verified: `63efbba22985c5e938be71bcfb2aebbc9db3ec1b9d12bd8d38c5a5ce5d666dd4`.

Inspected exact packed atlas at native 281px cells, all 20 poses in supplied equal-cell 96px and 192px before/after/reference comparisons, plus light-background composite and alpha-support diagnostic. No source pixels were changed. Playback implementation was read; direct animated playback was not exercised by this reviewer, so temporal smoothness beyond frame-order inspection is unverified.

## Blocking finding

**R1, all rows / transition idle→attack→skill→down: artwork rises above its previous ground line.** At alpha ≥128, exclusive bottom y is 246 for all idle frames; 244/246/244/244 for movement; 232/233/235/233 for basic attack; 223/225/224/224 for skill; 217/216/217/216 for hurt/down. Thus planted attack/recovery feet rise about 11–14px from idle, skill feet about 21–23px, and the final grounded body about 29–30px. In R3F4 and R4F4, the recovered standing stance should reconnect with idle ground but remains visibly higher. This is not normal head bob or collapse-height reduction: the bottom ground contact itself changes. The common numerical packing pivot [140,258] does not establish a common visual ground contact. Fix registration across all rows, preserving complete art and safe alpha containment, and re-review the new exact hash. Do not erase faint pixels merely to allow translation.

## Per-row visual observations

- Idle R1F1–F4: same lava-rock brute identity, two arms/two legs, large stone fists, dark red/brown rock and bright orange fissures; subtle pose variation. Idle opaque height mean 168.25px versus before 63.5px and reference 162.75px. Broad anatomy reads substantial at 96px without using FX to supply body height.
- Movement R2F1–F4: genuine leg/foot pose differences, not four translations of a static drawing. The foreground bent-leg motion dominates; the opposite half-stride is less explicit, so gait/4→1 rhythm deserves direct playback inspection. No definite added/missing limb found in these four frames. Horizontal body presence remains broadly stable.
- Basic R3F1–F4: anticipation, raised/cross-body wind-up, clear screen-left extended fist/impact, recovery. R3F2 has a large rounded shoulder above the lowered rear fist; inspected as shoulder anatomy, not evidence of a third arm. F3 compact impact is directed consistently left. Ground registration fails as above.
- Skill R4F1–F4: compact hand/flame buildup, crouched formation, three left-moving lava projectiles, dissipation/recovery. Face/body remain readable. Ground registration fails as above.
- Hurt/down R5F1–F4: stagger, kneel/weakened, collapse, genuinely prone final frame. R5F4 is fully down rather than an upright stun. The row has internally consistent ground contact, but is displaced upward relative to idle.

## Pixel/containment/provenance checks

Read-only command `python3 tools/assets/check_p10_atlas.py <candidate>` returned exit 0: RGBA PNG 1124×1405; all 20 cells occupied and distinct; every alpha >0 pixel inside [22,259). Exact candidate hash matches metadata. Packing records 20 source rectangles, pivots and common scale 0.7699836867862968. No mechanical geometry failure.

Dark colored outlines and small hard clusters remain readable at native and equal 96/192 preview sizes. No visible rectangular haze, full-body glow, text, background, obvious neighboring body fragment, or definite hallucinated limb was found. Alpha-support diagnostic does reveal faint detached specks (particularly above R2 and R5); many are near-transparent, so alpha>0 bounds are not reliable ground/body measurements. Example R5F2 alpha>0 top is y42 while opaque body starts y90. Do not describe these alpha bounds as anatomy or confidently certify them as intentional FX. No visible foreign anatomical fragment was established.

Runtime: not activated; in-game scale/camera/UI verification pending. This independent review is **not owner acceptance**. Re-review the registration remedy and direct loop playback before a visual PASS claim.
