import json
import unittest
from pathlib import Path
from unittest.mock import patch
import p13_roster_review as r

# P13 packages are frozen with the names at review time; display names were renamed to
# Han-Viet style afterwards (P10-species-naming-hanviet.json).
RENAMES={x['id']:x['name_vi'] for x in json.loads((Path(__file__).resolve().parents[2]/'.ai/plan/phases/P10-pet-model/P10-species-naming-hanviet.json').read_text())['records']}

class RosterReviewTests(unittest.TestCase):
    def test_groups_do_not_mix_class_or_star(self):
        p,old=r.build()
        byid={s['id']:s for s in old['species']}
        totals=dict(normal4=0,normal5=0,special4=0,special5=0)
        for g in p['roster_review']['groups']:
            for key in totals:
                totals[key]+=len(g[key])
                for s in g[key]:
                    if s.get('is_new'):
                        self.assertEqual(int(key[-1]),5)
                        self.assertIn(s['id'],r.STABLE.values())
                        continue
                    self.assertEqual(byid[s['id']]['class'],key[:-1])
                    self.assertEqual(byid[s['id']]['star'],int(key[-1]))
        self.assertEqual(totals,dict(normal4=17,normal5=20,special4=4,special5=15))

    def test_source_recipes_preserve_order_and_both_reverse_results(self):
        p,_=r.build();x=p['roster_review']
        self.assertEqual(len(x['recipes']),17)
        self.assertEqual(len(x['reversed_pairs']),3)
        self.assertTrue(all(not v['enabled'] for v in x['recipes']))

    def test_candidate_catalog_expands_without_rewriting_source_identity(self):
        p,old=r.build()
        original={s['id']:s for s in old['species']};candidate={s['id']:s for s in p['species']}
        self.assertEqual(len(candidate),160)
        for sid,before in original.items():
            for key in ['id','name','race','star','class','element','source_identity']:
                expected=RENAMES[sid] if key=='name' else before[key]
                self.assertEqual(expected,candidate[sid][key])
        self.assertEqual(p['candidate_catalog_meta']['validation']['layers_checked'],320)
        self.assertEqual(len(p['skills']),97)
        self.assertEqual(len(p['roster_review']['proposed_species']),6)
        self.assertEqual(len(p['roster_review']['proposed_special_species']),2)
        self.assertEqual(p['roster_review']['proposed_total'],160)
        self.assertEqual(p['roster_review']['star6_status'],'not_in_current_model_owner_confirmed')
        self.assertEqual(p['roster_review']['fusion_star_rule'],'normal5_plus_normal5_to_special5')

    def test_proposed_normal5_covers_both_primary_channels_without_special(self):
        p,_=r.build();review=p['roster_review']
        for g in review['groups']:
            roles={s['proposed_roles'][0] for s in g['normal5']}
            roles.update(s['primary_role'] for s in review['proposed_species'] if s['race']==g['race'])
            self.assertTrue({'physical_dps','magic_dps'} <= roles,g['name'])

    def test_normal4_covers_both_primary_channels_and_has_no_dead_end(self):
        p,_=r.build();review=p['roster_review']
        for g in review['groups']:
            self.assertTrue({'physical_dps','magic_dps'} <= {s['proposed_roles'][0] for s in g['normal4']},g['name'])
        self.assertEqual(review['fusion_review']['normal4_without_proposed_recipe'],[])

    def test_caster_recipe_does_not_require_a_physical_parent(self):
        p,_=r.build();recipes=p['roster_review']['fusion_review']['recipes']
        empress=next(x for x in recipes if x['target_id']=='species_0019')
        self.assertEqual([x['id'] for x in empress['parents']],['species_0018',r.STABLE['P13-NEW-05']])
        for x in recipes:
            if x['channel']=='magic':
                self.assertTrue(all('magic_dps' in y['roles'] and 'physical_dps' not in y['roles'] for y in x['parents']),x['target'])

    def test_candidate_has_unique_pairs_and_all_six_new_species_have_a_path(self):
        p,_=r.build();f=p['roster_review']['fusion_review'];rows=f['recipes']
        self.assertEqual(len(rows),28)
        self.assertEqual(len({tuple(sorted(y['id'] for y in x['parents'])) for x in rows}),28)
        self.assertTrue(all(x['status']=='authored_proposal_not_enabled' for x in rows))
        used={y['id'] for x in rows for y in x['parents']}
        self.assertTrue({r.STABLE[s['proposal_id']] for s in p['roster_review']['proposed_species']} <= used)
        self.assertEqual(f['normal5_without_proposed_recipe'],[])

    def test_hybrid5_parents_reach_special_hybrid5(self):
        p,_=r.build();rows=p['roster_review']['fusion_review']['recipes']
        hybrid5=[x for x in rows if x['parent_star']==5 and x['channel']=='hybrid']
        self.assertEqual(len(hybrid5),2)
        self.assertEqual({y['id'] for x in hybrid5 for y in x['parents']},{'species_0052','species_0069','species_0140'})
        self.assertTrue(all(x['target_roles'][0]=='hybrid' for x in hybrid5))
        skills={s['id']:s for s in p['skills']}
        for new in p['roster_review']['proposed_special_species']:
            kit=new['sample_build'];self.assertEqual(len(set(kit)),6)
            self.assertTrue({'physical','magic'} <= {skills[s]['kind'] for s in kit})
            self.assertIn('sweep_light',kit)
            self.assertTrue(any(s.startswith('wave_') and s.endswith('_light') for s in kit))

    def test_recipe_identity_star_class_and_race_alignment(self):
        p,_=r.build();rows=p['roster_review']['fusion_review']['recipes']
        for x in rows:
            self.assertEqual({y['star'] for y in x['parents']},{x['parent_star']})
            self.assertTrue(all(y['species_class']=='normal' for y in x['parents']))
            self.assertIn(x['target_race'],{y['race'] for y in x['parents']})
        self.assertEqual(sum(x['parent_star']==4 for x in rows),13)
        self.assertEqual(sum(x['parent_star']==5 for x in rows),15)
        self.assertEqual(len({x['target_id'] for x in rows}),19)

    def test_wrong_channel_and_duplicate_pair_are_rejected(self):
        wrong=list(r.FUSION_PROPOSALS)
        wrong[0]=('recipe_special_0001','species_0018','species_0038','magic','invalid caster + physical')
        with patch.object(r,'FUSION_PROPOSALS',wrong):
            with self.assertRaises(AssertionError):r.build()

    def test_new_signatures_are_exclusive_non_inheritable_and_use_one_slot(self):
        p,_=r.build();skills={s['id']:s for s in p['skills']}
        for new in p['roster_review']['proposed_special_species']:
            signature=skills[new['signature_skill_id']]
            self.assertEqual(signature['exclusive_species'],r.STABLE[new['proposal_id']])
            self.assertEqual(signature['inheritance'],[])
            self.assertEqual(signature['rank_policy'],'fixed_rank_1')
            self.assertEqual((signature['mp'],signature['cooldown'],signature['learn_level']),(28,3,40))
            owners=[s for s in p['species'] if signature['id'] in s['native_skills']]
            self.assertEqual([s['id'] for s in owners],[r.STABLE[new['proposal_id']]])
            self.assertIn(signature['id'],owners[0]['sample_build'])
            self.assertEqual(len(owners[0]['sample_build']),6)

    def test_role_changes_recompute_stats_growth_mp_and_native_pool(self):
        p,old=r.build();current={s['id']:s for s in p['species']};base={s['id']:s for s in old['species']}
        for sid in ['species_0035','species_0148']:
            row=current[sid]
            self.assertEqual(row['roles'][0],'magic_dps')
            for layer in ['base_stats','growth_baseline']:self.assertGreater(row[layer]['mag'],row[layer]['atk'])
            self.assertIn('wave_'+row['element']+'_light',row['native_skills'])
            self.assertNotEqual(row['base_stats'],base[sid]['base_stats'])
        self.assertEqual(current[r.STABLE['P13-SPECIAL-01']]['mp_profile']['base'],102)
        self.assertEqual(current[r.STABLE['P13-SPECIAL-02']]['mp_profile']['base'],99)

    def test_stat_authoring_never_writes_p11_baseline(self):
        before=r.candidate_stats.BASELINE.read_bytes();r.build()
        self.assertEqual(before,r.candidate_stats.BASELINE.read_bytes())
        duplicate=list(r.FUSION_PROPOSALS)
        duplicate[1]=('recipe_special_0002','P13-NEW-05','species_0018','physical','reversed pair duplicated')
        with patch.object(r,'FUSION_PROPOSALS',duplicate):
            with self.assertRaises(AssertionError):r.build()

    def test_p10_stable_ids_replace_proposal_ids_as_identifiers(self):
        import re
        p,_=r.build()
        ids=[s['id'] for s in p['species']]
        self.assertEqual(len(set(ids)),160)
        self.assertTrue(all(re.fullmatch(r'species_\d{4}',i) for i in ids))
        self.assertEqual(sorted(i for i in ids if i>='species_0153'),sorted(r.STABLE.values()))
        by={s['id']:s for s in p['species']}
        for proposal,stable in r.STABLE.items():
            self.assertEqual(by[stable]['proposal_id'],proposal)
        for rec in p['roster_review']['fusion_review']['recipes']:
            for ref in [rec['target_id']]+[y['id'] for y in rec['parents']]:
                self.assertIn(ref,by)
        skills={s['id']:s for s in p['skills']}
        self.assertEqual(skills['dual_seal_light']['exclusive_species'],'species_0159')
        self.assertEqual(skills['inverse_seal_dark']['exclusive_species'],'species_0160')
        for g in p['roster_review']['groups']:
            for key in ['normal4','normal5','special4','special5']:
                for x in g[key]:
                    self.assertIn(x['id'],by)

if __name__=='__main__':unittest.main()
