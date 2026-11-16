"""Permitted alpha removal/cropping of generated HP pixels and actual 9patch proof layouts."""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,shutil
R=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
m=json.loads((R/'manifest.json').read_text())
for side,slot,extract in [('ally',[55,61,234,86],[65,62,178,85]),('enemy',[58,62,233,86],[66,62,151,86])]:
 ident='battle_hp_'+side;folder=R/ident;original=folder/'original-combined.png'
 if not original.exists():shutil.copyfile(folder/'final.png',original)
 src=Image.open(original).convert('RGBA');frame=src.copy();a=frame.load();l,t,r,b=slot
 # Remove only old slot pixels. Gold outer border and crest are retained.
 for y in range(t,b):
  for x in range(l,r):
   rr,gg,bb,aa=a[x,y];a[x,y]=(rr,gg,bb,0)
 frame.save(folder/'final.png')
 fillid=ident+'_fill';out=R/fillid;out.mkdir(exist_ok=True)
 for name in ['raw-01.png','raw-02.png','prompt.md','provenance.json']:
  if (folder/name).exists():shutil.copyfile(folder/name,out/name)
 patch=src.crop(extract).resize((r-l,b-t),Image.Resampling.NEAREST)
 fill=Image.new('RGBA',(((r-l+34)//3)*3,((b-t+34)//3)*3));fill.alpha_composite(patch,(16,16));fill.save(out/'final.png')
 rec=next(a for a in m['assets'] if a['id']==ident)
 rec.update(sha256=sha(folder/'final.png'),notes='Separated frame: previous generated HP fill and slot interior removed by alpha mask; matching independent fill asset '+fillid+'.',slot_rect=slot,fill_asset=fillid,fill_offset=[l-16,t-16],approved=False)
 new=dict(rec);new.update(id=fillid,file=fillid+'/final.png',px=list(fill.size),frame_px=list(fill.size),world=[fill.width/128,fill.height/128],pivot_px=[fill.width/2,fill.height/2],sha256=sha(out/'final.png'),slot_rect=None,fill_asset=None,fill_offset=None,content_rect=[16,16,16+r-l,16+b-t],notes='Independent full-width HP fill extracted from generated '+ident+' colored strip. Clip CONTENT width for HP ratio; register via frame.fill_offset. No new pixels drawn.',derived_from=ident+'/original-combined.png',source_crop=extract)
 m['assets']=[a for a in m['assets'] if a['id']!=fillid];m['assets'].append(new)
 qa={'failures':[],'warnings':['Original source shape and frame gap require in-engine manual validation.'],'method':'crop/nearest resize for fill; alpha-only slot background removal for frame','slot_rect':slot,'fill_source_crop':extract,'original_combined_sha256':sha(original)}
 write(folder/'hp-separation.json',qa);write(out/'qa.json',{'failures':[],'warnings':[],'margins':[[16,16,fill.width-16-patch.width,fill.height-16-patch.height]]})
 for target in [folder,out]:
  provenance=json.loads((target/'provenance.json').read_text());provenance['postprocess_hp']=qa;write(target/'provenance.json',provenance)
 (out/'review.md').write_text('Independent '+side+' HP fill. Generated pixels copied from '+ident+'/original-combined.png. Alpha margins16px; no painted replacement art. Use content_rect and frame fill_offset for registration. approved:false.\n')
 (out/'prompt.md').write_text((out/'prompt.md').read_text()+'\nDerived operation: crop '+str(extract)+' from '+ident+'/original-combined.png; nearest resize to '+str([r-l,b-t])+'; pad16px alpha. No new generation.\n')
 # Actual25/50/100 percent composites, using only cropped generated fill pixels.
 proof=Image.new('RGBA',(frame.width*3,frame.height),(225,222,210,255))
 for i,ratio in enumerate([.25,.5,1]):
  part=patch.crop((0,0,round(patch.width*ratio),patch.height));proof.alpha_composite(part,(i*frame.width+l,t));proof.alpha_composite(frame,(i*frame.width,0))
 proof.convert('RGB').save(folder/'hp-fill-proof.png')
for ident,guides in [('battle_nameplate',[72,72,72,60]),('battle_actions',[192,72,192,72])]:
 rec=next(a for a in m['assets'] if a['id']==ident);rec['slice']=guides
 im=Image.open(R/rec['file']).convert('RGBA');w,h=im.size;l,t,r,b=guides
 def stretch(W,H):
  out=Image.new('RGBA',(W,H));xs=[0,l,w-r,w];ys=[0,t,h-b,h];dx=[0,l,W-r,W];dy=[0,t,H-b,H]
  for yy in range(3):
   for xx in range(3):
    patch=im.crop((xs[xx],ys[yy],xs[xx+1],ys[yy+1])).resize((dx[xx+1]-dx[xx],dy[yy+1]-dy[yy]),Image.Resampling.NEAREST);out.alpha_composite(patch,(dx[xx],dy[yy]))
  return out
 targets=[(max(l+r+24,round(w*.75)),h),(w,h),(round(w*1.5),round(h*1.25))]
 proof=Image.new('RGBA',(max(W for W,H in targets)+32,sum(H for W,H in targets)+96),(35,39,46,255));d=ImageDraw.Draw(proof);y=16
 for W,H in targets:
  d.text((16,y),f'{W} x {H}; slices {guides}',fill='white');y+=20;proof.alpha_composite(stretch(W,H),(16,y));y+=H+12
 proof.convert('RGB').save(R/ident/'9slice-stretch-proof.png')
 write(R/ident/'9slice-proof.json',{'guides':guides,'targets':[list(x) for x in targets],'method':'actual nine distinct source crops, independently nearest resized and composited','minimum_supported_px':[l+r+24,t+b+12],'warnings':['Stretch center texture remains visible; owner approval pending.']})
 rec['notes']='Actual9patch stretch proofs generated at0.75x/1x/1.5x width and1x/1.25x height. Guides preserve ornaments; see9slice-proof.json. Owner approval pending.'
write(R/'manifest.json',m)
assets=m['assets'];contact=Image.new('RGB',(1000,((len(assets)+7)//8)*140),(40,43,49));d=ImageDraw.Draw(contact)
preview=Image.new('RGB',(768,((len(assets)+5)//6)*112),(230,225,211));pd=ImageDraw.Draw(preview)
failures=[];raw_count=0
for i,s in enumerate(assets):
 im=Image.open(R/s['file']).convert('RGBA');w,h=s['frame_px'];part=im.crop((0,0,w,h));thumb=part.copy();thumb.thumbnail((100,100),Image.Resampling.NEAREST);x=i%8*125;y=i//8*140;contact.paste(thumb,(x+(125-thumb.width)//2,y),thumb);d.text((x,y+102),s['id'][:20],fill='white')
 x=i%6*128;y=i//6*112;small=part.resize((32,32),Image.Resampling.NEAREST);preview.paste(small,(x,y),small);big=part.resize((64,64),Image.Resampling.NEAREST);bg=Image.new('RGB',(64,64),(26,29,36));bg.paste(big,(0,0),big);preview.paste(bg,(x+40,y));pd.text((x,y+72),s['id'][:20],fill=(25,25,25))
 if list(im.size)!=s['px']:failures.append(s['id']+':dimensions')
 frames=[im.crop((n*w,0,(n+1)*w,h)) for n in range(s['frames'])]
 if len({f.tobytes() for f in frames})!=len(frames):failures.append(s['id']+':duplicate_frame')
 for f in frames:
  bb=f.getchannel('A').getbbox()
  if not bb or min(bb[0],bb[1],w-bb[2],h-bb[3])<8:failures.append(s['id']+':alpha_margin')
 for raw in (R/s['id']).glob('raw-*.png'):
  raw_count+=1
  if raw.read_bytes()!=(R/'jobs'/s['source_job']/raw.name).read_bytes():failures.append(s['id']+':raw_changed')
contact.save(R/'contact-sheet.png');preview.save(R/'game-size-light-dark.png')
write(R/'qa-summary.json',{'assets':len(assets),'animated_assets':sum(s['frames']>1 for s in assets),'animation_frames':sum(s['frames'] for s in assets if s['frames']>1),'raw_copies_byte_verified':raw_count,'mechanical_failures':failures,'hp_components_separated':True,'hp_fill_proof_ratios':[.25,.5,1],'nine_slice_proofs':2,'warnings':['Owner and in-engine review pending.','9slice center texture stretches; guide geometry visually reviewed.','Host model/cost not exposed.']})
print(json.dumps({'assets':len(m['assets']),'hp_fill_assets':2,'nine_slice_proofs':2}))
