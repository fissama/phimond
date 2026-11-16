"""Crop/key/palette generated raster art; preview composition only, never draws content."""
from pathlib import Path
import sys,json,hashlib,shutil
from PIL import Image,ImageDraw
import numpy as np
R=Path(__file__).resolve().parent
sys.path.insert(0,'/Users/phileanh/.codex/skills/generate2dmap/scripts')
from extract_prop_pack import key_sheet

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o):Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def bg(im,scale=1,dark=False):
 pic=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
 if dark:b=Image.new('RGBA',pic.size,(22,27,34,255))
 else:
  y,x=np.indices((pic.height,pic.width));v=np.where((x//(16*scale)+y//(16*scale))%2,65,94).astype('uint8');b=Image.fromarray(np.repeat(v[:,:,None],3,2)).convert('RGBA')
 b.alpha_composite(pic);return b.convert('RGB')
def fit(im,size,margin=16):
 out=Image.new('RGBA',tuple(size));bw,bh=size[0]-margin*2,size[1]-margin*2;s=min(bw/im.width,bh/im.height)
 n=im.resize((max(1,round(im.width*s)),max(1,round(im.height*s))),Image.Resampling.NEAREST)
 out.alpha_composite(n,((size[0]-n.width)//2,(size[1]-n.height)//2));return out

def nine(im,slices,size):
 l,t,r,b=slices;w,h=im.size;ow,oh=size
 xs=[0,l,w-r,w];ys=[0,t,h-b,h];dx=[0,l,ow-r,ow];dy=[0,t,oh-b,oh]
 out=Image.new('RGBA',size)
 for row in range(3):
  for col in range(3):
   tile=im.crop((xs[col],ys[row],xs[col+1],ys[row+1]));tile=tile.resize((dx[col+1]-dx[col],dy[row+1]-dy[row]),Image.Resampling.NEAREST);out.alpha_composite(tile,(dx[col],dy[row]))
 return out
jobname=sys.argv[1];J=R/'jobs'/jobname;job=json.loads((J/'job.json').read_text());man=json.loads((R/'manifest.json').read_text());records={a['id']:a for a in man['assets']}
for sp in job['assets']:
 d=R/sp['id'];d.mkdir(exist_ok=True);raw=J/sp.get('raw',job['raw']);im=Image.open(raw).convert('RGBA').crop(tuple(sp['box']))
 if sp.get('opaque'):keyed=im
 else:
  aa,report=key_sheet(np.asarray(im),'chroma_key',100,150,2);keyed=Image.fromarray(aa)
  bbox=keyed.getbbox()
  if not bbox:raise RuntimeError('EMPTY '+sp['id'])
  keyed=keyed.crop(bbox)
 keyed.save(d/'keyed-source.png');alpha=keyed.getchannel('A')
 # Nondithered palette reduction is the only color operation. No geometric cleanup/repaint.
 arr=np.asarray(keyed);visible=arr[:,:,3]>0;pixels=arr[:,:,:3][visible];budget=sp.get('colors',48)
 greens=(pixels[:,1].astype(int)>pixels[:,0].astype(int)+25)&(pixels[:,1].astype(int)>=pixels[:,2].astype(int)-20)
 reserve=4 if sp.get('reserve_jade') and greens.any() else 0
 sample=Image.fromarray(pixels.reshape(1,-1,3));qp=sample.quantize(colors=budget-reserve,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE);base=qp.getpalette();idx=sorted(set(qp.get_flattened_data()));colors=[tuple(base[i*3:i*3+3]) for i in idx]
 if reserve:
  gp=Image.fromarray(pixels[greens].reshape(1,-1,3)).quantize(colors=reserve,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE);gpal=gp.getpalette();colors += [tuple(gpal[i*3:i*3+3]) for i in sorted(set(gp.get_flattened_data()))]
 if job.get('shared_palette'):
  shared=J/'shared-palette.json'
  if shared.exists():colors=[tuple(c) for c in json.loads(shared.read_text())]
  else:write(shared,colors)
 if sp.get('palette_sources'):
  full=[];groups=[]
  for src in sp['palette_sources']:
   values=json.loads((R/src['file']).read_text())['colors'];cs=[tuple(bytes.fromhex((v['hex'] if isinstance(v,dict) else v)[1:])) for v in values];groups.append((src,cs));full.extend(cs)
  pre=Image.new('P',(1,1));preflat=[v for c in full for v in c];pre.putpalette(preflat+preflat[:3]*(256-len(full)))
  mapped=sample.quantize(palette=pre,dither=Image.Dither.NONE);counts={idx:count for count,idx in mapped.getcolors()};colors=[];off=0
  for src,cs in groups:
   ranked=sorted(range(len(cs)),key=lambda i:counts.get(off+i,0),reverse=True);colors.extend(cs[i] for i in ranked[:src['count']]);off+=len(cs)
 palette=Image.new('P',(1,1));colors=list(dict.fromkeys(colors));flat=[v for c in colors for v in c];palette.putpalette(flat+flat[:3]*(256-len(colors)))
 # Exact nearest palette mapping avoids Pillow15-bit cache merging nearby palette entries.
 ka=np.asarray(keyed);flatpixels=ka[:,:,:3].reshape(-1,3).astype(np.int32);cs=np.array(colors,dtype=np.int32);out=np.empty_like(flatpixels,dtype=np.uint8)
 for start in range(0,len(flatpixels),8192):
  dist=((flatpixels[start:start+8192,None,:]-cs[None,:,:])**2).sum(axis=2);out[start:start+8192]=cs[dist.argmin(axis=1)]
 ka=ka.copy();ka[:,:,:3]=out.reshape(ka.shape[:2]+(3,));ka[ka[:,:,3]==0,:3]=0;pal=Image.fromarray(ka)
 write(d/'palette.json',{'source':str(raw),'raw_sha256':sha(raw),'colors':['#%02x%02x%02x'%c for c in colors],'method':'visible pixel median-cut; jade ramp reserved from generated jade pixels when requested'})
 size=sp.get('master_size',sp['size'])
 if sp.get('opaque') or sp.get('stretch'):master=pal.resize(tuple(size),Image.Resampling.NEAREST)
 else:master=fit(pal,size,sp.get('margin',16 if not sp.get('master_size') else 48))
 if sp.get('master_size'):master.save(d/'master-1024.png')
 final=master.resize(tuple(sp['size']),Image.Resampling.NEAREST);final.save(d/'final.png')
 # Preserve every raw source byte-identically and exact ordered reference hashes.
 for rp in J.glob('raw-*.png'):shutil.copyfile(rp,d/rp.name)
 prompt=f"# {sp['id']}\n\nRoute: built-in image_gen. Model not exposed.\n\n{job['prompt']}\n\nActual attachments (ordered):\n"
 prompt+='\n'.join(f"{i+1}. {r['path']} — SHA256 {r['sha256']}" for i,r in enumerate(job['refs']))
 prompt+=f"\n\nRaw: {raw.name}; SHA256 {sha(raw)}; source box {sp['box']}. Final {sp['size']}. Non-dithered {sp.get('colors',48)}color finish, nearest scaling. No content drawn with code.\n"
 (d/'prompt.md').write_text(prompt)
 a=np.asarray(final);vis=a[:,:,3]>0;ys,xs=np.where(vis);rgb=a[:,:,:3].astype(int);key=vis&(rgb[:,:,0]>200)&(rgb[:,:,2]>200)&(rgb[:,:,1]<80)
 q={'id':sp['id'],'size':list(final.size),'mode':final.mode,'colors':len(np.unique(a[:,:,:3][vis],axis=0)),'partial_alpha_pixels':int(((a[:,:,3]>0)&(a[:,:,3]<255)).sum()),'key_residue_pixels':int(key.sum()),'margin':int(min(xs.min(),ys.min(),final.width-1-xs.max(),final.height-1-ys.max())),'raw_integrity':sha(d/raw.name)==sha(raw),'sha256':sha(d/'final.png'),'visual_review':'pending_actual_4x_inspection','failures':[]}
 if q['colors']>sp.get('colors',48):q['failures'].append('COLORS')
 if q['partial_alpha_pixels']:q['failures'].append('SEMI_ALPHA')
 if q['key_residue_pixels']:q['failures'].append('CHROMA')
 if not sp.get('opaque') and sp.get('tileable') not in ('x','xy') and q['margin']<8:q['failures'].append('MARGIN')
 write(d/'qa.json',q)
 for dark,label in [(True,'dark'),(False,'checker')]:
  bg(final,4,dark).save(d/f'review-4x-{label}.png')
  box=sp.get('review_crop',[max(0,final.width//2-192),max(0,final.height//2-128),min(final.width,final.width//2+192),min(final.height,final.height//2+128)])
  bg(final.crop(tuple(box)),4,dark).save(d/f'detail-4x-{label}.png')
 if sp.get('slice'):
  ds=[]
  for k,sz in enumerate([(384,480),(640,480),(960,640)]):
   pic=nine(final,sp['slice'],sz);bg(pic).save(d/f'nine-slice-{sz[0]}x{sz[1]}.png');ds.append({'size':list(sz),'file':f'nine-slice-{sz[0]}x{sz[1]}.png'})
  write(d/'nine-slice-qa.json',{'slice':sp['slice'],'renders':ds,'visual_review':'pending'})
 rec={'id':sp['id'],'category':sp['category'],'kit':jobname,'file':sp['id']+'/final.png','px':sp['size'],'size_px':sp['size'],'world':None if sp['category'].startswith('ui') or sp['category']=='icon' else [sp['size'][0]/128,sp['size'][1]/128],'world_size':None,'pivot':'center','pivot_px':[sp['size'][0]//2,sp['size'][1]//2],'pivot_uv':[.5,.5],'tileable':sp.get('tileable','none'),'slice':sp.get('slice'),'frames':sp.get('frames',1),'frame_px':sp.get('frame_px'),'fps':sp.get('fps'),'sway':False,'art_source':'host_image','route':'built-in image_gen','source_refs':[r['path'] for r in job['refs']],'source_raw':raw.name,'raw_sha256':sha(raw),'sha256':sha(d/'final.png'),'source_box':sp['box'],'approved':False,'status':'needs_claude_visual_review','mechanical_status':'blocked' if q['failures'] else 'pass','ui_scale':3 if sp['category'].startswith('ui') else None}
 if sp.get('master_size'):rec['master_file']=sp['id']+'/master-1024.png'
 if rec['world']:rec['world_size']=rec['world']
 records[sp['id']]=rec
 print(sp['id'],q['colors'],'colors',q['failures'])
man['assets']=list(records.values());man['stage']='continuous-redraw';man['status']='in_progress_needs_claude_visual_review';write(R/'manifest.json',man)
# QA contact sheet only; labels/checker are not exported game art.
W,H=640,400;N=len(records);sheet=Image.new('RGB',(W*2,H*((N+1)//2)),(23,28,37));dr=ImageDraw.Draw(sheet)
for i,rec in enumerate(records.values()):
 x=(i%2)*W;y=(i//2)*H;im=Image.open(R/rec['file']).convert('RGBA');thumb=fit(im,[W,340],16);sheet.paste(bg(thumb),(x,y+30));dr.text((x+12,y+8),rec['id']+' / draft',fill=(235,230,210))
sheet.save(R/'contact-sheet.png');job['state']='exported_pending_visual_review';write(J/'job.json',job)
