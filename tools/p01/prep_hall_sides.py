#!/usr/bin/env python3
"""Xử lý ảnh GPT (lan can/trụ/ô kính bên hông sảnh, nền magenta) → PNG alpha nhị phân, ≤48 màu, ghi assets.json.
Dùng: python3 tools/p01/prep_hall_sides.py <lan-can.png> <tru.png> <o-kinh.png>
"""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PUB = ROOT / "apps/client/public/hd2d"
# id, file index, chiều rộng đích (px), category
OUT = [("hall-side-balustrade", 0, 512), ("hall-side-pier", 1, 128), ("hall-side-window", 2, 256)]


def key(im):
    im = im.convert("RGB")
    px = im.load()
    w, h = im.size
    a = Image.new("L", (w, h), 255)
    ap = a.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if r > 170 and b > 170 and g < 120 and abs(r - b) < 90:
                ap[x, y] = 0
    out = im.convert("RGBA")
    out.putalpha(a)
    return out


def main(files):
    mf = PUB / "assets.json"
    A = json.loads(mf.read_text())
    for aid, i, tw in OUT:
        im = key(Image.open(files[i]))
        im = im.crop(im.getchannel("A").getbbox())
        th = round(im.height * tw / im.width)
        rgb = im.convert("RGB").resize((tw, th), Image.LANCZOS)
        al = im.getchannel("A").resize((tw, th), Image.BOX).point(lambda v: 255 if v >= 160 else 0)
        q = rgb.quantize(colors=48, method=Image.MEDIANCUT, dither=Image.NONE).convert("RGB").convert("RGBA")
        q.putalpha(al)
        q.save(PUB / f"{aid}.png")
        A[aid] = {"category": "prop", "px": [tw, th], "pivot_px": [tw / 2, th - 1], "frames": 1, "fps": None, "sway": False,
                  "tileable": "none", "world": [round(tw / 128, 4), round(th / 128, 4)]}
        print(aid, tw, th)
    mf.write_text(json.dumps(A, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main([Path(p) for p in sys.argv[1:4]])
