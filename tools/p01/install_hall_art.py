#!/usr/bin/env python3
"""Nạp bộ asset Triệu Linh Điện (GPT vẽ lại 2026-10-28) vào apps/client/public/hd2d và assets.json.

Chỉ thêm/ghi đè các id liệt kê dưới đây, không đụng mục khác của assets.json.
Dùng:  python3 tools/p01/install_hall_art.py <thư-mục-chứa-ảnh-đã-chép>   (xem SRC bên dưới để biết tên file)
Nguồn gốc ảnh: apps/game-web/art-src/hd2d/batch-02-octopath/summon-hall-redraw-20261028/ (lô 10-28) và .../completion-20261029/summon-hall-extra-assets.zip
(stone-floor-b, city-backdrop-wide, city-near-roofs, floor-light-1..3). Cột/nền/thành phố rộng nằm chung một thư mục khi chạy.
"""
import json, shutil, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PUB = ROOT / "apps/client/public/hd2d"
# id -> (file nguồn, category, pivot (None = giữa-đáy theo bbox alpha), world (None = px/128), frames, fps, tileable)
SPEC = {
    "hall-floor-marble": ("stone-floor.png", "floor", "center", [4, 4], 1, None, "xy"),
    "hall-city-backdrop": ("city-backdrop-wide.png", "backdrop_far", "bottom", None, 1, None, "none"),
    "hall-floor-marble-b": ("stone-floor-b.png", "floor", "center", [4, 4], 1, None, "xy"),
    "hall-city-roofs": ("city-near-roofs.png", "prop", "bottom", None, 1, None, "none"),
    "hall-floor-light-1": ("floor-light-1.png", "decal", "center", None, 1, None, "none"),
    "hall-floor-light-2": ("floor-light-2.png", "decal", "center", None, 1, None, "none"),
    "hall-floor-light-3": ("floor-light-3.png", "decal", "center", None, 1, None, "none"),
    "hall-column": ("column.png", "prop", "bbox-bottom", None, 1, None, "none"),
    "hall-lintel": ("lintel.png", "prop", "bottom", None, 1, None, "none"),
    "hall-threshold-left": ("threshold-left.png", "prop", "bbox-bottom", None, 1, None, "none"),
    "hall-threshold-right": ("threshold-right.png", "prop", "bbox-bottom", None, 1, None, "none"),
    "summon-pedestal-01": ("pedestal-01.png", "prop", "bbox-bottom", None, 1, None, "none"),
    "summon-pedestal-02": ("pedestal-02.png", "prop", "bbox-bottom", None, 1, None, "none"),
    "summon-pedestal-03": ("pedestal-03.png", "prop", "bbox-bottom", None, 1, None, "none"),
    "hall-lectern": ("prop-ceremonial-lectern.png", "prop", "bbox-bottom", None, 1, None, "none"),
    "hall-lantern": ("prop-hanging-lantern.png", "prop", "bbox-top", None, 1, None, "none"),
    "hall-banner": ("prop-heraldic-banner.png", "prop", "bbox-bottom", None, 1, None, "none"),
    "hall-globe": ("prop-oracle-globe.png", "prop", "bbox-bottom", None, 1, None, "none"),
    "hall-stained-glass": ("prop-stained-glass-panel.png", "prop", "bbox-bottom", None, 1, None, "none"),
}


def strip(names, out):
    ims = [Image.open(n).convert("RGBA") for n in names]
    w, h = ims[0].size
    sheet = Image.new("RGBA", (w * len(ims), h))
    for i, im in enumerate(ims):
        sheet.paste(im, (i * w, 0))
    sheet.save(out)
    return sheet.size


def main(src: Path):
    mf = PUB / "assets.json"
    A = json.loads(mf.read_text())
    for aid, (fn, cat, piv, world, frames, fps, tile) in SPEC.items():
        im = Image.open(src / fn).convert("RGBA")
        w, h = im.size
        bb = im.getchannel("A").getbbox() or (0, 0, w, h)
        pivot = {"center": [w / 2, h / 2], "bottom": [w / 2, h - 1], "bbox-bottom": [w / 2, bb[3]], "bbox-top": [w / 2, bb[1]]}[piv]
        shutil.copyfile(src / fn, PUB / f"{aid}.png")
        A[aid] = {"category": cat, "px": [w, h], "pivot_px": pivot, "frames": frames, "fps": fps, "sway": False,
                  "tileable": tile, "world": world or [round(w / 128, 4), round(h / 128, 4)]}
    # Dải nhiều khung: vòng triệu hồi (4), bụi linh khí (4)
    for aid, pre, fps in (("summon-circle-fx", "circle", 5), ("summon-motes-fx", "motes", 6)):
        names = [src / f"{pre}-{i}.png" for i in range(1, 5)]
        size = strip(names, PUB / f"{aid}.png")
        A[aid] = {"category": "fx", "px": list(size), "pivot_px": [96, 96], "frames": 4, "fps": fps, "sway": False,
                  "tileable": "none", "world": [1.5, 1.5]}
    # Lư hương: ảnh nguồn có hai lư (khác nhau ở làn khói) cạnh nhau → tách thành dải 2 khung hoạt hình khói.
    im = Image.open(src / "prop-incense-braziers.png").convert("RGBA")
    a = im.getchannel("A")
    mid = im.width // 2
    left = a.crop((0, 0, mid, im.height)).getbbox()
    right = a.crop((mid, 0, im.width, im.height)).getbbox()
    cw = max(left[2] - left[0], right[2] - right[0])
    y0, y1 = min(left[1], right[1]), max(left[3], right[3])
    sheet = Image.new("RGBA", (cw * 2, y1 - y0))
    sheet.paste(im.crop((left[0], y0, left[0] + cw, y1)), (0, 0))
    sheet.paste(im.crop((mid + right[0], y0, mid + right[0] + cw, y1)), (cw, 0))
    sheet.save(PUB / "hall-brazier.png")
    A["hall-brazier"] = {"category": "prop", "px": [cw * 2, y1 - y0], "pivot_px": [cw / 2, y1 - y0 - 1], "frames": 2, "fps": 2.5, "sway": False,
                         "tileable": "none", "world": [round(cw / 128, 4), round((y1 - y0) / 128, 4)]}
    mf.write_text(json.dumps(A, ensure_ascii=False, indent=1) + "\n")
    print("ok", len(SPEC) + 2, "asset")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
