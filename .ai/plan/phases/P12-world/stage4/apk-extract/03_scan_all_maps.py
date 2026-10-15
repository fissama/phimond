#!/usr/bin/env python3
"""Quét mọi map trong APK 3.2 (chỉ đọc): đếm trigger quái (TransEnemy), điểm spawn đánh số, NPC, cửa theo từng map.
Cần UnityPy==1.25.3, attrs>=23. Dùng: python3 -I 03_scan_all_maps.py <APK 3.2> <portal-geometry-draft.json> <đầu ra .json>"""
import sys, json, zipfile, collections, UnityPy
apk, geom, outp = sys.argv[1:4]
env = UnityPy.load(zipfile.ZipFile(apk).read('assets/bin/Data/data.unity3d'))
G = json.load(open(geom, encoding='utf-8'))
vb = collections.defaultdict(dict)
for r in G['map_visual_records']:
    vb[r['serialized_file']][r['map_id']] = r['visual_bounds']
byf = collections.defaultdict(dict)
for o in env.objects:
    byf[o.assets_file.name][o.path_id] = o
res = {}
for f, maps in vb.items():
    objs = byf[f]; tr = {}; go = {}
    for pid, o in objs.items():
        if o.type.name == 'Transform':
            d = o.read(); tr[pid] = (d.m_GameObject.path_id, d.m_Father.path_id, (d.m_LocalPosition.x, d.m_LocalPosition.y), (d.m_LocalScale.x, d.m_LocalScale.y))
        elif o.type.name == 'GameObject':
            d = o.read(); go[pid] = (d.m_Name, [c.component.path_id for c in d.m_Component])
    def world(t):
        chain = []
        while t in tr and t:
            chain.append(t); t = tr[t][1]
        px = py = 0; sx = sy = 1
        for c in reversed(chain):
            lp, ls = tr[c][2], tr[c][3]; px += lp[0]*sx; py += lp[1]*sy; sx *= ls[0]; sy *= ls[1]
        return px, py
    def owner(x, y):
        c = [(((b[2]-b[0])*(b[3]-b[1])), m) for m, b in maps.items() if b[0]-1 <= x <= b[2]+1 and b[1]-1 <= y <= b[3]+1]
        return min(c)[1] if c else None
    for m in maps: res[m] = dict(file=f, trans_enemy=0, markers=0, npcs=0, doors=0)
    npc_parent = {t for t, v in tr.items() if go[v[0]][0] == 'AllNpc'}
    for t, v in tr.items():
        name, comps = go[v[0]]
        kinds = {objs[c].type.name for c in comps if c in objs}
        m = owner(*world(t))
        if not m: continue
        if name == 'TransEnemy': res[m]['trans_enemy'] += 1
        elif name.isdigit() and 'MonoBehaviour' in kinds: res[m]['markers'] += 1
        elif v[1] in npc_parent and 'CapsuleCollider2D' in kinds and 'MonoBehaviour' in kinds: res[m]['npcs'] += 1
        elif name.startswith('Door') and 'MonoBehaviour' in kinds: res[m]['doors'] += 1
json.dump(res, open(outp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(res), 'maps')
