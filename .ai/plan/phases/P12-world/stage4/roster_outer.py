"""Roster NPC cho 58 map NGOÀI 17 map phạm vi (11 vùng). Owner 2026-10-15: mở rộng sang Sa Mạc, Mỏm Đá Gió, Đảo Ác Mộng,
Lăng Mộ, Giao Điểm và 6 vùng cao Lv40+. Số NPC mỗi map = số slot NPC trong APK 3.2 (apk-extract/map-scan.json).
Quy tắc owner: hồi máu và cửa hàng chỉ ở map an toàn (hub); map quái chỉ có NPC nhiệm vụ phụ; Trại Tàn Sinh là map hỗn hợp
(NPC và quái trộn) nên được phép có hồi máu/cửa hàng. Vị trí NPC chưa trích từ APK (chỉ biết số slot); đặt khi vẽ HD-2D."""
import json, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
PH = os.path.dirname(HERE)
SCAN = json.load(open(os.path.join(HERE, 'apk-extract/map-scan.json'), encoding='utf-8'))
_txt = ''.join(open(os.path.join(PH, f), encoding='utf-8').read() for f in ('P12-world-names-master.md', 'P12-naming-proposal-jrpg.md'))
NAME = {}
for _l in _txt.split('\n'):
    _i = re.findall(r'`([a-z0-9_]+)`', _l); _b = re.findall(r'\*\*([^*]+)\*\*', _l)
    if _i and _b and _i[0] in SCAN: NAME.setdefault(_i[0], _b[0])
# vùng: (khóa, tên vùng, tiền tố map, hub, tên 4 vai hub, tiêu đề NPC nhiệm vụ phụ ở map quái)
REG = [
 ('desert', 'Sa Mạc', 'desert_', 'desert_shicheng_ruins', ['Trạm Trưởng Sa Thạch', 'Thương Nhân Sa Mạc', 'Sư Phụ Hoang Sa', 'Lữ Khách Cát Vàng'], 'Người Tìm Nước'),
 ('wind', 'Mỏm Đá Gió', 'windrock_', 'windrock_mountain_camp', ['Trại Trưởng Phong Thạch', 'Thợ Đồ Sơn Cước', 'Sư Phụ Đá Gió', 'Người Chăn Dê Núi'], 'Thợ Săn Núi'),
 ('night', 'Đảo Ác Mộng', 'nightmare_', 'nightmare_island_survivor_camp', ['Đội Trưởng Tàn Sinh', 'Tiểu Thương Sống Sót', 'Người Kể Chuyện Đảo'], 'Người Sống Sót'),
 ('tomb', 'Lăng Mộ', 'tomb_', 'tomb_region_camp', ['Quản Trạm Canh Lăng', 'Người Bán Hương Nến', 'Sư Phụ Linh Lăng', 'Người Giữ Mộ'], 'Người Thắp Đèn Mộ'),
 ('cross', 'Giao Điểm', 'crossroads_', 'crossroads_unnamed_area_01', ['Trưởng Cổng Địa Đạo', 'Thợ Đèn Địa Đạo'], 'Người Dò Đường'),
 ('astral', 'Tinh Không', 'astral_', 'astral_realm_unnamed_area_01', ['Tiên Sứ Tử Vân', 'Hiền Giả Vân Ảnh'], 'Kẻ Ngắm Mây'),
 ('ancient', 'Di Tích Cổ', 'ancient_', 'ancient_ruins_unnamed_area_01', ['Thủ Hộ Tiền Sảnh', 'Học Giả Ngọc Lục'], 'Người Khảo Cổ'),
 ('ghost', 'Lâu Đài Ma', 'ghost_', 'ghost_castle_gate', ['Quản Cổng U Lâu', 'Du Hồn Thương Nhân'], 'Hồn Lang Thang'),
 ('tree', 'Cây Thế Giới', 'world_tree_', 'world_tree_gate', ['Hộ Vệ Thế Thụ', 'Dược Sư Lá Xanh'], 'Người Hái Lá'),
 ('tower', 'Tháp Chim', 'tower_', 'tower_region_main_tower', ['Điểu Sứ', 'Tăng Nhân Điểu Tháp'], 'Người Quan Sát Chim'),
 ('maze', 'Mê Thành', 'immortal_', 'immortal_maze_main_maze', ['Dẫn Lộ Mê Thành', 'Thương Nhân Mê Cung'], 'Kẻ Lạc Lối'),
]
POOL = ['Aven', 'Brisa', 'Calder', 'Dalia', 'Edda', 'Fenwick', 'Galen', 'Hesper', 'Iris', 'Jorin', 'Kestra', 'Loren', 'Mirel', 'Nolan', 'Orla', 'Pavel',
 'Quinn', 'Rhea', 'Soren', 'Talia', 'Ulric', 'Vesna', 'Wren', 'Xan', 'Yara', 'Zora', 'Alder', 'Bram', 'Cora', 'Dov', 'Elric', 'Fara', 'Gwen', 'Hale',
 'Ines', 'Joss', 'Kira', 'Lars', 'Mara', 'Neth', 'Olin', 'Perrin', 'Rue', 'Sable', 'Tove', 'Una', 'Vik', 'Willa', 'Yves', 'Zane', 'Aria', 'Bex', 'Cleo',
 'Dune', 'Esme', 'Finn', 'Gale', 'Hob', 'Isen', 'Jade', 'Knox', 'Lio2']
POOL = [p for p in POOL if p != 'Lio2']
def build():
    M2, R2, regions, k = {}, [], [], 0
    for key, rname, pre, hub, hubroles, freet in REG:
        maps = [m for m in SCAN if m.startswith(pre) and SCAN[m]['file'] is not None] if False else [m for m in SCAN if m.startswith(pre)]
        # Lăng Mộ dùng tiền tố tomb_region_; các vùng khác theo tiền tố; hub luôn đứng đầu
        maps = [hub] + [m for m in maps if m != hub]
        regions.append((key, rname, maps))
        for m in maps:
            M2[f'{key}:{m}'] = m
        for m in maps:
            n = SCAN[m]['npcs']; mk = f'{key}:{m}'
            if n == 0: continue
            if m == hub:
                lead, *rest = hubroles
                specs = []
                if len(hubroles) == 4: specs = [(lead, 'main', ['quest', 'heal'], 'Trưởng hub: nhiệm vụ vùng (hook chuỗi chính) + hồi máu.'),
                    (rest[0], 'service', ['shop'], 'Cửa hàng của vùng.'), (rest[1], 'service', ['learn'], 'Dạy kỹ năng; bậc do P13 quyết.'), (rest[2], 'free', ['free'], 'Nhiệm vụ phụ nhẹ, truyện nền.')]
                elif len(hubroles) == 3: specs = [(lead, 'main', ['quest', 'heal'], 'Map hỗn hợp (NPC và quái trộn, owner 2026-10-15): được phép hồi máu. Hook chuỗi chính.'),
                    (rest[0], 'service', ['shop', 'learn'], 'Map hỗn hợp: cửa hàng + dạy kỹ năng (bậc do P13).'), (rest[1], 'free', ['free'], 'Nhiệm vụ phụ, truyện nền.')]
                else: specs = [(lead, 'main', ['quest', 'heal'], 'Trưởng hub: nhiệm vụ vùng (hook chuỗi chính) + hồi máu.'),
                    (rest[0], 'service', ['shop', 'learn'], 'Cửa hàng + dạy kỹ năng (bậc do P13).')]
                assert len(specs) == n, (m, len(specs), n)
            else:
                specs = [(freet, 'free', ['free'], 'Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15).')] * n
            for t, tier, roles, note in specs:
                nm = f'{t} {POOL[k]}'; k += 1
                R2.append((mk, f'{key}_{POOL[k-1].lower()}', nm, tier, roles, None, 'MỚI (vị trí chưa trích từ APK). ' + note))
    assert k <= len(POOL), k
    return M2, R2, regions
M2, R2, REGIONS = build()
