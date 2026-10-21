# Kit verification — 2026-10-05

Scope: dispatch preparation and local preview utility; no new species generated,
no candidate accepted, no runtime integration, no server restart or deployment.

- `p10_redraw_jobs.py check-inputs`: PASS, exact 150 jobs + 2 excluded style anchors;
  input hashes match, 30 batches of 5, canonical mappings and isolated output paths.
- `python -B -m unittest discover -s tools/assets -p test_p10_redraw_kit.py`:
  6 tests passed, 0 skipped. Covers real input hashes, duplicate assignment,
  hash drift, output scope escape, byte-identical preview copy / overwrite refusal,
  and rejection of invalid geometry before creating a preview.
- All 30 saved batch briefs generated from the worker template and manifest.
- Existing `p10_provenance.py` pinned to
  `8510ed33aea979eff591f2155640c9c1d3db0efb`: 304 assets intact,
  0 modified, 0 missing; original manifest intact.

Limitations: preview export verified with synthetic geometry fixtures, not a
new production character. Browser playback has not been manually verified in
this task. The first actual batch must verify animation visually; automated
checks do not certify style, anatomy, meaningful poses or loop quality.

Existing concurrent runtime edits and other tasks' helper/art files were not
included in this delivery. The kit remains local/uncommitted for review.
