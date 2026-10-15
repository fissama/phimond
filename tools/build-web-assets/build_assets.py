#!/usr/bin/env python3
"""Xuất asset runtime cho apps/game-web từ nguồn đã duyệt.

  python3 tools/build-web-assets/build_assets.py [--atlas-dir DIR] [--actors-dir DIR] [--out DIR]

- Pet: atlas P10 4x5 ô 281px (idle/move/attack/cast/down, quay trái) -> WebP lossless full + nửa độ phân giải
  + manifest (feet = khoảng trống đáy ô, w = bề rộng thân), cho từng loài server (legacy) qua legacy-species-map.json.
- Người chơi: Boy Idle/Run 6 khung -> atlas 6x2 ô 64px.
- NPC: 5 sprite 80x80.
Nguồn mặc định lấy từ owner-atlas-selection.json (đường dẫn trong repo).
"""
import argparse, json, os, shutil
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
CELL, COLS, ROWS = 281, 4, 5
ROW_NAMES = ['idle', 'move', 'attack', 'cast', 'down']

ap = argparse.ArgumentParser()
ap.add_argument('--atlas-dir', help='thư mục chứa <id>.png (vd 0111.png); mặc định dùng đường dẫn trong owner-atlas-selection.json')
ap.add_argument('--actors-dir', help='thư mục chứa idle/ run/ và level*_*.png')
ap.add_argument('--out', default=os.path.join(ROOT, 'apps', 'game-web', 'public', 'assets'))
a = ap.parse_args()

mapping = json.load(open(os.path.join(HERE, 'legacy-species-map.json')))
mapping.pop('_note', None)
sel_path = os.path.join(ROOT, '.ai/plan/phases/P10-pet-model/redraw-kit/owner-atlas-selection.json')
selection = json.load(open(sel_path))['species'] if os.path.exists(sel_path) else {}

def atlas_source(sid):
    if a.atlas_dir:
        return os.path.join(a.atlas_dir, sid.replace('species_', '') + '.png')
    return os.path.join(ROOT, selection[sid]['candidate_path'])

out_pets = os.path.join(a.out, 'pets'); os.makedirs(out_pets, exist_ok=True)
out_act = os.path.join(a.out, 'actors'); os.makedirs(out_act, exist_ok=True)

manifest = {'cell': CELL, 'cols': COLS, 'rows': ROWS, 'rowNames': ROW_NAMES, 'species': {}, 'legacy': {}}
for sid in sorted({m['species'] for m in mapping.values()}):
    im = Image.open(atlas_source(sid)).convert('RGBA')
    assert im.size == (CELL * COLS, CELL * ROWS), (sid, im.size)
    arr = np.array(im)
    feet, wid, head = [], [], []
    for r in range(ROWS):
        fr, wr, hr = [], [], []
        for c in range(COLS):
            alpha = arr[r * CELL:(r + 1) * CELL, c * CELL:(c + 1) * CELL, 3] > 40
            ys, xs = np.where(alpha)
            if len(ys) == 0:
                fr.append(0); wr.append(0); hr.append(0); continue
            fr.append(int(CELL - 1 - ys.max()))       # px trống dưới chân
            wr.append(int(xs.max() - xs.min() + 1))
            hr.append(int(CELL - ys.min()))           # px từ đáy ô đến đỉnh
        feet.append(fr); wid.append(wr); head.append(hr)
    # ô chân dung vuông quanh khung idle đầu tiên (toạ độ trong atlas)
    a0 = arr[0:CELL, 0:CELL, 3] > 40
    ys0, xs0 = np.where(a0)
    bx0, bx1, by0, by1 = int(xs0.min()), int(xs0.max()), int(ys0.min()), int(ys0.max())
    side = max(bx1 - bx0, by1 - by0) + 24
    cx, cy = (bx0 + bx1) // 2, (by0 + by1) // 2
    px0 = max(0, min(CELL - side, cx - side // 2)); py0 = max(0, min(CELL - side, cy - side // 2))
    name = sid
    im.save(os.path.join(out_pets, name + '.webp'), 'WEBP', lossless=True, quality=100, method=6)
    im.resize((im.width // 2, im.height // 2), Image.BOX).save(os.path.join(out_pets, name + '_s.webp'), 'WEBP', lossless=True, method=6)
    # chân neo = hàng idle (đáy thấp nhất của 4 khung); chiều cao = trung bình hàng idle
    manifest['species'][sid] = dict(file=name + '.webp', small=name + '_s.webp', feet=feet, width=wid, height=head,
                                    portrait=[px0, py0, side], footPad=min(feet[0]), bodyH=int(np.mean(head[0])), bodyW=int(np.mean(wid[0])))
for legacy, m in mapping.items():
    manifest['legacy'][legacy] = dict(species=m['species'], artPending=bool(m.get('art_pending')))
json.dump(manifest, open(os.path.join(out_pets, 'manifest.json'), 'w'), indent=1)

# người chơi
src = a.actors_dir or os.path.join(ROOT, 'apps/game-client/assets/reference')
def frames(folder):
    return [Image.open(os.path.join(folder, f'{i:03d}.png')).convert('RGBA') for i in range(6)]
if a.actors_dir:
    idle, run = frames(os.path.join(src, 'idle')), frames(os.path.join(src, 'run'))
else:
    idle, run = frames(os.path.join(src, 'actors/Boy/Idle')), frames(os.path.join(src, 'actors/Boy/Run'))
pl = Image.new('RGBA', (64 * 6, 64 * 2), (0, 0, 0, 0))
for r, fr in enumerate([idle, run]):
    for i, f in enumerate(fr):
        pl.alpha_composite(f, (i * 64 + (64 - f.width) // 2, r * 64 + 64 - f.height))
pl.save(os.path.join(out_act, 'player.webp'), 'WEBP', lossless=True)
npcs = {'trainer': 'level3_1030', 'ranch_keeper': 'level3_1029', 'arena_master': 'level3_1024', 'forest_guide': 'level4_353', 'beach_guide': 'level5_668'}
npc_dir = src if a.actors_dir else os.path.join(src, 'npcs')
nm = {}
for k, f in npcs.items():
    im = Image.open(os.path.join(npc_dir, f + '.png')).convert('RGBA')
    bb = im.getbbox() or (0, 0, 80, 80)
    nm[k] = dict(file=f'npc_{k}.webp', w=im.width, h=im.height, bbox=list(bb))
    im.save(os.path.join(out_act, f'npc_{k}.webp'), 'WEBP', lossless=True)
json.dump(dict(player=dict(file='player.webp', cols=6, rows=2, cell=64, idle=[0, 6], run=[6, 12], fps=8), npcs=nm),
          open(os.path.join(out_act, 'manifest.json'), 'w'), indent=1)
print('ok', len(manifest['species']), 'species;', sum(os.path.getsize(os.path.join(out_pets, f)) for f in os.listdir(out_pets)) // 1024, 'KB pets')
