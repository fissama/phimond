# Rồng Có Cánh — static review

Candidate `packed.png`, SHA256 `68b1d8821f5b0a83f5f9dc52f006aa3166b95c90a9bdf34521f50a89dbdfcae0`. Original APK inputs only for identity; two approved anchors only for style. All20 raw and packed poses inspected, plus alpha-composited source on light background.

| Row | C1 | C2 | C3 | C4 |
| --- | --- | --- | --- | --- |
| Idle | crouched rest | wings rise | lower breath | settle |
| Move | front step | opposite step | wings lower and leg advances | opposite return |
| Attack | crouch | jaw opens, body winds | snout and foreleg lunge left | recover |
| Cast | brace | rear up | raised chest, long snout stays left | settle |
| Hurt/down | recoil | droop | belly down | fully down |

Red/orange body, tan wing membranes, dark horns, long narrow snout, yellow eyes, clawed limbs and tail retained. Fixed LEFT camera; R4C3 repaired from upward/stubby head. No FX or visible neighboring body fragments on normal compositing. Transparent inspector shows bright red halo, but RGBA diagnosis found36,808 bright-red pixels at alpha1; these are nearly invisible on a normally composited background, not opaque flames. Every alpha pixel retained in packing.

Mechanical PASS, common scale0.7095808, ground baseline209.33. Browser playback/human approval pending. Attempt03 halo cleanup was unnecessary and is superseded by this version. Some cluster shading is smoother than the anchors and should receive human style review.
