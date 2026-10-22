#!/usr/bin/env python3
"""Cắt asset thành phố (đơn 10, batch-12-city) từ ảnh owner nộp (ChatGPT web) → final.png + manifest.

Chạy từ gốc repo (cần Pillow + numpy + scipy):
    python3 tools/p01/cut_city_batch12.py          # cắt + ghi manifest + contact-sheet
    python3 tools/p01/cut_city_batch12.py --debug  # in danh sách vùng tìm được trên mỗi sheet

Nguồn: apps/game-web/art-src/hd2d/batch-12-city/_intake/don10-web-r{1,2,3}/
Kết quả: apps/game-web/art-src/hd2d/batch-12-city/<id>/final.png (và <id>/run.png cho người đi đường),
manifest.json (approved=false → client dùng với cờ provisional tới khi owner duyệt), contact-sheet.png.

Quy ước: 128 px = 1 đơn vị world. Nền magenta khử thành alpha nhị phân, giảm còn ≤ 64 màu.
Khung động: các tư thế đặt ngang trong một dải, mọi khung cùng tỉ lệ, căn theo `anchor`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

ROOT = Path(__file__).resolve().parents[2]
B = ROOT / "apps/game-web/art-src/hd2d/batch-12-city"
R1, R2, R3 = B / "_intake/don10-web-r1", B / "_intake/don10-web-r2", B / "_intake/don10-web-r3"
DEBUG = "--debug" in sys.argv


def key(path: Path) -> np.ndarray:
    """RGBA: nền magenta (và viền hồng pha nền) → trong suốt."""
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    bg = (r > 150) & (b > 150) & (g < 140) & (np.abs(r - b) < 90)
    # Viền/hạt pha hồng: kề nền và có sắc magenta rõ.
    pinkish = (r - g > 70) & (b - g > 70) & (np.abs(r - b) < 70)
    near = ndi.binary_dilation(bg, iterations=2)
    bg |= pinkish & near
    bg = ndi.binary_opening(~bg, iterations=1) == 0  # bỏ hạt lẻ 1 px
    alpha = np.where(bg, 0, 255)
    return np.dstack([a, alpha]).astype(np.uint8)


def regions(rgba: np.ndarray, grow: int = 6, min_area: int = 3000, rows: int = 2):
    """Các vùng vật thể, sắp theo hàng rồi theo cột."""
    fg = rgba[..., 3] > 0
    lab, n = ndi.label(ndi.binary_dilation(fg, iterations=grow))
    out = []
    for i, s in enumerate(ndi.find_objects(lab)):
        if s is None:
            continue
        m = (lab[s] == i + 1) & fg[s]
        if m.sum() < min_area:
            continue
        out.append((s, m))
    H = rgba.shape[0]
    # Lưới tối đa 2 hàng: hàng theo tâm dọc so với nửa ảnh, rồi trái → phải.
    out.sort(key=lambda o: (rows > 1 and (o[0][0].start + o[0][0].stop) / 2 > H / 2, o[0][1].start))
    return out


def crop(rgba: np.ndarray, reg) -> Image.Image:
    s, m = reg
    c = rgba[s].copy()
    c[..., 3] = np.where(m, c[..., 3], 0)
    return Image.fromarray(c, "RGBA")


def despill(im: Image.Image, t: int = 45) -> Image.Image:
    """Decal có hạt phấn/bụi pha nền: bỏ mọi điểm còn sắc magenta (r, b cao hơn g rõ)."""
    a = np.asarray(im).copy()
    r, g, b = (a[..., i].astype(int) for i in range(3))
    pink = (r - g > t) & (b - g > t)
    a[..., 3] = np.where(pink, 0, a[..., 3])
    # Phấn sáng pha hồng → trắng ngà.
    tint = (r - g > 6) & (b - g > 6) & (g > 140)
    v = ((r + g + b) / 3).astype(int)
    for i, k in enumerate((1.0, 0.98, 0.92)):
        a[..., i] = np.where(tint, np.clip(v * k, 0, 255), a[..., i])
    return Image.fromarray(a, "RGBA")


def finish(im: Image.Image, colors: int = 64) -> Image.Image:
    a = np.asarray(im).copy()
    alpha = np.where(a[..., 3] >= 128, 255, 0).astype(np.uint8)
    rgb = Image.fromarray(a[..., :3]).quantize(colors, method=Image.Quantize.MEDIANCUT).convert("RGB")
    out = np.dstack([np.asarray(rgb), alpha])
    out[alpha == 0, :3] = 0
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def tight(im: Image.Image) -> Image.Image:
    bb = im.getchannel("A").point(lambda v: 255 if v >= 128 else 0).getbbox()
    return im.crop(bb) if bb else im


def scale_to(im: Image.Image, s: float) -> Image.Image:
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)


manifest: list[dict] = []
sheets_debug: list[tuple[str, np.ndarray, list]] = []


def save(aid: str, im: Image.Image, category: str, extra: dict | None = None, name: str = "final.png") -> None:
    d = B / aid
    d.mkdir(parents=True, exist_ok=True)
    im.save(d / name)


def add_static(aid: str, im: Image.Image, height_px: int, category: str = "prop", **kw) -> None:
    im = tight(im)
    im = finish(tight(scale_to(im, height_px / im.height)))
    save(aid, im, category)
    e = {"id": aid, "file": f"{aid}/final.png", "category": category, "px": list(im.size),
         "pivot_px": [im.width / 2, im.height], "world": [im.width / 128, im.height / 128], "approved": False}
    e.update(kw)
    manifest.append(e)


def strip(frames: list[Image.Image], height_px: int, anchor: str = "base") -> tuple[Image.Image, int]:
    """Dải khung ngang: cùng tỉ lệ (theo khung cao nhất), căn đáy, căn ngang theo anchor."""
    frames = [tight(f) for f in frames]
    s = height_px / max(f.height for f in frames)
    frames = [scale_to(f, s) for f in frames]

    def ax(f: Image.Image) -> float:
        a = np.asarray(f)[..., 3] >= 128
        h = a.shape[0]
        rows = {"base": a[int(h * 0.88):], "top": a[: int(h * 0.3)], "bbox": a}[anchor]
        xs = np.where(rows.any(0))[0]
        return (xs.min() + xs.max() + 1) / 2 if len(xs) else f.width / 2

    anchors = [ax(f) for f in frames]
    left = max(anchors)
    right = max(f.width - a for f, a in zip(frames, anchors))
    fw = int(np.ceil(left + right)) + 2
    fh = max(f.height for f in frames)
    out = Image.new("RGBA", (fw * len(frames), fh), (0, 0, 0, 0))
    for i, (f, a) in enumerate(zip(frames, anchors)):
        out.alpha_composite(f, (i * fw + int(round(left - a)) + 1, fh - f.height))
    return finish(out), fw


def add_anim(aid: str, frames: list[Image.Image], height_px: int, fps: float, anchor: str = "base", category: str = "prop", order: list[int] | None = None, **kw) -> None:
    if order:
        frames = [frames[i] for i in order]
    im, fw = strip(frames, height_px, anchor)
    save(aid, im, category)
    e = {"id": aid, "file": f"{aid}/final.png", "category": category, "px": list(im.size), "frames": len(frames), "fps": fps,
         "pivot_px": [fw / 2, im.height], "world": [fw / 128, im.height / 128], "approved": False}
    e.update(kw)
    manifest.append(e)


def cell192(fig: Image.Image, s: float) -> Image.Image:
    fig = finish(scale_to(tight(fig), s))
    out = Image.new("RGBA", (192, 192), (0, 0, 0, 0))
    out.alpha_composite(fig, ((192 - fig.width) // 2, 184 - fig.height))
    return out


def add_walker(aid: str, poses: list[Image.Image], height_px: int, run: list[int]) -> None:
    """Người đi đường: final.png = tư thế đứng (ô 192), run.png = các tư thế bước (ô 192/khung)."""
    poses = [tight(p) for p in poses]
    s = height_px / poses[0].height
    if max(p.width for p in poses) * s > 186:
        s = 186 / max(p.width for p in poses)
    still = cell192(poses[0], s)
    save(aid, still, "walker")
    frames = [cell192(poses[i], s) for i in run]
    rs = Image.new("RGBA", (192 * len(frames), 192), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        rs.alpha_composite(f, (i * 192, 0))
    save(aid, rs, "walker", name="run.png")
    manifest.append({"id": aid, "file": f"{aid}/final.png", "run_strip": f"{aid}/run.png", "category": "walker", "px": [192, 192],
                     "pivot_px": [96, 184], "frames": 1, "run_frames": len(frames), "approved": False})


def sheet(path: Path, expect: int, grow: int = 6, min_area: int = 3000, rows: int = 1):
    rgba = key(path)
    regs = regions(rgba, grow, min_area, rows)
    if DEBUG:
        print(path.name, len(regs), [(r[0][1].start, r[0][0].start, r[0][1].stop - r[0][1].start, r[0][0].stop - r[0][0].start) for r in regs])
    if len(regs) != expect:
        raise SystemExit(f"{path.name}: tìm thấy {len(regs)} vùng, cần {expect} (chạy --debug để xem)")
    sheets_debug.append((path.name, rgba, regs))
    return [crop(rgba, r) for r in regs]


def main() -> None:
    # --- Mặt tiền nhà (tĩnh). Cao ~516 px như kit đã duyệt; tháp chuông cao hơn.
    inn, bakery, exchange = sheet(R1 / "sheet-02a-facades.png", 3)
    add_static("city-facade-inn", inn, 516, "backdrop_mid")
    add_static("city-facade-bakery", bakery, 480, "backdrop_mid")
    add_static("city-facade-exchange", exchange, 516, "backdrop_mid")
    warehouse, belltower, corner = sheet(R1 / "sheet-02b-facades.png", 3)
    add_static("city-facade-warehouse", warehouse, 500, "backdrop_mid")
    add_static("city-facade-belltower", belltower, 600, "backdrop_mid")
    add_static("city-facade-corner", corner, 540, "backdrop_mid")

    # --- Đồ phố bộ 2 (sheet 3; bồn sư tử dùng bản động vòng 3).
    sign, bunting, sacks, cart, _fountain_static, topiary = sheet(R1 / "sheet-03-props.png", 6, rows=2)
    add_static("city-hanging-sign", sign, 280, sway=True)
    add_static("city-bunting", bunting, 300, sway=True)
    add_static("city-sacks", sacks, 150)
    add_static("city-vendor-cart", cart, 230)
    add_static("city-topiary", topiary, 250, sway=True)

    # --- Mảnh nối giữa các nhà.
    alley, pipe, wallbox, fence = sheet(R1 / "sheet-06-connectors.png", 4)
    add_static("city-alley-arch", alley, 470, "backdrop_mid")
    add_static("city-pillar-drainpipe", pipe, 470, "backdrop_mid")
    add_static("city-wall-flowerbox", wallbox, 380, "backdrop_mid")
    add_static("city-iron-fence", fence, 220)

    # --- Dải mái lớp giữa (lặp ngang).
    (roof,) = sheet(R1 / "sheet-07-roofline.png", 1)
    roof = tight(roof)
    # Hai đầu chạm mép ảnh; cắt bỏ 2% mỗi đầu cho gọn mép lặp.
    cut = int(roof.width * 0.02)
    roof = roof.crop((cut, 0, roof.width - cut, roof.height))
    add_static("city-roofline-mid", roof, 230, "backdrop_mid", tileable="x")

    # --- Bộ Hoàng Môn v2 (cột cờ dùng bản động vòng 3).
    booth, planter, _flag_static, wall, lion_r, lion_l = sheet(R2 / "sheet-08-palace-v2.png", 6, rows=2)
    add_static("palace-guard-booth", booth, 340)
    add_static("palace-long-planter", planter, 150)
    add_static("palace-crenel-wall", wall, 410, "backdrop_mid")
    add_static("palace-lion-r", lion_r, 250)
    add_static("palace-lion-l", lion_l, 250)

    # --- Động vật tĩnh (vòng 1): chó, bướm, quạ — engine làm động nhẹ.
    animals = sheet(R1 / "sheet-05-animals.png", 6, grow=40, rows=2)
    _pigeons, _pigeon_fly, _cat, dog, butterflies, crow = animals
    add_static("animal-dog", dog, 80, breathe=True)
    add_static("animal-butterflies", butterflies, 64, flutter=True)
    add_static("animal-crow", crow, 72)

    # --- Khung động vòng 3.
    pg = sheet(R3 / "lan08-pigeon.png", 4)
    add_anim("animal-pigeon-peck", pg[0:2], 58, 2.5, "base")
    add_anim("animal-pigeon-fly", pg[2:4], 70, 8, "bbox")
    cat = sheet(R3 / "lan09-cat.png", 3)
    add_anim("animal-cat", cat, 96, 1.5, "top", order=[0, 1, 2, 1])
    flag = sheet(R3 / "lan10-flag.png", 3)
    add_anim("palace-flagpole", flag, 440, 3, "base", order=[0, 1, 2, 1])
    ftn = sheet(R3 / "lan11-fountain.png", 3)
    add_anim("city-lion-fountain", ftn, 230, 5, "base")

    # --- Decal mặt đất (nằm phẳng). Vũng nước có giọt rời → gom vùng rộng.
    dec = sheet(R3 / "lan01-decal.png", 6, grow=40, min_area=1500, rows=2)
    for aid, im, size in zip(["decal-cracks", "decal-drain", "decal-puddle", "decal-petals", "decal-hopscotch", "decal-ruts"], dec,
                             [190, 90, 200, 180, 230, 220]):
        im = tight(despill(im))
        s = size / max(im.size)
        im = finish(tight(despill(scale_to(im, s), 22)), 48)
        save(aid, im, "decal")
        manifest.append({"id": aid, "file": f"{aid}/final.png", "category": "decal", "px": list(im.size),
                         "pivot_px": [im.width / 2, im.height / 2], "world": [im.width / 128, im.height / 128], "approved": False})

    # --- Người đi đường (vòng 3: đứng + 2 tư thế bước, quay phải).
    walk = {"boy": (128, [1, 2]), "girl": (124, [1, 2]), "elder": (158, [1, 2]), "baker": (164, [1, 1]),
            "guard": (176, [1, 2]), "traveller": (170, [1, 2])}
    for i, (n, (h, run)) in enumerate(walk.items()):
        poses = sheet(R3 / f"lan{i + 2:02d}-walk-{n}.png", 3)
        add_walker(f"walker-{n}", poses, h, run)

    (B / "manifest.json").write_text(json.dumps({"batch": "batch-12-city", "source": "đơn 10 (ChatGPT web) vòng 1–3",
                                                 "assets": manifest}, ensure_ascii=False, indent=1) + "\n")
    contact()
    print(f"batch-12-city: {len(manifest)} asset")


def contact() -> None:
    tiles = []
    for e in manifest:
        im = Image.open(B / e["file"]).convert("RGBA")
        if e.get("run_strip"):
            r = Image.open(B / e["run_strip"]).convert("RGBA")
            both = Image.new("RGBA", (im.width + r.width, 192), (0, 0, 0, 0))
            both.alpha_composite(im, (0, 0))
            both.alpha_composite(r, (im.width, 0))
            im = both
        im.thumbnail((360, 260))
        tiles.append((e["id"], im))
    cols, cw, ch = 5, 372, 290
    rows = (len(tiles) + cols - 1) // cols
    out = Image.new("RGB", (cols * cw, rows * ch), (58, 62, 70))
    d = ImageDraw.Draw(out)
    for i, (n, im) in enumerate(tiles):
        x, y = (i % cols) * cw, (i // cols) * ch
        d.rectangle([x + 4, y + 4, x + cw - 4, y + ch - 4], fill=(96, 100, 108))
        out.paste(im, (x + (cw - im.width) // 2, y + 8 + (260 - im.height)), im)
        d.text((x + 8, y + ch - 20), n, fill=(255, 255, 255))
    out.save(B / "contact-sheet.png")


if __name__ == "__main__":
    main()
