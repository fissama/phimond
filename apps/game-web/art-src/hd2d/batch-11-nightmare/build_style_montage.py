#!/usr/bin/env python3
"""Build a style-reference montage from approved assets.

Composes unmodified approved PNGs (padding + nearest scaling only) into one PNG that
can be attached to an image model as a single subject reference. Records the SHA256 of
every original so the job file can prove what was actually attached.

Usage: build_style_montage.py <out.png> <cell_px> <image> [image ...]
"""
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

out = Path(sys.argv[1])
cell = int(sys.argv[2])
paths = [Path(p) for p in sys.argv[3:]]

cols = 2
rows = (len(paths) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cell, rows * cell), (18, 18, 22))
sources = []

for i, p in enumerate(paths):
    im = Image.open(p).convert("RGBA")
    scale = min(cell / im.width, cell / im.height)
    size = (max(1, round(im.width * scale)), max(1, round(im.height * scale)))
    im = im.resize(size, Image.Resampling.NEAREST)
    tile = Image.new("RGBA", (cell, cell), (0, 0, 0, 0))
    tile.alpha_composite(im, ((cell - im.width) // 2, (cell - im.height) // 2))
    # checker so transparent parts stay legible
    bg = Image.new("RGB", (cell, cell), (30, 30, 36))
    for y in range(0, cell, 16):
        for x in range(0, cell, 16):
            if (x // 16 + y // 16) % 2:
                bg.paste((52, 52, 60), (x, y, min(x + 16, cell), min(y + 16, cell)))
    bg.paste(tile, (0, 0), tile)
    sheet.paste(bg, ((i % cols) * cell, (i // cols) * cell))
    sources.append({
        "path": str(p),
        "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        "montage_cell": [i % cols, i // cols],
    })

out.parent.mkdir(parents=True, exist_ok=True)
sheet.save(out)
print(json.dumps({
    "montage": str(out),
    "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
    "size": [sheet.width, sheet.height],
    "sources": sources,
}, ensure_ascii=False, indent=2))
