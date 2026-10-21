"""Read-only artwork audit; writes new160-art approval inventory/evidence, never runtime."""
from pathlib import Path
import json,hashlib,importlib.util
ROOT=Path(__file__).resolve().parents[6];OUT=Path(__file__).resolve().parent;PLAN=OUT.parents[1];REMEDY=PLAN/'size-audit-20261019/remedy-20261020'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
old=read(PLAN/'redraw-kit/owner-atlas-selection.json');ext=read(PLAN/'extension-20261013/art-manifest.json');base=read(ROOT/'data/p10/species.json')['records'];auth=read(ROOT/'data/p10/species_authored.json')['records'];profiles={r['id']:r for r in read(REMEDY/'scale-trials/proposals.json')['records']};redo=read(REMEDY/'species_0147/art-redo-20261021/profile.json');progress={r['id']:r for r in read(REMEDY/'progress.json')['records']}
assert len(old['species'])==152 and len(ext['records'])==8
assert all(r['status']=='owner_approved_done' for r in old['species'].values())
assert all(r['owner_approved'] and r['human_approved'] for r in ext['records'].values())
owner=read(REMEDY/'owner-review-20261021.json');assert len(owner['records'])==56 and all(r['owner_art_approved'] and r['owner_size_approved'] for r in owner['records'])
mapping=read(PLAN/'extension-20261013/mapping.json')['proposal_to_stable'];assert set(mapping.values())==set(ext['records'])
spec=importlib.util.spec_from_file_location('checker',ROOT/'tools/assets/check_p10_atlas.py');checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
selected={};mechanical=[];integrity=[]
for sid in [f'species_{i:04d}' for i in range(1,161)]:
 origin=old['species'][sid] if sid in old['species'] else ext['records'][sid];path=origin['candidate_path'];expected=origin.get('sha256',origin.get('candidate_sha256'))
 if sid in ('species_0138','species_0141','species_0147'):
  path=progress[sid]['candidate'];expected=read(ROOT/Path(path).parent/'metadata.json')['candidate_sha256']
 assert sha(ROOT/path)==expected,(sid,'hash')
 check=checker.check(ROOT/path);assert check['status']=='pass',(sid,check['issues']);check['path']=path;mechanical.append(check)
 model=(base|auth)[sid];record={'candidate_path':path,'sha256':expected,'name':model['display_name']['vi'],'status':'owner_approved_done','approval_source':'owner_chat_confirmation_20261021' if sid in profiles or sid not in old['species'] else origin.get('approval_source','owner_web_review'),'completed_at':'2026-10-21','identity_provenance':'Phimond-authored' if sid in auth else 'APK84_identity_redrawn_art','runtime_activated':False}
 if sid in profiles:
  pr=profiles[sid];record['display_preview']={'status':'owner_approved_preview_not_runtime','profile_path':str((REMEDY/'scale-trials/proposals.json').relative_to(ROOT)),'profile_sha256':sha(REMEDY/'scale-trials/proposals.json'),'species_id':sid,'factor':pr['factor']}
 if sid=='species_0147':
  record['display_preview']={'status':'owner_approved_registered_preview_not_runtime','profile_path':str((REMEDY/'species_0147/art-redo-20261021/profile.json').relative_to(ROOT)),'profile_sha256':sha(REMEDY/'species_0147/art-redo-20261021/profile.json'),'factor':redo['profiles'][1]['factor'],'manual_frame_origins_required':True,'native_idle_height':140.25,'approved_display_target_idle_height':190,'note':'Standalone PNG is not registration/density equivalent to prior170px art. Future renderer must honor contact origins or re-review new packing.'}
 selected[sid]=record
for r in owner['records']:
 assert selected[r['id']]['candidate_path']==r['source_path'] and selected[r['id']]['sha256']==r['sha256'],(r['id'],'owner binding')
# Verify original304 portrait/sprite PNGs against pinned-source audit, preserve historical selected152bytes too.
for r in read(PLAN/'redraw-kit/source-audit-20261005.json')['assets']:
 assert sha(ROOT/r['path'])==r['expected_sha256'],r['path'];integrity.append({'path':r['path'],'sha256':r['expected_sha256'],'matches':True})
assert len(integrity)==304
for r in read(REMEDY/'preservation.json')['records']:assert sha(ROOT/r['path'])==r['sha256']
manifest={'schema_version':2,'scope':'160 owner-approved redraw art; runtime integration excluded','status':'owner_approved_done','total':160,'completed':160,'completed_at':'2026-10-21','runtime_activated':False,'historical_baseline_selection':'redraw-kit/owner-atlas-selection.json','approval_basis':'Owner chat: Okie hết rồi, review1vòng nếu k có gì bất ổn đóng phase redraw160species. Includes0147 registered preview, not a standalone registration-ready PNG.','species':selected}
(OUT/'done.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));(OUT/'mechanical.json').write_text(json.dumps({'passed':160,'failed':0,'atlases':mechanical},indent=2));(OUT/'source-integrity.json').write_text(json.dumps({'original_pngs_preserved':304,'baseline_review_sources_preserved':160,'assets':integrity},indent=2));(OUT/'summary.json').write_text(json.dumps({'selected':160,'mechanical_pass':160,'original_pngs_preserved':304,'stable_id_count':160,'authored_id_count':8,'runtime_activated':False},indent=2))
print('PASS:160 distinct stable IDs/atlas hashes/mechanical;304 originalPNG hashes;160 prior-source bytes preserved;8authoredIDs preserve mapping/provenance. New art inventory only.')
