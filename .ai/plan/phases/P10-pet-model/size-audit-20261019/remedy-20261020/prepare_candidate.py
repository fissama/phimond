"""Pack an observed 4x5 native image; record all pixels and build review only."""
import argparse, hashlib, importlib.util, json, shutil
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np

ROOT=Path(__file__).resolve().parents[6]
OUT=Path(__file__).resolve().parent

def module(name,rel):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def metrics(path):
    im=Image.open(path).convert('RGBA');out=[]
    for i in range(20):
        cell=im.crop(((i%4)*281,(i//4)*281,(i%4+1)*281,(i//4+1)*281))
        a=np.asarray(cell)[:,:,3];y,x=np.where(a>=128)
        out.append({'frame':i,'opaque_h':int(y.max()-y.min()+1),'opaque_w':int(x.max()-x.min()+1)})
    return out

def run(sid,raw,attempt,roots=None,dest_y=258,row_edges=None,column_edges=None):
    records=json.loads((OUT.parent/'measurements.json').read_text())['records']
    before=next(r for r in records if r['id']==sid)
    ref=next(r for r in records if r['id']=='species_0144')
    target=ROOT/f'apps/game-client/assets/pets/redraws/size-remedy-20261020/{sid}/{attempt}'
    target.mkdir(parents=True,exist_ok=True)
    dest=target/'raw.png'
    if not dest.exists():shutil.copyfile(raw,dest)
    im=Image.open(dest);w,h=im.size
    frames=[]
    for row in range(5):
        y0=row_edges[row] if row_edges else round(row*h/5)
        y1=row_edges[row+1] if row_edges else round((row+1)*h/5)
        alpha=np.asarray(im)[y0:y1,:,3]
        edges=[0]
        for col in (1,2,3):
            nominal=round(col*w/4)
            zero=np.where(np.all(alpha[:,nominal-60:nominal+60]==0,axis=0))[0]+nominal-60
            edges.append(int(zero[np.argmin(abs(zero-nominal))]) if len(zero) else nominal)
        edges.append(w)
        if column_edges and str(row) in column_edges:
            edges=column_edges[str(row)]
        for col in range(4):
            x0,x1=edges[col:col+2]
            # Gutter changes source ownership only; nominal root stays fixed.
            frames.append({'rect':[x0,y0,x1-x0,y1-y0],'pivot':[(col+.5)*w/4-x0,roots[row] if roots else y1-y0]})
    # One fixed cell-bottom registration, never per-pose bbox fitting.
    layout={'destination_pivot':[140,dest_y],'frames':frames}
    if (target/'packed.png').exists():
        assert json.loads((target/'layout.json').read_text())==layout, 'Use a new attempt when layout changes'
    (target/'layout.json').write_text(json.dumps(layout,indent=2))
    packed=target/'packed.png'
    if not packed.exists():
        pack=module('pack', 'tools/assets/pack_p10_atlas.py')
        result=pack.pack(dest,target/'layout.json',packed)
        (target/'packing.json').write_text(json.dumps(result,indent=2))
    check=module('checker','tools/assets/check_p10_atlas.py').check(packed)
    (target/'mechanical.json').write_text(json.dumps(check,indent=2))
    review=OUT/sid/attempt;review.mkdir(parents=True,exist_ok=True)
    for name,src in [('before',ROOT/before['path']),('after',packed),('reference',ROOT/ref['path'])]:
        shutil.copyfile(src,review/f'{name}.png')
    # QA views must respect alpha: hidden RGB under alpha=0 is not background art.
    for label,color in [('dark','#202936'),('light','#dce4ed')]:
        composite=Image.new('RGBA',(1124,1405),color)
        composite.alpha_composite(Image.open(packed).convert('RGBA'))
        composite.convert('RGB').save(review/f'native-{label}.jpg',quality=98)
    stats={'before':metrics(ROOT/before['path']),'after':metrics(packed),'reference':metrics(ROOT/ref['path'])}
    for size in (96,192):
        canvas=Image.new('RGBA',(3*4*size+170,5*(size+35)+50),(28,35,47,255));d=ImageDraw.Draw(canvas)
        f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',16)
        for n,name in enumerate(('before','after','reference')):
            atlas=Image.open(review/f'{name}.png').convert('RGBA')
            d.text((170+n*4*size,10),name+f' / cell {size}px',fill='white',font=f)
            for row,title in enumerate(('idle','movement','basic','skill','hurt/down')):
                d.text((5,50+row*(size+35)),title,fill='white',font=f)
                for col in range(4):
                    cell=atlas.crop((col*281,row*281,(col+1)*281,(row+1)*281)).resize((size,size),Image.Resampling.NEAREST)
                    canvas.alpha_composite(cell,(170+(n*4+col)*size,40+row*(size+35)))
        canvas.save(review/f'comparison-{size}.png')
    metadata={'species_id':sid,'name':before['name'],'action':'redraw','art_source':'host_image','runtime_activated':False,'owner_approved':False,
        'before_path':before['path'],'before_sha256':before['sha256'],'candidate_path':str(packed.relative_to(ROOT)),
        'candidate_sha256':hashlib.sha256(packed.read_bytes()).hexdigest(),'mechanical':check['status'],
        'visual_status':'pending_self_review','metrics':stats,'review_path':str(review.relative_to(ROOT))}
    (target/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2))
    (review/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2))
    html='''<!doctype html><meta charset="utf-8"><title>Candidate review</title><style>body{font:16px system-ui;background:#18202b;color:white;padding:24px}canvas{image-rendering:pixelated;border:1px solid #637082;margin:10px}button,select{font:inherit;margin:8px}img{max-width:100%;image-rendering:pixelated}section{display:flex;flex-wrap:wrap}</style><h1>TITLE</h1><p>Review only — chưa duyệt, chưa runtime. Cùng cell, không auto-fit. 281px là native; 96/192px là preview, chưa phải in-game capture.</p><select id="row"><option value="0">Idle loop</option><option value="1">Movement loop</option><option value="2">Basic one-shot</option><option value="3">Skill one-shot</option><option value="4">Hurt / fully down</option></select><select id="size"><option>96</option><option selected>192</option><option>281</option></select><button id="play">Play / restart</button><button id="stop">Pause</button><button id="bg">Light / dark</button><div id="steps"></div><section id="panels"></section><p id="status"></p><h2>All 20 frames at equal cell size</h2><img src="comparison-96.png"><p><a href="comparison-192.png">192px comparison</a> · <a href="metadata.json">Measurements and hashes</a></p><script>
const row=document.getElementById('row'),size=document.getElementById('size'),play=document.getElementById('play'),stop=document.getElementById('stop'),bg=document.getElementById('bg'),steps=document.getElementById('steps'),panels=document.getElementById('panels'),status=document.getElementById('status');
const names=['before','after','reference'];const imgs=names.map(n=>{const i=new Image();i.src=n+'.png';return i});const canv=names.map(n=>{const box=document.createElement('div');box.innerHTML='<h2>'+n+'</h2>';const c=document.createElement('canvas');box.append(c);panels.append(box);return c});let frame=0,running=false,last=0,light=false;
for(let j=0;j<4;j++){const b=document.createElement('button');b.textContent='Frame '+(j+1);b.onclick=()=>{running=false;frame=j;draw()};steps.append(b)}
function draw(){const s=Number(size.value),r=Number(row.value);canv.forEach((c,k)=>{c.width=c.height=s;const x=c.getContext('2d');x.imageSmoothingEnabled=false;x.fillStyle=light?'#dce3eb':'#222c39';x.fillRect(0,0,s,s);if(imgs[k].complete)x.drawImage(imgs[k],frame*281,r*281,281,281,0,0,s,s)});status.textContent='Row '+(r+1)+' / frame '+(frame+1)+' — '+(r<2?'loop':'one-shot; holds frame 4')}
row.onchange=()=>{frame=0;running=false;draw()};size.onchange=draw;play.onclick=()=>{frame=0;running=true;last=performance.now();draw()};stop.onclick=()=>running=false;bg.onclick=()=>{light=!light;draw()};imgs.forEach(i=>i.onload=draw);function tick(t){if(running&&t-last>=180){last=t;if(frame<3)frame++;else if(Number(row.value)<2)frame=0;else running=false;draw()}requestAnimationFrame(tick)}requestAnimationFrame(tick);draw();
</script>'''
    (review/'index.html').write_text(html.replace('TITLE',sid+' — '+before['name']))
    print(json.dumps({'candidate':str(packed),'mechanical':check['status'],'idle_h_before':sum(x['opaque_h'] for x in stats['before'][:4])/4,'idle_h_after':sum(x['opaque_h'] for x in stats['after'][:4])/4,'review':str(review)},ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('species');p.add_argument('raw',type=Path);p.add_argument('--attempt',default='attempt-01');p.add_argument('--roots',type=json.loads);p.add_argument('--dest-y',type=int,default=258);p.add_argument('--row-edges',type=json.loads);p.add_argument('--column-edges',type=json.loads);a=p.parse_args();run(a.species,a.raw,a.attempt,a.roots,a.dest_y,a.row_edges,a.column_edges)
