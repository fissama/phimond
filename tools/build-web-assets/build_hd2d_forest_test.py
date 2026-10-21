#!/usr/bin/env python3
"""Dựng map thử HD-2D 'forest_hd2d' từ asset batch-01-octopath (không dùng asset placeholder).
Xuất apps/game-web/public/scenes/forest_hd2d.json + texture hd2d_*.png. Chạy lại là ra cùng kết quả (seed cố định)."""
import json, random, shutil, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
B = f'{R}/apps/game-web/art-src/hd2d/batch-01-octopath'
OUT = f'{R}/apps/game-web/public/scenes'
man = {a['id']: a for a in json.load(open(f'{B}/manifest.json'))['assets']} if isinstance(json.load(open(f'{B}/manifest.json')), dict) else {a['id']: a for a in json.load(open(f'{B}/manifest.json'))}
used = {}
def tex(aid, src=None):
    name = f'hd2d_{aid}.png'
    s = src or f'{B}/{aid}/final.png'
    shutil.copyfile(s, f'{OUT}/tex/{name}'); used[aid] = name; return name
def wh(aid): return man[aid]['world']
rnd = random.Random(20261015)
X0, X1, Z0, Z1 = -6.13, 24.73, -2.4, 3.6
props, flats, back = [], [], []
def prop(aid, x, z, **kw):
    w, h = wh(aid); s = kw.pop('s', 1.0)
    p = dict(tex=tex(aid), x=round(x, 3), z=round(z, 3), w=round(w*s, 3), h=round(h*s, 3)); p.update(kw); props.append(p)
def tree(n, x, z, s=1.0):
    t = f'tree-large-0{n}'
    prop(f'{t}-trunk', x, z, s=s)
    prop(f'{t}-canopy', x, z+0.001, y=round(0.859375*s, 3), s=s, sway=1)

# ---- nền xa (3 lớp liên tục, phủ kín không gian sau)
# 1. Tường thành cây rừng xa (far wall)
w_far, h_far = wh('forest-wall-far')
for k in range(-1, 3):
    back.append(dict(tex=tex('forest-wall-far'), x=round(14.3+k*w_far, 3), z=-3.45, w=w_far, h=h_far, far=1))

# 2. Tán lá vòm cây giữa (mid canopy - lặp liền mạch theo trục X)
w_mid, h_mid = wh('forest-canopy-mid')
for k in range(-2, 4):
    back.append(dict(tex=tex('forest-canopy-mid'), x=round(10.0+k*w_mid, 3), z=-3.25, w=w_mid, h=h_mid, far=1, sway=1))

# 3. Bụi rậm hàng rào tiền cảnh rừng (front hedge - chắn chân tường, có lề trên >=8px alpha, hình bụi tự nhiên)
w_front, h_front = wh('forest-hedge-front')
for k in range(-2, 4):
    back.append(dict(tex=tex('forest-hedge-front'), x=round(10.0+k*w_front, 3), z=-2.95, w=w_front, h=h_front))

# ---- sàn: cỏ chạy sâu ra sau (z0=-9.2) để phủ kín hoàn toàn chân tường xa, không còn khe trống
floor = [dict(tex=tex('grass-floor-01'), x0=-15.6, x1=34.2, z0=-9.2, z1=4.5, tw=4.0, td=4.0)]
x = -16.0
while x < 34:
    flats.append(dict(tex=tex('edge-grass-dirt'), x=round(x+2, 3), z=1.2, w=4.0, d=4.0))
    # Xen kẽ dirt-floor-01 và dirt-floor-02 (cả hai đều khớp chuẩn mép đất của edge)
    dirt_tex = 'dirt-floor-01' if int(x/4) % 2 == 0 else 'dirt-floor-02'
    flats.append(dict(tex=tex(dirt_tex), x=round(x+2, 3), z=-2.8, w=4.0, d=4.0))
    x += 4.0

# ---- decal nhỏ
for aid, n in [('pebbles-01', 6), ('pebbles-02', 5), ('pebbles-03', 5), ('fallen-leaves-01', 7), ('fallen-leaves-02', 7), ('fallen-leaves-03', 6), ('moss-patch-01', 5), ('moss-patch-02', 4), ('mud-patch', 2)]:
    for _ in range(n):
        w, h = wh(aid); flats.append(dict(tex=tex(aid), x=round(rnd.uniform(X0-1, X1+1), 3), z=round(rnd.uniform(-2.6, 2.4), 3), w=w, d=h))
w, h = wh('mushroom-ring'); flats.append(dict(tex=tex('mushroom-ring'), x=9.0, z=-1.2, w=w, d=h))

# ---- hàng cây sau (z -3.0..-2.0) và hai bên
for i, x in enumerate([-5.5, -2.8, 0.2, 3.1, 6.3, 9.4, 12.6, 15.5, 18.6, 21.4, 24.2]):
    tree(1 + (i*2) % 3, x + rnd.uniform(-0.4, 0.4), rnd.uniform(-3.0, -2.2), s=rnd.uniform(0.95, 1.2))
for x in [-4.2, 7.7, 14.2, 22.8]:
    tree(1 + rnd.randrange(3), x, rnd.uniform(-1.5, -0.9), s=rnd.uniform(0.85, 1.0))
for aid, xs in [('tree-small-01', [1.5, 11.0, 19.8]), ('tree-small-02', [-3.5, 16.8, 23.5])]:
    for x in xs: prop(aid, x, rnd.uniform(-2.0, -0.4))

# ---- bụi, đá, thân cây đổ, rễ, nấm, hoa, cỏ
spots = lambda n, zr: [(rnd.uniform(X0, X1), rnd.uniform(*zr)) for _ in range(n)]
for aid, n, zr in [('bush-01', 7, (-2.4, 1.2)), ('bush-02', 6, (-2.4, 1.2)), ('bush-03', 6, (-2.4, 1.2)), ('flower-bush', 5, (-2.0, 1.8)),
                   ('rock-small', 6, (-1.6, 3.4)), ('rock-medium', 4, (-1.6, 3.0)), ('rock-large', 2, (-2.0, 0.2)), ('stump', 3, (-1.5, 2.0)), ('mushroom-ochre', 5, (-1.5, 2.5)),
                   ('mushroom-violet', 5, (-1.5, 2.5)), ('fern-01', 8, (-2.2, 3.0)), ('fern-02', 8, (-2.2, 3.0)), ('moss-pillar', 2, (-1.8, -0.8)), ('reed-clump', 3, (0.2, 2.5))]:
    for x, z in spots(n, zr):
        prop(aid, x, z, **({'sway': 1} if man[aid]['sway'] else {}))
for aid, n in [('grass-01', 14), ('grass-02', 14), ('grass-03', 12), ('grass-04', 10), ('flower-red', 8), ('flower-yellow', 8), ('flower-purple', 8), ('flower-white', 8)]:
    for x, z in spots(n, (-2.3, 3.4)): prop(aid, x, z, sway=1)
prop('fallen-log', 5.0, 0.0); prop('exposed-roots', 13.0, -0.6); prop('exposed-roots', -2.0, -1.0, s=0.9)
prop('signpost-blank', 22.4, 2.2)
prop('forest-portal-dormant', 24.2, -0.6)   # lối ra (trụ ngủ)
prop('wooden-exit-gate', -5.2, -0.5)         # cổng gỗ phía trái
props.sort(key=lambda p: p['z'])
scene = dict(id='forest_hd2d', name='Rừng HD-2D (thử)', floor=floor, flats=flats, back=back, props=props, lights=[],
  particles=[dict(kind='pollen', count=70, color=[1, 0.95, 0.55], size=0.07), dict(kind='leaf', count=18, color=[0.55, 0.85, 0.35], size=0.16)],
  anim=[dict(type='shaft', x=round(x, 2), z=round(rnd.uniform(-2, 0), 2), w=round(rnd.uniform(1.4, 2.4), 2), h=7.0, a=round(rnd.uniform(0.09, 0.14), 2), color=[1.0, 0.95, 0.7], phase=round(rnd.uniform(0, 6.28), 3)) for x in range(-4, 26, 4)],
  water=None, bg=[0.09, 0.24, 0.2], len=[-7.131, 25.731], ambient=dict(color=[0.78, 0.92, 0.86], strength=1.0),
  grade=dict(sat=1.08, contrast=1.06, warm=0.04, vignette=0.32, fog=[0.52, 0.74, 0.72], fogNear=26, fogFar=58),
  walk=dict(x0=X0, x1=X1, z0=Z0, z1=Z1))
json.dump(scene, open(f'{OUT}/forest_hd2d.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('props', len(props), 'flats', len(flats), 'back', len(back), 'tex', len(used))
