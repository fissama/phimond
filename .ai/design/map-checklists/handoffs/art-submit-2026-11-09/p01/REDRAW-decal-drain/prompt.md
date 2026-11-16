# REDRAW-decal-drain

Built-in image_gen; raw source preserved as `raw-01.png`.

Prompt: organic asymmetric damp sandstone patch around a small iron drain grate. Source city ground is warm pale stone with dark cracks; style refs guide crisp pixel clusters. Broken paving chunks, muted brown/olive damp discoloration, small centered grate with short bars. Must be an irregular nonrectangular decal, no square slab or separate object. Soft stepped pixel edge, 2–4 tones/material, transparent outside, no glow/shadow/text/watermark/magenta/fringe.

References:
- `.ai/design/map-checklists/refs/city_square.jpg` SHA256 `995db064ece8534304239e06d3882dc472bde1b9a2198a7784d127bfaad61cf0`
- `art/src/hd2d/batch-01-octopath/pebbles-01/final.png` SHA256 `328f80aff0c2acab7ba50d1ce79604854a00c2b481548f6b7267703d0a4c8e8a`
- `art/src/hd2d/batch-01-octopath/pebbles-02/final.png` SHA256 `e33a7f706de6592c7d3badeffa159820c8439a0d806dd62acb5e54a42deb583d`

Pipeline: crop alpha>250 bbox; nearest resize to 224×190; center on 256×256 canvas; binary alpha threshold 250; 40-color quantize.
