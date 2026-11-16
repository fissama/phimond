#!/usr/bin/env python3
"""Mechanical checks for garden-b 4x5 atlases packed by pack_atlas.py."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
CELL = 192

def report(key, ok, detail):
    print(f"{'PASS' if ok else 'FAIL'} {key}: {detail}")
    return bool(ok)

def frame_rgba(atlas, row, col):
    return atlas[row*CELL:(row+1)*CELL, col*CELL:(col+1)*CELL]

def bbox(mask):
    ys, xs = np.where(mask)
    return None if not len(xs) else [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]

def body_mask(alpha_mask):
    labels, count = ndimage.label(alpha_mask, structure=np.ones((3,3), dtype=np.uint8))
    if not count:
        return np.zeros_like(alpha_mask, dtype=bool)
    sizes = np.bincount(labels.ravel()); sizes[0] = 0
    return labels == int(np.argmax(sizes))

def iou(a, b):
    union = np.count_nonzero(a | b)
    return 1.0 if union == 0 else float(np.count_nonzero(a & b) / union)

def face_notes(path):
    txt = path.read_text(encoding='utf-8') if path.exists() else ''
    out = {}
    pat = r'face_row_(\d)\s*:\s*eyes\s*=\s*(\d+\s*,\s*\d+)\s*;\s*mouth\s*=\s*(\d+\s*,\s*\d+)\s*;\s*blink\s*=\s*(frame\d+|none)'
    for row, eyes, mouth, blink in re.findall(pat, txt, re.I):
        out[int(row)] = {'eyes': eyes, 'mouth': mouth, 'blink': blink.lower()}
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True)
    ap.add_argument('--kind', choices=['pot','crop'], required=True)
    args = ap.parse_args()
    folder = ROOT / args.id
    qa_path = folder / 'qa.json'
    try:
        previous_qa = json.loads(qa_path.read_text(encoding='utf-8'))
        pack_meta = previous_qa.get('packing')
        defringe_meta = previous_qa.get('defringe')
    except Exception:
        pack_meta = None
        defringe_meta = None
    try:
        im = Image.open(folder/'final.png').convert('RGBA')
    except Exception as exc:
        report('a', False, f'cannot open final.png: {exc}')
        return 1
    arr = np.asarray(im)
    alpha = arr[:,:,3]
    alphas = sorted(int(x) for x in np.unique(alpha))
    hidden = int(np.count_nonzero((alpha == 0) & np.any(arr[:,:,:3] != 0, axis=2)))
    checks = {}
    checks['a'] = report('a', im.size == (768,960) and alphas == [0,255] and hidden == 0,
                         f'size={im.size}, alpha={alphas}, alpha0_nonzero_rgb={hidden}')
    frames=[]; masks=[]; bodies=[]; boxes=[]; colors=set()
    if im.size == (768,960):
        for r in range(5):
            for c in range(4):
                fr=frame_rgba(arr,r,c); m=fr[:,:,3] > 0; frames.append(fr); masks.append(m); bodies.append(body_mask(m)); boxes.append(bbox(m))
                colors.update(map(tuple, fr[:,:,:3][m].tolist()))
    hashes=[f.tobytes() for f in frames]
    nonempty=sum(b is not None for b in boxes)
    checks['b']=report('b',nonempty==20 and len(set(hashes))==20,f'nonempty={nonempty}/20, unique={len(set(hashes))}/20')
    violations=[]
    for i,m in enumerate(masks):
        ys,xs=np.where(m)
        if len(xs) and (xs.min()<16 or ys.min()<16 or xs.max()>175 or ys.max()>175):
            violations.append((i//4+1,i%4+1,bbox(m)))
    checks['c']=report('c',not violations,f'violations={violations}; every opaque pixel must be inside [16,175]')
    checks['d']=report('d',len(colors)<=60,f'visible_colors={len(colors)} (≤60)')

    packing_frames=(pack_meta or {}).get('frames',[])
    pivot_results=[]
    for i,body in enumerate(bodies):
        ys,xs=np.where(body)
        if not len(xs):
            pivot_results.append({'row':i//4+1,'frame':i%4+1,'x':None,'y':None}); continue
        if args.kind=='crop':
            # Harvest frame 4 may intentionally contain only sparse rays; use
            # its complete effect mask as the anchor geometry, not one ray.
            use_mask=masks[i] if i==15 and packing_frames and packing_frames[i].get('body_component_px',99999)<1500 else body
            pyx=np.where(use_mask)
            low=int(pyx[0].max()); lowmask=use_mask & (np.indices(use_mask.shape)[0] >= max(0,low-5))
            px=float(np.where(lowmask)[1].mean()) if lowmask.any() else -999.0
            py=int(low); tx,ty=96,168
        else:
            low=ys.max(); bottom=body & (np.indices(body.shape)[0] == low)
            px=float(np.where(bottom)[1].mean()) if bottom.any() else -999.0
            py=int(low); tx,ty=96,175
        pivot_results.append({'row':i//4+1,'frame':i%4+1,'x':px,'y':py,'target':[tx,ty]})
    pivot_bad=[p for p in pivot_results if p['x'] is None or abs(p['x']-p['target'][0])>1 or abs(p['y']-p['target'][1])>1]
    checks['e']=report('e',len(pivot_results)==20 and not pivot_bad,f'pivot_failures={pivot_bad}; expected x/y ±1')

    if args.kind=='crop':
        heights={}; widths=[]; height_bad=[]
        for r,(lo,hi) in enumerate(((45,75),(85,112),(120,150))):
            vals=[]
            for c in range(4):
                b=bbox(bodies[r*4+c]); h=0 if b is None else 168-b[1]+1; w=0 if b is None else b[2]-b[0]+1
                vals.append(h); widths.append(w)
                if not lo<=h<=hi: height_bad.append((r+1,c+1,h,lo,hi))
            heights[str(r+1)]=vals
        maxw=max(widths,default=0)
        checks['f']=report('f',not height_bad and maxw<=140,f'heights={heights}, max_body_width={maxw}; fails={height_bad}')
        transitions={}; checks['g']=report('g',True,'N/A for crop')
        # Row 5 frame 4 is index 19; compare that plant endpoint to row 1 frame 1.
        h_iou=iou(masks[19],masks[0]) if len(masks)==20 else 0.0
        checks['h']=report('h',h_iou>=0.75,f'plant_f4_vs_sprout_f1_IoU={h_iou:.4f} (≥0.75; Claude criteria revision 2026-11-16)')
        notes=face_notes(folder/'review.md')
        loops=[1,2,3]
        blink_ok=all(r in notes and notes[r]['blink']!='none' for r in loops)
        annotated=all(r in notes for r in range(1,6))
        checks['i']=report('i',blink_ok and annotated,f'face_rows={sorted(notes)}, blink_rows={[r for r in loops if r in notes and notes[r]["blink"]!="none"]}; requires a blink in rows 1–3')
        loop_rows=loops
    else:
        # Soil luminance is sampled only in the elliptical planting mouth around (96,112).
        yy,xx=np.mgrid[0:CELL,0:CELL]
        mouth=((xx-96)/34.0)**2+((yy-112)/12.0)**2<=1.0
        def luminance(frame):
            rgb=frame[:,:,:3].astype(float)
            return 0.2126*rgb[:,:,0]+0.7152*rgb[:,:,1]+0.0722*rgb[:,:,2]
        def soil_mean(index):
            valid=mouth & masks[index]
            return float(luminance(frames[index])[valid].mean()) if valid.any() else float('inf')
        idle_l=soil_mean(0); wet_l=soil_mean(4)
        darkening=(idle_l-wet_l)/max(idle_l,1.0)
        body_adj=[]
        for r in range(5):
            for c in range(3): body_adj.append(iou(bodies[r*4+c],bodies[r*4+c+1]))
        transitions={'water4_to_wet1':iou(masks[11],masks[4]),'upgrade4_to_idle1':iou(masks[15],masks[0]),'clear4_to_idle1':iou(masks[19],masks[0])}
        g_ok=min(body_adj,default=0)>=0.94 and min(transitions.values())>=0.93 and darkening>=0.15
        checks['f']=report('f',True,'N/A for pot')
        checks['g']=report('g',g_ok,f'min_adjacent_body_IoU={min(body_adj,default=0):.4f} (≥0.94; Claude criteria revision 2026-11-16); transition_IoU={transitions} (≥0.93); idle_soil={idle_l:.2f}, wet_soil={wet_l:.2f}, darkening={darkening:.2%} (≥15%)')
        checks['h']=report('h',True,'N/A for pot')
        checks['i']=report('i',True,'N/A for pot (no face)')
        loop_rows=[1,2]
    adjacent=[]
    for r in loop_rows:
        for c in range(4): adjacent.append(iou(bodies[(r-1)*4+c],bodies[(r-1)*4+(c+1)%4]))
    j_ok=min(adjacent,default=0)>=0.85
    checks['j']=report('j',j_ok,f'min_loop_body_IoU={min(adjacent,default=0):.4f} (≥0.85), loop_rows={loop_rows}')
    metrics={'size_px':list(im.size),'alpha_values':alphas,'alpha0_nonzero_rgb':hidden,
             'nonempty_frames':nonempty,'unique_frames':len(set(hashes)),'cell_bounds':[{'row':i//4+1,'frame':i%4+1,'bbox':boxes[i]} for i in range(len(boxes))],
             'total_colors':len(colors),'pivot_measurements':pivot_results,'checks':checks,'all_pass':all(checks.values()),'asset_id':args.id,'kind':args.kind}
    if args.kind=='crop':
        metrics.update(stage_heights=heights,max_body_width_px=maxw,plant_sprout_iou=h_iou,face_annotations=notes,body_loop_iou=adjacent)
    else:
        metrics.update(soil_luminance={'idle':idle_l,'wet':wet_l,'darkening':darkening},transition_ious=transitions,body_adjacent_ious=body_adj)
    if pack_meta: metrics['packing']=pack_meta
    if defringe_meta: metrics['defringe']=defringe_meta
    qa_path.write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    passed=sum(bool(v) for v in checks.values())
    print(f"RESULT {'PASS' if all(checks.values()) else 'FAIL'} {args.id}: {passed}/10 checks")
    return 0 if all(checks.values()) else 2

if __name__=='__main__':
    raise SystemExit(main())
