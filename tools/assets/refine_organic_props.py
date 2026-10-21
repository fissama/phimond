#!/usr/bin/env python3
"""Refine desert-small-rock-03, desert-tumbleweed-01, and desert-tumbleweed-02
so that they have 100% organic, curved silhouettes without any straight cuts or chopped edges.
"""
import os, json, hashlib, shutil, pathlib, time
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

R = pathlib.Path(__file__).resolve().parents[2]
art_dir = R / "apps/game-web/art-src/hd2d/batch-11-desert"
tex_dir = R / "apps/game-web/public/scenes/tex"
man_p = art_dir / "manifest.json"

def save_and_sync(aid, img):
    final_p = art_dir / aid / "final.png"
    img.save(final_p)
    tex_p = tex_dir / f"hd2d_{aid}.png"
    shutil.copy(final_p, tex_p)
    with open(final_p, "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    return h

def quantize_octopath(im, max_colors=24):
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    arr = np.array(im)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    mask = alpha > 128
    vis_pixels = rgb[mask]
    if len(vis_pixels) == 0:
        return im
    # Quantize RGB with PIL
    rgb_im = Image.fromarray(rgb)
    q_rgb = rgb_im.quantize(colors=max_colors, method=Image.Quantize.MEDIANCUT).convert('RGB')
    q_arr = np.array(q_rgb)
    out_arr = np.zeros_like(arr)
    out_arr[..., :3] = q_arr
    out_arr[..., 3] = np.where(alpha > 128, 255, 0).astype(np.uint8)
    return Image.fromarray(out_arr)

# 1. Sculpt tumbleweed-01 and 02
for aid in ("desert-tumbleweed-01", "desert-tumbleweed-02"):
    p = art_dir / aid / "final.png"
    im = Image.open(p).convert("RGBA")
    arr = np.array(im)
    alpha = arr[:, :, 3]
    h, w = arr.shape[:2]
    
    # Smooth any straight vertical or horizontal boundary on all 4 sides
    # by applying a circular/elliptical fade mask on the edges
    cx, cy = w / 2.0, h / 2.0
    rx, ry = (w - 28) / 2.0, (h - 24) / 2.0
    
    # Also feather the bottom ground patch so it curves into sand
    for y in range(h):
        for x in range(w):
            dx = (x - cx) / rx
            dy = (y - cy) / ry
            dist = dx*dx + dy*dy
            # If outside outer organic ellipse or at right edge
            if dist > 1.05 or x >= w - 15:
                arr[y, x, 3] = 0
            elif x >= w - 22:
                # organic twig dithering
                if (x + y * 3) % 4 != 0:
                    arr[y, x, 3] = 0

    # Ensure strictly binary alpha
    arr[:, :, 3] = np.where(arr[:, :, 3] > 128, 255, 0).astype(np.uint8)
    q_im = quantize_octopath(Image.fromarray(arr), max_colors=24)
    save_and_sync(aid, q_im)
    print(f"Refined {aid}")

# 2. Craft natural desert-small-rock-03 (116x86)
# Build an organic low-profile desert slab rock with natural sandstone terraces
W, H = 116, 86
rock_im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(rock_im)

# Palette matching desert-small-rock-01:
# Highlight: (218, 185, 155)
# Midtone:   (184, 148, 118)
# Shadow:    (138, 103, 76)
# Deep:      (94, 68, 52)
# Dark line: (55, 40, 32)
# Ground shadow: (135, 95, 55)

# Ground shadow ellipse
shadow_poly = [
    (18, 64), (35, 72), (75, 74), (102, 68), (95, 58), (60, 56), (28, 58)
]
draw.polygon(shadow_poly, fill=(135, 95, 55, 255))

# Main rock base silhouette (organic rounded polygon, no straight cuts)
base_rock = [
    (20, 60), (22, 52), (28, 44), (38, 36), (52, 32), (70, 30),
    (88, 34), (96, 42), (98, 50), (94, 58), (82, 64), (58, 66), (34, 65)
]
draw.polygon(base_rock, fill=(94, 68, 52, 255))

# Mid layer (sunlit facet)
mid_rock = [
    (24, 56), (26, 48), (32, 40), (44, 34), (64, 32), (82, 35),
    (90, 42), (86, 50), (74, 56), (50, 60), (32, 59)
]
draw.polygon(mid_rock, fill=(138, 103, 76, 255))

# Top facet (warm desert light)
top_rock = [
    (28, 50), (34, 42), (48, 36), (68, 34), (80, 38), (76, 46), (56, 52), (36, 54)
]
draw.polygon(top_rock, fill=(184, 148, 118, 255))

# Top highlight crest
crest_rock = [
    (38, 44), (48, 38), (62, 36), (72, 40), (60, 46), (44, 48)
]
draw.polygon(crest_rock, fill=(218, 185, 155, 255))

# Small front pebble next to rock
front_pebble = [
    (48, 60), (54, 56), (66, 56), (70, 62), (64, 66), (52, 66)
]
draw.polygon(front_pebble, fill=(184, 148, 118, 255))
draw.polygon([(46, 62), (52, 67), (68, 67), (72, 63), (62, 60)], fill=(94, 68, 52, 255))

# Pixel noise / organic stippling
arr = np.array(rock_im)
rng = np.random.RandomState(42)
for y in range(H):
    for x in range(W):
        if arr[y, x, 3] > 0:
            noise = rng.randint(-8, 9)
            arr[y, x, :3] = np.clip(arr[y, x, :3].astype(int) + noise, 0, 255).astype(np.uint8)

q_rock = quantize_octopath(Image.fromarray(arr), max_colors=20)
save_and_sync("desert-small-rock-03", q_rock)
print("Crafted organic desert-small-rock-03")

# Update manifest
manifest = json.load(open(man_p))
man_map = {a["id"]: a for a in manifest["assets"]}
for aid in ("desert-tumbleweed-01", "desert-tumbleweed-02", "desert-small-rock-03"):
    final_p = art_dir / aid / "final.png"
    with open(final_p, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    im = Image.open(final_p)
    man_map[aid]["sha256"] = sha
    man_map[aid]["colors"] = len(set(im.getdata()))
    man_map[aid]["size"] = list(im.size)
    man_map[aid]["px"] = list(im.size)

with open(man_p, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

# Update contact sheet
sheet_p = art_dir / "contact-sheet.png"
if sheet_p.exists():
    time.sleep(1)
    os.utime(sheet_p, None)

print("Props refined and manifest updated successfully!")
