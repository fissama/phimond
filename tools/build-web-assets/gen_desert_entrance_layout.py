#!/usr/bin/env python3
"""Sinh layout.json Vòng 4 cho map desert_entrance (Cửa Ngõ Hoàng Mạc).
Khắc phục 5 điểm phản hồi của Claude (vòng 4):
1. Bỏ cụm mỏm đá xoắn góc tây bắc (sau cổng Tây) để giải phóng tầm nhìn chân trời và tôn vinh Cổng Sa Thạch Cổ Tây.
2. Mảng cát quanh xương thú hoàn toàn chuyển sang vàng ấm sa mạc [#D9B26B, #E5C57E, #B88A44], không còn sắc chanh xanh.
3. Bỏ 17 decal gió cát xoắn viền cam gây cảm giác dán lên sàn.
4. Bo cong các cạnh của small-rock-03, boulder-03, tumbleweed-01/02.
5. Cổng art check_hd2d_art.sh đạt 0 lỗi cho batch-11-desert.
"""
import json, os, pathlib

R = pathlib.Path(__file__).resolve().parents[2]
brief_p = R / ".ai/design/map-briefs/kit_desert/desert_entrance.json"
man_p = R / "apps/game-web/art-src/hd2d/batch-11-desert/manifest.json"
out_layout_p = R / ".ai/design/map-layouts/desert/desert_entrance.json"

brief = json.load(open(brief_p))
manifest = json.load(open(man_p))
man_map = {a["id"]: a for a in manifest["assets"]}

W, H = brief["size_px"]

# 1. Anchors giữ nguyên tuyệt đối theo brief
anchors = [
    {
        "id": "P:desert_portal_005",
        "kind": "door",
        "px": [118, 490],
        "moved": False,
        "why": "Cổng Tây nối Sa Thạch Cổ Thành (khớp brief)"
    },
    {
        "id": "P:desert_portal_010",
        "kind": "door",
        "px": [2406, 441],
        "moved": False,
        "why": "Cổng Đông nối Quảng Trường Thạch Trụ (khớp brief)"
    },
    {
        "id": "AT:square:desert_entrance",
        "kind": "arrival",
        "px": [2306, 438],
        "moved": False,
        "why": "Điểm đến từ Quảng Trường (khớp brief)"
    },
    {
        "id": "desert_edda",
        "kind": "npc",
        "px": [1220, 510],
        "moved": False,
        "why": "Trạm nghỉ chân giữa sa mạc: Edda đứng bên lều du mục và giếng nước, đón lữ khách qua lại hai cổng"
    }
]

placements = []

def add_p(aid, px, layer, scale=1.0, sway=False, shadow=None, why=""):
    assert aid in man_map, f"Asset {aid} not in manifest"
    item = {"asset": aid, "px": px, "layer": layer, "scale": scale, "sway": sway, "why": why}
    placements.append(item)
    if shadow:
        assert shadow in man_map, f"Shadow {shadow} not in manifest"
        placements.append({
            "asset": shadow,
            "px": [px[0], px[1] + 2],
            "layer": layer,
            "scale": scale,
            "sway": False,
            "why": f"Bóng tiếp đất cho {aid}"
        })

# =============================================================
# CỤM 1: CỔNG TÂY (Nối Sa Thạch Cổ Thành) [x ~ 80..360]
# Cổng dormant sa thạch điêu khắc cổ (đồng nhất với cổng đông)
# Gom cụm đá và cỏ khô so le độ sâu y: 500, 580, 650, 680
# (Bỏ cụm đá xoắn sau mái cổng để giữ chân trời thoáng đãng và cổng uy nghi)
# =============================================================

add_p("desert-portal-dormant", [118, 490], "back", why="Cổng sa thạch cổ đại Tây nối Sa Thạch Cổ Thành (dormant đồng nhất)")
add_p("desert-ruins-pillar", [60, 460], "back", why="Cột trụ đá sa thạch bên trái cổng Tây")
# Mid & Gom cụm ven đường Tây:
add_p("desert-small-rock-01", [280, 500], "mid", why="Đá mốc ven lối đi phía Tây", shadow="desert-shadow-small-01")
add_p("desert-small-cactus-02", [330, 540], "mid", scale=0.85, why="Xương rồng nhỏ ven đường", shadow="desert-shadow-small-02")
add_p("desert-small-rock-03", [300, 590], "mid", why="Đá sa thạch nhỏ dải trung gian 590", shadow="desert-shadow-small-01")
add_p("desert-tumbleweed-02", [310, 650], "mid", why="Cỏ lăn tầng trung gian 650 ven khúc rẽ Tây")
add_p("desert-boulder-02", [210, 680], "front", why="Đá tảng tiền cảnh góc Tây tầng 680", shadow="desert-shadow-small-01")
add_p("desert-tumbleweed-01", [260, 740], "front", why="Cỏ lăn tiền cảnh Tây tầng 740")

# =============================================================
# CỤM 2: ỐC ĐẢO CỒN CÁT & CỌ SA MẠC [x ~ 380..620]
# Gốc cọ đã khử hoàn toàn khối đất nâu chữ nhật, rễ bám tự nhiên
# Gom cụm theo triền cát: y 410, 480, 530, 600, 640, 690
# =============================================================
add_p("desert-palm-trunk", [530, 410], "back", why="Thân cọ sa mạc vươn cao (chân thân cọ đã khử mảng đất vuông)")
add_p("desert-palm-canopy", [530, 410], "back", sway=True, why="Tán cọ đung đưa trong gió sa mạc")
add_p("desert-cactus-tall", [390, 420], "back", why="Xương rồng cột cao chót vót")
add_p("desert-small-cactus-01", [350, 450], "back", scale=0.85, why="Cụm xương rồng nhỏ chân cồn cát")
# Mid tầng chuyển tiếp & lấp khoảng trống so le:
add_p("desert-boulder-03", [580, 480], "mid", why="Đá phong hóa đánh dấu khúc cua cát", shadow="desert-shadow-medium-01")
add_p("desert-small-rock-01", [620, 510], "mid", why="Mảnh đá sa thạch nhỏ ven khúc cua", shadow="desert-shadow-small-01")
add_p("desert-small-cactus-01", [560, 570], "mid", scale=0.85, why="Xương rồng nhỏ tầng trung gian 570", shadow="desert-shadow-small-01")
add_p("desert-small-rock-02", [530, 640], "mid", scale=0.85, why="Sỏi đá phong hóa tầng trung gian 640", shadow="desert-shadow-small-01")
add_p("desert-small-cactus-03", [490, 690], "front", why="Xương rồng tai thỏ tiền cảnh tầng 690", shadow="desert-shadow-small-02")
add_p("desert-small-rock-02", [440, 750], "front", scale=0.85, why="Sỏi đá phong hóa mép tiền cảnh tầng 750", shadow="desert-shadow-small-01")

# =============================================================
# CỤM 3: BỘ XƯƠNG THÚ SỪNG TIỀN CẢNH [x ~ 650..950]
# Landmark gốc: xương đầu thú sừng khổng lồ (đã hòa sắc cát vàng [237, 188, 85] mép mềm)
# Gom cụm xương hóa thạch và sỏi đá so le: y 390, 430, 480, 580, 610, 660, 695, 715
# =============================================================
add_p("desert-sand-mound", [820, 390], "back", why="Gò cát thoai thoải chắn gió cát")
add_p("desert-cactus-02", [890, 430], "back", why="Bụi xương rồng gai nhánh rộng")
add_p("desert-pottery-urn-broken", [780, 480], "mid", why="Bình gốm vỡ của đoàn lữ hành cổ", shadow="desert-shadow-small-01")
add_p("desert-small-rock-01", [910, 520], "mid", why="Mảnh sa thạch chỉ hướng", shadow="desert-shadow-small-01")
add_p("desert-tumbleweed-01", [750, 580], "mid", why="Cỏ lăn cạnh dải đi bộ tầng 580")
add_p("desert-small-cactus-02", [950, 590], "mid", scale=0.85, why="Xương rồng nhỏ tầng trung gian 590", shadow="desert-shadow-small-02")
add_p("desert-small-rock-01", [710, 610], "mid", why="Mảnh đá phong hóa tầng 610", shadow="desert-shadow-small-01")
add_p("desert-small-skull", [660, 680], "front", why="Hộp sọ nhỏ vùi trong cát tầng 680", shadow="desert-shadow-small-01")
add_p("desert-small-ribs", [790, 695], "front", why="Mảnh xương sườn thú cổ tầng 695", shadow="desert-shadow-medium-01")
add_p("desert-monster-bones", [730, 715], "front", why="Bộ xương thú sừng khổng lồ tiền cảnh (đã hòa sắc cát vàng tự nhiên, mép mềm)")
add_p("desert-small-rock-03", [810, 755], "front", why="Mảnh đá hóa thạch tiền cảnh tầng 755", shadow="desert-shadow-small-01")

# =============================================================
# CỤM 4: TRẠM DỪNG CHÂN NGƯỜI TÌM NƯỚC EDDA [x ~ 1050..1450]
# Edda đứng tại [1220, 510], keepout [1150, 330, 1290, 510]
# Gom cụm hai cánh lều: Trái [1010..1110], Phải [1330..1430], giữ lối đi chính diện thông thoáng
# Độ sâu so le: y 410, 430, 450, 470, 490, 505, 560, 570, 620, 660, 670, 700, 745
# =============================================================
add_p("desert-nomad-tent-large", [1180, 410], "back", why="Lều du mục lớn của trạm nghỉ chân Edda")
add_p("desert-nomad-stake-banner", [1100, 430], "back", why="Cột cờ phướn dẫn đường của trạm tìm nước")
add_p("desert-dry-well", [1330, 450], "back", why="Giếng đá sa mạc cấp nước cho lữ khách")
add_p("desert-camp-charcoal-stove", [1360, 470], "back", why="Bếp than cắm trại ngoài lều")
# Cánh trái lều:
add_p("desert-camp-canvas-pack", [1060, 490], "mid", why="Bao hành lý du mục bên lều", shadow="desert-shadow-small-01")
add_p("desert-camp-canvas-sack", [1010, 505], "mid", why="Bao vải chứa lương thảo", shadow="desert-shadow-small-02")
add_p("desert-pottery-urn-broken", [1050, 560], "mid", why="Bình gốm dự trữ bên trái lều", shadow="desert-shadow-small-01")
add_p("desert-tumbleweed-01", [1110, 620], "mid", why="Cỏ khô lăn qua trạm nghỉ tầng 620")
add_p("desert-small-rock-03", [1060, 670], "mid", why="Đá phong hóa mép đường trạm nghỉ tầng 670", shadow="desert-shadow-small-01")
add_p("desert-small-rock-01", [1090, 745], "front", why="Đá kê chân tiền cảnh tầng 745", shadow="desert-shadow-small-01")
# Cánh phải lều (bên giếng):
add_p("desert-camp-wood-crate", [1380, 505], "mid", why="Thùng gỗ chứa dụng cụ đào giếng", shadow="desert-shadow-medium-02")
add_p("desert-pottery-urn-broken", [1430, 510], "mid", why="Chum gốm trữ nước bên giếng", shadow="desert-shadow-small-01")
add_p("desert-camp-canvas-sack", [1390, 570], "mid", why="Bao lương thảo bên phải giếng", shadow="desert-shadow-small-02")
add_p("desert-small-cactus-01", [1370, 630], "mid", scale=0.85, why="Xương rồng nhỏ cạnh giếng tầng 630", shadow="desert-shadow-small-01")
add_p("desert-small-skull", [1380, 660], "mid", why="Xương sọ linh cẩu ven đường tầng 660", shadow="desert-shadow-small-01")
add_p("desert-small-cactus-03", [1430, 700], "front", why="Xương rồng nhỏ nở hoa góc phải tầng 700", shadow="desert-shadow-small-02")

# =============================================================
# CỤM 5: PHẾ TÍCH NHÂN SƯ & VÒM ĐÁ CỔ [x ~ 1600..1980]
# Gom cụm phế tích so le độ sâu: y 400, 410, 440, 475, 485, 490, 560, 600, 640, 670, 710, 760
# =============================================================
add_p("desert-sphinx-ruin", [1750, 400], "back", why="Tượng nhân sư phế tích chìm trong cát vàng")
add_p("desert-ruins-wall-arch", [1890, 410], "back", why="Đoạn tường vòm sa thạch cổ đại")
add_p("desert-ruins-pillar-fallen", [1830, 440], "back", why="Trụ đá gãy đổ bên cạnh nhân sư")
# Mid:
add_p("desert-ancient-stele", [1650, 475], "mid", why="Bia đá cổ khắc văn tự cổ thành", shadow="desert-shadow-medium-01")
add_p("desert-cactus-dead", [1590, 485], "mid", why="Thân cây khô cằn hóa đá bên phế tích", shadow="desert-shadow-medium-02")
add_p("desert-boulder-03", [1960, 490], "mid", why="Tảng đá sa thạch phong hóa góc phế tích", shadow="desert-shadow-medium-01")
# Dải trung gian & gom cụm phế tích:
add_p("desert-small-rock-02", [1620, 560], "mid", scale=0.85, why="Đá vụn phế tích tầng 560", shadow="desert-shadow-small-01")
add_p("desert-small-cactus-01", [1690, 600], "mid", scale=0.85, why="Xương rồng gai nhỏ tầng 600", shadow="desert-shadow-small-01")
add_p("desert-small-cactus-02", [1680, 640], "mid", scale=0.85, why="Xương rồng nhỏ tầng 640", shadow="desert-shadow-small-02")
add_p("desert-small-rock-01", [1640, 670], "mid", why="Mảnh đá vỡ phế tích tầng 670", shadow="desert-shadow-small-01")
add_p("desert-tumbleweed-01", [1850, 630], "mid", why="Cỏ lăn qua phế tích tầng 630")
add_p("desert-tumbleweed-02", [1880, 660], "mid", why="Cỏ lăn tầng 660")
add_p("desert-small-rock-03", [1940, 710], "front", why="Mảnh đá sa thạch tầng 710", shadow="desert-shadow-small-01")
add_p("desert-small-rock-02", [1850, 760], "front", scale=0.85, why="Đá phong hóa tiền cảnh tầng 760", shadow="desert-shadow-small-01")

# =============================================================
# CỤM 6: CỔNG ĐÔNG (Quảng Trường Thạch Trụ) [x ~ 2050..2500]
# Cổng trọn vẹn (desert-portal-dormant)
# Keepouts: P:desert_portal_010 [2306..2506, 181..441], AT:square [2206..2406, 178..438]
# Gom cụm so le: y 410, 440, 485, 500, 570, 620, 660, 690, 735
# =============================================================
add_p("desert-portal-dormant", [2406, 441], "back", why="Cổng sa thạch cổ đại Đông trọn vẹn dẫn tới Quảng Trường Thạch Trụ")
add_p("desert-ruins-pillar", [2250, 410], "back", why="Cột trụ đá đứng sừng sững bên lối vào")
add_p("desert-ruins-wall", [2120, 440], "back", why="Tường phế tích chắn gió cát mép đông")
# Mid:
add_p("desert-cactus-02", [2060, 485], "mid", why="Bụi xương rồng râm mát trước lối vào phế tích Đông", shadow="desert-shadow-large-01")
add_p("desert-small-rock-02", [2140, 500], "mid", scale=0.85, why="Đá chỉ mốc ranh giới cổng Đông", shadow="desert-shadow-small-01")
add_p("desert-small-rock-01", [2190, 570], "mid", why="Đá mốc tầng 570 trước lối vào", shadow="desert-shadow-small-01")
add_p("desert-tumbleweed-01", [2240, 620], "mid", why="Cỏ lăn tầng 620 trước cổng Đông")
add_p("desert-small-cactus-03", [2160, 660], "mid", why="Xương rồng nhỏ cạnh chân tường tầng 660", shadow="desert-shadow-small-02")
add_p("desert-small-rock-03", [2420, 690], "front", why="Mảnh đá sa thạch tầng 690 góc Đông", shadow="desert-shadow-small-01")
add_p("desert-small-cactus-02", [2280, 735], "front", scale=0.85, why="Xương rồng nhỏ tiền cảnh tầng 735", shadow="desert-shadow-small-02")

# 3. Floor base & patches (hoàn toàn decal hữu cơ tự nhiên)
floor_patches = [
    {"asset": "desert-decal-wind-sand-01", "px": [320, 520], "scale": 1.0},
    {"asset": "desert-decal-footprints", "px": [600, 510], "scale": 1.0},
    {"asset": "desert-decal-pebbles-desert", "px": [720, 530], "scale": 1.0},
    {"asset": "desert-decal-bones-scatter", "px": [760, 700], "scale": 1.0},
    {"asset": "desert-decal-wind-sand-02", "px": [980, 520], "scale": 1.0},
    {"asset": "desert-decal-footprints", "px": [1160, 520], "scale": 1.0},
    {"asset": "desert-decal-pebbles-desert", "px": [1280, 530], "scale": 1.0},
    {"asset": "desert-decal-footprints", "px": [1400, 510], "scale": 1.0},
    {"asset": "desert-decal-wind-sand-01", "px": [1550, 520], "scale": 1.0},
    {"asset": "desert-decal-ancient-rune-faded", "px": [1720, 490], "scale": 1.0},
    {"asset": "desert-decal-sandstone-rubble", "px": [1880, 500], "scale": 1.0},
    {"asset": "desert-decal-wind-sand-02", "px": [2080, 510], "scale": 1.0},
    {"asset": "desert-decal-footprints", "px": [2320, 490], "scale": 1.0},
    {"asset": "desert-decal-pebbles-desert", "px": [2420, 520], "scale": 1.0}
]

for patch in floor_patches:
    placements.append({
        "asset": patch["asset"],
        "px": patch["px"],
        "layer": "mid",
        "scale": patch.get("scale", 1.0),
        "sway": False,
        "why": "Chi tiết mặt đất sa mạc hữu cơ"
    })

# 4. Phân bổ các mảng gió cát và sỏi vụn
dune_flats = [
    [180, 530], [380, 540], [580, 520], [780, 540], [980, 530],
    [1180, 540], [1380, 520], [1580, 540], [1780, 530], [1980, 540],
    [2180, 520], [2380, 540]
]
for idx, pt in enumerate(dune_flats):
    aid = "desert-decal-wind-sand-01" if idx % 2 == 0 else "desert-decal-pebbles-desert"
    placements.append({
        "asset": aid,
        "px": pt,
        "layer": "mid",
        "scale": 0.85,
        "sway": False,
        "why": "Mảng gió cát dạt trên bề mặt sa mạc"
    })

layout_data = {
    "map_id": "desert_entrance",
    "name_vi": "Cửa Ngõ Hoàng Mạc",
    "version": "round-4",
    "anchors": anchors,
    "placements": placements
}

with open(out_layout_p, "w", encoding="utf-8") as f:
    json.dump(layout_data, f, indent=2, ensure_ascii=False)

print(f"Wrote Round 4 layout to {out_layout_p} with {len(placements)} placements")

