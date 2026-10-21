#!/usr/bin/env python3
"""Kiểm tra mép bounding box của các asset HD-2D theo quy chuẩn Claude:
(cột mép ngoài của bbox alpha đặc >35% chiều cao) -> LỖI cắt phẳng mép.
Bỏ qua tile và backdrop (vật thể lặp).
"""
import json, sys, os, glob, pathlib
from PIL import Image
import numpy as np

R = pathlib.Path(__file__).resolve().parents[2]
man_path = R / "apps/game-web/art-src/hd2d/batch-11-desert/manifest.json"

if not man_path.exists():
    print(f"Không tìm thấy {man_path}")
    sys.exit(1)

man = json.load(open(man_path))
errors = []

for a in man["assets"]:
    aid = a["id"]
    cat = a["category"]
    # Bỏ qua tile và backdrop vì chúng được thiết kế lặp toàn viền
    if cat in ("tile", "backdrop"):
        continue

    img_path = R / f"apps/game-web/art-src/hd2d/batch-11-desert/{aid}/final.png"
    if not img_path.exists():
        continue

    img = Image.open(img_path).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    if len(rows) == 0:
        continue

    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()
    h = ymax - ymin + 1
    w = xmax - xmin + 1

    # Kiểm tra cột trái và cột phải (alpha đặc > 50)
    left_dense = np.sum(alpha[ymin:ymax+1, xmin] > 50)
    right_dense = np.sum(alpha[ymin:ymax+1, xmax] > 50)

    l_ratio = left_dense / h
    r_ratio = right_dense / h

    reasons = []
    if l_ratio > 0.35:
        reasons.append(f"Cột mép TRÁI đặc {l_ratio:.1%} ({left_dense}/{h}px)")
    if r_ratio > 0.35:
        reasons.append(f"Cột mép PHẢI đặc {r_ratio:.1%} ({right_dense}/{h}px)")

    if reasons:
        errors.append((aid, reasons))

print(f"=== BBOX EDGE AUDIT: {len(man['assets'])} assets, {len(errors)} LỖI ===")
for aid, r in errors:
    print(f"  [LỖI] {aid:38s}: {', '.join(r)}")

if len(errors) > 0:
    sys.exit(1)
else:
    print("PASS: Tất cả asset (non-tile, non-backdrop) đều có viền tự nhiên, 0 mép cắt phẳng!")
    sys.exit(0)
