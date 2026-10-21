#!/usr/bin/env python3
"""Tạo ảnh so sánh đối chiếu desert_entrance_preview.png giữa ảnh gốc level6_Phiadong.png
và sơ đồ bố cục 3 tầng HD-2D Vòng 3 (desert_entrance.json).
"""
import json, pathlib
from PIL import Image, ImageDraw, ImageFont

R = pathlib.Path(__file__).resolve().parents[2]
src_map_p = R / "tools/.cache/reference/rooms/level6_Phiadong.png"
layout_p = R / ".ai/design/map-layouts/desert/desert_entrance.json"
brief_p = R / ".ai/design/map-briefs/kit_desert/desert_entrance.json"
man_p = R / "apps/game-web/art-src/hd2d/batch-11-desert/manifest.json"
out_p = R / ".ai/design/map-layouts/desert/desert_entrance_preview.png"

src_img = Image.open(src_map_p).convert("RGBA")
W, H = src_img.size

layout = json.load(open(layout_p))
brief = json.load(open(brief_p))
man = {a["id"]: a for a in json.load(open(man_p))["assets"]}

# Panel dưới: vẽ sơ đồ bố cục trên nền ảnh gốc mờ 60%
bot_img = src_img.copy()
draw = ImageDraw.Draw(bot_img, "RGBA")

# Vẽ dải đi bộ trung tâm walkable band
draw.rectangle([0, 480, W, 640], fill=(255, 230, 150, 40), outline=(217, 178, 107, 120), width=2)

# Phân loại màu theo layer:
# back: cyan (50, 150, 255)
# mid: amber (255, 170, 50)
# front: green (80, 220, 100)
layer_colors = {
    "back": (50, 150, 255, 180),
    "mid": (255, 170, 50, 180),
    "front": (80, 220, 100, 180)
}

for p in layout["placements"]:
    aid = p["asset"]
    a = man.get(aid)
    if not a: continue
    cat = a["category"]
    if cat in ("backdrop", "backdrop_far", "tile"): continue
    
    x, y = p["px"]
    sc = p.get("scale", 1.0)
    ww, wh = a["world"]
    w, h = ww * 100 * sc, wh * 100 * sc
    layer = p.get("layer", "mid")
    col = layer_colors.get(layer, (200, 200, 200, 150))
    
    # Bbox của vật thể
    bx1 = x - w / 2
    by1 = y - h
    bx2 = x + w / 2
    by2 = y
    draw.rectangle([bx1, by1, bx2, by2], outline=col, width=1)
    # Chấm chân vật
    draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=col)

# Vẽ Keepouts và Anchors
for a in brief["anchors"]:
    ko = a.get("keepout_px")
    if ko:
        draw.rectangle(ko, fill=(255, 50, 50, 60), outline=(255, 50, 50, 220), width=2)

for a in layout["anchors"]:
    px = a["px"]
    # Điểm vàng nổi bật
    draw.ellipse([px[0] - 6, px[1] - 6, px[0] + 6, px[1] + 6], fill=(255, 220, 0, 255), outline=(0, 0, 0, 255), width=2)
    # Nhãn text
    draw.text((px[0] + 8, px[1] - 8), a["id"], fill=(255, 255, 255, 255))

# Ghép 2 panel thành 1 ảnh preview cao 2 * H + 60
canvas = Image.new("RGBA", (W, H * 2 + 60), (30, 30, 30, 255))
cdraw = ImageDraw.Draw(canvas)

cdraw.text((15, 12), f"ANH GOC: level6_Phiadong.png ({W} x {H} px) - Cua Ngo Hoang Mac", fill=(220, 220, 220, 255))
canvas.paste(src_img, (0, 30))

cdraw.text((15, H + 40), f"BO CUC HD-2D VONG 3: desert_entrance.json (Xanh duong=Back, Vang=Mid, Xanh la=Front, Do=Keepout, Vang tron=Anchor)", fill=(220, 220, 220, 255))
canvas.paste(bot_img, (0, H + 60))

canvas.save(out_p)
print(f"Saved preview comparison to {out_p}")
