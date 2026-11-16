# S23 male side-run — Codex visual review — 2026-10-30

Reviewed the current `player-male.run.png`, all eight frames in `player-male.run.review.png`, and the enlarged frame 1/frame 5 comparison in `player-male.run.contact-1-5.review4x.png`.

## Results

- Frame 1: brown/near leg reaches forward while blue/far leg trails.
- Frame 5: blue/far leg reaches forward while brown/near leg trails. This is a clear opposite contact pose, so the key visual gait requirement passes manual inspection.
- Head/torso scale remains consistent across the eight frames; the fixed registration method uses one uniform scale and translation only. QA reports body heights 166–168 px around a 167 px target. No detached alpha pixels were found by its isolated-pixel check.
- Mechanical envelope: 1536×192, 8 frames at 192×192, pivot [96,184], 48 colors, no partial alpha, `warnings: []`.
- Automated `leg_alternation` remains `needs-visual-review` because the luminance heuristic cannot classify most NEAR/FAR pairs; it did not report a duplicated half-cycle. This manual comparison resolves that specific unknown for visual review but does not change the original QA envelope.

## Decision

This is a credible S23 male side-run candidate and can be sent to Claude for owner approval. It is not yet the approved S24 style anchor. Do not mark `approved:true` or install it until owner approval. Remaining production validation includes game-size playback and the other five player strips.
