#!/usr/bin/env python3
"""Sinh 5 cảnh HD-2D (severa, forest, beach, ranch, arena) cho apps/game-web.

  python3 tools/build-web-assets/build_scenes.py [--out apps/game-web/public/scenes]

Nguồn: lớp sprite Unity trích từ APK (source/sprites + meta.json) + vật trang trí pixel-art gốc (pixelart.py).
Tọa độ: x thế giới = x 2D; z = -KZ * (y2D + yoff); mặt sàn y = 0. 40 px = 1 đơn vị.
"""
import argparse, hashlib, json, math, os, random
from PIL import Image
import pixelart as PA

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
KZ = 1.5
PPU = 40.0
ap = argparse.ArgumentParser()
ap.add_argument('--out', default=os.path.join(ROOT, 'apps/game-web/public/scenes'))
ap.add_argument('--sprites', default=os.path.join(HERE, 'source/sprites'))
args = ap.parse_args()
META = json.load(open(os.path.join(args.sprites, 'meta.json')))
TEX = os.path.join(args.out, 'tex'); os.makedirs(TEX, exist_ok=True)
_saved = {}

def save_tex(im, hint):
    im = im.convert('RGBA')
    h = hashlib.sha1(im.tobytes() + str(im.size).encode()).hexdigest()[:10]
    if h in _saved: return _saved[h]
    name = f'{hint}_{h}.webp'
    im.save(os.path.join(TEX, name), 'WEBP', lossless=True, method=6)
    _saved[h] = name
    return name

def load_sprite(e):
    return Image.open(os.path.join(args.sprites, e['file'])).convert('RGBA')

class Scene:
    def __init__(self, sid, root, yoff, name):
        self.id, self.root, self.yoff = sid, root, yoff
        self.d = dict(id=sid, name=name, floor=[], flats=[], back=[], props=[], lights=[], particles=[], anim=[], water=None)
        self.entries = META[root]
        self.bg = None
    def z(self, y): return round(-KZ * (y + self.yoff), 3)
    def by(self, sprite, nth=None):
        r = [e for e in self.entries if e['sprite'] == sprite]
        return r if nth is None else r[nth]
    def bgcolor(self):
        e = [e for e in self.entries if e['sprite'] == 'Square'][0]
        px = Image.open(os.path.join(args.sprites, e['file'])).convert('RGBA').getpixel((1, 1))
        return [round(c / 255, 4) for c in px[:3]]
    def tex(self, e):
        return save_tex(load_sprite(e), f"{self.id}_{e['sprite'].replace('.', '_').replace(' ', '')}")
    # đặt sprite nguồn dạng đứng (billboard)
    def src_prop(self, e, kind='props', **kw):
        cx = e['x'] + e['w'] / 2; ybot = e['top'] - e['h']
        p = dict(tex=self.tex(e), x=round(cx, 3), z=self.z(ybot), w=round(e['w'], 3), h=round(e['h'], 3), _s=e['sprite'])
        p.update(kw)
        self.d[kind].append(p); return p
    def floor(self, tex_name, x0, x1, y_far, y_near, tw, td, **kw):
        f = dict(tex=tex_name, x0=x0 - 7.0, x1=x1 + 7.0, z0=self.z(y_far), z1=self.z(y_near), tw=tw, td=round(td * KZ, 3)); f.update(kw); self.d['floor'].append(f)
    def flat(self, tex_name, x, y, w, d, **kw):
        """decal nằm trên sàn: tâm (x,y2D), rộng w, sâu d (đơn vị thế giới)."""
        p = dict(tex=tex_name, x=round(x, 3), z=self.z(y), w=round(w, 3), d=round(d, 3)); p.update(kw); self.d['flats'].append(p)
    def prop(self, tex_name, x, y, w=None, h=None, px=None, **kw):
        if px is not None: w, h = px[0] / PPU, px[1] / PPU
        p = dict(tex=tex_name, x=round(x, 3), z=self.z(y), w=round(w, 3), h=round(h, 3)); p.update(kw); self.d['props'].append(p); return p
    def light(self, x, y, h, color, radius, intensity=1.0, flicker=0.0):
        self.d['lights'].append(dict(x=round(x, 3), y=h, z=self.z(y), color=color, radius=radius, intensity=intensity, flicker=flicker))


CELLS_EXT = 10   # mỗi bên thêm 10 ô lưới (lưới 40 → 60)

def ext_len(x0, x1, ml, mr):
    """Độ dài (đơn vị thế giới) của 10 ô lưới, giữ nguyên kích thước ô để các mốc không lệch."""
    return CELLS_EXT * (x1 - x0 - ml - mr) / 39.0

def extend_src(S, x0, x1, E, left=None, right=None, include=None, outward=None, copies=()):
    """Mở rộng cảnh ra E mỗi bên: dời đồ ở mép ra mép mới, lát lại cửa sổ (a,b) của đồ nguồn vào dải mới."""
    include = include or (lambda p: True)
    for key in ('props', 'flats'):
        for p in S.d[key]:
            sp = p.get('_s')
            if outward and sp and outward(p):
                p['x'] = round(p['x'] + (-E if p['x'] < (x0 + x1) / 2 else E), 3)
            elif p['x'] < x0 - 0.6: p['x'] = round(p['x'] - E, 3)
            elif p['x'] > x1 + 0.6: p['x'] = round(p['x'] + E, 3)
    base = [dict(p) for p in S.d['props'] if p.get('_s') and include(p)]
    for side, win in ((-1, left), (1, right)):
        if not win: continue
        a, b = win; wd = b - a; sel = [p for p in base if a <= p['x'] < b]; k = 1
        while (k - 1) * wd < E:
            sh = (-(a - x0) - k * wd) if side < 0 else ((x1 - b) + k * wd)
            for p in sel:
                nx = p['x'] + sh
                if (side < 0 and x0 - E - 0.2 < nx < x0 - 0.15) or (side > 0 and x1 + 0.15 < nx < x1 + E + 0.2):
                    S.d['props'].append(dict(p, x=round(nx, 3)))
            k += 1
    for b in [q for q in S.d['back']]:
        w = b['w'] * 0.985; k = 1
        while b['x'] - k * w > x0 - E - 8: S.d['back'].append(dict(b, x=round(b['x'] - k * w, 3))); k += 1
        k = 1
        while b['x'] + k * w < x1 + E + 8: S.d['back'].append(dict(b, x=round(b['x'] + k * w, 3))); k += 1
    for f in S.d['floor']: f['x0'] = round(f['x0'] - E, 3); f['x1'] = round(f['x1'] + E, 3)
    if S.d.get('water'): S.d['water']['x0'] -= E; S.d['water']['x1'] += E
    S.d['len'] = [round(x0 - E, 3), round(x1 + E, 3)]

def strip_tags(d):
    for key in ('props', 'flats', 'back'):
        for p in d.get(key, []): p.pop('_s', None)

def forest_lib(hint):
    ents = {e['sprite']: e for e in META['level4:rungsau']}
    out = {}
    for k in ('10_0', '9_0', '4_0', '3_0', '15_0'):
        e = ents[k]; out[k] = (save_tex(load_sprite(e), f'{hint}_{k}'), e['w'], e['h'])
    return out

def tree_wall(S, rnd, edge, sg, z_far, z_near, lib, tall=1.6):
    """Tường cây + bụi liền mạch ở mép bản đồ (cây lớn ở phía xa, bụi/dương xỉ phía gần), không để lộ nền."""
    z = z_far
    while z < z_near + 0.4:
        tx = edge + sg * (0.9 + rnd.random() * 0.7)
        if z < z_far + tall:
            t, w, h = lib[rnd.choice(('10_0', '9_0'))]; s_ = 1.0 + rnd.random() * 0.3
        else:
            t, w, h = lib[rnd.choice(('4_0', '4_0', '3_0'))]; s_ = 1.0 + rnd.random() * 0.35
        S.d['props'].append(dict(tex=t, x=round(tx, 3), z=round(z, 3), w=round(w * s_, 3), h=round(h * s_, 3), sway=1))
        z += 1.0 + rnd.random() * 0.5

def decal_tex(im, hint): return save_tex(im, hint), im.width / PPU, im.height / PPU

def scatter(rnd, n, x0, x1, y0, y1, avoid, min_d=0.6, tries=3000):
    pts = []; t = 0
    while len(pts) < n and t < tries:
        t += 1; x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1)
        if any(math.hypot(x - ax, (y - ay) * KZ) < ar for ax, ay, ar in avoid): continue
        if any(math.hypot(x - px, (y - py) * KZ) < min_d for px, py in pts): continue
        pts.append((x, y))
    return pts

def place_decor(S, rnd, kind_list, n, x0, x1, y0, y1, avoid, min_d=0.6, scale=(0.9, 1.1), flat=False, **kw):
    for (x, y) in scatter(rnd, n, x0, x1, y0, y1, avoid, min_d):
        name, w, h = rnd.choice(kind_list); s = rnd.uniform(*scale)
        if flat: S.flat(name, x, y, w * s, h * s * 1.0, **kw)
        else: S.prop(name, x, y, w * s, h * s, **kw)

def lib_grass(prefix, n=4, greens=('#2f7a2a', '#4fa83a', '#8ad04a')):
    return [decal_tex(PA.tuft(i, greens=greens), f'{prefix}_tuft{i}') for i in range(n)]

def lib_flowers(prefix, cols):
    out = []
    for i, (pet, cen) in enumerate(cols): out.append(decal_tex(PA.flower(i, pet, cen), f'{prefix}_flower{i}'))
    return out

def glow_tex(col, name): return save_tex(PA.glow(96, col), f'glow_{name}')

# ------------------------------------------------------------------ FOREST
def forest():
    S = Scene('forest', 'level4:rungsau', 0.0, 'Rừng Lục Bảo'); rnd = random.Random(7)
    x0, x1 = -1.9, 20.5
    S.d['bg'] = [0.16, 0.42, 0.34]; S.d['len'] = [x0, x1]
    gtex = save_tex(PA.ground_tile(3, 160, 96, ['#264f24', '#356b2c', '#4a8a36', '#69a845'], blade_n=90, speck_n=50, litter=['#6b4a2a', '#8a6a3a', '#a07a3c'], litter_n=26), 'forest_ground')
    S.floor(gtex, x0 - 1.5, x1 + 1.5, 2.3, -3.0, 4.0, 1.6)
    for e in S.entries:
        if e['sprite'] in ('Square', '1_0'): continue
        if e['sprite'] == '16_0': S.src_prop(e, 'back', far=1); continue
        sway = e['sprite'] in ('2_0', '3_0', '4_0', '5_0', '6_0', '7_0', '9_0', '10_0', '15_0')
        S.src_prop(e, sway=1 if sway else 0, front=1 if e['order'] >= 1 else 0)
    E = ext_len(x0, x1, 1.0, 1.0); X0, X1 = x0 - E, x1 + E
    extend_src(S, x0, x1, E, left=(0.0, 5.2), right=(14.3, 19.5))
    # cây xa, mờ sương
    props = {e['sprite']: e for e in S.entries}
    tree = [S.tex(props['10_0']), S.tex(props['9_0'])]; tsz = {tree[0]: (props['10_0']['w'], props['10_0']['h']), tree[1]: (props['9_0']['w'], props['9_0']['h'])}
    zb = S.z(2.3)
    x = X0 - 6
    while x < X1 + 6:
        t = rnd.choice(tree); w, h = tsz[t]; s = 1.35 + rnd.random() * 0.25
        S.d['props'].append(dict(tex=t, x=round(x, 3), z=round(zb - 1.6 - rnd.random() * 1.2, 3), w=round(w * s, 3), h=round(h * s, 3), sway=1, haze=1)); x += 3.4 + rnd.random() * 1.4
    bush = S.tex(props['4_0']); fern = S.tex(props['3_0']); fl = S.tex(props['6_0']); small = S.tex(props['2_0']); hedge = S.tex(props['15_0'])
    hs = (props['15_0']['w'], props['15_0']['h'])
    x = X0 - 3
    while x < X1 + 3:
        S.d['props'].append(dict(tex=hedge, x=round(x, 3), z=round(zb + 0.2 + rnd.random() * 0.5, 3), w=round(hs[0] * 0.95, 3), h=round(hs[1] * 0.95, 3), sway=1)); x += 3.3
    zf = S.z(-3.0)
    for edge, sg in ((X0, -1), (X1, 1)):
        z = zb + 0.3
        while z < zf + 0.4:
            tx = edge + sg * (0.9 + rnd.random() * 0.7)
            if z < zb + 1.6:
                t = rnd.choice(tree); w, h = tsz[t]; s = 1.0 + rnd.random() * 0.3
                S.d['props'].append(dict(tex=t, x=round(tx, 3), z=round(z, 3), w=round(w * s, 3), h=round(h * s, 3), sway=1))
            else:
                t = rnd.choice([bush, bush, fern]); w, h = (props['4_0']['w'], props['4_0']['h']) if t == bush else (props['3_0']['w'], props['3_0']['h']); s = 1.0 + rnd.random() * 0.35
                S.d['props'].append(dict(tex=t, x=round(tx, 3), z=round(z, 3), w=round(w * s, 3), h=round(h * s, 3), sway=1))
            z += 1.0 + rnd.random() * 0.5
    # trang trí tầng sàn (HD-2D): cỏ, hoa, đá, lá rụng
    greens = lib_grass('fo', 4, ('#1f5a22', '#3a8a30', '#6fc040'))
    flowers = lib_flowers('fo', [('#ffffff', '#ffd84a'), ('#ff8fb8', '#fff0a0'), ('#8fc8ff', '#ffffff'), ('#ffd84a', '#e8743a')])
    peb = [decal_tex(PA.pebbles(i), f'fo_peb{i}') for i in range(3)]
    avoid = []
    place_decor(S, rnd, greens, 96, X0 + .3, X1 - .3, -2.6, 2.0, avoid, 0.45, (0.8, 1.35), sway=1)
    place_decor(S, rnd, flowers, 54, X0 + .3, X1 - .3, -2.8, 1.9, avoid, 0.8, (0.8, 1.1), sway=1)
    place_decor(S, rnd, peb, 22, X0 + .3, X1 - .3, -2.6, 1.8, avoid, 1.0, (0.9, 1.3), flat=True)
    # ánh nắng xuyên tán
    for i in range(8):
        S.d['anim'].append(dict(type='shaft', x=round(X0 + 3 + i * 4.2 + rnd.uniform(-.8, .8), 2), z=S.z(rnd.uniform(.5, 1.8)), w=round(rnd.uniform(1.4, 2.4), 2), h=7.0, a=round(rnd.uniform(.10, .18), 3), color=[1.0, .95, .7], phase=rnd.random() * 6))
    S.d['particles'] = [dict(kind='pollen', count=70, color=[1, .95, .55], size=.07), dict(kind='leaf', count=18, color=[.55, .85, .35], size=.16)]
    S.d['ambient'] = dict(color=[.78, .92, .86], strength=1.0)
    S.d['grade'] = dict(sat=1.08, contrast=1.06, warm=0.04, vignette=.32, fog=[.52, .74, .72], fogNear=26, fogFar=58)
    S.d['walk'] = dict(x0=X0 + 1.0, x1=X1 - 1.0, z0=S.z(1.6), z1=S.z(-2.4))
    return S

# ------------------------------------------------------------------ SEVERA
def severa():
    S = Scene('severa', 'level3:QTTP', 0.0, 'Thành Severa'); rnd = random.Random(11)
    x0, x1 = -14.0, 11.0
    S.d['bg'] = [0.0, 0.78, 1.0]; S.d['len'] = [x0, x1]
    floor_tex = S.tex(S.by('10_0', 0))
    S.floor(floor_tex, x0 - 1, x1 + 1, 0.9, -4.2, 5.95, 1.7)
    for e in S.entries:
        sp = e['sprite']
        if sp in ('Square', '9_0', '10_0'): continue
        if sp == '6_0': S.src_prop(e, 'back', far=1, sky=1); continue
        if sp in ('13_0', '14_0', '15_0'):  # decal nằm trên sàn
            S.flat(S.tex(e), e['x'] + e['w'] / 2, e['top'] - e['h'] / 2, e['w'], e['h'] * KZ); continue
        S.src_prop(e, sway=1 if sp in ('3_0', '4_0', '5_0') else 0, front=1 if e['order'] >= 1 else 0)
    E = ext_len(x0, x1, 1.0, 1.0); X0, X1 = x0 - E, x1 + E
    extend_src(S, x0, x1, E, left=(-9.9, -6.5), right=(5.9, 11.2), include=lambda p: p['_s'] in ('3_0', '4_0', '5_0', '12_0', '11_0', '16_0', '2_0'))
    # Bố cục theo ảnh gốc QTTP: không thêm đồ trang trí tự chế (đèn, cờ, lều, ghế...). Chỉ giữ cỏ/sỏi rất nhẹ.
    # Trụ teleport (owner chốt 2026-10-14) đặt trên bệ phép thoi xanh ngọc phía dưới bên phải.
    S.d['pillar'] = dict(x=6.35, z=2.75)
    greens = lib_grass('sv', 3, ('#3a7a3a', '#5aa648', '#9ad86a'))
    peb = [decal_tex(PA.pebbles(i), f'sv_peb{i}') for i in range(3)]
    place_decor(S, rnd, peb, 19, X0 + .5, X1 - .5, -3.9, 0.5, [(6.35, -1.2, 2.6)], 1.6, (0.8, 1.3), flat=True)
    place_decor(S, rnd, greens, 22, X0 + .5, X1 - .5, -3.9, 0.5, [(6.35, -1.2, 2.6)], 1.4, (.8, 1.1), sway=1)
    S.d['anim'].append(dict(type='fountain', x=-3.6, z=S.z(0.35), h=1.6))
    S.d['anim'].append(dict(type='shaft', x=-2.0, z=S.z(1.0), w=2.4, h=8.0, a=.10, color=[1, .96, .8], phase=1.0))
    S.d['anim'].append(dict(type='shaft', x=6.0, z=S.z(1.0), w=2.0, h=8.0, a=.08, color=[1, .96, .8], phase=3.0))
    S.d['particles'] = [dict(kind='petal', count=26, color=[1, .78, .86], size=.11), dict(kind='pollen', count=40, color=[1, .96, .75], size=.06)]
    S.d['ambient'] = dict(color=[1.0, .97, .9], strength=1.0)
    S.d['grade'] = dict(sat=1.06, contrast=1.05, warm=0.05, vignette=.28, fog=[.62, .86, 1.0], fogNear=30, fogFar=70)
    S.d['walk'] = dict(x0=X0 + 1.0, x1=X1 - 1.0, z0=S.z(0.2), z1=S.z(-3.4))
    return S

# ------------------------------------------------------------------ RANCH
def ranch():
    S = Scene('ranch', 'level3:NongTrai', 26.0, 'Nông Trại Thì Thầm'); rnd = random.Random(23)
    x0, x1 = -12.4, 9.9
    S.d['bg'] = [0.0, 0.5, 1.0]; S.d['len'] = [x0, x1]
    grass = save_tex(PA.ground_tile(8, 160, 96, ['#5f9a26', '#7ab932', '#93d040', '#b4e45e'], blade_n=70, speck_n=40), 'ranch_ground')
    S.floor(grass, x0 - 1.5, x1 + 1.5, -24.3, -29.3, 4.0, 1.6)
    Ls = lambda y: y - 26.0
    E = {}
    for e in S.entries: E.setdefault(e['sprite'], []).append(e)
    for e in S.entries:
        sp = e['sprite']
        if sp in ('Square', 'area512.pkg_0', 'area55.pkg_0', 'area513.pkg_0', 'area57.pkg_0', 'area516.pkg_0'): continue
        if sp == 'area515.pkg_0': S.src_prop(e, 'back', far=1, sky=1); continue
        if sp == 'area514.pkg_0': S.src_prop(e, 'back', far=0); continue
        if sp in ('area516.pkg_0', 'area510.pkg_0', 'area511.pkg_0', 'area55.pkg_0'):
            S.flat(S.tex(e), e['x'] + e['w'] / 2, e['top'] - e['h'] / 2, e['w'], e['h'] * KZ); continue
        S.src_prop(e, sway=1 if sp in ('area59.pkg_0', 'area57.pkg_0') else 0, front=1 if e['order'] >= 1 else 0)
    E_ = ext_len(x0, x1, 3.0, 0.8); X0, X1 = x0 - E_, x1 + E_
    extend_src(S, x0, x1, E_)
    # cụm vách đá + bụi cây ở mép trái nguyên bản dời ra mép mới (cửa vẫn nằm cạnh vách); phản chiếu một bản sang mép phải
    CL = x0 + 7.6
    cluster = [dict(p) for p in S.d['props'] if p['x'] < CL and not p.get('far')]
    for key in ('props', 'flats'):
        for p in S.d[key]:
            if p['x'] < CL and not p.get('far') and p not in S.d['back']: p['x'] = round(p['x'] - E_, 3)
    fl = forest_lib('ranch_wall'); zfar = S.z(Ls(1.0)) - 0.2; znear = S.z(Ls(-2.6)) + 0.4
    for edge, sg in ((X0, -1), (X1, 1)): tree_wall(S, rnd, edge, sg, zfar, znear, fl)
    # hàng rào bụi sau lưng để nối liền với tường cây
    hedge_t, hw, hh = fl['15_0']; xx = X0 - 3
    while xx < X1 + 3:
        S.d['props'].append(dict(tex=hedge_t, x=round(xx, 3), z=round(zfar - 0.5 - rnd.random() * 0.4, 3), w=round(hw * 0.95, 3), h=round(hh * 0.95, 3), sway=1)); xx += 3.3
    greens = lib_grass('rn', 4, ('#5a8a20', '#86b82c', '#c8e45a'))
    flowers = lib_flowers('rn', [('#ffffff', '#ffd84a'), ('#ffe36a', '#e8743a'), ('#ff9ac0', '#fff0a0')])
    avoid = [(-0.7, Ls(-2.0), 3.2), (-8.0, Ls(0.0), 4.5)]
    place_decor(S, rnd, greens, 70, X0 + 4.5, X1 - 4.5, Ls(-3.0), Ls(1.2), avoid, .5, (.8, 1.4), sway=1)
    place_decor(S, rnd, flowers, 46, X0 + 4.5, X1 - 4.5, Ls(-3.0), Ls(1.2), avoid, .9, (.8, 1.1), sway=1)
    hay = decal_tex(PA.haystack(), 'rn_hay'); fence = decal_tex(PA.fence(), 'rn_fence'); barrel = decal_tex(PA.barrel(), 'rn_barrel'); crate = decal_tex(PA.crate(), 'rn_crate'); sign = decal_tex(PA.sign(), 'rn_sign')
    for (x, y) in ((3.4, -1.2), (4.4, -1.6), (-1.0, -2.0)): S.prop(hay[0], x, Ls(y), hay[1], hay[2], shadow=1)
    for (x, y) in ((2.2, -0.2), (5.8, -0.2), (7.4, -0.2)): S.prop(fence[0], x, Ls(y), fence[1], fence[2], shadow=1)
    S.prop(barrel[0], 1.0, Ls(-0.9), barrel[1], barrel[2], shadow=1); S.prop(crate[0], 1.9, Ls(-0.9), crate[1], crate[2], shadow=1); S.prop(sign[0], -3.4, Ls(-1.3), sign[1], sign[2], shadow=1)
    for i in range(7): S.d['anim'].append(dict(type='shaft', x=round(X0 + 3 + i * 5.2, 2), z=S.z(Ls(1.4)), w=2.4, h=8.0, a=.07, color=[1, .95, .75], phase=i * 1.7))
    S.d['particles'] = [dict(kind='pollen', count=60, color=[1, .96, .6], size=.07), dict(kind='butterfly', count=6, color=[1, .75, .3], size=.14), dict(kind='leaf', count=10, color=[.7, .9, .4], size=.12)]
    S.d['ambient'] = dict(color=[1.0, .98, .88], strength=1.0)
    S.d['grade'] = dict(sat=1.02, contrast=1.04, warm=0.05, vignette=.26, fog=[.7, .86, 1.0], fogNear=30, fogFar=70)
    S.d['walk'] = dict(x0=X0 + 3.0, x1=X1 - 0.8, z0=S.z(Ls(1.0)), z1=S.z(Ls(-2.6)))
    return S

# ------------------------------------------------------------------ BEACH
def beach():
    S = Scene('beach', 'level5:BaiBien', 0.0, 'Bãi Biển Kho Báu'); rnd = random.Random(31)
    x0, x1 = -11.3, 11.1
    S.d['bg'] = [0.27, 0.33, 0.55]; S.d['len'] = [x0, x1]
    sand = save_tex(PA.sand_tile(4, 160, 96), 'beach_sand')
    S.floor(sand, x0 - 1.5, x1 + 1.5, 0.4, -3.0, 4.0, 1.6)
    S.d['water'] = dict(x0=x0 - 14, x1=x1 + 14, z0=S.z(10.0), z1=S.z(0.4), shore=S.z(0.4), deep=[.04, .14, .34], mid=[.12, .42, .62], shallow=[.45, .82, .86], foam=[.96, .99, 1.0])
    for e in S.entries:
        sp = e['sprite']
        if sp in ('Square', '13'): continue
        if sp in ('10', '11', '12', '15'): continue  # sóng 2D thay bằng shader nước
        S.src_prop(e, sway=1 if sp in ('3', '4') else 0, bob=1 if sp in ('7',) else 0, front=1 if e['order'] >= 1 else 0)
    E = ext_len(x0, x1, 1.0, 1.0); X0, X1 = x0 - E, x1 + E
    extend_src(S, x0, x1, E, left=(-6.6, -1.0), right=(4.6, 10.6), include=lambda p: p['_s'] in ('3', '4', '2'))
    shells = [decal_tex(PA.shell(i), f'bc_shell{i}') for i in range(4)]; star = decal_tex(PA.starfish(), 'bc_star'); wood = decal_tex(PA.driftwood(), 'bc_wood'); reed = [decal_tex(PA.reed(i), f'bc_reed{i}') for i in range(2)]
    peb = [decal_tex(PA.pebbles(i), f'bc_peb{i}') for i in range(3)]; rk = [decal_tex(PA.rock(i, base=(138, 132, 126, 255)), f'bc_rock{i}') for i in range(2)]
    place_decor(S, rnd, shells, 35, X0 + .5, X1 - .5, -2.6, -0.2, [], .9, (.8, 1.2), flat=True)
    place_decor(S, rnd, [star], 10, X0 + .5, X1 - .5, -2.4, -0.4, [], 2.0, (.8, 1.1), flat=True)
    place_decor(S, rnd, peb, 19, X0 + .5, X1 - .5, -2.8, 0.1, [], 1.3, (.8, 1.2), flat=True)
    place_decor(S, rnd, reed, 16, X0 + .5, X1 - .5, -2.7, -0.5, [], 1.8, (.8, 1.2), sway=1)
    place_decor(S, rnd, rk, 8, X0 + 1, X1 - 1, -3.0, -2.2, [], 4.0, (.9, 1.3))
    S.prop(wood[0], 7.8 + E * .6, -2.1, wood[1], wood[2], shadow=1); S.prop(wood[0], -8.4, -1.5, wood[1], wood[2], shadow=1)
    S.d['anim'].append(dict(type='shaft', x=-2.0, z=S.z(4.0), w=3.0, h=9.0, a=.08, color=[1, .94, .78], phase=2.0))
    S.d['particles'] = [dict(kind='spray', count=60, color=[.9, .97, 1.0], size=.08), dict(kind='gull', count=3, color=[1, 1, 1], size=.3)]
    S.d['ambient'] = dict(color=[.96, .98, 1.0], strength=1.0)
    S.d['grade'] = dict(sat=1.1, contrast=1.06, warm=0.02, vignette=.3, fog=[.5, .66, .86], fogNear=30, fogFar=70)
    S.d['walk'] = dict(x0=X0 + 1.0, x1=X1 - 1.0, z0=S.z(-0.3), z1=S.z(-2.6))
    return S

# ------------------------------------------------------------------ ARENA
def arena():
    S = Scene('arena', 'level3:DauTruong', -39.0, 'Đấu Trường Hoàng Gia'); rnd = random.Random(41)
    x0, x1 = 24.3, 46.6
    S.d['bg'] = [0.09, 0.06, 0.12]; S.d['len'] = [x0, x1]
    floor_e = S.by('9', 0)
    S.floor(S.tex(floor_e), x0 - 0.5, x1 + 0.5, 40.8, 36.5, 2.8, 2.15)
    for e in S.entries:
        sp = e['sprite']
        if sp == 'Square' or (sp == '9'): continue
        if sp == '2': continue  # thảm nguồn là hai nửa chéo; thay bằng thảm đỏ viền vàng dựng riêng bên dưới
        S.src_prop(e, front=1 if e['order'] >= 1 else 0)
    E = ext_len(x0, x1, 3.2, 3.2); X0, X1 = x0 - E, x1 + E
    extend_src(S, x0, x1, E, left=(29.0, 34.0), right=(37.0, 42.0), include=lambda p: p['_s'] in ('8', '4', '7', '10'), outward=lambda p: p['_s'] in ('5', '6'))
    carpet = decal_tex(PA.carpet(72, 36), 'ar_carpet')
    S.flat(carpet[0], 35.45, 39.0, 8.6, 4.6)
    # đuốc + ánh lửa
    ft = save_tex(PA.torch_frames(), 'ar_torch'); gl = glow_tex((255, 160, 70), 'fire')
    for x, y in ((27.6 - E * .55, 40.0), (27.6, 40.0), (43.4, 40.0), (43.4 + E * .55, 40.0), (31.2 - E * .8, 36.9), (31.2, 36.9), (39.9, 36.9), (39.9 + E * .8, 36.9)):
        S.d['props'].append(dict(tex=ft, x=x, z=S.z(y), w=0.5, h=1.2, frames=4, fps=9, shadow=1))
        S.d['props'].append(dict(tex=gl, x=x, z=S.z(y) + .03, y=1.15, w=3.4, h=3.4, additive=1, flicker=.25, billboard=1))
        S.light(x, y, 1.1, [1, .62, .26], 5.0, 1.0, .22)
    S.d['anim'].append(dict(type='shaft', x=35.4, z=S.z(40.5), w=3.0, h=8.0, a=.12, color=[1, .85, .5], phase=0.4))
    banner = decal_tex(PA.banner(col='#7a1f6a'), 'ar_banner')
    for x in (26.0 - E * .55, 26.0, 45.0, 45.0 + E * .55): S.prop(banner[0], x, 40.6, banner[1] * 1.2, banner[2] * 1.2, sway=1, shadow=1)
    S.d['particles'] = [dict(kind='dust', count=70, color=[1, .9, .65], size=.05), dict(kind='ember', count=26, color=[1, .6, .25], size=.06)]
    S.d['ambient'] = dict(color=[.92, .86, .9], strength=1.0)
    S.d['grade'] = dict(sat=1.08, contrast=1.08, warm=0.08, vignette=.42, fog=[.2, .12, .2], fogNear=24, fogFar=52)
    S.d['walk'] = dict(x0=X0 + 3.2, x1=X1 - 3.2, z0=S.z(40.0), z1=S.z(37.0))
    return S

BUILDERS = dict(severa=severa, forest=forest, beach=beach, ranch=ranch, arena=arena)
if __name__ == '__main__':
    stats = {}
    for sid, fn in BUILDERS.items():
        S = fn(); d = S.d
        # Vật thể lớn ở mép trái/phải không được che người chơi đứng ở biên (x=0 / x=39): đẩy ra sau làn đi.
        w = d['walk']; mid = (w['z0'] + w['z1']) / 2; moved = 0
        if sid != 'ranch': d_props = []
        else: d_props = d['props']
        for pr in d_props:
            if pr.get('h', 0) >= 2.5 and pr['z'] > mid - 0.4 and (pr['x'] < w['x0'] + 2.5 or pr['x'] > w['x1'] - 2.5) and not pr.get('far'):
                pr['z'] = round(w['z0'] + 0.3, 3); moved += 1
        if moved: print(sid, 'đẩy lùi', moved, 'vật thể che mép')
        strip_tags(d)
        json.dump(d, open(os.path.join(args.out, sid + '.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
        stats[sid] = dict(floors=len(d['floor']), props=len(d['props']), flats=len(d['flats']), back=len(d['back']), lights=len(d['lights']))
    print(stats, len(_saved), 'textures')
