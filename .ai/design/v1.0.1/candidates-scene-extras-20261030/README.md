# Scene extras candidate art — 2026-10-30

These are isolated, unapproved candidate PNGs generated for the four missing scene extras listed in `PLAN-OCTOPATH-V101.md` (M11–M14). They are not installed into `apps/client/public/hd2d`, not referenced by runtime code, and do not change any status/checklist.

## Candidate files

| File | Planned asset | Size | Background / QA |
|---|---|---:|---|
| `fg-deep-vines.png` | M11 Deep Forest foreground vines and mushrooms | 512×384 | Transparent; binary alpha; 36 RGBA colors |
| `fg-gate-banner-edge.png` | M12 Palace Gate hanging banners | 384×512 | Transparent; binary alpha; 43 RGBA colors |
| `hall-side-corner.png` | M13 hall front-corner pier + balustrade connector | 256×400 | Transparent; binary alpha; 38 RGBA colors |
| `hall-outside-roofs-side.png` | M14 exterior rooftops side plate | 512×384 | Opaque; 48 RGB colors |

The generated source images were scaled to the dimensions in the plan with nearest-neighbor resampling and constrained to the plan's palette limit. Transparent candidates use alpha values 0 or 255; transparent pixels were normalized to black RGB to remove matte fringes.

## Provenance and prompt set

Generated with the built-in `image_gen` tool on 2026-10-30. Prompt text and reference images are recorded in `PROMPTS.md`. Sources checked before generation:

- `.ai/design/v1.0.1/GPT-PROMPTS-OCTOPATH.md`
- `.ai/design/v1.0.1/PLAYTEST-OCTOPATH-GAP.md`
- `.ai/design/v1.0.1/PLAN-OCTOPATH-V101.md`
- Existing runtime asset names and use in `apps/client/src/render/scene.ts` and `apps/client/public/hd2d/assets.json`

## Visual review and assumptions

- M11: readable layered hanging vines, leaves and small green mushrooms. It is a distinct Deep Forest foreground variant; placement, scale, and overlap with the player remain unvalidated in-game.
- M12: two readable blue-and-gold hanging standards with sun emblems. The source plan does not specify the banner count per side or exact gate-relative anchor positions; this candidate assumes two symmetrical banners with a central sightline left open.
- M13: one front-facing corner pier with balustrade runs on both sides. The precise corner orientation and the desired run lengths are not documented; runtime currently has side pier and balustrade assets but does not define a front-corner placement for this candidate.
- M14: opaque city-side view with rooftops, a far tower, sky and hills. The plan provides size and content but not whether each side should use a mirrored/shared plate or distinct compositions; this is one reusable plate candidate.

All four images were visually inspected after resizing and rechecked on a contact sheet on 2026-10-30. Per-file measurements, hashes and review limits are in the adjacent `*.qa.json` files. Subject, composition, and palette are plausible candidates; they have not been integrated, approved, or tested in a scene. In-engine scale, blur strength, exact placement, and seamless joins still need owner review.

## Runtime placement trace (read-only review, 2026-10-30)

The existing renderer was checked to make the pending placement review specific; no runtime files were changed.

- **M11 Deep Forest vines:** `apps/client/src/render/scene.ts:541–546` already camera-anchors two near branches near the upper left/right (`ax=-0.8/0.82`, `ay=0.74/0.82`) and lower bushes. The new wide vine sprite would overlap those branches if simply added. Review it as a replacement/variant for one upper branch first; confirm portal and player visibility before approval.
- **M12 Palace Gate banners:** the current city foreground uses generic bunting plus a mirrored lantern pair (`scene.ts:548–549`); no gate-specific banner anchor exists. The candidate's two standards likely need a separate pair of map anchors or to replace a current foreground element. Owner should select which placement before it can pass scene review.
- **M13 hall corner:** the hall renderer places side balustrades at `z=3.8,7.8` and piers at `z=1.8,5.8,9.8`, with the left/right sides rotated in opposite directions (`scene.ts:738–740`). The candidate could close the front end of each side rail, but must be mirrored/oriented correctly and checked against actual joins.
- **M14 side roofs:** the renderer already stretches `hall-city-backdrop` and `hall-city-roofs` across the hall width (`scene.ts:661–684`). Treat the new plate as a possible cropped edge filler only if a scene capture proves a gap; otherwise it duplicates the current backdrop layers.

These traces narrow likely use but do not substitute for an in-engine composition check. QA files remain `approved:false` until the intended placements are reviewed.
