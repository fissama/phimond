#!/usr/bin/env python3
"""Cài dải idle 4 khung (192×192 mỗi khung) cho 7 NPC mới vẽ lại: Mira, bia_free, bia_skill, sq_pillar, sq_skill, sq_exchange, sq_warehouse.

Chạy từ gốc repo (cần Pillow + numpy):
    python3 tools/p01/install_idle_npcs.py [--src DIR] [--dry]

- Nguồn mặc định: apps/game-web/art-src/hd2d/p01-release-art-20261023/delivery/<id>.idle.png.
- Kiểm: kích thước (n×192)×192, alpha nhị phân, khử điểm ảnh hồng/tím sót ở mép (cùng hàm với install_s01_s27.py),
  chân khung nào cũng chạm gần cùng một hàng (để nhân vật không "nhảy" giữa các khung).
- Ghi apps/client/public/hd2d/<id>.idle.png và đặt `idle_frames` trong assets.json (giữ nguyên các trường khác).
Chạy lại nhiều lần cho cùng kết quả.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("s01", ROOT / "tools/p01/install_s01_s27.py")
s01 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s01)

DEFAULT_SRC = ROOT / "apps/game-web/art-src/hd2d/p01-release-art-20261023/delivery"
HD = ROOT / "apps/client/public/hd2d"
NPCS = ["summoner_mira", "bia_free", "bia_skill", "sq_pillar", "sq_skill", "sq_exchange", "sq_warehouse"]
FRAME = 192


def foot_rows(a: np.ndarray, n: int) -> list[int]:
    rows = []
    for i in range(n):
        al = a[:, i * FRAME : (i + 1) * FRAME, 3] > 0
        ys = np.nonzero(al.any(axis=1))[0]
        rows.append(int(ys.max()) if len(ys) else -1)
    return rows


def main() -> None:
    dry = "--dry" in sys.argv
    src = Path(sys.argv[sys.argv.index("--src") + 1]) if "--src" in sys.argv else DEFAULT_SRC
    assets_path = HD / "assets.json"
    assets = json.loads(assets_path.read_text())
    for npc in NPCS:
        name = f"npc-{npc}"
        im = Image.open(src / f"{name}.idle.png").convert("RGBA")
        w, h = im.size
        n = w // FRAME
        assert h == FRAME and w == n * FRAME and n >= 2, f"{name}: kích thước {w}x{h} không phải dải {FRAME}px"
        a = np.array(im)
        semi = int(((a[..., 3] > 0) & (a[..., 3] < 255)).sum())
        if semi:
            a[..., 3] = np.where(a[..., 3] >= 128, 255, 0)
        a, fixed = s01.despill(a)
        feet = foot_rows(a, n)
        spread = max(feet) - min(feet)
        colors = len({tuple(p) for p in a.reshape(-1, 4) if p[3]})
        print(f"{name:26s} {n} khung, bán trong suốt {semi}, despill {fixed}, chân {feet} (lệch {spread}), {colors} màu")
        if spread > 6:
            print(f"  CẢNH BÁO: chân lệch {spread} px giữa các khung")
        if dry:
            continue
        Image.fromarray(a).save(HD / f"{name}.idle.png", optimize=True)
        assets.setdefault(name, {})["idle_frames"] = n
    if not dry:
        assets_path.write_text(json.dumps(assets, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
