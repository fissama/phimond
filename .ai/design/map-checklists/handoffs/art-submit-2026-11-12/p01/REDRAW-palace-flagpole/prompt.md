# REDRAW-palace-flagpole

Built-in image_gen, raw preserved as `raw-01.png`.

Prompt: standalone ornate brass and dark wood palace flagpole with finial, short blank deep teal banner, lightly curling; full pole and base visible. Approx. 2.1×3.4 world units. Muted sandstone/gold/teal city palette, warm upper-left light, dark outline, 2–4 firm tones, crisp pixels, transparent margins. No ground/shadow, glow, text/logo, magenta, smooth gradient, extra flags/scenery.

References (source content/palette, style only):
- `.ai/design/map-checklists/refs/city_royal_palace.jpg` SHA256 `4824318a48f0ad36193b7aa73689f7929175b3468a02695f6cd554b3cabbd524`
- `art/src/hd2d/batch-01-octopath/signpost-blank/final.png` SHA256 `9cc53bec8892542b0d7776fa659a8c84b5b9c9d56c4f7981cf85dfe19b59153c`

Pipeline: alpha>240 bbox crop; nearest resize to fit 252×424; center on 268×440 canvas; binary alpha threshold 127; 40-color quantize.
