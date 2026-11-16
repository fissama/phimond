# Summoning Hall ceremonial prop kit — candidate review

Status: **art candidate; pending owner review/approval**. No runtime, scene, manifest, or approval state was changed.

Six props were generated for the Summoning Hall: stained-glass panel, heraldic banner, oracle globe, paired incense braziers, hanging lantern, and ceremonial lectern. Each final is a 256×256 RGBA sprite finished through Sprite Forge and the shared 48-color palette. Individual Forge strict QC and palette binary-alpha/off-palette checks passed. See each prop's `review.md` and `qa.json` for evidence.

The initial 2×3 master sheet was retained as `raw-01.png`. Its sheet-level spill QA **failed** (`cross_cell_components=2`, `cross_cell_visible=2`) and warned (`boundary_band=1621`, `safe_frame=6`). The six props were isolated as individual crops; no failed sheet was treated as accepted. The oracle globe needed a wider isolated crop to exclude neighboring props. Incense smoke was revised once from pink to ivory and reprocessed through Forge and the shared palette.

Style review: carved silhouettes, warm metal/wood highlights and the crimson/gold accent fit the hall better than the rough v1.0.0 set. The oracle globe and glass panel have the highest color density; inspect them at actual in-scene scale before approval. The incense smoke is a static sprite detail, not an animation. These assets remain unintegrated candidates and are not self-approved.

Generation route: built-in Codex ImageGen (`host_image`), followed by `generate2dsprite.py process` and `palette_tool.py build/apply`. ImageGen did not return a model name or cost estimate.
