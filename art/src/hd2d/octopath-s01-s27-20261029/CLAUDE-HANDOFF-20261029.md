# Claude handoff — Octopath S01–S27 (2026-10-29)

## Ready state

There are 45 static PNGs in `delivery/`, each with a prompt and QA JSON. Mechanical QA confirms requested dimensions, ≤48 visible colors and binary alpha. Claude's later visual review found pink fringe in several files. The full linked index is [`delivery/REVIEW-BOOK.md`](delivery/REVIEW-BOOK.md).

## Review received after this delivery

Claude's latest decisions are in [REVIEW-GPT-S01-S27-STATIC.md](../../../../../.ai/design/v1.0.1/REVIEW-GPT-S01-S27-STATIC.md). The review records that fringes and the dark strip were cleaned, the two redraw-v2 assets were approved, and 31 static files were installed. Wall, cliff and bridge assets retain repeat-seam limitations; follow the per-file usage restrictions.

The two replacement PNGs are available individually in [`delivery/redraw-v2/`](delivery/redraw-v2/README.md), with prompts and QA. Claude approved them for their intended use; the slightly tall/narrow city architecture was accepted for a distant backdrop. Both were installed per review section F.

The review's section A lists 23 file names although its heading says 21; section B lists 12 although its heading says 13. `stone-wall-face` appears both as approved in A and as restricted for horizontal repetition in C. Resolve these counts and the usage restriction against the individual names before installation.

## Previously approved exact files

- `stone-floor-b.png` and `floor-light-1/2/3.png` exactly match the E18/E21 approved source files. They are already in the approved summon-hall delivery.
- E19/E20 city assets were approved earlier, but the Oct 29 S07/S08 files have different SHA-256 hashes. Do not transfer the old approval to these new files. Review the current copies if intended for v1.0.0.

## Send these static assets for visual approval

Follow Claude's individual decisions and required cleanup in the review above. Only the specific approved or corrected file should be added to `apps/client/public/` / v1.0.0.

## Motion assets

### S23 — redraw all six player strips

- A guided 2×4 male attempt was assembled and registered to 192×192 frames, but [its QA](processed/cli-male-guided-walk-qc/sheet-qc.json) reports `leg_alternation: fail` and `phase_coverage: warn`; it is not a release candidate.
- `player-male.run.png` — R01–R06 are marked rejected. The latest male horizontal candidate fails `leg_alternation` (frame 1 vs 5) and `identity_head_ratio` (1.078 at frames 4 and 8; max 1.05). Full evidence: [`rejected/player-male-run-20261029.qa.json`](rejected/player-male-run-20261029.qa.json) and [`processed/player-male.run-segmented/frames-qc/sheet-qc.json`](processed/player-male.run-segmented/frames-qc/sheet-qc.json).
- `player-female.run.png` — R02 rejected: leg alternation and stray pixels.
- `player-male.run-down.png` and `player-female.run-down.png` — R03–R04 rejected: the old frames do not show a clear change of legs.
- `player-male.run-up.png` and `player-female.run-up.png` — R05–R06 rejected: the old frames do not show a clear change of legs; R06 also varies in height.
- A new Codex image_gen male-horizontal attempt is preserved in [`rejected/host-image-male-run-attempt-03/`](rejected/host-image-male-run-attempt-03/review.md); it repeats a four-pose cycle, so it is rejected as well.

### S24 — 18 existing NPC candidates, not approved

All 18 old PNGs are in `../p01-release-art-20261023/delivery/` with QA/GIF previews. The 2026-10-24 machine queue classifies 5 pass, 9 warn, 4 fail. `pass` is only an automated candidate result, not approval under the new frame-1/frame-5 requirement. S24 asks for an approved `player-male.run.png` style reference; none currently exists. Do not integrate S24 until that anchor is approved and each NPC strip passes visual review.

- **QA pass candidates for Claude review (5):** `walker-boy.run-down.png`, `walker-elder.run-up.png`, `walker-girl.run-up.png`, `walker-guard.run-down.png`, `walker-traveller.run-up.png`.
- **Warn; repair/recheck (9):** `walker-baker.run.png`, `walker-baker.run-down.png`, `walker-baker.run-up.png`, `walker-elder.run-down.png`, `walker-boy.run.png`, `walker-boy.run-up.png`, `walker-girl.run.png`, `walker-girl.run-down.png`, `walker-traveller.run-down.png`.
- **Fail; redraw (4):** `walker-elder.run.png`, `walker-guard.run.png`, `walker-guard.run-up.png`, `walker-traveller.run.png`.

Detailed machine results: [`p01-release-art-20261023/REVIEW-QUEUE.md`](../p01-release-art-20261023/REVIEW-QUEUE.md).

## What may enter v1.0.0 now

Claude's review section F records which static assets are installed and which remain approved but unused. The exact approved S20/S21 assets are already part of the earlier approved hall delivery. Follow the review for any remaining use restrictions.
