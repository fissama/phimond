from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,sys,hashlib
R=Path(__file__).parent.resolve();F=Path('/Users/phileanh/.codex/skills');P=sys.executable
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def run(a):
 r=subprocess.run([P,*map(str,a)],capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stdout+r.stderr)
 return r.stdout
records=[]
for jf in sorted((R/'jobs').glob('*/job.json')):
 j=json.loads(jf.read_text());jd=jf.parent;raw=jd/'raw-01.png'
 if not raw.exists():continue
 labels=[a['id'] for a in j['assets']]+['skip']*(4-len(j['assets']));out=jd/j.get('extracted_dir',('extracted-reviewed' if j.get('boxes_file') else 'extracted'))
 if not out.exists():print(run([F/'generate2dmap/scripts/extract_prop_pack.py','--input',raw,*(['--boxes-file',jd/j['boxes_file']] if j.get('boxes_file') else ['--rows',2,'--cols',2,'--grid-rounding','nearest','--labels',','.join(labels)]),'--output-dir',out,'--background-mode','native_alpha','--alpha-hygiene','both','--component-mode','all','--component-padding',8,'--art-source','host_image']))
 pack=json.loads((out/'prop-pack.json').read_text());items={a.get('display_name',a['label']):a for a in pack['accepted']}
 for a in j['assets']:
  im=Image.open(out/items[a['id']]['image']).convert('RGBA');im.putalpha(im.getchannel('A').point(lambda x:255 if x>=128 else 0));im=im.crop(im.getbbox());size=256 if j.get('portrait') else 192;height=240 if j.get('portrait') else 168
  sc=min(height/im.height,(size-16)/im.width);im=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.NEAREST);canvas=Image.new('RGBA',(size,size));canvas.alpha_composite(im,((size-im.width)//2,size-8-im.height))
  for tid in a['target_ids']:
   dest=R/tid;dest.mkdir(exist_ok=True);canvas.save(dest/'crop.png');(dest/'raw-01.png').write_bytes(raw.read_bytes());(dest/'prompt.md').write_text((jd/'prompt.md').read_text());(dest/'review.md').write_text('# Source identification\n\n'+a['identity']+'\n\n'+j['source_card']+'\n\nDraft; approved:false. Full source identity reviewed before generation. Shared costumes intentionally reused for IDs with identical apk_sprite. New roles use family reference, not a claimed original. No animation has been generated.\n')
   rec={'id':tid,'category':'player' if tid.startswith('player') else 'npc','kit':'human-portrait' if j.get('portrait') else 'human-master','file':tid+'/final.png','px':[size,size],'world':[size/128,size/128],'pivot':'bottom_center','pivot_px':[size//2,size-8],'tileable':'none','slice':None,'frames':1,'fps':None,'sway':False,'source_refs':j['refs'],'replaces':None,'approved':False,'status':'needs_owner_review','art_source':'host_image','route':'built-in image_gen','model':'not exposed','source_job':j['id'],'shared_costume_master':a['id'],'raw_sha256':sha(raw),'notes':'Master still draft; not activated. Animation blocked pending owner approval and configured image-to-video capability.'};records.append(rec)
inputs=R/'palette-inputs';inputs.mkdir(exist_ok=True)
for x in records:(inputs/(x['id']+'.png')).write_bytes((R/x['id']/'crop.png').read_bytes())
palette=R/('palette-all-v3' if any(x['kit']=='human-portrait' for x in records) else 'palette-masters-v2')
if not palette.exists():print(run([F/'generate2dsprite/scripts/palette_tool.py','build','--input',inputs,'--colors',48,'--balance','--output-dir',palette]))
for x in records:
 dest=R/x['id'];finish=dest/palette.name
 if not finish.exists():run([F/'generate2dsprite/scripts/palette_tool.py','apply','--input',dest/'crop.png','--palette',palette/'palette.json','--output-dir',finish])
 (dest/'final.png').write_bytes((finish/'crop.png').read_bytes());im=Image.open(dest/'final.png').convert('RGBA');bb=im.getbbox();m=[bb[0],bb[1],im.width-bb[2],im.height-bb[3]];colors=len({p[:3] for p in im.getdata() if p[3]});partial=sum(p[3] not in [0,255] for p in im.getdata());qa={'alpha_margins':m,'colors':colors,'partial_alpha':partial,'raw_integrity':sha(dest/'raw-01.png')==x['raw_sha256'],'failures':[]}
 if min(m)<8:qa['failures'].append('alpha_margin_8')
 if colors>48:qa['failures'].append('palette48')
 if partial:qa['failures'].append('binary_alpha')
 if x['kit']=='human-master' and not 160<=bb[3]-bb[1]<=170:qa['failures'].append('body_height160_170')
 write(dest/'qa.json',qa);x['mechanical_status']='blocked' if qa['failures'] else 'pass';x['sha256']=sha(dest/'final.png')
 w,h=im.size;preview=Image.new('RGB',(4*w+32,3*h+80));d=ImageDraw.Draw(preview)
 for s in [1,2]:
  pic=im.resize((w*s,h*s),Image.Resampling.NEAREST);y=20 if s==1 else h+60
  for col,bg in enumerate([(238,233,219),(25,29,36)]):
   xx=col*(w*s+16);preview.paste(bg,(xx,y,xx+pic.width,y+pic.height));preview.paste(pic,(xx,y),pic);d.text((xx,y-16),str(s)+'x',fill='white')
 preview.save(dest/'review-light-dark.png')
write(R/'manifest.json',{'batch':'05-octopath','approved':False,'status':'draft_animation_blocked','assets':records,'expected_npcs':49,'expected_players':2,'actual_main_portraits':11,'plan_main_portraits':17,'unspecified_portrait_slots':6,'animation_blocker':'No configured image-to-video route; no owner-approved masters.'})
cols=6;cw=280;ch=310;c=Image.new('RGB',(cols*cw,60+((len(records)+cols-1)//cols)*ch),(32,36,44));d=ImageDraw.Draw(c);d.text((12,12),'PHIMOND / OCTOPATH HUMAN MASTER DRAFTS / OWNER REVIEW PENDING',fill='white')
for i,x in enumerate(records):
 im=Image.open(R/x['file']).convert('RGBA');xx=i%cols*cw;yy=60+i//cols*ch;c.paste(im,(xx+(cw-im.width)//2,yy),im);d.text((xx+8,yy+265),x['id'],fill='white');d.text((xx+8,yy+283),x['mechanical_status'],fill='white')
c.save(R/'contact-sheet.png');print(json.dumps({'total':len(records),'pass':sum(x['mechanical_status']=='pass' for x in records)}))
