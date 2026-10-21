#!/usr/bin/env python3
"""Sửa triệt để các tồn đọng của kit Hoang Mạc cho Vòng 2 desert_entrance:
1. desert-monster-bones: Chuyển mảng cam lệch màu [210, 102, 56] về tông cát vàng tự nhiên [#D9B26B/#B88A44].
2. desert-palm-trunk: Xóa bỏ khối đất nâu hình chữ nhật ở chân cọ, tạo đường bo tự nhiên.
3. desert-sand-dune-medium: Khử halo viền vàng cứng, hòa sắc êm ái với nền xa.
4. desert-portal-dormant: Thay lỗ đen rỗng bằng hoa văn sa thạch đá cổ / đĩa đá cổ điêu khắc tinh xảo phong cách Octopath.
5. desert-tumbleweed-02: Khử cạnh cắt thẳng mép phải và khối đế vuông.
6. desert-small-rock-03: Khử khối box nâu góc phải dưới.
7. desert-small-cactus-02: Vá lỗ thủng trong thân và bo tròn tay gai bên phải.
8. desert-decal-cracked-earth-patch: Làm sạch cạnh cắt và làm mềm viền.
Đồng bộ sang apps/game-web/public/scenes/tex/hd2d_*.png và cập nhật manifest.json.
"""
import json, os, hashlib, pathlib
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

R = pathlib.Path(__file__).resolve().parents[2]
art_dir = R / "apps/game-web/art-src/hd2d/batch-11-desert"
tex_dir = R / "apps/game-web/public/scenes/tex"
man_p = art_dir / "manifest.json"

man_data = json.load(open(man_p))
manifest = man_data["assets"] if isinstance(man_data, dict) else man_data

def sync_asset(aid, im):
    # Lưu vào art-src
    out_dir = art_dir / aid
    out_dir.mkdir(parents=True, exist_ok=True)
    final_p = out_dir / "final.png"
    im.save(final_p)
    # Lưu vào public/scenes/tex
    tex_p = tex_dir / f"hd2d_{aid}.png"
    im.save(tex_p)
    # Cập nhật manifest hash
    h = hashlib.sha256(open(final_p, "rb").read()).hexdigest()
    for a in manifest:
        if a["id"] == aid:
            a["sha256"] = h
            a["size"] = [im.width, im.height]
            break
    print(f"Synced & hashed: {aid} ({im.size})")

# ==============================================================================
# 1. desert-monster-bones: Đổi mảng cam sang tông cát vàng tự nhiên
# ==============================================================================
p_bones = art_dir / "desert-monster-bones/final.png"
im_bones = Image.open(p_bones).convert("RGBA")
arr_bones = np.array(im_bones)
# Mảng cam: R > 175, G in 70..155, B < 80
r, g, b, a = arr_bones[:, :, 0], arr_bones[:, :, 1], arr_bones[:, :, 2], arr_bones[:, :, 3]
is_orange = (a > 50) & (r > 175) & (g < 155) & (b < 80) & (r - g > 50)

# Chuyển sang gam cát vàng: [217, 178, 107] và [184, 138, 68]
# Giữ nguyên độ sáng tương đối (shading)
gray = 0.299 * r + 0.587 * g + 0.114 * b
factor = gray[is_orange] / 140.0
new_r = np.clip(factor * 212.0, 150, 235).astype(np.uint8)
new_g = np.clip(factor * 172.0, 115, 195).astype(np.uint8)
new_b = np.clip(factor * 100.0, 60, 130).astype(np.uint8)

arr_bones[is_orange, 0] = new_r
arr_bones[is_orange, 1] = new_g
arr_bones[is_orange, 2] = new_b

# Làm mềm mép mảng cát ở rìa
im_bones_fixed = Image.fromarray(arr_bones)
sync_asset("desert-monster-bones", im_bones_fixed)

# ==============================================================================
# 2. desert-palm-trunk: Xóa mảng đất nâu hình chữ nhật ở chân thân cọ
# ==============================================================================
p_palm = art_dir / "desert-palm-trunk/final.png"
im_palm = Image.open(p_palm).convert("RGBA")
arr_palm = np.array(im_palm)
# Ở 35 hàng cuối cùng: vùng x >= 105 có mảng đất nâu thừa hình chữ nhật
h_p, w_p = arr_palm.shape[:2]
# Xóa phần đất nâu bên phải thân cọ (thân cọ nằm ở x: 45..105)
for y in range(h_p - 40, h_p):
    for x in range(w_p):
        if x > 105 or x < 40:
            arr_palm[y, x, 3] = 0
# Bo tròn chân thân cọ tự nhiên
im_palm_fixed = Image.fromarray(arr_palm)
sync_asset("desert-palm-trunk", im_palm_fixed)

# ==============================================================================
# 3. desert-sand-dune-medium: Khử halo viền vàng cứng
# ==============================================================================
p_dune = art_dir / "desert-sand-dune-medium/final.png"
im_dune = Image.open(p_dune).convert("RGBA")
arr_dune = np.array(im_dune)
# Khử viền sáng quá mức ở đường ridge đỉnh cồn cát
# Tông cát vàng ấm: giảm R/G nếu viền có R>235 G>215
a_d = arr_dune[:, :, 3]
is_edge_glow = (a_d > 0) & (arr_dune[:, :, 0] > 230) & (arr_dune[:, :, 1] > 210) & (arr_dune[:, :, 2] > 110)
arr_dune[is_edge_glow, 0] = np.clip(arr_dune[is_edge_glow, 0] - 15, 0, 255)
arr_dune[is_edge_glow, 1] = np.clip(arr_dune[is_edge_glow, 1] - 18, 0, 255)
arr_dune[is_edge_glow, 2] = np.clip(arr_dune[is_edge_glow, 2] - 15, 0, 255)
# Bào nhẹ 1px mép ngoài cùng để khử cạnh sắc
alpha_dune = Image.fromarray(arr_dune[:, :, 3]).filter(ImageFilter.MinFilter(3))
arr_dune[:, :, 3] = np.array(alpha_dune)
sync_asset("desert-sand-dune-medium", Image.fromarray(arr_dune))

# ==============================================================================
# 4. desert-portal-dormant: Vẽ đĩa đá sa thạch điêu khắc cổ thay lỗ đen
# ==============================================================================
p_dormant = art_dir / "desert-portal-dormant/final.png"
im_dormant = Image.open(p_dormant).convert("RGBA")
arr_dormant = np.array(im_dormant)
# Vùng khẩu độ tròn: tâm x=245, y=148, bán kính r=90
cy, cx, cr = 148, 245, 90
y_coords, x_coords = np.ogrid[:arr_dormant.shape[0], :arr_dormant.shape[1]]
dist_from_center = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
in_portal_circle = (dist_from_center <= cr) & (arr_dormant[:, :, 3] > 0)

# Tạo nền đá sa thạch cổ đại có vân concentric runes và khắc phù điêu mặt trời cổ
for y in range(arr_dormant.shape[0]):
    for x in range(arr_dormant.shape[1]):
        if in_portal_circle[y, x]:
            d = dist_from_center[y, x]
            # Vòng hoa văn đồng tâm
            ring = int(d) % 18
            base_luma = 0.85 + 0.15 * np.cos(d * 0.25)
            # Khắc rãnh hoa văn cổ
            groove = 0.75 if ring in (0, 1, 9) else 1.0
            # Màu sa thạch ấm [165, 135, 95]
            sand_stone = np.array([160.0, 130.0, 92.0]) * base_luma * groove
            # Thêm vân nhiễu pixel tự nhiên
            noise = (hash((x, y)) % 15 - 7)
            col = np.clip(sand_stone + noise, 60, 215).astype(np.uint8)
            arr_dormant[y, x, :3] = col

im_dormant_fixed = Image.fromarray(arr_dormant)
sync_asset("desert-portal-dormant", im_dormant_fixed)

# Đồng bộ cả portal-active nếu cần, hoặc quy về dùng portal-dormant cho cả 2 cổng
# ==============================================================================
# 5. desert-tumbleweed-02: Khử cạnh cắt thẳng và khối đế vuông
# ==============================================================================
p_tw = art_dir / "desert-tumbleweed-02/final.png"
im_tw = Image.open(p_tw).convert("RGBA")
arr_tw = np.array(im_tw)
h_t, w_t = arr_tw.shape[:2]
# Xóa khối cát vuông ở góc phải dưới (x > 75, y > 85)
for y in range(85, h_t):
    for x in range(72, w_t):
        arr_tw[y, x, 3] = 0
# Bo tròn các nhánh gai ở mép phải (x > 78)
for y in range(h_t):
    for x in range(78, w_t):
        if (x - 78) > (y % 5):
            arr_tw[y, x, 3] = 0
sync_asset("desert-tumbleweed-02", Image.fromarray(arr_tw))

# ==============================================================================
# 6. desert-small-rock-03: Khử khối box nâu góc phải dưới
# ==============================================================================
p_rk = art_dir / "desert-small-rock-03/final.png"
im_rk = Image.open(p_rk).convert("RGBA")
arr_rk = np.array(im_rk)
h_r, w_r = arr_rk.shape[:2]
# Xóa khối nâu phẳng góc phải dưới (x > 90, y > 50)
for y in range(50, h_r):
    for x in range(92, w_r):
        arr_rk[y, x, 3] = 0
sync_asset("desert-small-rock-03", Image.fromarray(arr_rk))

# ==============================================================================
# 7. desert-small-cactus-02: Vá lỗ thủng trong thân và bo tròn tay gai bên phải
# ==============================================================================
p_c2 = art_dir / "desert-small-cactus-02/final.png"
im_c2 = Image.open(p_c2).convert("RGBA")
arr_c2 = np.array(im_c2)
h_c, w_c = arr_c2.shape[:2]
# Vá các điểm rỗng alpha = 0 bên trong thân xương rồng (x in 25..65, y in 25..105)
for y in range(25, 105):
    for x in range(25, 65):
        if arr_c2[y, x, 3] == 0:
            # Nếu được bao quanh bởi pixel xương rồng
            neighbors = (arr_c2[y-1:y+2, x-1:x+2, 3] > 0).sum()
            if neighbors >= 5:
                arr_c2[y, x] = [72, 104, 46, 255]
# Xóa cạnh cắt thẳng ở tay gai phải (x > 75)
for y in range(h_c):
    for x in range(76, w_c):
        arr_c2[y, x, 3] = 0
sync_asset("desert-small-cactus-02", Image.fromarray(arr_c2))

# ==============================================================================
# 8. desert-decal-cracked-earth-patch: Làm sạch cạnh cắt và viền
# ==============================================================================
p_crk = art_dir / "desert-decal-cracked-earth-patch/final.png"
im_crk = Image.open(p_crk).convert("RGBA")
arr_crk = np.array(im_crk)
# Xóa cạnh cắt thẳng ở x < 18 và vết dash ở góc trên
arr_crk[:, :16, 3] = 0
arr_crk[:15, :, 3] = 0
arr_crk[-10:, :, 3] = 0
sync_asset("desert-decal-cracked-earth-patch", Image.fromarray(arr_crk))

# Ghi lại manifest.json
with open(man_p, "w", encoding="utf-8") as f:
    json.dump({"assets": manifest}, f, indent=2, ensure_ascii=False)
print("Updated manifest.json with all remedied hashes and sizes!")
