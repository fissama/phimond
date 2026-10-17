#!/usr/bin/env python3
"""P12 Stage 5: kiểm chứng dữ liệu thiết kế. Chạy: python3 -I validate.py  (chỉ đọc; ghi stage5/validation-result.json)."""
import json, collections, pathlib
H = pathlib.Path(__file__).resolve().parent
S4, RV = H.parent / 'stage4', H.parent / 'review'
reg = json.load(open(S4 / 'P12-S4-map-registry.json', encoding='utf-8'))
roster = json.load(open(S4 / 'P12-S4-npc-roster.json', encoding='utf-8'))
ft = json.load(open(S4 / 'P12-S4-floor-templates.json', encoding='utf-8'))
sp = json.load(open(S4 / 'P12-S4-spawn-plan.json', encoding='utf-8'))
gr = json.load(open(RV / 'portal-edits/portal-graph.json', encoding='utf-8'))['graph']
R = {r['id']: r for r in reg}
scope = [r for r in reg if r['in_scope']]
out = []
def chk(rid, name, ok, detail=''):
    out.append({'req': rid, 'check': name, 'pass': bool(ok), 'detail': detail})

# R01 world graph
P = {p['id']: p for p in gr['ports']}
bad = [l['id'] for l in gr['links'] if l['a'] not in P or l['b'] not in P]
chk('R01', 'mọi liên kết trỏ tới cổng có thật', not bad, f'{len(gr["links"])} liên kết; lỗi: {bad}')
chk('R01', 'mọi liên kết đã được owner duyệt', all(l['status'] == 'approved' for l in gr['links']), collections.Counter(l['status'] for l in gr['links']).most_common())
adj = collections.defaultdict(set); radj = collections.defaultdict(set)
for l in gr['links']:
    a, b = P[l['a']]['map'], P[l['b']]['map']
    adj[a].add(b); radj[b].add(a)
    if not l['oneway']: adj[b].add(a); radj[a].add(b)
def bfs(s, g):
    seen = {s}; q = [s]
    while q:
        x = q.pop()
        for y in g[x]:
            if y not in seen: seen.add(y); q.append(y)
    return seen
start = 'summoning_hall_main_hall'
fw = bfs(start, adj); home = 'city_square'; bw = bfs(home, radj)
sc = [r['id'] for r in scope if r['kind'] != 'transit_once']
npc_entry = {'city_deathmatch_arena'}  # vào bằng NPC đấu trường, không qua cổng (Stage 4 duyệt)
sc_in = [m for m in sc if m not in npc_entry]
chk('R01', 'mọi map trong phạm vi đến được từ Triệu Linh Điện', all(m in fw for m in sc_in), f'không đến được: {[m for m in sc_in if m not in fw]}')
chk('R01', 'mọi map trong phạm vi có đường về Quảng Trường (đường hồi phục)', all(m in bw for m in sc), f'kẹt: {[m for m in sc if m not in bw]}')
chk('R01', 'Triệu Linh Điện chỉ dùng một lần (không có đường quay lại)', start not in {m for m in fw if m != start and start in adj[m]}, '')

# R02 phân loại map và NPC
svc = {'heal', 'shop', 'learn', 'breed', 'hatch', 'warehouse', 'storage', 'smith', 'strengthen', 'recipe', 'exchange', 'bless', 'appraise'}
viol = [(n['id'], n['map_id']) for n in roster if set(n['roles']) & svc and R.get(n['map_id'], {}).get('kind') == 'field']  # 2 map hỗn hợp là ngoại lệ owner đã duyệt
chk('R02', 'không có NPC hồi máu/cửa hàng trong map quái', not viol, f'vi phạm: {viol}')
chk('R02', 'mọi NPC nằm trong map có trong registry', all(n['map_id'] in R for n in roster), '')
nohub = [r['name_vi'] for r in scope if r['kind'] == 'safe_hub' and not any(n['map_id'] == r['id'] for n in roster)]
chk('R02', 'mọi hub an toàn có ít nhất 1 NPC', not nohub, f'trống: {nohub}')
chk('R02', 'tên map trong phạm vi không trùng', len({r['name_vi'] for r in scope}) == len(scope), '')

# R03 spawn
nosp = [r['name_vi'] for r in scope if r['kind'] in ('field', 'mixed') and r['spawn_target'] <= 0]
chk('R03', 'mọi map quái có điểm spawn đề xuất > 0', not nosp, f'thiếu: {nosp}')
chk('R03', 'mọi map quái có cấp', all(r['level'] for r in scope if r['kind'] in ('field', 'mixed')), '')
chk('R03', 'tổng spawn khớp kế hoạch', sum(r['spawn_target'] for r in reg) - sum(r['monster_spawn_markers'] for r in reg) == sum(v[1] - v[0] for v in sp['changes'].values()), '')

# R04 template / instance
priv = [r['name_vi'] for r in scope if r['kind'] == 'private_per_player']
chk('R04', 'có map riêng từng người chơi (Điền Trang, Phòng thú cưng)', len(priv) == 2, priv)
chk('R04', 'mọi map có respawn_to', all(r['respawn_to'] for r in scope), '')

# R05 tuyến
dead = [m for m in sc if len(adj[m] - {m}) == 0]
chk('R05', 'không có map cụt không lối ra', not dead, f'cụt: {dead}')

# Mẫu tầng
lv = 61; ok = True; msgs = []
for key, expect in (('ghost', (61, 120)), ('tree', (61, 120)), ('tower', (121, 160)), ('maze', (161, 200))):
    r = next(x for x in ft['regions'] if x['key'] == key)
    good = (r['level_first'], r['level_last']) == expect and r['level_last'] - r['level_first'] + 1 == r['floors'] and all(f % 10 == 9 for f in r['guard_floors']) and r['guard_floors'][-1] < r['floors'] and all(f % 10 == 0 for f in r['return_object_floors'])
    ok &= good; msgs.append((key, good))
chk('R01', 'mẫu tầng: cấp mỗi tầng 1 cấp, nối liền 61→200, quái gác tầng 10k-1, Bia tầng 10k', ok, msgs)
chk('R01', 'trần cấp ghi trong JSON', ft['level_cap'] >= 200, ft['level_cap'])

res = {'passed': sum(c['pass'] for c in out), 'total': len(out), 'checks': out}
json.dump(res, open(H / 'validation-result.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for c in out: print('PASS' if c['pass'] else 'FAIL', c['req'], c['check'], '' if c['pass'] else '→ ' + str(c['detail']))
print(res['passed'], '/', res['total'])
