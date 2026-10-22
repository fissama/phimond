#!/usr/bin/env python3
"""Cắt bộ artwork phát hành P01 (p01-release-art-20261022/sources) thành asset batch-13-release.

Chạy từ gốc repo: python3 tools/p01/cut_release_art.py [--debug]

Đầu vào (GPT vẽ bằng image_gen, KHÔNG ghép/kéo méo bằng code):
- male-walk-side / female-walk-side / male-walk-down: sheet 3×2 ô 512, 6 pha của MỘT chu kỳ đi.
- terrain-edges: 6 mảnh chuyển tiếp đất↔cỏ (4 rìa + 2 đầu cụt có vệt bánh xe).
- forest-boundary: bộ viền rừng theo lớp (tán xa, thân giữa, bụi trước, góc, bờ gần camera, cổng).

Xử lý cơ học duy nhất: tách nền magenta, đưa vào ô 192×192 (người) với tỉ lệ đồng nhất theo sheet, căn chân và căn thân,
giảm ≤64 màu, alpha nhị phân. Không sửa hình. Mọi asset approved=false tới khi kiểm trong cảnh thật.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cut_city_batch12 as c  # noqa: E402  (dùng lại key/despill/finish/tight/scale_to)

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "apps/game-web/art-src/hd2d/p01-release-art-20261022/sources"
OUT = ROOT / "apps/game-web/art-src/hd2d/batch-13-release"
c.B = OUT  # c.save() ghi vào batch mới
DEBUG = "--debug" in sys.argv
PLAYER_H = 166  # chuẩn người chơi đã duyệt: cao ~168 px, chân y=184
manifest: list[dict] = []


def grid_cells(path: Path, cols: int = 3, rows: int = 2) -> list[Image.Image]:
    rgba = c.key(path)
    H, W = rgba.shape[:2]
    cw, ch = W // cols, H // rows
    out = []
    for r in range(rows):
        for q in range(cols):
            cell = rgba[r * ch : (r + 1) * ch, q * cw : (q + 1) * cw].copy()
            out.append(c.despill(Image.fromarray(cell, "RGBA"), 60))
    return out


def torso_x(im: Image.Image) -> float:
    """Tâm ngang của thân trên (15–55% chiều cao): ổn định hơn bbox khi chân dang rộng."""
    a = np.asarray(im)[..., 3] >= 128
    ys, xs = np.where(a)
    y0, y1 = ys.min(), ys.max()
    h = y1 - y0
    band = a[y0 + int(h * 0.15) : y0 + int(h * 0.55)]
    bx = np.where(band.any(0))[0]
    return (bx.min() + bx.max() + 1) / 2


def walk_strip(frames: list[Image.Image]) -> Image.Image:
    """6 pha → dải 6 ô 192: cùng tỉ lệ cho cả sheet (theo chiều cao trung vị), đáy chân y=184, thân căn giữa x=96."""
    frames = [c.tight(f) for f in frames]
    hs = sorted(f.height for f in frames)
    s = PLAYER_H / hs[len(hs) // 2]
    out = Image.new("RGBA", (192 * len(frames), 192), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        tx = torso_x(f)
        g = c.scale_to(f, s)
        gx = tx * s
        cell = Image.new("RGBA", (192, 192), (0, 0, 0, 0))
        px, py = int(round(96 - gx)), 184 - g.height
        cell.alpha_composite(g, (max(px, 0), max(py, 0)), (max(-px, 0), max(-py, 0)))
        out.alpha_composite(cell, (i * 192, 0))
    return c.finish(out, 48)


def leg_diff(strip: Image.Image) -> list[int]:
    """% khác biệt vùng chân (60px dưới) giữa khung 0 và các khung khác — chứng minh chân đổi chỗ thật."""
    a = np.asarray(strip)[..., 3] >= 128
    n = a.shape[1] // 192
    legs = [a[124:185, i * 192 : (i + 1) * 192] for i in range(n)]
    return [int(100 * (legs[0] ^ legs[i]).sum() / max(1, legs[0].sum())) for i in range(1, n)]


def player(aid: str, side: Path | None, down: Path | None, up: Path | None = None) -> None:
    d = OUT / aid
    d.mkdir(parents=True, exist_ok=True)
    e: dict = {"id": aid, "override": True, "category": "player", "approved": False, "px": [192, 192], "pivot_px": [96, 184]}
    for kind, p, key in (("run", side, "run_strip"), ("run-down", down, "run_down_strip"), ("run-up", up, "run_up_strip")):
        if p is None or not p.exists():
            continue
        st = walk_strip(grid_cells(p))
        st.save(d / f"{kind}.png")
        e[key] = f"{aid}/{kind}.png"
        e[key.replace("_strip", "_frames")] = 6
        print(f"  {aid} {kind}: leg diff% vs f0 {leg_diff(st)}")
    manifest.append(e)


def terrain() -> None:
    p = SRC / "terrain-edges-raw-01.png"
    if not p.exists():
        return
    names = ["path-fringe-gn", "path-fringe-gs", "path-fringe-gw", "path-fringe-ge", "path-cap-n", "path-cap-s"]
    for aid, im in zip(names, grid_cells(p)):
        im = c.finish(c.tight(im), 64)
        c.save(aid, im, "ground_patch")
        manifest.append({"id": aid, "file": f"{aid}/final.png", "category": "ground_patch", "px": list(im.size),
                         "pivot_px": [im.width / 2, im.height / 2], "world": [im.width / 128, im.height / 128], "approved": False})


def forest() -> None:
    p = SRC / "forest-boundary-raw-01.png"
    if not p.exists():
        return
    names = ["forest-far-canopy", "forest-mid-trunks", "forest-fg-bank", "forest-corner", "forest-cam-bank", "forest-portal-arch"]
    for aid, im in zip(names, grid_cells(p)):
        im = c.finish(c.tight(im), 64)
        c.save(aid, im, "prop")
        manifest.append({"id": aid, "file": f"{aid}/final.png", "category": "prop", "px": list(im.size),
                         "pivot_px": [im.width / 2, im.height], "world": [im.width / 128, im.height / 128], "approved": False})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("người chơi")
    player("player-male", SRC / "male-walk-side-raw-01.png", SRC / "male-walk-down-raw-01.png")
    player("player-female", SRC / "female-walk-side-raw-01.png", None)
    terrain()
    forest()
    (OUT / "manifest.json").write_text(json.dumps({"assets": manifest}, ensure_ascii=False, indent=1) + "\n")
    print(f"{len(manifest)} mục → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
