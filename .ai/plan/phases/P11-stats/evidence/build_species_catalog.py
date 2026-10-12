#!/usr/bin/env python3
"""Reproduce/check the P11 design catalog; never writes runtime content or simulates play."""
import argparse
from collections import Counter
from decimal import Decimal as D, ROUND_HALF_UP, ROUND_FLOOR
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PHASE = ROOT / '.ai/plan/phases/P11-stats'
SOURCE = ROOT / 'data/p10/species.json'
REGISTRY = ROOT / 'data/p10/id_registry.json'
STATS = ('hp', 'atk', 'mag', 'def', 'spd', 'status_resistance')
ROLES = {'P': 'physical_dps', 'M': 'magic_dps', 'T': 'tank', 'S': 'support', 'D': 'disruptor', 'H': 'hybrid'}
ELEMENTS = {'F': 'fire', 'W': 'water', 'A': 'wind', 'E': 'earth', 'L': 'light', 'D': 'dark'}
SHARES = {'P': (25,45,10,20), 'M': (25,10,45,20), 'T': (40,15,10,35), 'H': (25,30,30,15), 'S': (25,25,25,25), 'D': (25,25,25,25)}
ROLE_INTENT = {'P': 'physical damage', 'M': 'magic damage', 'T': 'frontline survival and protection', 'S': 'ally recovery, protection or cleansing', 'D': 'action control or offensive-stat debuffs beyond HP damage', 'H': 'usable physical and magic damage'}

# Explicit per-ID design decisions, NOT classification rules inferred from Race,
# recipes, empty prose, or image matching. First token ID, then Element, Primary,
# optional Secondary. Short note is intentional Phimond role/Element direction.
CHOICES = '''
1 D P - spectral physical hunter
2 E T S durable bone guard with ally healing
3 D P T dark claw attacker with bulk
4 D M - curse caster; resistance is not a control skill
5 E T - slow durable corpse wall
6 D M - spectral vitality caster
7 F P - aggressive infernal physical hound
8 F M S flame caster with single-target recovery
9 D P - authored claw attacker; source prose absent
10 W P T aquatic bone bruiser
11 D P - counterattacking butcher
12 D T D bulky curse controller
13 D P S physical shade with cleanse support
14 E M S forest occult caster with ally buffs
15 D P S death-themed attacker with petrification cleanse
16 D M D confusion caster
17 W P T ice-themed physical dragon
18 D M S authored bone queen with ally protection
19 D M D authored underworld control caster
20 D T P authored armored dark commander
21 E T - authored thorn guard
22 L S M authored flower healer with magic fallback
23 E D - authored fungal action inhibition, beyond poison damage
24 E M - authored woodland caster
25 W M - concealed aquatic group caster
26 E P T strong living-wood bruiser
27 D D - authored fright and attack-debuff fruit
28 W S M team healer with aquatic magic
29 E T S bamboo guard with recovery
30 E P D authored biting plant with binding
31 E P - repeated physical damage does not imply Disruptor
32 E P T sturdy flower fighter
33 L M D light-themed caster with defense reduction
34 D T D pumpkin guard with binding
35 E T S authored elder tree protector
36 E P T multiheaded plant bruiser
37 E D M authored vine binding and magic; poison alone insufficient
38 L S T flower spirit team recovery with defensive emphasis
39 A P - fast winged physical attacker
40 F P - red dragon physical offense
41 E M T intelligent resilient bone serpent
42 D H S physical and magic dragon with minor healing
43 E T D high-vitality dragon with weakening
44 E P D claw attacker with defense reduction
45 E T M rock dragon with magic support offense
46 E M - armored magic attacker with self enhancement
47 F P S flame dragon with ally combat support
48 A M - thunder-themed magic dragon
49 E D T weakening-focused durable emerald dragon
50 W M D water caster with action control
51 D H - authored dark dragon dual damage
52 L H S authored ancient holy dragon with protection
53 F M - authored small infernal caster
54 W P S fast sea attacker with recovery
55 D M S eye caster with healing
56 D P T armored demonic claw fighter
57 F H - infernal agile dual attacker
58 F P - authored infernal hunting hound
59 F P T resilient demonic warrior
60 E T P counterattacking durable beast
61 D M - broadly balanced demonic caster
62 D M D caster reducing enemy physical offense
63 F P T slow powerful demon general
64 D D - binding dancer and attack debuffer
65 D M - divination-themed high magic attacker
66 D M D magic attacker with offensive debuffs
67 F P T durable infernal physical king
68 W H - authored azure dragon dual damage
69 D S M authored fallen angel protective magic
70 E P - authored large-claw beast
71 F P - authored red raptor physical offense
72 E T D authored living tree guard with roots
73 W T S authored turtle guard with ally protection
74 E P - authored grounded wolf hunter
75 E T - authored armored pangolin
76 E P - authored saber-tooth attacker
77 W P S polar bird with ally buffs
78 E S - authored flock protector with recovery
79 W D M authored ink-based accuracy impairment and magic
80 E P T authored sturdy scarred bear
81 F T S lava turtle with group buffs
82 E P T high-vitality physical elephant
83 F M S fox caster with ally resource support
84 E T D vitality-focused ape with binding
85 W P D snow attacker with blindness
86 L M - eastern magic panda
87 A P - authored swift white tiger
88 F P - authored flame wolf hunter
89 A P S small bird attacker with recovery
90 D D - authored bat disorientation beyond HP damage
91 A P - authored crested aerial attacker
92 A P T thunder bird with physical group attack
93 D P S swift dark raptor with healing
94 A M - authored owl wind caster
95 A P - authored aerial scavenger fighter
96 D M - dark harpy caster
97 D M D vitality caster with slowing
98 D P S grave raven with ally speed support
99 A P - physical bird; self resistance does not imply Support
100 A P - authored poison-claw attacker; poison not control
101 A P D griffin attacker with slowing
102 F M - red-feather caster with self speed
103 A D M sleep and group slow with magic fallback
104 A P S bird attacker with speed and silence cleanse
105 F M S authored vermilion bird with recovery
106 D M D fast infernal owl with slowing
107 L P - authored golden eagle physical offense
108 E P - venom attacker; no control role from venom alone
109 E M - earth magic scorpion directly described in source
110 E T P armored mantis physical guard
111 W T - heavily defended snail
112 E P - authored mountain spider claw offense
113 E H - explicitly physical and magic beetle
114 E P T authored armored saber beetle
115 E P D burrowing attacker with max-HP debuff
116 E M - magic and poison locust; poison not control
117 E M T sturdy magic beetle with self vitality
118 A S M butterfly group healing with magic fallback
119 W T H aquatic guard with both damage modes
120 W P S lobster with curse cleanse and ally vitality
121 W M D sea caster with max-HP impairment
122 D M D curse insect with misfortune impairment
123 E P D physical insect with petrification
124 E T - authored durable underground insect
125 L M - vitality-focused spirit-touched caster
126 E S D authored brood protector with enemy binding
127 E P S chest fighter with recovery
128 A M - wind construct area magic
129 F P T lava physical bruiser
130 E T - stone guard with petrification resistance
131 D M - void caster with speed emphasis reserved for skills
132 L M S spellbook caster with healing
133 D P - magic sword physical attack with self vitality
134 E P D stone construct with weakening
135 D M T sturdy magic jack-in-box
136 E D P authored scarecrow binding and physical fallback
137 L M D reflective caster with misfortune impairment
138 F P D lava bruiser with group magic-offense debuff
139 W T S authored sacred turtle protector
140 E H - authored sphinx dual attacker
141 E S M authored totem ally buffs with magic fallback
142 E P T authored giant warrior bruiser
143 A M S authored djinn with ally protection
144 L S M authored flower spirit healer
145 E T S authored great tree protector
146 D M - authored vampiric caster; self recovery not Support
147 W T P authored ancient snow guard
148 E P S authored grass-mud mount with ally protection
149 L P - authored golden unicorn attacker
150 W T S authored island guardian with ally protection
151 E P D authored scorpion king with binding beyond poison
152 L S M authored love bird healer with magic fallback
'''

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rounded(value, growth):
    return value.quantize(D('.001') if growth else D(1), rounding=ROUND_HALF_UP)

def number(value):
    return int(value) if value == int(value) else float(value)

def targets(source, primary, secondary, growth):
    star = source['star']
    special = source['species_class'] == 'special'
    budget = D(({4:148,5:172}[star] if special else [100,110,122,136,160][star-1]))
    if growth:
        budget *= D('.02')
    weights = [(primary, D('.75')), (secondary, D('.25'))] if secondary else [(primary, D(1))]
    shares = [sum(D(SHARES[r][i])/100*w for r,w in weights) for i in range(4)]
    result = dict(zip(STATS[:4], [budget*shares[0]*10]+[budget*s for s in shares[1:]]))
    sr_star = ({4:D('1.105'),5:D('1.135')}[star] if special else [D(s) for s in ('1','1.03','1.06','1.09','1.12')][star-1])
    spd_star = ({4:D('1.07'),5:D('1.09')}[star] if special else [D(s) for s in ('1','1.02','1.04','1.06','1.08')][star-1])
    result['status_resistance'] = (D('.510') if growth else D(20))*sr_star*sum((D('1.1') if r in ('T','S') else D(1))*w for r,w in weights)
    result['spd'] = (D('1.020') if growth else D(40))*spd_star*sum({'T':D('.9'),'S':D('1.05'),'D':D('1.1')}.get(r,D(1))*w for r,w in weights)
    return budget, result

def authored_values(source, template, growth):
    values = {stat:rounded(value,growth) for stat,value in template.items()}
    if source['race_id'] == 'bird':
        # Owner-approved authoring priority, already embedded in Species values.
        # Floor at the +5% boundary so quantization never exceeds the band.
        values['spd'] = (template['spd']*D('1.05')).quantize(
            D('.001') if growth else D(1), rounding=ROUND_FLOOR)
    return values

def validate_bird_priority(records):
    # A strict Lv1 advantage plus nonlower growth proves ordering for every
    # legal level and common grade under cumulative floor, without simulation.
    cohort = lambda r:(r['star'],r['species_class'],r['primary_role'],r['secondary_role'])
    birds=[r for r in records.values() if r['race_id']=='bird']
    others=[r for r in records.values() if r['race_id']!='bird']
    pairs=0
    for bird in birds:
        for other in others:
            if cohort(bird)!=cohort(other): continue
            assert bird['base_stats']['spd']>other['base_stats']['spd'],(bird['id'],other['id'],'Bird base ordering')
            assert D(str(bird['growth_baseline']['spd']))>=D(str(other['growth_baseline']['spd'])),(bird['id'],other['id'],'Bird growth ordering')
            pairs+=1
    # Also cover legal cohorts absent from this frozen roster, not just those
    # which happen to contain both a Bird and another Race today.
    templates=0
    for star,special in [(s,False) for s in range(1,6)]+[(4,True),(5,True)]:
        source={'star':star,'species_class':'special' if special else 'normal','race_id':'bird'}
        for primary in SHARES:
            for secondary in [None]+[r for r in SHARES if r!=primary]:
                _,base=targets(source,primary,secondary,False)
                _,growth=targets(source,primary,secondary,True)
                bird_base=authored_values(source,base,False)['spd']
                bird_growth=authored_values(source,growth,True)['spd']
                assert bird_base>rounded(base['spd'],False)
                assert bird_growth>=rounded(growth['spd'],True)
                templates+=1
    return {'birds':len(birds),'actual_same_cohort_pairs':pairs,'template_cohorts':templates,
            'comparison':'same Star/class, ordered role blend, level and SPD grade; no inheritance/equipment/effects',
            'proof':'strict integer base SPD advantage and nonlower growth imply strict grown SPD advantage at every level with a common positive multiplier'}

def build():
    source = json.loads(SOURCE.read_text())['records']
    records = {}
    for line in CHOICES.strip().splitlines():
        ordinal, element, primary, secondary, note = line.split(' ', 4)
        key = f'species_{int(ordinal):04d}'
        assert key not in records, key
        s = source[key]
        secondary = None if secondary == '-' else secondary
        desc = s['description']['vi']
        rec = {'id':key, 'name_vi':s['display_name']['vi'], 'race_id':s['race_id'], 'star':s['star'], 'species_class':s['species_class'], 'element_id':ELEMENTS[element], 'primary_role':ROLES[primary], 'secondary_role':ROLES.get(secondary), 'role_ids':[ROLES[r] for r in (primary, secondary) if r], 'source_identity':s['source'], 'source_description_vi':desc, 'source_description_status':'observed_qualitative_only' if desc else 'missing_not_recovered', 'assignment_provenance':'phimond_authored_design_v1_not_source_certified', 'approval_basis':'owner_delegated_P11_design_completion_2026-10-12', 'rationale':note, 'p13_native_pool_contract':{'primary_function':ROLE_INTENT[primary], 'secondary_function':ROLE_INTENT.get(secondary), 'status':'required_future_skill_design_not_implemented'}, 'element_provenance':'Phimond authored thematic placement; no Race mapping or source chart claim', 'numeric_provenance':'approved role/budget targets; Bird SPD authored at upper +5% bound with floor-to-grid; other values nearest half-up; no runtime Race bonus', 'layers':{}}
        for growth, name in ((False,'base_stats'),(True,'growth_baseline')):
            budget, exact = targets(s, primary, secondary, growth)
            values = authored_values(s, exact, growth)
            rec[name] = {stat:number(value) for stat,value in values.items()}
            rec['layers'][name] = {'main_target':number(budget), 'main_budget':number(values['hp']/10+sum(values[k] for k in ('atk','mag','def'))), 'exact_role_template':{k:str(v) for k,v in exact.items()}, 'relative_modifiers':{k:str(values[k]/exact[k]-1) for k in STATS}, 'main_tolerance':'.02' if s['species_class']=='special' else '.03'}
        records[key] = rec
    return {'schema_version':1, 'status':'design_only_not_runtime', 'catalog_version':'P11-v1.1-bird-spd-2026-10-12', 'authority':'owner-authorized autonomous P11 design completion; future runtime activation separate', 'source_species_sha256':digest(SOURCE), 'source_registry_sha256':digest(REGISTRY), 'element_ids':list(ELEMENTS.values()), 'records':records}

def validate(catalog):
    source = json.loads(SOURCE.read_text())['records']
    registry = json.loads(REGISTRY.read_text())['species']
    records = catalog['records']
    assert set(records)==set(source) and len(records)==152
    assert catalog['source_species_sha256']==digest(SOURCE)
    assert catalog['source_registry_sha256']==digest(REGISTRY)
    counts = Counter(s['species_class'] for s in source.values())
    assert counts=={'normal':135,'special':17}
    assert Counter(s['star'] for s in source.values() if s['species_class']=='special')=={4:4,5:13}
    reverse = {v:k for k,v in ROLES.items()}
    checked = 0
    for key, rec in records.items():
        s = source[key]
        assert registry[s['source']['species_id']]==key==rec['id']
        assert rec['source_identity']==s['source']
        assert rec['name_vi']==s['display_name']['vi']
        assert rec['source_description_vi']==s['description']['vi']
        for field in ('star','species_class','race_id'):
            assert rec[field]==s[field]
        assert rec['element_id'] in ELEMENTS.values()
        primary=reverse[rec['primary_role']]
        secondary=reverse[rec['secondary_role']] if rec['secondary_role'] else None
        assert secondary!=primary
        assert rec['role_ids']==[ROLES[r] for r in (primary,secondary) if r]
        for growth,name in ((False,'base_stats'),(True,'growth_baseline')):
            values={k:D(str(v)) for k,v in rec[name].items()}
            assert set(values)==set(STATS)
            target, template=targets(s,primary,secondary,growth)
            B=values['hp']/10+sum(values[k] for k in ('atk','mag','def'))
            tolerance=D('.02') if s['species_class']=='special' else D('.03')
            assert abs(B/target-1)<=tolerance,(key,name,'budget')
            assert D(str(rec['layers'][name]['main_budget']))==B
            assert D(str(rec['layers'][name]['main_target']))==target
            assert rec['layers'][name]['exact_role_template']=={k:str(v) for k,v in template.items()}
            for k,v in values.items():
                assert v>0 and v==rounded(v,growth),(key,name,k,'precision')
                assert abs(v/template[k]-1)<=(D('.05') if k in STATS[4:] else D('.10')),(key,name,k,'deviation')
            if primary=='P': assert values['atk']>=D('.35')*B and values['atk']>=D('1.25')*values['mag'],(key,name,'P signature')
            if primary=='M': assert values['mag']>=D('.35')*B and values['mag']>=D('1.25')*values['atk'],(key,name,'M signature')
            if primary=='T': assert values['hp']/10+values['def']>=D('.60')*B,(key,name,'T signature')
            if primary=='H': assert min(values['atk'],values['mag'])>=D('.20')*B and values['atk']+values['mag']>=D('.50')*B,(key,name,'H signature')
            checked+=1
    bird_priority=validate_bird_priority(records)
    assert sum(not s['description']['vi'] for s in source.values())==55
    return {'status':'PASS', 'scope':'static design artifact validation; no runtime, combat or long-run simulation', 'species_records':152,'layers_checked':checked,'bird_spd_priority':bird_priority, 'normal':135,'special':17,'special4':4,'special5':13,'source_descriptions_present':97,'source_descriptions_missing':55,'primary_roles':dict(sorted(Counter(r['primary_role'] for r in records.values()).items())),'elements':dict(sorted(Counter(r['element_id'] for r in records.values()).items())),'checks':['frozen ID/registry equality and source hashes','frozen identity/name/Race/Star/class/source descriptions preserved','152 unique complete assignments','integer base / <=3-decimal growth / positive six stats','exact targets and 75/25 secondary blending','independent base/growth main-budget tolerances','independent per-stat main +/-10%, auxiliary +/-5%','Physical/Magic/Tank/Hybrid Primary signatures both layers','Bird strict base SPD/nonlower growth against same-cohort non-Birds; all252 template cohorts','source limitations retained; no inferred recovery','generated JSON/Markdown deterministic reproduction'], 'source_species_sha256':digest(SOURCE), 'source_registry_sha256':digest(REGISTRY)}

def markdown(catalog):
    lines=['# P11 — 152 Species catalog v1.1: Bird speed priority','', 'Status: **DESIGN COMPLETE; NOT RUNTIME-ACTIVATED**, 2026-10-12.', '', 'These are Phimond authoring decisions under the owner’s delegated P11 completion scope. The frozen roster remains unchanged. This companion JSON is the complete stat/Element/role design, not a replacement runtime dataset, save migration, recovered APK table or P13 skill implementation.', '', '## Provenance and constraints', '', '- 152 frozen IDs: 135 Normal, 4 Special4★, 13 Special5★. Names, Race, Star, class, source IDs, assets and recipes remain frozen in their existing files; no art or parent recipe is edited.', '- 97 source descriptions are quoted verbatim in JSON as qualitative evidence. The other 55 remain explicitly missing; their roles and all Element placements are intentional Phimond authoring, never claimed as recovered source behavior.', '- Element IDs: `fire`, `water`, `wind`, `earth`, `light`, `dark`. Ice themes use water and thunder themes use wind in this initial vocabulary. This is an explicit design simplification, not an APK fact. No automatic Race mapping, stat multiplier, STAB or element chart is supplied.', '- Primary describes dominant intended native function; optional Secondary describes a usable supporting function. JSON records both concrete thematic rationale and the P13 native-pool function contract. P13 must realize these roles through concrete skills or explicitly reopen the assignment. No skill is granted here.', '- Poison/burn damage alone does not justify Disruptor; assigned Disruptors require control/impairment beyond HP loss. Self-only recovery/resistance alone does not justify Support.', '- Budget/template version: accepted P11 Q10/Q11 main shares, 75/25 blend, main budgets 100/110/122/136/160, Special148/172, growth2% of main base target; approved SR/SPD factors. Exact intermediates are Decimal. Nearest integer base and nearest .001 growth use half-up authoring quantization, except Bird SPD uses floor-to-grid of the exact +5% upper bound; every constraint is checked. This is catalog-authoring quantization, not a change to gameplay floor rules.', '- V1.1 encodes the owner-approved Bird SPD priority inside Species base/growth: the highest representable value at or below 105% of the exact SPD target. Other Races retain the neutral rounded target. At the same Star/class, ordered role blend, level and SPD grade, Bird grown SPD is strictly higher. Different roles, inheritance, equipment and effects can change matchup order. This is an authoring rule, not a runtime Race multiplier. Other Race identities remain proposed in P11-race-identity-direction.md; broader catalog balance findings remain open.', '- Base and growth guards run separately; modifiers, exact templates and realized normalized main budgets are included per record. Roles do not constrain owned-Pet inherited totals.', '', '## Reproduce / validate', '', 'From repository root:', '', '```sh', 'rtk proxy python3 .ai/plan/phases/P11-stats/evidence/build_species_catalog.py --write', 'rtk proxy python3 .ai/plan/phases/P11-stats/evidence/build_species_catalog.py --check', '```', '', 'The builder writes only these design artifacts and static evidence. `--check` independently checks committed JSON constraints and exact deterministic reproduction, without writing. It is not a stat engine or gameplay simulation. Source file hashes bind this catalog to the frozen inputs.', '', '## Assignment ledger', '', 'P=physical_dps, M=magic_dps, T=tank, S=support, D=disruptor, H=hybrid. “Missing” means source description absent, not authoring incomplete. Full six-stat values and provenance are in `P11-species-catalog.json`.', '', '| ID | Name | Element | Primary / Secondary | Source prose | Phimond design rationale |','|---|---|---|---|---|---|']
    for key,r in catalog['records'].items():
        roles=r['primary_role']+(' / '+r['secondary_role'] if r['secondary_role'] else '')
        lines.append(f"| {key} | {r['name_vi']} | {r['element_id']} | {roles} | {'Present' if r['source_description_vi'] else 'Missing'} | {r['rationale']} |")
    lines+=['', '## Downstream acceptance', '', 'P13 owns the interaction chart, skill formulas/eligibility and actual native pools. P02/P07 own battle-mode viability testing; P15 owns pacing. Content activation and legacy14→152 mapping require a later additive implementation delivery with migration/rollback review. Passing this static catalog validator establishes only the approved numeric constraints and frozen-identity coverage.', '']
    return '\n'.join(lines)

def encoded(value):
    return json.dumps(value,ensure_ascii=False,indent=2)+'\n'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    expected=build()
    evidence=validate(expected)
    outputs={PHASE/'P11-species-catalog.json':encoded(expected),PHASE/'P11-species-catalog.md':markdown(expected),PHASE/'evidence/catalog-validation.json':encoded(evidence)}
    if args.write:
        for path,content in outputs.items(): path.write_text(content)
    else:
        validate(json.loads((PHASE/'P11-species-catalog.json').read_text()))
        for path,content in outputs.items(): assert path.read_text()==content,f'not reproducible: {path}'
    print('PASS: 152 frozen species; 304 independently validated stat layers; deterministic design catalog.')

if __name__=='__main__': main()
