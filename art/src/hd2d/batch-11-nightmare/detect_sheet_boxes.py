#!/usr/bin/env python3
"""Locate isolated sprites on a flat chroma sheet and report their pixel boxes.

Read-only measurement of a generated sheet. It finds the flat key colour, labels
8-connected blobs of non-key pixels, drops specks, and prints the surviving boxes
ordered top-to-bottom then left-to-right. This lets the job file declare real
source boxes instead of guessed ones.

Usage: detect_sheet_boxes.py <sheet.png> [--min-area N] [--key r,g,b]
"""
import argparse
import json

import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("sheet")
ap.add_argument("--min-area", type=int, default=400)
ap.add_argument("--key", default="255,0,255")
ap.add_argument("--key-tol", type=int, default=40)
ap.add_argument("--out", default=None)
args = ap.parse_args()

key = np.array([int(v) for v in args.key.split(",")])
im = Image.open(args.sheet).convert("RGB")
a = np.asarray(im).astype(np.int16)
dist = np.abs(a - key).sum(axis=2)
bg = dist <= args.key_tol * 3
fg = ~bg

try:
    from scipy import ndimage
    lab, n = ndimage.label(fg, structure=np.ones((3, 3), dtype=int))
    objs = ndimage.find_objects(lab)
except ImportError:
    lab, n = None, None

boxes = []
if lab is not None:
    for i, sl in enumerate(objs, start=1):
        ys, xs = sl
        area = int((lab[sl] == i).sum())
        if area < args.min_area:
            continue
        boxes.append({
            "x0": int(xs.start), "y0": int(ys.start),
            "x1": int(xs.stop), "y1": int(ys.stop),
            "w": int(xs.stop - xs.start), "h": int(ys.stop - ys.start),
            "area": area,
        })
else:  # pragma: no cover - scipy is a hard dependency in practice
    raise SystemExit("scipy is required")

boxes.sort(key=lambda b: (round(b["y0"] / 64), b["x0"]))
key_frac = float(bg.mean())
print(json.dumps({
    "sheet": args.sheet, "size": list(im.size),
    "key": key.tolist(), "key_fraction": round(key_frac, 4),
    "components": len(boxes), "boxes": boxes,
}, ensure_ascii=False, indent=2))
if args.out:
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(boxes, f, ensure_ascii=False, indent=2)
