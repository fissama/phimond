# Static review species_0142

Candidate SHA256: `7f1c9bab1eb2fd759ee502854030200592e31dce02eb2a109d9b373cff3e45b2`

Identity compared with original APK portrait/atlas only. Approved DocDangNu and DaoThienDuong provide style only. All20 frames inspected as normal RGBA light composites after packing. No runtime activation. Human acceptance and continuous animation review pending.

Camera exception: original mechanical ghost is frontal; retain one fixed frontal view throughout, no alternating camera.

| Row | Observed four-frame action |
|---|---|
| 1 | Gray plates and red ghost tail bob in fixed frontal source view |
| 2 | Ghost tail swings side to side while gauntlets counter-move |
| 3 | Small gauntlet winds across chest, prepares, punches left, returns |
| 4 | Same gauntlet draws in, raises, extends, recovers |
| 5 | Armor recoils, dips, folds sideways, lies low |

Mechanical PASS verifies canvas, transparency, safe bounds and distinct cell pixels only. Physical pose changes reviewed separately above. One common nearest-neighbor scale; all source alpha preserved. Wide poses and faint source alpha reduce body size; check 64/96px preview before acceptance.
