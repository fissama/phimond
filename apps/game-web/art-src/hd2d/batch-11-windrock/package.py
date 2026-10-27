"""Crop/key/palette generated raster art; preview composition only, never draws content."""
from pathlib import Path
import sys,json,hashlib,shutil
from PIL import Image,ImageDraw
import numpy as np
R=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else Path(__file__).resolve().parent
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
jobname=sys.argv[1];J=R/'jobs'/jobname;job=json.loads((J/'job.json').read_text());man=json.loads((R/'manifest.json').read_text()) if (R/'manifest.json').exists() else {'batch':'batch-11-windrock','approved':False,'assets':[]};records={a['id']:a for a in man['assets']}
for sp in job['assets']:
 d=R/sp['id'];d.mkdir(exist_ok=True);raw=J/sp.get('raw',job['raw']);im=Image.open(raw).convert('RGBA').crop(tuple(sp['box']))
 if sp.get('native_alpha'):
  keyed=im
  bbox=keyed.getbbox()
  if not bbox:raise RuntimeError('EMPTY NATIVE ALPHA '+sp['id'])
  keyed=keyed if sp.get('keep_source_box') else keyed.crop(bbox)
 elif sp.get('opaque'):keyed=im
 else:
  aa,report=key_sheet(np.asarray(im),'chroma_key',100,150,2);keyed=Image.fromarray(aa)
  if sp.get('crop_polygon'):
   selection=Image.new('L',keyed.size,0);ImageDraw.Draw(selection).polygon([tuple(p) for p in sp['crop_polygon']],fill=255)
   ka=np.asarray(keyed).copy();ka[:,:,3]=np.minimum(ka[:,:,3],np.asarray(selection));keyed=Image.fromarray(ka)
  if sp.get('extraction_alpha_mask'):
   stencil=Image.open(sp['extraction_alpha_mask'])
   stencil=stencil.getchannel('A') if stencil.mode=='RGBA' else stencil.convert('L')
   if stencil.size!=keyed.size:raise RuntimeError('CUTTING STENCIL SIZE MISMATCH '+sp['id'])
   ka=np.asarray(keyed).copy();ka[:,:,3]=np.minimum(ka[:,:,3],np.asarray(stencil));keyed=Image.fromarray(ka)
  bbox=keyed.getbbox()
  if not bbox:raise RuntimeError('EMPTY '+sp['id'])
  keyed=keyed if sp.get('keep_source_box') else keyed.crop(bbox)
 if sp.get('source_registration'):
  reg=sp['source_registration'];dx,dy=reg['translate'];cw,ch=reg['canvas'];bounds=keyed.getbbox()
  if bounds and (bounds[0]+dx<0 or bounds[1]+dy<0 or bounds[2]+dx>cw or bounds[3]+dy>ch):raise RuntimeError('REGISTRATION WOULD CLIP VISIBLE PIXELS '+sp['id'])
  registered=Image.new('RGBA',(cw,ch));registered.alpha_composite(keyed,(dx,dy));keyed=registered
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
 if job.get('palette_source'):
  colors=[tuple(bytes.fromhex(c['hex'][1:])) for c in json.loads((R/job['palette_source']).read_text())['colors']]
 if sp.get('palette_sources'):
  full=[];groups=[]
  for src in sp['palette_sources']:
   values=json.loads((R/src['file']).read_text())['colors'];cs=[tuple(bytes.fromhex((v['hex'] if isinstance(v,dict) else v)[1:])) for v in values];groups.append((src,cs));full.extend(cs)
  pre=Image.new('P',(1,1));preflat=[v for c in full for v in c];pre.putpalette(preflat+preflat[:3]*(256-len(full)))
  mapped=sample.quantize(palette=pre,dither=Image.Dither.NONE);counts={idx:count for count,idx in mapped.getcolors()};colors=[];off=0
  for src,cs in groups:
   ranked=sorted(range(len(cs)),key=lambda i:counts.get(off+i,0),reverse=True);colors.extend(cs[i] for i in ranked[:src['count']]);off+=len(cs)
 palette=Image.new('P',(1,1));colors=list(dict.fromkeys(colors));flat=[v for c in colors for v in c];palette.putpalette(flat+flat[:3]*(256-len(colors)))
 # Per-material palette subset, global color mapping only. No spatial edge painting.
 if sp.get('base_palette_filter'):
  rule=sp['base_palette_filter'];base=tuple(bytes.fromhex(rule['hex'][1:]));colors=[c for c in colors if c==base or sum((v-b)**2 for v,b in zip(c,base))>rule['radius']**2]
  if base not in colors:colors.append(base)
 if sp.get('palette_include'):
  allowed={tuple(bytes.fromhex(h[1:])) for h in sp['palette_include']};colors=[c for c in colors if c in allowed]
 if sp.get('palette_exclude'):
  excluded={tuple(bytes.fromhex(h[1:])) for h in sp['palette_exclude']};colors=[c for c in colors if c not in excluded]
 # Exact nearest palette mapping avoids Pillow15-bit cache merging nearby palette entries.
 ka=np.asarray(keyed);flatpixels=ka[:,:,:3].reshape(-1,3).astype(np.int32);cs=np.array(colors,dtype=np.int32);out=np.empty_like(flatpixels,dtype=np.uint8)
 for start in range(0,len(flatpixels),8192):
  dist=((flatpixels[start:start+8192,None,:]-cs[None,:,:])**2).sum(axis=2);out[start:start+8192]=cs[dist.argmin(axis=1)]
 if sp.get('palette_remap'):
  aliases={tuple(bytes.fromhex(k[1:])):tuple(bytes.fromhex(v[1:])) for k,v in sp['palette_remap'].items()}
  original=out.copy()
  for src,dst in aliases.items():out[np.all(original==src,axis=1)]=dst
  colors=list(dict.fromkeys(aliases.get(c,c) for c in colors))
 ka=ka.copy();ka[:,:,:3]=out.reshape(ka.shape[:2]+(3,));ka[ka[:,:,3]==0,:3]=0;pal=Image.fromarray(ka)
 write(d/'palette.json',{'source':str(raw),'raw_sha256':sha(raw),'colors':['#%02x%02x%02x'%c for c in colors],'method':'exact nearest kit palette mapping; optional global material subset only' if job.get('palette_source') else 'visible pixel median-cut'})
 size=sp.get('master_size',sp['size'])
 if sp.get('native_pixels'):
  if sp.get('master_size'):raise RuntimeError('NATIVE PROP CANNOT USE RESAMPLED MASTER '+sp['id'])
  desired=sp.get('desired_world_size')
  if not desired or any(abs(desired[i]*128-size[i])>1e-6 for i in range(2)):raise RuntimeError('NATIVE PROP WORLD SIZE NOT PREDECLARED '+sp['id'])
  pb=pal.getbbox()
  if not pb or pal.width>size[0] or pal.height>size[1] or pb[2]-pb[0]>size[0]-16 or pb[3]-pb[1]>size[1]-16:raise RuntimeError('NATIVE PROP EXCEEDS PIXEL BUDGET; REDRAW, DO NOT SHRINK '+sp['id'])
  master=Image.new('RGBA',tuple(size));master.alpha_composite(pal,((size[0]-pal.width)//2,(size[1]-pal.height)//2))
 elif sp.get('opaque') or sp.get('stretch'):master=pal.resize(tuple(size),Image.Resampling.NEAREST)
 else:master=fit(pal,size,sp.get('margin',16 if not sp.get('master_size') else 48))
 if sp.get('master_size'):master.save(d/'master-1024.png')
 final=master.copy() if sp.get('native_pixels') else master.resize(tuple(sp['size']),Image.Resampling.NEAREST);final.save(d/'final.png')
 # Preserve every raw source byte-identically and exact ordered reference hashes.
 if not (d/'raw-01.png').exists():shutil.copyfile(raw,d/'raw-01.png')
 for rp in J.glob('raw-*.png'):
  target=d/rp.name
  if target.exists() and sha(target)!=sha(rp):
   archived=d/(rp.stem+'-before-'+jobname+rp.suffix)
   if not archived.exists():shutil.copyfile(target,archived)
   if rp.name=='raw-01.png':continue
  shutil.copyfile(rp,target)
 selected_raw_name=raw.name
 if sha(d/raw.name)!=sha(raw):
  selected_raw_name=raw.stem+'-selected-'+jobname+raw.suffix
  shutil.copyfile(raw,d/selected_raw_name)
 prompt=f"# {sp['id']}\n\nRoute: built-in image_gen. Model not exposed.\n\n{job['prompt']}\n\nActual attachments (ordered):\n"
 prompt+='\n'.join(f"{i+1}. {r['path']} — SHA256 {r['sha256']}" for i,r in enumerate(job['refs']))
 if job.get('reference_montage_sources'):prompt+='\n\nQA reference montage contains these actual approved images (unmodified pixels, padding only):\n'+json.dumps(job['reference_montage_sources'],ensure_ascii=False,indent=2)
 if job.get('native_reference_source'):prompt+='\n\nNative guide source provenance:\n'+json.dumps(job['native_reference_source'],ensure_ascii=False,indent=2)
 if job.get('native_reference_sources'):prompt+='\n\nNative guide source provenance (snapshots retained):\n'+json.dumps(job['native_reference_sources'],ensure_ascii=False,indent=2)
 scaling='native1:1 pixel copy and transparent padding; NO resampling' if sp.get('native_pixels') else 'nearest scaling'
 prompt+=f"\n\nRaw: {selected_raw_name}; SHA256 {sha(raw)}; source box {sp['box']}; sheet extraction polygon {sp.get('crop_polygon')}; translation-only source registration {sp.get('source_registration')}. Final {sp['size']}. Non-dithered {sp.get('colors',48)}color finish, {scaling}. No content drawn with code.\n"
 if sp.get('extraction_alpha_mask'):prompt+=f"\nCutting stencil only: {sp['extraction_alpha_mask']}; SHA256 {sha(sp['extraction_alpha_mask'])}. Alpha intersection removes outside source pixels; no missing pixels filled or painted.\n"
 (d/'prompt.md').write_text(prompt)
 if sp.get('native_pixels'):
  with (d/'prompt.md').open('a') as pf:pf.write('\nNative scale: '+json.dumps({'desired_world_size_before_drawing':sp['desired_world_size'],'height_relative_to_player':sp.get('height_relative_to_player'),'source_footprint_px':list(pal.size),'resampling':'NONE; source pixels copied1:1, transparent padding only'},ensure_ascii=False)+'\n')
 a=np.asarray(final);vis=a[:,:,3]>0;ys,xs=np.where(vis);rgb=a[:,:,:3].astype(int);key=vis&(rgb[:,:,0]>200)&(rgb[:,:,2]>200)&(rgb[:,:,1]<80)
 q={'id':sp['id'],'size':list(final.size),'mode':final.mode,'colors':len(np.unique(a[:,:,:3][vis],axis=0)),'partial_alpha_pixels':int(((a[:,:,3]>0)&(a[:,:,3]<255)).sum()),'key_residue_pixels':int(key.sum()),'margin':int(min(xs.min(),ys.min(),final.width-1-xs.max(),final.height-1-ys.max())),'raw_integrity':sha(d/selected_raw_name)==sha(raw),'sha256':sha(d/'final.png'),'visual_review':'pending_actual_4x_inspection','failures':[]}
 if q['colors']>sp.get('colors',48):q['failures'].append('COLORS')
 if q['colors']<33 and sp['category']!='shadow':q['failures'].append('COLORS_BELOW33')
 if q['partial_alpha_pixels'] and not(sp['category']=='shadow' and sp.get('allow_soft_alpha')):q['failures'].append('SEMI_ALPHA')
 if sp.get('exception'):q['documented_exception']=sp['exception']
 q['alpha_max']=int(a[:,:,3].max())
 if q['key_residue_pixels']:q['failures'].append('CHROMA')
 if not sp.get('opaque') and sp.get('tileable') not in ('x','xy') and q['margin']<8:q['failures'].append('MARGIN')
 if sp.get('tileable') in ('xy','x'):
  rgb=a[:,:,:3].astype(int);q['seam_x_mean']=float(abs(rgb[:,0]-rgb[:,-1]).mean());q['seam_x_max']=int(abs(rgb[:,0]-rgb[:,-1]).max())
  if sp['tileable']=='xy':q['seam_y_mean']=float(abs(rgb[0]-rgb[-1]).mean());q['seam_y_max']=int(abs(rgb[0]-rgb[-1]).max())
  q['outer8_uniform']=bool((rgb[:8]==rgb[0,0]).all() and (rgb[-8:]==rgb[0,0]).all() and (rgb[:,:8]==rgb[0,0]).all() and (rgb[:,-8:]==rgb[0,0]).all()) if sp['tileable']=='xy' else None
  repeat=Image.new('RGBA',(final.width*3,final.height*(3 if sp['tileable']=='xy' else 1)))
  for ry in range(3 if sp['tileable']=='xy' else 1):
   for rx in range(3):repeat.alpha_composite(final,(rx*final.width,ry*final.height))
  bg(repeat).save(d/'repeat-3x3.png')
  if q['seam_x_max']!=0:q['failures'].append('SEAM_X_NONZERO')
  if sp['tileable']=='xy' and q['seam_y_max']!=0:q['failures'].append('SEAM_Y_NONZERO')
  if sp['tileable']=='xy' and not q['outer8_uniform']:q['failures'].append('OUTER8_NOT_FLAT')
 write(d/'qa.json',q)
 with (d/'prompt.md').open('a') as pf:pf.write('\nFinish details: '+json.dumps({'visible_colors':q['colors'],'palette_source':job.get('palette_source'),'palette_include':sp.get('palette_include'),'palette_exclude':sp.get('palette_exclude'),'palette_remap':sp.get('palette_remap'),'base_palette_filter':sp.get('base_palette_filter'),'native_alpha':sp.get('native_alpha',False),'documented_exception':sp.get('exception'),'job_palette_note':job.get('palette_finish_note')},ensure_ascii=False)+'\n')
 for dark,label in [(True,'dark'),(False,'checker')]:
  bg(final,4,dark).save(d/f'review-4x-{label}.png')
  box=sp.get('review_crop',[max(0,final.width//2-192),max(0,final.height//2-128),min(final.width,final.width//2+192),min(final.height,final.height//2+128)])
  bg(final.crop(tuple(box)),4,dark).save(d/f'detail-4x-{label}.png')
 if sp.get('slice'):
  ds=[]
  for k,sz in enumerate([(384,480),(640,480),(960,640)]):
   pic=nine(final,sp['slice'],sz);bg(pic).save(d/f'nine-slice-{sz[0]}x{sz[1]}.png');ds.append({'size':list(sz),'file':f'nine-slice-{sz[0]}x{sz[1]}.png'})
  write(d/'nine-slice-qa.json',{'slice':sp['slice'],'renders':ds,'visual_review':'pending'})
 rec={'id':sp['id'],'category':sp['category'],'kit':jobname,'file':sp['id']+'/final.png','px':sp['size'],'size_px':sp['size'],'world':None if sp['category'].startswith('ui') or sp['category']=='icon' else [sp['size'][0]/(64 if sp['category']=='backdrop_far' else 128),sp['size'][1]/(64 if sp['category']=='backdrop_far' else 128)],'world_size':None,'pivot':'bottom-center' if sp['category'] in ('prop','decal','marker') else 'center','pivot_px':[sp['size'][0]//2,int(ys.max()+1) if sp['category'] in ('prop','decal','marker') else sp['size'][1]//2],'pivot_uv':[.5,float(ys.max()+1)/sp['size'][1] if sp['category'] in ('prop','decal','marker') else .5],'tileable':sp.get('tileable','none'),'slice':sp.get('slice'),'frames':sp.get('frames',1),'frame_px':sp.get('frame_px'),'fps':sp.get('fps'),'sway':False,'art_source':'host_image','route':'built-in image_gen','source_refs':[r['path'] for r in job['refs']],'source_raw':selected_raw_name,'raw_sha256':sha(raw),'sha256':sha(d/'final.png'),'source_box':sp['box'],'approved':False,'status':'needs_claude_visual_review','mechanical_status':'blocked' if q['failures'] else 'pass','ui_scale':3 if sp['category'].startswith('ui') else None}
 if sp.get('master_size'):rec['master_file']=sp['id']+'/master-1024.png'
 if sp.get('native_pixels'):rec['native_scale']={'desired_world_size_before_drawing':sp['desired_world_size'],'source_footprint_px':list(pal.size),'resampled':False}
 if rec['world']:rec['world_size']=rec['world']
 if sp.get('exception'):rec['documented_exception']=sp['exception']
 if sp.get('map_id'):rec['map_id']=sp['map_id']
 if sp.get('content_provenance'):rec['content_provenance']=sp['content_provenance']
 records[sp['id']]=rec
 print(sp['id'],q['colors'],'colors',q['failures'])
man['assets']=list(records.values());man['stage']='continuous-redraw';man['status']='in_progress_needs_claude_visual_review';write(R/'manifest.json',man)
# QA contact sheet only; labels/checker are not exported game art.
W,H=640,400;N=len(records);sheet=Image.new('RGB',(W*2,H*((N+1)//2)),(23,28,37));dr=ImageDraw.Draw(sheet)
for i,rec in enumerate(records.values()):
 x=(i%2)*W;y=(i//2)*H;im=Image.open(R/rec['file']).convert('RGBA');thumb=fit(im,[W,340],16);sheet.paste(bg(thumb),(x,y+30));dr.text((x+12,y+8),rec['id']+' / draft',fill=(235,230,210))
sheet.save(R/'contact-sheet.png');job['state']='exported_pending_visual_review';write(J/'job.json',job)
