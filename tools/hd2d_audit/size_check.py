#!/usr/bin/env python3
"""Kiểm tỉ lệ asset theo vật thật (người chơi = 1.31 đơn vị ≈ 1.7 m, 1 đơn vị ≈ 1.3 m).
Dùng: size_check.py <manifest.json> [layout.json ...]
Lớp kích thước theo tên id: (regex, h_min, h_max, w_max). Khớp đầu tiên thắng.
Ngoài ra kiểm thứ tự tương đối (túi < ba lô < rương < lều) và, nếu có layout,
kích thước hiệu dụng (world×scale), vật nhỏ bị đè bởi vật lớn, vật đè NPC.
"""
import json, re, sys, pathlib
PLAYER = 1.31
CLASSES = [
 (r'sack|pouch',            0.25, 0.65, 0.8),
 (r'pack|backpack|satchel', 0.40, 1.10, 1.2),
 (r'crate|chest|barrel|box',0.40, 1.05, 1.3),
 (r'stove|brazier|pot\b',   0.40, 0.95, 1.1),
 (r'urn|jar|vase|pottery',  0.40, 1.10, 1.1),
 (r'tumbleweed',            0.40, 1.20, 1.4),
 (r'small-rock|pebble',     0.20, 0.85, 1.5),
 (r'small-cactus|small-',   0.20, 0.90, 1.2),
 (r'skull',                 0.30, 1.10, 1.5),
 (r'ribs',                  0.40, 1.50, 2.5),
 (r'banner|flag|signpost',  1.60, 3.80, 3.0),
 (r'tent-large',            2.20, 3.60, 5.0),
 (r'tent',                  1.40, 3.00, 3.8),
 (r'well',                  0.80, 1.80, 2.4),
 (r'stairs|steps',          0.50, 2.00, 4.0),
 (r'stele|obelisk',         1.80, 4.00, 2.6),
 (r'pillar-fallen',         0.60, 1.60, 5.0),
 (r'pillar',                2.00, 4.00, 2.6),
]
ORDER = [('sack','pack'),('pack','tent'),('sack','crate'),('crate','tent'),('urn','tent'),('stove','tent'),('sack','tent')]  # nhỏ < lớn (theo diện tích)
def cls(i):
    for rx,*r in CLASSES:
        if re.search(rx,i): return rx,r
    return None,None
def check_manifest(m):
    errs=[]; A={a['id']:a for a in m['assets']}
    for a in A.values():
        if a['category'] not in ('prop',): continue
        rx,r=cls(a['id'])
        if not r: continue
        w,h=a['world']; hmin,hmax,wmax=r
        if h>hmax or w>wmax: errs.append(f"SIZE {a['id']}: {w}×{h} vượt cỡ vật thật ({rx}: cao ≤{hmax}, rộng ≤{wmax}; người={PLAYER})")
        if h<hmin: errs.append(f"SIZE {a['id']}: cao {h} < tối thiểu {hmin} cho nhóm {rx}")
    def area(k):
        v=[x['world'][0]*x['world'][1] for i,x in A.items() if re.search(k,i) and x['category']=='prop']
        return min(v) if v else None
    for s,b in ORDER:
        sa=[x['world'][0]*x['world'][1] for i,x in A.items() if re.search(s,i) and x['category']=='prop']
        ba=[x['world'][0]*x['world'][1] for i,x in A.items() if re.search(b,i) and x['category']=='prop']
        if sa and ba and max(sa)>0.5*min(ba): errs.append(f"SIZE thứ tự: '{s}' (diện tích {max(sa):.2f}) phải nhỏ hơn hẳn '{b}' ({min(ba):.2f}), tối đa 50%")
    return errs
def check_layout(m,L,keepouts=()):
    errs=[]; A={a['id']:a for a in m['assets']}; boxes=[]
    for p in L['placements']:
        a=A.get(p['asset'])
        if not a or a['category']!='prop': continue
        sc=p.get('scale',1.0); w,h=a['world'][0]*sc,a['world'][1]*sc
        rx,r=cls(a['id'])
        if r and (h>r[1]*1.1 or w>r[2]*1.1): errs.append(f"SIZE layout {a['id']} scale {sc}: {w:.2f}×{h:.2f} vượt cỡ vật thật")
        x,y=p['px'][0]/100,p['px'][1]/100; boxes.append((a['id'],x-w/2,x+w/2,w*h,r is not None))
    for i,(ia,x0,x1,ar,small) in enumerate(boxes):
        if not small: continue
        for ib,y0,y1,br,_ in boxes:
            if ib==ia or br<=ar*2: continue
            ov=max(0,min(x1,y1)-max(x0,y0))/max(x1-x0,1e-6)
            if ov>0.85 and abs(((x0+x1)/2)-((y0+y1)/2))<0.3: errs.append(f"SIZE layout: {ia} bị che bởi {ib} (cùng vị trí)")
    return errs
if __name__=='__main__':
    m=json.load(open(sys.argv[1])); e=check_manifest(m)
    for lp in sys.argv[2:]: e+=check_layout(m,json.load(open(lp)))
    e=list(dict.fromkeys(e)); print('\n'.join(e) or 'size OK'); sys.exit(1 if e else 0)
