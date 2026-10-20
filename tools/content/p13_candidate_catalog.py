"""Versioned P13 stats candidate; P10/P11 baseline files are never written."""
import copy
import json
import types
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASELINE=ROOT/'.ai/plan/phases/P11-stats/P11-species-catalog.json'
BUILDER=ROOT/'.ai/plan/phases/P11-stats/evidence/build_species_catalog.py'

def build(amendments, additions):
    b=types.ModuleType('p13_p11_candidate_builder');b.__file__=str(BUILDER)
    exec(compile(BUILDER.read_bytes(),str(BUILDER),'exec'),b.__dict__)
    baseline=json.loads(BASELINE.read_text())
    assert b.build()==baseline,'P11 canonical builder changed: reconcile before authoring'
    reverse={v:k for k,v in b.ROLES.items()}
    lines=[]
    for line in b.CHOICES.strip().splitlines():
        ordinal,element,primary,secondary,note=line.split(' ',4)
        sid=f'species_{int(ordinal):04d}'
        if sid in amendments:
            roles=amendments[sid];primary=reverse[roles[0]];secondary=reverse[roles[1]] if len(roles)>1 else '-'
            note='P13 owner review role amendment; candidate pending acceptance'
            if primary in 'PMH':b.ACCENTS[sid]={'P':'atk','M':'mag','H':'dual'}[primary]
        lines.append(' '.join([ordinal,element,primary,secondary,note]))
    b.CHOICES='\n'.join(lines)
    catalog=b.build();baseline_check=b.validate(catalog)
    for x in additions:
        sid=x['proposal_id'];roles=x.get('roles',[x.get('primary_role')]);primary=reverse[roles[0]]
        secondary=reverse[roles[1]] if len(roles)>1 else None
        source=dict(id=sid,race_id=x['race'],star=x['star'],species_class=x['species_class'])
        b.ACCENTS[sid]={'P':'atk','M':'mag','H':'dual','T':'def','S':'mag','D':'mag'}[primary]
        element={'Địa':'earth','Quang':'light','Hỏa':'fire','Âm':'dark'}[x['proposed_element']]
        rec=dict(id=sid,name_vi=x['working_name'],race_id=x['race'],star=x['star'],species_class=x['species_class'],element_id=element,primary_role=roles[0],secondary_role=roles[1] if len(roles)>1 else None,role_ids=roles,source_identity={'namespace':'phimond_p13_authored_proposal','proposal_id':sid,'apk_jar_source':False},source_description_vi='',source_description_status='new_authored_species_not_source_recovered',rationale=x['art_brief'],assignment_provenance='p13_candidate_not_runtime',approval_basis='owner_requested_eight_species_extension_P10_registration_pending',race_identity_brief_vi=b.RACE_BRIEF[x['race']],species_stat_accent=b.ACCENTS[sid],layers={},p13_native_pool_contract={'primary_function':b.ROLE_INTENT[primary],'secondary_function':b.ROLE_INTENT.get(secondary),'status':'authored_native_pool_candidate','race_function_direction':b.RACE_BRIEF[x['race']],'race_function_scope':'native pool only; no automatic Race passive'},art_status='P10_new_art_pending',registry_status='proposal_id_pending_P10_stable_id')
        for growth,name in [(False,'base_stats'),(True,'growth_baseline')]:
            target,exact=b.targets(source,primary,secondary,growth)
            values=b.authored_values(source,exact,growth,primary)
            rec[name]={k:b.number(v) for k,v in values.items()}
            rec['layers'][name]=dict(main_target=b.number(target),main_budget=b.number(values['hp']/10+sum(values[k] for k in ['atk','mag','def'])),exact_role_template={k:str(v) for k,v in exact.items()})
        catalog['records'][sid]=rec
    mp_factors=dict(physical_dps=b.D('1'),magic_dps=b.D('1.3'),tank=b.D('1'),hybrid=b.D('1.15'),support=b.D('1.3'),disruptor=b.D('1.15'))
    checked=0
    for sid,r in catalog['records'].items():
        if sid in amendments:
            r['assignment_provenance']='p13_owner_review_role_amendment_candidate'
            r['approval_basis']='candidate_pending_owner_acceptance_not_P11_promotion'
        r['p13_native_pool_contract']['status']='authored_native_pool_candidate'
        primary=reverse[r['primary_role']];secondary=reverse[r['secondary_role']] if r['secondary_role'] else None
        for growth,name in [(False,'base_stats'),(True,'growth_baseline')]:
            target,exact=b.targets(r,primary,secondary,growth);values={k:b.D(str(v)) for k,v in r[name].items()}
            budget=values['hp']/10+sum(values[k] for k in ['atk','mag','def'])
            assert abs(budget/target-1)<=b.D('.02' if r['species_class']=='special' else '.03'),sid
            assert set(values)==set(b.STATS)
            for k,v in values.items():
                assert v>0 and v==b.rounded(v,growth)
                assert abs(v/exact[k]-1)<=b.D('.05' if k in b.STATS[4:] else '.10'),(sid,k)
            if primary=='P':assert values['atk']>=b.D('.35')*budget and values['atk']>=b.D('1.25')*values['mag']
            if primary=='M':assert values['mag']>=b.D('.35')*budget and values['mag']>=b.D('1.25')*values['atk']
            if primary=='T':assert values['hp']/10+values['def']>=b.D('.60')*budget
            if primary=='H':assert min(values['atk'],values['mag'])>=b.D('.20')*budget and values['atk']+values['mag']>=b.D('.50')*budget
            checked+=1
        factor=mp_factors[r['primary_role']]
        if r['secondary_role']:factor=factor*b.D('.75')+mp_factors[r['secondary_role']]*b.D('.25')
        star_factor=b.D(str({4:1.48,5:1.72}[r['star']])) if r['species_class']=='special' else b.D(str([1,1.1,1.22,1.36,1.6][r['star']-1]))
        r['mp_profile']=dict(base=b.number(b.rounded(50*star_factor*factor,False)),growth=b.number(b.rounded(b.D('.5')*star_factor*factor,True)),rule='base + floor(growth*(level-1)); P11 F04, no inheritance or automatic refill')
        if sid in baseline['records']:
            for key in ['id','name_vi','race_id','star','species_class','element_id','source_identity','source_description_vi']:
                assert r[key]==baseline['records'][sid][key],(sid,key)
    assert len(catalog['records'])==160 and checked==320
    catalog.update(catalog_version='P13-v7-owner-review-160',authority='candidate_pending_owner_acceptance_not_P11_promotion',validation=dict(status='PASS',species_records=160,layers_checked=checked,preserved_source_records=152,new_authored_records=8,p11_existing_layers=baseline_check['layers_checked']))
    return copy.deepcopy(catalog)
