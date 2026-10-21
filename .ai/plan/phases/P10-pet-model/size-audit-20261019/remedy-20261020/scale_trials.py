"""Private display-size proposals. No art, registry or runtime activation."""
import hashlib,json,math,shutil
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np

ROOT=Path(__file__).resolve().parents[6];OUT=Path(__file__).resolve().parent
records=json.loads((OUT.parent/'measurements.json').read_text())['records']
states={r['id']:r for r in json.loads((OUT/'progress.json').read_text())['records']}
# Deliberate species-specific silhouette goals in reference source-pixel units.
# Width is the important axis for low/wide anatomy, not humanoid height.
width={17:215,20:205,36:180,50:210,51:210,52:210,68:190,87:190,106:185,107:180,124:190,139:190,140:195,149:195,150:185,151:205,154:210,155:215,159:225}
height={15:180,16:164,18:164,19:164,35:175,37:164,38:164,66:175,67:175,69:175,84:175,85:180,86:155,88:164,103:155,122:164,126:175,137:164,138:190,141:164,142:190,143:164,145:190,146:180,147:190,148:155,152:164,158:190}
uncertain={15,69,156,51,126}
height[156]=180
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',16)
small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',13)
trial=OUT/'scale-trials';trial.mkdir(exist_ok=True)
(trial/'images').mkdir(exist_ok=True)
items=[];images={}
for r in records:
    sid=r['id'];n=int(sid[-4:]);state=states.get(sid,{})
    candidate=state.get('candidate') if state.get('status')=='self_review_pass_pending_owner' else None
    path=ROOT/(candidate or r['path'])
    im=Image.open(path).convert('RGBA');a=np.asarray(im)[:,:,3];hs=[];ws=[];bottom=[];bounds=[]
    for i in range(20):
        cell=a[i//4*281:(i//4+1)*281,i%4*281:(i%4+1)*281];y,x=np.where(cell>=128)
        bounds.append([int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)])
        if i<4:hs.append(y.max()-y.min()+1);ws.append(x.max()-x.min()+1);bottom.append(y.max()+1)
    hh=float(np.mean(hs));ww=float(np.mean(ws));pivot=[140,float(np.median(bottom))]
    factor=width[n]/ww if n in width else height.get(n,hh)/hh
    if n==144:factor=1
    item={'id':sid,'name':r['name'],'star':r['star'],'path':str(path.relative_to(ROOT)),
        'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'action':'redraw_and_scale_preview' if candidate else 'scale_only_review',
        'factor':round(factor,5),'pivot':pivot,'before_pivot':[140,float(np.median([f['128']['bottom']+1 for f in r['frames'][:4]]))],
        'idle_h':hh,'idle_w':ww,'target_h':round(hh*factor,2),'target_w':round(ww*factor,2),
        'axis':'width' if n in width else 'height','face_contrast_focus':n in uncertain,
        'visual_status':'pending_trial_review','runtime_activated':False,'owner_approved':False,'bounds':bounds}
    items.append(item);images[sid]=im
    if n==156:
        # Manually reviewed boots/base, not an automatic effect-bbox fit.
        item['pivots_by_row']=[[140,y] for y in (202,222,202,212,197)]
        item['registration_note']='Manual action origins compensate source row translations; movement flame trail excluded from boot placement. One factor for all20; no per-frame fit. Trial only.'
    shutil.copyfile(path,trial/'images'/(sid+'.png'))
json_path=trial/'proposals.json'
json_path.write_text(json.dumps({'status':'private_preview_not_runtime_config','reference':'species_0144','cell_display_sizes':[96,192],
    'method':'Same reference pixels-to-display scale; one common factor and idle ground pivot for all20frames. No per-frame fit. Goals use silhouette bbox and require anatomy/contrast review.',
    'records':items},ensure_ascii=False,indent=2))

observed=[]
def pose_canvas(im,frame,factor,pivot,cell=96):
    # One fixed world-view canvas for everyone. Keep complete transformed frame;
    # do not clip large effects merely to make the comparison look neat.
    size=cell*4;ground=cell*3
    out=Image.new('RGBA',(size,size),(32,41,54,255));dr=ImageDraw.Draw(out)
    dr.line((0,ground,size,ground),fill='#596779')
    k=cell/281*factor;side=round(281*k)
    crop=im.crop(((frame%4)*281,(frame//4)*281,(frame%4+1)*281,(frame//4+1)*281))
    crop=crop.resize((side,side),Image.Resampling.NEAREST)
    x=round(size/2-pivot[0]*k);y=round(ground-pivot[1]*k)
    # Alpha footprint, not full transparent quad, determines any clipping.
    bb=crop.getchannel('A').getbbox()
    assert x+bb[0]>=0 and y+bb[1]>=0 and x+bb[2]<=size and y+bb[3]<=size, (frame,factor)
    if cell==96:observed.append([x+bb[0],y+bb[1],x+bb[2],y+bb[3]])
    out.alpha_composite(crop,(x,y));return out

ref=next(r for r in items if r['id']=='species_0144')
def pivot_for(item,frame):
    return item.get('pivots_by_row',[item['pivot']]*5)[frame//4]
# Every target: both96/192 scales, every20frame footprint checked, no crop.
for item in items:
    for cell in (96,192):
        for frame in range(20):pose_canvas(images[item['id']],frame,item['factor'],pivot_for(item,frame),cell)

# One shared review-camera crop for ALL56/ALL20; never per-frame/per-species fit.
camera=[max(0,min(b[0] for b in observed)-8),max(0,min(b[1] for b in observed)-8),
        min(384,max(b[2] for b in observed)+8),min(384,max(b[3] for b in observed)+8)]
(trial/'frames').mkdir(exist_ok=True)
for item in items:
    for cell in (96,192):
        mult=cell//96;crop=[v*mult for v in camera];cw=crop[2]-crop[0];ch=crop[3]-crop[1]
        sheet=Image.new('RGBA',(cw*4,ch*5+44),(24,31,42,255));dr=ImageDraw.Draw(sheet)
        dr.text((8,12),f"{item['id']} {item['name']} / preview cell{cell} / scale{item['factor']:.3f}x / NOT runtime",font=font,fill='white')
        for frame in range(20):
            scene=pose_canvas(images[item['id']],frame,item['factor'],pivot_for(item,frame),cell).crop(crop)
            sheet.alpha_composite(scene,((frame%4)*cw,44+(frame//4)*ch))
        sheet.convert('RGB').save(trial/'frames'/f"{item['id']}-{cell}.jpg",quality=97)
proof={'species':56,'frames_per_species':20,'display_cells':[96,192],'alpha_footprints_checked':2240,
       'common_camera_crop_at96':camera,'per_frame_fit':False,'alpha_erased':False,'runtime_activated':False,
       'note':'Canvas preview and source hashes; no certification of actual game camera, body masks, UI overlap or50CCU.'}
(trial/'verification.json').write_text(json.dumps(proof,indent=2))

# Compact overview uses identical pixels/world, floor and panel for all56.
# It crops a FIXED window from each completed scene, identical for all species.
for page,start in enumerate(range(0,len(items),8),1):
    sheet=Image.new('RGBA',(1100,8*185+70),(24,31,42,255));d=ImageDraw.Draw(sheet)
    d.text((15,12),f'DISPLAY SCALE TRIAL {page}/7 — same reference scale; preview only',font=font,fill='white')
    d.text((350,42),'Before',font=small,fill='white');d.text((610,42),'Proposed display',font=small,fill='white');d.text((870,42),'Linh Tiên reference',font=small,fill='white')
    for row,item in enumerate(items[start:start+8]):
        yy=70+row*185;sid=item['id'];old=next(r for r in records if r['id']==sid)
        d.text((12,yy+20),sid+' '+str(item['star'])+'★',font=font,fill='white')
        d.text((12,yy+48),item['name'],font=font,fill='#ffd88a')
        d.text((12,yy+76),f"{item['factor']:.2f}x / {item['axis']}",font=small,fill='#b7c8d9')
        for col,(im,fac,piv) in enumerate([(Image.open(ROOT/old['path']).convert('RGBA'),1,item['before_pivot']),(images[sid],item['factor'],item['pivot']),(images['species_0144'],1,ref['pivot'])]):
            scene=pose_canvas(im,0,fac,piv)
            # Fixed lower camera window includes full standing silhouettes;
            # complete20-frame uncropped proofs are generated in browser stage.
            view=scene.crop((64,145,320,325))
            sheet.alpha_composite(view,(310+col*260,yy))
    sheet.convert('RGB').save(trial/f'overview-{page:02}.jpg',quality=96)
print(f'{len(items)} proposals; {len(items)*20*2} alpha footprints fit uncropped stage at96/192. Seven overview pages.')
