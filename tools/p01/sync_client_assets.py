#!/usr/bin/env python3
"""Đồng bộ art cho client mới (apps/client/public) từ nguồn art HD-2D.

Chạy từ gốc repo (cần Pillow + numpy):
    python3 tools/p01/sync_client_assets.py

Kết quả:
- apps/client/public/hd2d/<id>.png (+ <id>.idle.png / <id>.run.png cho người chơi/NPC)
- apps/client/public/hd2d/assets.json: kích thước, pivot, số khung, cờ `provisional`
- apps/client/public/ui/: bộ UI HD-2D đã duyệt (HUD, trận, menu, icon) + ui.json (kích thước, 9-slice)
- apps/client/public/i18n/vi.json: tên tiếng Việt của nội dung
- apps/client/public/pets/: atlas linh thú P10 (14 loài cũ hiển thị bằng atlas P10, nợ N02)

Chỉ lấy asset `approved: true` trong manifest. Một số asset chặn 1.0.0 chưa duyệt được xử lý TẠM
từ bản owner nộp (`_intake/`) và đánh dấu `provisional: true`: client vẫn chạy, review art sau sẽ
thay bằng bản duyệt (chạy lại script).
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "apps/game-web/art-src/hd2d"
OUT = ROOT / "apps/client/public/hd2d"
PETS_SRC = ROOT / "apps/game-web/public/assets/pets"
PETS_OUT = ROOT / "apps/client/public/pets"
BATCHES = ["batch-01-octopath", "batch-02-octopath", "batch-05-octopath"]
INTAKE3 = SRC / "batch-05-octopath/_intake/don09-chang-3-5"
INTAKE10 = SRC / "batch-05-octopath/_intake/don10-v1.0.0-remaining"


def manifest_items(batch: str):
    m = json.loads((SRC / batch / "manifest.json").read_text())
    a = m.get("assets", m)
    return a if isinstance(a, list) else [dict(id=k, **v) for k, v in a.items()]


def entry(i, px, extra=None):
    e = {
        "category": i.get("category"),
        "px": px,
        "pivot_px": i.get("pivot_px") or [px[0] / 2, px[1]],
        "frames": i.get("frames") or 1,
        "fps": i.get("fps"),
        "sway": bool(i.get("sway")),
        "tileable": i.get("tileable"),
    }
    if i.get("world"):
        e["world"] = i["world"]
    if extra:
        e.update(extra)
    return e


def key_magenta(im: Image.Image) -> Image.Image:
    a = np.asarray(im.convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    bg = (r > 150) & (b > 150) & (g < 140) & (np.abs(r - b) < 90)
    rgba = np.dstack([a, np.where(bg, 0, 255)]).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def binary_alpha(im: Image.Image) -> Image.Image:
    a = np.asarray(im).copy()
    a[..., 3] = np.where(a[..., 3] >= 128, 255, 0)
    return Image.fromarray(a, "RGBA")


def bbox(im: Image.Image):
    a = np.asarray(im)[..., 3] > 0
    ys, xs = np.where(a)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def cell_sprite(fig: Image.Image, height: int = 166) -> Image.Image:
    """Đặt nhân vật vào ô 192×192, chân ở y=184, cao `height` px."""
    x0, y0, x1, y1 = bbox(fig)
    fig = fig.crop((x0, y0, x1, y1))
    s = height / fig.height
    w = max(1, round(fig.width * s))
    if w > 188:
        s = 188 / fig.width
        w = 188
    fig = binary_alpha(fig.resize((w, max(1, round(fig.height * s))), Image.LANCZOS))
    out = Image.new("RGBA", (192, 192), (0, 0, 0, 0))
    out.alpha_composite(fig, ((192 - fig.width) // 2, 184 - fig.height))
    return out


def tile512(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGB").resize((512, 512), Image.LANCZOS)
    return im.quantize(48, method=Image.Quantize.MEDIANCUT).convert("RGBA")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    assets: dict[str, dict] = {}

    # 1) Asset đã duyệt.
    for batch in BATCHES:
        for i in manifest_items(batch):
            if not i.get("approved") or i.get("category") == "portrait":
                continue
            src = SRC / batch / i["file"]
            if not src.exists():
                continue
            shutil.copyfile(src, OUT / f"{i['id']}.png")
            px = list(Image.open(src).size)
            extra = {}
            for kind in ("idle", "run"):
                strip = i.get(f"{kind}_strip")
                if strip and (SRC / batch / strip).exists():
                    shutil.copyfile(SRC / batch / strip, OUT / f"{i['id']}.{kind}.png")
                    extra[f"{kind}_frames"] = Image.open(SRC / batch / strip).size[0] // 192
            assets[i["id"]] = entry(i, px, extra)

    # 2) Tạm thời từ bản owner nộp (chưa duyệt) — đánh dấu provisional.
    prov = {"provisional": True}
    tiles = {
        "city-paving-01": INTAKE3 / "01-city-paving-01.png",
        "city-paving-02": INTAKE3 / "02-city-paving-02.png",
        "city-paving-03": INTAKE10 / "city-paving-03.png",
        "city-brick-path": INTAKE10 / "city-brick-path.png",
        "hall-floor-stone": INTAKE3 / "05-hall-floor-stone.png",
    }
    for tid, p in tiles.items():
        if p.exists() and tid not in assets:
            tile512(p).save(OUT / f"{tid}.png")
            assets[tid] = {"category": "floor", "px": [512, 512], "pivot_px": [256, 256], "frames": 1, "world": [4, 4], "tileable": "xy", **prov}

    sky = INTAKE3 / "06-city-skyline-far-transparent.png"
    if sky.exists() and "city-skyline-far" not in assets:
        im = Image.open(sky).convert("RGBA")
        x0, y0, x1, y1 = bbox(binary_alpha(im))
        im = im.crop((0, y0, im.width, y1))
        s = 480 / im.height
        im = binary_alpha(im.resize((round(im.width * s), 480), Image.LANCZOS))
        out = Image.new("RGBA", (im.width, 512), (0, 0, 0, 0))
        out.alpha_composite(im, (0, 512 - im.height))
        out.save(OUT / "city-skyline-far.png")
        assets["city-skyline-far"] = {"category": "backdrop_far", "px": [out.width, 512], "pivot_px": [out.width / 2, 256], "frames": 1,
                                      "world": [out.width / 64, 8], "tileable": "x", **prov}

    def cut(sheet: Path, boxes: dict[str, tuple[float, float, float, float]]):
        if not sheet.exists():
            return
        im = key_magenta(Image.open(sheet))
        W, H = im.size
        for nid, (fx0, fy0, fx1, fy1) in boxes.items():
            aid = f"npc-{nid}"
            if aid in assets:
                continue
            fig = im.crop((int(fx0 * W), int(fy0 * H), int(fx1 * W), int(fy1 * H)))
            cell_sprite(fig).save(OUT / f"{aid}.png")
            assets[aid] = {"category": "npc", "px": [192, 192], "pivot_px": [96, 184], "frames": 1, **prov}

    cut(INTAKE3 / "09-npc-sheet-1-mira-rowan-tuli-orsa.png",
        {"summoner_mira": (0, 0, .5, .5), "bia_skill": (.5, 0, 1, .5), "bia_free": (0, .5, .5, 1), "sq_pillar": (.5, .5, 1, 1)})
    cut(INTAKE10 / "npc-sheet-2.png",
        {"sq_skill": (0, .2, .345, .8), "sq_exchange": (.345, .2, .655, .8), "sq_warehouse": (.655, .2, 1, .8)})

    mb = INTAKE3 / "10-city-mailbox-2-states.png"
    if mb.exists():
        im = key_magenta(Image.open(mb))
        for k, (y0, y1) in {"city-mailbox": (0, .5), "city-mailbox-glow": (.5, 1)}.items():
            if k in assets:
                continue
            fig = im.crop((0, int(y0 * im.height), im.width, int(y1 * im.height)))
            x0, fy0, x1, fy1 = bbox(fig)
            fig = fig.crop((x0, fy0, x1, fy1))
            s = 180 / fig.height
            fig = binary_alpha(fig.resize((round(fig.width * s), 180), Image.LANCZOS))
            fig.save(OUT / f"{k}.png")
            assets[k] = {"category": "prop", "px": list(fig.size), "pivot_px": [fig.width / 2, fig.height], "frames": 1,
                         "world": [fig.width / 128, fig.height / 128], **prov}

    # 2b) Đồ thành phố đơn 10 (batch-12-city, cắt bằng tools/p01/cut_city_batch12.py). Chưa duyệt → provisional.
    b12 = SRC / "batch-12-city"
    if (b12 / "manifest.json").exists():
        for i in manifest_items("batch-12-city"):
            src = b12 / i["file"]
            if not src.exists() or i["id"] in assets:
                continue
            shutil.copyfile(src, OUT / f"{i['id']}.png")
            extra = {} if i.get("approved") else dict(prov)
            if i.get("run_strip") and (b12 / i["run_strip"]).exists():
                shutil.copyfile(b12 / i["run_strip"], OUT / f"{i['id']}.run.png")
                extra["run_frames"] = i.get("run_frames") or 1
            for k in ("breathe", "flutter"):
                if i.get(k):
                    extra[k] = True
            assets[i["id"]] = entry(i, list(Image.open(src).size), extra)

    (OUT / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=1) + "\n")

    # 3) Atlas linh thú.
    if PETS_SRC.exists():
        if PETS_OUT.exists():
            shutil.rmtree(PETS_OUT)
        shutil.copytree(PETS_SRC, PETS_OUT)

    # 4) Bộ UI HD-2D đã duyệt (HUD, trận, menu, icon, font số) → apps/client/public/ui.
    ui_out = ROOT / "apps/client/public/ui"
    if ui_out.exists():
        shutil.rmtree(ui_out)
    ui_out.mkdir(parents=True)
    ui: dict[str, dict] = {}
    for batch in ["batch-06-octopath", "batch-07-octopath", "batch-08-octopath", "batch-09-octopath", "batch-10-octopath"]:
        for i in manifest_items(batch):
            if not i.get("approved") or i.get("category") not in ("ui_sprite", "ui_9slice", "icon", "font"):
                continue
            src = SRC / batch / i["file"]
            if not src.exists():
                continue
            shutil.copyfile(src, ui_out / f"{i['id']}.png")
            ui[i["id"]] = {"px": list(Image.open(src).size), "slice": i.get("slice")}
    (ui_out / "ui.json").write_text(json.dumps(ui, ensure_ascii=False, indent=1) + "\n")
    print(f"ui: {len(ui)} asset → {ui_out.relative_to(ROOT)}")

    # 5) Bản dịch tên nội dung (loài, vật phẩm, kỹ năng…) sang tiếng Việt.
    vi = ROOT / "apps/game-web/public/assets/i18n/vi.json"
    if vi.exists():
        (ROOT / "apps/client/public/i18n").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(vi, ROOT / "apps/client/public/i18n/vi.json")

    n_prov = sum(1 for a in assets.values() if a.get("provisional"))
    print(f"hd2d: {len(assets)} asset ({n_prov} tạm thời) → {OUT.relative_to(ROOT)}")
    print(f"pets: {len(list(PETS_OUT.iterdir()))} file → {PETS_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
