#!/usr/bin/env python3
"""Dựng map thử HD-2D 'tomb_hd2d' từ batch-11-tomb (pilot Revision 3).
Bao gồm:
- Tường thành xa: tomb-necropolis-wall-far (z=-2.85)
- Sàn đất nghĩa địa: tomb-graveyard-dirt (phủ từ z0=-9.2 đến z1=4.5)
- Đường gạch lát: tomb-brick-floor (z=3.2)
- Decal chuyển tiếp: tomb-tile-edge-decal (z=-0.8)
- Các prop: bia mộ, quan tài đá, cổng vòm, cổng dịch chuyển, đèn lồng u linh (4 frame)
Xuất apps/game-web/public/scenes/tomb_hd2d.json + texture hd2d_*.png.
"""
import json, random, shutil, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
B = f'{R}/apps/game-web/art-src/hd2d/batch-11-tomb'
OUT = f'{R}/apps/game-web/public/scenes'
man = {a['id']: a for a in json.load(open(f'{B}/manifest.json'))['assets']}
used = {}
def tex(aid):
    n = f'hd2d_{aid}.png'
    shutil.copyfile(f'{B}/{aid}/final.png', f'{OUT}/tex/{n}')
    used[aid] = n
    return n

rnd = random.Random(1016)
X0, X1, Z0, Z1 = -6.13, 24.73, -2.4, 3.6
props, flats, back = [], [], []

def prop(aid, x, z, **kw):
    w, h = man[aid]['world']
    p = dict(tex=tex(aid), x=round(x, 3), z=round(z, 3), w=w, h=h)
    p.update(kw)
    props.append(p)

# ---- nền xa (chân trời tường thành lăng mộ nghĩa địa đêm, neo sát chân đất)
w_far, h_far = man['tomb-necropolis-wall-far']['world']
for k in range(-1, 3):
    back.append(dict(tex=tex('tomb-necropolis-wall-far'), x=round(10.0 + k * w_far, 3), z=-2.85, w=w_far, h=h_far))

# ---- sàn đất nghĩa địa phủ kín sâu ra sau (z0=-9.2) để không lộ khoảng trống chân tường
floor = [dict(tex=tex('tomb-graveyard-dirt'), x0=-15.6, x1=34.2, z0=-9.2, z1=4.5, tw=4.0, td=4.0)]

# ---- decal chuyển tiếp và đường lát gạch lăng mộ
x = -16.0
while x < 34:
    flats.append(dict(tex=tex('tomb-tile-edge-decal'), x=round(x + 2, 3), z=-0.8, w=4.0, d=4.0))
    flats.append(dict(tex=tex('tomb-brick-floor'), x=round(x + 2, 3), z=3.2, w=4.0, d=4.0))
    x += 4.0

# ---- cổng vào & cổng ra
prop('tomb-arch-gate', -4.3, -1.7)
prop('tomb-portal-dormant', 23.2, -0.9)

# ---- bia mộ hai bên lối đi
for gx in [-3.2, -1.2, 1.2, 3.6, 6.2, 8.8, 11.2, 13.8, 16.2, 18.8, 21.2]:
    prop(rnd.choice(['tomb-gravestone-01', 'tomb-gravestone-02']), gx + rnd.uniform(-0.3, 0.3), rnd.uniform(-2.4, -1.7))
for gx in [-2.6, 5.6, 12.2, 18.4]:
    prop(rnd.choice(['tomb-gravestone-01', 'tomb-gravestone-02']), gx, rnd.uniform(2.6, 3.2))

# ---- quan tài đá cổ
for gx in [2.5, 9.0, 15.0, 21.0]:
    prop('tomb-sarcophagus-01', gx, rnd.uniform(-1.0, -0.3))

# ---- đèn lồng linh hồn (animation 4 frames)
lw, lh = man['tomb-lantern-spirit']['world']
for lx in [-2.2, 3.0, 8.0, 13.0, 18.0, 22.0]:
    props.append(dict(tex=tex('tomb-lantern-spirit'), x=lx, z=round(rnd.uniform(1.8, 2.4), 3), w=round(lw/4, 3), h=lh, frames=4, fps=5))

props.sort(key=lambda p: p['z'])
scene = dict(id='tomb_hd2d', name='Lăng Mộ HD-2D (thử)', floor=floor, flats=flats, back=back, props=props, lights=[],
  particles=[dict(kind='dust', count=40, color=[0.55, 0.9, 0.8], size=0.06), dict(kind='ember', count=14, color=[0.4, 1.0, 0.8], size=0.08)],
  anim=[], water=None, bg=[0.06, 0.10, 0.13], len=[-7.131, 25.731], ambient=dict(color=[0.75, 0.90, 0.95], strength=2.0),
  grade=dict(sat=1.05, contrast=1.04, warm=-0.04, vignette=0.35, fog=[0.10, 0.18, 0.20], fogNear=22, fogFar=52),
  walk=dict(x0=X0, x1=X1, z0=Z0, z1=Z1))

json.dump(scene, open(f'{OUT}/tomb_hd2d.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('props', len(props), 'flats', len(flats), 'back', len(back), 'tex', len(used))
