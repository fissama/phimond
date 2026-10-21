# Independent static review — species_0141 attempt-03

Decision: **PASS for inspected static art and mechanical requirements.** No remaining blocking static finding. Direct playback is being reviewed separately; owner approval and runtime acceptance remain pending. This is not an all-gates animation or owner approval.

Exact reviewed SHA-256: `b15bad7de0237aefa83ac5c5e464df1f4dad5f3a0abd93fc74a3622671e56612`.
Candidate: `apps/game-client/assets/pets/redraws/size-remedy-20261020/species_0141/attempt-03/packed.png`.

Inspected all 20 poses at native 281px cells, equal 96px and 192px before/new/Linh Tiên comparison sheets, and compared packed pixels with attempt-02. The visible R5F3 fragment blocker from attempt-02 is resolved. At cell-local x≥225, R5F3 now has no alpha ≥128 support. The former arc was part of the following frame crest: R5F4 now has a complete left crest edge rather than a separated strip. No new visible neighboring body fragments or invented limbs were found across the remaining poses.

## Packing/provenance verification

Raw bytes for attempts 02 and 03 are identical: SHA-256 `ae020f49917105c88ff4055837a54fa4deb20c99566d8ad3156897438c33240e`.
Raw size is 1121×1403. Coverage check over all 20 declared source rectangles found **no uncovered alpha>0 source pixel**. Thus the source-rectangle change accounts for the repair without deleting alpha. Last row rectangles are [0,1131,280,272], [280,1131,280,272], [560,1131,260,272], [820,1131,301,272]. The F3/F4 boundary is x820, preserving the complete F4 crest. One common scale 0.6666666666666665 and destination pivot [140,210] remain recorded. Packed differences are restricted to last-row F2/F3/F4; other 17 cells compare unchanged.

Read-only `python3 tools/assets/check_p10_atlas.py <candidate>` returned exit 0 / PASS: RGBA PNG 1124×1405, 20 occupied/distinct cells, all alpha>0 pixels inside cell-local [22,259). Exact hash above comes from this run.

## All-pose static observations

- R1F1–F4: gold fan crest, carved turquoise-accented face, cylindrical/slab body, two armored arms and no legs retain identity. Distinct small idle changes. Idle mean opaque height remains 155.75px versus old 66px and Linh Tiên 162.75px; body and face remain readable at equal 96px without relying on skill FX for size.
- R2F1–F4: consistent hovering locomotion with alternating tilt/arm changes and compact turquoise square particles beneath. No visible opaque spill from the preceding row, no added legs, no arm-count drift. Temporal 4→1 smoothness belongs to separate playback review.
- R3F1–F4: anticipation, raised fist wind-up, screen-left extended punch, recovery. Two arms and unchanged crest/face remain readable. No visible registration jump comparable with the earlier species_0138 issue.
- R4F1–F4: compact gather squares, one formed triangular rune, three released triangular runes on the left, dissipating squares. Gold/turquoise geometric effect remains crisp and clear of the face. The triangular symbols point right while the effect group is on the left; actual travel direction is a separate playback check, not inferred from geometric symbol orientation alone.
- R5F1–F4: stagger, lean/weaken, collapse, fully horizontal down. R5F3 now has no detached bronze arc. R5F4 crest is visibly complete, and the two arms/face remain attached to the correct down body. Final pose is genuinely fully down rather than an upright stun.

Native dark outlines and hard pixel clusters remain readable at equal 96/192px. No visible rectangular haze, full-body glow, text, background, foreign anatomy or definite hallucinated limb found. Near-transparent residual pixels are not body measurements or proof of intentional FX, but no other visible fragment blocker was established.

Saved only this review. No selection, source art, metadata, owner approval or runtime mapping was changed. Browser playback and in-game validation remain separate; owner retains final art acceptance.
