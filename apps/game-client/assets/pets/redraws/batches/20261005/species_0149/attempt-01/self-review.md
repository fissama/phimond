# Static review species_0149

Candidate SHA256: `d9e4cb7fc1bef189e33f52a60b4cfc3c976c4f7f3506edad8fae18b0739eca78`

Identity compared with original APK portrait/atlas only. Approved DocDangNu and DaoThienDuong provide style only. All20 frames inspected as normal RGBA light composites after packing. No runtime activation. Human acceptance and continuous animation review pending.

| Row | Observed four-frame action |
|---|---|
| 1 | Single horn, white chest and red mane retained; head/tail phase changes |
| 2 | Four hooves alternate supports and lifted phases |
| 3 | Crouch, rear, front hoof strike left, recover |
| 4 | Lower head, rear with raised hoof, extend hoof left, return |
| 5 | Recoil, crouch, fold forelegs, prone with horn left |

Mechanical PASS verifies canvas, transparency, safe bounds and distinct cell pixels only. Physical pose changes reviewed separately above. One common nearest-neighbor scale; all source alpha preserved. Wide poses and faint source alpha reduce body size; check 64/96px preview before acceptance.
