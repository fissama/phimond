"""Pack already generated/cut loading sprites; no drawing. QA boards only."""
from pathlib import Path
import json,shutil,hashlib
from PIL import Image,ImageDraw
import numpy as np
p=Path(__file__).resolve().parent

def sha(x):return hashlib.sha256(x.read_bytes()).hexdigest()
def bg(im,scale=1,dark=False):
 im=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
 if dark:b=Image.new('RGBA',im.size,(22,27,34,255))
 else:
  y,x=np.indices((im.height,im.width));v=np.where((x//(16*scale)+y//(16*scale))%2,65,94).astype('uint8');b=Image.fromarray(np.repeat(v[:,:,None],3,2)).convert('RGBA')
 b.alpha_composite(im);return b.convert('RGB')
m=json.loads((p/'manifest.json').read_text());r={a['id']:a for a in m['assets']}
aux=p/'aux-manifest.json'
if aux.exists():r.update({a['id']:a for a in json.loads(aux.read_text())['assets']})
partsall=[]
for name,parts,fps,jobname in [('loading-ornament-corners',['loading-corner-tl','loading-corner-tr','loading-corner-bl','loading-corner-br'],None,'loading-corners-final'),('loading-spinner',[f'loading-spinner-frame-{i:02d}' for i in range(8)],8,'loading-spinner-v2')]:
 d=p/name;d.mkdir(exist_ok=True);j=p/'jobs'/jobname;ims=[Image.open(p/n/'final.png').convert('RGBA') for n in parts];w,h=ims[0].size;out=Image.new('RGBA',(w*len(ims),h))
 for i,im in enumerate(ims):out.alpha_composite(im,(i*w,0))
 out.save(d/'final.png');shutil.copyfile(j/'raw-01.png',d/'raw-01.png');(d/'prompt.md').write_text((p/parts[0]/'prompt.md').read_text()+'\n\nAtlas packed without drawing pixels from: '+', '.join(parts)+'\n')
 a=np.asarray(out);alpha=a[:,:,3];q={'id':name,'size':list(out.size),'colors':len(np.unique(a[:,:,:3][alpha>0],axis=0)),'partial_alpha_pixels':int(((alpha>0)&(alpha<255)).sum()),'sha256':sha(d/'final.png'),'raw_integrity':sha(d/'raw-01.png')==sha(j/'raw-01.png'),'visual_review':'pending_actual_4x_inspection','failures':[]};(d/'qa.json').write_text(json.dumps(q,indent=2))
 for dark,label in [(True,'dark'),(False,'checker')]:
  cols=4 if len(ims)==8 else 2
  board=Image.new('RGB',(w*4*cols,h*4*((len(ims)+cols-1)//cols)))
  for i,im in enumerate(ims):board.paste(bg(im,4,dark),((i%cols)*w*4,(i//cols)*h*4))
  board.save(d/f'review-4x-{label}.png')
 rec=dict(r[parts[0]]);rec.update(id=name,file=name+'/final.png',px=list(out.size),size_px=list(out.size),frames=len(parts),frame_px=[w,h],fps=fps,sha256=q['sha256'],kit='loading-v2',packed_parts=parts,source_raw='raw-01.png',raw_sha256=sha(d/'raw-01.png'));r[name]=rec
 for n in parts:partsall.append(r.pop(n))
spinner=r.pop('loading-spinner');partsall.append(spinner)
m['assets']=list(r.values());m['deferred_stages']=['D intro'];(p/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2));aux.write_text(json.dumps({'assets':partsall},ensure_ascii=False,indent=2))
shutil.copyfile(p/'loading-spinner/final.png',p/'loading-ornament-corners/spinner-8frames.png')
W,H=640,400;out=Image.new('RGB',(W*2,H*((len(r)+1)//2)),(23,28,37));dr=ImageDraw.Draw(out)
for i,a in enumerate(r.values()):
 im=Image.open(p/a['file']).convert('RGBA');scale=min((W-32)/im.width,340/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);pic=Image.new('RGBA',(W,340));pic.alpha_composite(im,((W-im.width)//2,(340-im.height)//2));x=i%2*W;y=i//2*H;out.paste(bg(pic),(x,y+30));dr.text((x+12,y+8),a['id']+' / draft',fill=(235,230,210))
out.save(p/'contact-sheet.png')
print('Root assets',len(r),'aux',len(partsall),'packed colors',[(n,json.loads((p/n/'qa.json').read_text())['colors']) for n in ['loading-ornament-corners','loading-spinner']])
