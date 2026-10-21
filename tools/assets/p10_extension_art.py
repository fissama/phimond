#!/usr/bin/env python3
"""Record and pack an authored extension candidate; never select runtime art."""
from pathlib import Path
import argparse, hashlib, json, shutil
from PIL import Image
from pack_p10_atlas import pack
from check_p10_atlas import check
from preview_p10_redraw import export

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / '.ai/plan/phases/P10-pet-model/extension-20261013'
ART = ROOT / 'apps/game-client/assets/pets/redraws/extension-20261013'
ANCHOR = ROOT / 'apps/game-client/assets/pets/redraws/owner-feedback-20261009/species_0052/attempt-01/packed.png'

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, value): p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def source_rectangles(image):
    """Partition the complete raw canvas at its least occupied gutters.

    This measures alpha without editing it. All rectangles cover the complete
    canvas exactly once. A visible effect may extend past a nominal grid edge;
    packing must use the actual gutter rather than cut that effect in two.
    Geometry is a proposal and still requires exact-image visual review.
    """
    alpha=image.getchannel('A')
    if alpha.getbbox() is None:raise ValueError('Empty source')
    w,h=image.size
    def count(box):
        tile=alpha.crop(box)
        histogram=tile.histogram()
        # Protect opaque anatomy and visible effects before faint glow. A thin
        # solid tail must not be cut just to avoid a wider translucent fringe.
        return (sum(histogram[128:]),sum(histogram[16:]),sum(histogram[1:]))
    ys=[0]
    for r in range(1,5):
        nominal=round(r*h/5);radius=round(h/5*.34)
        ys.append(min(range(max(ys[-1]+1,nominal-radius),min(h,nominal+radius+1)),
                      key=lambda y:(count((0,y,w,y+1)),abs(y-nominal))))
    ys.append(h)
    frames=[]
    for r in range(5):
        y0,y1=ys[r:r+2]
        xs=[0]
        for c in range(1,4):
            nominal=round(c*w/4);radius=round(w/4*.34)
            xs.append(min(range(max(xs[-1]+1,nominal-radius),min(w,nominal+radius+1)),
                          key=lambda x:(count((x,y0,x+1,y1)),abs(x-nominal))))
        xs.append(w)
        row=[]
        for c in range(4):
            x0,x1=xs[c:c+2]
            bounds=alpha.crop((x0,y0,x1,y1)).getbbox()
            if bounds is None:raise ValueError('Empty source pose')
            row.append({'rect':[x0,y0,x1-x0,y1-y0],
                        'pivot':[(c+.5)*w/4-x0,bounds[3]]})
        ground=max(f['pivot'][1] for f in row)
        for f in row:f['pivot'][1]=ground
        frames.extend(row)
    return frames

def prepare(sid, generated, attempt=1, prompt_path=None, reference=None, facing='left', adaptive=True):
    jobs = {j['species_id']:j for j in json.loads((PLAN/'art-jobs.json').read_text())}
    job = jobs[sid]
    folder = ART / sid / f'attempt-{attempt:02d}'
    folder.mkdir(parents=True, exist_ok=True)
    raw = folder/'raw.png'
    if (folder/'packed.png').exists(): raise ValueError('Packed attempt already exists')
    if raw.exists():
        if digest(raw)!=digest(generated): raise ValueError('Raw attempt hash differs; use a new attempt')
    else: shutil.copy2(generated, raw)
    reference = (reference or ANCHOR).resolve()
    shutil.copy2(reference, folder/'style-reference.png')
    (folder/'prompt.txt').write_text(prompt_path.read_text() if prompt_path else job['prompt'])
    write(folder/'inputs.json', {'tool':'built-in image_gen','provenance':'Phimond-authored',
        'generation_output':str(generated),'raw_sha256':digest(raw),
        'style_reference':{'path':str(reference.relative_to(ROOT)), 'sha256':digest(reference),
                           'owner_status':'owner_approved_done' if reference == ANCHOR else 'unapproved_revision_input',
                           'purpose':'style only' if reference == ANCHOR else 'edit previous authored candidate identity'}})
    image = Image.open(raw)
    w,h = image.size
    frames=[]
    for r in range(5):
        for c in range(4):
            x0,x1=round(c*w/4),round((c+1)*w/4)
            y0,y1=round(r*h/5),round((r+1)*h/5)
            box=image.crop((x0,y0,x1,y1)).getchannel('A').getbbox()
            if box is None: raise ValueError('Empty source frame')
            frames.append({'rect':[x0,y0,x1-x0,y1-y0], 'pivot':[(x1-x0)/2,box[3]]})
    for r in range(5):
        ground=max(f['pivot'][1] for f in frames[r*4:r*4+4])
        for f in frames[r*4:r*4+4]:f['pivot'][1]=ground
    if adaptive:frames=source_rectangles(image)
    write(folder/'layout.json', {'destination_pivot':[140,237],'frames':frames})
    packed=folder/'packed.png'
    packing=pack(raw,folder/'layout.json',packed)
    write(folder/'packing.json',packing)
    mechanical=check(packed)
    write(folder/'mechanical.json',mechanical)
    if mechanical['status']!='pass':raise ValueError('Mechanical failure')
    preview=export(packed,folder/'preview')
    with Image.open(packed) as atlas:
        for size in (64,96,192):
            contact=Image.new('RGB',(4*size,5*size),'#ddd7c8')
            for i in range(20):
                frame=atlas.crop((i%4*281,i//4*281,i%4*281+281,i//4*281+281))
                tile=frame.resize((size,size),Image.Resampling.NEAREST)
                contact.paste(tile,(i%4*size,i//4*size),tile)
            contact.save(folder/f'contact-{size}.png')
        for row in range(5):
            tiles=[]
            for col in range(4):
                frame=atlas.crop((col*281,row*281,col*281+281,row*281+281))
                tile=Image.new('RGBA',(281,281),'#ddd7c8');tile.alpha_composite(frame)
                tiles.append(tile.convert('RGB'))
            options={'loop':0} if row<2 else {}
            tiles[0].save(folder/f'row-{row+1}.gif',save_all=True,append_images=tiles[1:],
                          duration=180,disposal=2,**options)
    result={'species_id':sid,'proposal_id':job['proposal_id'],'name':job['name'],
        'provenance':'Phimond-authored','status':'candidate_for_owner_review','base_facing':facing,
        'candidate_path':str(packed.relative_to(ROOT)),'candidate_sha256':digest(packed),
        'mechanical':'pass','visual_status':'awaiting_visual_review','human_approved':False,
        'owner_approved':False,'runtime_activated':False,
        'preview_path':str((folder/'preview/preview.html').relative_to(ROOT)),
        'source_partition':'20 adaptive gutter rectangles; full canvas coverage, no alpha erased' if adaptive else '20 full canvas rectangles; no alpha erased',
        'timing':'review presets, not runtime gameplay timings'}
    write(ART/sid/'result.json',result)
    manifest_path=PLAN/'art-manifest.json'
    manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {
        'schema_version':1,'total':8,'owner_approved':0,'runtime_activated':False,'records':{}}
    manifest['records'][sid]=result
    write(manifest_path,manifest)
    print(json.dumps({'species_id':sid,'mechanical':mechanical['status'],
                     'sha256':result['candidate_sha256'],'scale':packing['scale']},ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('species_id');p.add_argument('generated',type=Path)
    p.add_argument('--attempt',type=int,default=1)
    p.add_argument('--prompt-file',type=Path);p.add_argument('--reference',type=Path)
    p.add_argument('--facing',choices=['left','right'],default='left')
    p.add_argument('--adaptive',action='store_true',default=True)
    p.add_argument('--regular-grid',dest='adaptive',action='store_false',
                   help='Only for a source whose regular grid was visually confirmed')
    a=p.parse_args();prepare(a.species_id,a.generated,a.attempt,a.prompt_file,a.reference,a.facing,a.adaptive)
