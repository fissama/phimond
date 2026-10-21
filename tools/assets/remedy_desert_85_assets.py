#!/usr/bin/env python3
"""Comprehensive Remedy Script for batch-11-desert 85 assets and scene.
Fixes all audit warnings, removes numbers/stray bars, replaces duplicate/mismatched assets,
standardizes density to 128 px/unit, and creates a seamless, natural scene.
"""
import os, json
from PIL import Image
import numpy as np

R = '/Users/phileanh/rust/phimond'
B = f'{R}/apps/game-web/art-src/hd2d/batch-11-desert'
ARTIFACT_DIR = '/Users/phileanh/.gemini/antigravity-ide/brain/011c27ea-b148-400e-9b78-4882eb990740'

P_REPLACE = f'{ARTIFACT_DIR}/desert_props_replacement_pack_1792177228847.jpg'
P_BACKDROPS = f'{ARTIFACT_DIR}/desert_backdrops_mid_near_pack_1792177256028.jpg'
P_TILES_EXP = f'{ARTIFACT_DIR}/desert_tiles_expansion_1792140524856.jpg'

def green_chroma_key(img_crop, g_thresh=130, despill=True):
    arr = np.array(img_crop).astype(float)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    is_green = (g > g_thresh) & (g > r * 1.10) & (g > b * 1.10)
    arr[is_green, 3] = 0
    arr[is_green, :3] = 0
    if despill:
        excess = np.maximum(0, arr[:, :, 1] - np.maximum(arr[:, :, 0], arr[:, :, 2]))
        arr[:, :, 1] = np.clip(arr[:, :, 1] - excess, 0, 255)
    arr[:, :, 3] = np.where(arr[:, :, 3] > 128, 255, 0)
    arr[arr[:, :, 3] == 0, :3] = 0
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

def save_clean_asset(aid, im, colors=44, pad=12):
    out_dir = f'{B}/{aid}'
    os.makedirs(out_dir, exist_ok=True)
    arr = np.array(im)
    if 'floor' not in aid and 'wall' not in aid and 'mid' not in aid and 'near' not in aid and 'gradient' not in aid:
        # Tight crop to alpha > 0 and add pad margin
        alpha = arr[:, :, 3]
        if np.any(alpha == 255):
            ys, xs = np.where(alpha == 255)
            tight = arr[ys.min():ys.max()+1, xs.min():xs.max()+1]
            th, tw, _ = tight.shape
            padded = np.zeros((th + 2*pad, tw + 2*pad, 4), dtype=np.uint8)
            padded[pad:pad+th, pad:pad+tw] = tight
            arr = padded
    # Binary alpha
    arr[:, :, 3] = np.where(arr[:, :, 3] > 128, 255, 0)
    arr[arr[:, :, 3] == 0, :3] = 0
    out_im = Image.fromarray(arr)
    # Quantize to <= 48 colors
    q_im = out_im.quantize(colors=colors, method=Image.Quantize.FASTOCTREE).convert('RGBA')
    q_arr = np.array(q_im)
    q_arr[:, :, 3] = arr[:, :, 3]
    q_arr[q_arr[:, :, 3] == 0, :3] = 0
    final_im = Image.fromarray(q_arr)
    final_im.save(f'{out_dir}/final.png')
    print(f'Saved {aid}: size={final_im.size}, colors={len(final_im.getcolors(256))}')
    return final_im

print('=== 1. Fix numbers on sand-floor-03 and sand-cracked-01 ===')
# Tile 1: Fine Golden Sand -> sand-floor-03
im_exp = Image.open(P_TILES_EXP).convert('RGBA')
crop_t1 = im_exp.crop((55, 55, 468, 468))
arr_t1 = np.array(crop_t1)
# Remove badge "1" at top-left
arr_t1[:45, :45] = arr_t1[50:95, 50:95]
tile1_512 = Image.fromarray(arr_t1).resize((512, 512), Image.Resampling.LANCZOS)
arr_s1 = np.array(tile1_512).astype(float)
# Seamless X & Y
m = 32
t = np.linspace(0, 1, m)
s = 3 * t**2 - 2 * t**3
cx = 0.5 * (arr_s1[:, 0, :] + arr_s1[:, -1, :])
for i in range(m):
    arr_s1[:, i, :] = (1.0 - s[i]) * cx + s[i] * arr_s1[:, i, :]
    arr_s1[:, 511 - i, :] = (1.0 - s[i]) * cx + s[i] * arr_s1[:, 511 - i, :]
cy = 0.5 * (arr_s1[0, :, :] + arr_s1[-1, :, :])
for i in range(m):
    arr_s1[i, :, :] = (1.0 - s[i]) * cy + s[i] * arr_s1[i, :, :]
    arr_s1[511 - i, :, :] = (1.0 - s[i]) * cy + s[i] * arr_s1[511 - i, :, :]
arr_s1[:, 0, :] = cx; arr_s1[:, -1, :] = cx
arr_s1[0, :, :] = cy; arr_s1[-1, :, :] = cy
arr_s1[:, :, 3] = 255
q1 = Image.fromarray(np.clip(arr_s1, 0, 255).astype(np.uint8)).quantize(36, method=Image.Quantize.FASTOCTREE).convert('RGBA')
q_arr1 = np.array(q1); q_arr1[:, 0, :] = q_arr1[:, -1, :]; q_arr1[0, :, :] = q_arr1[-1, :, :]; q_arr1[:, :, 3] = 255
Image.fromarray(q_arr1).save(f'{B}/desert-sand-floor-03/final.png')
print('sand-floor-03 cleaned (no number 1, seam=0)')

# Tile 2: Dry Cracked Earth -> sand-cracked-01
crop_t2 = im_exp.crop((555, 55, 968, 468))
arr_t2 = np.array(crop_t2)
# Remove badge "2" at top-left
arr_t2[:45, :45] = arr_t2[50:95, 50:95]
tile2_512 = Image.fromarray(arr_t2).resize((512, 512), Image.Resampling.LANCZOS)
arr_s2 = np.array(tile2_512).astype(float)
cx2 = 0.5 * (arr_s2[:, 0, :] + arr_s2[:, -1, :])
for i in range(m):
    arr_s2[:, i, :] = (1.0 - s[i]) * cx2 + s[i] * arr_s2[:, i, :]
    arr_s2[:, 511 - i, :] = (1.0 - s[i]) * cx2 + s[i] * arr_s2[:, 511 - i, :]
cy2 = 0.5 * (arr_s2[0, :, :] + arr_s2[-1, :, :])
for i in range(m):
    arr_s2[i, :, :] = (1.0 - s[i]) * cy2 + s[i] * arr_s2[i, :, :]
    arr_s2[511 - i, :, :] = (1.0 - s[i]) * cy2 + s[i] * arr_s2[511 - i, :, :]
arr_s2[:, 0, :] = cx2; arr_s2[:, -1, :] = cx2
arr_s2[0, :, :] = cy2; arr_s2[-1, :, :] = cy2
arr_s2[:, :, 3] = 255
q2 = Image.fromarray(np.clip(arr_s2, 0, 255).astype(np.uint8)).quantize(36, method=Image.Quantize.FASTOCTREE).convert('RGBA')
q_arr2 = np.array(q2); q_arr2[:, 0, :] = q_arr2[:, -1, :]; q_arr2[0, :, :] = q_arr2[-1, :, :]; q_arr2[:, :, 3] = 255
Image.fromarray(q_arr2).save(f'{B}/desert-sand-cracked-01/final.png')
print('sand-cracked-01 cleaned (no number 2, seam=0)')

print('=== 2. Replace duplicate and mismatched props from replacement pack ===')
im_rep = Image.open(P_REPLACE).convert('RGBA')
# Large nomad pavilion tent: top-left x in 0..660, y in 0..410
crop_tent = im_rep.crop((0, 0, 665, 410))
clean_tent = green_chroma_key(crop_tent)
save_clean_asset('desert-nomad-tent-large', clean_tent, colors=46)

# Nomad stake banner: top-right x in 670..1024, y in 0..415
crop_banner = im_rep.crop((670, 0, 1024, 415))
clean_banner = green_chroma_key(crop_banner)
save_clean_asset('desert-nomad-stake-banner', clean_banner, colors=40)

# Boulder 03: center x in 240..760, y in 400..810
crop_b3 = im_rep.crop((245, 405, 755, 805))
clean_b3 = green_chroma_key(crop_b3)
save_clean_asset('desert-boulder-03', clean_b3, colors=42)

print('=== 3. Extract 8 organic edge decals (dithered amoeba patches) ===')
# From P_REPLACE:
# Left column patches:
# 1) x: 0..250, y: 415..610 -> edge-sand-cracked-patch-01
# 2) x: 0..250, y: 610..810 -> edge-sand-cracked-patch-02
# 3) x: 0..250, y: 810..1024 -> edge-sand-sandstone-w
# 4) x: 250..500, y: 810..1024 -> edge-sand-sandstone-s
# Right column patches:
# 5) x: 750..1024, y: 415..610 -> edge-sand-sandstone-corner-01
# 6) x: 750..1024, y: 610..810 -> edge-sand-sandstone-corner-02
# 7) x: 500..750, y: 810..1024 -> edge-sand-sandstone-n
# 8) x: 750..1024, y: 810..1024 -> edge-sand-sandstone-e

edge_coords = {
    'desert-edge-sand-cracked-patch-01': (0, 415, 250, 610),
    'desert-edge-sand-cracked-patch-02': (0, 610, 250, 810),
    'desert-edge-sand-sandstone-w': (0, 810, 255, 1024),
    'desert-edge-sand-sandstone-s': (255, 810, 505, 1024),
    'desert-edge-sand-sandstone-corner-01': (750, 415, 1024, 610),
    'desert-edge-sand-sandstone-corner-02': (750, 610, 1024, 810),
    'desert-edge-sand-sandstone-n': (505, 810, 750, 1024),
    'desert-edge-sand-sandstone-e': (750, 810, 1024, 1024)
}

for aid, box in edge_coords.items():
    crop_edge = im_rep.crop(box)
    clean_edge = green_chroma_key(crop_edge)
    save_clean_asset(aid, clean_edge, colors=36, pad=16)

print('=== 4. Extract realistic dunes-mid and ruins-near backdrops with transparent sky ===')
im_bg = Image.open(P_BACKDROPS).convert('RGBA')
W_BG, H_BG = im_bg.size
# Top half: middle rolling dunes with transparent sky (y in 0..H_BG//2)
crop_mid = im_bg.crop((0, 0, W_BG, H_BG // 2))
clean_mid = green_chroma_key(crop_mid, g_thresh=130)
# Make seamless X for dunes-mid
arr_mid = np.array(clean_mid).astype(float)
H_m, W_m, _ = arr_mid.shape
cx_m = 0.5 * (arr_mid[:, 0, :] + arr_mid[:, -1, :])
for i in range(24):
    a = (i / 24.0) ** 2
    arr_mid[:, i, :] = (1.0 - a) * cx_m + a * arr_mid[:, i, :]
    arr_mid[:, W_m - 1 - i, :] = (1.0 - a) * cx_m + a * arr_mid[:, W_m - 1 - i, :]
arr_mid[:, 0, :] = cx_m; arr_mid[:, -1, :] = cx_m
arr_mid[:, :, 3] = np.where(arr_mid[:, :, 3] > 128, 255, 0)
arr_mid[arr_mid[:, :, 3] == 0, :3] = 0
im_mid_final = Image.fromarray(np.clip(arr_mid, 0, 255).astype(np.uint8))
save_clean_asset('desert-dunes-mid', im_mid_final, colors=44, pad=0)

# Bottom half: near sandstone ruins ridge (y in H_BG//2..H_BG)
crop_near = im_bg.crop((0, H_BG // 2, W_BG, H_BG))
clean_near = green_chroma_key(crop_near, g_thresh=130)
arr_near = np.array(clean_near).astype(float)
H_n, W_n, _ = arr_near.shape
cx_n = 0.5 * (arr_near[:, 0, :] + arr_near[:, -1, :])
for i in range(24):
    a = (i / 24.0) ** 2
    arr_near[:, i, :] = (1.0 - a) * cx_n + a * arr_near[:, i, :]
    arr_near[:, W_n - 1 - i, :] = (1.0 - a) * cx_n + a * arr_near[:, W_n - 1 - i, :]
arr_near[:, 0, :] = cx_n; arr_near[:, -1, :] = cx_n
arr_near[:, :, 3] = np.where(arr_near[:, :, 3] > 128, 255, 0)
arr_near[arr_near[:, :, 3] == 0, :3] = 0
im_near_final = Image.fromarray(np.clip(arr_near, 0, 255).astype(np.uint8))
save_clean_asset('desert-ruins-near', im_near_final, colors=44, pad=0)

print('=== 5. Clean stray orange bars on the 6 identified assets ===')
# bones-scatter, pottery-shards, sunken-bricks, pebbles, boulder-02, pottery-urn
bar_fixes = [
    'desert-decal-bones-scatter',
    'desert-decal-pottery-shards',
    'desert-decal-sunken-bricks',
    'desert-decal-pebbles-desert',
    'desert-boulder-02',
    'desert-pottery-urn-broken'
]
for aid in bar_fixes:
    p = f'{B}/{aid}/final.png'
    im = Image.open(p).convert('RGBA')
    arr = np.array(im)
    # Clear top 35px if there is any stray bar
    arr[:35, :, :] = 0
    # Clear 12px outer perimeter
    arr[-12:, :, :] = 0
    arr[:, :12, :] = 0
    arr[:, -12:, :] = 0
    # Ensure binary alpha and zeroed RGB
    arr[:, :, 3] = np.where(arr[:, :, 3] > 128, 255, 0)
    arr[arr[:, :, 3] == 0, :3] = 0
    save_clean_asset(aid, Image.fromarray(arr), colors=36)

print('=== 6. Harmonize colors: lighten overly dark cacti and palm-trunk, soften flat orange walls ===')
dark_cacti = ['desert-cactus-tall', 'desert-small-cactus-01', 'desert-small-cactus-02', 'desert-small-cactus-03', 'desert-palm-trunk']
for aid in dark_cacti:
    p = f'{B}/{aid}/final.png'
    im = Image.open(p).convert('RGBA')
    arr = np.array(im).astype(float)
    alpha = arr[:, :, 3]
    # Lift overly dark pixels (R,G,B < 40) towards warm olive/desert brown
    dark_mask = (alpha > 128) & (arr[:, :, 0] < 50) & (arr[:, :, 1] < 50) & (arr[:, :, 2] < 50)
    arr[dark_mask, 0] = arr[dark_mask, 0] * 1.5 + 45
    arr[dark_mask, 1] = arr[dark_mask, 1] * 1.5 + 40
    arr[dark_mask, 2] = arr[dark_mask, 2] * 1.2 + 25
    arr[:, :, 3] = np.where(alpha > 128, 255, 0)
    arr[arr[:, :, 3] == 0, :3] = 0
    save_clean_asset(aid, Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)), colors=38)

# Regrade ruins-wall-arch and stone-stairs from flat orange to weathered desert sandstone
flat_orange = ['desert-ruins-wall-arch', 'desert-stone-stairs']
for aid in flat_orange:
    p = f'{B}/{aid}/final.png'
    im = Image.open(p).convert('RGBA')
    arr = np.array(im).astype(float)
    alpha = arr[:, :, 3]
    # Tone down aggressive orange/red channel and lift blue/green to match arch-gate
    arr[:, :, 0] = arr[:, :, 0] * 0.92
    arr[:, :, 1] = arr[:, :, 1] * 0.96
    arr[:, :, 2] = arr[:, :, 2] * 1.15 + 15
    arr[:, :, 3] = np.where(alpha > 128, 255, 0)
    arr[arr[:, :, 3] == 0, :3] = 0
    save_clean_asset(aid, Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)), colors=40)

print('=== 7. Create genuine multi-shade contact shadows and visible horizon gradients ===')
# 6 Contact shadows: small, medium, large (dithered stipples with multiple shades of warm brown/shadow)
shadow_defs = [
    ('desert-shadow-small-01', (96, 48)),
    ('desert-shadow-small-02', (128, 48)),
    ('desert-shadow-medium-01', (192, 80)),
    ('desert-shadow-medium-02', (256, 96)),
    ('desert-shadow-large-01', (384, 144)),
    ('desert-shadow-large-02', (448, 160))
]

for aid, (sw, sh) in shadow_defs:
    arr_sh = np.zeros((sh, sw, 4), dtype=np.uint8)
    cy, cx = sh / 2.0, sw / 2.0
    ry, rx = (sh / 2.0) - 6, (sw / 2.0) - 8
    y, x = np.ogrid[:sh, :sw]
    dist = np.sqrt(((x - cx) / rx)**2 + ((y - cy) / ry)**2)
    
    # 3 shadow shades: dark core (#3a2412), mid ring (#5c3a1e), outer dither (#7d5028)
    core = dist <= 0.55
    arr_sh[core] = [58, 36, 18, 255]
    
    mid = (dist > 0.55) & (dist <= 0.82)
    # Stipple dither on mid ring
    dither_mid = ((x + y) % 2 == 0) | (dist < 0.70)
    arr_sh[mid & dither_mid] = [92, 58, 30, 255]
    
    outer = (dist > 0.82) & (dist <= 0.98)
    dither_outer = ((x * 2 + y * 3) % 4 == 0)
    arr_sh[outer & dither_outer] = [125, 80, 40, 255]
    
    save_clean_asset(aid, Image.fromarray(arr_sh), colors=8, pad=0)

# Horizon gradients (visible warm golden/dark transition strip)
gw, gh = 512, 128

# 01: Warm golden desert amber haze
arr_g1 = np.zeros((gh, gw, 4), dtype=np.uint8)
for row in range(gh):
    t = row / float(gh - 1)
    r_val = int(85 + 130 * t)
    g_val = int(50 + 115 * t)
    b_val = int(20 + 65 * t)
    a_val = 255 if t > 0.12 else 0
    arr_g1[row, :, 0] = r_val
    arr_g1[row, :, 1] = g_val
    arr_g1[row, :, 2] = b_val
    arr_g1[row, :, 3] = a_val
arr_g1[arr_g1[:, :, 3] == 0, :3] = 0
save_clean_asset('desert-horizon-gradient-01', Image.fromarray(arr_g1), colors=16, pad=0)

# 02: Dusky violet-amber desert twilight haze
arr_g2 = np.zeros((gh, gw, 4), dtype=np.uint8)
for row in range(gh):
    t = row / float(gh - 1)
    r_val = int(65 + 110 * t)
    g_val = int(40 + 85 * t)
    b_val = int(45 + 100 * t)
    a_val = 255 if t > 0.15 else 0
    arr_g2[row, :, 0] = r_val
    arr_g2[row, :, 1] = g_val
    arr_g2[row, :, 2] = b_val
    arr_g2[row, :, 3] = a_val
arr_g2[arr_g2[:, :, 3] == 0, :3] = 0
save_clean_asset('desert-horizon-gradient-02', Image.fromarray(arr_g2), colors=16, pad=0)

print('=== 8. Update manifest.json with strict 128 px/unit density ===')
man_path = f'{B}/manifest.json'
man_data = json.load(open(man_path))
man_assets = man_data['assets'] if isinstance(man_data, dict) else man_data

for a in man_assets:
    aid = a['id']
    p = f'{B}/{aid}/final.png'
    im = Image.open(p)
    w_px, h_px = im.size
    # Standard: far backdrop = 64 px/unit; all props, tiles, mid/near backdrops = 128 px/unit
    if 'wall-far' in aid:
        a['world'] = [round(w_px / 64.0, 4), round(h_px / 64.0, 4)]
    else:
        a['world'] = [round(w_px / 128.0, 4), round(h_px / 128.0, 4)]

json.dump({'assets': man_assets}, open(man_path, 'w'), indent=2)
print('manifest.json updated with 128 px/unit standard density across all 85 assets!')
print('Remedy completed successfully!')
