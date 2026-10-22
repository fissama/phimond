#!/usr/bin/env python3
"""Dựng 5 map Đợt A (P01 v1.0.0) thành data/maps/p01/<id>.json theo ADR-P01-01.

Chạy: python3 tools/p01/build_maps.py        (ghi file)
      python3 tools/p01/build_maps.py --check (chỉ kiểm, không ghi)

Bố cục là dữ liệu chuẩn duy nhất cho va chạm (R02). Ký tự `layout`:
  Đi được : . cỏ   , đất   : đá lát   = sàn gỗ   _ sàn đá   + gạch
            f hoa  g cỏ cao  m nấm   (trang trí đi xuyên được)
  Chặn    : # tường/rìa   T cây lớn   t cây nhỏ   b bụi   r đá   ~ nước
            H mặt tiền nhà (neo đáy-giữa)   F đài phun   C cột   w giếng   x thùng/hòm
            L đèn   B ghế   S tượng   Q bảng nhiệm vụ   K kệ sách   O trụ dịch chuyển
            1 2 3 bệ triệu hồi   s cửa hàng (quầy)
NPC luôn chặn ô đứng của mình (cộng thêm khi tính `walk`).
Rừng sinh bằng RNG cố định (seed theo map) để kết quả ổn định giữa các lần chạy.
"""
from __future__ import annotations

import json
import random
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/maps/p01"

WALK = set(".,:=_+fgm")


# ---------------------------------------------------------------- lưới tiện ích
class Grid:
    def __init__(self, w: int, h: int, fill: str):
        self.w, self.h = w, h
        self.c = [[fill] * w for _ in range(h)]

    def get(self, x, y):
        return self.c[y][x] if 0 <= x < self.w and 0 <= y < self.h else "#"

    def set(self, x, y, ch):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.c[y][x] = ch

    def rect(self, x, y, w, h, ch):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, ch)

    def rows(self):
        return ["".join(r) for r in self.c]


def from_rows(rows: list[str]) -> Grid:
    w = len(rows[0])
    for i, r in enumerate(rows):
        assert len(r) == w, f"hàng {i} dài {len(r)} != {w}: {r!r}"
    g = Grid(w, len(rows), "#")
    g.c = [list(r) for r in rows]
    return g


def carve_path(g: Grid, pts, ch=",", width=2):
    """Đường đất nối các điểm theo đoạn ngang/dọc."""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        x, y = x0, y0
        while (x, y) != (x1, y1):
            for d in range(width):
                g.set(x, y + d, ch) if x != x1 else g.set(x + d, y, ch)
            if x != x1:
                x += 1 if x1 > x else -1
            else:
                y += 1 if y1 > y else -1
        for d in range(width):
            g.set(x1 + d, y1, ch)
            g.set(x1, y1 + d, ch)


def scatter(g: Grid, rng, chars, count, area, spacing=2, on="."):
    x0, y0, w, h = area
    placed, tries = 0, 0
    while placed < count and tries < count * 60:
        tries += 1
        x, y = rng.randrange(x0, x0 + w), rng.randrange(y0, y0 + h)
        if g.get(x, y) != on:
            continue
        if any(g.get(x + dx, y + dy) not in WALK for dx in range(-spacing, spacing + 1) for dy in range(-spacing, spacing + 1) if (dx, dy) != (0, 0) and abs(dx) + abs(dy) <= spacing):
            continue
        g.set(x, y, rng.choice(chars))
        placed += 1


def forest_border(g: Grid, rng, depth=2):
    for y in range(g.h):
        for x in range(g.w):
            edge = min(x, y, g.w - 1 - x, g.h - 1 - y)
            if edge < depth:
                g.set(x, y, "#")
            elif edge == depth and rng.random() < 0.35:
                g.set(x, y, rng.choice("Ttb"))


# ---------------------------------------------------------------- 5 map
# Kích thước theo game gốc (P01 review 2026-10-22): map gốc là dải ngang ~20–28 đơn vị, vùng đi sâu ~4–6.
# Bản HD-2D rộng hơn gốc ~20–30% và sâu 7–9 ô (camera nghiêng cần chiều sâu), cổng ở hai mép trái/phải.

def strip_forest(rng, w, h, *, top=2, bottom=2):
    """Rừng dải ngang: hàng cây dày phía trên, bụi phía dưới, mép trái/phải kín (cổng đục riêng)."""
    g = Grid(w, h, ".")
    for y in range(h):
        for x in range(w):
            if y < top or y >= h - bottom or x == 0 or x == w - 1:
                g.set(x, y, "#")
    # Hàng cây/bụi sát rìa để mép rừng có chiều sâu (vẫn chặn).
    for x in range(1, w - 1):
        if rng.random() < 0.45:
            g.set(x, top, rng.choice("Ttb"))
        if rng.random() < 0.35:
            g.set(x, h - bottom - 1, rng.choice("bbr"))
    return g


def summoning_hall():
    rows = [
        "###################",
        "##K==C=======C==K##",
        "##===============##",
        "##===1===2===3===##",
        "##===============##",
        "##=L===========L=##",
        "##===============##",
        "##===============##",
        "##===============##",
        "########===########",
        "########===########",
    ]
    g = from_rows(rows)
    return {
        "id": "summoning_hall_main_hall",
        "name": "Triệu Linh Điện",
        "kind": "transit_once",
        "theme": "hall",
        "level": None,
        "grid": g,
        "spawn_default": {"x": 9, "y": 7, "face": "up"},
        "respawn_to": "emerald_forest_main_woods",
        "portals": [
            {"id": "hall_exit", "rect": [8, 9, 3, 2], "to": "emerald_forest_main_woods",
             "arrive": {"x": 3, "y": 6, "face": "right"}, "requires": "has_pet"},
        ],
        "pedestals": [
            {"index": 0, "x": 5, "y": 3, "starter": "tien_chuong", "species": "flower_fairy"},
            {"index": 1, "x": 9, "y": 3, "starter": "sa_hat", "species": "spider"},
            {"index": 2, "x": 13, "y": 3, "starter": "xich_ung", "species": "sea_demon"},
        ],
        "npcs": [{"id": "summoner_mira", "x": 9, "y": 1, "face": "down"}],
        "spawn_zones": [],
        "backdrop": None,
    }


def forest_main():
    rng = random.Random(2101)
    g = strip_forest(rng, 34, 13)
    carve_path(g, [(1, 6), (12, 6), (12, 7), (33, 7)])
    g.rect(33, 5, 1, 3, ",")  # lối sang Rừng Sâu (mép đông)
    g.rect(2, 3, 13, 8, ".")  # bãi trống NPC
    carve_path(g, [(1, 6), (12, 6)])
    scatter(g, rng, "Tt", 7, (16, 3, 17, 2), spacing=2)
    scatter(g, rng, "br", 5, (16, 9, 17, 2), spacing=2)
    g.rect(19, 3, 12, 7, g.get(19, 3) if False else ".")
    carve_path(g, [(12, 7), (33, 7)])
    scatter(g, rng, "g", 26, (19, 3, 12, 7), spacing=0)
    scatter(g, rng, "fm", 14, (2, 3, 30, 8), spacing=1)
    scatter(g, rng, "t", 3, (19, 3, 12, 7), spacing=2)
    g.set(9, 2, "s")  # quầy Tiểu Thương Wen (sát hàng cây)
    scatter(g, rng, "f", 4, (2, 3, 12, 8), spacing=1)
    return {
        "id": "emerald_forest_main_woods",
        "name": "Bìa Rừng Lục Bảo",
        "kind": "mixed",
        "theme": "forest",
        "level": [1, 5],
        "grid": g,
        "spawn_default": {"x": 3, "y": 6, "face": "right"},
        "respawn_to": "emerald_forest_main_woods",
        "portals": [
            {"id": "to_deep_woods", "rect": [33, 5, 1, 3], "to": "emerald_forest_deep_woods",
             "arrive": {"x": 2, "y": 6, "face": "right"}},
        ],
        "npcs": [
            {"id": "forest_guide", "x": 6, "y": 4, "face": "down"},
            {"id": "bia_shop", "x": 10, "y": 3, "face": "down"},
            {"id": "bia_skill", "x": 13, "y": 9, "face": "up"},
            {"id": "bia_free", "x": 4, "y": 9, "face": "right"},
        ],
        "spawn_zones": [
            {"id": "z1", "rect": [19, 3, 12, 7], "species": ["snail", "flower_fairy", "mushroom", "spider"],
             "max_alive": 4, "respawn_s": 25},
        ],
        "backdrop": "forest-wall-far",
    }


def forest_deep():
    rng = random.Random(2102)
    g = strip_forest(rng, 38, 13)
    carve_path(g, [(1, 6), (10, 6), (10, 8), (24, 8), (24, 5), (37, 5)])
    g.rect(0, 5, 1, 3, ",")   # lối về Bìa Rừng (tây)
    g.rect(37, 4, 1, 3, ",")  # lối ra Hoàng Môn / Quảng Trường (đông)
    g.rect(2, 3, 5, 7, ".")
    for z in [(8, 3, 9, 7), (19, 3, 8, 7), (28, 3, 7, 7)]:
        scatter(g, rng, "g", 16, z, spacing=0)
    scatter(g, rng, "Ttb", 9, (8, 3, 28, 2), spacing=2)
    scatter(g, rng, "r", 4, (8, 8, 28, 2), spacing=2)
    scatter(g, rng, "m", 10, (2, 3, 34, 7), spacing=1)
    g.rect(2, 3, 5, 7, ".")
    carve_path(g, [(0, 6), (10, 6)])
    carve_path(g, [(24, 5), (37, 5)])
    return {
        "id": "emerald_forest_deep_woods",
        "name": "Rừng Sâu Lục Bảo",
        "kind": "field",
        "theme": "deep_forest",
        "level": [5, 10],
        "grid": g,
        "spawn_default": {"x": 3, "y": 6, "face": "right"},
        "respawn_to": "emerald_forest_main_woods",
        "portals": [
            {"id": "to_main_woods", "rect": [0, 5, 1, 3], "to": "emerald_forest_main_woods",
             "arrive": {"x": 31, "y": 6, "face": "left"}},
            # Lần đầu tới Hoàng Môn theo cốt truyện; các lần sau đi thẳng Quảng Trường (P01-scope §2).
            {"id": "to_city", "rect": [37, 4, 1, 3], "to": "city_palace_gate",
             "arrive": {"x": 2, "y": 6, "face": "right"},
             "redirect": {"if_visited": "city_palace_gate", "to": "city_square", "arrive": {"x": 2, "y": 6, "face": "right"}}},
        ],
        "npcs": [
            {"id": "sau_guard", "x": 5, "y": 3, "face": "down"},
            {"id": "sau_free", "x": 4, "y": 9, "face": "up"},
        ],
        "spawn_zones": [
            {"id": "z1", "rect": [8, 3, 9, 7], "species": ["mushroom", "spider", "wolf"], "max_alive": 3, "respawn_s": 30},
            {"id": "z2", "rect": [19, 3, 8, 7], "species": ["wolf", "spider", "flower_fairy"], "max_alive": 3, "respawn_s": 30},
            {"id": "z3", "rect": [28, 3, 7, 7], "species": ["snail", "mushroom"], "max_alive": 2, "respawn_s": 30},
        ],
        "backdrop": "forest-wall-far",
    }


def palace_gate():
    rows = [
        "##########################",
        "####H#######H#######H#####",
        "#C::::::::::::::::::::::C#",
        "#:L:b::::S:::::S::::b:L:##",
        "#::::::::::::::::::::::::#",
        "#::::::::+++++++++::::::::",
        "#::::::::+++++++++::::::::",
        "#::::::::+++++++++::::::::",
        "#::::::::::::::::::::::::#",
        "#bt" + ":" * 20 + "tb#",
        "##########################",
    ]
    g = from_rows(rows)
    return {
        "id": "city_palace_gate",
        "name": "Hoàng Môn",
        "kind": "safe_hub",
        "theme": "city",
        "level": None,
        "grid": g,
        "spawn_default": {"x": 12, "y": 6, "face": "up"},
        "respawn_to": "city_square",
        "facades": {"4,1": "city-facade-shop", "12,1": "palace-gate", "20,1": "city-facade-townhouse"},
        "portals": [
            {"id": "gate_to_square", "rect": [25, 5, 1, 3], "to": "city_square",
             "arrive": {"x": 2, "y": 6, "face": "right"}},
            {"id": "gate_to_market", "rect": [4, 2, 1, 1], "to": "city_market", "locked": True},
            {"id": "gate_to_palace", "rect": [12, 2, 1, 1], "to": "city_royal_palace", "locked": True},
        ],
        "npcs": [
            {"id": "gate_captain", "x": 14, "y": 4, "face": "down"},
            {"id": "gate_guild", "x": 19, "y": 4, "face": "down"},
        ],
        "spawn_zones": [],
        "backdrop": "city-skyline-far",
    }


def city_square():
    rows = [
        "################################",
        "####H######H#######H######H#####",
        "#C::::::::::::###:::::::::::::C#",
        "#:L:::::::::::#F#::::::::::::L:#",
        "::::::::::::::::::::::::::::::::",
        "::::B::::::::::::::::::::::B::::",
        "::::::::::::::::::::::::::::::::",
        "#:::::::t::::::::::::::t::::::Q#",
        "#:::::O::::::::+++:::::::::::::#",
        "#b::x:::::::::::::::::::::::::b#",
        "#:::::::::::::::::::::::::::::::",
        "################################",
    ]
    rows = [r if len(r) == 32 else r[:32] for r in rows]
    rows[4] = "#" + rows[4][1:-1] + "#"
    rows[5] = "::" + rows[5][2:-2] + "::"
    rows[6] = "::" + rows[6][2:-2] + "::"
    rows[4] = "::" + rows[4][2:-2] + "::"
    rows[10] = "#" + rows[10][1:-1] + "#"
    g = from_rows(rows)
    return {
        "id": "city_square",
        "name": "Quảng Trường Thạch Trụ",
        "kind": "safe_hub",
        "theme": "city",
        "level": None,
        "grid": g,
        "spawn_default": {"x": 16, "y": 6, "face": "down"},
        "respawn_to": "city_square",
        "facades": {"4,1": "city-facade-guild", "11,1": "city-facade-artisan", "19,1": "city-facade-shop", "26,1": "city-facade-townhouse"},
        "portals": [
            {"id": "square_to_gate", "rect": [0, 4, 1, 3], "to": "city_palace_gate",
             "arrive": {"x": 23, "y": 6, "face": "left"}},
            {"id": "square_to_market", "rect": [31, 4, 1, 3], "to": "city_market", "locked": True},
        ],
        "pillar": {"x": 6, "y": 8, "npc": "sq_pillar", "dest": [
            {"map": "emerald_forest_main_woods", "arrive": {"x": 3, "y": 6, "face": "right"}},
            {"map": "city_farm", "locked": True},
            {"map": "treasure_beach_east_shore", "locked": True},
        ]},
        "npcs": [
            {"id": "trainer_elin", "x": 13, "y": 5, "face": "down"},
            {"id": "sq_healer", "x": 9, "y": 3, "face": "down"},
            {"id": "sq_skill", "x": 22, "y": 3, "face": "down"},
            {"id": "sq_free", "x": 25, "y": 8, "face": "left"},
            {"id": "sq_pillar", "x": 7, "y": 9, "face": "up"},
            {"id": "sq_arena", "x": 26, "y": 3, "face": "down"},
            {"id": "sq_board", "x": 29, "y": 7, "face": "left"},
            {"id": "sq_exchange", "x": 4, "y": 3, "face": "down"},
            {"id": "sq_warehouse", "x": 11, "y": 9, "face": "up"},
            {"id": "sq_mailbox", "x": 13, "y": 9, "face": "up"},
        ],
        "spawn_zones": [],
        "backdrop": "city-skyline-far",
    }


MAPS = [summoning_hall, forest_main, forest_deep, palace_gate, city_square]


# ---------------------------------------------------------------- xuất + kiểm
def rle(row: str) -> str:
    out, i = [], 0
    while i < len(row):
        j = i
        while j < len(row) and row[j] == row[i]:
            j += 1
        out.append(f"{j - i}{row[i]}")
        i = j
    return "".join(out)


def walk_rows(m) -> list[str]:
    g: Grid = m["grid"]
    blocked = {(n["x"], n["y"]) for n in m["npcs"]}
    if m.get("pillar"):
        blocked.add((m["pillar"]["x"], m["pillar"]["y"]))
    rows = []
    for y in range(g.h):
        rows.append("".join("." if g.c[y][x] in WALK and (x, y) not in blocked else "#" for x in range(g.w)))
    return rows


def spawn_points(m, rows):
    """Điểm quái cố định trong vùng: chọn ổn định, cách nhau ≥3 ô."""
    out = []
    for z in m["spawn_zones"]:
        x0, y0, w, h = z["rect"]
        rng = random.Random(f"{m['id']}:{z['id']}")
        cells = [(x, y) for y in range(y0, y0 + h) for x in range(x0, x0 + w) if rows[y][x] == "."]
        rng.shuffle(cells)
        pts = []
        for c in cells:
            if all(max(abs(c[0] - p[0]), abs(c[1] - p[1])) >= 3 for p in pts):
                pts.append(c)
            if len(pts) == z["max_alive"]:
                break
        assert len(pts) == z["max_alive"], f"{m['id']}/{z['id']}: chỉ đặt được {len(pts)} điểm"
        for i, (x, y) in enumerate(pts):
            out.append({"id": f"{m['id']}:{z['id']}:{i}", "zone": z["id"], "species_id": z["species"][i % len(z["species"])],
                        "x": x, "y": y, "respawn_s": z["respawn_s"]})
    return out


def check(all_maps):
    ids = {m["id"] for m in all_maps}
    errs = []
    for m in all_maps:
        rows = walk_rows(m)
        w, h = m["grid"].w, m["grid"].h
        ok = lambda x, y: 0 <= x < w and 0 <= y < h and rows[y][x] == "."
        sd = m["spawn_default"]
        if not ok(sd["x"], sd["y"]):
            errs.append(f"{m['id']}: spawn_default bị chặn")
        seen = {(sd["x"], sd["y"])}
        q = deque(seen)
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if n not in seen and ok(*n):
                    seen.add(n)
                    q.append(n)
        for p in m["portals"]:
            x, y, pw, ph = p["rect"]
            cells = [(xx, yy) for yy in range(y, y + ph) for xx in range(x, x + pw)]
            if p.get("locked"):
                if not any(abs(cx - sx) + abs(cy - sy) <= 1 for cx, cy in cells for sx, sy in seen):
                    errs.append(f"{m['id']}/{p['id']}: cổng khóa không tới gần được")
                continue
            if not any(c in seen for c in cells):
                errs.append(f"{m['id']}/{p['id']}: không tới được vùng cổng")
            if p["to"] not in ids:
                errs.append(f"{m['id']}/{p['id']}: map đích {p['to']} không có (thiếu locked?)")
        for n in m["npcs"] + ([m["pillar"]] if m.get("pillar") else []):
            if not any((n["x"] + dx, n["y"] + dy) in seen for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                errs.append(f"{m['id']}/{n.get('id', 'pillar')}: không tới gần được NPC")
        for p in m.get("pedestals", []):
            if not any((p["x"] + dx, p["y"] + dy) in seen for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                errs.append(f"{m['id']}/bệ {p['index']}: không tới gần được")
        for s in spawn_points(m, rows):
            if (s["x"], s["y"]) not in seen:
                errs.append(f"{m['id']}/{s['id']}: điểm quái bị cô lập")
    # điểm đến của cổng: đi được, không nằm trong/kề vùng cổng của map đích
    by = {m["id"]: m for m in all_maps}
    arrivals = []
    for m in all_maps:
        for p in m["portals"]:
            if not p.get("locked"):
                arrivals.append((m["id"], p["id"], p["to"], p["arrive"]))
                if p.get("redirect"):
                    arrivals.append((m["id"], p["id"] + "(redirect)", p["redirect"]["to"], p["redirect"]["arrive"]))
        if m.get("pillar"):
            for d in m["pillar"]["dest"]:
                if not d.get("locked"):
                    arrivals.append((m["id"], "pillar", d["map"], d["arrive"]))
    for src, pid, to, a in arrivals:
        if to not in by:
            errs.append(f"{src}/{pid}: map đích {to} không có")
            continue
        t = by[to]
        rows = walk_rows(t)
        if not (0 <= a["x"] < t["grid"].w and 0 <= a["y"] < t["grid"].h and rows[a["y"]][a["x"]] == "."):
            errs.append(f"{src}/{pid}: điểm đến ({a['x']},{a['y']}) ở {to} bị chặn")
        for q in t["portals"]:
            x, y, pw, ph = q["rect"]
            if x - 1 <= a["x"] <= x + pw and y - 1 <= a["y"] <= y + ph:
                errs.append(f"{src}/{pid}: điểm đến ở {to} nằm trong/kề cổng {q['id']}")
    return errs


def export(m):
    g: Grid = m["grid"]
    rows = walk_rows(m)
    out = {k: v for k, v in m.items() if k not in ("grid",)}
    out.update({
        "width": g.w,
        "height": g.h,
        "walk": "/".join(rle(r) for r in rows),
        "layout": g.rows(),
        "wild_spawns": spawn_points(m, rows),
        "confidence": "designed",
        "source": "P01 v1.0.0 Đợt A — tools/p01/build_maps.py (bố cục HD-2D mới, không khôi phục bản gốc)",
    })
    order = ["id", "name", "kind", "theme", "level", "width", "height", "spawn_default", "respawn_to", "portals", "pillar",
             "pedestals", "npcs", "spawn_zones", "wild_spawns", "walk", "layout", "facades", "backdrop", "confidence", "source"]
    return {k: out[k] for k in order if k in out}


def main():
    maps = [f() for f in MAPS]
    errs = check(maps)
    for e in errs:
        print("LỖI:", e)
    if errs:
        sys.exit(1)
    if "--check" in sys.argv:
        print(f"OK: {len(maps)} map hợp lệ")
        return
    OUT.mkdir(parents=True, exist_ok=True)
    for m in maps:
        (OUT / f"{m['id']}.json").write_text(json.dumps(export(m), ensure_ascii=False, indent=1) + "\n")
        print("ghi", m["id"], f"{m['grid'].w}x{m['grid'].h}")
        print("\n".join("   " + r for r in m["grid"].rows()))


if __name__ == "__main__":
    main()
