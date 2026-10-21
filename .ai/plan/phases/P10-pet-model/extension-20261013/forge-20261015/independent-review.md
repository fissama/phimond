# Independent review — Forge master proposals, 2026-10-15

Five single master stills are ready for **conditional owner design review**. No hard missing/cut anatomy was observed. These are not animated atlases, approved masters or runtime assets.

## Exact source verification

- All five hashes match the proposal manifest and original image-tool outputs byte-for-byte.
- Native RGBA source dimensions: 1254×1254. References match their recorded hashes.
- Original 152 registry and 919 frozen file hashes remain unchanged. Owner-approved 0154/0156/0158 exact bytes remain unchanged.
- Visually reviewed at source resolution and in-memory 64/96 px nearest-neighbor previews; no source image was edited.

## Proposals

### species_0153

SHA256: `da5812328fc08e3a88dd172d2c02a3d9a1f8da326f5e7f253d3076d1ed4f759a`

[Master proposal](/Users/phileanh/rust/phimond/.ai/plan/phases/P10-pet-model/extension-20261013/forge-20261015/species_0153/master-proposal.png)

- Full LEFT-facing four-legged elegant deer; TWO natural woody branched antlers and leafy moss remain. Large mounted golden moon ornaments removed.
- Branches curve but read primarily as a natural branched rack; how strongly the crescent curvature should read remains owner judgment. Small flank crescent retained.
- Antler-led basic motion and gait cannot be evaluated from one rest still.
- Alpha bounds>0: `[0, 21, 1226, 1230]`; bounds>16: `[325, 146, 1008, 1102]`. Visible body has framing room; faint edge noise is a preprocessing concern.

### species_0155

SHA256: `6bd6b293235b20f2138a2164ed00da9063c11d8ccaa5384316bdff510854800c`

[Master proposal](/Users/phileanh/rust/phimond/.ai/plan/phases/P10-pet-model/extension-20261013/forge-20261015/species_0155/master-proposal.png)

- Full LEFT-facing mature night-blue/gold dragon, chest light core, four legs, two folded wings with far wing partly occluded and one curved star-tip tail.
- Noble face and night/star identity preserved. Tiny overlapping star glints at tail tip are effect highlights, not extra anatomical tail.
- Latest request for richer basic/skill FX cannot be satisfied or evaluated by a rest master still; requires approved-master action generation.
- Alpha bounds>0: `[0, 23, 1236, 1216]`; bounds>16: `[134, 242, 1193, 1054]`. Visible body has framing room; faint edge noise is a preprocessing concern.

### species_0157

SHA256: `0ec22f256c9e8f106509bdafb302093501497bd1fe283b5afb877747b111f084`

[Master proposal](/Users/phileanh/rust/phimond/.ai/plan/phases/P10-pet-model/extension-20261013/forge-20261015/species_0157/master-proposal.png)

- Full LEFT-facing sinister ONE ocular-outline creature, pupil replaced by central vertical black mouth lined with ivory fangs; no floating crown runes. Six curled tentacle tips are visually identifiable in this still.
- Fangs/maw distinguish it from the previous ordinary pupil at64/96px; this master is partly open rather than fully closed. Closed-to-open performance requires animation and owner approval.
- No extra ocular portal, gore or disconnected anatomy observed.
- Alpha bounds>0: `[0, 21, 1242, 1238]`; bounds>16: `[232, 241, 1180, 1037]`. Visible body has framing room; faint edge noise is a preprocessing concern.

### species_0159

SHA256: `1fca2058e4c178af4f007d7899eda479732a13ddf2607809425f12de658331df`

[Master proposal](/Users/phileanh/rust/phimond/.ai/plan/phases/P10-pet-model/extension-20261013/forge-20261015/species_0159/master-proposal.png)

- Full LEFT-facing levitating upright golden dragon, TWO clawed arms and TWO small dangling hind legs. TWO compact angular wings, far wing partly occluded.
- TWO separate tails each ending in ONE integrated jade/gold leaf-shaped seal, no old chest/flank seal medallions. Clear separation of tail ends; plain ivory/gold torso.
- Tail seal engravings compress at64px but the two tips remain distinct. Claw-then-tail-seal choreography/float motion cannot be evaluated from one still.
- Alpha bounds>0: `[0, 9, 1240, 1254]`; bounds>16: `[238, 144, 1118, 1078]`. Visible body has framing room; faint edge noise is a preprocessing concern.

### species_0160

SHA256: `768178e5967ec6804b40e4c6f5c6a2e78a960f820af9ed80d4a73d139f636121`

[Master proposal](/Users/phileanh/rust/phimond/.ai/plan/phases/P10-pet-model/extension-20261013/forge-20261015/species_0160/master-proposal.png)

- Full LEFT-facing youthful adult masculine character with muscular bare torso, two horns, one spear, opposite caster hand and purple leg armor.
- White/pale-lavender neat center-part curtain hair with cleaner side/back silhouette; focused cool gaze and neutral mouth. Exact apparent age around20 and hairstyle preference remain owner judgment.
- Face/hair cues read at96px but are tiny at64px. No observed cut feet, spear or detached recovery oval in this rest proposal.
- Alpha bounds>0: `[25, 17, 1230, 1254]`; bounds>16: `[182, 205, 1086, 1176]`. Visible body has framing room; faint edge noise is a preprocessing concern.

## Remaining gates

- Human approval is required before master approval or animation work. No approval has been granted by this reviewer.
- Doctor video route: `none`; no video generation route: write a motion brief and report the missing capability (supplied clips can still be processed).
- One still cannot prove gait, loop seams, skill choreography, down pose or a 20-frame contract. No animation or pixel palette finish was generated by this route.
- Pixel-scale/palette/alpha finishing and game integration remain pending. Strong style/age/face/antler preferences require owner judgment.

## Published diagnostic warnings and failures

These diagnostics belong to older raw character sheets and are not current-master results. No claim that all checks pass is made. Full source inputs/check structures are retained verbatim in independent-review.json and qa-warnings-verbatim.json.

Source file: `.ai/plan/phases/P10-pet-model/extension-20261013/forge-20261015/qa-existing-ma-chu/sheet-qc.json`
- `cross_cell_components` fail: value `17`; threshold `0`. solid parts crossing a cell line are cut or misassigned when the sheet is sliced
- `cross_cell_visible` fail: value `17`; threshold `0`. the same test on the visible edge (alpha > 16)
- `boundary_band` warn: value `4966`; threshold `0`. solid pixels within 6 px of a cell line; a different crop or rounding can cut them
- `safe_frame` warn: value `20`; threshold `0`. owned art closer than 15% of the cell to its edge; ask for more margin next time
- `faint_specks` warn: value `{"floor_px": 224097, "detached_components": 43}`; threshold `0`. alpha haze and detached specks; process removes them with --alpha-hygiene both

Source file: `.ai/plan/phases/P10-pet-model/extension-20261013/forge-20261015/qa-existing-ma-nhan/sheet-qc.json`
- `cross_cell_components` fail: value `16`; threshold `0`. solid parts crossing a cell line are cut or misassigned when the sheet is sliced
- `cross_cell_visible` fail: value `15`; threshold `0`. the same test on the visible edge (alpha > 16)
- `boundary_band` warn: value `4518`; threshold `0`. solid pixels within 6 px of a cell line; a different crop or rounding can cut them
- `safe_frame` warn: value `20`; threshold `0`. owned art closer than 15% of the cell to its edge; ask for more margin next time
- `faint_specks` warn: value `{"floor_px": 103577, "detached_components": 47}`; threshold `0`. alpha haze and detached specks; process removes them with --alpha-hygiene both

Doctor non-OK checks (verbatim detail):
- `deps.scipy` WARN: not installed; needed for faster labelling and keying (forge_core falls back to numpy)
- `deps.resvg-py` MISSING: not installed; needed for codeart2d SVG rendering (PixelSpec needs only numpy and Pillow)
- `skills.present` WARN: ~/.codex/skills: missing codeart2d
- `media.api.openai` MISSING: OPENAI_API_KEY is not configured
- `media.api.gemini` MISSING: GOOGLE_API_KEY or GEMINI_API_KEY is not configured
- `media.api.xai` MISSING: XAI_API_KEY is not configured
- `media.api.byteplus` MISSING: ARK_API_KEY is not configured
- `media.api.fal` MISSING: FAL_KEY is not configured
- `cli.grok` MISSING: Grok Build CLI not found on PATH or in $GROK_HOME/bin
- `route.codex-cli:image_gen` UNKNOWN: PRESENT: no proof for this version

Only independent-review.json/md were written by the reviewer. Old artwork, approval records, manifests and runtime selection were not changed.
