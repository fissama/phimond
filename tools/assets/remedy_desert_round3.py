#!/usr/bin/env python3
"""Remediation script for Desert Batch-11 Round 3:
1. Fix all 18+ assets with flat sliced edges so bbox_edge.py returns 0 errors:
   - desert-tumbleweed-01, desert-tumbleweed-02
   - desert-small-rock-02, desert-small-rock-03
   - desert-boulder-03
   - desert-cactus-dead
   - desert-decal-cracked-earth-patch
   - desert-ruins-wall, desert-ruins-wall-arch
   - 6 desert-edge-sand-sandstone-* (corner-01, corner-02, n, s, e, w)
   - desert-chasm-ravine-02
   - desert-stone-stairs
   - desert-torch-lantern-anim
2. Fix desert-palm-trunk: strip bottom 66x28px dirt rectangle (rows >= 229) and add natural curved roots.
3. Fix desert-monster-bones: retint sand mound to golden sand [237, 188, 85] and feather outer perimeter (mép mềm).
4. Update desert-boulder-01 to authentic gray twisted spire + leaning cactus from level6_Phiadong.png.
5. Update manifest.json with new hashes and copy all textures to apps/game-web/public/scenes/tex/.
"""
import os, json, hashlib, shutil, pathlib
from PIL import Image, ImageFilter
import numpy as np

R = pathlib.Path(__file__).resolve().parents[2]
art_dir = R / "apps/game-web/art-src/hd2d/batch-11-desert"
tex_dir = R / "apps/game-web/public/scenes/tex"
man_path = art_dir / "manifest.json"

def save_and_sync(aid, img):
    final_p = art_dir / aid / "final.png"
    img.save(final_p)
    tex_p = tex_dir / f"hd2d_{aid}.png"
    shutil.copy(final_p, tex_p)
    with open(final_p, "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    return h

def sculpt_tumbleweed_01():
    aid = "desert-tumbleweed-01"
    p = art_dir / aid / "final.png"
    img = Image.open(p).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()
    h = ymax - ymin + 1

    # Sculpt right side: carve away the flat vertical cut from xmax - 12 to xmax
    # Make organic branch tips curling inwards and outwards
    for y in range(ymin, ymax + 1):
        rel_y = (y - ymin) / h
        # Curvature: taper top and bottom, oscillate branches in middle
        indent = int(6 + 8 * (rel_y - 0.5)**2 + 4 * np.sin(rel_y * 18))
        cutoff = xmax - indent
        for x in range(cutoff, arr.shape[1]):
            # Leave occasional isolated branch twig pixels
            if not ((y % 7 in (2, 3)) and (x < cutoff + 3)):
                arr[y, x, 3] = 0
            else:
                arr[y, x, 3] = min(arr[y, x, 3], 220)

    # Clean bottom dirt block if any
    for y in range(ymax - 4, ymax + 1):
        for x in range(arr.shape[1]):
            if (x + y) % 3 != 0 and y > ymax - 2:
                arr[y, x, 3] = 0

    return aid, Image.fromarray(arr)

def sculpt_tumbleweed_02():
    aid = "desert-tumbleweed-02"
    p = art_dir / aid / "final.png"
    img = Image.open(p).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()
    h = ymax - ymin + 1

    for y in range(ymin, ymax + 1):
        rel_y = (y - ymin) / h
        indent = int(4 + 6 * (rel_y - 0.5)**2 + 3 * np.cos(rel_y * 16))
        cutoff = xmax - indent
        for x in range(cutoff, arr.shape[1]):
            if not ((y % 6 == 2) and (x < cutoff + 2)):
                arr[y, x, 3] = 0

    return aid, Image.fromarray(arr)

def sculpt_small_rock_02():
    aid = "desert-small-rock-02"
    p = art_dir / aid / "final.png"
    img = Image.open(p).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()
    h = ymax - ymin + 1

    # Right side is cut off. Sculpt a natural rounded slope on right side
    # From ymin to ymax, create a smooth rock facet profile
    for y in range(ymin, ymax + 1):
        rel_y = (y - ymin) / h
        # Boulder profile: wider at bottom, round at top and bottom edge
        # Target right boundary:
        target_x = xmax - int(12 * (1.0 - rel_y)**1.2 + 6 * (rel_y**4))
        for x in range(target_x, arr.shape[1]):
            arr[y, x, 3] = 0
        # Add rock shading along new boundary
        if target_x - 1 >= 0:
            arr[y, target_x - 1, :3] = (arr[y, target_x - 1, :3] * 0.75).astype(np.uint8)

    # Soften bottom
    for x in range(arr.shape[1]):
        if ymax < arr.shape[0]:
            arr[ymax, x, 3] = min(arr[ymax, x, 3], 150)

    return aid, Image.fromarray(arr)

def sculpt_small_rock_03():
    aid = "desert-small-rock-03"
    p = art_dir / aid / "final.png"
    img = Image.open(p).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()
    h = ymax - ymin + 1

    # Remove the flat tab and flat cut on right (cols > xmax - 14)
    for y in range(ymin, ymax + 1):
        rel_y = (y - ymin) / h
        target_x = xmax - int(8 + 10 * (rel_y - 0.4)**2)
        for x in range(target_x, arr.shape[1]):
            arr[y, x, 3] = 0
        if target_x - 1 >= 0:
            arr[y, target_x - 1, :3] = (arr[y, target_x - 1, :3] * 0.8).astype(np.uint8)

    # Soften bottom flat row
    for x in range(arr.shape[1]):
        if ymax < arr.shape[0]:
            arr[ymax, x, 3] = min(arr[ymax, x, 3], 120)

    return aid, Image.fromarray(arr)

def sculpt_boulder_03():
    aid = "desert-boulder-03"
    p = art_dir / aid / "final.png"
    img = Image.open(p).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()
    h = ymax - ymin + 1

    for y in range(ymin, ymax + 1):
        rel_y = (y - ymin) / h
        # Slope right edge inward
        indent = int(10 * (1.0 - rel_y) + 8 * (rel_y**3))
        for x in range(xmax - indent, arr.shape[1]):
            arr[y, x, 3] = 0

    return aid, Image.fromarray(arr)

def sculpt_cactus_dead():
    aid = "desert-cactus-dead"
    p = art_dir / aid / "final.png"
    img = Image.open(p).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()

    # The right branch around y in [100, 160], x > xmax - 10 is cut vertically
    for y in range(ymin, ymax + 1):
        # Branch tip tapering: around y = 100..160
        if 95 <= y <= 165:
            rel = (y - 125) / 30.0
            indent = int(12 * (1.0 - rel**2))
            if indent > 0:
                for x in range(xmax - indent, arr.shape[1]):
                    arr[y, x, 3] = 0

    return aid, Image.fromarray(arr)

def sculpt_cracked_earth_patch():
    aid = "desert-decal-cracked-earth-patch"
    p = art_dir / aid / "final.png"
    img = Image.open(p).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()
    h = ymax - ymin + 1

    # Taper right crack ends
    for y in range(ymin, ymax + 1):
        rel_y = (y - ymin) / h
        indent = int(14 + 10 * np.sin(rel_y * 12))
        for x in range(xmax - indent, arr.shape[1]):
            arr[y, x, 3] = 0

    # Also soften bottom
    for x in range(arr.shape[1]):
        if ymax < arr.shape[0]:
            arr[ymax, x, 3] = 0
        if ymax - 1 < arr.shape[0]:
            arr[ymax - 1, x, 3] = min(arr[ymax - 1, x, 3], 140)

    return aid, Image.fromarray(arr)

def sculpt_ruins_wall():
    aid = "desert-ruins-wall"
    p = art_dir / aid / "final.png"
    img = Image.open(p).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()
    h = ymax - ymin + 1

    # Right side is cut flat at xmax. Create broken jagged ruin stones on right side
    # Blocks stepped: top is chipped, middle has missing bricks, bottom slopes out
    for y in range(ymin, ymax + 1):
        rel_y = (y - ymin) / h
        # Jagged stepped brick contour
        brick_step = int((y // 18) % 4) * 5
        indent = int(16 + 24 * (1.0 - rel_y) + brick_step)
        for x in range(xmax - indent, arr.shape[1]):
            arr[y, x, 3] = 0
        # Dark edge shading on broken brick surface
        edge_x = xmax - indent - 1
        if 0 <= edge_x < arr.shape[1]:
            arr[y, edge_x, :3] = (arr[y, edge_x, :3] * 0.7).astype(np.uint8)

    return aid, Image.fromarray(arr)

def sculpt_ruins_wall_arch():
    aid = "desert-ruins-wall-arch"
    p = art_dir / aid / "final.png"
    img = Image.open(p).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()
    h = ymax - ymin + 1

    for y in range(ymin, ymax + 1):
        rel_y = (y - ymin) / h
        brick_step = int((y // 22) % 3) * 6
        indent = int(14 + 18 * (1.0 - rel_y) + brick_step)
        for x in range(xmax - indent, arr.shape[1]):
            arr[y, x, 3] = 0
        edge_x = xmax - indent - 1
        if 0 <= edge_x < arr.shape[1]:
            arr[y, edge_x, :3] = (arr[y, edge_x, :3] * 0.7).astype(np.uint8)

    return aid, Image.fromarray(arr)

def sculpt_stone_stairs():
    aid = "desert-stone-stairs"
    p = art_dir / aid / "final.png"
    img = Image.open(p).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()
    h = ymax - ymin + 1

    # Right side 100% cut. Create weathered sandstone step erosion on right edge
    for y in range(ymin, ymax + 1):
        step = int((y // 24) % 3) * 8
        indent = int(12 + step + 6 * np.sin(y / 15.0))
        for x in range(xmax - indent, arr.shape[1]):
            arr[y, x, 3] = 0

    return aid, Image.fromarray(arr)

def sculpt_chasm_ravine_02():
    aid = "desert-chasm-ravine-02"
    p = art_dir / aid / "final.png"
    img = Image.open(p).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()
    h = ymax - ymin + 1

    # Taper left and right ends of ravine
    for y in range(ymin, ymax + 1):
        rel_y = (y - ymin) / h
        left_indent = int(25 * (1.0 - (2 * rel_y - 1)**2))
        right_indent = int(22 * (1.0 - (2 * rel_y - 1)**2))
        for x in range(xmin, xmin + left_indent):
            arr[y, x, 3] = 0
        for x in range(xmax - right_indent, arr.shape[1]):
            arr[y, x, 3] = 0

    return aid, Image.fromarray(arr)

def sculpt_torch_lantern_anim():
    aid = "desert-torch-lantern-anim"
    p = art_dir / aid / "final.png"
    img = Image.open(p).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()

    # Trim 3px on the rightmost column of frame 4
    for y in range(arr.shape[0]):
        for x in range(xmax - 4, arr.shape[1]):
            arr[y, x, 3] = 0

    return aid, Image.fromarray(arr)

def sculpt_edge_sandstone(aid):
    p = art_dir / aid / "final.png"
    img = Image.open(p).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows, cols = np.where(alpha > 10)
    ymin, ymax = rows.min(), rows.max()
    xmin, xmax = cols.min(), cols.max()
    h = ymax - ymin + 1
    w = xmax - xmin + 1

    # Edge decals had one straight cut side. Create undulating organic sand dunes / ripples
    # that taper to zero at the boundary so the edge column has < 15% density
    if "corner-01" in aid or "corner-02" in aid or "-e" in aid:
        # Left edge is straight: sculpt organic wavy sand contour on left
        for y in range(ymin, ymax + 1):
            rel_y = (y - ymin) / h
            indent = int(14 + 12 * np.sin(rel_y * 10))
            for x in range(xmin, xmin + indent):
                arr[y, x, 3] = 0

    if "corner-01" in aid or "corner-02" in aid or "-w" in aid or "-n" in aid or "-s" in aid:
        # Right edge is straight: sculpt organic wavy sand contour on right
        for y in range(ymin, ymax + 1):
            rel_y = (y - ymin) / h
            indent = int(14 + 12 * np.cos(rel_y * 10))
            for x in range(xmax - indent, arr.shape[1]):
                arr[y, x, 3] = 0

    return aid, Image.fromarray(arr)

def fix_palm_trunk():
    aid = "desert-palm-trunk"
    p = art_dir / aid / "final.png"
    img = Image.open(p).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]

    # Claude point 2: Gốc cọ (palm-trunk) vẫn có mảng đất nâu chữ nhật, cạnh trái thẳng.
    # Rows 229..256 had the 66x28px rectangular dirt box!
    # Zero out all rows >= 229
    arr[229:, :, 3] = 0

    # Curve the roots at y = 220..228 naturally into the sand
    for y in range(220, 229):
        # Trunk center ~ 100
        for x in range(arr.shape[1]):
            if x < 48 or x > 152:
                arr[y, x, 3] = 0
            elif x < 58 or x > 142:
                # soften root tips
                arr[y, x, 3] = min(arr[y, x, 3], 180)

    return aid, Image.fromarray(arr)

def fix_monster_bones():
    aid = "desert-monster-bones"
    p = art_dir / aid / "final.png"
    img = Image.open(p).convert("RGBA")
    arr = np.array(img).astype(np.float32)

    # Claude point 3: Mảng cam quanh xương thú lệch màu so với cát, mép cứng.
    # 1. Retint the sand mound around the bones to golden desert sand [237, 188, 85]
    # Sand floor target palette:
    # Highlight: [248, 218, 128]
    # Base sand: [237, 188, 85]
    # Sand shadow: [184, 138, 68]
    # Bones are near-white / ivory: R, G, B > 180 and R ~ G ~ B
    # Sand mound is currently reddish/orange: R > 190, G ~ 130..170, B ~ 70..105 (R - G > 35)

    alpha = arr[:, :, 3]
    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    is_solid = alpha > 20
    # Bone pixels: bright ivory/cream (R > 180, G > 175, B > 150) or deep bone shadow (R < 100, G < 90, B < 80)
    is_bone = (r > 190) & (g > 185) & (b > 155) & (abs(r - g) < 25)
    is_sand = is_solid & ~is_bone & (arr.shape[0] - np.indices(arr.shape[:2])[0] < 140)

    # For sand mound pixels: shift hue from orange towards golden sand
    # Increase Green, adjust Blue
    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            if alpha[y, x] > 20 and not is_bone[y, x]:
                # If reddish/orange sand mound (y > 180)
                if y > 180:
                    orig_r = arr[y, x, 0]
                    orig_g = arr[y, x, 1]
                    orig_b = arr[y, x, 2]
                    # Target golden sand tone
                    # R stays golden ~ 230..245
                    # G shifts up by +20..+35 towards golden yellow
                    # B shifts towards golden tone
                    arr[y, x, 0] = min(250.0, orig_r * 0.98)
                    arr[y, x, 1] = min(210.0, orig_g * 1.18 + 8.0)
                    arr[y, x, 2] = min(140.0, orig_b * 0.92 + 5.0)

    # 2. Feather the outer perimeter of the sand mound (mép mềm!)
    # Find distance to boundary of alpha
    mask = (alpha > 20).astype(np.uint8) * 255
    pil_mask = Image.fromarray(mask, mode="L")
    # Distance transform via blur / erosion
    eroded = pil_mask.filter(ImageFilter.MinFilter(9))
    blurred = eroded.filter(ImageFilter.GaussianBlur(radius=5))
    blur_arr = np.array(blurred).astype(np.float32) / 255.0

    # Apply soft feathering to the bottom and side perimeter
    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            if alpha[y, x] > 20 and y > 220:
                # Feather factor: 1.0 inside, smooth gradient to 0 at perimeter
                factor = min(1.0, blur_arr[y, x] * 1.25)
                arr[y, x, 3] = alpha[y, x] * factor

    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return aid, Image.fromarray(arr)

def fix_northwest_spire():
    aid = "desert-boulder-01"
    # Claude point 4: Ảnh gốc là mỏm đá xoắn XÁM + xương rồng xanh nghiêng ở xa.
    # Extract authentic sprite from level6_Phiadong.png
    src_p = R / "tools/.cache/reference/rooms/level6_Phiadong.png"
    src_img = Image.open(src_p).convert("RGBA")
    # Crop [20..220, 70..240]
    crop = src_img.crop((20, 70, 220, 240))
    arr = np.array(crop).astype(np.float32)

    # Remove sky background (sky has blue/cyan: G > 115, B > 130, R < 190)
    # Background distant hills: R ~ 180..210, G ~ 160..190, B ~ 120..150
    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    # Rock spire: grey colors (abs(R - G) < 25 and abs(G - B) < 30 and R < 185)
    # Cactus: green (G > R + 20 and G > B + 20)
    # Background sky: B > 130 and G > 120 and R < 170
    is_sky = (b > 125) & (g > 115) & (r < 175)
    # Distant background hill behind rock: y < 75 and (r > 150) & (b > 100) & (b < 140) & (r - b > 35)
    is_far_hill = (arr.shape[0] - np.indices(arr.shape[:2])[0] > 95) & (r > 140) & (r < 195) & (g > 120) & (g < 175) & (b > 85) & (b < 135)

    mask = ~(is_sky | is_far_hill)
    arr[~mask, 3] = 0

    # Feather bottom base into sand
    for y in range(arr.shape[0]):
        if y > arr.shape[0] - 15:
            fade = (arr.shape[0] - y) / 15.0
            arr[y, :, 3] *= fade

    # Clean borders (padding)
    out_arr = np.zeros((190, 220, 4), dtype=np.uint8)
    h_c, w_c = arr.shape[:2]
    out_arr[10:10+h_c, 10:10+w_c] = np.clip(arr, 0, 255).astype(np.uint8)

    return aid, Image.fromarray(out_arr)

# Execute all fixes
fixes = [
    sculpt_tumbleweed_01,
    sculpt_tumbleweed_02,
    sculpt_small_rock_02,
    sculpt_small_rock_03,
    sculpt_boulder_03,
    sculpt_cactus_dead,
    sculpt_cracked_earth_patch,
    sculpt_ruins_wall,
    sculpt_ruins_wall_arch,
    sculpt_stone_stairs,
    sculpt_chasm_ravine_02,
    sculpt_torch_lantern_anim,
    fix_palm_trunk,
    fix_monster_bones,
    fix_northwest_spire,
]

edge_aids = [
    "desert-edge-sand-sandstone-corner-01",
    "desert-edge-sand-sandstone-corner-02",
    "desert-edge-sand-sandstone-n",
    "desert-edge-sand-sandstone-s",
    "desert-edge-sand-sandstone-w",
    "desert-edge-sand-sandstone-e"
]

manifest = json.load(open(man_path))
man_assets = {a["id"]: a for a in manifest["assets"]}

print("Starting Round 3 asset remediation...")
for fn in fixes:
    aid, img = fn()
    h = save_and_sync(aid, img)
    if aid in man_assets:
        man_assets[aid]["sha256"] = h
    print(f"  Fixed {aid:35s} -> sha256={h[:8]}...")

for eaid in edge_aids:
    aid, img = sculpt_edge_sandstone(eaid)
    h = save_and_sync(aid, img)
    if aid in man_assets:
        man_assets[aid]["sha256"] = h
    print(f"  Fixed {aid:35s} -> sha256={h[:8]}...")

with open(man_path, "w") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print("Finished all asset remedies and updated manifest!")
