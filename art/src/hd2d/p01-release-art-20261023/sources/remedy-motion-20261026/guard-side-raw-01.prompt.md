# Guard rear run candidate 01

- Generated: 2026-10-27 via built-in ImageGen in this Codex session.
- Source image: `guard-side-raw-01.png` (raw is preserved; not installed into delivery).
- Prompt references: `walker-guard-approved-idle-6x.png`, `guide/guide.png`.
- Intended layout: 4 columns × 2 rows, eight-frame rear-facing run, spear upright on screen-right.
- Background: flat `#FF00FF` chroma key; extracted by `scale_frames.py --key magenta`.
- Processing: `finish_candidate.py --rows 2 --cols 4 --facing vertical --key magenta`; palette build/apply (48 colors), registered 192×192 frames, fixed anchor (96,184), Sprite Forge `sheet_qc.py`.
- QA: FAIL. `identity_head_ratio` frame 0 = 0.943 against [0.95,1.05]. Other identity residual and torso drift passed. Auto phase/leg checks are skipped for vertical-facing motion; detailed alternation diagnostics are not valid for this facing and must not be treated as a gate result.
- Approval: false. Requires a corrected generation and human visual approval before release use.
- Generated source SHA256 and candidate SHA256 are recorded in `guard-side-candidate-01/candidate-qa.json`.

The attempted follow-up edit changed multiple cells, so it was rejected and not processed or substituted.
