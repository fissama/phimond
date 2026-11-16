# Redraws from Claude review — 2026-10-30

This batch responds to R1–R4 in `.ai/design/v1.0.1/ART-REVIEW-20261030.md`. Generated candidates are not installed or owner-approved unless explicitly stated below.

## Candidate files ready for Claude visual review

| Item | Candidate | Checks | Remaining review |
|---|---|---|---|
| R3 N09 | `r3-n09/delivery-palette-v1/chat-frame.png` | 768×176, 41 visible colors, binary alpha; transparent interior; gold double border | Confirm 9-slice joins in renderer |
| R3 N09 | `r3-n09/delivery-palette-v1/chat-tab-normal.png` | 160×44, 40 visible colors, binary alpha; dark teal/gold | Confirm fit against frame |
| R3 N09 | `r3-n09/delivery-palette-v1/chat-tab-selected.png` | 160×44, 43 visible colors, binary alpha; dark teal/gold; bottom edge open | Confirm open join against frame |
| R4 N03 | `r4-n03/delivery-v1/slot-common.png` | 96×96, 18 shared-palette colors used, binary alpha; silver-grey border | Confirm the corner trim is plain enough |
| R4 N03 | `r4-n03/delivery-v1/slot-legendary.png` | 96×96, 33 shared-palette colors used, binary alpha; gold-orange border and four small star sparks | Confirm geometry matches common at game size |

Palette apply QA is in `r3-n09/delivery-palette-v1/apply-qa.json` and `r4-n03/delivery-v1/apply-qa.json`. Both report `output_off_palette_px=0` and `output_partial_alpha_px=0`; no max-ΔE limit was set. The image generator returned wider source canvases, so R3 was resampled non-uniformly to the required wide canvas before palette finishing; inspect final proportions in the game renderer before approval.

## Still rejected / incomplete

- R1: two hall-rooftop redraw attempts are preserved in `r1-hall-outside/raw/`. The newer dusk version has the requested 4:3 view and roof-tone strip, but its left/right scene edges do not tile and it exceeds 48 colors before palette processing. No R1 delivery candidate is claimed.
- R2: the latest elder and traveller frame-1/frame-5 stills are preserved in `r2-run-contact/raw/`; pose crops from the approved player anchor are in `r2-run-contact/pose-refs/`. Both pairs still show the same leading leg, including an elder retry with enlarged isolated leg references. No six-frame continuation was generated from an invalid pair, and no new run strip is delivered.
- R4 failed experimental attempts are retained in the Codex generated-image history; they are not substitutes for `delivery-v1`.

## Status

R3 and R4 are review candidates only; they have not been installed. R1 and R2 remain open. See each subfolder for raw images, source references, prompts and pipeline metadata.
