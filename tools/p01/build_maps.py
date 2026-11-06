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
            A sạp mái hiên   W giếng   n cờ   k xe đẩy
            (đơn 10) P bồn sư tử   V xe bán hàng   X bao tải   Y cây cắt tỉa   G biển treo
                     J/j sư tử đá (nhìn phải/trái)   Z cột cờ
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

WALK = set(".,:=_+fgmRN")  # R/N: luống đất Điền Trang (đi được)


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


def mirror_rows(rows: list[str]) -> list[str]:
    """Lật trái-phải bố cục (bản phác APK/P12: Quảng Trường và Hoàng Môn đặt cổng, trụ, NPC theo hướng ngược bản v1.0.0 đầu)."""
    return [r[::-1] for r in rows]


def summoning_hall():
    rows = [
        "###################",
        "##K==C=======C==K##",
        "##===============##",
        "##===1=======3===##",
        "##===============##",
        "##=L===========L=##",
        "##===============##",
        "##===============##",
        "##===============##",
        "########===########",
        "########===########",
    ]
    rows[2] = rows[2][:9] + "2" + rows[2][10:]  # cung 3 bệ (P12 U10): bệ giữa lùi sau hai bệ bên
    g = from_rows(rows)
    return {
        "id": "summoning_hall_main_hall",
        "name": "Triệu Linh Điện",
        "kind": "transit_once",
        "theme": "hall",
        "level": None,
        "grid": g,
        "spawn_default": {"x": 9, "y": 5, "face": "down"},
        "respawn_to": "emerald_forest_main_woods",
        "portals": [
            {"id": "hall_exit", "rect": [8, 9, 3, 2], "to": "emerald_forest_main_woods",
             "arrive": {"x": 3, "y": 6, "face": "right"}, "requires": "has_pet"},
        ],
        "pedestals": [
            {"index": 0, "x": 5, "y": 3, "starter": "species_0021", "species": "species_0021", "display": "species_0144"},
            {"index": 1, "x": 9, "y": 2, "starter": "species_0109", "species": "species_0109", "display": "species_0151"},
            {"index": 2, "x": 13, "y": 3, "starter": "species_0071", "species": "species_0071", "display": "species_0149"},
        ],
        "npcs": [{"id": "summoner_mira", "x": 14, "y": 4, "face": "down"}],
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
    g.set(15, 2, "s")  # quầy Tiểu Thương Wen (sát hàng cây)
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
            # Thứ tự trái → phải theo bản phác APK: Lio, Tuli, Rowan, Wen.
            {"id": "forest_guide", "x": 5, "y": 4, "face": "down"},
            {"id": "bia_free", "x": 8, "y": 9, "face": "right"},
            {"id": "bia_skill", "x": 12, "y": 9, "face": "up"},
            {"id": "bia_shop", "x": 15, "y": 3, "face": "down"},
        ],
        "spawn_zones": [
            {"id": "z1", "rect": [19, 3, 12, 7], "species": ["species_0111", "species_0022", "species_0023", "species_0112"],
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
             "redirect": {"if_visited": "city_palace_gate", "to": "city_square", "arrive": {"x": 29, "y": 6, "face": "left"}}},
        ],
        "npcs": [
            {"id": "sau_guard", "x": 27, "y": 4, "face": "down"},
            {"id": "sau_free", "x": 4, "y": 9, "face": "up"},
        ],
        "spawn_zones": [
            {"id": "z1", "rect": [8, 3, 9, 7], "species": ["species_0023", "species_0112", "species_0074"], "max_alive": 3, "respawn_s": 30},
            {"id": "z2", "rect": [19, 3, 8, 7], "species": ["species_0074", "species_0112", "species_0022"], "max_alive": 3, "respawn_s": 30},
            {"id": "z3", "rect": [28, 3, 7, 7], "species": ["species_0111", "species_0023"], "max_alive": 2, "respawn_s": 30},
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
        "#:::::::::::::::::::::::::",
        "#:::::::::::::::::::::::::",
        "#:::::::::::::::::::::::::",
        "#::::::::::::::::::::::::#",
        "#bt" + ":" * 20 + "tb#",
        "##########################",
    ]
    def put(x, y, ch):
        rows[y] = rows[y][:x] + ch + rows[y][x + 1:]
    for x, y, ch in [(8, 2, "Z"), (16, 2, "Z"), (7, 9, "b"), (18, 9, "b"), (21, 8, "k"), (5, 8, "x"),
                     (10, 2, "j"), (14, 2, "J")]:
        put(x, y, ch)
    rows = mirror_rows(rows)  # bản phác APK: cổng Quảng Trường bên trái, Chợ bên phải, cổng cung điện ở giữa
    # Lối thảm đỏ dọc theo trục cổng cung điện (x=12..14), từ chân cổng xuống sân.
    for y in range(2, 9):
        for x in (12, 13, 14):
            rows[y] = rows[y][:x] + "+" + rows[y][x + 1:]
    for y in (5, 6, 7):  # hai mép trái/phải đều mở: trái về Quảng Trường, phải sang Chợ
        rows[y] = ":" + rows[y][1:-1] + ":"
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
        "facades": {"5,1": "city-facade-townhouse", "13,1": "palace-gate", "21,1": "city-facade-shop"},
        "portals": [
            {"id": "gate_to_square", "rect": [0, 5, 1, 3], "to": "city_square",
             "arrive": {"x": 29, "y": 6, "face": "left"}},
            {"id": "gate_to_market", "rect": [25, 5, 1, 3], "to": "city_market",
             "arrive": {"x": 2, "y": 6, "face": "right"}},
            {"id": "gate_to_palace", "rect": [13, 2, 1, 1], "to": "city_royal_palace",
             "arrive": {"x": 13, "y": 8, "face": "up"}},
        ],
        "npcs": [
            {"id": "gate_captain", "x": 11, "y": 4, "face": "down"},
            {"id": "gate_guild", "x": 6, "y": 4, "face": "down"},
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
        "#:::::O::::::::::::::::::::::::#",
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
    def put(x, y, ch):
        rows[y] = rows[y][:x] + ch + rows[y][x + 1:]
    # Bày biện: chợ có mái hiên, giếng, xe đẩy, cờ, chậu hoa dọc vỉa hè (P01 review 2026-10-22).
    for x, y, ch in [(18, 9, "A"), (21, 9, "A"), (24, 10, "A"), (3, 7, "W"), (28, 10, "k"), (29, 9, "x"),
                     (6, 2, "n"), (26, 2, "n"), (11, 2, "b"), (19, 2, "b"), (17, 7, "b"),
                     # Đơn 10: bồn sư tử, cây cắt tỉa hai bên đài phun, biển treo, xe bán hàng + bao tải.
                     (8, 2, "P"), (13, 2, "Y"), (17, 2, "Y"), (24, 2, "G"), (16, 10, "V"), (17, 10, "X")]:
        put(x, y, ch)
    rows = mirror_rows(rows)  # bản phác APK: cổng Hoàng Môn bên phải, Chợ bên trái, trụ teleport dưới-phải (P12 U1)
    g = from_rows(rows)
    return {
        "id": "city_square",
        "name": "Quảng Trường Thạch Trụ",
        "kind": "safe_hub",
        "theme": "city",
        "level": None,
        "grid": g,
        "spawn_default": {"x": 15, "y": 6, "face": "down"},
        "respawn_to": "city_square",
        "facades": {"27,1": "city-facade-guild", "20,1": "city-facade-artisan", "12,1": "city-facade-shop", "5,1": "city-facade-townhouse"},
        "portals": [
            {"id": "square_to_gate", "rect": [31, 4, 1, 3], "to": "city_palace_gate",
             "arrive": {"x": 2, "y": 6, "face": "right"}},
            {"id": "square_to_market", "rect": [0, 4, 1, 3], "to": "city_market",
             "arrive": {"x": 27, "y": 6, "face": "left"}},
            {"id": "square_to_arena", "rect": [4, 2, 1, 1], "to": "city_deathmatch_arena",
             "arrive": {"x": 6, "y": 6, "face": "right"}},
        ],
        "pillar": {"x": 25, "y": 8, "npc": "sq_pillar", "dest": [
            {"map": "emerald_forest_main_woods", "arrive": {"x": 3, "y": 6, "face": "right"}},
            {"map": "city_farm", "arrive": {"x": 3, "y": 6, "face": "right"}},
            {"map": "treasure_beach_east_shore", "locked": True},
        ]},
        "npcs": [
            {"id": "trainer_elin", "x": 18, "y": 5, "face": "down"},
            {"id": "sq_healer", "x": 3, "y": 3, "face": "down"},
            {"id": "sq_skill", "x": 9, "y": 3, "face": "down"},
            {"id": "sq_free", "x": 6, "y": 8, "face": "right"},
            {"id": "sq_pillar", "x": 24, "y": 9, "face": "up"},
            {"id": "sq_arena", "x": 5, "y": 3, "face": "down"},
            {"id": "sq_board", "x": 2, "y": 7, "face": "right"},
            {"id": "sq_exchange", "x": 27, "y": 3, "face": "down"},
            {"id": "sq_warehouse", "x": 20, "y": 9, "face": "up"},
            {"id": "sq_mailbox", "x": 17, "y": 9, "face": "up"},
        ],
        "spawn_zones": [],
        "backdrop": "city-skyline-far",
    }


def city_market():
    """Thương Phố (v1.1.0 Đợt B1): dải chợ ngang, cổng trái về Hoàng Môn, cổng phải về Quảng Trường."""
    W, H = 30, 12
    rows = ["#" * W] + ["#" + ":" * (W - 2) + "#" for _ in range(H - 2)] + ["#" * W]
    def put(x, y, ch):
        rows[y] = rows[y][:x] + ch + rows[y][x + 1:]
    for x in (4, 10, 16, 22, 27):
        put(x, 1, "H")
    for y in (5, 6, 7):  # hai mép mở: trái → Hoàng Môn, phải → Quảng Trường
        put(0, y, ":")
        put(W - 1, y, ":")
    # Sạp mái hiên dọc hàng trên, xe bán hàng + bao tải + thùng dọc hàng dưới, đèn và cờ.
    for x, y, ch in [(7, 3, "A"), (12, 3, "A"), (17, 3, "A"), (22, 3, "A"),
                     (2, 2, "L"), (27, 2, "L"), (9, 2, "n"), (20, 2, "n"),
                     (8, 10, "V"), (9, 10, "X"), (21, 10, "V"), (22, 10, "X"),
                     (3, 9, "x"), (26, 9, "x"), (14, 10, "k"), (5, 9, "b"), (24, 9, "b"),
                     (13, 9, "b"), (16, 9, "b")]:
        put(x, y, ch)
    g = from_rows(rows)
    return {
        "id": "city_market",
        "name": "Thương Phố",
        "kind": "safe_hub",
        "theme": "city",
        "level": None,
        "grid": g,
        "spawn_default": {"x": 14, "y": 6, "face": "down"},
        "respawn_to": "city_square",
        "facades": {"4,1": "city-facade-shop", "10,1": "city-facade-bakery", "16,1": "city-facade-exchange",
                    "22,1": "city-facade-warehouse", "27,1": "city-facade-inn"},
        "portals": [
            {"id": "market_to_gate", "rect": [0, 5, 1, 3], "to": "city_palace_gate",
             "arrive": {"x": 23, "y": 6, "face": "left"}},
            {"id": "market_to_square", "rect": [29, 5, 1, 3], "to": "city_square",
             "arrive": {"x": 2, "y": 5, "face": "right"}},
        ],
        "npcs": [
            {"id": "mk_general", "x": 8, "y": 4, "face": "down"},
            {"id": "mk_trader", "x": 21, "y": 8, "face": "up"},
        ],
        "spawn_zones": [],
        "backdrop": "city-skyline-far",
    }


def city_royal_palace():
    """Vương Cung (v1.1.0 Đợt B1): sân thảm đỏ; cổng dưới về Hoàng Môn, cửa trên vào Vạn Sự Hội Sảnh."""
    W, H = 26, 13
    rows = ["#" * W] + ["#" + ":" * (W - 2) + "#" for _ in range(H - 2)] + ["#" * W]
    def put(x, y, ch):
        rows[y] = rows[y][:x] + ch + rows[y][x + 1:]
    for x in (4, 13, 21):
        put(x, 1, "H")
    for y in range(2, 11):  # thảm đỏ dọc trục giữa, từ cửa Hội Sảnh xuống cổng Hoàng Môn
        for x in (12, 13, 14):
            put(x, y, "+")
    for x, y, ch in [(3, 2, "C"), (22, 2, "C"), (7, 2, "Z"), (19, 2, "Z"), (10, 4, "S"), (16, 4, "S"),
                     (2, 4, "L"), (23, 4, "L"), (6, 8, "Y"), (19, 8, "Y"), (4, 10, "B"), (21, 10, "B"),
                     (8, 10, "b"), (17, 10, "b")]:
        put(x, y, ch)
    g = from_rows(rows)
    return {
        "id": "city_royal_palace",
        "name": "Vương Cung",
        "kind": "safe_hub",
        "theme": "city",
        "level": None,
        "grid": g,
        "spawn_default": {"x": 13, "y": 8, "face": "up"},
        "respawn_to": "city_square",
        "facades": {"4,1": "city-facade-guild", "13,1": "palace-gate", "21,1": "city-facade-guild"},
        "portals": [
            {"id": "palace_to_gate", "rect": [12, 11, 3, 1], "to": "city_palace_gate",
             "arrive": {"x": 13, "y": 5, "face": "down"}},
            {"id": "palace_to_hall", "rect": [13, 2, 1, 1], "to": "city_activity_hall",
             "arrive": {"x": 9, "y": 6, "face": "up"}},
        ],
        "npcs": [
            {"id": "pal_healer", "x": 9, "y": 6, "face": "right"},
        ],
        "spawn_zones": [],
        "backdrop": "city-skyline-far",
    }


def city_activity_hall():
    """Vạn Sự Hội Sảnh (v1.1.0 Đợt B1): sảnh đá có bảng nhiệm vụ; lối ra phía dưới về Vương Cung."""
    W, H = 20, 11
    rows = ["#" * W] + ["##" + "=" * (W - 4) + "##" for _ in range(H - 3)] + ["#" * W, "#" * W]
    rows[0] = "#" * W
    def put(x, y, ch):
        rows[y] = rows[y][:x] + ch + rows[y][x + 1:]
    for y in (9, 10):  # hành lang ra
        for x in (8, 9, 10):
            put(x, y, "=")
    for x, y, ch in [(2, 1, "K"), (17, 1, "K"), (5, 1, "C"), (14, 1, "C"), (3, 5, "L"), (16, 5, "L"),
                     (4, 2, "Q"), (15, 2, "Q")]:
        put(x, y, ch)
    g = from_rows(rows)
    return {
        "id": "city_activity_hall",
        "name": "Vạn Sự Hội Sảnh",
        "kind": "safe_hub",
        "theme": "hall",
        "level": None,
        "grid": g,
        "spawn_default": {"x": 9, "y": 6, "face": "up"},
        "respawn_to": "city_square",
        "portals": [
            {"id": "hall_to_palace", "rect": [8, 9, 3, 2], "to": "city_royal_palace",
             "arrive": {"x": 13, "y": 5, "face": "down"}},
        ],
        "npcs": [{"id": "act_events", "x": 10, "y": 3, "face": "down"}],
        "spawn_zones": [],
        "backdrop": None,
    }


def city_farm():
    """Điền Trang Lục Dã (v1.1.0 Đợt B1): ruộng, chuồng, cối xay; cổng trái về Quảng Trường, cổng phải sang Phòng thú cưng."""
    W, H = 34, 14
    rows = ["#" * W] + ["#" + "." * (W - 2) + "#" for _ in range(H - 2)] + ["#" * W]
    def put(x, y, ch):
        rows[y] = rows[y][:x] + ch + rows[y][x + 1:]
    for x in range(1, W - 1):  # đường đất ngang
        for y in (6, 7):
            put(x, y, ",")
    for y in range(3, 6):  # lối đất lên chuồng
        put(24, y, ",")
        put(9, y, ",")
    # Ruộng (decal): trái x10-15, phải x18-23, y9-10 (rìa rừng che từ y12); lối đất x16-17 giữa hai bên (chặn bằng 'x' vô hình)
    for y in range(9, 11):
        for x in list(range(10, 16)) + list(range(18, 24)):
            put(x, y, "x")
    for y in range(8, 13):
        for x in (16, 17):
            put(x, y, ",")
    for x in list(range(10, 16)) + list(range(18, 24)):  # hàng rào phía trên ruộng (chừa lối x16-17)
        put(x, 8, "j")
    for y in range(9, 11):
        put(9, y, "k")
        put(24, y, "k")
    put(9, 8, "n")
    put(24, 8, "n")
    for y in (6, 7):  # cổng mở hai mép
        put(0, y, ",")
        put(W - 1, y, ",")
    for x in (22, 23, 25, 26):  # kho thóc (5 ô rộng) ở hàng 2
        put(x, 2, "#")
    for x in (7, 8, 10, 11):  # chuồng ngựa
        put(x, 2, "#")
    for x, y in ((30, 3), (32, 3)):  # cối xay
        put(x, y, "#")
    for x, y, ch in [(24, 2, "M"), (9, 2, "U"), (31, 3, "E"), (27, 4, "D"), (28, 4, "D"), (4, 3, "z"), (4, 11, "z"),
                     (12, 4, "q"), (16, 11, "G"), (19, 4, "Q"), (21, 5, "W"), (5, 9, "V"), (29, 9, "V"), (2, 9, "f"),
                     (3, 10, "f"), (29, 11, "f"), (30, 10, "f"), (26, 11, "y")]:
        put(x, y, ch)
    g = from_rows(rows)
    return {
        "id": "city_farm",
        "name": "Điền Trang Lục Dã",
        "kind": "safe_hub",
        "theme": "forest",
        "level": None,
        "grid": g,
        "spawn_default": {"x": 4, "y": 7, "face": "right"},
        "respawn_to": "city_square",
        "portals": [
            {"id": "farm_to_square", "rect": [0, 6, 1, 2], "to": "city_square",
             "arrive": {"x": 23, "y": 6, "face": "left"}},
            {"id": "farm_to_pet_room", "rect": [33, 6, 1, 2], "to": "city_pet_room",
             "arrive": {"x": 3, "y": 6, "face": "right"}},
        ],
        "npcs": [{"id": "ranch_keeper", "x": 6, "y": 5, "face": "down"}],
        "spawn_zones": [],
        "backdrop": "farm-hills-far",
    }


def city_pet_room():
    """Phòng thú cưng (v1.1.0 Đợt B1): gian gỗ có ổ nằm, chén ăn; cửa trái ra Điền Trang."""
    W, H = 20, 11
    rows = ["#" * W, "#" * W] + ["#" + "=" * (W - 2) + "#" for _ in range(H - 3)] + ["#" * W]
    def put(x, y, ch):
        rows[y] = rows[y][:x] + ch + rows[y][x + 1:]
    for y in (5, 6, 7):
        put(0, y, "=")
    for x, y, ch in [(2, 2, "K"), (17, 2, "Y"), (4, 2, "P"), (14, 2, "I"), (5, 3, "u"), (6, 3, "o"), (5, 8, "v"), (6, 8, "o"),
                     (15, 8, "h"), (14, 8, "o"), (13, 9, "J"), (10, 9, "X"), (2, 9, "I"), (4, 9, "P"), (17, 6, "x"), (17, 7, "x"), (11, 3, "x")]:
        put(x, y, ch)
    g = from_rows(rows)
    return {
        "id": "city_pet_room",
        "name": "Phòng thú cưng",
        "kind": "safe_hub",
        "theme": "room",
        "level": None,
        "grid": g,
        "spawn_default": {"x": 9, "y": 6, "face": "down"},
        "respawn_to": "city_square",
        "facades": {"4,1": "hall-wall-timber", "11,1": "hall-wall-timber", "18,1": "hall-wall-timber"},
        "portals": [
            {"id": "pet_room_to_farm", "rect": [0, 5, 1, 3], "to": "city_farm",
             "arrive": {"x": 31, "y": 6, "face": "left"}},
        ],
        "npcs": [
            {"id": "pet_master", "x": 9, "y": 3, "face": "down"},
            {"id": "pet_shop", "x": 13, "y": 4, "face": "down"},
        ],
        "spawn_zones": [],
        "backdrop": None,
    }


def city_deathmatch_arena():
    """Huyết Chiến Đài (v1.1.0 Đợt B1): chỉ cảnh + lối ra; vào bằng NPC ở Quảng Trường (nợ N01)."""
    W, H = 30, 13
    rows = ["#" * W, "#" * W] + ["#" + ":" * (W - 2) + "#" for _ in range(H - 3)] + ["#" * W]
    def put(x, y, ch):
        rows[y] = rows[y][:x] + ch + rows[y][x + 1:]
    for y in (5, 6, 7):
        put(0, y, ":")
    for x, y, ch in [(3, 2, "l"), (26, 2, "l"), (3, 10, "l"), (26, 10, "l"), (8, 2, "i"), (18, 2, "e"),
                     (15, 2, "d"), (2, 4, "c"), (27, 4, "c"), (2, 9, "c"), (27, 9, "c"),
                     (13, 2, "w"), (12, 2, "x"), (14, 2, "x"), (21, 2, "J"), (20, 2, "x"), (22, 2, "x"),
                     (6, 4, "k"), (23, 4, "k"), (6, 9, "k"), (23, 9, "k")] + [(x, 2, "j") for x in (5, 6, 7, 9, 10, 11, 16, 17, 24, 25)]:
        put(x, y, ch)
    g = from_rows(rows)
    return {
        "id": "city_deathmatch_arena",
        "name": "Huyết Chiến Đài",
        "kind": "safe_hub",
        "theme": "arena",
        "level": None,
        "min_level": 10,
        "grid": g,
        "spawn_default": {"x": 6, "y": 6, "face": "right"},
        "respawn_to": "city_square",
        "facades": {f"{x},1": "arena-grandstand" for x in (2, 6, 10, 14, 18, 22, 26, 29)},
        "portals": [
            {"id": "arena_to_square", "rect": [0, 5, 1, 3], "to": "city_square",
             "arrive": {"x": 6, "y": 5, "face": "down"}},
        ],
        "npcs": [{"id": "arena_master", "x": 10, "y": 3, "face": "down"}],
        "spawn_zones": [],
        "backdrop": "arena-stands-far",
    }


MAPS = [summoning_hall, forest_main, forest_deep, palace_gate, city_square, city_market, city_royal_palace, city_activity_hall, city_farm, city_pet_room, city_deathmatch_arena]


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
    order = ["id", "name", "kind", "theme", "level", "min_level", "width", "height", "spawn_default", "respawn_to", "portals", "pillar",
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
