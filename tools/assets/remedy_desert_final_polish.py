#!/usr/bin/env python3
"""
Final polish on batch-11-desert:
1. sand-dune-medium: clean left slope dark artifact and erode 1px light halo.
2. desert-sphinx-ruin: erode 1px light halo.
3. wind-sand-01 & 02: clean tail orphan pixels and taper smoothly to 0.
4. desert-shadow-*: boost max_alpha from 115 to 150 for visible grounding.
"""

import os, json, hashlib
from pathlib import Path
from PIL import Image
import numpy as np
import scipy.ndimage as ndi

WORKSPACE = Path('/Users/phileanh/rust/phimond')
BATCH_DIR = WORKSPACE / 'apps/game-web/art-src/hd2d/batch-11-desert'

print("=== 1. Polishing sand-dune-medium ===")
dune_path = BATCH_DIR / 'desert-sand-dune-medium/final.png'
im_dune = Image.open(dune_path)
arr_d = np.array(im_dune)
alpha_d = arr_d[:, :, 3] > 0

# Remove 1px perimeter fringe to eliminate light halo
eroded_alpha_d = ndi.binary_erosion(alpha_d, iterations=1)
# Clean left dark spot (x < 100, dark pixels)
r, g, b = arr_d[:,:,0], arr_d[:,:,1], arr_d[:,:,2]
dark_spot = (arr_d[:, :, 3] > 0) & (r < 75) & (g < 60)
eroded_alpha_d[dark_spot] = False

arr_d[:, :, 3] = np.where(eroded_alpha_d, 255, 0).astype(np.uint8)
arr_d[arr_d[:, :, 3] == 0] = [0, 0, 0, 0]
Image.fromarray(arr_d).save(dune_path, optimize=True)
print("Saved cleaned desert-sand-dune-medium")

print("=== 2. Polishing desert-sphinx-ruin ===")
sp_path = BATCH_DIR / 'desert-sphinx-ruin/final.png'
im_sp = Image.open(sp_path)
arr_sp = np.array(im_sp)
alpha_sp = arr_sp[:, :, 3] > 0
eroded_alpha_sp = ndi.binary_erosion(alpha_sp, iterations=1)
arr_sp[:, :, 3] = np.where(eroded_alpha_sp, 255, 0).astype(np.uint8)
arr_sp[arr_sp[:, :, 3] == 0] = [0, 0, 0, 0]
Image.fromarray(arr_sp).save(sp_path, optimize=True)
print("Saved cleaned desert-sphinx-ruin")

print("=== 3. Polishing wind-sand-01 & 02 tails ===")
for aid in ['desert-decal-wind-sand-01', 'desert-decal-wind-sand-02']:
    ws_path = BATCH_DIR / aid / 'final.png'
    im_ws = Image.open(ws_path)
    arr_ws = np.array(im_ws)
    # Remove small orphan components < 15 px
    labeled, num = ndi.label(arr_ws[:, :, 3] > 0)
    if num > 1:
        sizes = np.bincount(labeled.ravel())
        mask = np.isin(labeled, np.where(sizes >= 15)[0])
        mask[0, 0] = False
        arr_ws[~mask] = [0, 0, 0, 0]
    
    # Smooth taper the bottom 15 rows to clean point
    alpha = arr_ws[:, :, 3] > 0
    ys, xs = np.where(alpha)
    if len(ys) > 0:
        y_max = ys.max()
        for y in range(y_max - 10, y_max + 1):
            row_xs = np.where(alpha[y, :])[0]
            if len(row_xs) > 6:
                # trim outer 2 pixels
                arr_ws[y, row_xs[:1], 3] = 0
                arr_ws[y, row_xs[-1:], 3] = 0
    arr_ws[arr_ws[:, :, 3] == 0] = [0, 0, 0, 0]
    Image.fromarray(arr_ws).save(ws_path, optimize=True)
    print(f"Saved cleaned {aid}")

print("=== 4. Boosting desert-shadow-* max_alpha to 150 ===")
def make_smooth_shadow(aid, w_px, h_px, pad=16, max_alpha=150):
    aw, ah = w_px + 2*pad, h_px + 2*pad
    arr = np.zeros((ah, aw, 4), dtype=np.uint8)
    cy, cx = ah / 2.0, aw / 2.0
    rx, ry = (w_px / 2.0), (h_px / 2.0)
    y, x = np.ogrid[:ah, :aw]
    dist = np.sqrt(((x - cx)/rx)**2 + ((y - cy)/ry)**2)
    
    fade = np.clip((1.0 - dist) / 0.70, 0.0, 1.0)
    alpha = np.where(dist <= 1.0, (max_alpha * (fade**1.3)).astype(np.uint8), 0).astype(np.uint8)
    
    arr[:, :, 0] = 96
    arr[:, :, 1] = 65
    arr[:, :, 2] = 36
    arr[:, :, 3] = alpha
    
    out_dir = BATCH_DIR / aid
    out_dir.mkdir(parents=True, exist_ok=True)
    Image.fromarray(arr).save(out_dir / 'final.png', optimize=True)
    print(f"Saved boosted shadow {aid}: max_alpha={max_alpha}")

make_smooth_shadow('desert-shadow-small-01', 128, 64)
make_smooth_shadow('desert-shadow-small-02', 154, 76)
make_smooth_shadow('desert-shadow-medium-01', 205, 102)
make_smooth_shadow('desert-shadow-medium-02', 230, 115)
make_smooth_shadow('desert-shadow-large-01', 307, 154)
make_smooth_shadow('desert-shadow-large-02', 358, 179)

# Update manifest sha256 and px
man_path = BATCH_DIR / 'manifest.json'
man_data = json.load(open(man_path))
assets = man_data['assets'] if isinstance(man_data, dict) else man_data
for rec in assets:
    fp = BATCH_DIR / rec['file']
    if fp.exists():
        rec['sha256'] = hashlib.sha256(fp.read_bytes()).hexdigest()
        im = Image.open(fp)
        rec['px'] = list(im.size)

if isinstance(man_data, dict):
    man_data['assets'] = assets
    json.dump(man_data, open(man_path, 'w'), indent=2, ensure_ascii=False)
else:
    json.dump(assets, open(man_path, 'w'), indent=2, ensure_ascii=False)

print("Updated desert manifest.json successfully!")
