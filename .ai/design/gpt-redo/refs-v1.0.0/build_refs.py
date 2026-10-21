#!/usr/bin/env python3
"""Dựng bộ ảnh tham chiếu cho đơn GPT 09 (v1.0.0 + art còn dở).

Chạy từ gốc repo:  python3 .ai/design/gpt-redo/refs-v1.0.0/build_refs.py [MAP_IMAGES_DIR]
MAP_IMAGES_DIR mặc định ~/Downloads/Phimond-P12-Review/map-images (ảnh map gốc, chỉ đọc).
Chỉ ghép/phóng to ảnh có sẵn (nearest), không sinh nội dung mới.
"""
import os, sys, json, glob
from PIL import Image, ImageDraw

ROOT = os.getcwd()
OUT = os.path.join(ROOT, ".ai/design/gpt-redo/refs-v1.0.0")
MI = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Downloads/Phimond-P12-Review/map-images")
REF = "apps/game-client/assets/reference"
HD = "apps/game-web/art-src/hd2d"
SP = "tools/build-web-assets/source/sprites"
BG = (28, 32, 42, 255)

def up(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)

def sheet(items, path, cols=4, cell=None, k=1, label=True):
    """items: list of (label, PIL.Image)."""
    ims = [(l, up(i.convert("RGBA"), k)) for l, i in items]
    cw = cell or max(i.width for _, i in ims) + 24
    ch = max(i.height for _, i in ims) + (40 if label else 24)
    rows = (len(ims) + cols - 1) // cols
    s = Image.new("RGBA", (cw * min(cols, len(ims)), ch * rows), BG)
    d = ImageDraw.Draw(s)
    for n, (l, i) in enumerate(ims):
        x, y = (n % cols) * cw, (n // cols) * ch
        if i.width > cw - 12:
            sc = (cw - 12) / i.width
            i = i.resize((int(i.width * sc), max(1, int(i.height * sc))), Image.NEAREST)
        s.alpha_composite(i, (x + (cw - i.width) // 2, y + 8))
        if label:
            d.text((x + 6, y + ch - 26), l, fill=(230, 230, 230, 255))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    s.save(path)
    return path

def strip(folder, k=4):
    fr = [Image.open(f).convert("RGBA") for f in sorted(glob.glob(folder + "/*.png"))]
    w = max(f.width for f in fr); h = max(f.height for f in fr)
    s = Image.new("RGBA", (len(fr) * (w + 4), h), (0, 0, 0, 0))
    for n, f in enumerate(fr):
        s.alpha_composite(f, (n * (w + 4) + (w - f.width) // 2, h - f.height))  # canh đáy
    return up(s, k), len(fr)

def hd(batch, aid):
    return Image.open(f"{HD}/{batch}/{aid}/final.png")

def mapimg(name, maxw=2400):
    p = os.path.join(MI, name + ".png")
    if not os.path.exists(p):
        p = f"{REF}/rooms/{ {'city_square':'severa','emerald_forest_main_woods':'forest','treasure_beach_fishermen_beach':'beach','city_farm':'ranch','city_deathmatch_arena':'arena'}.get(name, name)}.png"
    im = Image.open(p).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    return im

def save_map(name, sub):
    p = f"{OUT}/{sub}/orig-map-{name}.png"
    os.makedirs(os.path.dirname(p), exist_ok=True)
    mapimg(name).save(p)
    return p

def tile2x2(im, n=2):
    im = im.convert("RGBA").resize((256, 256), Image.NEAREST)
    s = Image.new("RGBA", (256 * n, 256 * n))
    for x in range(n):
        for y in range(n):
            s.paste(im, (x * 256, y * 256))
    return s

made = []
# ---------- 01 nhân vật chính ----------
for g, gid in (("Boy", "male"), ("Girl", "female")):
    for a in ("Idle", "Run"):
        s, n = strip(f"{REF}/actors/{g}/{a}")
        p = f"{OUT}/01-player/orig-{gid}-{a.lower()}-{n}f-x4.png"; os.makedirs(os.path.dirname(p), exist_ok=True); s.save(p); made.append(p)
made.append(sheet([("LOCK player-male (da duyet)", hd("batch-05-octopath", "player-male")),
                   ("LOCK player-female (da duyet)", hd("batch-05-octopath", "player-female")),
                   ("style: npc-forest_guide", hd("batch-05-octopath", "npc-forest_guide")),
                   ("style: npc-gate_captain", hd("batch-05-octopath", "npc-gate_captain"))],
                  f"{OUT}/01-player/design-lock-and-style.png", cols=4, k=2))
made.append(sheet([("player-male", hd("batch-05-octopath", "player-male")),
                   ("bush-01 (1.06u cao)", hd("batch-01-octopath", "bush-01")),
                   ("barrel", hd("batch-02-octopath", "barrel")),
                   ("streetlamp-unlit", hd("batch-02-octopath", "streetlamp-unlit"))],
                  f"{OUT}/01-player/scale-compare-128px-per-unit.png", cols=4))
made.append(save_map("emerald_forest_main_woods", "01-player"))

# ---------- 02 sàn lát thành ----------
for m in ("city_square", "city_palace_gate", "summoning_hall_main_hall"):
    made.append(save_map(m, "02-city-floor"))
q = sorted(glob.glob(f"{SP}/level3_QTTP/*.png"))[1:]
made.append(sheet([(os.path.basename(f)[-7:-4], Image.open(f)) for f in q], f"{OUT}/02-city-floor/orig-QTTP-sprites-x3.png", cols=8, k=3))
bad = ["city-paving-01", "city-paving-02", "city-paving-03", "city-brick-path", "hall-floor-stone"]
made.append(sheet([(f"REJECT {b} (ghep 2x2)", tile2x2(hd("batch-02-octopath", b))) for b in bad], f"{OUT}/02-city-floor/rejected-seams-2x2.png", cols=3))
made.append(sheet([(f"VAT LIEU GIU {b}", hd("batch-02-octopath", b)) for b in bad], f"{OUT}/02-city-floor/material-to-keep.png", cols=5))
made.append(sheet([("STYLE OK grass-floor-01", tile2x2(hd("batch-01-octopath", "grass-floor-01"))),
                   ("STYLE OK hall-floor-wood", tile2x2(hd("batch-02-octopath", "hall-floor-wood"))),
                   ("STYLE OK dirt-floor-01", tile2x2(hd("batch-01-octopath", "dirt-floor-01")))],
                  f"{OUT}/02-city-floor/style-seamless-ok.png", cols=3))

# ---------- 03 nền xa thành ----------
for m in ("city_square", "city_palace_gate", "city_royal_palace", "city_market"):
    made.append(save_map(m, "03-city-skyline"))
made.append(sheet([(i, hd("batch-02-octopath", i)) for i in ("city-facade-guild", "city-facade-shop", "city-facade-artisan", "city-facade-townhouse", "city-roof-module", "palace-gate", "palace-tower", "palace-wall-section", "city-tree-01")],
                  f"{OUT}/03-city-skyline/style-city-kit.png", cols=5))
made.append(sheet([("STYLE OK forest-wall-far (far 64px/u)", hd("batch-01-octopath", "forest-wall-far")),
                   ("STYLE OK sea-islands-far", hd("batch-03-octopath", "sea-islands-far"))], f"{OUT}/03-city-skyline/style-far-strip.png", cols=1))
made.append(sheet([("REJECT city-skyline-far (Gemini: dai thua, mau mem)", hd("batch-02-octopath", "city-skyline-far"))], f"{OUT}/03-city-skyline/rejected-gemini.png", cols=1))

# ---------- 04 NPC ----------
made.append(save_map("summoning_hall_main_hall", "04-npc"))
on = sorted(glob.glob(f"{REF}/npcs/*.png"))
made.append(sheet([("orig " + os.path.basename(f)[:-4], Image.open(f)) for f in on], f"{OUT}/04-npc/orig-apk-npcs-x4.png", cols=5, k=4))
roster = json.load(open(".ai/plan/phases/P12-world/stage4/P12-S4-npc-roster.json"))
roster = roster if isinstance(roster, list) else roster.get("npcs", roster)
A = {"summoning_hall_main_hall", "emerald_forest_main_woods", "emerald_forest_deep_woods", "city_palace_gate", "city_square"}
dec = json.load(open(".ai/design/hd2d-approval-20261021.json"))
redo5 = set(dec["redo"]["batch-05-octopath"])
ok = [n for n in roster if n["map_id"] in A and os.path.exists(f"{HD}/batch-05-octopath/npc-{n['id']}/final.png") and "npc-" + n["id"] not in redo5]
made.append(sheet([("DA CO " + n["id"], hd("batch-05-octopath", "npc-" + n["id"])) for n in ok], f"{OUT}/04-npc/approved-wave-A-must-differ.png", cols=7))
allok = [d[4:] for d in sorted(os.listdir(f"{HD}/batch-05-octopath")) if d.startswith("npc-") and d not in redo5 and os.path.exists(f"{HD}/batch-05-octopath/{d}/final.png")]
made.append(sheet([(i, hd("batch-05-octopath", "npc-" + i)) for i in allok], f"{OUT}/04-npc/all-approved-npcs-must-differ.png", cols=12, k=1))
made.append(sheet([(i, hd("batch-02-octopath", i)) for i in ("well", "streetlamp-unlit", "bench", "city-carved-pillar", "hall-quest-board")], f"{OUT}/04-npc/mailbox-material-ref.png", cols=5))

# ---------- 05 phần còn lại (sau v1.0.0) ----------
for m in ("city_farm", "city_deathmatch_arena", "city_royal_palace", "treasure_beach_fishermen_beach", "treasure_beach_east_beach", "treasure_beach_deep_sea", "treasure_beach_prosperity_island", "emerald_forest_deep_woods"):
    made.append(save_map(m, "05-later"))
rj = [("batch-02-octopath", i) for i in ("farm-tilled-01", "farm-tilled-02", "arena-floor", "farm-dirt-path-strip")] + [("batch-03-octopath", i) for i in ("sand-dry-warm", "sand-seagrass")]
made.append(sheet([(f"REJECT {i} 2x2", tile2x2(hd(b, i))) for b, i in rj if "strip" not in i], f"{OUT}/05-later/rejected-tiles-2x2.png", cols=3))
made.append(sheet([(f"REJECT {i}", hd(b, i)) for b, i in [("batch-02-octopath", "arena-stands-far"), ("batch-02-octopath", "farm-hills-far"), ("batch-02-octopath", "royal-carpet-runner"), ("batch-03-octopath", "deep-sea-floor-tile"), ("batch-01-octopath", "deep-woods-giant-tree"), ("batch-03-octopath", "coastal-cliff-mid"), ("batch-02-octopath", "farm-dirt-path-strip"), ("batch-10-octopath", "loading-bar-fill")]], f"{OUT}/05-later/rejected-other.png", cols=4))
for d in ("level3_NongTrai", "level3_DauTruong", "level5_BaiBien", "level4_rungsau"):
    fs = sorted(glob.glob(f"{SP}/{d}/*.png"))[1:]
    made.append(sheet([(os.path.basename(f)[-7:-4], Image.open(f)) for f in fs], f"{OUT}/05-later/orig-{d}-sprites-x3.png", cols=8, k=3))
made.append(sheet([(f"REJECT {i}", hd("batch-09-octopath", i)) for i in ("rank33", "rank41", "rank53", "rank54")] + [(f"OK {i}", hd("batch-09-octopath", i)) for i in ("rank32", "rank52")], f"{OUT}/05-later/ranks.png", cols=6, k=1))
made.append(sheet([("frame (da duyet)", hd("batch-10-octopath", "loading-bar-frame")), ("REJECT fill", hd("batch-10-octopath", "loading-bar-fill")), ("loading-bg", hd("batch-10-octopath", "loading-bg"))], f"{OUT}/05-later/loading.png", cols=3))

print(len(made), "files")
