#!/usr/bin/env python3
"""Sinh P12-S4-npc-matrix.md (bảng NPC nguồn APK 3.2) từ apk-extract/npcs.json. Chạy trong thư mục stage4: python3 -I gen_npc_matrix.py"""
import json, collections
n = json.load(open('apk-extract/npcs.json', encoding='utf-8'))
by = collections.defaultdict(list)
for r in n: by[r['map'][0]].append(r)
role = {'thaythuoc': 'thầy thuốc (hồi máu?)', 'TTTD': 'chưa rõ (viết tắt)', 'guild': 'bang hội', 'Shop': 'cửa hàng', 'Skill': 'kỹ năng', 'LamMoi': '"làm mới" (chưa rõ)', 'ChucPhuc': 'chúc phúc', 'Ong Poke': 'Ông Poke (nhân vật)', 'QuanLy': 'quản lý (nông trại?)'}
order = ['summoning_hall_main_hall', 'city_square', 'city_market', 'city_palace_gate', 'city_royal_palace', 'city_activity_hall', 'city_pet_room', 'city_farm', 'city_deathmatch_arena', 'emerald_forest_main_woods', 'emerald_forest_deep_woods', 'treasure_beach_fishermen_beach', 'treasure_beach_east_beach', 'treasure_beach_deep_sea', 'treasure_beach_west_beach', 'treasure_beach_prosperity_island', 'middle_corridor_main_hall']
L = ["# P12 Stage 4 — Ma trận NPC nguồn APK 3.2 (44 slot, vai trò gốc chỉ là suy đoán; roster thiết kế: P12-S4-npc-roster.md)\n",
 "Mỗi dòng là một object trong container `AllNpc` có collider + script. **Vai trò là suy đoán từ tên object**, không đọc được từ script (IL2CPP, không có type tree). Tọa độ là đơn vị thế giới Unity (x,y), đã gộp hierarchy. `active=false` = đối tượng ẩn trong scene, script bật sau.\n",
 "Sprite là tên sprite trong APK, chưa ánh xạ sang asset game.\n"]
for m in order:
    rows = by.get(m, [])
    L.append(f"\n## {m}  ({len(rows)} NPC)\n")
    if m == 'summoning_hall_main_hall':
        L.append("Scene có 4 nhóm `poke*` ở (-3.15, -0.22), mỗi nhóm 2 sprite: `pokeLinhThe` (linh thể), `pokeThu` (thú), `pokeThucVat` (thực vật), `pokeSau` (sâu/côn trùng) → bản gốc có **4** lựa chọn pet khởi đầu; thiết kế Phimond đã chốt 3 (Thực vật / Côn trùng / Thú), bỏ Linh thể.\n")
    if not rows:
        L.append("(không có NPC)\n"); continue
    L += ["| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |", "|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: r['xy'][0]):
        base = r['name'].split(' (')[0]
        L.append(f"| `{r['name']}` | {role.get(base, 'chưa rõ')} | {r['sprite']} | {r['xy'][0]}, {r['xy'][1]} | {'có' if r['active'] else 'ẩn'} |")
open('P12-S4-npc-matrix.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print(len(n), 'NPC')
