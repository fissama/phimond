# Summon hall extra assets — 2026-10-29

Six PNG deliverables are in the parent directory:

| File | Size | Visible RGB colors | Alpha |
| --- | --- | --- | --- |
| stone-floor-b.png | 512×512 | 34 | opaque |
| city-backdrop-wide.png | 2432×486 | 48 | opaque |
| city-near-roofs.png | 2432×220 | 47 | binary |
| floor-light-1.png | 256×256 | 31 | binary |
| floor-light-2.png | 256×256 | 31 | binary |
| floor-light-3.png | 256×256 | 31 | binary |

Transparent assets have one additional transparent RGBA entry, so total palette counts remain at or below 48/32. Exact dimensions, alpha values {0,255}, absence of magenta, city flat top sky and opaque roofs baseline are checked by `verify.py`. `verification.json` records measured boundary differences and limitations. Technical checks do not certify subjective visual acceptance.

## Review

Open `review.html` for the contact sheet, floor B repeated 3×3, old/new floor mixed 3×3, and roofs repeated twice at actual pixel size. `contact-sheet.png` is the compact preview. The roofs have an internal 1216px period, repeated twice to form the 2432px asset. Visual joins still need owner review.

**WARN floor-zero-reuse:** The absolute requirement that every brick/crack shape differ is not fully satisfied/certified. A 2–8px collar retains partial reference boundary fragments to preserve A/B compatibility. The generated interior has different arrangements and cracks; 85.6% of its RGBA pixels differ from the reference. That statistic is not a proof that every shape is unique.

## Provenance and reproduction

- Art source: `host_image`, built-in `image_gen.imagegen`, six separate generation calls using the supplied references. Model: tool default; monetary cost not exposed.
- `raw/`: unchanged copies of all six generated PNGs, retaining originals in Codex generated_images too.
- `prompts.json`: full generation prompts, including common style block and explicit reference roles. Native transparent output replaces the intermediate magenta key stage.
- `sources.json`: original tool output paths.
- `finalize.mjs`: nearest sizing, hard minimum-error edge cuts, binary ordered alpha, palette conformance, and exported repeat previews. No procedural replacement artwork.
- `preview.mjs`: preview-only contact composition and HTML.
- Reproduce: run `node finalize.mjs`, `python3 verify.py`, and `node preview.mjs` from this directory. Scripts use the bundled Sharp/pngjs installation and Python Pillow/numpy.
- `doctor.json`: host image generation is ready; optional unrelated render/video/API routes report missing dependencies/configuration and were not used.

## Workspace validation

Fetched origin before work. Existing unrelated dirty work and three local commits were present; those were not staged, committed, pushed, reset, or removed. Deliverables remain uncommitted. This asset-only task is not a phase/sprint delivery.

Server source was unchanged from committed HEAD `4d29a735`; `go build -o /tmp/phimond-server ./cmd/server` passed. Server restarted with `GAME_METRICS=1`, database `phimond_reconstruction`, address `127.0.0.1:8090`. PID at validation: `55112`. `/healthz` returned `{"service":"Phimond","status":"ok"}`. Log: `/tmp/p00-serve.log`. No Godot listener on 6007. No runtime scene integration is included in this deliverable.
