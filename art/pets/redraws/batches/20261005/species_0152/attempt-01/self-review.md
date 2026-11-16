# Static review species_0152

Candidate SHA256: `0bfd7e0131091bd54bd2cff3fbaf0914a58ef1e3cc5b73cc8d422ed2b4ac6cb8`

Identity compared with original APK portrait/atlas only. Approved DocDangNu and DaoThienDuong provide style only. All20 frames inspected as normal RGBA light composites after packing. No runtime activation. Human acceptance and continuous animation review pending.

| Row | Observed four-frame action |
|---|---|
| 1 | Gold hair and white outfit stable while purple wings flap |
| 2 | Two legs alternate lifted stride with wing counter-movement |
| 3 | Wings fold, rise in windup, arm strikes left, recover |
| 4 | Arms draw in, both raise, one extends left, lower |
| 5 | Recoils, kneels, folds forward, lies with wings closed |

Mechanical PASS verifies canvas, transparency, safe bounds and distinct cell pixels only. Physical pose changes reviewed separately above. One common nearest-neighbor scale; all source alpha preserved. Wide poses and faint source alpha reduce body size; check 64/96px preview before acceptance.
