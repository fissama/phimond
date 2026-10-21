"""Read-only atlas audit; emits evidence, never modifies source art or runtime."""
import csv, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
PLAN = ROOT / '.ai/plan/phases/P10-pet-model'
roster = json.loads((ROOT/'data/p10/species_effective.json').read_text())['records']
selected = json.loads((PLAN/'redraw-kit/owner-atlas-selection.json').read_text())['species']
extra = json.loads((PLAN/'extension-20261013/art-manifest.json').read_text())['records']
fontpath = '/System/Library/Fonts/Supplemental/Arial.ttf'
font = ImageFont.truetype(fontpath, 16)
small = ImageFont.truetype(fontpath, 13)

def source(sid):
    entry = extra.get(sid, selected.get(sid))
    return entry, ROOT/entry['candidate_path']

def measure(path):
    im = Image.open(path).convert('RGBA')
    a = np.asarray(im)[:,:,3]
    frames = []
    for i in range(20):
        al = a[(i//4)*281:(i//4+1)*281,(i%4)*281:(i%4+1)*281]
        vals = {}
        for threshold in (1,41,128):
            y,x = np.where(al >= threshold)
            vals[str(threshold)] = {'w':int(x.max()-x.min()+1),'h':int(y.max()-y.min()+1),'top':int(y.min()),'bottom':int(y.max()),'pixels':int(len(x))}
        frames.append(vals)
    idle = frames[:4]
    height = sum(f['128']['h'] for f in idle)/4
    denom = int(sum(281-f['41']['top'] for f in idle)/4)
    visible = sum(f['41']['h'] for f in idle)/4
    return im, frames, height, denom, visible/denom

refid='species_0144'
_,refpath=source(refid)
ref,_,refh,_,_=measure(refpath)
rows=[]
images={}
for sid,s in roster.items():
    if s['star']<4: continue
    entry,path=source(sid)
    im,frames,h,denom,fraction=measure(path)
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    expected=entry.get('candidate_sha256',entry.get('sha256'))
    assert digest==expected, sid
    images[sid]=im
    rows.append({'id':sid,'name':s['display_name']['vi'],'star':s['star'],'race':s['race_id'],
        'special':s['species_class']=='special','path':str(path.relative_to(ROOT)),
        'sha256':digest,'approval':entry.get('status'),
        'idle_solid_h':round(h,2),'idle_solid_w':round(sum(f['128']['w'] for f in frames[:4])/4,2),
        'reference_ratio':round(h/refh,3),'builder_bodyH':denom,
        'modeled_visible_fraction':round(fraction,3),'frames':frames})
summary={'scope':'56 source atlases plus current renderer; not a live 56-species playtest',
    'reference':{'id':refid,'path':str(refpath),'idle_mean_h':refh},'records':rows}
(OUT/'measurements.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
with (OUT/'measurements.csv').open('w') as f:
    keys=[k for k in rows[0] if k!='frames']
    writer=csv.DictWriter(f,keys);writer.writeheader()
    writer.writerows({k:r[k] for k in keys} for r in rows)

def paste_frame(canvas,im,frame,x,y,size=112):
    crop=im.crop(((frame%4)*281,(frame//4)*281,(frame%4+1)*281,(frame//4+1)*281))
    crop=crop.resize((size,size),Image.Resampling.NEAREST)
    canvas.alpha_composite(crop,(x,y))

for page,start in enumerate(range(0,len(rows),8),1):
    canvas=Image.new('RGBA',(1010,1140),(24,30,40,255));d=ImageDraw.Draw(canvas)
    d.text((16,12),f'4/5 STAR SIZE AUDIT — {page}/7 — equal 112px cells, no auto-fit',font=font,fill='white')
    paste_frame(canvas,ref,0,650,38)
    d.text((16,50),'Reference: species_0144 Linh Tiên Hoa Hương',font=font,fill='#ffd982')
    d.text((16,80),f'Idle mean {refh:.1f}px / 281px; opaque alpha >= 128',font=small,fill='#bbc5d1')
    for col,title in enumerate(['idle f0','move f5','attack f10','skill f14','down f19']):
        d.text((385+col*123,160),title,font=small,fill='#bbc5d1')
    for n,r in enumerate(rows[start:start+8]):
        y=183+n*118
        d.rectangle((10,y,1000,y+114),fill=(34,43,57,255))
        d.text((16,y+12),f"{r['id']}  {r['star']}★  {r['race']}",font=font,fill='white')
        d.text((16,y+38),r['name'],font=font,fill='#ffd982')
        d.text((16,y+66),f"solid {r['idle_solid_h']}px / ref {r['reference_ratio']:.2f}x",font=small,fill='#bbc5d1')
        for col,frame in enumerate((0,5,10,14,19)):
            paste_frame(canvas,images[r['id']],frame,385+col*123,y)
    canvas.convert('RGB').save(OUT/f'contact-{page:02}.jpg',quality=94)
print(json.dumps({'count':len(rows),'reference_h':refh,'min_h':min(r['idle_solid_h'] for r in rows),'max_h':max(r['idle_solid_h'] for r in rows),'below_80pct_reference':[r['id'] for r in rows if r['reference_ratio']<.8]},ensure_ascii=False))
