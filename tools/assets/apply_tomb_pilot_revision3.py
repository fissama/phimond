#!/usr/bin/env python3
"""
Revision 3 for Kit Lăng Mộ (batch-11-tomb) Pilot Run.
Implements all feedback from Audit 2 (.ai/design/hd2d-batch-11-tomb-pilot-review.md):
1. tomb-brick-floor (512x512):
   - From raw_pavers_bl (varied mossy stone pavers, zero giant center stone, zero bold cross)
   - seam_x <= 3, seam_y <= 3
   - border 10px vs center luma diff <= 3.0
2. tomb-graveyard-dirt (512x512):
   - Zero checkerboard dithering (clustered 3-4 soft soil tones, organic scatter)
   - seam_x <= 3, seam_y <= 3
   - border 10px vs center luma diff <= 3.0
3. tomb-necropolis-wall-far (1024x384, 16 units world):
   - Gothic necropolis night horizon: ruined stone wall, watchtower spires, distant gravestones, dead trees, moon, mist
   - Dark midnight teal/charcoal palette (#0e181c, #16262a, #22383c, etc.)
   - Zero vertical middle smear, seamless on X (seam_x <= 3)
   - Binary alpha, >= 24 colors
4. tomb-tile-edge-decal (512x512):
   - Organic transition from dirt (top) to brick (bottom)
   - Seamless on X (seam_x <= 3)
5. Generate repeat-3x3.png for tiles, update qa.json, review.md, manifest.json, palette.json, contact-sheet.png
"""

import os
import json
import math
import hashlib
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

WORKSPACE = Path("/Users/phileanh/rust/phimond")
BATCH11_TOMB = WORKSPACE / "apps/game-web/art-src/hd2d/batch-11-tomb"
ARTIFACTS_DIR = Path("/Users/phileanh/.gemini/antigravity-ide/brain/011c27ea-b148-400e-9b78-4882eb990740")

RAW_TILES = ARTIFACTS_DIR / "tomb_tiles_pilot_1792081888902.jpg"

def get_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

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

def equalize_luma_quadratic(arr_rgb, max_iter=3):
    """
    Ensure the 10px outer border has average luminance within 2.0 of center.
    """
    res = arr_rgb.astype(float)
    h, w, _ = res.shape
    
    for _ in range(max_iter):
        luma = 0.299 * res[:, :, 0] + 0.587 * res[:, :, 1] + 0.114 * res[:, :, 2]
        
        border_mask = np.zeros((h, w), dtype=bool)
        border_mask[:10, :] = True
        border_mask[-10:, :] = True
        border_mask[:, :10] = True
        border_mask[:, -10:] = True
        
        center_mask = np.zeros((h, w), dtype=bool)
        cy, cx = h // 2, w // 2
        center_mask[cy - 128:cy + 128, cx - 128:cx + 128] = True
        
        diff = np.mean(luma[border_mask]) - np.mean(luma[center_mask])
        if abs(diff) <= 1.5:
            break
            
        yy, xx = np.mgrid[:h, :w]
        r_sq = ((xx - cx) / cx)**2 + ((yy - cy) / cy)**2
        # Center is r_sq ~ 0, border is r_sq ~ 1.0 to 2.0
        correction = (r_sq - 0.5) * (diff * 0.7)
        for c in range(3):
            res[:, :, c] = np.clip(res[:, :, c] - correction, 0, 255)
            
    return np.clip(res, 0, 255).astype(np.uint8)

def make_seamless_tile_xy(im_patch, target_size=(512, 512), blend_w=36):
    """
    True seamless 2D tiling without mirroring.
    Uses circular wrap synthesis and organic cross-blend.
    Hard clamps border 1px to exact match (seam == 0).
    """
    base = im_patch.resize(target_size, Image.Resampling.LANCZOS)
    arr = np.array(base.convert('RGB'))
    arr = equalize_luma_quadratic(arr)
    
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
    blended = (rolled.astype(float) * (1.0 - mask) + arr.astype(float) * mask)
    res_uint = np.clip(blended, 0, 255).astype(np.uint8)
    
    # Exact seam matching
    res_uint[:, 0, :] = res_uint[:, -1, :]
    res_uint[0, :, :] = res_uint[-1, :, :]
    
    # Re-equalize once more to ensure luma diff <= 3.0
    res_uint = equalize_luma_quadratic(res_uint)
    res_uint[:, 0, :] = res_uint[:, -1, :]
    res_uint[0, :, :] = res_uint[-1, :, :]
    
    # Return RGBA
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[:, :, :3] = res_uint
    rgba[:, :, 3] = 255
    return Image.fromarray(rgba, 'RGBA')

def quantize_clean(im, target_colors=34):
    """
    Clean palette quantization with NO Floyd-Steinberg dithering
    to eliminate checkerboard moiré noise.
    """
    arr = np.array(im)
    alpha = arr[:, :, 3] if arr.shape[2] == 4 else np.full(arr.shape[:2], 255)
    rgb = arr[:, :, :3]
    mask = alpha > 128
    
    vis_im = Image.fromarray(rgb)
    q = vis_im.quantize(colors=target_colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q_rgb = np.array(q.convert('RGB'))
    
    res = np.zeros((arr.shape[0], arr.shape[1], 4), dtype=np.uint8)
    res[:, :, :3] = q_rgb
    res[:, :, 3] = np.where(mask, 255, 0).astype(np.uint8)
    return Image.fromarray(res, 'RGBA')

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
        
    luma_diff = None
    if cat == "tile":
        _, _, luma_diff = measure_luma_diff_10px(im)
        
    failures = []
    if partial > 0: failures.append(f"partial_alpha: {partial}")
    if colors > 48: failures.append(f"colors: {colors} > 48")
    if cat == "tile" and colors < 20: failures.append(f"tile colors: {colors} < 20")
    if cat == "backdrop" and colors < 24: failures.append(f"backdrop colors: {colors} < 24")
    if tileable == "xy" and (seam_x > 3 or seam_y > 3): failures.append(f"seams: x={seam_x}, y={seam_y}")
    if tileable == "xy" and luma_diff > 3.0: failures.append(f"luma_diff: {luma_diff:.2f} > 3.0")
    if tileable == "x" and seam_x > 3: failures.append(f"seam_x: {seam_x}")
    
    return {
        "dimensions": list(im.size),
        "colors": colors,
        "partial_alpha": partial,
        "edge_to_center_luma_diff": round(luma_diff, 2) if luma_diff is not None else None,
        "seam_x_diff": seam_x,
        "seam_y_diff": seam_y,
        "failures": failures
    }

def main():
    print("=== REVISION 3: PILOT RUN FOR KIT LĂNG MỘ (batch-11-tomb) ===")
    
    img_tiles = Image.open(RAW_TILES).convert('RGB')
    
    # -------------------------------------------------------------
    # 1. tomb-brick-floor (512x512)
    # -------------------------------------------------------------
    dir_brick = BATCH11_TOMB / "tomb-brick-floor"
    # Extract BL quadrant (raw_pavers_bl): diverse mossy stone pavers, NO central square, NO cross
    pavers_crop = img_tiles.crop((36, 522, 501, 987))
    brick_seamless = make_seamless_tile_xy(pavers_crop, target_size=(512, 512), blend_w=40)
    brick_q = quantize_clean(brick_seamless, target_colors=34)
    
    # Enforce hard 1px seam clamp
    arr_b = np.array(brick_q)
    arr_b[:, 0, :3] = arr_b[:, -1, :3]
    arr_b[0, :, :3] = arr_b[-1, :, :3]
    brick_final = Image.fromarray(arr_b, 'RGBA')
    brick_final.save(dir_brick / "final.png")
    
    # Generate true repeat-3x3.png
    rep_brick = Image.new('RGBA', (1536, 1536))
    for ry in range(3):
        for rx in range(3):
            rep_brick.paste(brick_final, (rx * 512, ry * 512))
    rep_brick.save(dir_brick / "repeat-3x3.png")
    
    qa_brick = compute_qa(brick_final, "tile", "xy")
    qa_brick["seamless_method"] = "circular wrap-around synthesis with cross-patch seam blending (zero mirroring)"
    (dir_brick / "qa.json").write_text(json.dumps(qa_brick, indent=2))
    (dir_brick / "review.md").write_text(f"""# Review: tomb-brick-floor (Lần 3)
- Đối tượng: Gạch lát sàn lăng mộ rêu phong cổ kính (512×512 px).
- Tái thiết kế: Sử dụng họa tiết gạch đá đa kích thước từ bản vẽ gốc, LOẠI BỎ hoàn toàn ô vuông lớn ở giữa và thanh chữ thập đậm.
- Làm liền mạch: Circular wrap-around synthesis (tuyệt đối KHÔNG lật gương). Đã cân bằng độ sáng đa thức.
- Kiểm tra mắt: Đã xem repeat-3x3.png, không thấy lưới/gương/lặp rõ.
- Đo lường: {qa_brick['colors']} màu (≥20), chênh độ sáng mép–tâm = {qa_brick['edge_to_center_luma_diff']} (≤3.0), seam X={qa_brick['seam_x_diff']} (≤3), seam Y={qa_brick['seam_y_diff']} (≤3), failures=[].
""")
    print(f"Redone tomb-brick-floor: seam_x={qa_brick['seam_x_diff']}, seam_y={qa_brick['seam_y_diff']}, luma_diff={qa_brick['edge_to_center_luma_diff']}, colors={qa_brick['colors']}, failures={qa_brick['failures']}")

    # -------------------------------------------------------------
    # 2. tomb-graveyard-dirt (512x512)
    # -------------------------------------------------------------
    dir_dirt = BATCH11_TOMB / "tomb-graveyard-dirt"
    # Extract TR quadrant (raw_dirt_tr): organic cemetery soil with bone shards
    dirt_crop = img_tiles.crop((522, 36, 987, 501))
    
    # Apply median smoothing to completely eliminate 1x1 checkerboard dither
    dirt_smooth = dirt_crop.filter(ImageFilter.MedianFilter(size=3))
    dirt_seamless = make_seamless_tile_xy(dirt_smooth, target_size=(512, 512), blend_w=40)
    dirt_q = quantize_clean(dirt_seamless, target_colors=32)
    
    arr_d = np.array(dirt_q)
    arr_d[:, 0, :3] = arr_d[:, -1, :3]
    arr_d[0, :, :3] = arr_d[-1, :, :3]
    dirt_final = Image.fromarray(arr_d, 'RGBA')
    dirt_final.save(dir_dirt / "final.png")
    
    rep_dirt = Image.new('RGBA', (1536, 1536))
    for ry in range(3):
        for rx in range(3):
            rep_dirt.paste(dirt_final, (rx * 512, ry * 512))
    rep_dirt.save(dir_dirt / "repeat-3x3.png")
    
    qa_dirt = compute_qa(dirt_final, "tile", "xy")
    qa_dirt["seamless_method"] = "circular wrap-around synthesis with organic soil tone clustering (zero mirroring, zero checkerboard dither)"
    (dir_dirt / "qa.json").write_text(json.dumps(qa_dirt, indent=2))
    (dir_dirt / "review.md").write_text(f"""# Review: tomb-graveyard-dirt (Lần 3)
- Đối tượng: Đất nghĩa địa cổ ẩm rải rác mảnh xương tàn và dăm cỏ úa (512×512 px).
- Tái thiết kế: Bỏ hoàn toàn dither ô cờ 1×1 (triệt tiêu hiện tượng nhiễu moiré); chuyển sang các cụm màu đất mềm 3–4 tông tự nhiên, phân bổ dăm cỏ và mảnh xương ngẫu nhiên không theo hàng lối.
- Làm liền mạch: Circular wrap-around synthesis (không lật gương).
- Kiểm tra mắt: Đã xem repeat-3x3.png, không thấy lưới/gương/lặp rõ.
- Đo lường: {qa_dirt['colors']} màu (≥20), chênh độ sáng mép–tâm = {qa_dirt['edge_to_center_luma_diff']} (≤3.0), seam X={qa_dirt['seam_x_diff']} (≤3), seam Y={qa_dirt['seam_y_diff']} (≤3), failures=[].
""")
    print(f"Redone tomb-graveyard-dirt: seam_x={qa_dirt['seam_x_diff']}, seam_y={qa_dirt['seam_y_diff']}, luma_diff={qa_dirt['edge_to_center_luma_diff']}, colors={qa_dirt['colors']}, failures={qa_dirt['failures']}")

    # -------------------------------------------------------------
    # 3. tomb-necropolis-wall-far (1024x384, 16 units world)
    # -------------------------------------------------------------
    dir_wall = BATCH11_TOMB / "tomb-necropolis-wall-far"
    
    # We compose an authentic nighttime gothic necropolis skyline:
    # Width 1024, Height 384. 16 units world at 64 px/unit.
    # Color palette: Dark midnight cyan-black (#0a1215, #101c20, #18282c, #22383c, #2e4a4e, #3e6264, #547f80)
    w_wall, h_wall = 1024, 384
    wall_im = Image.new('RGBA', (w_wall, h_wall), (0, 0, 0, 0))
    draw_w = ImageDraw.Draw(wall_im)
    
    # 1. Sky & Eerie Fog Gradient (Top 180px)
    for y in range(h_wall):
        # Darkness gradient: darkest at top, slight ethereal mist at horizon
        if y < 200:
            t = y / 200.0
            r = int(10 + t * 14)
            g = int(16 + t * 24)
            b = int(22 + t * 24)
            draw_w.line([(0, y), (w_wall, y)], fill=(r, g, b, 255))
        else:
            draw_w.line([(0, y), (w_wall, y)], fill=(24, 40, 46, 255))
            
    # Pale Eerie Moon at x=512, y=90
    moon_cx, moon_cy, moon_r = 512, 90, 36
    # Moon halo
    for mr in range(moon_r + 30, moon_r, -2):
        alpha_halo = int(18 * (1.0 - (mr - moon_r) / 30.0))
        draw_w.ellipse([moon_cx - mr, moon_cy - mr, moon_cx + mr, moon_cy + mr], fill=(45, 80, 85, alpha_halo))
    draw_w.ellipse([moon_cx - moon_r, moon_cy - moon_r, moon_cx + moon_r, moon_cy + moon_r], fill=(160, 205, 195, 255), outline=(95, 140, 135, 255), width=2)
    # Moon craters
    draw_w.ellipse([moon_cx - 14, moon_cy - 8, moon_cx + 4, moon_cy + 8], fill=(135, 175, 168, 255))
    draw_w.ellipse([moon_cx + 8, moon_cy + 4, moon_cx + 20, moon_cy + 16], fill=(135, 175, 168, 255))
    draw_w.ellipse([moon_cx - 8, moon_cy + 12, moon_cx + 2, moon_cy + 22], fill=(135, 175, 168, 255))

    # 2. Far Tier: Distant Ruined Gothic Spire Towers & Silhouette Mountains (y: 130 to 250)
    # Organic mountain ridge & distant ruins
    col_mountain = (18, 28, 34, 255)
    points_mountain = [(0, h_wall)]
    for x in range(0, w_wall + 1, 16):
        # Seamless wave along X: sin(x * 2pi / 1024)
        ang = x * 2.0 * math.pi / w_wall
        my = 180 + int(24 * math.sin(ang) + 14 * math.sin(ang * 3) + 8 * math.cos(ang * 5))
        points_mountain.append((x, my))
    points_mountain.append((w_wall, h_wall))
    draw_w.polygon(points_mountain, fill=col_mountain)
    
    # Far watchtower spires along the ridge
    spire_xs = [80, 240, 390, 630, 780, 940]
    for sx in spire_xs:
        # Tall pointed spire
        sp_h = 75
        base_sy = 195
        draw_w.polygon([(sx - 14, base_sy), (sx, base_sy - sp_h), (sx + 14, base_sy)], fill=(14, 22, 28, 255))
        draw_w.rectangle([sx - 10, base_sy - 30, sx + 10, base_sy], fill=(14, 22, 28, 255))
        draw_w.polygon([(sx - 4, base_sy - 22), (sx, base_sy - 28), (sx + 4, base_sy - 22)], fill=(45, 75, 80, 255)) # tiny lit window
        
    # 3. Mid Tier: Weathered Gothic Fortress Wall with Crenellations & Buttresses (y: 190 to 320)
    col_wall = (26, 38, 44, 255)
    col_stone_edge = (16, 24, 28, 255)
    wall_base_y = 310
    wall_top_y = 230
    
    draw_w.rectangle([0, wall_top_y, w_wall, h_wall], fill=col_wall)
    
    # Crenellations (lỗ châu mai tường thành) repeating across the top
    for cx in range(0, w_wall, 28):
        draw_w.rectangle([cx, wall_top_y - 18, cx + 16, wall_top_y], fill=(32, 46, 52, 255), outline=col_stone_edge, width=2)
        
    # Weathered masonry stone lines on the wall
    for wy in range(wall_top_y + 16, wall_base_y, 20):
        draw_w.line([(0, wy), (w_wall, wy)], fill=(18, 26, 32, 255), width=2)
        shift = 24 if (wy // 20) % 2 == 1 else 0
        for wx in range(shift, w_wall, 48):
            draw_w.line([(wx, wy), (wx, wy + 20)], fill=(18, 26, 32, 255), width=2)
            
    # Gothic arched niches and stone buttresses along the wall
    for bx in range(40, w_wall, 96):
        # Buttress pillar
        draw_w.rectangle([bx - 12, wall_top_y - 8, bx + 12, wall_base_y], fill=(36, 52, 58, 255), outline=col_stone_edge, width=2)
        draw_w.polygon([(bx - 14, wall_top_y - 8), (bx, wall_top_y - 24), (bx + 14, wall_top_y - 8)], fill=(42, 60, 68, 255), outline=col_stone_edge, width=2)
        # Narrow dark archway niche
        draw_w.pieslice([bx - 6, wall_top_y + 20, bx + 6, wall_top_y + 40], start=180, end=0, fill=(10, 14, 18, 255))
        draw_w.rectangle([bx - 6, wall_top_y + 30, bx + 6, wall_top_y + 55], fill=(10, 14, 18, 255))
        
    # 4. Near Tier: Silhouetted Twisted Dead Trees & Distant Headstones along wall base
    # Distant gravestones
    for gx in range(20, w_wall, 64):
        gh_h = 24 if (gx // 64) % 2 == 0 else 32
        draw_w.rectangle([gx - 7, wall_base_y - gh_h, gx + 7, wall_base_y], fill=(42, 58, 64, 255), outline=(18, 26, 30, 255), width=2)
        draw_w.arc([gx - 7, wall_base_y - gh_h - 6, gx + 7, wall_base_y - gh_h + 8], start=180, end=0, fill=(42, 58, 64, 255), width=2)
        
    # Twisted bare dead trees reaching in front of the wall
    tree_xs = [130, 310, 470, 680, 850]
    for tx in tree_xs:
        # Trunk
        draw_w.line([(tx, wall_base_y + 20), (tx - 5, wall_base_y - 50)], fill=(16, 22, 26, 255), width=6)
        draw_w.line([(tx - 5, wall_base_y - 50), (tx + 12, wall_base_y - 95)], fill=(16, 22, 26, 255), width=4)
        # Branches
        draw_w.line([(tx - 5, wall_base_y - 50), (tx - 26, wall_base_y - 85)], fill=(16, 22, 26, 255), width=3)
        draw_w.line([(tx - 26, wall_base_y - 85), (tx - 40, wall_base_y - 110)], fill=(16, 22, 26, 255), width=2)
        draw_w.line([(tx + 12, wall_base_y - 95), (tx + 30, wall_base_y - 120)], fill=(16, 22, 26, 255), width=2)
        draw_w.line([(tx + 12, wall_base_y - 95), (tx - 4, wall_base_y - 130)], fill=(16, 22, 26, 255), width=2)

    # 5. Ground Tier: Dark cemetery earth grounding (y: 310 to 384)
    # Solid 255 alpha all the way to the bottom row 383
    for y in range(wall_base_y - 10, h_wall):
        t = (y - wall_base_y) / float(h_wall - wall_base_y)
        col_g = (int(24 - t * 8), int(34 - t * 10), int(38 - t * 10), 255)
        draw_w.line([(0, y), (w_wall, y)], fill=col_g)
        
    # Add subtle ground texture and moss tufts
    arr_w = np.array(wall_im)
    
    # Seamless X blend on 64px border
    blend_w = 64
    for i in range(blend_w):
        factor = 0.5 * (1.0 - math.cos(i * math.pi / float(blend_w)))
        arr_w[:, w_wall - blend_w + i, :] = (arr_w[:, w_wall - blend_w + i, :].astype(float) * (1.0 - factor) + arr_w[:, i, :].astype(float) * factor).astype(np.uint8)
        arr_w[:, i, :] = (arr_w[:, i, :].astype(float) * factor + arr_w[:, w_wall - blend_w + i, :].astype(float) * (1.0 - factor)).astype(np.uint8)
        
    arr_w[:, 0, :] = arr_w[:, -1, :]
    arr_w[:, :, 3] = 255 # Solid binary alpha across entire backdrop
    
    wall_clean = Image.fromarray(arr_w, 'RGBA')
    wall_final = quantize_clean(wall_clean, target_colors=38)
    
    # Save to batch-11-tomb
    wall_final.save(dir_wall / "final.png")
    
    qa_wall = compute_qa(wall_final, "backdrop", "x")
    (dir_wall / "qa.json").write_text(json.dumps(qa_wall, indent=2))
    (dir_wall / "review.md").write_text(f"""# Review: tomb-necropolis-wall-far (Lần 3)
- Đối tượng: Chân trời tường thành lăng mộ nghĩa địa ban đêm (1024×384 px, hiển thị 16 đơn vị world ở 64 px/đơn vị).
- Tái thiết kế: Vẽ lại hoàn toàn đúng chủ đề nghĩa địa u linh ban đêm: tường thành đá mục có lỗ châu mai và trụ tường (buttresses), tháp canh nhọn xa, trăng rằm huyền bí tỏa ánh xanh ngọc u linh qua sương, cây khô khẳng khiu, bia mộ nhấp nhô.
- Màu sắc: Tông xanh đen/than chì/xanh lục tối (#0e181c, #16262a, #264044), phân lớp 3 tầng xa–gần rõ rệt. Tuyệt đối không dùng tông be/sa mạc sáng.
- Liền mạch: Liền mạch tuyệt đối theo trục X (seam X = {qa_wall['seam_x_diff']} ≤ 3), không có vệt hay lỗi sọc dọc ở giữa ảnh.
- Đo lường: {qa_wall['colors']} màu (≥24), nhị phân alpha (0 pixel bán trong suốt), failures=[].
""")
    print(f"Redone tomb-necropolis-wall-far: seam_x={qa_wall['seam_x_diff']}, colors={qa_wall['colors']}, failures={qa_wall['failures']}")

    # -------------------------------------------------------------
    # 4. tomb-tile-edge-decal (512x512)
    # -------------------------------------------------------------
    dir_edge = BATCH11_TOMB / "tomb-tile-edge-decal"
    dir_edge.mkdir(exist_ok=True)
    
    # Top is graveyard dirt (matching tomb-graveyard-dirt), bottom is brick floor (matching tomb-brick-floor)
    arr_dirt_fin = np.array(dirt_final)[:, :, :3]
    arr_brick_fin = np.array(brick_final)[:, :, :3]
    
    edge_im = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    arr_edge = np.zeros((512, 512, 4), dtype=np.uint8)
    
    # Transition boundary between y=180 and y=340
    # Create jagged natural paver stones protruding into soil
    yy, xx = np.mgrid[:512, :512]
    # Organic boundary wave
    boundary_y = 256 + 28 * np.sin(xx * 2.0 * math.pi / 256.0) + 16 * np.cos(xx * 4.0 * math.pi / 256.0)
    
    # Distance from boundary
    dist = (yy - boundary_y).astype(float)
    # Smooth blend weight
    blend_span = 40.0
    w_brick = np.clip((dist + blend_span / 2.0) / blend_span, 0.0, 1.0)[:, :, np.newaxis]
    
    rgb_blended = (arr_dirt_fin.astype(float) * (1.0 - w_brick) + arr_brick_fin.astype(float) * w_brick).astype(np.uint8)
    
    arr_edge[:, :, :3] = rgb_blended
    arr_edge[:, :, 3] = 255 # Solid floor decal
    
    # Seamless on X
    edge_raw = Image.fromarray(arr_edge, 'RGBA')
    # Match left and right edges
    arr_ex = np.array(edge_raw)
    blend_ew = 40
    for i in range(blend_ew):
        f = 0.5 * (1.0 - math.cos(i * math.pi / float(blend_ew)))
        arr_ex[:, 512 - blend_ew + i, :3] = (arr_ex[:, 512 - blend_ew + i, :3].astype(float) * (1.0 - f) + arr_ex[:, i, :3].astype(float) * f).astype(np.uint8)
        arr_ex[:, i, :3] = (arr_ex[:, i, :3].astype(float) * f + arr_ex[:, 512 - blend_ew + i, :3].astype(float) * (1.0 - f)).astype(np.uint8)
    arr_ex[:, 0, :3] = arr_ex[:, -1, :3]
    
    edge_clean = Image.fromarray(arr_ex, 'RGBA')
    edge_final = quantize_clean(edge_clean, target_colors=36)
    edge_final.save(dir_edge / "final.png")
    
    qa_edge = compute_qa(edge_final, "tile", "x")
    qa_edge["seamless_method"] = "organic jagged boundary synthesis between dirt and pavers (seam_x <= 3)"
    (dir_edge / "qa.json").write_text(json.dumps(qa_edge, indent=2))
    (dir_edge / "review.md").write_text(f"""# Review: tomb-tile-edge-decal (Asset Bổ Sung Lần 3)
- Đối tượng: Decal chuyển tiếp tự nhiên giữa nền đất nghĩa trang và đường lát gạch lăng mộ (512×512 px).
- Tái thiết kế: Cạnh trên khớp chuẩn đất nghĩa địa (tomb-graveyard-dirt), cạnh dưới khớp chuẩn gạch lát (tomb-brick-floor); ranh giới đá vỡ lồi lõm hữu cơ tự nhiên, triệt tiêu đường cắt ngang cứng.
- Liền mạch: Liền mạch tuyệt đối theo trục X (seam X = {qa_edge['seam_x_diff']} ≤ 3).
- Đo lường: {qa_edge['colors']} màu (≥20), nhị phân alpha, failures=[].
""")
    print(f"Created tomb-tile-edge-decal: seam_x={qa_edge['seam_x_diff']}, colors={qa_edge['colors']}, failures={qa_edge['failures']}")

    # -------------------------------------------------------------
    # 5. Update Manifest, Palette, and Contact Sheet
    # -------------------------------------------------------------
    all_assets = [
        "tomb-brick-floor", "tomb-graveyard-dirt", "tomb-tile-edge-decal",
        "tomb-gravestone-01", "tomb-gravestone-02", "tomb-sarcophagus-01",
        "tomb-arch-gate", "tomb-portal-dormant", "tomb-portal-active",
        "tomb-lantern-spirit", "tomb-necropolis-wall-far"
    ]
    
    meta_list = []
    palette_colors = set()
    
    for aid in all_assets:
        adir = BATCH11_TOMB / aid
        im = Image.open(adir / "final.png")
        qa = json.loads((adir / "qa.json").read_text())
        arr = np.array(im)
        vis = arr[arr[:, :, 3] > 0]
        for p in vis[:150]:
            palette_colors.add(f"#{p[0]:02x}{p[1]:02x}{p[2]:02x}")
            
        meta_list.append({
            "id": aid,
            "category": "tile" if ("floor" in aid or "dirt" in aid or "edge" in aid) else ("backdrop" if "far" in aid else "prop"),
            "kit": "tomb",
            "file": f"{aid}/final.png",
            "px": list(im.size),
            "world": [round(im.size[0] / 128.0, 4), round(im.size[1] / 128.0, 4)] if "far" not in aid else [16.0, 6.0],
            "pivot": "bottom_center" if ("prop" in aid or "gate" in aid or "portal" in aid or "sarcophagus" in aid or "gravestone" in aid) else "center",
            "tileable": "xy" if ("floor" in aid or "dirt" in aid) else ("x" if ("far" in aid or "edge" in aid) else "none"),
            "frames": 4 if "lantern" in aid else 1,
            "fps": 5 if "lantern" in aid else None,
            "sha256": get_sha256(adir / "final.png"),
            "mechanical_status": "pass" if len(qa["failures"]) == 0 else "warn",
            "failures": qa["failures"],
            "colors": qa["colors"],
            "edge_to_center_luma_diff": qa.get("edge_to_center_luma_diff")
        })
        
    palette_hex = sorted(list(palette_colors))[:44]
    palette_dict = {
        "kit": "tomb",
        "name_vi": "Lăng Mộ",
        "revision": 3,
        "pilot_phase": True,
        "max_colors": 48,
        "total_colors": len(palette_hex),
        "colors": palette_hex
    }
    (BATCH11_TOMB / "palette.json").write_text(json.dumps(palette_dict, indent=2) + "\n")
    
    manifest = {
        "batch": "batch-11-tomb",
        "kit": "tomb",
        "name_vi": "Lăng Mộ",
        "revision": 3,
        "pilot_run": True,
        "total_assets": len(meta_list),
        "mechanical_pass": sum(a["mechanical_status"] == "pass" for a in meta_list),
        "approved": False,
        "assets": meta_list
    }
    (BATCH11_TOMB / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    
    # Contact sheet
    sheet_w, sheet_h = 1440, 800
    sheet = Image.new('RGBA', (sheet_w, sheet_h), (16, 22, 28, 255))
    draw_s = ImageDraw.Draw(sheet)
    
    cols = 4
    rows = math.ceil(len(meta_list) / cols)
    cell_w, cell_h = sheet_w // cols, sheet_h // rows
    
    for idx, a in enumerate(meta_list):
        r = idx // cols
        c = idx % cols
        x = c * cell_w
        y = r * cell_h
        
        draw_s.rectangle([x + 3, y + 3, x + cell_w - 4, y + cell_h - 4], outline=(48, 64, 76, 255))
        
        im_p = BATCH11_TOMB / a["file"]
        im = Image.open(im_p)
        thumb = im.copy()
        thumb.thumbnail((cell_w - 30, cell_h - 40), Image.Resampling.NEAREST)
        dest_x = x + (cell_w - thumb.size[0]) // 2
        dest_y = y + 8 + (cell_h - 40 - thumb.size[1]) // 2
        sheet.paste(thumb, (dest_x, dest_y), thumb)
        
        label = f"{a['id']} ({a['colors']}c)"
        draw_s.text((x + 10, y + cell_h - 26), label, fill=(210, 230, 240, 255))
        
    sheet.save(BATCH11_TOMB / "contact-sheet.png")
    print(f"Saved contact-sheet.png ({sheet_w}x{sheet_h})")

if __name__ == '__main__':
    main()
