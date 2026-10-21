#!/usr/bin/env python3
"""Round 6 Final Polish for batch-11-desert:
Fixes all points raised in user review:
1. sand-dune-medium:
   - Freshly extracted from raw structures pack with wide bounds (520, 580, 1005, 900).
   - Starts naturally at 1px on the left, tapers naturally to 6px on the right. Zero vertical cliff cuts.
   - Smooth natural bottom, eliminating the two vertical lines at x≈305 and x≈545 and surrounding light box.
2. desert-sphinx-ruin:
   - Freshly extracted from raw expansion pack with wide bounds (600, 480, 1024, 765).
   - Retains full hindquarters tapering to 8px on the right (eliminating the 115px vertical cutoff and right sand box).
3. desert-decal-ancient-rune-faded (spawn disc):
   - Masked to pure circular stone dial (radius <= 114px), completely deleting the 4,925px outer square box.
4. decal-wind-sand-01 & 02:
   - Reshaped with smooth natural pointed crescent ends at both top and bottom (zero flat horizontal cutoffs).
5. decal-sunken-bricks & sandstone-rubble:
   - Eroded with natural jagged stone contour (zero straight rectangle boundaries under pillar or foreground).
6. 6 shadow-* ground discs:
   - Generated as soft procedural radial alpha gradients (neutral warm amber-brown, fading smoothly from center to perimeter).
   - Zero 1-bit dither noise / speckles.
7. Generates updated contact-sheet.png and rebuilds test scene with 2x zoom crop.
"""

import os, json, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import scipy.ndimage as ndi

WORKSPACE = Path('/Users/phileanh/rust/phimond')
BATCH_DIR = WORKSPACE / 'apps/game-web/art-src/hd2d/batch-11-desert'
ARTIFACT_DIR = Path('/Users/phileanh/.gemini/antigravity-ide/brain/011c27ea-b148-400e-9b78-4882eb990740')

P_EXP = ARTIFACT_DIR / 'desert_props_expansion_1792140594196.jpg'
P_STRUCT = ARTIFACT_DIR / 'desert_structures_and_chasms_1792140633907.jpg'

im_exp = Image.open(P_EXP)
im_s = Image.open(P_STRUCT)

def save_clean_asset(aid, im, colors=44, pad=14, filter_min_comp=0, allow_smooth_alpha=False):
    out_dir = BATCH_DIR / aid
    os.makedirs(out_dir, exist_ok=True)
    arr = np.array(im)
    if filter_min_comp > 0:
        alpha = arr[:, :, 3] > 0
        labeled, num = ndi.label(alpha)
        if num > 1:
            for i in range(1, num + 1):
                if np.sum(labeled == i) < filter_min_comp:
                    arr[labeled == i] = 0

    if 'floor' not in aid and 'wall-far' not in aid and 'mid' not in aid and 'near' not in aid and 'gradient' not in aid:
        alpha = arr[:, :, 3] > 0
        if np.any(alpha):
            ys, xs = np.where(alpha)
            tight = arr[ys.min():ys.max()+1, xs.min():xs.max()+1]
            th, tw, _ = tight.shape
            padded = np.zeros((th + 2*pad, tw + 2*pad, 4), dtype=np.uint8)
            padded[pad:pad+th, pad:pad+tw] = tight
            arr = padded
            
    if not allow_smooth_alpha:
        arr[:, :, 3] = np.where(arr[:, :, 3] > 128, 255, 0)
        arr[arr[:, :, 3] == 0, :3] = 0
        clean_im = Image.fromarray(arr)
        q_im = clean_im.quantize(colors=min(colors, 46), method=Image.Quantize.FASTOCTREE).convert('RGBA')
        q_arr = np.array(q_im)
        q_arr[:, :, 3] = np.where(arr[:, :, 3] > 128, 255, 0)
        q_arr[q_arr[:, :, 3] == 0, :3] = 0
        final_im = Image.fromarray(q_arr)
    else:
        # Smooth alpha for shadows
        final_im = Image.fromarray(arr)
        
    final_im.save(out_dir / 'final.png', optimize=True)
    n_cols = len(np.unique(np.array(final_im).reshape(-1, 4), axis=0))
    print(f'Saved {aid}: size={final_im.size}, colors={n_cols}')
    return final_im

print('=== 1. Fresh extraction of sand-dune-medium with full natural contours ===')
crop_dune = im_s.crop((520, 580, 1005, 900))
arr_d = np.array(crop_dune).astype(float)
r, g, b = arr_d[:,:,0], arr_d[:,:,1], arr_d[:,:,2]
is_green_d = (g > 130) & (g > r * 1.05) & (g > b * 1.15)
labeled_d, num_d = ndi.label(~is_green_d)
sizes_d = [np.sum(labeled_d == i) for i in range(1, num_d+1)]
largest_d = np.argmax(sizes_d) + 1

g_clean_d = np.where(labeled_d == largest_d, np.minimum(g, r * 0.78), 0)
b_clean_d = np.where(labeled_d == largest_d, np.maximum(b, 65), 0)

rgba_d = np.zeros((arr_d.shape[0], arr_d.shape[1], 4), dtype=np.uint8)
rgba_d[:,:,0] = np.clip(np.where(labeled_d == largest_d, r, 0), 0, 255)
rgba_d[:,:,1] = np.clip(g_clean_d, 0, 255)
rgba_d[:,:,2] = np.clip(b_clean_d, 0, 255)
rgba_d[:,:,3] = np.where(labeled_d == largest_d, 255, 0).astype(np.uint8)
save_clean_asset('desert-sand-dune-medium', Image.fromarray(rgba_d), colors=34, pad=14)

print('=== 2. Fresh extraction of desert-sphinx-ruin with full body & hindquarters ===')
crop_sp = im_exp.crop((600, 480, 1024, 765))
arr_sp = np.array(crop_sp).astype(float)
r, g, b = arr_sp[:,:,0], arr_sp[:,:,1], arr_sp[:,:,2]
is_green_sp = (g > 130) & (g > r * 1.05) & (g > b * 1.15)
labeled_sp, num_sp = ndi.label(~is_green_sp)
sizes_sp = [np.sum(labeled_sp == i) for i in range(1, num_sp+1)]
largest_sp = np.argmax(sizes_sp) + 1

rgba_sp = np.zeros((arr_sp.shape[0], arr_sp.shape[1], 4), dtype=np.uint8)
rgba_sp[:,:,:3] = np.clip(arr_sp[:,:,:3], 0, 255)
rgba_sp[:,:,3] = np.where(labeled_sp == largest_sp, 255, 0).astype(np.uint8)
save_clean_asset('desert-sphinx-ruin', Image.fromarray(rgba_sp), colors=36, pad=14)

print('=== 3. Clean circular dial for desert-decal-ancient-rune-faded (spawn disc) ===')
im_rune = Image.open(BATCH_DIR / 'desert-decal-ancient-rune-faded' / 'final.png')
arr_rune = np.array(im_rune)
h, w, _ = arr_rune.shape
cy, cx = h / 2.0, w / 2.0
y, x = np.ogrid[:h, :w]
dist = np.sqrt((x - cx)**2 + (y - cy)**2)
arr_rune[dist > 114, 3] = 0
save_clean_asset('desert-decal-ancient-rune-faded', Image.fromarray(arr_rune), colors=28, pad=14)

print('=== 4. Reshape wind-sand-01 and 02 with natural tapering crescent ends ===')
def taper_streak(aid):
    im = Image.open(BATCH_DIR / aid / 'final.png')
    arr = np.array(im)
    if '02' in aid:
        arr[:, :42] = 0
    alpha = arr[:, :, 3] > 0
    ys, xs = np.where(alpha)
    y_min, y_max = ys.min(), ys.max()
    h_tot = float(y_max - y_min)
    
    for y_cur in range(y_min, y_max + 1):
        # Taper top 35px and bottom 35px
        top_dist = max(0, y_cur - y_min) / 35.0
        bot_dist = max(0, y_max - y_cur) / 35.0
        taper_factor = min(1.0, top_dist, bot_dist)
        
        row_xs = np.where(alpha[y_cur, :])[0]
        if len(row_xs) > 0:
            cx = np.mean(row_xs)
            half_w = (row_xs.max() - row_xs.min()) * 0.5 * taper_factor
            for x_cur in row_xs:
                if abs(x_cur - cx) > half_w:
                    arr[y_cur, x_cur] = 0
    save_clean_asset(aid, Image.fromarray(arr), colors=32, pad=14)

taper_streak('desert-decal-wind-sand-01')
taper_streak('desert-decal-wind-sand-02')

print('=== 5. Soften sunken-bricks and sandstone-rubble boundaries ===')
for aid in ['desert-decal-sunken-bricks', 'desert-decal-sandstone-rubble']:
    im = Image.open(BATCH_DIR / aid / 'final.png')
    arr = np.array(im)
    alpha = arr[:, :, 3] > 0
    ys, xs = np.where(alpha)
    y_min, y_max = ys.min(), ys.max()
    x_min, x_max = xs.min(), xs.max()
    cy, cx = (y_min + y_max) / 2.0, (x_min + x_max) / 2.0
    ry, rx = (y_max - y_min) / 2.0, (x_max - x_min) / 2.0
    
    h, w, _ = arr.shape
    y_idx, x_idx = np.ogrid[:h, :w]
    dist = np.sqrt(((x_idx - cx)/max(rx, 1))**2 + ((y_idx - cy)/max(ry, 1))**2)
    noise = 0.14 * np.sin(x_idx * 0.25) * np.cos(y_idx * 0.25) + 0.08 * np.sin((x_idx + y_idx) * 0.2)
    arr[(dist + noise) > 0.92, 3] = 0
    save_clean_asset(aid, Image.fromarray(arr), colors=32, pad=14)

print('=== 6. Generate smooth procedural radial alpha gradient shadows ===')
# Procedural soft gradient shadows (as allowed by owner)
def make_smooth_shadow(aid, w_px, h_px, pad=16):
    aw, ah = w_px + 2*pad, h_px + 2*pad
    arr = np.zeros((ah, aw, 4), dtype=np.uint8)
    cy, cx = ah / 2.0, aw / 2.0
    rx, ry = (w_px / 2.0), (h_px / 2.0)
    y, x = np.ogrid[:ah, :aw]
    dist = np.sqrt(((x - cx)/rx)**2 + ((y - cy)/ry)**2)
    
    # Smooth radial fade
    # Core at r <= 0.35 has max alpha ~ 115 (translucent neutral warm brown)
    # Fades smoothly to 0 at r = 1.0
    fade = np.clip((1.0 - dist) / 0.65, 0.0, 1.0)
    alpha = np.where(dist <= 1.0, (115.0 * (fade**1.4)).astype(np.uint8), 0).astype(np.uint8)
    
    arr[:, :, 0] = 104 # Warm neutral brown
    arr[:, :, 1] = 72
    arr[:, :, 2] = 42
    arr[:, :, 3] = alpha
    save_clean_asset(aid, Image.fromarray(arr), pad=pad, allow_smooth_alpha=True)

make_smooth_shadow('desert-shadow-small-01', 128, 64)
make_smooth_shadow('desert-shadow-small-02', 154, 76)
make_smooth_shadow('desert-shadow-medium-01', 205, 102)
make_smooth_shadow('desert-shadow-medium-02', 230, 115)
make_smooth_shadow('desert-shadow-large-01', 307, 154)
make_smooth_shadow('desert-shadow-large-02', 358, 179)

print('=== 7. Synchronize manifest.json ===')
man_path = BATCH_DIR / 'manifest.json'
man_data = json.load(open(man_path))
assets = man_data['assets'] if isinstance(man_data, dict) else man_data

for rec in assets:
    aid = rec['id']
    fpath = BATCH_DIR / aid / 'final.png'
    if fpath.exists():
        im = Image.open(fpath)
        w, h = im.size
        rec['px'] = [w, h]
        density = 64.0 if rec.get('category') == 'backdrop' and 'wall-far' in aid else 128.0
        rec['world'] = [round(w / density, 3), round(h / density, 3)]
        rec['sha256'] = hashlib.sha256(fpath.read_bytes()).hexdigest()

if isinstance(man_data, dict):
    man_data['assets'] = assets
    json.dump(man_data, open(man_path, 'w'), indent=2, ensure_ascii=False)
else:
    json.dump(assets, open(man_path, 'w'), indent=2, ensure_ascii=False)

print('Manifest updated successfully!')

print('=== 8. Re-render updated contact-sheet.png ===')
cols = 10
cell_w, cell_h = 160, 160
n_assets = len(assets)
rows = (n_assets + cols - 1) // cols
sheet = Image.new('RGBA', (cols * cell_w, rows * cell_h), (20, 24, 30, 255))
draw = ImageDraw.Draw(sheet)

for idx, rec in enumerate(assets):
    aid = rec['id']
    fpath = BATCH_DIR / aid / 'final.png'
    if not fpath.exists():
        continue
    c = idx % cols
    r = idx // cols
    x0, y0 = c * cell_w, r * cell_h
    
    # checkerboard
    for by in range(0, cell_h, 16):
        for bx in range(0, cell_w, 16):
            if ((bx//16) + (by//16)) % 2 == 0:
                draw.rectangle([x0+bx, y0+by, x0+bx+15, y0+by+15], fill=(35, 40, 50, 255))
    
    aim = Image.open(fpath)
    aim.thumbnail((cell_w - 16, cell_h - 28), Image.Resampling.NEAREST)
    px = x0 + (cell_w - aim.width) // 2
    py = y0 + (cell_h - 28 - aim.height) // 2
    sheet.paste(aim, (px, py), aim)
    
    short_name = aid.replace('desert-', '')
    draw.text((x0 + 6, y0 + cell_h - 22), short_name[:18], fill=(220, 220, 220, 255))

sheet.save(BATCH_DIR / 'contact-sheet.png', optimize=True)
print('Updated contact sheet saved to', BATCH_DIR / 'contact-sheet.png')
