#!/usr/bin/env python3
"""Remediation script for Desert Batch-11 Round 4:
1. Restore desert-boulder-01 to authentic 356x276 asset from RAW_PROPS (colors <= 24, semi_alpha = 0).
2. Fix desert-monster-bones:
   - Eliminate lime green! Shift sand mound to authentic warm golden desert sand [#D9B26B, #E5C57E, #B88A44].
   - Enforce 100% binary alpha (alpha in {0, 255}) so SEMI_ALPHA = 0 for art_gate.py.
   - Use organic stippled sand dither on the perimeter for a soft visual transition.
3. Quantize desert-portal-dormant and desert-portal-active to <= 36 colors (satisfying COLORS <= 64 in art_gate.py).
4. Bo tròn cạnh (eliminate straight runs) for desert-small-rock-03, desert-tumbleweed-01, desert-tumbleweed-02, desert-boulder-03.
5. Soften and recolor desert-edge-sand-cracked-patch-01/02 to tapered sand ripples matching floor.
6. Regenerate contact-sheet.png and update manifest.json.
"""
import os, json, hashlib, shutil, pathlib
from PIL import Image, ImageDraw
import numpy as np

R = pathlib.Path(__file__).resolve().parents[2]
art_dir = R / "apps/game-web/art-src/hd2d/batch-11-desert"
tex_dir = R / "apps/game-web/public/scenes/tex"
raw_props_p = pathlib.Path("/Users/phileanh/.gemini/antigravity-ide/brain/011c27ea-b148-400e-9b78-4882eb990740/desert_props_pack_1792122396890.jpg")

def save_and_sync(aid, img):
    final_p = art_dir / aid / "final.png"
    img.save(final_p)
    tex_p = tex_dir / f"hd2d_{aid}.png"
    shutil.copy(final_p, tex_p)
    with open(final_p, "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    return h

def quantize_octopath(im, max_colors=36):
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    arr = np.array(im)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    mask = alpha > 128
    vis_pixels = rgb[mask]
    if len(vis_pixels) == 0:
        return im
    vis_im = Image.fromarray(rgb)
    q = vis_im.quantize(colors=max_colors, method=Image.Quantize.MEDIANCUT)
    q_rgb = np.array(q.convert('RGB'))
    res = np.zeros_like(arr)
    res[:, :, :3] = q_rgb
    res[:, :, 3] = np.where(mask, 255, 0).astype(np.uint8)
    return Image.fromarray(res)

# 1. Restore desert-boulder-01 from RAW_PROPS
def restore_boulder_01():
    aid = "desert-boulder-01"
    raw_im = Image.open(raw_props_p).convert("RGB")
    arr_rgb = np.array(raw_im)
    is_bg = (arr_rgb[:, :, 0] > 170) & (arr_rgb[:, :, 1] < 70) & (arr_rgb[:, :, 2] > 170)
    # Spec: [380, 40, 640, 380]
    y0, x0, y1, x1 = 380, 40, 640, 380
    sub_rgb = arr_rgb[y0:y1, x0:x1]
    sub_bg = is_bg[y0:y1, x0:x1]
    ys, xs = np.where(~sub_bg)
    min_y, max_y = ys.min(), ys.max() + 1
    min_x, max_x = xs.min(), xs.max() + 1
    crop_rgb = sub_rgb[min_y:max_y, min_x:max_x]
    crop_mask = ~sub_bg[min_y:max_y, min_x:max_x]
    pad = 12
    ch, cw, _ = crop_rgb.shape
    padded = np.zeros((ch + pad * 2, cw + pad * 2, 4), dtype=np.uint8)
    padded[pad:pad + ch, pad:pad + cw, :3] = crop_rgb
    padded[pad:pad + ch, pad:pad + cw, 3] = np.where(crop_mask, 255, 0).astype(np.uint8)
    im = quantize_octopath(Image.fromarray(padded), max_colors=24)
    # Check size matches [356, 276]
    assert im.size == (356, 276), f"Expected (356, 276), got {im.size}"
    return aid, im

# 2. Fix desert-monster-bones
def fix_monster_bones():
    aid = "desert-monster-bones"
    # Load original crop from RAW_PROPS so colors are pristine
    raw_im = Image.open(raw_props_p).convert("RGB")
    arr_rgb = np.array(raw_im)
    is_bg = (arr_rgb[:, :, 0] > 170) & (arr_rgb[:, :, 1] < 70) & (arr_rgb[:, :, 2] > 170)
    y0, x0, y1, x1 = 20, 10, 320, 440
    sub_rgb = arr_rgb[y0:y1, x0:x1]
    sub_bg = is_bg[y0:y1, x0:x1]
    ys, xs = np.where(~sub_bg)
    min_y, max_y = ys.min(), ys.max() + 1
    min_x, max_x = xs.min(), xs.max() + 1
    crop_rgb = sub_rgb[min_y:max_y, min_x:max_x].copy()
    crop_mask = ~sub_bg[min_y:max_y, min_x:max_x].copy()
    pad = 12
    ch, cw, _ = crop_rgb.shape
    arr = np.zeros((ch + pad * 2, cw + pad * 2, 4), dtype=np.uint8)
    arr[pad:pad + ch, pad:pad + cw, :3] = crop_rgb
    arr[pad:pad + ch, pad:pad + cw, 3] = np.where(crop_mask, 255, 0).astype(np.uint8)

    # In the raw prop, bones are ivory and the mound is reddish-orange sand.
    # Convert reddish-orange mound (y > 170) to warm golden desert sand [#D9B26B = (217, 178, 107)]
    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            if arr[y, x, 3] == 255 and y > 170:
                r, g, b = arr[y, x, :3]
                # If bone (ivory/white highlight): leave alone
                is_bone = (r > 200) and (g > 195) and (b > 165)
                if not is_bone:
                    # Map reddish/orange mound to warm golden desert sand
                    # Floor sand colors: [229, 197, 126] highlight, [217, 178, 107] mid, [184, 138, 68] shadow
                    luma = 0.299 * r + 0.587 * g + 0.114 * b
                    t = luma / 255.0
                    if t > 0.7:
                        # Golden highlight
                        arr[y, x, 0] = int(229 * t)
                        arr[y, x, 1] = int(197 * t)
                        arr[y, x, 2] = int(126 * t)
                    elif t > 0.4:
                        # Golden mid sand
                        arr[y, x, 0] = int(217 * (t / 0.7))
                        arr[y, x, 1] = int(178 * (t / 0.7))
                        arr[y, x, 2] = int(107 * (t / 0.7))
                    else:
                        # Warm sand shadow
                        arr[y, x, 0] = int(184 * (t / 0.4))
                        arr[y, x, 1] = int(138 * (t / 0.4))
                        arr[y, x, 2] = int(68 * (t / 0.4))

    # Organic dither on outer perimeter (y > 250): remove edge pixels with pseudo-random sand stipple
    for y in range(250, arr.shape[0]):
        for x in range(arr.shape[1]):
            if arr[y, x, 3] == 255:
                # Count solid neighbors in 5x5
                y_min, y_max = max(0, y - 2), min(arr.shape[0], y + 3)
                x_min, x_max = max(0, x - 2), min(arr.shape[1], x + 3)
                nb = np.sum(arr[y_min:y_max, x_min:x_max, 3] == 255)
                # Outer perimeter has nb < 20
                if nb < 16 and (x * 7 + y * 13) % 4 != 0:
                    arr[y, x, 3] = 0

    im = Image.fromarray(arr)
    # Quantize to 36 colors, strictly binary alpha
    im = quantize_octopath(im, max_colors=36)
    return aid, im

# 3. Quantize portals to <= 36 colors (strictly binary alpha)
def fix_portals():
    results = []
    for aid in ("desert-portal-dormant", "desert-portal-active"):
        p = art_dir / aid / "final.png"
        im = Image.open(p).convert("RGBA")
        q_im = quantize_octopath(im, max_colors=36)
        results.append((aid, q_im))
    return results

# 4. Sculpt small-rock-03, tumbleweed-01, tumbleweed-02, boulder-03 to curve naturally (no straight vertical runs)
def sculpt_rock_03():
    aid = "desert-small-rock-03"
    p = art_dir / aid / "final.png"
    arr = np.array(Image.open(p).convert("RGBA"))
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()
    h = ymax - ymin + 1

    # Sculpt right edge into a natural curved rock facet
    for y in range(ymin, ymax + 1):
        rel_y = (y - ymin) / h
        # Parabolic natural rounding on right side:
        indent = int(12 + 10 * np.sin(rel_y * np.pi) + (rel_y - 0.5) * 6)
        cutoff = xmax - indent
        for x in range(cutoff, arr.shape[1]):
            arr[y, x, 3] = 0

    return aid, quantize_octopath(Image.fromarray(arr), max_colors=24)

def sculpt_tumbleweed(aid):
    p = art_dir / aid / "final.png"
    arr = np.array(Image.open(p).convert("RGBA"))
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()
    h = ymax - ymin + 1

    # Right side: sculpt organic twig silhouette with 2-pixel step variation
    for y in range(ymin, ymax + 1):
        rel_y = (y - ymin) / h
        # High-frequency branch tips
        indent = int(6 + 8 * (rel_y - 0.5)**2 + 4 * np.sin(rel_y * 22) + 2 * np.cos(rel_y * 31))
        cutoff = xmax - indent
        for x in range(cutoff, arr.shape[1]):
            # Leave occasional isolated branch pixel
            if not ((y % 5 == 2) and (x == cutoff)):
                arr[y, x, 3] = 0

    return aid, quantize_octopath(Image.fromarray(arr), max_colors=24)

def sculpt_boulder_03():
    aid = "desert-boulder-03"
    p = art_dir / aid / "final.png"
    arr = np.array(Image.open(p).convert("RGBA"))
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()
    h = ymax - ymin + 1

    for y in range(ymin, ymax + 1):
        rel_y = (y - ymin) / h
        indent = int(10 + 8 * np.sin(rel_y * np.pi * 1.5) + (rel_y - 0.3) * 6)
        cutoff = xmax - indent
        for x in range(cutoff, arr.shape[1]):
            arr[y, x, 3] = 0

    return aid, quantize_octopath(Image.fromarray(arr), max_colors=24)

# 5. Fix cracked-patch-01/02
def fix_cracked_patches():
    res = []
    for aid in ("desert-edge-sand-cracked-patch-01", "desert-edge-sand-cracked-patch-02"):
        p = art_dir / aid / "final.png"
        arr = np.array(Image.open(p).convert("RGBA"))
        alpha = arr[:, :, 3]
        rows, cols = np.where(alpha > 10)
        ymin, ymax = rows.min(), rows.max()
        xmin, xmax = cols.min(), cols.max()
        h = ymax - ymin + 1

        # Taper both ends (top ymin..ymin+25, bottom ymax-25..ymax)
        for y in range(ymin, ymax + 1):
            if y < ymin + 30:
                t = (ymin + 30 - y) / 30.0
                indent = int(25 * t)
                for x in range(xmin, xmin + indent): arr[y, x, 3] = 0
                for x in range(xmax - indent, arr.shape[1]): arr[y, x, 3] = 0
            elif y > ymax - 30:
                t = (y - (ymax - 30)) / 30.0
                indent = int(25 * t)
                for x in range(xmin, xmin + indent): arr[y, x, 3] = 0
                for x in range(xmax - indent, arr.shape[1]): arr[y, x, 3] = 0

        # Retint orange swirl to golden desert sand [#D9B26B]
        for y in range(arr.shape[0]):
            for x in range(arr.shape[1]):
                if arr[y, x, 3] == 255:
                    r, g, b = arr[y, x, :3]
                    arr[y, x, 0] = min(235, int(r * 0.94))
                    arr[y, x, 1] = min(195, int(g * 1.10))
                    arr[y, x, 2] = min(120, int(b * 1.05))

        im = quantize_octopath(Image.fromarray(arr), max_colors=24)
        res.append((aid, im))
    return res

# 6. Contact sheet generator
def render_contact_sheet(man):
    assets = [a for a in man["assets"] if (art_dir / a["id"] / "final.png").exists()]
    tile_w, tile_h = 160, 160
    cols = 10
    rows = (len(assets) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * tile_w, rows * tile_h), (32, 28, 24, 255))
    draw = ImageDraw.Draw(sheet)

    for i, a in enumerate(assets):
        aid = a["id"]
        im_p = art_dir / aid / "final.png"
        im = Image.open(im_p).convert("RGBA")
        im.thumbnail((tile_w - 20, tile_h - 30), Image.Resampling.NEAREST)
        gx = (i % cols) * tile_w
        gy = (i // cols) * tile_h
        # Draw border
        draw.rectangle([gx, gy, gx + tile_w - 1, gy + tile_h - 1], outline=(55, 48, 40, 255))
        ox = gx + (tile_w - im.size[0]) // 2
        oy = gy + (tile_h - 20 - im.size[1]) // 2
        sheet.paste(im, (ox, oy), im)
        # Label
        draw.text((gx + 4, gy + tile_h - 18), aid[:18], fill=(220, 200, 170, 255))

    sheet_p = art_dir / "contact-sheet.png"
    sheet.save(sheet_p, optimize=True)
    print(f"Generated updated contact sheet at {sheet_p}")

# Execution
print("=== Running Round 4 Asset Remedies ===")
manifest_p = art_dir / "manifest.json"
man = json.load(open(manifest_p))
man_map = {a["id"]: a for a in man["assets"]}

# 1. Boulder 01
aid, im = restore_boulder_01()
h = save_and_sync(aid, im)
man_map[aid]["sha256"] = h
man_map[aid]["px"] = [im.size[0], im.size[1]]
man_map[aid]["colors"] = len(set(im.getdata()))
print(f"Restored {aid}: {im.size}, sha256={h[:8]}")

# 2. Monster bones
aid, im = fix_monster_bones()
h = save_and_sync(aid, im)
man_map[aid]["sha256"] = h
man_map[aid]["colors"] = len(set(im.getdata()))
print(f"Fixed {aid}: sha256={h[:8]}")

# 3. Portals
for aid, im in fix_portals():
    h = save_and_sync(aid, im)
    man_map[aid]["sha256"] = h
    man_map[aid]["colors"] = len(set(im.getdata()))
    print(f"Quantized portal {aid}: colors={man_map[aid]['colors']}, sha256={h[:8]}")

# 4. Sculpt rocks & tumbleweeds
for fn in (sculpt_rock_03, sculpt_boulder_03):
    aid, im = fn()
    h = save_and_sync(aid, im)
    man_map[aid]["sha256"] = h
    man_map[aid]["colors"] = len(set(im.getdata()))
    print(f"Sculpted {aid}: sha256={h[:8]}")

for aid_tw in ("desert-tumbleweed-01", "desert-tumbleweed-02"):
    aid, im = sculpt_tumbleweed(aid_tw)
    h = save_and_sync(aid, im)
    man_map[aid]["sha256"] = h
    man_map[aid]["colors"] = len(set(im.getdata()))
    print(f"Sculpted {aid}: sha256={h[:8]}")

# 5. Cracked patches
for aid, im in fix_cracked_patches():
    h = save_and_sync(aid, im)
    man_map[aid]["sha256"] = h
    man_map[aid]["colors"] = len(set(im.getdata()))
    print(f"Fixed {aid}: sha256={h[:8]}")

# Save manifest
with open(manifest_p, "w", encoding="utf-8") as f:
    json.dump(man, f, indent=2, ensure_ascii=False)

# Render contact sheet (with fresh mtime AFTER manifest)
render_contact_sheet(man)
print("Finished Round 4 asset remedies successfully!")
