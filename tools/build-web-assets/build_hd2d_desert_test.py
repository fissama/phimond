#!/usr/bin/env python3
"""Dựng map thử HD-2D 'desert_hd2d' từ batch-11-desert (85 assets).
Xuất apps/game-web/public/scenes/desert_hd2d.json + texture hd2d_*.png.
Bố cục tự nhiên có chiều sâu không gian, loại bỏ hoàn toàn hàng ngang triển lãm,
khắc phục triệt để vạch dọc backdrop và tích hợp đầy đủ decal chuyển tiếp hữu cơ.
"""
import json, random, shutil, os

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
B = f'{R}/apps/game-web/art-src/hd2d/batch-11-desert'
OUT = f'{R}/apps/game-web/public/scenes'

man_data = json.load(open(f'{B}/manifest.json'))
man = {a['id']: a for a in (man_data['assets'] if isinstance(man_data, dict) else man_data)}
used = {}

def tex(aid):
    name = f'hd2d_{aid}.png'
    dst = f'{OUT}/tex/{name}'
    shutil.copyfile(f'{B}/{aid}/final.png', dst)
    used[aid] = name
    return name

def wh(aid):
    return man[aid]['world']

rnd = random.Random(20261017)
X0, X1, Z0, Z1 = -6.13, 24.73, -2.4, 3.6
props, flats, back = [], [], []

def prop(aid, x, z, **kw):
    w, h = wh(aid)
    s = kw.pop('s', 1.0)
    p = dict(tex=tex(aid), x=round(x, 3), z=round(z, 3), w=round(w*s, 3), h=round(h*s, 3))
    p.update(kw)
    props.append(p)

def palm(x, z, s=1.0):
    prop('desert-palm-trunk', x, z, s=s)
    tw, th = wh('desert-palm-trunk')
    prop('desert-palm-canopy', x, z + 0.001, y=round(th * s * 0.85, 3), s=s, sway=1)

# ==============================================================================
# 1. NỀN XA ĐA TẦNG (GROUP H) — BƯỚC ĐẶT CHÍNH XÁC, TRIỆT TIÊU VẠCH DỌC
# ==============================================================================
# Đặt far=0 tại z=-3.8 với bước nhảy đúng bằng w_far=16.0 (không co giãn z-warp, không chồng lấn)
# Seam_x_max=0.0 khớp tuyệt đối từng pixel channel tại điểm nối
# y=-0.45 để chân backdrop chìm tự nhiên dưới mặt phẳng sàn cát y=0
w_far = 16.0
for k in range(-1, 3):
    back.append(dict(tex=tex('desert-dunes-wall-far'), x=round(6.0 + k * w_far, 3), y=-0.45, z=-3.8, w=w_far, h=4.3))

# Lớp cồn cát trung cảnh (dunes-mid 1024x384, w=8.0, h=3.0)
w_mid = 8.0
for k in range(-2, 5):
    back.append(dict(tex=tex('desert-dunes-mid'), x=round(4.0 + k * w_mid, 3), y=-0.25, z=-3.4, w=w_mid, h=3.0))

# Lớp phế tích sa thạch gần (ruins-near 1024x384, w=8.0, h=3.0)
w_near = 8.0
for k in range(-2, 5):
    back.append(dict(tex=tex('desert-ruins-near'), x=round(6.0 + k * w_near, 3), y=-0.10, z=-3.0, w=w_near, h=3.0))

# ==============================================================================
# 2. SÀN TIÊU CHUẨN DUY NHẤT (GROUP A) — CÁT VÀNG SÓNG LƯỢN ĐỒNG NHẤT
# ==============================================================================
# Duy nhất 1 tile chủ đạo desert-sand-floor-01 phủ toàn bộ map, triệt tiêu mọi cạnh khối chữ nhật
floor = [
    dict(tex=tex('desert-sand-floor-01'), x0=-15.6, x1=34.2, z0=-9.2, z1=4.5, tw=4.0, td=4.0)
]

# ==============================================================================
# 3. DECAL CHUYỂN TIẾP HỮU CƠ (GROUP B) — VỆT DITHER LOANG TỰ NHIÊN
# ==============================================================================
# Rải các mảng vách đá sa thạch phong hóa tự nhiên rải rác quanh khu di tích
flats.append(dict(tex=tex('desert-edge-sand-sandstone-corner-01'), x=-2.4, z=-2.1, w=1.5, d=1.5))
flats.append(dict(tex=tex('desert-edge-sand-sandstone-corner-02'), x=8.4, z=-1.8, w=1.5, d=1.5))
flats.append(dict(tex=tex('desert-edge-sand-sandstone-n'), x=2.8, z=-2.2, w=2.0, d=1.2))
flats.append(dict(tex=tex('desert-edge-sand-sandstone-s'), x=10.5, z=-1.6, w=2.0, d=1.2))
flats.append(dict(tex=tex('desert-edge-sand-sandstone-w'), x=-2.2, z=-1.0, w=1.0, d=2.2))
flats.append(dict(tex=tex('desert-edge-sand-sandstone-e'), x=8.2, z=-1.0, w=1.0, d=2.2))
flats.append(dict(tex=tex('desert-edge-sand-cracked-patch-01'), x=11.0, z=1.2, w=1.2, d=1.6))
flats.append(dict(tex=tex('desert-edge-sand-cracked-patch-02'), x=17.5, z=1.5, w=1.2, d=1.4))

# ==============================================================================
# 4. DECAL BỀ MẶT & KHE NỨT ĐỊA HÌNH (GROUP C & G)
# ==============================================================================
# Vực sâu khe nứt khổng lồ cắt xéo mặt đất tiền cảnh
flats.append(dict(tex=tex('desert-chasm-ravine-01'), x=13.2, z=2.4, w=4.8, d=2.9))

# Gạch sụt lún sa mạc
flats.append(dict(tex=tex('desert-decal-sunken-bricks'), x=1.5, z=-1.2, w=1.5, d=1.3))

# Vệt cát bay uốn lượn theo chiều gió
flats.append(dict(tex=tex('desert-decal-wind-sand-01'), x=2.8, z=0.8, w=1.4, d=2.6))
flats.append(dict(tex=tex('desert-decal-wind-sand-02'), x=16.0, z=0.9, w=1.4, d=2.6))
flats.append(dict(tex=tex('desert-decal-wind-sand-01'), x=-2.2, z=2.4, w=1.3, d=2.4))
flats.append(dict(tex=tex('desert-decal-wind-sand-02'), x=6.8, z=2.1, w=1.6, d=2.8))
flats.append(dict(tex=tex('desert-decal-wind-sand-01'), x=21.2, z=2.2, w=1.5, d=2.5))

# Dấu chân lữ hành băng qua sa mạc về hướng lều trại và giếng nước
flats.append(dict(tex=tex('desert-decal-footprints'), x=4.0, z=0.6, w=2.4, d=1.0))
flats.append(dict(tex=tex('desert-decal-footprints'), x=8.2, z=0.1, w=2.4, d=1.0))
flats.append(dict(tex=tex('desert-decal-footprints'), x=0.5, z=1.6, w=2.2, d=0.9))
flats.append(dict(tex=tex('desert-decal-footprints'), x=11.5, z=1.8, w=2.5, d=1.0))

# Xương rải rác, mảnh gốm vỡ và sỏi vụn quanh khu di tích & rải rác tiền cảnh
flats.append(dict(tex=tex('desert-decal-bones-scatter'), x=14.8, z=-0.2, w=1.2, d=1.1))
flats.append(dict(tex=tex('desert-decal-pottery-shards'), x=-1.2, z=-1.0, w=1.0, d=0.9))
flats.append(dict(tex=tex('desert-decal-sandstone-rubble'), x=10.0, z=-1.4, w=1.3, d=1.1))
flats.append(dict(tex=tex('desert-decal-pebbles-desert'), x=1.0, z=1.8, w=1.3, d=0.9))
flats.append(dict(tex=tex('desert-decal-pebbles-desert'), x=5.5, z=2.7, w=1.4, d=1.0))
flats.append(dict(tex=tex('desert-decal-pebbles-desert'), x=17.2, z=2.0, w=1.3, d=0.9))
flats.append(dict(tex=tex('desert-decal-pebbles-desert'), x=-3.8, z=1.2, w=1.2, d=0.8))

# Vòng ma thuật cổ mờ khắc trên đá dưới cổng dịch chuyển
flats.append(dict(tex=tex('desert-decal-ancient-rune-faded'), x=23.2, z=-0.9, w=2.5, d=2.5))

# ==============================================================================
# 5. CẤU TRÚC BẢN ĐỒ & CÔNG TRÌNH LỚN (GROUP F & G)
# ==============================================================================
# Cổng đá vòm lối vào phía tây
prop('desert-arch-gate', -4.5, -1.6, s=0.72)

# Cổng dịch chuyển lối ra phía đông
prop('desert-portal-dormant', 23.2, -0.9, s=0.70)

# Cụm lều du mục: lều lớn trung tâm + lều phụ
prop('desert-nomad-tent-large', 5.5, -0.9, s=0.72)
prop('desert-nomad-tent', 3.2, -0.7, s=0.68)
prop('desert-nomad-stake-banner', 1.8, -0.5, s=0.72)

# Giếng cổ sa mạc bên cạnh trại
prop('desert-dry-well', 1.6, -0.8, s=0.70)

# Khu phế tích sa thạch phía tây: tường vòm kết hợp bậc thang đá 3/4
prop('desert-ruins-wall-arch', -1.2, -1.8, s=0.72)
prop('desert-stone-stairs', 0.6, -1.4, s=0.70)

# Xương quái khổng lồ vùi trong cát
prop('desert-monster-bones', 15.2, -0.4, s=0.76)

# Tượng nhân sư sa mạc cổ trấn giữ (đế cát dither tan dần, không còn khung chữ nhật)
prop('desert-sphinx-ruin', 19.8, -1.3, s=0.74)

# Tảng đá sa thạch trung (boulder-03 mới) đặt tự nhiên bên gò cát
prop('desert-boulder-03', 14.2, 1.2, s=0.70)

# Cồn cát uốn lượn có vân sóng cát và chân dither mềm mại
prop('desert-sand-mound', -2.5, 2.3, s=0.82)
prop('desert-sand-dune-medium', 18.2, 2.5, s=0.82)

# Cây chà là sa mạc vươn cao
palm(-3.0, -1.8, s=0.78)
palm(8.5, -1.5, s=0.82)

# ==============================================================================
# 6. PROP VỪA (GROUP E)
# ==============================================================================
prop('desert-ruins-pillar', -1.8, -1.5, s=0.66)
prop('desert-ruins-pillar', 10.2, -1.6, s=0.66)
prop('desert-ruins-pillar-fallen', 0.2, -1.4, s=0.70)
prop('desert-ancient-stele', 17.8, -1.1, s=0.64)
prop('desert-boulder-02', -3.2, 2.5, s=0.66)

# Xương rồng các loại phân bổ tự nhiên theo độ sâu
prop('desert-cactus-tall', -4.0, -0.8, s=0.70)
prop('desert-cactus-tall', 13.0, -1.0, s=0.72)
prop('desert-cactus-dead', 7.5, 1.2, s=0.68)
prop('desert-cactus-dead', 18.5, 0.4, s=0.68)
for cx in [-2.5, 1.2, 8.0, 11.8, 16.2, 21.8]:
    prop('desert-cactus-01', cx + rnd.uniform(-0.2, 0.2), rnd.uniform(-2.1, -1.4), s=rnd.uniform(0.55, 0.68))
for cx in [-1.0, 4.8, 10.8, 19.5]:
    prop('desert-cactus-02', cx, rnd.uniform(2.6, 3.3), s=rnd.uniform(0.52, 0.64))

# ==============================================================================
# 7. PROP NHỎ RẢI NỀN (GROUP D)
# ==============================================================================
# Đồ đạc sinh hoạt quanh trại du mục
prop('desert-camp-wood-crate', 5.0, -0.4, s=0.66)
prop('desert-camp-canvas-pack', 5.4, -0.3, s=0.66)
prop('desert-camp-canvas-sack', 2.8, -0.4, s=0.66)
prop('desert-camp-charcoal-stove', 4.5, -0.45, s=0.68)
prop('desert-pottery-urn-broken', -0.8, -0.9, s=0.68)

# Xương nhỏ rải rác gần bộ xương lớn
prop('desert-small-skull', 14.0, -0.1, s=0.66)
prop('desert-small-ribs', 16.2, -0.2, s=0.66)

# Cỏ lăn sa mạc tumbleweed
prop('desert-tumbleweed-01', 6.5, 1.0, s=0.66)
prop('desert-tumbleweed-02', 16.5, 0.8, s=0.66)
prop('desert-tumbleweed-01', -0.5, 0.6, s=0.62)

for aid in ['desert-small-rock-01', 'desert-small-rock-02', 'desert-small-rock-03']:
    for _ in range(4):
        prop(aid, rnd.uniform(X0, X1), rnd.uniform(-1.6, 2.9), s=rnd.uniform(0.55, 0.70))

for aid in ['desert-small-cactus-01', 'desert-small-cactus-02', 'desert-small-cactus-03']:
    for _ in range(3):
        prop(aid, rnd.uniform(X0, X1), rnd.uniform(-1.9, 2.7), s=rnd.uniform(0.55, 0.70))

# ==============================================================================
# 8. HOẠT HỌA / FX 4 KHUNG (GROUP I)
# ==============================================================================
# Spawn marker (lề an toàn >= 16px mỗi bên)
mw, mh = wh('desert-spawn-marker')
props.append(dict(tex=tex('desert-spawn-marker'), x=22.0, z=2.2, w=round(mw*0.7/4, 3), h=round(mh*0.7, 3), frames=4, fps=5))

# Đèn bão / ngọn lửa trại trước lều
lw, lh = wh('desert-torch-lantern-anim')
props.append(dict(tex=tex('desert-torch-lantern-anim'), x=4.5, z=-0.2, w=round(lw*0.65/4, 3), h=round(lh*0.65, 3), frames=4, fps=6))

# Lốc bụi sa mạc (dust devil) xoay ở xa
dw, dh = wh('desert-dust-devil-anim')
props.append(dict(tex=tex('desert-dust-devil-anim'), x=10.5, z=-2.3, w=round(dw*0.8/4, 3), h=round(dh*0.8, 3), frames=4, fps=6, additive=True))

# Vòng ma thuật phát quang gần cổng
rw, rh = wh('desert-magic-rune-anim')
props.append(dict(tex=tex('desert-magic-rune-anim'), x=23.2, z=-0.75, w=round(rw*0.65/4, 3), h=round(rh*0.65, 3), frames=4, fps=4, additive=True))

# ==============================================================================
# 9. TỔNG HỢP VÀ XUẤT SCENE JSON
# ==============================================================================
props.sort(key=lambda p: p['z'])

scene = dict(
    id='desert_hd2d',
    name='Hoang Mạc HD-2D',
    floor=floor,
    flats=flats,
    back=back,
    props=props,
    lights=[],
    particles=[
        dict(kind='dust', count=45, color=[1.0, 0.88, 0.6], size=0.05),
        dict(kind='ember', count=10, color=[1.0, 0.65, 0.25], size=0.06),
    ],
    anim=[],
    water=None,
    bg=[0.24, 0.16, 0.08],
    len=[-7.131, 25.731],
    ambient=dict(color=[1.0, 0.96, 0.90], strength=1.2),
    grade=dict(sat=1.05, contrast=1.04, warm=0.03, vignette=0.25, fog=[0.78, 0.70, 0.55], fogNear=30, fogFar=75),
    walk=dict(x0=X0, x1=X1, z0=Z0, z1=Z1)
)

json.dump(scene, open(f'{OUT}/desert_hd2d.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print(f'Done desert_hd2d! Props: {len(props)}, Flats: {len(flats)}, Back: {len(back)}, Textures: {len(used)}')
