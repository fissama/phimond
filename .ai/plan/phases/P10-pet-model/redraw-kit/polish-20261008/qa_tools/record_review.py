"""Record lead visual review; final QA requires separate battle and independent evidence."""
import argparse
import hashlib
import json
from pathlib import Path

REPO=Path(__file__).resolve().parents[7]
KIT=REPO/'.ai/plan/phases/P10-pet-model/redraw-kit/polish-20261008'
ASSETS=REPO/'apps/game-client/assets/pets/redraws/polish-20261008'

def dump(path,data): path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--species',required=True)
    p.add_argument('--candidate',required=True,type=Path)
    p.add_argument('--note',required=True)
    a=p.parse_args();root=a.candidate.resolve();atlas=root/'packed.png'
    catalog=json.loads((REPO/'data/p10/species.json').read_text())['records'][a.species]
    sha=hashlib.sha256(atlas.read_bytes()).hexdigest()
    mechanical=json.loads((root/'mechanical.json').read_text())
    if mechanical['status']!='pass': raise ValueError('Mechanical QA failed')
    previous_path=ASSETS/a.species/'result.json'
    previous=json.loads(previous_path.read_text()) if previous_path.exists() else {}
    result={'species_id':a.species,'name_vi':catalog['display_name']['vi'],'status':'qa_pending_battle_layout','candidate_path':str(atlas.relative_to(REPO)),'candidate_sha256':sha,'preview_path':str((root/'preview/preview.html').relative_to(REPO)),'human_approved':bool(previous.get('human_approved',False) and previous.get('candidate_sha256')==sha),'animation_playback_verified':True,'lead_visual_review_passed':True,'battle_trial_passed':False,'independent_review_passed':False,'runtime_active':False,'review_note':a.note+' Final battle-size trial and independent exact-hash review pending; no runtime activation.'}
    dump(previous_path,result)
    review=f"# {result['name_vi']} — lead visual review\n\n{a.note}\n\n- Generation identity references are original APK images only; exact portrait/sprite inputs and hashes are recorded in inputs.json.\n- Whole source alpha preserved; common NN packing scale, no per-frame resizing.\n- Mechanical checker PASS for exact candidate SHA `{sha}`.\n- All five animation rows checked at 64/96/192; light/dark preview inspected.\n- Battle-size trial and independent exact-hash review remain pending. Owner approval is recorded separately; runtime inactive.\n"
    (root/'review.md').write_text(review)
    progress_path=KIT/'progress.json';progress=json.loads(progress_path.read_text())
    ready=[]
    for sid in progress['ordered_species_ids']:
        rp=ASSETS/sid/'result.json'
        if not rp.exists():continue
        r=json.loads(rp.read_text())
        if r.get('status')!='repair_required' and r.get('animation_playback_verified'):ready.append(sid)
    progress['lead_visual_ready_ids']=ready
    if a.species not in progress['blocked_ids']:progress['blocked_ids'].append(a.species)
    order=progress['ordered_species_ids'];index=order.index(a.species)
    progress['last_completed_species_id']=a.species
    progress['active_species_id']=order[index+1] if index+1<len(order) else None
    dump(progress_path,progress)
    qa=len(progress['qa_passed_ids']);visual=len(ready)
    with (KIT/'execution-ledger.md').open('a') as f:
        f.write(f"\n#{index+1} {a.species} {result['name_vi']} — LEAD ART REVIEW PASS, FINAL GATES PENDING. {a.note} SHA {sha}. Lead visually ready {visual}/48 ({visual/48*100:.2f}%); final QA {qa}/48 ({qa/48*100:.2f}%).\n")
    print(json.dumps({'species':a.species,'name':result['name_vi'],'order':index+1,'lead_visual_ready':visual,'lead_visual_percent':round(visual/48*100,2),'qa_passed':qa,'qa_percent':round(qa/48*100,2),'next':progress['active_species_id']},ensure_ascii=False))

if __name__=='__main__':main()
