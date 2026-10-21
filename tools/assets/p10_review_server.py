#!/usr/bin/env python3
"""Local effective-roster art review, with version-bound owner feedback."""
import argparse
from datetime import datetime, timezone
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
from urllib.parse import unquote, urlsplit
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PETS = ROOT / 'apps/game-client/assets/pets'
KIT = ROOT / '.ai/plan/phases/P10-pet-model/redraw-kit'
PAGE = Path(__file__).with_name('p10_review.html')
EXTENSION = PETS / 'redraws/extension-20261013'
RACES = {'undead':'Bất Tử','plant':'Thực Vật','dragon':'Rồng','demon':'Ác Ma','beast':'Dã Thú','bird':'Chim','insect':'Côn Trùng','spirit':'Linh Thể'}

def read_json(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default

def asset_url(path):
    return '/assets/' + path.resolve().relative_to(PETS).as_posix()

def atlas_details(path, sid):
    path = path.resolve()
    if not path.is_relative_to(PETS.resolve()):
        raise ValueError('Atlas outside pet assets')
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    with Image.open(path) as atlas:
        if atlas.mode != 'RGBA' or atlas.size != (1124, 1405):
            raise ValueError(f'Invalid atlas: {sid}')
        bounds = []
        for row in range(5):
            for col in range(4):
                box = atlas.crop((col*281, row*281, (col+1)*281, (row+1)*281)).getchannel('A').getbbox()
                if not box:
                    raise ValueError(f'Empty pose: {sid}')
                bounds.append(box)
    return sha, bounds

def authored_review_row(sid, rec):
    """Pending art remains visible without inventing an APK portrait or approval."""
    result = read_json(EXTENSION/sid/'result.json', {})
    candidate = result.get('candidate_path')
    path = (ROOT/candidate).resolve() if candidate else None
    sha = None
    bounds = []
    if path is not None and path.is_file():
        sha, bounds = atlas_details(path, sid)
        expected = result.get('candidate_sha256')
        if not expected or sha != expected:
            raise ValueError(f'Authored candidate hash mismatch: {sid}')
    else:
        path = None
    name = rec['display_name']['vi']
    visual_notes = result.get('visual_notes', [])
    if isinstance(visual_notes, list):
        visual_notes = ' · '.join(note for note in visual_notes if isinstance(note, str))
    elif not isinstance(visual_notes, str):
        visual_notes = ''
    return {'id': sid, 'name': name, 'star': rec['star'], 'race': rec['race_id'],
            'race_name': RACES[rec['race_id']], 'special': rec['species_class']=='special',
            'atlas': asset_url(path) if path else None, 'sha256': sha,
            'original': None, 'bounds': bounds, 'draft': True,
            'audit': result.get('independent_review', 'pending'),
            'previously_approved': False, 'owner_done': False,
            'runtime_activated': False, 'provenance': 'Phimond-authored',
            'art_status': 'candidate_for_owner_review' if path else 'awaiting_candidate',
            'version': str(path.parent.relative_to(PETS/'redraws')) if path else 'Chưa có atlas',
            'revision_note': visual_notes}

def build_catalog():
    roster=read_json(ROOT/'data/p10/species.json')['records']
    jobs={j['species_id']:j for j in read_json(KIT/'manifest.json')['jobs']}
    trial=read_json(PETS/'redraws/polish-20261008/battle-trial-20261009/manifest.json',{'entries':[]})
    drafts={e['id']:e for e in trial['entries'] if not e['selected']}
    audit=read_json(KIT/'polish-20261008/independent-review-20261009.json',{'entries':[]})
    reviewed={e['sha256']:e['independent_visual_status'] for e in audit['entries']}
    selections=read_json(KIT/'owner-atlas-selection.json',{'species':{}})['species']
    rows=[]
    for sid,rec in roster.items():
        options=[PETS/'redraws/polish-20261008'/sid/'result.json']
        if sid in jobs:options.append(ROOT/jobs[sid]['output_dir']/'result.json')
        result={};path=None;draft=False
        for rp in options:
            candidate=read_json(rp,{})
            possible=ROOT/candidate.get('candidate_path','')
            if possible.is_file():result=candidate;path=possible;break
        if sid in drafts:
            possible=(PETS/'redraws/polish-20261008/battle-trial-20261009'/drafts[sid]['atlas']).resolve()
            if possible.is_file() and hashlib.sha256(possible.read_bytes()).hexdigest()==drafts[sid]['sha256']:
                path=possible;draft=True
        selection=selections.get(sid)
        if selection:
            path=(ROOT/selection['candidate_path']).resolve()
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=selection['sha256']:
                raise ValueError(f'Owner selection hash mismatch: {sid}')
            draft=selection.get('status')=='owner_revision_ready'
        if path is None:raise ValueError(f'Missing atlas: {sid}')
        path=path.resolve()
        if not path.is_relative_to(PETS.resolve()):raise ValueError('Atlas outside pet assets')
        sha=hashlib.sha256(path.read_bytes()).hexdigest()
        atlas=Image.open(path).convert('RGBA')
        if atlas.size!=(1124,1405):raise ValueError(f'Invalid atlas: {sid}')
        bounds=[]
        for r in range(5):
            for c in range(4):
                box=atlas.crop((c*281,r*281,(c+1)*281,(r+1)*281)).getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox()
                if not box:raise ValueError(f'Empty pose: {sid}')
                bounds.append(box)
        original=PETS/'apk84'/rec['source']['species_id']/'portrait.png'
        rows.append({'id':sid,'name':rec['display_name']['vi'],'star':rec['star'],'race':rec['race_id'],'race_name':RACES[rec['race_id']],'special':rec['species_class']=='special','atlas':asset_url(path),'sha256':sha,'original':asset_url(original),'bounds':bounds,'draft':draft,'audit':reviewed.get(sha,'pending'),'previously_approved':bool(result.get('human_approved') and result.get('candidate_sha256')==sha),'version':str(path.parent.relative_to(PETS/'redraws'))})
        rows[-1]['revision_note']=selection.get('revision_note','') if selection else ''
        rows[-1]['owner_done']=selection.get('status')=='owner_approved_done' if selection else False
        rows[-1]['previously_approved'] |= rows[-1]['owner_done']
        rows[-1]['provenance']='APK source identity · owner-approved redraw' if rows[-1]['owner_done'] else 'APK source identity'
        rows[-1]['art_status']='owner_approved_done' if rows[-1]['owner_done'] else 'candidate_for_owner_review'
    if len(rows)!=152:raise ValueError('Frozen roster must contain 152 species')
    effective = read_json(ROOT/'data/p10/species_effective.json', {'records': roster})['records']
    for sid, rec in effective.items():
        if sid not in roster:
            rows.append(authored_review_row(sid, rec))
    if len(rows) not in (152,160):raise ValueError('Effective roster must contain 152 or 160 species')
    return rows

class ReviewServer(ThreadingHTTPServer):
    def __init__(self, address, reviews_path):
        self.catalog=build_catalog()
        self.species={e['id']:e for e in self.catalog}
        self.reviews_path=Path(reviews_path)
        self.lock=threading.Lock()
        super().__init__(address, Handler)

    def reviews(self):
        return read_json(self.reviews_path,{'schema_version':1,'reviews':{}})

class Handler(BaseHTTPRequestHandler):
    def send(self, status, data, mime='application/json; charset=utf-8'):
        payload=json.dumps(data,ensure_ascii=False).encode() if isinstance(data,(dict,list)) else data
        self.send_response(status)
        self.send_header('Content-Type',mime)
        self.send_header('Content-Length',str(len(payload)))
        self.send_header('Cache-Control','no-store' if not mime.startswith('image/') else 'private, max-age=3600')
        self.end_headers();self.wfile.write(payload)

    def do_GET(self):
        path=unquote(urlsplit(self.path).path)
        if path in ('/','/index.html'):return self.send(200,PAGE.read_bytes(),'text/html; charset=utf-8')
        if path=='/api/species':return self.send(200,{'total':len(self.server.catalog),'species':self.server.catalog})
        if path=='/api/reviews':
            with self.server.lock:return self.send(200,self.server.reviews())
        if path=='/healthz':return self.send(200,{'status':'ok','species':len(self.server.catalog)})
        if path.startswith('/assets/'):
            target=(PETS/path[len('/assets/'):]).resolve()
            if target.is_relative_to(PETS.resolve()) and target.suffix.lower()=='.png' and target.is_file():
                return self.send(200,target.read_bytes(),'image/png')
        self.send(404,{'error':'Không tìm thấy'})

    def do_POST(self):
        if urlsplit(self.path).path!='/api/reviews':return self.send(404,{'error':'Không tìm thấy'})
        origin=self.headers.get('Origin')
        host=self.headers.get('Host','')
        if origin and origin not in ('http://'+host,):return self.send(403,{'error':'Origin không hợp lệ'})
        if self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.send(415,{'error':'Cần JSON'})
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=32768:raise ValueError('Độ dài không hợp lệ')
            data=json.loads(self.rfile.read(length));sid=data['species_id'];sha=data['sha256'];comment=data.get('comment','');approved=data['approved']
            if not isinstance(comment,str) or len(comment)>10000 or type(approved) is not bool:raise ValueError('Nhận xét không hợp lệ')
            current=self.server.species.get(sid)
            if not current or not current['sha256'] or current['sha256']!=sha:return self.send(409,{'error':'Phiên bản atlas đã đổi hoặc chưa có atlas. Hãy tải lại trang.'})
            atlas = (PETS/current['atlas'][len('/assets/'):]).resolve()
            if not atlas.is_relative_to(PETS.resolve()) or not atlas.is_file() or hashlib.sha256(atlas.read_bytes()).hexdigest()!=sha:
                return self.send(409,{'error':'Bytes atlas đã đổi. Hãy tải lại server/trang review.'})
            record={'species_id':sid,'name':current['name'],'sha256':sha,'approved':approved,'comment':comment,'animation':data.get('animation','idle'),'updated_at':datetime.now(timezone.utc).isoformat(),'source':'owner_web_review'}
            with self.server.lock:
                doc=self.server.reviews();doc['reviews'].setdefault(sid,{})[sha]=record
                dest=self.server.reviews_path;dest.parent.mkdir(parents=True,exist_ok=True)
                tmp=dest.with_suffix('.tmp');tmp.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n');tmp.replace(dest)
            return self.send(200,{'saved':True,'review':record})
        except (ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:return self.send(400,{'error':str(exc)})

def main():
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8125);p.add_argument('--reviews',type=Path,default=KIT/'owner-reviews.json');args=p.parse_args()
    server=ReviewServer(('127.0.0.1',args.port),args.reviews)
    print(f'P10 review: http://127.0.0.1:{server.server_port} · {len(server.catalog)} species · reviews {args.reviews}',flush=True)
    server.serve_forever()

if __name__=='__main__':main()
