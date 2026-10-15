#!/usr/bin/env python3
"""Sinh ma trận portal Stage 4 cho 17 map trong phạm vi từ dữ liệu Stage 1 (chỉ đọc).
Dùng: python3 -I gen_portal_matrix.py <thư mục Phimond-P12-Review> <thư mục đầu ra>
Không sửa nguồn, không đụng runtime."""
import json, sys, os
from collections import defaultdict
src, out = sys.argv[1], sys.argv[2]
SCOPE = ['city_square','city_market','city_royal_palace','city_palace_gate','city_pet_room','city_farm',
 'city_deathmatch_arena','city_activity_hall','emerald_forest_main_woods','emerald_forest_deep_woods',
 'treasure_beach_fishermen_beach','treasure_beach_east_beach','treasure_beach_deep_sea',
 'treasure_beach_west_beach','treasure_beach_prosperity_island','summoning_hall_main_hall','middle_corridor_main_hall']
R = json.load(open(f'{src}/normalized-code-registry.json', encoding='utf-8'))
G = {g['portal_id']: g for g in json.load(open(f'{src}/portal-geometry-draft.json', encoding='utf-8'))['portal_geometry']}
maps = {m['id']: m for m in R['maps']}
rows = []
for p in R['portals']:
    g = G.get(p['id'], {})
    cands = g.get('source_map_candidates') or ([p['source_map_id']] if p.get('source_map_id') else [])
    dest = p.get('destination_map_id')
    if not (set(cands) & set(SCOPE) or dest in SCOPE): continue
    b = p['source_bindings'][0]
    rows.append(dict(portal_id=p['id'], source=cands, destination=dest, kind=p.get('transition_kind'),
        mode=b.get('mode_name_raw'), scene_param=b.get('scene_name_parameter_raw'), world_xy=g.get('world_xy'),
        vector_arrival=p.get('position_parameter'), level_param=p.get('level_parameter'),
        in_scope_src=bool(set(cands)&set(SCOPE)), in_scope_dst=dest in SCOPE, object=b.get('object_name_raw')))
json.dump(rows, open(f'{out}/portal-matrix.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
vi = lambda i: (maps[i]['display_name_vi'] if i in maps else str(i))
L = ['# P12 Stage 4 — Ma trận portal (sinh tự động, nguồn APK 3.2 + 8.4 trong Stage 1)\n',
 f'{len(rows)} portal chạm phạm vi (nguồn hoặc đích). Tên VI là tên APK (`display_name_vi`), **không phải** tên owner; tên owner xem `P12-world-names-master.md`.\n',
 'Cột *Đích/nguồn ngoài phạm vi* = portal đi ra/vào map ngoài 17 map, giữ để thấy dependency.\n']
by = defaultdict(list)
for r in rows:
    for s in (r['source'] or ['(không rõ nguồn)']): by[s].append(r)
for s in SCOPE + [k for k in by if k not in SCOPE]:
    if s not in by: continue
    L += [f'\n## {s} — {vi(s)}\n','| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |','|---|---|---|---|---|---|']
    for r in by[s]:
        xy = ', '.join(f'{v:.2f}' for v in r['world_xy']) if r['world_xy'] else '—'
        vv = ', '.join(f'{v:.2f}' for v in r['vector_arrival']) if r['vector_arrival'] else '—'
        L.append(f"| `{r['portal_id']}` | {r['mode']} | {r['destination']} | {'' if r['in_scope_dst'] else 'có'} | {xy} | {vv} |")
open(f'{out}/P12-S4-portal-matrix.md','w',encoding='utf-8').write('\n'.join(L)+'\n')
print(len(rows),'portals;', {s:len(v) for s,v in by.items() if s in SCOPE})
