#!/usr/bin/env python3
"""Cổng chất lượng asset/map HD-2D. Chạy từ tools/check.sh. Thoát 1 nếu còn lỗi.
Phạm vi: các kit batch-11-* (kit cũ có tồn đọng đã biết, dùng --all để quét hết).
Gemini phải sửa tới 0 lỗi TRƯỚC khi báo nghiệm thu; Claude vẫn duyệt thêm bằng mắt.
"""
import sys, os, glob, json, subprocess, tempfile, itertools, collections
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART = f'{ROOT}/apps/game-web/art-src/hd2d'
LAYOUTS = f'{ROOT}/.ai/design/map-layouts'
BRIEFS = f'{ROOT}/.ai/design/map-briefs'
VALID = f'{ROOT}/tools/build-web-assets/validate_hd2d_map_layout.py'
errs, warns = [], []
# Miễn trừ do Claude/owner duyệt bằng mắt: tools/hd2d_audit/gate_waivers.json  {"<batch>/<asset-id>": {"<mã>": "lý do"}}, mã = audit|bbox-edge|tile|...
WAIVERS = {}
_wp = f'{ROOT}/tools/hd2d_audit/gate_waivers.json'
if os.path.exists(_wp): WAIVERS = json.load(open(_wp))
def waived(key, code): return code in WAIVERS.get(key, {})
def E(m): errs.append(m)
def W(m): warns.append(m)

all_kits = '--all' in sys.argv
kit_dirs = sorted(d for d in glob.glob(f'{ART}/batch-*/') if all_kits or os.path.basename(d.rstrip('/')).startswith('batch-11-'))
kits = [os.path.basename(d.rstrip('/')) for d in kit_dirs]

# 1. audit manifest (kích thước, margin, màu, mật độ, seam, alpha, thiếu file)
with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as t: tmp = t.name
subprocess.run([sys.executable, f'{ROOT}/tools/hd2d_audit/audit.py', ART, tmp], stdout=subprocess.DEVNULL, check=True)
rows = [r for r in json.load(open(tmp)) if r['batch'] in kits]
for r in rows:
    for i in r['issues']:
        # bóng thủ tục và dải horizon được phép alpha mềm
        if i.startswith('SEMI_ALPHA') and any(k in r['id'] for k in ('shadow', 'gradient', 'horizon')): continue
        if waived(f"{r['batch']}/{r['id']}", 'audit'): continue
        E(f"[audit] {r['batch']}/{r['id']}: {i}")

# 2. bbox-edge: vật bị cắt thẳng mép ngoài (cột mép ngoài của bbox alpha đặc >60% chiều cao vật)
NOCUT = ('floor', 'backdrop', 'backdrop_far', 'backdrop_mid', 'fx')
for d in kit_dirs:
    b = os.path.basename(d.rstrip('/'))
    man = {}
    for mf in ('manifest.json', 'aux-manifest.json'):
        if os.path.exists(d + mf):
            j = json.load(open(d + mf)); man.update({x['id']: x for x in (j['assets'] if isinstance(j, dict) else j)})
    for p in sorted(glob.glob(d + '*/final.png')):
        n = os.path.basename(os.path.dirname(p)); m = man.get(n, {})
        if m.get('category') in NOCUT or m.get('tileable') in ('xy', 'x') or any(k in n for k in ('gradient', 'horizon', 'anim')): continue
        if waived(f'{b}/{n}', 'bbox-edge'): continue
        a = np.array(Image.open(p).convert('RGBA'))[..., 3] > 127
        if a.sum() < 200: continue
        ys, xs = np.where(a); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max(); h = y1 - y0 + 1
        l = a[y0:y1+1, x0].sum() / h; r = a[y0:y1+1, x1].sum() / h
        if l > .6 or r > .6: E(f"[bbox-edge] {b}/{n}: mép trái {l:.2f} phải {r:.2f} (nghi bị cắt thẳng; vật tự nhiên thẳng cạnh thì xin miễn trừ để Claude duyệt)")


# 2b. tỉ lệ vật thật (size_check.py): túi/rương/bếp/đá nhỏ phải nhỏ hơn người (1.31), nhỏ hơn hẳn lều, v.v.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import size_check
for d in kit_dirs:
    b = os.path.basename(d.rstrip('/'))
    if not os.path.exists(d + 'manifest.json'): continue
    for e in size_check.check_manifest(json.load(open(d + 'manifest.json'))):
        if waived(b + '/' + e.split()[1].rstrip(':'), 'size'): continue
        E(f'[size] {b}: {e[5:]}')

# 3. tile sàn: bản sao đội lốt (cùng ảnh đổi màu)
def xc(a, b):
    a = a - a.mean(); b = b - b.mean()
    c = np.fft.ifft2(np.fft.fft2(a) * np.conj(np.fft.fft2(b))).real
    return c.max() / (np.sqrt((a**2).sum() * (b**2).sum()) + 1e-9)
for d in kit_dirs:
    tiles = []
    for p in sorted(glob.glob(d + '*floor*/final.png')):
        im = np.array(Image.open(p).convert('RGB')).astype(float)
        if im.shape[0] == im.shape[1]: tiles.append((os.path.basename(os.path.dirname(p)), im))
    for (na, a), (nb, b) in itertools.combinations(tiles, 2):
        if a.shape != b.shape: continue
        if waived(f'{os.path.basename(d.rstrip("/"))}/{na}', 'tile') or waived(f'{os.path.basename(d.rstrip("/"))}/{nb}', 'tile'): continue
        if xc(a.mean(2), b.mean(2)) > 0.9: E(f'[tile] {na} và {nb} là CÙNG MỘT ẢNH (tương quan>0.9), chỉ đổi màu')

# 4. contact-sheet và review phải mới hơn manifest
for d in kit_dirs:
    m = d + 'manifest.json'; c = d + 'contact-sheet.png'
    if not os.path.exists(c): E(f'[sheet] {os.path.basename(d.rstrip("/"))}: thiếu contact-sheet.png')
    elif os.path.getmtime(c) + 5 < os.path.getmtime(m): E(f'[sheet] {os.path.basename(d.rstrip("/"))}: contact-sheet.png cũ hơn manifest (chưa cập nhật)')

# 5. layout từng map: validator + bằng chứng render
for lp in sorted(glob.glob(f'{LAYOUTS}/*/*.json')):
    mid = os.path.basename(lp)[:-5]; kitname = os.path.basename(os.path.dirname(lp))
    manifest = f'{ART}/batch-11-{kitname}/manifest.json'
    brief = next(iter(glob.glob(f'{BRIEFS}/*/{mid}.json')), None)
    args = [sys.executable, VALID, lp] + ([brief] if brief else []) + ([manifest] if os.path.exists(manifest) else [])
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0: E(f'[layout] {mid}: validator lỗi\n' + '\n'.join('    ' + x for x in (r.stdout + r.stderr).strip().splitlines()[-8:]))
    base = os.path.join(os.path.dirname(lp), mid)
    for suf in ('_cam_015', '_cam_050', '_cam_085', '_preview'):
        f = f'{base}{suf}.png'
        if not os.path.exists(f): E(f'[layout] {mid}: thiếu ảnh bằng chứng {os.path.basename(f)}')
        elif os.path.getmtime(f) + 5 < os.path.getmtime(lp): E(f'[layout] {mid}: {os.path.basename(f)} cũ hơn layout.json (chưa render lại)')
    if not glob.glob(f'{base}_zoom_*.png'): E(f'[layout] {mid}: thiếu ảnh zoom 2× (cổng/NPC)')

print(f'Art gate: kit {", ".join(kits) or "(không)"}; {len(rows)} asset; {len(errs)} lỗi, {len(warns)} cảnh báo')
c = collections.Counter(e.split(']')[0] + ']' for e in errs)
for k, v in c.items(): print('  ', k, v)
for e in errs: print(' ✗', e)
for w in warns: print(' !', w)
if errs: print('\nCHƯA ĐẠT: sửa hết lỗi trên (kèm nhìn lại ảnh render) rồi mới báo nghiệm thu.')
sys.exit(1 if errs else 0)
