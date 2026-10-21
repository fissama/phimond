"""Crop generated UI ownership boxes and pixel-finish; never draws replacement art."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json,hashlib
import numpy as np,math
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[4]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o):Path(p).write_text(json.dumps(o,indent=2)+"\n")
def stretch(im,size,s):
 l,t,r,b=s;w,h=im.size;ow,oh=size
 out=Image.new('RGBA',size)
 xs=[0,l,w-r,w];ys=[0,t,h-b,h];xx=[0,l,ow-r,ow];yy=[0,t,oh-b,oh]
 for i in range(3):
  for j in range(3):
   tile=im.crop((xs[i],ys[j],xs[i+1],ys[j+1])).resize((xx[i+1]-xx[i],yy[j+1]-yy[j]),Image.Resampling.NEAREST)
   out.paste(tile,(xx[i],yy[j]))
 return out
records=[]
for jp in sorted((ROOT/'jobs').glob('*/job.json')):
 job=json.loads(jp.read_text());raw=jp.parent/job.get('selected_raw','raw-01.png');sheet=Image.open(raw).convert('RGBA')
 refs=[{'path':p,'sha256':sha(p)} for p in job['refs']]
 for spec in job['assets']:
  dest=ROOT/spec['id'];dest.mkdir(exist_ok=True)
  im=sheet.crop(spec['box']);a=im.getchannel('A').point(lambda v:255 if v>=160 else 0);im.putalpha(a);bb=im.getchannel('A').getbbox()
  if not bb:raise RuntimeError(spec['id'])
  im=im.crop(bb)
  if spec.get('remove_ground_shadow'):
   ar=np.array(im);yy=np.arange(im.height)[:,None];mask=(yy>im.height*.91)&(ar[:,:,2]>ar[:,:,0]+5)&(ar[:,:,0]<110);ar[mask,3]=0;im=Image.fromarray(ar);im=im.crop(im.getchannel('A').getbbox())
  if spec.get('rotate'):im=im.rotate(spec['rotate'],expand=True,resample=Image.Resampling.NEAREST)
  body=spec['body']
  if spec.get('angle') is not None:
   pts=np.argwhere(np.array(im.getchannel('A'))>0)[:,::-1];cov=np.cov(pts.T);vals,vec=np.linalg.eigh(cov);v=vec[:,np.argmax(vals)];angle=math.degrees(math.atan2(v[1],v[0]));angle=(angle+90)%180-90
   im=im.rotate(angle-spec['angle'],expand=True,resample=Image.Resampling.NEAREST);im=im.crop(im.getchannel('A').getbbox());im=ImageOps.contain(im,tuple(body),Image.Resampling.NEAREST)
   fitted=Image.new('RGBA',tuple(body));fitted.alpha_composite(im,((body[0]-im.width)//2,(body[1]-im.height)//2));im=fitted
  else:im=im.resize(tuple(body),Image.Resampling.NEAREST)
  # Palette reduction is permitted pixel finishing, without new drawn content.
  alpha=im.getchannel('A');rgb=im.convert('RGB').quantize(colors=48,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB');im=rgb.convert('RGBA');im.putalpha(alpha)
  canvas=Image.new('RGBA',(body[0]+24,body[1]+24));canvas.alpha_composite(im,(12,12));canvas.save(dest/'final.png')
  (dest/raw.name).write_bytes(raw.read_bytes())
  (dest/'prompt.md').write_text((jp.parent/'prompt.txt').read_text()+'\n\nOrdered references:\n'+'\n'.join(str(x) for x in refs)+'\n\nRoute: built-in image_gen / art_source host_image. Raw SHA256 '+sha(raw)+'\nOwnership box '+str(spec['box'])+'\n')
  slice_=spec.get('slice');size=canvas.size
  if slice_:
   proof=Image.new('RGB',(max(size[0],int(size[0]*1.5))+32,size[1]*3+80),(232,228,216));d=ImageDraw.Draw(proof)
   for k,scale in enumerate((1,1.5)):
    stretched=stretch(canvas,(int(size[0]*scale),int(size[1]*(1 if k==0 else 1.4))),slice_)
    proof.paste(stretched,(16,24+k*(size[1]+40)),stretched)
   proof.save(dest/'stretch-preview.png')
  bb=canvas.getchannel('A').getbbox();m=[bb[0],bb[1],size[0]-bb[2],size[1]-bb[3]];colors=len({p[:3] for p in canvas.getdata() if p[3]})
  qa={'mode':'RGBA','alpha_margins':m,'colors':colors,'binary_alpha':True,'raw_byte_identical':sha(dest/raw.name)==sha(raw),'failures':[],'warnings':spec.get('warnings',[]),'stretch_preview_created':bool(slice_)}
  if min(m)<8:qa['failures'].append('alpha_margin_8')
  write(dest/'qa.json',qa)
  (dest/'review.md').write_text('# Source identity\n\n'+job['source_card']+'\n\nExport '+spec['id']+': '+spec.get('identity',spec['id'])+'.\n\nTransform: reviewed ownership crop; binary alpha threshold160; nearest size normalization to @3x body dimensions; <=48 color finish;12px alpha border. No new artwork drawn in code.\n\n'+('9-slice stretch preview generated for inspection. ' if slice_ else '')+'Owner approval pending; source identity and pixel style are draft review candidates.\n'+'\n'.join(spec.get('warnings',[])))
  preview=Image.new('RGB',(size[0]*3+48,size[1]*3+72),(40,44,52));d=ImageDraw.Draw(preview)
  for k,scale in enumerate((1,2)):
   pic=canvas.resize((size[0]*scale,size[1]*scale),Image.Resampling.NEAREST)
   # Game size is @1/3 source; previews additionally show source1x/2x.
   x=16 if k==0 else size[0]+32;y=24
   bg=Image.new('RGB',pic.size,(237,232,219) if k==0 else (19,24,32));bg.paste(pic,(0,0),pic);preview.paste(bg,(x,y));d.text((x,4),str(scale)+'x',fill='white')
  preview.save(dest/'review-light-dark.png')
  records.append({'id':spec['id'],'category':'ui_9slice' if slice_ else 'ui_sprite','kit':job.get('kit','world-hud'),'file':spec['id']+'/final.png','px':list(size),'world':None,'logical_body':[v/3 for v in body],'ui_scale':3,'pivot':'center','tileable':'none','slice':slice_,'frames':1,'fps':None,'sway':False,'source_refs':job['refs'],'replaces':spec.get('replaces'),'approved':False,'status':'needs_owner_review','mechanical_status':'pass' if not qa['failures'] else 'blocked','art_source':'host_image','route':'built-in image_gen','source_job':jp.parent.name,'source_box':spec['box'],'sha256':sha(dest/'final.png'),'notes':spec.get('notes','Blank labels rendered by engine. Draft only; not activated.')})
write(ROOT/'manifest.json',{'batch':ROOT.name,'approved':False,'status':'draft_review','assets':records})
cols=4;cw=340;ch=225;contact=Image.new('RGB',(cols*cw,50+((len(records)+3)//4)*ch),(30,34,43));d=ImageDraw.Draw(contact);d.text((16,16),ROOT.name+' / DRAFT / OWNER APPROVAL PENDING',fill='white')
for i,r in enumerate(records):
 im=Image.open(ROOT/r['file']);im=ImageOps.contain(im,(cw-24,ch-50),Image.Resampling.NEAREST);x=i%cols*cw;y=i//cols*ch+50;contact.paste(im,(x+12,y),im);d.text((x+12,y+ch-32),r['id'],fill='white')
contact.save(ROOT/'contact-sheet.png')
write(ROOT/'qa-summary.json',{'count':len(records),'mechanical_pass':sum(r['mechanical_status']=='pass' for r in records),'owner_approved':0,'warning':'Generated UI has richer surface texture than ideal flat centers. Review stretch previews before integration.'})
print(json.dumps({'batch':ROOT.name,'count':len(records)}))
