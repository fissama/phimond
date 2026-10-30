#!/usr/bin/env python3
"""Sinh dữ liệu runtime v1.0.0 từ các phase đã đóng thiết kế: P11 (160 loài, chỉ số, MP) và P13 (97 kỹ năng, pool bản
địa 160 loài, bảng hệ). Ghi đè data/pets/species.json, data/skills/skills.json, data/skills/statuses.json, đổi id loài
cũ trong map/recipes/quests sang id chuẩn species_XXXX.

Chạy: python3 tools/p01/apply_p11_p13.py [--plan DIR]   (DIR mặc định .ai/plan/phases; cần P11-stats và P13-skills)
Nguồn: P11-species-catalog-160.json, P13-skills/roster-review-package.json (V7.1 đã duyệt 2026-10-20).
Xuất lại nhiều lần cho kết quả giống nhau (không dùng ngẫu nhiên).
"""
import argparse, json, re, sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ap = argparse.ArgumentParser()
ap.add_argument('--plan', default=str(ROOT / '.ai/plan/phases'))
args = ap.parse_args()
PLAN = Path(args.plan)

# id loài cũ (server 1.0.0 trước P11) -> id chuẩn. Lấy từ bảng hiển thị đã duyệt của client (legacy-species-map.json);
# 4 loài cũ chưa có ảnh (artPending) trỏ sang loài chuẩn cùng Race/Sao gần nhất ở phần STAND_IN bên dưới.
LEGACY = {k: v['species'] for k, v in json.load(open(ROOT / 'tools/build-web-assets/legacy-species-map.json')).items() if not k.startswith('_')}

def D(x):
    return Decimal(str(x))

def milli(x):  # chuỗi/số thập phân -> số nguyên nghìn, chính xác
    v = D(x) * 1000
    assert v == v.to_integral_value(), x
    return int(v)

p11 = json.load(open(PLAN / 'P11-stats/P11-species-catalog-160.json'))['records']
pkg = json.load(open(PLAN / 'P13-skills/roster-review-package.json'))
pools = {s['id']: s for s in pkg['species']}
assert len(p11) == 160 and len(pools) == 160

STAT_KEYS = ['hp', 'atk', 'mag', 'def', 'spd', 'status_resistance']
CAPTURE = {1: 0.24, 2: 0.18, 3: 0.12, 4: 0.08, 5: 0.05}

species = {}
for sid, r in sorted(p11.items()):
    pool = pools[sid]
    # Hai nguồn phải khớp chỉ số (P13 sinh từ P11); lệch là lỗi nguồn, dừng thay vì đoán.
    assert pool['base_stats'] == r['base_stats'] and pool['growth_baseline'] == r['growth_baseline'], sid
    cls = r['species_class']
    species[sid] = {
        'id': sid,
        'name': r['name_vi'],
        'race': r['race_id'],
        'element': r['element_id'],
        'star': r['star'],
        'class': cls,
        'roles': r['role_ids'],
        'primary_role': r['primary_role'],
        'secondary_role': r['secondary_role'],
        'base': {k: r['base_stats'][k] for k in STAT_KEYS},
        'growth_milli': {k: milli(r['growth_baseline'][k]) for k in STAT_KEYS},
        'mp_base': r['mp_profile']['base'],
        'mp_growth_milli': milli(r['mp_profile']['growth']),
        'skills': pool['native_skills'],
        'capture_rate': CAPTURE[r['star']] if cls == 'normal' else 0,
        'catchable': cls == 'normal',
        'description': r.get('gameplay_description_vi', ''),
        'confidence': 'authored',
        'source': 'P11 catalog v3 (' + json.load(open(PLAN / 'P11-stats/P11-species-catalog-160.json'))['catalog_version'] + ') + P13 ' + pkg['revision'],
    }

# ---- kỹ năng ----
def eff(e):
    if not e:
        return {}
    o = {}
    for k, v in e.items():
        if k == 'chance':
            o['chance_pm'] = milli(v)
        elif k == 'amount':
            o['amount_bp'] = int(D(v) * 10000)
        elif k == 'penetration':
            o['penetration_pm'] = milli(v)
        elif k in ('tick_power', 'shield_mag', 'shield_hp', 'heal_mag'):
            o[k + '_pm'] = milli(v)
        else:
            o[k] = v  # status, stat, hits, self_buff, cleanse, cleanse_one, heal_flat
    return o

skills = {}
for s in pkg['skills']:
    skills[s['id']] = {
        'id': s['id'], 'name': s['name'], 'kind': s['kind'], 'target': s['target'], 'mp': s['mp'], 'cooldown': s['cooldown'],
        'learn_level': s['learn_level'], 'element': s['element'], 'description': s['description'], 'functions': s['functions'],
        'inheritance': s['inheritance'], 'power_pm': milli(s['power']) if s['power'] is not None else 0, 'effect': eff(s['effect']),
        'rank_policy': s['rank_policy'], 'channel': s['action_channel'], 'shape': s['target_shape'], 'damage_mode': s['damage_mode'],
        'exclusive_species': s.get('exclusive_species', ''), 'confidence': 'authored',
        'source': 'P13 ' + pkg['revision'] + ' (' + s['provenance'] + ')',
    }
assert len(skills) == 97
for sp in species.values():
    for k in sp['skills']:
        assert k in skills, (sp['id'], k)

# ---- trạng thái (tên lấy từ kỹ năng cùng id; hành vi nằm trong code theo P13 §5) ----
def sname(i, fb):
    return skills[i]['name'] if i in skills else fb
STATUSES = {
    'sleep': ('control', None), 'petrify': ('control', None), 'confuse': ('control', None),
    'bind': ('restraint', None), 'silence': ('restraint', None),
    'slow': ('debuff', 'Chậm'), 'blind': ('debuff', None), 'misfortune': ('debuff', None), 'frailty': ('debuff', 'Suy nhược'),
    'poison': ('dot', 'Trúng độc'), 'burn': ('dot', 'Bỏng cháy'),
}
statuses = {i: {'id': i, 'name': (fb or sname(i, i)), 'kind': k, 'confidence': 'authored', 'source': 'P13 §5'} for i, (k, fb) in STATUSES.items()}
for i, n in [('shield', 'Khiên'), ('regen', 'Hồi sinh lực'), ('grace', 'Miễn khống chế')]:
    statuses[i] = {'id': i, 'name': n, 'kind': 'buff' if i != 'grace' else 'grace', 'confidence': 'authored', 'source': 'P13 §5'}

def dump(path, obj):
    Path(ROOT / path).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + '\n')

dump('data/pets/species.json', species)
dump('data/skills/skills.json', skills)
dump('data/skills/statuses.json', statuses)

# ---- đổi id cũ trong dữ liệu khác ----
# 4 loài cũ chưa có ảnh: chọn loài chuẩn Normal cùng Race và Sao, ưu tiên role Hybrid/Phép; ổn định theo id.
STAND_IN_SPEC = {'grove_guardian': ('plant', 2), 'tide_sentinel': ('spirit', 3), 'moon_warden': ('undead', 4), 'dawn_sovereign': ('bird', 5)}
for old, (race, star) in STAND_IN_SPEC.items():
    cands = sorted((s for s in species.values() if s['race'] == race and s['star'] == star and s['class'] == 'normal'), key=lambda s: (0 if 'hybrid' in s['roles'] else 1, s['id']))
    LEGACY[old] = cands[0]['id']

ID_RE = re.compile(r'"(' + '|'.join(sorted(LEGACY, key=len, reverse=True)) + r')"')
changed = []
# Công thức: chỉ đổi parent_a/parent_b/result (id công thức giữ nguyên).
rp = ROOT / 'data/recipes/recipes.json'
rec = json.load(open(rp))
before = json.dumps(rec, sort_keys=True)
for r in rec.values():
    for k in ('parent_a', 'parent_b', 'result'):
        r[k] = LEGACY.get(r[k], r[k])
if json.dumps(rec, sort_keys=True) != before:
    rp.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + '\n')
    changed.append('data/recipes/recipes.json')
for rel in ['data/quests/quests.json'] + sorted(str(p.relative_to(ROOT)) for p in (ROOT / 'data/maps').rglob('*.json')):
    p = ROOT / rel
    txt = p.read_text()
    new = ID_RE.sub(lambda m: '"' + LEGACY[m.group(1)] + '"', txt)
    if new != txt:
        p.write_text(new)
        changed.append(rel)
print('species', len(species), 'skills', len(skills), 'statuses', len(statuses))
print('đổi id trong:', *changed, sep='\n  ')
print('stand-in:', {k: LEGACY[k] for k in STAND_IN_SPEC})

# bảng id loài cũ -> chuẩn, dùng để chuyển save trước P11 (MigrateLegacy); chỉ các id còn tồn tại
(ROOT / 'data/pets/legacy_species.json').write_text(json.dumps({k: v for k, v in sorted(LEGACY.items()) if v in species and k not in species}, ensure_ascii=False, indent=1) + '\n')
