"""Executable design checks; no gameplay runtime is activated."""
import unittest
from fractions import Fraction
import json
import p13_design as d


class DesignTests(unittest.TestCase):
    def test_damage_examples_and_rounding(self):
        self.assertEqual(d.damage(100, 50, Fraction(6, 5), Fraction(5, 4)), 100)
        self.assertEqual(d.damage(100, 50, Fraction(6, 5), Fraction(4, 5)), 64)
        self.assertEqual(d.damage(0, 50, Fraction(1), Fraction(1)), 0)
        self.assertEqual(d.damage(1, 9999, Fraction(1), Fraction(1)), 1)

    def test_status_resistance_and_zero_chance(self):
        self.assertEqual(d.status_chance(Fraction(3, 4), 100), Fraction(9, 20))
        self.assertEqual(d.status_chance(Fraction(0), 100), 0)
        self.assertGreater(d.status_chance(Fraction(1), 1000000), Fraction(1, 5))

    def test_inheritance_uses_only_learned_and_eligibility(self):
        skills = {'a': {'inheritance': ['bird', 'beast']}, 'b': {'inheritance': []}}
        self.assertEqual(d.inherited_pool(['a', 'b'], ['a'], 'beast', skills), ['a'])
        self.assertEqual(d.inherited_pool(['a'], [], 'plant', skills), [])

    def test_catalog_contract_and_duplicate_stat_kit_difference(self):
        package = d.build_package()
        errors = d.validate(package)
        self.assertEqual(errors, [])
        self.assertEqual(len(package['species']), 152)
        s = {r['id']: r for r in package['species']}
        self.assertNotEqual(s['species_0009']['native_skills'], s['species_0011']['native_skills'])
        self.assertNotEqual(s['species_0070']['native_skills'], s['species_0074']['native_skills'])

    def test_validator_detects_missing_pool_reference(self):
        p = d.build_package()
        p['species'][0]['native_skills'].append('missing_skill')
        self.assertTrue(any('missing_skill' in e for e in d.validate(p)))

    def test_validator_detects_role_gap(self):
        p = d.build_package()
        next(s for s in p['species'] if s['roles'] == ['support'])['native_skills'] = ['strike']
        self.assertTrue(any('support' in e for e in d.validate(p)))

    def test_all_60_source_records_have_explicit_candidate_mapping(self):
        p = d.build_package()
        source = json.loads((d.PHASE / 'evidence/apk84-skills.json').read_text())
        expected = {r['id'] for r in source['rows']}
        mapped = {sid for s in p['skills'] for sid in s['source_ids']}
        self.assertEqual(mapped, expected)

    def test_special_signature_is_species_exclusive_and_not_inherited(self):
        p = d.build_package()
        signatures = [s for s in p['skills'] if s.get('exclusive_species')]
        self.assertEqual(len(signatures), 7)
        self.assertEqual({s['element'] for s in signatures}, {e for e, _, _ in d.ELEMENTS})
        by = {s['id']: s for s in p['species']}
        for skill in signatures:
            owner = by[skill['exclusive_species']]
            self.assertEqual(owner['class'], 'special')
            self.assertEqual(owner['element'], skill['element'])
            self.assertIn(owner['star'], (4, 5))
            self.assertEqual(skill['inheritance'], [])
            self.assertEqual(skill['rank_policy'], 'fixed_rank_1')
            self.assertEqual([s['id'] for s in p['species'] if skill['id'] in s['native_skills']], [owner['id']])
            self.assertIn(skill['id'], owner['sample_build'])
            self.assertLessEqual(len(owner['sample_build']), 6)
            self.assertEqual(d.inherited_pool([skill['id']], [], owner['race'], {skill['id']: skill}), [])

    def test_validator_rejects_signature_in_another_species_pool(self):
        p = d.build_package()
        sig = next(s for s in p['skills'] if s.get('exclusive_species'))
        p['species'][0]['native_skills'].append(sig['id'])
        self.assertTrue(any('exclusive' in e for e in d.validate(p)))

    def test_apk_aoe_tiers_remain_separate_and_light_is_cheaper(self):
        p=d.build_package(); by={s['id']:s for s in p['skills']}
        for base in ['sweep']+['wave_'+e for e,_,_ in d.ELEMENTS]:
            ids=[base+'_light',base,base+'_advanced',base+'_super']
            rows=[by[x] for x in ids]
            self.assertEqual([s['tier_index'] for s in rows],[1,2,3,4])
            self.assertEqual(len({s['source_ids'][0] for s in rows}),4)
            self.assertTrue(all(s['target']=='enemy_all' and s['rank_policy']=='fixed_rank_1' for s in rows))
            self.assertTrue(all(rows[i]['mp']<rows[i+1]['mp'] and Fraction(rows[i]['power'])<Fraction(rows[i+1]['power']) for i in range(3)))
            # MAG/ATK100, DEF50, neutral, three hit enemies; light retains MP efficiency.
            for row in rows:
                self.assertGreater(d.damage(100,50,Fraction(row['power'])),0)
            for pet in p['species']:
                if base in pet['native_skills']:
                    self.assertTrue(set(ids)<=set(pet['native_skills']))

    def test_each_race_has_real_physical_and_magic_species_and_usable_damage(self):
        p=d.build_package();by={s['id']:s for s in p['skills']}
        for race in d.RACES:
            rows=[s for s in p['species'] if s['race']==race]
            for role,kind in [('physical_dps','physical'),('magic_dps','magic')]:
                candidates=[s for s in rows if s['roles'][0]==role]
                self.assertGreaterEqual(len(candidates),2,race+' '+role)
                for pet in candidates:
                    usable=[by[s] for s in pet['native_skills'] if by[s]['kind']==kind]
                    self.assertTrue(any(s['target']=='enemy_one' for s in usable))
                    self.assertTrue(any(s['target']=='enemy_all' and s.get('tier_index')==1 for s in usable))

    def test_validator_rejects_race_without_primary_casters(self):
        p=d.build_package()
        p['species']=[s for s in p['species'] if not(s['race']=='beast' and s['roles'][0]=='magic_dps')]
        self.assertTrue(any('race damage coverage' in e for e in d.validate(p)))

    def test_light_tier_farm_saves_mp_at_same_kills(self):
        p=d.build_package();by={s['id']:s for s in p['skills']}
        light,strong=by['sweep_light'],by['sweep_super']
        self.assertGreaterEqual(d.damage(100,50,Fraction(light['power'])),25)
        self.assertGreaterEqual(d.damage(100,50,Fraction(strong['power'])),25)
        self.assertEqual(50//light['mp'],5)
        self.assertEqual(50//strong['mp'],1)
        self.assertEqual(light['cooldown'],0)

    def test_target_and_effect_taxonomy(self):
        by={s['id']:s for s in d.build_package()['skills']}
        for sid,shape,mode in [('strike','single','damage_only'),('sweep_light','aoe','damage_only'),('burn','single','damage_with_effect'),('sleep','single','effect_only'),('group_heal','aoe','effect_only'),('attack_up','aoe','effect_only')]:
            self.assertEqual(by[sid]['target_shape'],shape)
            self.assertEqual(by[sid]['damage_mode'],mode)

    def test_inheriting_one_current_tier_does_not_grant_family(self):
        by={s['id']:s for s in d.build_package()['skills']}
        self.assertEqual(d.inherited_pool(['sweep_light'],['sweep_light'],'bird',by),['sweep_light'])
        self.assertEqual(d.inherited_pool(['sweep_light'],['sweep_super'],'bird',by),['sweep_light','sweep_super'])


if __name__ == '__main__':
    unittest.main()
