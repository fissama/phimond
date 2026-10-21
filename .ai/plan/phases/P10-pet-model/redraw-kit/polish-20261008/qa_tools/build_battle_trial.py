"""Standalone art-size/layout evidence; never modifies atlas pixels or runtime."""
import hashlib
import json
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[7]
ASSETS = REPO / 'apps/game-client/assets/pets/redraws/polish-20261008'
KIT = REPO / '.ai/plan/phases/P10-pet-model/redraw-kit/polish-20261008'
OUT = ASSETS / 'battle-trial-20261009'
ANCHORS = [(76,125),(206,125),(141,275),(363,199)]

def intersects(a,b):
    return a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]

def main():
    OUT.mkdir(exist_ok=True)
    catalog=json.loads((REPO/'data/p10/species.json').read_text())['records']
    order=json.loads((KIT/'progress.json').read_text())['ordered_species_ids']
    entries=[]
    for sid in order:
        rp=ASSETS/sid/'result.json'
        result=json.loads(rp.read_text()) if rp.exists() else {}
        path=REPO/result['candidate_path'] if result.get('candidate_path') else None
        # Pending drafts are explicitly labeled; they never become selected by this tool.
        if sid=='species_0019': path=ASSETS/sid/'cohesive-20261009/attempt-02/packed.png'
        if sid=='species_0086': path=ASSETS/sid/'cohesive-20261009/attempt-04/packed.png'
        if path is None or not path.exists(): continue
        atlas=Image.open(path).convert('RGBA')
        if atlas.size!=(1124,1405): raise ValueError(f'{sid}: wrong dimensions')
        cells=[atlas.crop((c*281,r*281,(c+1)*281,(r+1)*281)) for r in range(5) for c in range(4)]
        body=[im.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox() for im in cells]
        visual=[im.getchannel('A').point(lambda v:255 if v>=16 else 0).getbbox() for im in cells]
        rec=catalog[sid];special=rec['species_class']=='special'
        height=64 if rec['star']==4 or sid=='species_0148' else 82 if special else 74
        width=88 if rec['star']==4 else 108 if special else 100
        # One global factor for the complete atlas, including wings, staff and FX.
        factor=min(height/(body[0][3]-body[0][1]),width/max(b[2]-b[0] for b in visual),90/max(210-b[1] for b in visual))
        poses=[];errors=[]
        for i,b in enumerate(visual):
            boxes=[];labels=[];bars=[]
            for j,(x,y) in enumerate(ANCHORS):
                flip=j<3
                left=x+((140-b[2]) if flip else (b[0]-140))*factor
                right=x+((140-b[0]) if flip else (b[2]-140))*factor
                top=y+(b[1]-210)*factor;bottom=y+(b[3]-210)*factor
                box=[left,top,right,bottom]
                boxes.append(box);labels.append([x-55,top-28,x+55,top-4]);bars.append([x-29,bottom+9,x+29,bottom+14])
                if min(left,top-28)<0 or right>480 or bottom+14>320:errors.append({'frame':i,'unit':j,'type':'viewport_clip'})
            for j in range(4):
                for k in range(j+1,4):
                    groups=[('sprite',boxes),('name',labels),('hp',bars)]
                    for na,ga in groups:
                        for nb,gb in groups:
                            if intersects(ga[j],gb[k]):errors.append({'frame':i,'units':[j,k],'type':na+'_'+nb+'_overlap'})
            poses.append({'frame':i,'alpha16_bounds':list(b),'sprite_boxes':boxes,'name_boxes':labels,'hp_boxes':bars})
        sha=hashlib.sha256(path.read_bytes()).hexdigest()
        entry={'id':sid,'name':rec['display_name']['vi'],'star':rec['star'],'special':special,'nominal_height':height,'trial_idle_height':round((body[0][3]-body[0][1])*factor,2),'factor':factor,'max_width':width,'sha256':sha,'atlas':'../'+str(path.relative_to(ASSETS)),'original':'/original/'+rec['source']['species_id']+'/portrait.png','selected':result.get('candidate_sha256')==sha,'lead_reviewed':result.get('candidate_sha256')==sha and result.get('lead_visual_review_passed',False),'bounds':visual,'geometry_passed':not errors,'errors':errors,'poses':poses}
        entries.append(entry)
    (OUT/'manifest.json').write_text(json.dumps({'scope':'Standalone ART TRIAL, not runtime integration or owner approval','canvas':[480,320],'anchors':ANCHORS,'alpha_threshold_geometry':16,'entries':entries},ensure_ascii=False,indent=2)+'\n')
    (OUT/'index.html').write_text(HTML.replace('__ENTRIES__',json.dumps(entries,ensure_ascii=False)))
    print(json.dumps({'trial':str(OUT),'entries':len(entries),'geometry_passed':sum(e['geometry_passed'] for e in entries),'unselected':[e['id'] for e in entries if not e['selected']],'art_capped':[e['id'] for e in entries if e['trial_idle_height']<e['nominal_height']-1]},ensure_ascii=False))

HTML='''<!doctype html><html lang="vi"><meta charset="utf-8"><title>P10 — thử size 48 loài</title>
<style>body{background:#242933;color:#f6f2e6;font:15px system-ui;margin:20px}h1{font-size:23px}select,button{font:inherit;padding:7px;margin:4px}canvas{image-rendering:pixelated;max-width:100%;border:1px solid #737d90}#gallery{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.card{border:1px solid #687384;padding:8px}.card canvas{width:100%;height:auto}.card button{font-size:13px}#main{display:flex;gap:20px;flex-wrap:wrap}#detail{max-width:450px}code{overflow-wrap:anywhere}#allposes{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}#allposes canvas{width:100%}.bad{color:#ffb58f}</style>
<h1>P10 — thử kích thước và khoảng cách battle</h1><p>48 loài · màn 480×320 · cùng một tỷ lệ cho mọi pose. Bản thử mỹ thuật, chưa tích hợp game; chưa suy ra owner duyệt.</p>
<label>Loài <select id="species"></select></label><label>Hoạt ảnh <select id="row"><option>Idle</option><option>Move</option><option>Đánh thường</option><option>Cast</option><option>Hurt / Down</option></select></label><button id="pause">Dừng / chạy</button><button id="theme">Đổi nền</button>
<div id="main"><canvas id="battle" width="480" height="320"></canvas><div id="detail"></div></div><h2>20 pose tại tỷ lệ battle</h2><div id="allposes"></div><h2>So sánh 48 loài — Idle</h2><div id="gallery"></div>
<script>
const entries=__ENTRIES__, images=new Map(), anchors=[[76,125],[206,125],[141,275],[363,199]];
const picker=document.getElementById('species'), row=document.getElementById('row'), battle=document.getElementById('battle'),detail=document.getElementById('detail');let dark=true,paused=false,start=performance.now();
for(const e of entries){const o=new Option(e.name+' · '+e.star+'★'+(e.special?' Special':''),e.id);picker.add(o);const im=new Image();im.src=e.atlas;images.set(e.id,im)}
function drawPose(ctx,e,frame,x,y,flip=false){const im=images.get(e.id);if(!im.complete||!im.naturalWidth)return;ctx.save();ctx.translate(x,y);if(flip)ctx.scale(-1,1);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,(frame%4)*281,Math.floor(frame/4)*281,281,281,-140*e.factor,-210*e.factor,281*e.factor,281*e.factor);ctx.restore()}
function nameLines(name){const words=name.split(' ');if(words.length<3)return[name];const cut=Math.ceil(words.length/2);return[words.slice(0,cut).join(' '),words.slice(cut).join(' ')]}
function scene(canvas,e,frame){const ctx=canvas.getContext('2d');ctx.fillStyle=dark?'#515e69':'#dfdac4';ctx.fillRect(0,0,480,320);ctx.font='11px system-ui';ctx.textAlign='center';const b=e.bounds[frame];for(let j=0;j<4;j++){const[x,y]=anchors[j],top=y+(b[1]-210)*e.factor,bottom=y+(b[3]-210)*e.factor;ctx.strokeStyle=j===3?'#ffd981':'#afc9d8';ctx.lineWidth=1;ctx.beginPath();ctx.ellipse(x,y+4,30,5,0,0,Math.PI*2);ctx.stroke();drawPose(ctx,e,frame,x,y,j<3);ctx.fillStyle=dark?'#fff8df':'#202b35';const lines=nameLines(e.name);lines.forEach((line,k)=>ctx.fillText(line,x,top-17+k*12));ctx.fillStyle='#25302d';ctx.fillRect(x-29,bottom+9,58,5);ctx.fillStyle='#8ce1a3';ctx.fillRect(x-28,bottom+10,48,3)}}
function refresh(){const e=entries.find(e=>e.id===picker.value);detail.innerHTML='';const heading=document.createElement('h2');heading.textContent=e.name;detail.append(heading);const p=document.createElement('p');p.textContent=`${e.star}★ ${e.special?'Special':''} · thân Idle ${e.trial_idle_height}px (đề xuất ${e.nominal_height}px) · giới hạn rộng ${e.max_width}px. Geometry ${e.geometry_passed?'PASS':'CẦN SỬA'}. ${e.selected?'Bản chọn':'Bản thử chưa chọn'}.`;detail.append(p);const hash=document.createElement('code');hash.textContent=e.sha256;detail.append(hash);const all=document.getElementById('allposes');all.replaceChildren();for(let f=0;f<20;f++){const box=document.createElement('div'),label=document.createElement('p');label.textContent=`R${Math.floor(f/4)+1} C${f%4+1}`;const c=document.createElement('canvas');c.width=480;c.height=320;box.append(label,c);all.append(box);scene(c,e,f)}}
picker.onchange=refresh;document.getElementById('pause').onclick=()=>paused=!paused;document.getElementById('theme').onclick=()=>{dark=!dark;refresh();gallery()};
function gallery(){const g=document.getElementById('gallery');g.replaceChildren();for(const e of entries){const box=document.createElement('div');box.className='card';const button=document.createElement('button');button.textContent=e.name+' '+e.star+'★';button.onclick=()=>{picker.value=e.id;refresh();window.scrollTo(0,0)};const c=document.createElement('canvas');c.width=480;c.height=320;box.append(button,c);g.append(box);scene(c,e,0)}}
picker.value='species_0037';let current=0;function tick(t){if(!paused)current=Math.floor((t-start)/180)%4;const e=entries.find(e=>e.id===picker.value);scene(battle,e,row.selectedIndex*4+current);requestAnimationFrame(tick)}
Promise.all([...images.values()].map(im=>im.complete?Promise.resolve():new Promise(r=>{im.onload=r;im.onerror=r}))).then(()=>{refresh();gallery();requestAnimationFrame(tick)});
</script></html>'''

if __name__=='__main__':main()
