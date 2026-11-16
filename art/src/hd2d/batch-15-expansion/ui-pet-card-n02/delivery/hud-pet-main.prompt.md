# N02 `hud-pet-main.png`

Generated with Codex built-in ImageGen (`host_image`) using the 360×128 layout guide and approved `ui-minimap.png` as style reference. Prompt: create an Octopath-like pixel-art pet HUD card following the supplied geometry guide; dark teal plaque, thin double gold frame, portrait ring centered (68,64), 104 px diameter; level badge centered (104,100), 28 px diameter; empty magenta HP trough x132–344/y40–52 and MP trough x132–344/y62–72, muted red/blue ends; transparent magenta outside and within the wells; no text/icons; crisp hard edges, ≤48 colors.

Processing: resize the model result to 360×128 with Lanczos to match the exact contract canvas, key with `assemble_frames.py --key chroma --key-color magenta --key-quality auto --pixel-art`, build a 48-color palette and apply with `palette_tool.py`. This is a candidate for owner review; geometry is close but not accepted as exact by this report.
