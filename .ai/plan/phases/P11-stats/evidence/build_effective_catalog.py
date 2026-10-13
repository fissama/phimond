#!/usr/bin/env python3
"""Reconcile the effective 160-species design without modifying frozen P10/P11 inputs."""
import argparse
import copy
from collections import Counter
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
PHASE = Path(__file__).resolve().parents[1]
MANIFEST = PHASE / 'evidence/roster-amendment-160.json'
BASELINE = PHASE / 'P11-species-catalog.json'
spec = importlib.util.spec_from_file_location('p11_snapshot_builder', PHASE / 'evidence/build_species_catalog.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
INITIAL_ACCENTS = dict(b.ACCENTS)
REVERSE = {v:k for k,v in b.ROLES.items()}
MP_FACTORS = dict(P='1', M='1.3', T='1', H='1.15', S='1.3', D='1.15')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def numeric_hash(catalog, fields):
    rows = [{f:r[f] for f in fields} for _,r in sorted(catalog['records'].items())]
    return hashlib.sha256(json.dumps(rows, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()

def author(record):
    primary = REVERSE[record['primary_role']]
    secondary = REVERSE[record['secondary_role']] if record['secondary_role'] else None
    for growth,name in [(False,'base_stats'),(True,'growth_baseline')]:
        target,template = b.targets(record,primary,secondary,growth)
        values = b.authored_values(record,template,growth,primary)
        record[name] = {k:b.number(v) for k,v in values.items()}
        record['layers'][name] = {
            'main_target':b.number(target),
            'main_budget':b.number(values['hp']/10+sum(values[k] for k in ('atk','mag','def'))),
            'exact_role_template':{k:str(v) for k,v in template.items()},
            'relative_modifiers':{k:str(values[k]/template[k]-1) for k in b.STATS},
            'main_tolerance':'.02' if record['species_class']=='special' else '.03',
        }

def describe(record):
    primary = REVERSE[record['primary_role']]
    secondary = REVERSE[record['secondary_role']] if record['secondary_role'] else None
    record['race_identity_brief_vi'] = b.RACE_BRIEF[record['race_id']]
    record['gameplay_description_vi'] = 'Thiên về '+b.ROLE_VI[primary]+(' với chức năng phụ '+b.ROLE_VI[secondary] if secondary else '')+'. '+record['race_identity_brief_vi']+' Điểm nhấn riêng: '+{'hp':'HP','atk':'ATK','mag':'MAG','def':'DEF','dual':'ATK và MAG'}[record['species_stat_accent']]+'.'
    record['p13_native_pool_contract'] = {
        'primary_function':b.ROLE_INTENT[primary], 'secondary_function':b.ROLE_INTENT.get(secondary),
        'race_function_direction':record['race_identity_brief_vi'],
        'race_function_scope':'intended native pool only; no automatic Race skill or passive',
        'status':'P13 candidate kit requires phase acceptance and later runtime implementation',
    }
    factor = b.D(MP_FACTORS[primary])
    if secondary:
        factor = factor*b.D('.75')+b.D(MP_FACTORS[secondary])*b.D('.25')
    star_factor = b.D({4:'1.48',5:'1.72'}[record['star']]) if record['species_class']=='special' else b.D(['1','1.1','1.22','1.36','1.6'][record['star']-1])
    record['mp_profile'] = {
        'base':b.number(b.rounded(50*star_factor*factor,False)),
        'growth':b.number(b.rounded(b.D('.5')*star_factor*factor,True)),
        'rule':'base + floor(growth*(level-1)); P11 F04, no inheritance or automatic refill',
    }

def build():
    b.ACCENTS = dict(INITIAL_ACCENTS)
    m = json.loads(MANIFEST.read_text())
    assert sha(BASELINE)==m['baseline_catalog_sha256'],'Frozen v2 input changed; explicit reconciliation required'
    baseline = json.loads(BASELINE.read_text())
    assert b.build()==baseline
    b.validate(baseline)
    catalog = copy.deepcopy(baseline)
    for change in m['role_amendments']:
        r = catalog['records'][change['id']]
        r['primary_role'] = change['roles'][0]
        r['secondary_role'] = change['roles'][1] if len(change['roles'])>1 else None
        r['role_ids'] = change['roles']
        r['species_stat_accent'] = change['accent']
        b.ACCENTS[r['id']] = change['accent']
        r['rationale'] = 'Owner-directed 4/5-star development reconciliation; '+r['primary_role']+(' / '+r['secondary_role'] if r['secondary_role'] else '')
        r['assignment_provenance'] = 'phimond_authored_P11_v3_role_amendment_not_APK_fact'
        r['approval_basis'] = m['authorization']
        author(r)
    for item in m['additions']:
        stable_id = m['proposal_to_stable'][item['id']]
        assert stable_id not in catalog['records']
        r = copy.deepcopy(item)
        r['proposal_id'] = r['id']
        r['id'] = stable_id
        r.update(primary_role=r['role_ids'][0], secondary_role=r['role_ids'][1] if len(r['role_ids'])>1 else None,
                 source_description_vi='',source_description_status='new_authored_species_not_source_recovered',
                 registry_status='P10_authored_allocation_pinned_at_reconciliation',art_status='P10_new_art_pending_owner_review',
                 approval_basis=m['authorization'],assignment_provenance='Phimond-authored P11 effective design; not APK source identity',
                 element_provenance='P13 expansion thematic Element, reconciled under owner P11 request',
                 numeric_provenance='P11 unchanged templates/budgets and Race authoring; no runtime Race multiplier',layers={})
        b.ACCENTS[r['id']] = r['species_stat_accent']
        author(r)
        catalog['records'][r['id']] = r
    for r in catalog['records'].values():
        describe(r)
    catalog.update(catalog_version=m['version'],status='effective_design_only_not_runtime',
                   authority=m['authorization'],snapshot_catalog='P11-species-catalog.json (152-source v2 snapshot)',
                   input_candidate_sha256=m['input_catalog_sha256'],registry_status='160 stable IDs; 152 source + 8 authored allocations',
                   proposal_to_stable=m['proposal_to_stable'],registry_mapping_source=m['mapping_source_path'],
                   registry_full_sha256_at_reconciliation=m['registry_full_sha256'])
    assert numeric_hash(catalog,m['numeric_projection_fields'])==m['expected_numeric_projection_sha256'],'P13 v7 numeric parity failed'
    return catalog

def validate(catalog):
    m = json.loads(MANIFEST.read_text())
    baseline = json.loads(BASELINE.read_text())['records']
    records = catalog['records']
    new_ids = set(m['proposal_to_stable'].values())
    assert len(new_ids)==8 and len(m['proposal_to_stable'])==8
    registry=json.loads(b.REGISTRY.read_text())
    # Design reproduction uses the pinned P10 allocation checkpoint. A checkout
    # with only the historical source namespace can reproduce the design, but
    # this is never evidence that the live registry/migration is enabled.
    if 'authored_species' in registry:
        assert registry['authored_species']==m['proposal_to_stable'],'P10 allocation drift'
    assert len(records)==160 and set(records)==set(baseline)|new_ids
    assert Counter(r['species_class'] for r in records.values())=={'normal':141,'special':19}
    assert len(m['role_amendments'])==14 and len(new_ids)==8
    assert Counter(r['star'] for r in records.values() if r['species_class']=='special')=={4:4,5:15}
    layers = 0
    coverage = {}
    for key,r in records.items():
        assert r['id']==key and len(r['role_ids']) in (1,2)
        assert r['role_ids']==[v for v in (r['primary_role'],r['secondary_role']) if v]
        assert r['primary_role']!=r['secondary_role'] and r['element_id'] in b.ELEMENTS.values()
        assert r['race_identity_brief_vi']==b.RACE_BRIEF[r['race_id']] and 'nhất' not in r['gameplay_description_vi']
        if key in baseline:
            for field in ('id','name_vi','race_id','star','species_class','element_id','source_identity','source_description_vi'):
                assert r[field]==baseline[key][field],(key,field,'frozen identity')
        else:
            assert key in new_ids and r['registry_status']=='P10_authored_allocation_pinned_at_reconciliation'
            assert m['proposal_to_stable'][r['proposal_id']]==key
            assert r['source_identity']['apk_jar_source'] is False
        primary = REVERSE[r['primary_role']]
        secondary = REVERSE[r['secondary_role']] if r['secondary_role'] else None
        for growth,name in [(False,'base_stats'),(True,'growth_baseline')]:
            target,template = b.targets(r,primary,secondary,growth)
            values = {k:b.D(str(v)) for k,v in r[name].items()}
            assert set(values)==set(b.STATS)
            budget = values['hp']/10+sum(values[k] for k in ('atk','mag','def'))
            assert abs(budget/target-1)<=b.D('.02' if r['species_class']=='special' else '.03'),(key,name,'budget')
            assert b.D(str(r['layers'][name]['main_budget']))==budget
            for k,v in values.items():
                assert v>0 and v==b.rounded(v,growth)
                assert abs(v/template[k]-1)<=b.D('.05' if k in b.STATS[4:] else '.10'),(key,name,k,'band')
            if primary=='P': assert values['atk']>=b.D('.35')*budget and values['atk']>=b.D('1.25')*values['mag']
            if primary=='M': assert values['mag']>=b.D('.35')*budget and values['mag']>=b.D('1.25')*values['atk']
            if primary=='T': assert values['hp']/10+values['def']>=b.D('.60')*budget
            if primary=='H': assert min(values['atk'],values['mag'])>=b.D('.20')*budget and values['atk']+values['mag']>=b.D('.50')*budget
            # Assert embedded Race emphases survived role changes.
            stat={'beast':'hp','dragon':'def','undead':'status_resistance'}.get(r['race_id'])
            if stat: assert values[stat]>template[stat],(key,name,'Race emphasis')
            if r['race_id']=='spirit' and primary in 'MHSD': assert values['mag']>template['mag']
            if r['race_id']=='demon':
                damage=('atk','mag') if primary=='H' else ('mag' if primary in 'MSD' else 'atk',)
                assert all(values[k]>template[k] for k in damage)
            layers += 1
    for star in (4,5):
        coverage[str(star)] = {}
        for race in b.RACE_VI:
            subset=[r for r in records.values() if r['race_id']==race and r['star']==star and r['species_class']=='normal']
            channels={role:[r['id'] for r in subset if r['primary_role']==role] for role in ('physical_dps','magic_dps')}
            assert all(channels.values()),(race,star,'primary channel coverage')
            coverage[str(star)][race]=channels
    assert numeric_hash(catalog,m['numeric_projection_fields'])==m['expected_numeric_projection_sha256']
    vectors=Counter(tuple(r[name][stat] for name in ('base_stats','growth_baseline') for stat in b.STATS) for r in records.values())
    return {'status':'PASS','scope':'static design only; not combat/recipe/runtime certification',
            'species_records':160,'layers_checked':layers,'normal':141,'special':19,'special4':4,'special5':15,
            'stable_source_ids':152,'stable_authored_ids':8,'role_amendments':14,
            'bird_spd_priority':b.validate_bird_priority(records),'normal_channel_coverage':coverage,
            'numeric_parity':'P13 v7 pinned numeric projection including MP',
            'distinct_numeric_vectors':len(vectors),'species_in_shared_vectors':sum(n for n in vectors.values() if n>1),
            'elements':dict(Counter(r['element_id'] for r in records.values()))}

def markdown(catalog,report):
    lines=['# P11 — Effective 160-Species catalog v3','',
           'Current design authority, 2026-10-13. 141 Normal + 19 Special. No runtime activation.',
           '152 source IDs preserved; eight authored IDs species_0153–species_0160 allocated by P10. New art awaits owner review. Proposal aliases remain for P13 reference migration. The adjacent 152 JSON/Markdown remains the reproducible historical v2 input, not the current full roster.','',
           'Formulas/budgets/grades/Race directions are unchanged. Fourteen role amendments regenerate base/growth/MP; numeric projection matches pinned P13 v7. No parent stats are averaged into Species templates.',
           'Pure DoT does not make Disruptor; Hybrid keeps two separate damage channels without adding turns. P13 owns kits and P16/P20 recipes.', '',
           'Order: HP / ATK / MAG / DEF / SPD / SR. MP uses a separate base / growth pair.', '',
           '| ID / Name | Race / Star / Class | Primary / Secondary | Base | Growth | MP |',
           '|---|---|---|---|---|---|']
    for k,r in catalog['records'].items():
        base=' / '.join(str(r['base_stats'][s]) for s in b.STATS)
        growth=' / '.join(str(r['growth_baseline'][s]) for s in b.STATS)
        roles=' / '.join(r['role_ids']);mp=r['mp_profile']
        lines.append(f"| {k} — {r['name_vi']} | {b.RACE_VI[r['race_id']]} / {r['star']} / {r['species_class']} | {roles} | {base} | {growth} | {mp['base']} / {mp['growth']} |")
    lines+=['', '## Checks and limits', '',
            f"320 layers valid; {report['distinct_numeric_vectors']} distinct vectors; {report['species_in_shared_vectors']} Species in shared-vector groups. Every Race has primary Physical and Magic Normal choices at both 4★ and 5★. Bird priority is checked against current ordered role cohorts, including new Species.",
            'All descriptions/provenance are in JSON. Numeric equality does not prove kit equality or measured balance. P13/P16 references must consume the explicit proposal-to-stable mapping before runtime activation.', '',
            '```sh', 'rtk proxy python3 .ai/plan/phases/P11-stats/evidence/build_effective_catalog.py --check', '```', '']
    return '\n'.join(lines)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');parser.add_argument('--check',action='store_true');args=parser.parse_args()
    catalog=build();report=validate(catalog)
    outputs={PHASE/'P11-species-catalog-160.json':b.encoded(catalog),PHASE/'P11-species-catalog-160.md':markdown(catalog,report),PHASE/'evidence/catalog-validation-160.json':b.encoded(report)}
    if args.write:
        for path,value in outputs.items():path.write_text(value)
    else:
        validate(json.loads((PHASE/'P11-species-catalog-160.json').read_text()))
        for path,value in outputs.items():assert path.read_text()==value,f'not reproducible: {path}'
    print('PASS: effective 160 species; 320 stat layers; 8-race Normal4/5 channel coverage; Bird priority; P13 v7 numeric/MP parity')

if __name__=='__main__':main()
