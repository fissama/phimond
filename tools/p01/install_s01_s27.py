#!/usr/bin/env python3
"""Cài các ảnh tĩnh lô S01–S27 (GPT, 2026-10-29) đã được Claude duyệt vào apps/client/public.

Chạy từ gốc repo (cần Pillow + numpy):
    python3 tools/p01/install_s01_s27.py [--dry]

Danh sách duyệt nằm trong .ai/design/v1.0.1/REVIEW-GPT-S01-S27-STATIC.md. Script này làm các việc review đã nêu:
- khử điểm ảnh hồng/tím sót ở mép (mép trong suốt thì xoá, nằm trong thân thì thay bằng màu láng giềng);
- cắt dải đen đặc ở rìa (forest-far-layers đáy, dirt-cliff-face trên);
- cobweb tím của fg-city-lantern-pair đổi sang xám ấm.
Ảnh sau xử lý ghi vào apps/client/public/hd2d/ (hoặc public/battle/ cho fx) và đăng ký vào assets.json.
Chạy lại nhiều lần cho cùng kết quả (không phụ thuộc trạng thái trước).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "apps/game-web/art-src/hd2d/octopath-s01-s27-20261029/delivery"
V2 = SRC / "redraw-v2"
HD = ROOT / "apps/client/public/hd2d"
BATTLE = ROOT / "apps/client/public/battle"
UI = ROOT / "apps/client/public/ui"

# (tên, thư mục nguồn, loại trong assets.json, ghi chú xử lý)
HD_ITEMS: list[tuple[str, Path, str, str]] = [
    ("city-facade-column", SRC, "prop", ""),
    ("city-facade-gutter", SRC, "prop", ""),
    ("city-facade-alley", SRC, "prop", ""),
    ("shadow-canopy", SRC, "decal", ""),
    ("shadow-rect", SRC, "decal", ""),
    ("shadow-round-large", SRC, "decal", ""),
    ("shadow-round-small", SRC, "decal", ""),
    ("stone-plinth-square", SRC, "prop", ""),
    ("stone-plinth-round", SRC, "prop", "despill"),
    ("stone-wall-face", SRC, "prop", "once"),
    ("stone-step-face", SRC, "prop", "despill"),
    ("stone-step-side-left", SRC, "prop", "despill"),
    ("stone-step-side-right", SRC, "prop", "despill"),
    ("palace-wall-fill", SRC, "prop", "once"),
    ("palace-courtyard-passage", SRC, "prop", "despill"),
    ("wood-bridge-plank", SRC, "prop", "once"),
    ("fence-stone-low", SRC, "prop", "despill"),
    ("grass-ledge-top", SRC, "prop", "despill"),
    ("dirt-cliff-face", SRC, "prop", "once;crop-top"),
    ("city-near-roofs", SRC, "backdrop_mid", "despill"),
    ("city-backdrop-wide", V2, "backdrop_far", ""),
    ("forest-far-layers", SRC, "backdrop_far", "crop-bottom-black"),
    ("fg-city-awning-edge", SRC, "fg", ""),
    ("fg-city-bunting", V2, "fg", ""),
    ("fg-city-lantern-pair", SRC, "fg", "despill;cobweb"),
    ("fg-forest-branch-a", SRC, "fg", "despill"),
    ("fg-forest-branch-b", SRC, "fg", "despill"),
    ("fg-forest-bush-a", SRC, "fg", ""),
    ("fg-forest-bush-b", SRC, "fg", ""),
    ("fg-forest-bush-c", SRC, "fg", ""),
    ("fg-hall-curtain", SRC, "fg", "despill"),
]
FX_ITEMS = ["fx-beast", "fx-insect", "fx-plant"]
# Ba hệ đã duyệt từ lô P01 trước (fx-fire/water/earth); phong/quang/ám/vô chưa có (M01–M04).
FX_OLD = ["fx-fire", "fx-water", "fx-earth"]
OLD = ROOT / "apps/game-web/art-src/hd2d/p01-release-art-20261023/delivery"
# bar-frame-*/bar-label-* đã duyệt nhưng chưa cài: HUD mới dùng vạch mảnh, chờ N01/N02 rồi mới quyết dùng.
UI_ITEMS = ["ui-minimap"]


def fringe_mask(a: np.ndarray) -> np.ndarray:
    r, g, b, al = (a[..., i].astype(int) for i in range(4))
    return (al > 0) & (r > 150) & (b > 130) & (g < r - 60) & (g < b - 30)


def despill(a: np.ndarray) -> tuple[np.ndarray, int]:
    total = 0
    for _ in range(4):
        m = fringe_mask(a)
        n = int(m.sum())
        if not n:
            break
        total += n
        h, w = m.shape
        out = a.copy()
        for y, x in zip(*np.nonzero(m)):
            nb = [(y + dy, x + dx) for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            edge = any(not (0 <= yy < h and 0 <= xx < w) or a[yy, xx, 3] == 0 for yy, xx in nb)
            if edge:
                out[y, x, 3] = 0
                continue
            good = [
                a[yy, xx, :3]
                for yy in range(max(0, y - 1), min(h, y + 2))
                for xx in range(max(0, x - 1), min(w, x + 2))
                if a[yy, xx, 3] > 0 and not m[yy, xx]
            ]
            if good:
                out[y, x, :3] = np.median(np.array(good), axis=0).astype(np.uint8)
            else:
                out[y, x, 3] = 0
        a = out
    return a, total


def recolor_cobweb(a: np.ndarray) -> tuple[np.ndarray, int]:
    r, g, b, al = (a[..., i].astype(int) for i in range(4))
    m = (al > 0) & (b > r) & (r > 140) & (g < b - 25) & (b > 190)
    a = a.copy()
    a[m, 0], a[m, 1], a[m, 2] = 168, 158, 146
    return a, int(m.sum())


def black_rows(a: np.ndarray, from_bottom: bool) -> int:
    n = 0
    rows = a[::-1] if from_bottom else a
    for row in rows:
        px = row[::4]
        if np.all(px[:, 3] > 0) and np.all(px[:, :3].sum(axis=1) < 30):
            n += 1
        else:
            break
    return n


def process(src: Path, ops: str) -> tuple[Image.Image, str]:
    im = Image.open(src).convert("RGBA")
    a = np.array(im)
    notes = []
    for op in filter(None, ops.split(";")):
        if op == "despill":
            a, n = despill(a)
            notes.append(f"despill {n}")
        elif op == "cobweb":
            a, n = recolor_cobweb(a)
            notes.append(f"cobweb {n}")
        elif op == "crop-bottom-black":
            n = black_rows(a, True)
            a = a[: a.shape[0] - n]
            notes.append(f"cắt đáy {n}")
        elif op == "crop-top":
            n = black_rows(a, False)
            a = a[n:]
            notes.append(f"cắt đỉnh {n}")
    return Image.fromarray(a), ", ".join(notes)


def entry(kind: str, im: Image.Image, once: bool) -> dict:
    w, h = im.size
    pivot = [w / 2, h - 1] if kind in ("prop", "fg") else [w / 2, h / 2]
    return {
        "category": kind,
        "px": [w, h],
        "pivot_px": pivot,
        "frames": 1,
        "fps": None,
        "sway": False,
        # "once": cạnh trái/phải lệch màu (xem review) — chỉ dựng một lần theo bề rộng, không lặp ngang.
        "tileable": "none",
        "world": [round(w / 128, 4), round(h / 128, 4)],
        **({"repeat": "never"} if once else {}),
        "source": "octopath-s01-s27-20261029",
    }


def main() -> None:
    dry = "--dry" in sys.argv
    assets_path = HD / "assets.json"
    assets = json.loads(assets_path.read_text())
    for name, folder, kind, ops in HD_ITEMS:
        once = "once" in ops
        proc = ";".join(o for o in ops.split(";") if o not in ("once",))
        im, note = process(folder / f"{name}.png", proc)
        print(f"{name:28s} {im.size[0]}x{im.size[1]} {kind:13s} {note}")
        if not dry:
            im.save(HD / f"{name}.png", optimize=True)
            assets[name] = entry(kind, im, once)
    for name in FX_ITEMS:
        im = Image.open(SRC / f"{name}.png").convert("RGBA")
        print(f"{name:28s} {im.size[0]}x{im.size[1]} battle-fx")
        if not dry:
            BATTLE.mkdir(exist_ok=True)
            im.save(BATTLE / f"{name}.png", optimize=True)
    for name in FX_OLD:
        im = Image.open(OLD / f"{name}.png").convert("RGBA")
        print(f"{name:28s} {im.size[0]}x{im.size[1]} battle-fx (P01)")
        if not dry:
            BATTLE.mkdir(exist_ok=True)
            im.save(BATTLE / f"{name}.png", optimize=True)
    for name in UI_ITEMS:
        im, note = process(SRC / f"{name}.png", "")
        print(f"{name:28s} {im.size[0]}x{im.size[1]} ui")
        if not dry:
            im.save(UI / f"{name}.png", optimize=True)
    if not dry:
        assets_path.write_text(json.dumps(assets, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
