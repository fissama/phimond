# Static review species_0144

Candidate SHA256: `1150468f713eb0d6dd44bc97c9aeb0c12df433ce1267adc8dc21d2736d79ed0c`

Identity compared with original APK portrait/atlas only. Approved DocDangNu and DaoThienDuong provide style only. All20 frames inspected as normal RGBA light composites after packing. No runtime activation. Human acceptance and continuous animation review pending.

| Row | Observed four-frame action |
|---|---|
| 1 | Flower crown and pink petals breathe with visible head bob |
| 2 | Purple leaf skirt and petal tips alternate while body advances |
| 3 | Green hand bends inward, lifts, reaches left, returns |
| 4 | Leaf hand raises then points left with torso lean |
| 5 | Recoils, bows, knees/leaves fold, lies face-left |

Mechanical PASS verifies canvas, transparency, safe bounds and distinct cell pixels only. Physical pose changes reviewed separately above. One common nearest-neighbor scale; all source alpha preserved. Wide poses and faint source alpha reduce body size; check 64/96px preview before acceptance.
