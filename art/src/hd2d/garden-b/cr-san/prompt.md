# cr-san — ImageGen prompts and provenance

Character from C07: Sắn (Lv46), cassava puppy; brown root tail, palmate leaves, friendly and loyal. Eight ImageGen outputs retained as `raw-01.png` through `raw-08.png`. `raw-03.png` and `raw-04.png` used the packed sprout frame as a direct image reference to match plant f4 to sprout f1. `raw-07.png` is the best measured candidate; SHA-256 `b866871760b5b045b74536c2132bf9d688b07bb144d64c6dffa19583da4d4435`.

Reference SHA-256:
- Pilot style anchor `cr-bac-ha/final.png`: `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`
- Pilot style anchor `cr-moc-nhi/final.png`: `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`

The prompts requested a 4×5 bright-magenta-key pixel atlas, hard pixel clusters, warm brown contours, a tiny sprout → medium grow → mature puppy progression, a waving harvest sequence and seed-to-sprout plant sequence. Attempts 1, 4, 5, 6, and 8 failed packing because no common scale ≥0.6 fits all source components in safe bounds. Attempts 2, 3 and 7 packed. Raw-07 passed all mechanical gates, but its 4× preview retains visible pink/violet fringe. No post-generation pixel edits were performed.
