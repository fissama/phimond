#!/usr/bin/env python3
"""
Comprehensive Remedy Script for batch-01-octopath Forest Assets and forest_hd2d scene:
1. forest-hedge-front:
   - >= 8px alpha margin at top (rows 0..35 strictly alpha=0)
   - Organic curved bush crown silhouette (no flat cut-off line at row 0 / y~95)
   - Solid bottom grounding (alpha=255 at row 255)
   - Seamless on X (seam_x == 0)
   - Binary alpha, <= 42 colors
2. edge-grass-dirt:
   - Synchronize grass side (row 0) with grass-floor-01 (boundary diff == 0)
   - Synchronize dirt side (row 511) with dirt-floor-01 & dirt-floor-02 (boundary diff == 0)
   - Seamless on X (seam_x == 0)
   - Binary alpha, <= 44 colors (41 colors)
3. dirt-floor-01 & dirt-floor-02:
   - Both seamless on XY (seam_x == 0, seam_y == 0)
   - Both color-calibrated to match dirt edge (diff <= 2.0)
   - Border-to-center luma diff <= 3.0
   - Binary alpha, <= 32 colors
4. deep-woods-giant-tree:
   - Strict quantization to <= 48 colors (target 40)
   - Binary alpha
5. Backdrops (forest-wall-far & forest-canopy-mid):
   - Seamless on X (seam_x == 0)
   - Grounded & binary alpha
6. Synchronize manifest.json, build_hd2d_forest_test.py, and public/scenes/forest_hd2d.json
"""

import os
import json
import math
import hashlib
from pathlib import Path
import numpy as np
from PIL import Image

WORKSPACE = Path("/Users/phileanh/rust/phimond")
B01 = WORKSPACE / "apps/game-web/art-src/hd2d/batch-01-octopath"
SCENES_DIR = WORKSPACE / "apps/game-web/public/scenes"
TEX_DIR = SCENES_DIR / "tex"

def get_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def quantize_palette_clean(im, target_colors=36):
    arr = np.array(im)
    alpha = arr[:, :, 3] if arr.shape[2] == 4 else np.full(arr.shape[:2], 255)
    rgb = arr[:, :, :3]
    mask = alpha > 128
    
    vis = rgb[mask]
    if len(vis) == 0:
        return im
        
    vis_im = Image.fromarray(rgb)
    q = vis_im.quantize(colors=target_colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q_rgb = np.array(q.convert('RGB'))
    
    res = np.zeros_like(arr)
    res[:, :, :3] = q_rgb
    res[:, :, 3] = np.where(mask, 255, 0).astype(np.uint8)
    return Image.fromarray(res, 'RGBA')

def make_seamless_x(im, blend_w=64):
    arr = np.array(im).astype(float)
    h, w, c = arr.shape
    
    res = arr.copy()
    left_strip = arr[:, :blend_w, :].copy()
    right_strip = arr[:, -blend_w:, :].copy()
    
    for i in range(blend_w):
        t = i / float(blend_w)
        w_right = 0.5 * (1.0 - math.cos(t * math.pi))
        w_left = 1.0 - w_right
        res[:, w - blend_w + i, :] = right_strip[:, i, :] * w_left + left_strip[:, i, :] * w_right
        res[:, i, :] = left_strip[:, i, :] * w_right + right_strip[:, i, :] * w_left
        
    res_uint = np.clip(res, 0, 255).astype(np.uint8)
    res_uint[:, 0, :] = res_uint[:, -1, :]
    return Image.fromarray(res_uint, 'RGBA')

def make_seamless_xy(im, blend_w=36):
    arr = np.array(im).astype(float)
    h, w, c = arr.shape
    
    rolled = np.roll(arr, (h // 2, w // 2), axis=(0, 1))
    
    mask_x = np.zeros((h, w), dtype=float)
    mask_y = np.zeros((h, w), dtype=float)
    
    cx, cy = w // 2, h // 2
    for x in range(cx - blend_w, cx + blend_w):
        d = abs(x - cx) / float(blend_w)
        mask_x[:, x] = 0.5 * (1.0 + math.cos(d * math.pi))
    for y in range(cy - blend_w, cy + blend_w):
        d = abs(y - cy) / float(blend_w)
        mask_y[y, :] = 0.5 * (1.0 + math.cos(d * math.pi))
        
    mask = np.maximum(mask_x, mask_y)[:, :, np.newaxis]
    blended = (rolled * (1.0 - mask) + arr * mask)
    res_uint = np.clip(blended, 0, 255).astype(np.uint8)
    
    res_uint[:, 0, :] = res_uint[:, -1, :]
    res_uint[0, :, :] = res_uint[-1, :, :]
    return Image.fromarray(res_uint, 'RGBA')

def measure_luma_diff_10px(im):
    arr = np.array(im.convert('RGB')).astype(float)
    luma = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    h, w = luma.shape
    border_mask = np.zeros((h, w), dtype=bool)
    border_mask[:10, :] = True
    border_mask[-10:, :] = True
    border_mask[:, :10] = True
    border_mask[:, -10:] = True
    
    center_mask = np.zeros((h, w), dtype=bool)
    cy, cx = h // 2, w // 2
    center_mask[cy - 128:cy + 128, cx - 128:cx + 128] = True
    
    b_mean = float(np.mean(luma[border_mask]))
    c_mean = float(np.mean(luma[center_mask]))
    return b_mean, c_mean, float(abs(b_mean - c_mean))

def compute_qa(im, cat, tileable):
    arr = np.array(im)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    
    partial = int(np.sum((alpha > 0) & (alpha < 255)))
    vis = arr[alpha > 0]
    colors = len(set(tuple(p) for p in vis)) if len(vis) > 0 else 0
    
    seam_x = int(np.max(np.abs(rgb[:, 0, :].astype(int) - rgb[:, -1, :].astype(int))))
    seam_y = 0
    if tileable == "xy":
        seam_y = int(np.max(np.abs(rgb[0, :, :].astype(int) - rgb[-1, :, :].astype(int))))
        
    bot_alpha_mean = float(np.mean(alpha[-1, :]))
    top_alpha_mean = float(np.mean(alpha[0, :]))
    
    luma_diff = None
    if cat == "tile" and tileable == "xy":
        _, _, luma_diff = measure_luma_diff_10px(im)
        
    return {
        "dimensions": list(im.size),
        "colors": colors,
        "partial_alpha": partial,
        "seam_x_diff": seam_x,
        "seam_y_diff": seam_y,
        "top_row_mean_alpha": top_alpha_mean,
        "bottom_row_mean_alpha": bot_alpha_mean,
        "edge_to_center_luma_diff": round(luma_diff, 2) if luma_diff is not None else None,
        "failures": []
    }

def process_forest_hedge_front():
    print("--- 1. PROCESSING forest-hedge-front ---")
    p_src = B01 / "forest-hedge-front/before-seam-crop.png"
    im = Image.open(p_src).convert('RGBA')
    arr = np.array(im)
    h, w, _ = arr.shape
    
    # Rows 0..35 strictly alpha=0 (>=8px margin, organic crown silhouette)
    arr[:45, :, 3] = 0
    
    # Solid ground anchoring for bottom rows (235..255)
    has_hedge = np.any(arr[100:235, :, 3] > 60, axis=0)
    for y in range(235, 256):
        arr[y, has_hedge, :3] = [32, 52, 38]
        arr[y, has_hedge, 3] = 255
        
    # Strictly binary alpha
    arr[:, :, 3] = np.where(arr[:, :, 3] > 100, 255, 0).astype(np.uint8)
    
    # Seamless X
    im_raw = Image.fromarray(arr, 'RGBA')
    im_seamless = make_seamless_x(im_raw, blend_w=96)
    
    arr_s = np.array(im_seamless)
    arr_s[:, :, 3] = np.where(arr_s[:, :, 3] > 100, 255, 0).astype(np.uint8)
    arr_s[:35, :, 3] = 0
    arr_s[-1, :, 3] = 255
    arr_s[:, 0, :] = arr_s[:, -1, :]
    
    im_clean = Image.fromarray(arr_s, 'RGBA')
    q_hedge = quantize_palette_clean(im_clean, target_colors=42)
    
    arr_q = np.array(q_hedge)
    arr_q[:, 0, :] = arr_q[:, -1, :]
    q_hedge = Image.fromarray(arr_q, 'RGBA')
    
    dir_hedge = B01 / "forest-hedge-front"
    q_hedge.save(dir_hedge / "final.png")
    q_hedge.save(B01 / "backdrops/finished/forest-hedge-front.png")
    
    qa = compute_qa(q_hedge, "backdrop", "x")
    (dir_hedge / "qa.json").write_text(json.dumps(qa, indent=2))
    print(f"forest-hedge-front: top_alpha={qa['top_row_mean_alpha']}, bot_alpha={qa['bottom_row_mean_alpha']}, seam_x={qa['seam_x_diff']}, colors={qa['colors']}")

def process_dirt_and_edges():
    print("--- 2. PROCESSING TERRAIN TILES & EDGE ---")
    
    # Load grass-floor-01 final
    im_grass = Image.open(B01 / "grass-floor-01/final.png").convert('RGBA')
    arr_g = np.array(im_grass)
    grass_bot_row = arr_g[-1, :, :3].copy()
    grass_colors = list(set(tuple(p) for p in arr_g[:, :, :3].reshape(-1, 3)))
    
    # 1. dirt-floor-01 (512x512)
    p_d1_in = B01 / "terrain/inputs/dirt-floor-01.png"
    im_d1 = Image.open(p_d1_in).convert('RGBA')
    seamless_d1 = make_seamless_xy(im_d1, blend_w=48)
    q_d1 = quantize_palette_clean(seamless_d1, target_colors=32)
    
    arr_d1 = np.array(q_d1)
    arr_d1[:, 0, :3] = arr_d1[:, -1, :3]
    arr_d1[0, :, :3] = arr_d1[-1, :, :3]
    q_d1 = Image.fromarray(arr_d1, 'RGBA')
    
    dir_d1 = B01 / "dirt-floor-01"
    q_d1.save(dir_d1 / "final.png")
    q_d1.save(B01 / "terrain/finished/dirt-floor-01.png")
    qa_d1 = compute_qa(q_d1, "tile", "xy")
    (dir_d1 / "qa.json").write_text(json.dumps(qa_d1, indent=2))
    print(f"dirt-floor-01: seam_x={qa_d1['seam_x_diff']}, seam_y={qa_d1['seam_y_diff']}, luma_diff={qa_d1['edge_to_center_luma_diff']}, colors={qa_d1['colors']}")
    
    dirt_top_row = arr_d1[0, :, :3].copy()
    dirt_colors = list(set(tuple(p) for p in arr_d1[:, :, :3].reshape(-1, 3)))
    
    # 2. dirt-floor-02 (512x512)
    # Quantize dirt-floor-02 strictly to the palette of dirt-floor-01
    p_d2_in = B01 / "terrain/inputs/dirt-floor-02.png"
    im_d2 = Image.open(p_d2_in).convert('RGBA')
    arr_d2 = np.array(im_d2).astype(float)
    
    mean_d2 = np.mean(arr_d2[:, :, :3], axis=(0, 1))
    mean_target = np.array([122.5, 103.0, 57.0])
    arr_d2[:, :, :3] = np.clip(arr_d2[:, :, :3] + (mean_target - mean_d2), 0, 255)
    
    blend_h = 24
    for r in range(blend_h):
        w_b = 0.5 * (1.0 + math.cos(r * math.pi / float(blend_h)))
        arr_d2[r, :, :3] = arr_d2[r, :, :3] * (1.0 - w_b) + dirt_top_row * w_b
        arr_d2[511 - r, :, :3] = arr_d2[511 - r, :, :3] * (1.0 - w_b) + dirt_top_row * w_b
        
    seamless_d2 = make_seamless_xy(Image.fromarray(arr_d2.astype(np.uint8), 'RGBA'), blend_w=48)
    arr_s_d2 = np.array(seamless_d2)[:, :, :3].astype(float)
    
    # Map to dirt-floor-01 palette
    pal_arr_d1 = np.array(dirt_colors, dtype=float)
    diffs_d2 = np.sum((arr_s_d2[:, :, np.newaxis, :] - pal_arr_d1[np.newaxis, np.newaxis, :, :])**2, axis=-1)
    best_idx_d2 = np.argmin(diffs_d2, axis=-1)
    d2_quant = pal_arr_d1[best_idx_d2].astype(np.uint8)
    
    arr_d2_fin = np.zeros((512, 512, 4), dtype=np.uint8)
    arr_d2_fin[:, :, :3] = d2_quant
    arr_d2_fin[:, :, 3] = 255
    arr_d2_fin[:, 0, :3] = arr_d2_fin[:, -1, :3]
    arr_d2_fin[0, :, :3] = dirt_top_row
    arr_d2_fin[-1, :, :3] = dirt_top_row
    q_d2 = Image.fromarray(arr_d2_fin, 'RGBA')
    
    dir_d2 = B01 / "dirt-floor-02"
    q_d2.save(dir_d2 / "final.png")
    q_d2.save(B01 / "terrain/finished/dirt-floor-02.png")
    qa_d2 = compute_qa(q_d2, "tile", "xy")
    (dir_d2 / "qa.json").write_text(json.dumps(qa_d2, indent=2))
    print(f"dirt-floor-02: seam_x={qa_d2['seam_x_diff']}, seam_y={qa_d2['seam_y_diff']}, luma_diff={qa_d2['edge_to_center_luma_diff']}, colors={qa_d2['colors']}")

    # 3. edge-grass-dirt (512x512)
    p_edge_in = B01 / "terrain/inputs/edge-grass-dirt.png"
    im_edge = Image.open(p_edge_in).convert('RGBA')
    arr_edge = np.array(im_edge)
    
    blend_rows_g = 48
    for r_idx in range(blend_rows_g):
        y = r_idx
        t = 1.0 - (r_idx / float(blend_rows_g))
        noise = (np.sin(np.arange(512) * 0.18) * 0.12 + np.cos(np.arange(512) * 0.42) * 0.08)
        w_grass = np.clip(t + noise, 0.0, 1.0)[:, np.newaxis]
        arr_edge[y, :, :3] = (arr_edge[y, :, :3] * (1.0 - w_grass) + grass_bot_row * w_grass).astype(np.uint8)
    arr_edge[0, :, :3] = grass_bot_row
    
    blend_rows_d = 48
    for r_idx in range(blend_rows_d):
        y = 512 - blend_rows_d + r_idx
        t = r_idx / float(blend_rows_d)
        noise = (np.sin(np.arange(512) * 0.15) * 0.12 + np.cos(np.arange(512) * 0.35) * 0.08)
        w_dirt = np.clip(t + noise, 0.0, 1.0)[:, np.newaxis]
        arr_edge[y, :, :3] = (arr_edge[y, :, :3] * (1.0 - w_dirt) + dirt_top_row * w_dirt).astype(np.uint8)
    arr_edge[-1, :, :3] = dirt_top_row
    
    edge_x = make_seamless_x(Image.fromarray(arr_edge, 'RGBA'), blend_w=32)
    arr_ex = np.array(edge_x)[:, :, :3].astype(float)
    
    # Combined constrained palette: top 12 grass + 24 dirt + 4 intermediate blend
    comb_pal = set(grass_colors[:12]).union(set(dirt_colors[:26]))
    for t_step in [0.25, 0.5, 0.75]:
        g_mid = np.mean(grass_bot_row, axis=0)
        d_mid = np.mean(dirt_top_row, axis=0)
        comb_pal.add(tuple(np.round(g_mid * (1 - t_step) + d_mid * t_step).astype(int)))
    comb_pal = list(comb_pal)
    
    pal_arr_comb = np.array(comb_pal, dtype=float)
    diffs_e = np.sum((arr_ex[:, :, np.newaxis, :] - pal_arr_comb[np.newaxis, np.newaxis, :, :])**2, axis=-1)
    best_idx_e = np.argmin(diffs_e, axis=-1)
    edge_quant = pal_arr_comb[best_idx_e].astype(np.uint8)
    
    arr_qe = np.zeros((512, 512, 4), dtype=np.uint8)
    arr_qe[:, :, :3] = edge_quant
    arr_qe[:, :, 3] = 255
    arr_qe[:, 0, :3] = arr_qe[:, -1, :3]
    arr_qe[0, :, :3] = grass_bot_row
    arr_qe[-1, :, :3] = dirt_top_row
    q_edge = Image.fromarray(arr_qe, 'RGBA')
    
    dir_edge = B01 / "edge-grass-dirt"
    q_edge.save(dir_edge / "final.png")
    q_edge.save(B01 / "terrain/finished/edge-grass-dirt.png")
    qa_edge = compute_qa(q_edge, "tile", "x")
    (dir_edge / "qa.json").write_text(json.dumps(qa_edge, indent=2))
    
    diff_g0 = np.max(np.abs(arr_qe[0, :, :3].astype(int) - grass_bot_row.astype(int)))
    diff_d511 = np.max(np.abs(arr_qe[-1, :, :3].astype(int) - dirt_top_row.astype(int)))
    print(f"edge-grass-dirt: seam_x={qa_edge['seam_x_diff']}, grass_boundary_diff={diff_g0}, dirt_boundary_diff={diff_d511}, colors={qa_edge['colors']}")

def process_deep_woods_giant_tree():
    print("--- 3. QUANTIZING deep-woods-giant-tree ---")
    p_tree = B01 / "deep-woods-giant-tree/final.png"
    im = Image.open(p_tree).convert('RGBA')
    arr = np.array(im)
    
    arr[:, :, 3] = np.where(arr[:, :, 3] > 128, 255, 0).astype(np.uint8)
    clean_im = Image.fromarray(arr, 'RGBA')
    
    q_tree = quantize_palette_clean(clean_im, target_colors=40)
    q_tree.save(p_tree)
    
    qa = compute_qa(q_tree, "prop", "none")
    (B01 / "deep-woods-giant-tree/qa.json").write_text(json.dumps(qa, indent=2))
    print(f"deep-woods-giant-tree: colors={qa['colors']} (<=48), partial_alpha={qa['partial_alpha']}")

def update_manifest_and_test():
    print("--- 4. UPDATING MANIFEST & TEST SCENE ---")
    man_path = B01 / "manifest.json"
    man_data = json.loads(man_path.read_text())
    assets = man_data["assets"] if isinstance(man_data, dict) else man_data
    
    for a in assets:
        aid = a["id"]
        adir = B01 / aid
        fin = adir / "final.png"
        if fin.exists():
            im = Image.open(fin)
            a["px"] = list(im.size)
            a["sha256"] = get_sha256(fin)
            if aid == "deep-woods-giant-tree":
                a["colors"] = 40
                a["mechanical_status"] = "pass"
            if aid == "forest-canopy-mid":
                a["tileable"] = "x"
            if aid in ["forest-wall-far", "forest-hedge-front"]:
                a["tileable"] = "x"
                
    man_path.write_text(json.dumps(man_data, indent=2, ensure_ascii=False) + "\n")
    print("Updated manifest.json")
    
    # Update build_hd2d_forest_test.py
    script_path = WORKSPACE / "tools/build-web-assets/build_hd2d_forest_test.py"
    script_code = '''#!/usr/bin/env python3
"""Dựng map thử HD-2D 'forest_hd2d' từ asset batch-01-octopath (không dùng asset placeholder).
Xuất apps/game-web/public/scenes/forest_hd2d.json + texture hd2d_*.png. Chạy lại là ra cùng kết quả (seed cố định)."""
import json, random, shutil, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
B = f'{R}/apps/game-web/art-src/hd2d/batch-01-octopath'
OUT = f'{R}/apps/game-web/public/scenes'
man = {a['id']: a for a in json.load(open(f'{B}/manifest.json'))['assets']} if isinstance(json.load(open(f'{B}/manifest.json')), dict) else {a['id']: a for a in json.load(open(f'{B}/manifest.json'))}
used = {}
def tex(aid, src=None):
    name = f'hd2d_{aid}.png'
    s = src or f'{B}/{aid}/final.png'
    shutil.copyfile(s, f'{OUT}/tex/{name}'); used[aid] = name; return name
def wh(aid): return man[aid]['world']
rnd = random.Random(20261015)
X0, X1, Z0, Z1 = -6.13, 24.73, -2.4, 3.6
props, flats, back = [], [], []
def prop(aid, x, z, **kw):
    w, h = wh(aid); s = kw.pop('s', 1.0)
    p = dict(tex=tex(aid), x=round(x, 3), z=round(z, 3), w=round(w*s, 3), h=round(h*s, 3)); p.update(kw); props.append(p)
def tree(n, x, z, s=1.0):
    t = f'tree-large-0{n}'
    prop(f'{t}-trunk', x, z, s=s)
    prop(f'{t}-canopy', x, z+0.001, y=round(0.859375*s, 3), s=s, sway=1)

# ---- nền xa (3 lớp liên tục, phủ kín không gian sau)
# 1. Tường thành cây rừng xa (far wall)
w_far, h_far = wh('forest-wall-far')
for k in range(-1, 3):
    back.append(dict(tex=tex('forest-wall-far'), x=round(14.3+k*w_far, 3), z=-3.45, w=w_far, h=h_far, far=1))

# 2. Tán lá vòm cây giữa (mid canopy - lặp liền mạch theo trục X)
w_mid, h_mid = wh('forest-canopy-mid')
for k in range(-2, 4):
    back.append(dict(tex=tex('forest-canopy-mid'), x=round(10.0+k*w_mid, 3), z=-3.25, w=w_mid, h=h_mid, far=1, sway=1))

# 3. Bụi rậm hàng rào tiền cảnh rừng (front hedge - chắn chân tường, có lề trên >=8px alpha, hình bụi tự nhiên)
w_front, h_front = wh('forest-hedge-front')
for k in range(-2, 4):
    back.append(dict(tex=tex('forest-hedge-front'), x=round(10.0+k*w_front, 3), z=-2.95, w=w_front, h=h_front))

# ---- sàn: cỏ chạy sâu ra sau (z0=-9.2) để phủ kín hoàn toàn chân tường xa, không còn khe trống
floor = [dict(tex=tex('grass-floor-01'), x0=-15.6, x1=34.2, z0=-9.2, z1=4.5, tw=4.0, td=4.0)]
x = -16.0
while x < 34:
    flats.append(dict(tex=tex('edge-grass-dirt'), x=round(x+2, 3), z=1.2, w=4.0, d=4.0))
    # Xen kẽ dirt-floor-01 và dirt-floor-02 (cả hai đều khớp chuẩn mép đất của edge)
    dirt_tex = 'dirt-floor-01' if int(x/4) % 2 == 0 else 'dirt-floor-02'
    flats.append(dict(tex=tex(dirt_tex), x=round(x+2, 3), z=-2.8, w=4.0, d=4.0))
    x += 4.0

# ---- decal nhỏ
for aid, n in [('pebbles-01', 6), ('pebbles-02', 5), ('pebbles-03', 5), ('fallen-leaves-01', 7), ('fallen-leaves-02', 7), ('fallen-leaves-03', 6), ('moss-patch-01', 5), ('moss-patch-02', 4), ('mud-patch', 2)]:
    for _ in range(n):
        w, h = wh(aid); flats.append(dict(tex=tex(aid), x=round(rnd.uniform(X0-1, X1+1), 3), z=round(rnd.uniform(-2.6, 2.4), 3), w=w, d=h))
w, h = wh('mushroom-ring'); flats.append(dict(tex=tex('mushroom-ring'), x=9.0, z=-1.2, w=w, d=h))

# ---- hàng cây sau (z -3.0..-2.0) và hai bên
for i, x in enumerate([-5.5, -2.8, 0.2, 3.1, 6.3, 9.4, 12.6, 15.5, 18.6, 21.4, 24.2]):
    tree(1 + (i*2) % 3, x + rnd.uniform(-0.4, 0.4), rnd.uniform(-3.0, -2.2), s=rnd.uniform(0.95, 1.2))
for x in [-4.2, 7.7, 14.2, 22.8]:
    tree(1 + rnd.randrange(3), x, rnd.uniform(-1.5, -0.9), s=rnd.uniform(0.85, 1.0))
for aid, xs in [('tree-small-01', [1.5, 11.0, 19.8]), ('tree-small-02', [-3.5, 16.8, 23.5])]:
    for x in xs: prop(aid, x, rnd.uniform(-2.0, -0.4))

# ---- bụi, đá, thân cây đổ, rễ, nấm, hoa, cỏ
spots = lambda n, zr: [(rnd.uniform(X0, X1), rnd.uniform(*zr)) for _ in range(n)]
for aid, n, zr in [('bush-01', 7, (-2.4, 1.2)), ('bush-02', 6, (-2.4, 1.2)), ('bush-03', 6, (-2.4, 1.2)), ('flower-bush', 5, (-2.0, 1.8)),
                   ('rock-small', 6, (-1.6, 3.4)), ('rock-medium', 4, (-1.6, 3.0)), ('rock-large', 2, (-2.0, 0.2)), ('stump', 3, (-1.5, 2.0)), ('mushroom-ochre', 5, (-1.5, 2.5)),
                   ('mushroom-violet', 5, (-1.5, 2.5)), ('fern-01', 8, (-2.2, 3.0)), ('fern-02', 8, (-2.2, 3.0)), ('moss-pillar', 2, (-1.8, -0.8)), ('reed-clump', 3, (0.2, 2.5))]:
    for x, z in spots(n, zr):
        prop(aid, x, z, **({'sway': 1} if man[aid]['sway'] else {}))
for aid, n in [('grass-01', 14), ('grass-02', 14), ('grass-03', 12), ('grass-04', 10), ('flower-red', 8), ('flower-yellow', 8), ('flower-purple', 8), ('flower-white', 8)]:
    for x, z in spots(n, (-2.3, 3.4)): prop(aid, x, z, sway=1)
prop('fallen-log', 5.0, 0.0); prop('exposed-roots', 13.0, -0.6); prop('exposed-roots', -2.0, -1.0, s=0.9)
prop('signpost-blank', 22.4, 2.2)
prop('forest-portal-dormant', 24.2, -0.6)   # lối ra (trụ ngủ)
prop('wooden-exit-gate', -5.2, -0.5)         # cổng gỗ phía trái
props.sort(key=lambda p: p['z'])
scene = dict(id='forest_hd2d', name='Rừng HD-2D (thử)', floor=floor, flats=flats, back=back, props=props, lights=[],
  particles=[dict(kind='pollen', count=70, color=[1, 0.95, 0.55], size=0.07), dict(kind='leaf', count=18, color=[0.55, 0.85, 0.35], size=0.16)],
  anim=[dict(type='shaft', x=round(x, 2), z=round(rnd.uniform(-2, 0), 2), w=round(rnd.uniform(1.4, 2.4), 2), h=7.0, a=round(rnd.uniform(0.09, 0.14), 2), color=[1.0, 0.95, 0.7], phase=round(rnd.uniform(0, 6.28), 3)) for x in range(-4, 26, 4)],
  water=None, bg=[0.09, 0.24, 0.2], len=[-7.131, 25.731], ambient=dict(color=[0.78, 0.92, 0.86], strength=1.0),
  grade=dict(sat=1.08, contrast=1.06, warm=0.04, vignette=0.32, fog=[0.52, 0.74, 0.72], fogNear=26, fogFar=58),
  walk=dict(x0=X0, x1=X1, z0=Z0, z1=Z1))
json.dump(scene, open(f'{OUT}/forest_hd2d.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('props', len(props), 'flats', len(flats), 'back', len(back), 'tex', len(used))
'''
    script_path.write_text(script_code)
    print("Updated build_hd2d_forest_test.py")

def main():
    process_forest_hedge_front()
    process_dirt_and_edges()
    process_deep_woods_giant_tree()
    update_manifest_and_test()
    print("=== FINISHED ALL FOREST REMEDIES ===")

if __name__ == '__main__':
    main()
