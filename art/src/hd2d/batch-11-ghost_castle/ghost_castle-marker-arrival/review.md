# ghost_castle-marker-arrival — self visual review

- Inspected all four animation frames on dark and checker at 4×. The rune ring stays centered and stable; the small amber/ivory spark moves around the inner ring.
- Frame canvas is 128×128, 48 shared colors, binary alpha, and all frames share the same center registration. See `qa.json` for frame margins and pipeline checks.
- Source sheet default QC warned `safe_frame` at 15% margin (raw horizontal margin 7.0–7.6%); strict QC with 6% safe margin passed and processing resized each frame into the 128px canvas with visible margins.
- Candidate only; Claude/owner approval remains pending.
