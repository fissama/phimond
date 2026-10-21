"""Crop actual host-generated artwork; preserve raw bytes and provenance. No artwork drawing."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil,sys
import numpy as np
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def package(root):
 records=[]
 for jf in sorted((root/'jobs').glob('*/job.json')):
  job=json.loads(jf.read_text());raw=jf.parent/job.get('selected_raw','raw-01.png')
  if not raw.exists():continue
  atlas=Image.open(raw).convert('RGBA');cols=job['cols'];rows=job['rows']
  for i,spec in enumerate(job['assets']):
   if spec is None:continue
   dest=root/spec['id'];dest.mkdir(exist_ok=True)
   for attempt in jf.parent.glob('raw-*.png'):shutil.copyfile(attempt,dest/attempt.name)
   frames=spec.get('frames',1);parts=[];boxes=[]
   for f in range(frames):
    index=i*frames+f if frames>1 else i;row,col=divmod(index,cols)
    xb=job.get('x_bounds',[round(k*atlas.width/cols) for k in range(cols+1)]);yb=job.get('y_bounds',[round(k*atlas.height/rows) for k in range(rows+1)])
    box=spec.get('source_boxes',[])[f] if spec.get('source_boxes') else [xb[col],yb[row],xb[col+1],yb[row+1]]
    part=atlas.crop(box);a=np.array(part)
    # Native transparency is kept. Flat chroma is removed only when explicitly requested in job.
    if job.get('key'):
     key=np.array(job['key']);delta=np.max(np.abs(a[:,:,:3].astype(int)-key),axis=2);mask=delta<45
     if job.get('despill_magenta',True):mask|=(a[:,:,0]>170)&(a[:,:,2]>130)&(a[:,:,1]<95)
     a[:,:,3][mask]=0;part=Image.fromarray(a)
    if job.get('alpha_floor'):
     a=np.array(part);a[:,:,3][a[:,:,3]<job['alpha_floor']]=0;part=Image.fromarray(a)
    if frames==1:
     bb=part.getchannel('A').getbbox()
     if bb:part=part.crop(bb)
     target=tuple(spec.get('px',[256,256]));factor=min((target[0]-32)/part.width,(target[1]-32)/part.height)
     part=part.resize((max(1,round(part.width*factor)),max(1,round(part.height*factor))),Image.Resampling.NEAREST)
     canvas=Image.new('RGBA',target);canvas.alpha_composite(part,((target[0]-part.width)//2,target[1]-16-part.height if spec.get('category')=='font' else (target[1]-part.height)//2));part=canvas
    else:
     size=spec.get('cell',192);maxw=max(xb[k+1]-xb[k] for k in range(cols));maxh=max(yb[k+1]-yb[k] for k in range(rows));factor=(size-32)/max(maxw,maxh);part=part.resize((round(part.width*factor),round(part.height*factor)),Image.Resampling.NEAREST);canvas=Image.new('RGBA',(size,size));canvas.alpha_composite(part,((size-part.width)//2,(size-part.height)//2));part=canvas
    parts.append(part);boxes.append(box)
   final=Image.new('RGBA',(parts[0].width*frames,parts[0].height))
   for f,part in enumerate(parts):final.alpha_composite(part,(f*part.width,0))
   final.save(dest/'final.png');refs=[{'path':p,'sha256':sha(p)} for p in job['refs']]
   original_refs=[{'path':p,'sha256':sha(p)} for p in job.get('original_refs',job['refs'])]
   provenance={'route':'built-in image_gen','model_returned':None,'estimate_usd':None,'selected_raw':raw.name,'attempts':[{'file':p.name,'sha256':sha(p),'prompt':job.get('original_prompt',job['prompt']) if p.name=='raw-01.png' else job['prompt'],'ordered_references':original_refs if p.name=='raw-01.png' else refs} for p in sorted(jf.parent.glob('raw-*.png'))]}
   write(dest/'provenance.json',provenance)
   (dest/'prompt.md').write_text(('Attempt1 original prompt:\n'+job['original_prompt']+'\n\n' if job.get('original_prompt') else '')+'Selected prompt:\n'+job['prompt']+'\n\nSelected ordered references:\n'+'\n'.join(f"{n+1}. {r['path']} sha256={r['sha256']}" for n,r in enumerate(refs))+'\n\nRoute: built-in image_gen; model not exposed; cost unknown.\nRaw SHA256: '+sha(raw)+'\nFull per-attempt provenance: provenance.json\n')
   qa={'failures':[],'warnings':[],'source_boxes':boxes,'margins':[]}
   for part in parts:
    bb=part.getchannel('A').getbbox();m=[bb[0],bb[1],part.width-bb[2],part.height-bb[3]] if bb else [0]*4;qa['margins'].append(m)
    if min(m)<8:qa['failures'].append('alpha_margin_below_8')
    if not bb:qa['failures'].append('empty_frame')
   if frames>1:
    qa['warnings'].append('Animation phase progression and pivot require owner/in-engine review; grid registration preserved, not independently bbox-centered.')
    previews=[]
    for p in parts:
     bg=Image.new('RGBA',p.size,(33,37,43,255));bg.alpha_composite(p);previews.append(bg.convert('RGB'))
    previews[0].save(dest/'preview.gif',save_all=True,append_images=previews[1:],duration=1000//spec.get('fps',10),loop=0)
   write(dest/'qa.json',qa)
   (dest/'review.md').write_text('# Source identity\n\n'+spec.get('identity',spec['id'])+'\n\n'+job.get('source_card','Original motif references and runtime IDs; semantic redesign where no one-to-one historic mapping is proven.')+'\n\nMechanical failures: '+str(qa['failures'])+'\nWarnings: '+str(qa['warnings'])+'\n\nDraft, approved:false. Visual review performed on generated sheet; per-icon owner review and engine validation remain. No runtime activation.\n')
   w,h=parts[0].size;records.append({'id':spec['id'],'category':spec.get('category','icon'),'kit':spec.get('kit',job.get('kit','icons')),'file':spec['id']+'/final.png','px':list(final.size),'frame_px':[w,h],'world':[w/128,h/128],'pivot':'center','pivot_px':[w/2,h/2],'tileable':'none','slice':spec.get('slice'),'frames':frames,'fps':spec.get('fps'),'sway':False,'source_refs':job['refs'],'replaces':spec.get('replaces'),'approved':False,'status':'blocked' if qa['failures'] else 'needs_owner_review','mechanical_status':'fail' if qa['failures'] else 'pass','source_job':job['id'],'raw_sha256':sha(raw),'sha256':sha(dest/'final.png'),'route':'built-in image_gen','notes':spec.get('notes','Draft art; owner approval pending.'),'content_id':spec.get('content_id')})
 write(root/'manifest.json',{'approved':False,'route':'built-in image_gen','assets':records})
 n=len(records);contact=Image.new('RGB',(1000,max(1,(n+7)//8)*140),(40,43,49));d=ImageDraw.Draw(contact)
 for i,r in enumerate(records):
  im=Image.open(root/r['file']);im=im.crop((0,0,r['frame_px'][0],r['frame_px'][1]));im.thumbnail((100,100),Image.Resampling.NEAREST);x=(i%8)*125;y=(i//8)*140;contact.paste(im,(x+(125-im.width)//2,y),im);d.text((x,y+102),r['id'][:20],fill='white')
 contact.save(root/'contact-sheet.png')
 # Game-size samples over light and dark, exactly32px and64px.
 preview=Image.new('RGB',(768,max(1,(n+5)//6)*112),(230,225,211));d=ImageDraw.Draw(preview)
 for i,r in enumerate(records):
  p=Image.open(root/r['file']).crop((0,0,*r['frame_px']));x=i%6*128;y=i//6*112
  preview.paste(p.resize((32,32),Image.Resampling.NEAREST),(x,y),p.resize((32,32),Image.Resampling.NEAREST));dark=Image.new('RGB',(64,64),(26,29,36));p=p.resize((64,64),Image.Resampling.NEAREST);dark.paste(p,(0,0),p);preview.paste(dark,(x+40,y));d.text((x,y+72),r['id'][:20],fill=(25,25,25))
 preview.save(root/'game-size-light-dark.png')
 print(json.dumps({'root':str(root),'assets':n,'blocked':[r['id'] for r in records if r['mechanical_status']=='fail']}))
if __name__=='__main__':
 root=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT
 package(root)
 if root.name=='batch-07-octopath' and (root/'refine_ui.py').exists():
  import subprocess
  subprocess.run([sys.executable,str(root/'refine_ui.py')],check=True)
