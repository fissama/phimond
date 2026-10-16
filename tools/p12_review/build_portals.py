"""Sinh .ai/plan/phases/P12-world/review/portal-package.json: đồ thị điểm dịch chuyển (cửa APK ghép cặp + trụ theo quyết định owner).
Dùng: python3 tools/p12_review/build_portals.py [thư mục Phimond-P12-Review]   (mặc định ~/Downloads/Phimond-P12-Review; chỉ đọc)"""
import json, math, os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
PH = ROOT / '.ai/plan/phases/P12-world'
sys.path.insert(0, str(PH / 'stage4'))
from roster_outer import NAME, REGIONS
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else next((Path(os.path.expanduser(p)) for p in ('~/Downloads/Phimond-P12-Review', '~/mnt/Downloads/Phimond-P12-Review') if Path(os.path.expanduser(p)).exists()), Path('Phimond-P12-Review'))
OUT = PH / 'review/portal-package.json'
CORE = ['summoning_hall_main_hall', 'emerald_forest_main_woods', 'emerald_forest_deep_woods', 'city_square', 'city_market', 'city_palace_gate',
 'city_royal_palace', 'city_activity_hall', 'city_pet_room', 'city_farm', 'city_deathmatch_arena', 'treasure_beach_fishermen_beach',
 'treasure_beach_east_beach', 'treasure_beach_west_beach', 'treasure_beach_deep_sea', 'treasure_beach_prosperity_island', 'middle_corridor_main_hall']
GROUP = {'summoning_hall': 'Khởi đầu', 'emerald': 'Emerald', 'city': 'Thành phố', 'treasure_beach': 'Bãi biển', 'middle_corridor': 'Hải Tặc Hào'}
HIGH = {'astral': 'Tinh Không', 'ancient': 'Di Tích Cổ', 'ghost': 'Lâu Đài Ma', 'tree': 'Cây Thế Giới', 'tower': 'Tháp Chim', 'maze': 'Mê Thành'}
maps_ids = list(CORE)
region_of = {}
for key, rname, ms in REGIONS:
    for m in ms: maps_ids.append(m); region_of[m] = (rname, key in HIGH)
for m in CORE:
    pre = next(p for p in GROUP if m.startswith(p)); region_of[m] = (GROUP[pre], False)
SCOPE = set(maps_ids)
G = json.load(open(SRC / 'portal-geometry-draft.json', encoding='utf-8'))
VB = {r['map_id']: r['visual_bounds'] for r in G['map_visual_records']}
GEO = {g['portal_id']: g for g in G['portal_geometry']}
REG = json.load(open(SRC / 'normalized-code-registry.json', encoding='utf-8'))
npcs = json.load(open(PH / 'stage4/apk-extract/npcs.json', encoding='utf-8'))
def inb(m, x, y, pad=0.0):
    b = VB[m]; return b[0] - pad <= x <= b[2] + pad and b[1] - pad <= y <= b[3] + pad
def toward_center(m, xy, d=1.0):
    b = VB[m]; cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2; dx, dy = cx - xy[0], cy - xy[1]; n = math.hypot(dx, dy) or 1
    x, y = xy[0] + dx / n * d, xy[1] + dy / n * d
    return [round(min(max(x, b[0] + .3), b[2] - .3), 2), round(min(max(y, b[1] + .3), b[3] - .3), 2)]
doors = []
for p in REG['portals']:
    g = GEO.get(p['id'], {}); c = g.get('source_map_candidates') or ([p['source_map_id']] if p.get('source_map_id') else [])
    if not c or not g.get('world_xy'): continue
    pos = p.get('position_parameter') or [0, 0, 0]
    b = p['source_bindings'][0]
    doors.append(dict(id=p['id'], s=c[0], d=p.get('destination_map_id'), xy=[round(g['world_xy'][0], 2), round(g['world_xy'][1], 2)], vec=pos[:2],
                      mode=b.get('mode_name_raw'), scene=b.get('scene_name_parameter_raw')))
ports, links = {}, []
def add_port(pid, m, xy, kind, label, origin, flag=None):
    ports[pid] = dict(id=pid, map=m, xy=[round(xy[0], 2), round(xy[1], 2)], kind=kind, label=label, origin=origin, flag=flag); return pid
def add_link(a, b, oneway, origin, note, doors_=None, mode=None):
    links.append(dict(id=f'L{len(links) + 1:03d}', a=a, b=b, oneway=oneway, origin=origin, note=note, door_ids=doors_ or [], mode=mode,
                      status='pending', comment=''))
ext = {}
inscope = [d for d in doors if d['s'] in SCOPE]
for d in inscope: add_port('P:' + d['id'], d['s'], d['xy'], 'door', 'Cửa → ' + NAME.get(d['d'], str(d['d'])), 'apk')
used = set()
by_pair = {}
for d in inscope: by_pair.setdefault((d['s'], d['d']), []).append(d)
for (s, dd), A in sorted(by_pair.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
    if dd not in SCOPE:
        for a in A: used.add(a['id']); ext.setdefault(s, []).append(dict(door=a['id'], to=dd, name=NAME.get(dd, str(dd))))
        continue
    B = [x for x in by_pair.get((dd, s), []) if x['id'] not in used]
    for a in A:
        if a['id'] in used: continue
        best = None
        if B:
            valid = a['vec'] != [0, 0] and inb(dd, *a['vec'], pad=1.5)
            best = min(B, key=lambda b: math.dist(a['vec'], b['xy'])) if valid else B[0]
        if best is not None:
            B.remove(best); used.update([a['id'], best['id']])
            add_link('P:' + a['id'], 'P:' + best['id'], False, 'apk', 'Cửa hai chiều (ghép theo cửa đối ứng).', [a['id'], best['id']], a['mode'])
        else:
            used.add(a['id'])
            v = a['vec']
            back = by_pair.get((dd, s), [])
            if v != [0, 0] and inb(dd, *v, pad=0.5): xy, fl = v, None
            elif back: xy, fl = toward_center(dd, back[0]['xy']), 'đề xuất cạnh cửa đối ứng'
            else: b = VB[dd]; xy, fl = [round((b[0] + b[2]) / 2, 2), round(b[1] + 1.0, 2)], 'cần đặt'
            pid = add_port(f"A:{a['id']}", dd, xy, 'arrival', 'Điểm đến từ ' + NAME.get(s, s), 'apk' if not fl else 'proposed', fl)
            add_link('P:' + a['id'], pid, True, 'apk', 'Một chiều (không có cửa đối ứng).' + (' Điểm đến không có trong APK, đề xuất: ' + fl + '.' if fl else ''), [a['id']], a['mode'])
ext_in = {}
for d in doors:
    if d['s'] not in SCOPE and d['d'] in SCOPE: ext_in.setdefault(d['d'], []).append(dict(door=d['id'], frm=d['s'], name=NAME.get(d['s'], str(d['s']))))
# --- trụ (quyết định owner, §3 thiết kế) ---
def pillar_pos(m): return next(n['xy'] for n in npcs if n['map'][0] == m and n['name'] == 'TTTD')
def door_to(m, to):
    c = [p for p in ports.values() if p['map'] == m and p['kind'] == 'door' and p['id'][2:] in {d['id'] for d in doors if d['d'] == to}]
    return c[0] if c else None
sq = add_port('T:square', 'city_square', pillar_pos('city_square'), 'pillar', 'Trụ Quảng Trường', 'owner')
sh = add_port('T:ship', 'middle_corridor_main_hall', pillar_pos('middle_corridor_main_hall'), 'pillar', 'Trụ Hải Tặc Hào', 'owner')
def arrival(src_pillar, dest_map, back_to, label, note):
    dr = door_to(dest_map, back_to)
    if dr: xy, fl, org = toward_center(dest_map, dr['xy']), None, 'proposed'
    else: b = VB[dest_map]; xy, fl, org = [round((b[0] + b[2]) / 2, 2), round((b[1] + b[3]) / 2, 2)], 'cần đặt', 'proposed'
    pid = add_port(f"AT:{src_pillar[2:]}:{dest_map}", dest_map, xy, 'arrival', label, org, fl)
    add_link(src_pillar, pid, True, 'owner', note)
entry = lambda back: [m for m in maps_ids if door_to(m, back)]
for tgt, why in [('treasure_beach_east_beach', 'Owner Q2: trụ → Bờ Đông Ngọc Bích, từ đó vào Bến Ngư Châu.')]: arrival(sq, tgt, 'city_square', 'Đến từ trụ Quảng Trường', why)
for key, rname, ms in REGIONS:
    if key in HIGH or key in ('night',) and False: continue
for key, rname, ms in REGIONS:
    if key in HIGH: continue
    es = [m for m in ms if door_to(m, 'city_square')]
    for m in es: arrival(sq, m, 'city_square', 'Đến từ trụ Quảng Trường', f'Trụ → vùng {rname} (Lv1–40).')
arrival(sq, 'city_farm', 'city_square', 'Đến từ trụ Quảng Trường', 'Owner: Điền Trang vào bằng trụ.')
b = VB['middle_corridor_main_hall']; arrival(sq, 'middle_corridor_main_hall', None, 'Đến từ trụ Quảng Trường', 'Owner: trụ → Hải Tặc Hào (Lv40+).')
for key, rname, ms in REGIONS:
    if key not in HIGH: continue
    for m in [m for m in ms if door_to(m, 'middle_corridor_main_hall')]: arrival(sh, m, 'middle_corridor_main_hall', 'Đến từ trụ Hải Tặc Hào', f'Trụ tàu → vùng cao {rname}.')
arrival(sh, 'city_farm', 'city_square', 'Đến từ trụ Hải Tặc Hào', 'Owner: trụ tàu → Điền Trang.')
arrival(sh, 'city_square', None, 'Đến từ trụ Hải Tặc Hào', 'Owner: trụ tàu → Quảng Trường.')
maps = [dict(id=m, name=NAME.get(m, m), group=region_of[m][0], high=region_of[m][1], bounds=[round(v, 3) for v in VB[m]],
             size=[round((VB[m][2] - VB[m][0]) * 100), round((VB[m][3] - VB[m][1]) * 100)], ext_out=ext.get(m, []), ext_in=ext_in.get(m, [])) for m in maps_ids]
pkg = dict(schema_version=1, title='P12 · Điểm dịch chuyển', revision='P12-portals-20261016', maps=maps, ports=list(ports.values()), links=links,
           notes='Cửa lấy từ APK 3.2 (157 portal, trùng 8.4). Vị trí cửa là tọa độ APK trên ảnh ghép sprite tĩnh; điểm đến đề xuất cách cửa đối ứng khoảng 1 đơn vị.')
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(pkg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(len(maps), 'maps;', len(ports), 'ports;', len(links), 'links;', sum(1 for l in links if l['origin'] == 'apk'), 'apk;', sum(1 for p in ports.values() if p['flag'] == 'cần đặt'), 'cần đặt;', sum(1 for p in ports.values() if p['flag'] and p['flag'] != 'cần đặt'), 'đề xuất')
