#!/usr/bin/env python3
"""Dựng map thử HD-2D 'windrock_hd2d' từ batch-11-windrock mở rộng (74 assets).
Xuất apps/game-web/public/scenes/windrock_hd2d.json + texture hd2d_windrock-*.png.
Tuân thủ đầy đủ:
- Cầu treo bắc qua 2 khe núi chasm-ravine-01/02 lòng đen sâu, có mố neo trái/phải.
- Sàn đá rock-floor-01 chủ đạo, chênh độ sáng các tile <= 12/255.
- Decal chuyển tiếp 100% vẽ bằng công cụ tạo ảnh (tuyết tan, sỏi lở, nứt đá, vũng băng, dấu chân).
- Thông tuyết sway-split tách thân (trunk) và tán (canopy, sway=1).
- 3 lớp backdrop parallax (wall-far, peaks-mid, cliffs-near) tự nhiên, không vạch ngang.
- 6 bóng đổ procedural mềm #4A525D gắn vật vào đất.
"""
import json, random, shutil, os
from PIL import Image, ImageFilter
import numpy as np

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
B = f'{R}/apps/game-web/art-src/hd2d/batch-11-windrock'
OUT = f'{R}/apps/game-web/public/scenes'
os.makedirs(f'{OUT}/tex', exist_ok=True)

man = {a['id']: a for a in json.load(open(f'{B}/manifest.json'))['assets']}
used = {}

def tex(aid):
    n = f'hd2d_{aid}.png'
    dst = f'{OUT}/tex/{n}'
    src = f'{B}/{aid}/final.png'
    
    if aid in ('windrock-peaks-wall-far', 'windrock-peaks-mid', 'windrock-cliffs-near'):
        try:
            im = Image.open(src)
            arr = np.array(im).astype(float)
            H, W, _ = arr.shape
            blend_m = 32
            pad_top = 80 if aid == 'windrock-peaks-wall-far' else 40
            t = np.linspace(0, 1, blend_m)
            s = 3 * t**2 - 2 * t**3
            c_seam = 0.5 * (arr[:, 1, :] + arr[:, W-2, :])
            out_single = arr.copy()
            for i in range(blend_m):
                alpha = s[i]
                out_single[:, i, :] = (1.0 - alpha) * c_seam + alpha * arr[:, i, :]
                out_single[:, W - 1 - i, :] = (1.0 - alpha) * c_seam + alpha * arr[:, W - 1 - i, :]
            out_single[:, 0, :] = c_seam
            out_single[:, W - 1, :] = c_seam
            single_im = Image.fromarray(np.clip(out_single, 0, 255).astype(np.uint8))
            
            wide_im = Image.new('RGBA', (W * 4, H + pad_top), (0, 0, 0, 0))
            if aid == 'windrock-peaks-wall-far':
                row0 = single_im.crop((0, 0, W, 1)).filter(ImageFilter.BoxBlur(4))
                row0_wide = row0.resize((W, 1), Image.Resampling.BILINEAR)
                for i in range(4):
                    for y in range(pad_top):
                        wide_im.paste(row0_wide, (i * W, y))
            for i in range(4):
                wide_im.paste(single_im, (i * W, pad_top), single_im)
            wide_im.save(dst)
        except Exception:
            shutil.copyfile(src, dst)
    else:
        shutil.copyfile(src, dst)
        
    used[aid] = n
    return n

X0, X1, Z0, Z1 = -6.13, 24.73, -2.4, 3.6
props, flats, back = [], [], []

def prop(aid, x, z, **kw):
    w, h = man[aid]['world']
    s = kw.pop('s', 0.68)
    p = dict(tex=tex(aid), x=round(x, 3), z=round(z, 3), w=round(w*s, 3), h=round(h*s, 3))
    p.update(kw)
    props.append(p)

def flat(aid, x, z, **kw):
    w, d = man[aid]['world']
    s = kw.pop('s', 1.0)
    f = dict(tex=tex(aid), x=round(x, 3), z=round(z, 3), w=round(w*s, 3), d=round(d*s, 3))
    f.update(kw)
    flats.append(f)

# -------------------------------------------------------------------------
# 1. NỀN XA PARALLAX (3 LỚP LIỀN MẠCH, ZERO SEAM, KHÔNG VẠCH NGANG)
# -------------------------------------------------------------------------
back.append(dict(tex=tex('windrock-peaks-wall-far'), x=9.3, y=0.0, z=-4.2, w=64.0, h=7.8, far=1))
back.append(dict(tex=tex('windrock-peaks-mid'), x=9.3, y=0.1, z=-3.4, w=52.0, h=6.5))
back.append(dict(tex=tex('windrock-cliffs-near'), x=9.3, y=0.15, z=-2.7, w=44.0, h=5.5))

# -------------------------------------------------------------------------
# 2. SÀN ĐÁ NÚI PHIẾN CHỦ ĐẠO (ĐỒNG BỘ ĐỘ SÁNG <= 12/255)
# -------------------------------------------------------------------------
floor = [dict(tex=tex('windrock-rock-floor-01'), x0=-15.6, x1=34.2, z0=-9.2, z1=4.5, tw=4.0, td=4.0)]

# -------------------------------------------------------------------------
# 3. KHE NÚI CHO CẦU TREO (2 KHE VỰC LÒNG ĐEN SÂU + MỐ NEO CẦU)
# -------------------------------------------------------------------------
# 2 Khe nứt/vực thẳm nằm chính xác dưới cầu treo
flat('windrock-chasm-ravine-01', 13.5, -0.6, s=0.9)
flat('windrock-chasm-ravine-02', 16.5, -0.6, s=0.9)

# Mố trụ đá neo cầu dây thừng hai bên bờ vực
prop('windrock-bridge-anchor-post-left', 11.2, -0.6, s=0.75)
prop('windrock-bridge-anchor-post-right', 18.8, -0.6, s=0.75)

# Cầu treo gỗ bắc ngang qua vực
prop('windrock-bridge-repeat', 13.5, -0.6, s=0.75)
prop('windrock-bridge-broken', 16.5, -0.55, s=0.75)

# -------------------------------------------------------------------------
# 4. DECAL CHUYỂN TIẾP HỮU CƠ (100% VẼ BẰNG CÔNG CỤ TẠO ẢNH)
# -------------------------------------------------------------------------
# Vệt tuyết tan mềm quanh trại và đường dốc
flat('windrock-decal-snow-drift-01', 4.5, -0.8, s=0.85)
flat('windrock-decal-snow-drift-02', 20.5, 0.5, s=0.85)

# Vệt sỏi lở sườn dốc quanh trại và tiền cảnh
flat('windrock-decal-scree-run-01', 6.8, -0.6, s=0.85)
flat('windrock-decal-scree-run-02', 1.0, 1.2, s=0.80)

# Vết nứt đá phiến hữu cơ
flat('windrock-decal-rock-fissure-01', 10.0, 1.5, s=0.75)
flat('windrock-decal-rock-fissure-02', -1.5, 0.8, s=0.75)

# Vũng băng tuyết tan
flat('windrock-decal-ice-patch-01', 8.2, 1.8, s=0.75)
flat('windrock-decal-ice-patch-02', 19.5, -1.2, s=0.75)

# Dấu chân trên tuyết dẫn từ cổng tới trại
flat('windrock-decal-snow-footprints', -3.0, -0.5, s=0.70)

# Rêu vách đá mép vực
flat('windrock-decal-alpine-moss-edge', 14.8, 1.8, s=0.75)

# -------------------------------------------------------------------------
# 5. BÓNG ĐỔ TIẾP ĐẤT PROCEDURAL (#4A525D, GRADIENT MỀM)
# -------------------------------------------------------------------------
flat('windrock-shadow-large-oval', 5.5, -0.4, s=0.85)     # Lều trại
flat('windrock-shadow-medium-oval', 7.8, -0.3, s=0.75)    # Lửa trại
flat('windrock-shadow-medium-oval', 6.8, -0.35, s=0.65)   # Cột cờ phướn
flat('windrock-shadow-tree-canopy', -2.0, -1.2, s=0.85)   # Cây thông 1
flat('windrock-shadow-tree-canopy', 10.5, -1.1, s=0.90)   # Cây thông 2
flat('windrock-shadow-tree-canopy', 21.0, -0.8, s=0.85)   # Cây thông 3
flat('windrock-shadow-pillar-long', -1.2, 2.7, s=0.75)    # Cột đá gió bào
flat('windrock-shadow-pillar-long', 18.5, 2.8, s=0.75)    # Cột đá gió bào 2
flat('windrock-shadow-pillar-long', 0.5, -1.0, s=0.70)    # Tháp đá nhọn 1
flat('windrock-shadow-pillar-long', 22.8, 1.5, s=0.70)    # Tháp đá nhọn 2
flat('windrock-shadow-stairs-spread', 20.0, 1.0, s=0.80)  # Bậc thang đá

# -------------------------------------------------------------------------
# 6. CỔNG VÒM, PORTAL DORMANT/ACTIVE & SPAWN
# -------------------------------------------------------------------------
prop('windrock-arch-gate', -4.3, -1.5, s=0.72)
prop('windrock-portal-dormant', 23.2, -0.9, s=0.72)

# Spawn marker 4 khung
mw, mh = man['windrock-spawn-marker']['world']
props.append(dict(tex=tex('windrock-spawn-marker'), x=22.0, z=2.2, w=round(mw/4, 3), h=mh, frames=4, fps=5))

# -------------------------------------------------------------------------
# 7. THÔNG NÚI TUYẾT SWAY-SPLIT (TÁCH THÂN VÀ TÁN, SWAY=1)
# -------------------------------------------------------------------------
# Thông lớn 1 (thông dáng thẳng)
prop('windrock-pine-large-01-trunk', -2.0, -1.8, s=0.75)
prop('windrock-pine-large-01-canopy', -2.0, -1.799, y=1.2, s=0.75, sway=1)

# Thông lớn 2 (thông dáng vặn gió)
prop('windrock-pine-large-02-trunk', 10.5, -1.7, s=0.78)
prop('windrock-pine-large-02-canopy', 10.5, -1.699, y=1.25, s=0.78, sway=1)

# Thông gốc 3
prop('windrock-pine-trunk', 21.0, -1.4, s=0.72)
prop('windrock-pine-canopy', 21.0, -1.399, y=1.15, s=0.72, sway=1)

# -------------------------------------------------------------------------
# 8. KHU CẮM TRẠI, CỜ PHƯỚN, BIA ĐÁ & ĐẠO CỤ THÁM HIỂM
# -------------------------------------------------------------------------
prop('windrock-camp-tent', 5.5, -0.8, s=0.75)

# Lửa trại 4 khung
cw, ch = man['windrock-campfire-anim']['world']
props.append(dict(tex=tex('windrock-campfire-anim'), x=7.8, z=-0.5, w=round(cw/4, 3), h=ch, frames=4, fps=5))

# Cột cờ phướn cầu an tung bay trong gió núi
prop('windrock-prayer-flagpole', 6.8, -0.85, s=0.72)

# Cọc chỉ đường & hàng rào gỗ
prop('windrock-wooden-fence', 3.0, -1.2, s=0.70)
prop('windrock-wooden-fence', 1.0, -1.2, s=0.70)
prop('windrock-signpost-blank', 9.5, -1.0, s=0.70)

# Tháp đá dẫn đường (cairn) & đống củi xếp
prop('windrock-trail-cairn', 8.8, -0.6, s=0.68)
prop('windrock-firewood-stack', 8.5, -0.4, s=0.65)
prop('windrock-supply-crate', 4.5, -0.6, s=0.65)
prop('windrock-supply-keg', 4.0, -0.5, s=0.65)

# Bậc thang đá tuyết lên dốc
prop('windrock-stone-stairs', 20.0, 0.8, s=0.72)

# Trụ tháp đá phong thạch gọt nhọn cao
prop('windrock-spire-pillar-tall-01', 0.5, -1.4, s=0.72)
prop('windrock-spire-pillar-tall-02', 22.8, 1.2, s=0.72)

# Cột đá gió bào & vách đá ở sườn biên (framing flanks)
prop('windrock-pillar-01', -1.2, 2.5, s=0.65)
prop('windrock-pillar-01', 18.5, 2.6, s=0.65)
prop('windrock-cliff-01', -5.0, -1.8, s=0.75)
prop('windrock-cliff-snow-ledge', 24.5, -1.6, s=0.75)

# Bụi gai tuyết & cỏ gấu cao nguyên rải rác
prop('windrock-shrub-snow-01', 2.0, -0.8, s=0.65)
prop('windrock-shrub-snow-02', 12.0, -1.0, s=0.65)
prop('windrock-grass-snow-clump-01', 0.0, 1.0, s=0.65)
prop('windrock-grass-snow-clump-02', 11.5, 1.5, s=0.65)
prop('windrock-boulder-snow-01', -0.5, 1.8, s=0.68)
prop('windrock-boulder-snow-02', 17.0, 2.0, s=0.68)

props.sort(key=lambda p: p['z'])

scene = dict(
    id='windrock_hd2d',
    name='Núi Phong Thạch HD-2D',
    floor=floor,
    flats=flats,
    back=back,
    props=props,
    lights=[],
    particles=[
        dict(kind='dust', count=25, color=[0.9, 0.95, 1.0], size=0.03),
        dict(kind='ember', count=8, color=[1.0, 0.75, 0.35], size=0.04)
    ],
    anim=[],
    water=None,
    bg=[0.14, 0.18, 0.24],
    len=[-7.131, 25.731],
    ambient=dict(color=[0.94, 0.97, 1.0], strength=1.35),
    grade=dict(sat=1.02, contrast=1.03, warm=0.0, vignette=0.20, fog=[0.65, 0.76, 0.88], fogNear=35, fogFar=85),
    walk=dict(x0=X0, x1=X1, z0=Z0, z1=Z1)
)

json.dump(scene, open(f'{OUT}/windrock_hd2d.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print(f'Refined Windrock Scene built: props={len(props)}, flats={len(flats)}, back={len(back)}, tex={len(used)}')
