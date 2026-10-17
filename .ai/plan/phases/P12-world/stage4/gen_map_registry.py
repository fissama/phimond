#!/usr/bin/env python3
"""Sinh registry map canonical (P12 Stage 4, đề xuất chờ owner duyệt): P12-S4-map-registry.json + .md. Chạy trong thư mục stage4: python3 -I gen_map_registry.py
Đọc apk-extract/map-scan.json (92 map: quái, NPC, cửa), roster_outer.py (tên owner), roster_data.py (map phạm vi)."""
import json, sys
sys.path.insert(0, '.')
from roster_outer import SCAN, NAME, REGIONS
from roster_data import M
CORE = set(M.values())
REG = {m: (rn, key) for key, rn, ms in REGIONS for m in ms}
LV = {'emerald_forest_main_woods': '1–5', 'emerald_forest_deep_woods': '5–10', 'treasure_beach_east_beach': '10–12', 'treasure_beach_west_beach': '12–13',
 'treasure_beach_deep_sea': '13–14', 'treasure_beach_prosperity_island': '14–15'}
RLV = {'desert': '15–20', 'wind': '20–25', 'night': '25–30', 'tomb': '30–35', 'cross': '35–40'}
HIGHK = {'astral', 'ancient', 'ghost', 'tree', 'tower', 'maze'}
PRIV = {'city_farm', 'city_pet_room'}
INST = {'city_deathmatch_arena', 'chaos_arena_main_field', 'team_arena_main_field', 'maya_floor_01', 'dungeon_floor_01'}
def group(m):
    if m in REG: return REG[m][0]
    for p, g in [('summoning', 'Khởi đầu'), ('emerald', 'Emerald'), ('city', 'Thành phố'), ('treasure', 'Bãi biển'), ('middle', 'Hải Tặc Hào'), ('guild', 'Bang hội'), ('wolf', 'Sói–Cừu')]:
        if m.startswith(p): return g
    return 'Hoạt động / hầm ngục'
def kind(m, s):
    if m in PRIV: return 'private_per_player'
    if m in INST or m.startswith('wolf_sheep_') and m != 'wolf_sheep_waiting_hall': return 'instance'
    if m.startswith('guild_'): return 'guild_shared'
    if m == 'summoning_hall_main_hall': return 'transit_once'
    if m in ('emerald_forest_main_woods', 'nightmare_island_survivor_camp'): return 'mixed'
    if s['trans_enemy'] or s['markers']: return 'field'
    if s['npcs']: return 'safe_hub'
    return 'transit'
def respawn(m, g):
    return {'Khởi đầu': 'Bìa Rừng Lục Bảo', 'Emerald': 'Bìa Rừng Lục Bảo', 'Thành phố': 'Quảng Trường Thạch Trụ', 'Bãi biển': 'Bến Ngư Châu', 'Hải Tặc Hào': 'Hải Tặc Hào',
            'Đảo Ác Mộng': 'Trại Tàn Sinh'}.get(g) or (NAME[[mm for mm in REG if REG[mm][0] == g][0]] if g in {r[0] for r in REG.values()} else 'Quảng Trường Thạch Trụ')
FT = json.load(open('P12-S4-floor-templates.json', encoding='utf-8'))
SP = json.load(open('P12-S4-spawn-plan.json', encoding='utf-8'))['changes']
FL_LV = {}
for r_ in FT['regions']:
    FL_LV[r_['floor_map']] = f"Tầng 1–{r_['floors']} = Lv{r_['level_first']}–{r_['level_last']}"
    FL_LV[r_['secret_map']] = 'Lv' + r_['secret']['level']
for m_, i_ in FT['banded_fields']['maps'].items(): FL_LV[m_] = FT['banded_fields']['bands'][i_]
rows = []
for m, s in SCAN.items():
    g = group(m); k = kind(m, s); key = REG.get(m, (None, None))[1]
    lv = LV.get(m) or RLV.get(key) or ('40+' if key in HIGHK else None)
    lv = FL_LV.get(m, lv)
    hub = next((mm for mm in REG if REG[mm][0] == g), None)
    rows.append(dict(id=m, name_vi=NAME[m], group=g, kind=k, in_scope=m in CORE or m in REG, level=lv if k in ('field', 'mixed') else None,
        monster_spawn_markers=s['markers'], spawn_target=(SP[m][1] if m in SP else s['markers']), has_monster_trigger=bool(s['trans_enemy']), apk_npc_slots=s['npcs'], apk_doors=s['doors'],
        respawn_to=(respawn(m, g) if g in {r[0] for r in REG.values()} | {'Khởi đầu', 'Emerald', 'Thành phố', 'Bãi biển', 'Hải Tặc Hào'} and k not in ('instance', 'guild_shared') else 'Quảng Trường Thạch Trụ')))
json.dump(rows, open('P12-S4-map-registry.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
KL = {'safe_hub': 'hub an toàn', 'field': 'bãi quái', 'mixed': 'hỗn hợp (NPC và quái)', 'instance': 'instance', 'private_per_player': 'riêng từng người chơi', 'guild_shared': 'chung theo bang', 'transit': 'trung chuyển', 'transit_once': 'dùng một lần'}
L = ['# P12 Stage 4 — Registry map canonical (đề xuất, chờ owner duyệt)\n', f'{len(rows)} map APK 3.2; {sum(r["in_scope"] for r in rows)} map trong phạm vi roster. Sinh bằng `gen_map_registry.py` từ `apk-extract/map-scan.json`.',
     'Loại map là suy luận: có trigger quái hoặc điểm spawn → bãi quái; không quái mà có NPC → hub an toàn; instance/riêng/chung theo bang là **đề xuất**, APK chưa có bằng chứng. Cấp quái ngoài 17 map là dải vùng (APK), chưa chia từng map.\n',
     '| Map | Nhóm | Loại | Cấp | Spawn APK → đề xuất | Slot NPC | Cửa | Hồi sinh về | Phạm vi |', '|---|---|---|---|---|---|---|---|---|']
for r in rows:
    L.append(f"| **{r['name_vi']}** (`{r['id']}`) | {r['group']} | {KL[r['kind']]} | {r['level'] or '—'} | {r['monster_spawn_markers']}{' → ' + str(r['spawn_target']) if r['spawn_target'] != r['monster_spawn_markers'] else ''} | {r['apk_npc_slots']} | {r['apk_doors']} | {r['respawn_to']} | {'có' if r['in_scope'] else 'không'} |")
open('P12-S4-map-registry.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
import collections; print(len(rows), collections.Counter(r['kind'] for r in rows))
