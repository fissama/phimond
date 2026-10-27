#!/usr/bin/env python3
"""Sinh checklist asset theo từng map/kit (Markdown) cho Codex.
Nguồn: map-images (Downloads/Phimond-P12-Review), map-images.json, names master, maps-75 prompt,
briefs, manifest batch-01..04, 11, 12. Ra: .ai/design/map-checklists/*.md + refs/<map_id>.jpg.
Chạy lại để cập nhật trạng thái: python3 tools/build-web-assets/gen_map_asset_checklists.py
"""
import json, re, os, glob, unicodedata, hashlib, collections, pathlib
from PIL import Image

R = pathlib.Path(__file__).resolve().parents[2]
OUT = R / '.ai/design/map-checklists'
(OUT / 'refs').mkdir(parents=True, exist_ok=True)
IMG = next(p for p in (pathlib.Path('~/Downloads/Phimond-P12-Review/map-images').expanduser(),
                       pathlib.Path('~/mnt/Downloads/Phimond-P12-Review/map-images').expanduser()) if p.exists())
ART = R / 'apps/game-web/art-src/hd2d'
MI = json.load(open(IMG.parent / 'map-images.json'))
NAMES = dict(re.findall(r'\| `(\w+)` \| \*\*(.+?)\*\*', open(R / '.ai/plan/phases/P12-world/P12-world-names-master.md').read()))
DOC = open(R / '.ai/design/hd2d-maps-75-gemini-prompt.md').read()


def slug(s):
    s = unicodedata.normalize('NFKD', s.replace('đ', 'd').replace('Đ', 'D'))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def split_top(s):
    out, d, cur = [], 0, ''
    for ch in s:
        if ch in '(（':
            d += 1
        if ch in ')）':
            d -= 1
        if ch == ',' and d == 0:
            out.append(cur.strip())
            cur = ''
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


# ---------- kit từ prompt 75 map ----------
KITS = {}
for m in re.finditer(r'### kit_(\w+) — (.+?) \(.*?\) — (\d+) map\n(.*?)(?=\n### kit_|\n## Phần D)', DOC, re.S):
    k, title, n, body = m.groups()
    style = re.search(r'\*\*Phong cách/bảng màu:\*\* (.+)', body).group(1)
    pieces = re.search(r'\*\*Mảnh tối thiểu cần vẽ cho kit.*?\*\* (.+)', body).group(1)
    rows = re.findall(r'^\| `(\w+)` \| (.+?) \| (\d+) \| (.+?) \| (\d+) \| (.+?) \| (.*?) \|$', body, re.M)
    KITS[k] = dict(title=title, style=style, pieces=pieces,
                   maps=[dict(id=r[0], name=r[1], portals=r[2], monsters=r[3], spawn=r[4], npc=r[5], note=r[6]) for r in rows])
EXTRA = {
    'forest': dict(title='Rừng Lục Bảo', maps=['emerald_forest_main_woods', 'emerald_forest_deep_woods'], batches=['batch-01-octopath'],
                   style='Rừng ôliu/lá ấm, bảng màu phimond-octopath-forest (48 màu)'),
    'city': dict(title='Thành phố, Hoàng Cung, nội thất, trang trại, đấu trường',
                 maps=['city_square', 'city_market', 'city_palace_gate', 'city_royal_palace', 'city_activity_hall', 'city_pet_room',
                       'city_farm', 'city_deathmatch_arena', 'summoning_hall_main_hall'],
                 batches=['batch-02-octopath', 'batch-12-city'], style='Gạch xám ấm, mái ngói đỏ, cổng cung điện, phòng gỗ/đá'),
    'beach': dict(title='Bãi biển châu báu', maps=['treasure_beach_fishermen_beach', 'treasure_beach_east_beach', 'treasure_beach_west_beach',
                                                   'treasure_beach_deep_sea', 'treasure_beach_prosperity_island'],
                  batches=['batch-03-octopath'], style='Cát ấm/cát lạnh, biển lam, san hô, cọ'),
    'ship': dict(title='Tàu cướp biển', maps=['middle_corridor_main_hall'], batches=['batch-04-octopath'],
                 style='Gỗ boong tàu, buồm, đèn bão, cờ hải tặc'),
}


def load_man(b):
    p = ART / b / 'manifest.json'
    if not p.exists():
        return []
    j = json.load(open(p))
    A = j['assets'] if isinstance(j, dict) and 'assets' in j else j
    for a in A:
        a['_batch'] = b
    return A


BATCH_OF_KIT = {'desert': ['batch-11-desert'], 'tomb': ['batch-11-tomb'], 'windrock': ['batch-11-windrock']}
for k, v in EXTRA.items():
    BATCH_OF_KIT[k] = v['batches']
REJECT = {'batch-11-windrock': '❌ Gemini bị trả — vẽ lại', 'batch-11-tomb': '❌ pilot Gemini — vẽ lại'}


def status(a):
    if a['_batch'] in REJECT:
        return REJECT[a['_batch']]
    ap = a.get('approved')
    return '✅ duyệt' if ap is True else ('⏳ nháp, chờ duyệt' if ap is False else '❔ chưa duyệt')


def drawn(a):
    d = ART / a['_batch']
    ok = (d / a['id'] / 'final.png').exists() or (a.get('file') and (d / a['file']).exists())
    return '✅' if ok else '⬜'


def prompt_link(a):
    p = R / f"apps/game-web/art-src/hd2d/{a['_batch']}/{a['id']}/prompt.md"
    return f"[prompt.md]({os.path.relpath(p, OUT)})" if p.exists() else '—'


def cat(a):
    c = a.get('category') or a.get('kind') or ''
    i = a['id']
    if 'portal' in i or 'teleport' in i:
        return 'portal'
    if 'marker' in i:
        return 'marker'
    return 'floor' if c == 'tile' else c


QUOTA = [('floor', 8, 'tile sàn 512×512 seamless, mỗi biến thể là texture khác'), ('edge', 3, 'dải chuyển tiếp 512×128 liền hai đầu'),
         ('prop', 36, 'prop đứng, ≥2–3 biến thể thật/chủng loại'), ('decal', 12, 'decal tiếp đất bất quy tắc, mép mềm'),
         ('shadow', 4, 'bóng procedural alpha mềm (ngoại lệ)'), ('backdrop', 3, 'far/mid/near, lặp ngang liền'),
         ('portal', 2, 'cặp dormant/active cùng mask'), ('marker', 1, 'điểm xuất hiện 4 khung'), ('fx', 3, 'hạt/tia sáng sprite sheet')]


def bucket(c):
    return 'backdrop' if c.startswith('backdrop') else c


def quota_table(A):
    cnt = collections.Counter(bucket(cat(a)) for a in A)
    rows = ['| Loại | Có | Cần tối thiểu | Ghi chú |', '|---|---|---|---|']
    for c, n, note in QUOTA:
        have = cnt.get(c, 0)
        rows.append(f"| {c} | {have} | {n} | {'✅' if have >= n else '⬜ thiếu ' + str(n - have)} · {note} |")
    return '\n'.join(rows)


# NPC batch-05 trùng sprite
H = collections.defaultdict(list)
for p in glob.glob(str(ART / 'batch-05-octopath/npc-*/final.png')):
    H[hashlib.sha256(open(p, 'rb').read()).hexdigest()].append(p.split('/')[-2][4:])
DUP = {i: [j for j in v if j != i] for v in H.values() if len(v) > 1 for i in v}


def pieces_items(text):
    items = []
    for part in re.split(r';\s*', text):
        mode = 'prop'
        mm = re.match(r'(prop|backdrop xa):\s*(.*)', part)
        if mm:
            mode = 'prop' if mm.group(1) == 'prop' else 'backdrop_far'
            part = mm.group(2)
        elif part.startswith('tile'):
            mode = 'floor'
        for it in split_top(part):
            n = 1
            m = re.search(r'×\s*(\d+)', it) or re.search(r'\((\d+) biến thể\)', it)
            if m:
                n = int(m.group(1))
            base = re.sub(r'\s*×\s*\d+', '', re.sub(r'\(\s*\d+ biến thể\)', '', it)).strip().strip('.')
            if base.lower().startswith('tile '):
                base = base[5:]
            if not base:
                continue
            for i in range(n):
                items.append((mode, base, slug(base) + (f'-{i + 1:02d}' if n > 1 else '')))
    return items


def sheet_prompts(kit, title, style):
    return f"""```text
[Dán Master v2: .ai/design/gpt-redo/00-master-v2.md]
Dùng agent-sprite-forge ($generate2dmap cho tile/prop, $generate2dsprite cho prop/decal/FX/marker). Route ảnh: image_gen tích hợp của Codex (kiểm `route_media.py resolve --kind image`). KHÔNG codeart2d, KHÔNG API, KHÔNG vẽ bằng code.
Kit: {title} ({kit}). Style: {style}. Style anchor: batch-01-octopath/contact-sheet.png + 2 sprites.png linh thú.
Mỗi lần gọi: 1 sheet ~6 vật trên nền #FF00FF, bố trí 2×3/3×2, cách nhau ≥48 px, không chạm mép. Giữ raw-01.png byte-identical. Cắt/khử nền/pixel finish bằng script forge. 33–48 màu, alpha nhị phân, lề ≥8 px, 128 px = 1 đơn vị (far 64), người = 1.31 đơn vị (cỡ tối đa vật nhỏ: tools/hd2d_audit/size_check.py).
Mỗi asset: thư mục raw-01/final/prompt.md/review.md/qa.json trong apps/game-web/art-src/hd2d/batch-11-{kit}/<id>/. Tự nhìn 4× nền tối/caro. Xong: `python3 tools/hd2d_audit/art_gate.py batch-11-{kit}` = 0 lỗi, contact-sheet mới hơn manifest.
```"""


def one_liner(title, desc, mode):
    t = {'floor': 'tile sàn nhìn từ trên xuống, seamless 512×512', 'prop': 'prop đứng billboard, pivot giữa-đáy',
         'backdrop_far': 'backdrop xa 1280×384 lặp ngang liền (64 px/đơn vị)'}[mode]
    return f"{desc} — {t}; HD-2D Octopath pixel art, palette {title}, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ."


def ref_image(mid):
    dst = OUT / 'refs' / f'{mid}.jpg'
    im0 = Image.open(IMG / f'{mid}.png')
    if not dst.exists():
        im = im0.convert('RGB')
        w, h = im.size
        if w > 1400:
            im = im.resize((1400, round(h * 1400 / w)), Image.LANCZOS)
        im.save(dst, quality=84, optimize=True)
    return im0.size


def brief_of(mid):
    p = next(iter(glob.glob(str(R / f'.ai/design/map-briefs/*/{mid}.json'))), None)
    return (json.load(open(p)), os.path.relpath(p[:-5] + '.md', OUT)) if p else (None, None)


def brief_lines(b):
    if not b:
        return ['- Brief điểm neo: **chưa có** (thiếu bounds P12). Codex đối chiếu ảnh gốc bằng mắt; Claude bổ sung brief trước khi dựng layout.']
    L = []
    for a in b.get('anchors', []):
        L.append(f"- neo `{a.get('id')}` ({a.get('kind', '')}) {a.get('label', '')}: px {a.get('px') or 'CẦN ĐẶT'}")
    return L or ['- (brief không có neo)']


def asset_table(A):
    rows = ['| Vẽ | Duyệt | id | loại | kích thước (world) | prompt/nguồn |', '|---|---|---|---|---|---|']
    for a in sorted(A, key=lambda a: (cat(a), a['id'])):
        rows.append(f"| {drawn(a)} | {status(a)} | `{a['id']}` | {cat(a)} | {a.get('world') or a.get('world_size') or '—'} | {prompt_link(a)} |")
    return '\n'.join(rows)


CITY_RULES = {
    'city_square': ['city-', 'streetlamp', 'bench', 'barrel', 'wooden-', 'flowerpot', 'handcart', 'well', 'fountain', 'stone-', 'balustrade', 'banner', 'awning', 'market', 'animal', 'walker', 'decal'],
    'city_market': ['awning', 'market', 'city-facade', 'barrel', 'wooden-', 'handcart', 'flowerpot', 'city-roof', 'decal', 'walker'],
    'city_palace_gate': ['palace', 'balustrade', 'stone-steps', 'banner', 'city-statue', 'city-carved'],
    'city_royal_palace': ['royal', 'palace-throne', 'palace-chandelier', 'palace-curtain', 'palace-carpet', 'palace-marble', 'palace-column', 'palace-guard', 'hall-torch'],
    'city_activity_hall': ['hall-', 'pet-', 'banner'], 'city_pet_room': ['pet-', 'hall-'], 'city_farm': ['farm-', 'decal'],
    'city_deathmatch_arena': ['arena'], 'summoning_hall_main_hall': ['summon', 'hall-', 'palace-carpet']}
BEACH_RULES = {
    'treasure_beach_fishermen_beach': ['pier', 'fishing', 'drying', 'fisher', 'shore', 'sand', 'driftwood', 'shell', 'palm'],
    'treasure_beach_east_beach': ['sand', 'palm', 'shell', 'starfish', 'driftwood', 'shore', 'lighthouse', 'coastal'],
    'treasure_beach_west_beach': ['sand', 'palm', 'shell', 'starfish', 'driftwood', 'shore', 'coastal'],
    'treasure_beach_deep_sea': ['coral', 'kelp', 'undersea', 'sea', 'deep', 'seagrass'],
    'treasure_beach_prosperity_island': ['prosperity', 'treasure', 'palm', 'lighthouse', 'shore', 'sand']}


def pick(A, pref):
    return [a for a in A if any(a['id'].startswith(p) or p in a['id'] for p in pref)]


CODEX_HEAD = ('> **Quy tắc bắt buộc cho Codex** (xem README.md): dùng https://github.com/0x0funky/agent-sprite-forge '
              '(generate2dmap / generate2dsprite) với route image_gen tích hợp; cấm codeart2d, API trả phí, vẽ bằng code, lật gương; '
              'không commit; không sửa tools/hd2d_audit/*, gate_waivers.json, check.sh; mỗi asset phải tự nhìn ảnh trước khi ghi "vẽ xong"; '
              'chỉ Claude/owner đánh dấu "duyệt".')
ALL = []


def write_kit(kit, title, style, maps_meta, A, req_items=None, pieces_text=None):
    md = [f"# Kit `{kit}` — {title}", '', CODEX_HEAD, '', f"- Style/palette: {style}",
          f"- Thư mục asset: `apps/game-web/art-src/hd2d/{BATCH_OF_KIT.get(kit, ['batch-11-' + kit])[0]}/`", f"- Số map: {len(maps_meta)}", '']
    if A:
        md += ['## 1. Trạng thái asset hiện có', '',
               f"Tổng {len(A)} · duyệt {sum(1 for a in A if a.get('approved') is True)} · nháp {sum(1 for a in A if a.get('approved') is False)} · khác {sum(1 for a in A if a.get('approved') is None)}",
               '', quota_table(A), '', '### Danh sách asset', '', asset_table(A), '']
    if req_items is not None:
        md += ['## 1. Danh sách asset cần vẽ (kit chưa có asset)', '',
               f"Nguồn: Phần C `hd2d-maps-75-gemini-prompt.md`. Yêu cầu gốc: {pieces_text}", '',
               '| Vẽ | Duyệt | id (số thứ tự; đặt tên tiếng Anh vào manifest `name`) | loại | mô tả + prompt đi kèm |', '|---|---|---|---|---|']
        nfloor = 0
        ctr = collections.Counter()
        for mode, base, sid in req_items:
            nfloor += mode == 'floor'
            short = {'floor': 'floor', 'prop': 'prop', 'backdrop_far': 'backdrop-far'}[mode]
            ctr[short] += 1
            md.append(f"| ⬜ | ⬜ | `{kit}-{short}-{ctr[short]:02d}` | {mode} | {one_liner(title, base, mode)} |")
        for i in range(max(0, 8 - nfloor)):
            md.append(f"| ⬜ | ⬜ | `{kit}-floor-extra-{i + 1:02d}` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |")
        for i in range(1, 4):
            md.append(f"| ⬜ | ⬜ | `{kit}-edge-{i:02d}` | edge | dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc |")
        for i in range(1, 13):
            md.append(f"| ⬜ | ⬜ | `{kit}-decal-{i:02d}` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |")
        for i in range(1, 5):
            md.append(f"| ⬜ | ⬜ | `{kit}-shadow-{i:02d}` | shadow | bóng procedural alpha mềm, màu kit |")
        for nm in ('backdrop-far', 'backdrop-mid', 'backdrop-near'):
            md.append(f"| ⬜ | ⬜ | `{kit}-{nm}` | backdrop | 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác |")
        md += [f"| ⬜ | ⬜ | `{kit}-portal-dormant` | portal | cổng nhìn thẳng mặt trước, đúng tông kit |",
               f"| ⬜ | ⬜ | `{kit}-portal-active` | portal | cùng mask với dormant |",
               f"| ⬜ | ⬜ | `{kit}-marker-arrival` | marker | vòng sáng 4 khung |"]
        md += [f"| ⬜ | ⬜ | `{kit}-fx-{i:02d}` | fx | hạt/tia sáng sprite sheet theo chủ đề |" for i in range(1, 4)]
        md.append('')
    md += ['## 2. Prompt sheet chung cho kit', '', sheet_prompts(kit, title, style), '', '## 3. Từng map', '']
    for mm in maps_meta:
        mid = mm['id']
        w, h = ref_image(mid)
        mi = MI.get(mid, {})
        b, bl = brief_of(mid)
        md += [f"### `{mid}` — {NAMES.get(mid, mm.get('name', ''))}", '', f"![{mid}](refs/{mid}.jpg)", '',
               f"- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/{mid}.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/{mid}.png`, {w}×{h} px, 100 px = 1 đơn vị APK)",
               f"- Nguồn APK: scene `{mi.get('source_scene', '?')}`, {mi.get('sprite_count', '?')} sprite ghép; brief: " + (f"[{bl}]({bl})" if bl else 'chưa có')]
        if 'portals' in mm:
            md.append(f"- Cổng: {mm['portals']} · vùng quái: {mm['monsters']} · spawn: {mm['spawn']} · NPC: {mm['npc']}" + (f" · ghi chú: {mm['note']}" if mm.get('note') else ''))
        md += brief_lines(b)
        if mm.get('npc') and mm['npc'] != '—':
            md.append(f"- NPC cần sprite (batch-05; kiểm trùng): {mm['npc']}")
        sub = []
        if kit == 'city':
            sub = pick(A, CITY_RULES.get(mid, []))
        if kit == 'beach':
            sub = pick(A, BEACH_RULES.get(mid, []))
        if sub:
            md += ['', 'Asset chính cho map này (rút từ kit):', '', asset_table(sub), '']
        else:
            md += ['', 'Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):', '',
                   '| Vẽ | Duyệt | id | loại | mô tả | prompt |', '|---|---|---|---|---|---|',
                   f"| ⬜ | ⬜ | `{mid}-landmark-01` | landmark | (vật nhận diện #1 trong ảnh gốc) | — |",
                   f"| ⬜ | ⬜ | `{mid}-landmark-02` | landmark | (vật nhận diện #2, nếu có) | — |", '']
        md += ['Prompt cho Codex:', '', '```text',
               f"Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map {mid} ({NAMES.get(mid, '')}), kit {kit}.",
               f"Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/{mid}.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.",
               'Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).',
               'Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".', '```', '']
    fn = f"kit-{kit}.md"
    (OUT / fn).write_text('\n'.join(md), encoding='utf-8')
    ALL.append((kit, fn, title, maps_meta, A))


for kit in ('forest', 'city', 'beach', 'ship'):
    A = [a for b in EXTRA[kit]['batches'] for a in load_man(b)]
    if kit == 'beach':
        A += load_man('batch-04-octopath')
    write_kit(kit, EXTRA[kit]['title'], EXTRA[kit]['style'], [dict(id=m) for m in EXTRA[kit]['maps']], A)
for kit, K in KITS.items():
    A = [a for b in BATCH_OF_KIT.get(kit, []) for a in load_man(b)]
    write_kit(kit, K['title'], K['style'], K['maps'], A, req_items=None if A else pieces_items(K['pieces']), pieces_text=K['pieces'])

tot = sum(len(x[3]) for x in ALL)
LABEL = {'forest': 'ĐANG HOÀN THIỆN (v1.0.0)', 'city': 'ĐANG HOÀN THIỆN Hoàng Cung/thành (v1.0.0); phòng còn lại rà lại',
         'desert': 'ĐANG HOÀN THIỆN (GPT vẽ lại, nháp)', 'windrock': 'VẼ LẠI (bản Gemini bị trả)', 'tomb': 'VẼ ĐỦ KIT (pilot Gemini)',
         'beach': 'rà lại cho v1.0.x', 'ship': 'rà lại'}
RM = ["# Checklist asset theo map — Phimond HD-2D (cho Codex)", '',
      f"Sinh bởi `tools/build-web-assets/gen_map_asset_checklists.py` (chạy lại để cập nhật trạng thái). {tot} map / {len(ALL)} kit.", '',
      '## Cách dùng với Codex', '',
      '1. **Cài agent-sprite-forge** (bắt buộc): https://github.com/0x0funky/agent-sprite-forge — Codex: `git clone https://github.com/0x0funky/agent-sprite-forge.git && cd agent-sprite-forge && python -m pip install -r requirements.txt && python tools/install_skills.py --apply --host codex`, rồi mở phiên Codex mới. Bản đã dùng cho batch-00: commit `5324342fdfab72430f4e9604f3fe427009f8596d` (skills ở `~/.codex/skills/`). Cần Python ≥3.10, numpy/Pillow/scipy, ffmpeg ≥5.1.',
      '2. Kiểm route ảnh: `python "<generate2dmedia>/scripts/route_media.py" resolve --kind image` phải ra route image_gen/Codex đã đăng nhập; `forge_doctor.py` báo cấu hình. Nếu route rơi về `codeart2d` → DỪNG và báo (codeart2d chỉ là phương án cuối, bị cấm ở đây).',
      '3. Skills: `generate2dmap` (tile, prop kit, tách/kiểm seam), `generate2dsprite` (prop, icon, FX, đóng gói khung + pixel finish `finish_frames.py`), `generate2dmedia` (định tuyến). Mỗi asset: raw-01 giữ nguyên → cắt/khử nền/finish bằng script forge → `final.png`.',
      '4. Làm theo thứ tự ở bảng trạng thái. Mỗi kit: đọc `kit-<tên>.md`, rà bảng, vẽ theo sheet 6 vật, cập nhật cột Vẽ, chạy `python3 tools/hd2d_audit/art_gate.py batch-11-<kit>`.',
      '5. Luật chung: `.ai/design/gpt-redo/00-master-v2.md` (style DNA, lỗi đã bị trả, tỉ lệ: người chơi = 1.31 đơn vị, bảng cỡ ở `tools/hd2d_audit/size_check.py`). Ảnh gốc từng map nằm ngay trong kit file (đính kèm vào image_gen là bắt buộc).',
      '6. KHÔNG: codeart2d, API trả phí, vẽ bằng code, lật gương, đổi màu để thành asset mới, commit, sửa runtime/gate/waivers. CHỈ Claude/owner đánh "Duyệt".', '',
      '## Trạng thái chung (v1.0.0: đang hoàn thiện Rừng, Hoàng Cung, Sa Mạc)', '',
      '| Kit | Map | Asset có | Duyệt | Việc |', '|---|---|---|---|---|']
for kit, fn, title, maps, A in ALL:
    RM.append(f"| [{kit}]({fn}) {title} | {len(maps)} | {len(A)} | {sum(1 for a in A if a.get('approved') is True)} | {LABEL.get(kit, 'CHƯA CÓ asset — vẽ mới')} |")
RM += ['', '## Map → file', '']
for kit, fn, title, maps, A in ALL:
    RM.append(f"- **{kit}**: " + ', '.join(f"[`{m['id']}`]({fn}#{m['id']})" for m in maps))
RM += ['', '## NPC (batch-05)', '', f"- {len(DUP)} NPC đang dùng chung sprite với NPC khác (xem `.ai/design/gpt-redo/04-batch-05-npc-redo.md`). Mỗi map liệt kê NPC roster; Codex chỉ vẽ lại NPC trùng.", '']
(OUT / 'README.md').write_text('\n'.join(RM), encoding='utf-8')
print(tot, 'map', len(ALL), 'kit', len(DUP), 'npc trùng')
