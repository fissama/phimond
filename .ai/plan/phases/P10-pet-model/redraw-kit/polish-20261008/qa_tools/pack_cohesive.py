"""Pack intact 4x5 generated poses using actual empty gutters; never repaint alpha."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[7]

def dump(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

def gutter(values, preferred, radius):
    lo, hi = max(1, int(preferred-radius)), min(len(values)-1, int(preferred+radius))
    runs, start = [], None
    for i in range(lo, hi):
        if values[i] == 0:
            if start is None: start = i
        elif start is not None:
            if i-start >= 4: runs.append((start, i))
            start = None
    if start is not None and hi-start >= 4: runs.append((start, hi))
    if not runs: raise ValueError(f"No intact empty gutter near {preferred}; regenerate source")
    a, b = min(runs, key=lambda pair: abs((pair[0]+pair[1])/2-preferred))
    return (a+b)//2

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--species', required=True)
    parser.add_argument('--raw', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--portrait-only', action='store_true')
    args=parser.parse_args()
    root=args.out.resolve();root.mkdir(parents=True, exist_ok=True)
    target=root/'raw.png'
    if target.exists(): raise ValueError('Versioned source already exists')
    shutil.copy2(args.raw, target)
    catalog=json.loads((REPO/'data/p10/species.json').read_text())['records'][args.species]
    source_name=catalog['source']['species_id']
    refs=[]
    for n in (['portrait.png'] if args.portrait_only else ['portrait.png','sprites.png']):
        p=REPO/'apps/game-client/assets/pets/apk84'/source_name/n
        refs.append({'path':str(p.relative_to(REPO)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    provenance={'species_id':args.species,'original_references':refs,'generated_path':str(args.raw),'raw_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'source_alpha_unmodified':True,'packing_status':'source_analysis_pending'}
    dump(root/'inputs.json',provenance)
    im=Image.open(target).convert('RGBA');w,h=im.size
    sig=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
    pixels=sig.load()
    ys=[sum(bool(pixels[x,y]) for x in range(w)) for y in range(h)]
    rows=[0]+[gutter(ys,k*h/5,h/5*.30) for k in range(1,5)]+[h]
    cuts=[]
    for y0,y1 in zip(rows,rows[1:]):
        xs=[sum(bool(pixels[x,y]) for y in range(y0,y1)) for x in range(w)]
        cuts.append([0]+[gutter(xs,k*w/4,w/4*.18) for k in range(1,4)]+[w])
    anchors=[]
    for c in range(4):
        x0,x1=cuts[0][c:c+2];box=sig.crop((x0,rows[0],x1,rows[1])).getbbox()
        if box is None: raise ValueError('Empty neutral pose')
        anchors.append(x0+(box[0]+box[2])/2)
    frames=[];audit=[]
    for r in range(5):
        for c in range(4):
            x0,x1=cuts[r][c:c+2];y0,y1=rows[r:r+2]
            box=sig.crop((x0,y0,x1,y1)).getbbox()
            if box is None: raise ValueError('Empty animation pose')
            frames.append({'rect':[x0,y0,x1-x0,y1-y0],'pivot':[anchors[c]-x0,box[3]]})
            audit.append({'row':r+1,'column':c+1,'visible_alpha_bounds':list(box)})
    dump(root/'layout.json',{'destination_pivot':[140,210],'frames':frames})
    provenance.update(row_boundaries=rows,column_boundaries_by_row=cuts,source_frames=audit,packing_status='layout_ready',layout_rule='Actual empty gutters preserve complete poses. Source pivots align ground-contact baseline; one uniform NN scale. No per-frame resizing or erased alpha.')
    dump(root/'inputs.json',provenance)
    commands=[['pack_p10_atlas.py','--source',str(target),'--layout',str(root/'layout.json'),'--output',str(root/'packed.png')],['check_p10_atlas.py',str(root/'packed.png')],['preview_p10_redraw.py','--atlas',str(root/'packed.png'),'--out',str(root/'preview')]]
    for command,name in zip(commands,['packing.json','mechanical.json','preview-export.json']):
        run=subprocess.run([sys.executable,str(REPO/'tools/assets'/command[0]),*command[1:]],capture_output=True,text=True)
        (root/name).write_text(run.stdout)
        if run.returncode: raise ValueError(run.stderr or run.stdout)
    bg=Image.new('RGBA',im.size,(235,230,217,255));bg.alpha_composite(im)
    bg.convert('RGB').save(root/'raw-review.png')
    report=json.loads((root/'packing.json').read_text())
    print(json.dumps({'species_id':args.species,'status':'mechanical_pass_visual_review_pending','candidate':str(root/'packed.png'),'sha256':report['output_sha256'],'common_scale':report['scale'],'row_boundaries':rows}))

if __name__=='__main__': main()
