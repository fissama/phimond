# Rejected candidate — N01

Codex image_gen returned a transparent sprite-like UI plate; ffmpeg converted it to 320×88 with nearest scaling and a 48-color palette. Mechanical QA: 33 RGBA colors, alpha levels 0/255, 107 opaque pixels matched the magenta-fringe threshold, 0 near-black opaque pixels, no opaque pixels on the outer top/bottom rows. Reject: pink fringe remains and the badge/title-strip proportions miss the prompt (ring roughly 62 px rather than 56 px; main strip roughly 230 px rather than about 150 px). Not a deliverable.
