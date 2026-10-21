# Targeted image repair template

Attach candidate + original identity refs + both approved style refs to the
image-editing tool. Inspect all attached files before editing. Save a new attempt,
never overwrite the candidate being reviewed. Fill concrete findings below.

```text
Repair this Phimond 20-pose sprite sheet for [NAME / CANONICAL ID].
Candidate reference hash: [SHA256].
Reference roles: [EXACT ATTACHMENT ORDER AND ROLES].
Identity lock: [ANATOMY, PALETTE, WEAPONS/HANDS, CLOTHING, SILHOUETTE].

Fix these specific errors, using row/column indexed from 1:
- [R?C?: observed error → required visual correction]
- [R?C?: observed error → required visual correction]

Preserve the identity, palette, outline style, framing and successful pose intent
of the other cells. Keep weapons/accessories in all 20 frames, including cast
and prone down. Do not hide defects with glow or opaque effects.
Preserve exact 4×5 order: idle loop / move loop / basic attack left / cast left
/ hurt-to-fully-down. True RGBA alpha, 1124×1405, 281×281 cells, all alpha>0
inside local [22,259). No labels, grid, scenery or baked checkerboard.
Return the complete repaired sheet, not a cropped fragment or diagram.
```

Image editing can also change cells that were already good. Recheck all 20 after
each attempt, record the new hash, rerun mechanical and visual review. Do not
claim unchanged pixels without comparison. Stop at the worker's retry budget.
