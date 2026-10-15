#!/usr/bin/env python3
"""Trích vị trí trigger quái (TransEnemy) và điểm spawn đánh số của map Emerald + Bãi biển trong APK 3.2, chỉ đọc.
Cần UnityPy==1.25.3, attrs>=23. Dùng: python3 04_extract_spawn_markers.py <APK 3.2> <portal-geometry-draft.json> <đầu ra spawn-markers.json>"""
import sys, json, zipfile, collections, UnityPy
apk, geom, outp = sys.argv[1:4]
env = UnityPy.load(zipfile.ZipFile(apk).read('assets/bin/Data/data.unity3d'))
G = json.load(open(geom, encoding='utf-8'))
vb = {r['map_id']: (r['serialized_file'], r['visual_bounds']) for r in G['map_visual_records'] if r['map_id'].startswith(('emerald', 'treasure_beach'))}
byf = collections.defaultdict(dict)
for o in env.objects: byf[o.assets_file.name][o.path_id] = o
out = {}
for f in sorted({v[0] for v in vb.values()}):
    objs = byf[f]; tr = {}; go = {}
    for pid, o in objs.items():
        if o.type.name == 'Transform':
            d = o.read(); tr[pid] = (d.m_GameObject.path_id, d.m_Father.path_id, (d.m_LocalPosition.x, d.m_LocalPosition.y), (d.m_LocalScale.x, d.m_LocalScale.y))
        elif o.type.name == 'GameObject':
            d = o.read(); go[pid] = (d.m_Name, [c.component.path_id for c in d.m_Component], d.m_IsActive)
    def world(t):
        chain = []
        while t in tr and t: chain.append(t); t = tr[t][1]
        px = py = 0; sx = sy = 1
        for c in reversed(chain):
            lp, ls = tr[c][2], tr[c][3]; px += lp[0]*sx; py += lp[1]*sy; sx *= ls[0]; sy *= ls[1]
        return px, py
    for t, v in tr.items():
        n, comps, act = go[v[0]]
        if 'MonoBehaviour' in [objs[c].type.name for c in comps if c in objs] and (n.isdigit() or n == 'TransEnemy'):
            x, y = world(t)
            for k, (ff, b) in vb.items():
                if ff == f and b[0]-1 <= x <= b[2]+1 and b[1]-1 <= y <= b[3]+1:
                    out.setdefault(k, []).append((n, round(x, 2), round(y, 2), act))
res = {}
for k, v in out.items():
    mk = [a for a in v if a[0] != 'TransEnemy']
    res[k] = dict(trans_enemy=[a[1:3] for a in v if a[0] == 'TransEnemy'], markers=len(mk), marker_xy=[a[1:3] for a in mk])
json.dump(res, open(outp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(res), 'map')
