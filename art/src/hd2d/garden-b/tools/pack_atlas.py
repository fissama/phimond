#!/usr/bin/env python3
"""Pack a generated 4x5 sheet by connected components and fixed local pivots.

Only chroma keying, component extraction, uniform nearest-neighbour scaling,
translation, shared palette reduction, and atlas assembly are performed.
"""
from __future__ import annotations
import argparse, json, math, shutil
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
from defringe import defringe_rgba, purple_edge_count_rgba

ROOT = Path(__file__).resolve().parents[1]
SAFE_MIN, SAFE_MAX = 16, 175
N_COLS, N_ROWS = 4, 5

def keyed_background(rgb):
    """Return magenta-key pixels, including the generated background's hue drift."""
    a=rgb.astype(np.int16)
    return (a[:,:,0] >= 130) & (a[:,:,2] >= 120) & (a[:,:,1] <= 85) & (np.abs(a[:,:,0]-a[:,:,2]) <= 100)

def nearest_cell(cx, cy, w, h):
    col=max(0,min(N_COLS-1,int(cx/(w/N_COLS))))
    row=max(0,min(N_ROWS-1,int(cy/(h/N_ROWS))))
    return row,col

def connected_components(rgb):
    alpha=~keyed_background(rgb)
    labels,count=ndimage.label(alpha,structure=np.ones((3,3),dtype=np.uint8))
    if count==0: raise ValueError('No non-magenta components found')
    sizes=np.bincount(labels.ravel(),minlength=count+1); sizes[0]=0
    sums_y=np.bincount(labels.ravel(),weights=np.repeat(np.arange(rgb.shape[0]),rgb.shape[1]),minlength=count+1)
    sums_x=np.bincount(labels.ravel(),weights=np.tile(np.arange(rgb.shape[1]),rgb.shape[0]),minlength=count+1)
    centers={}
    for label in range(1,count+1):
        n=int(sizes[label])
        if not n: continue
        centers[label]=(float(sums_x[label]/n),float(sums_y[label]/n))
    return labels,sizes,centers

def body_components(labels,sizes,centers,w,h):
    """Find one largest connected body candidate in each expanded nominal cell."""
    bodies={}; body_labels=set()
    for row in range(N_ROWS):
        for col in range(N_COLS):
            x0,x1,y0,y1=frame_source_rect(row,col,w,h)
            candidates=[]
            for lab,(cx,cy) in centers.items():
                rr,cc=nearest_cell(cx,cy,w,h)
                if rr==row and cc==col and x0<=cx<x1 and y0<=cy<y1:
                    candidates.append(lab)
            if not candidates:
                raise ValueError(f'No body candidate in row {row+1}, frame {col+1}')
            candidates.sort(key=lambda lab:int(sizes[lab]),reverse=True)
            bodies[(row,col)]=candidates[0]; body_labels.add(candidates[0])
    return bodies,body_labels

def assign_components(labels,sizes,centers,bodies,body_labels,w,h):
    """Assign detached effect components to the closest detected body center."""
    groups={key:[lab] for key,lab in bodies.items()}
    body_centers={key:centers[lab] for key,lab in bodies.items()}
    for lab,(cx,cy) in centers.items():
        if lab in body_labels: continue
        # Normalize by cell dimensions so rows/columns have comparable distance.
        key=min(body_centers,key=lambda k:(((cx-body_centers[k][0])/(w/N_COLS))**2 + ((cy-body_centers[k][1])/(h/N_ROWS))**2))
        groups[key].append(lab)
    return groups

def components_for_cell(rgb,labels,sizes,ids):
    ids=sorted(ids,key=lambda lab:int(sizes[lab]),reverse=True)
    components=[]
    for lab in ids:
        yy,xx=np.where(labels==lab)
        if not len(xx): continue
        components.append({'label':lab,'size':int(len(xx)),'x':xx.astype(np.int32),'y':yy.astype(np.int32),
                           'bbox':[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())]})
    return components

def body_pivot(body, kind, components=None):
    xs,ys=body['x'],body['y']
    # A final harvest frame may contain only detached sparse rays. With no
    # character-sized component, anchor the complete effect cluster as one.
    if kind=='crop' and body['size']<1500 and components:
        xs=np.concatenate([comp['x'] for comp in components])
        ys=np.concatenate([comp['y'] for comp in components])
    if kind=='crop':
        lowest=int(ys.max()); take=ys>=max(int(ys.min()),lowest-5)
        return float(xs[take].mean()),float(lowest)
    lowest=int(ys.max()); take=ys==lowest
    return float(xs[take].mean()),float(lowest)

def frame_source_rect(row,col,w,h):
    cw=w/N_COLS; ch=h/N_ROWS
    x0=col*cw; x1=(col+1)*cw; y0=row*ch; y1=(row+1)*ch
    return [max(0.0,x0-.12*cw),min(float(w),x1+.12*cw),max(0.0,y0-.12*ch),min(float(h),y1+.12*ch)]

def base_offset(px, py, scale, target):
    ox=target[0]-int(np.rint(px*scale)); oy=target[1]-int(np.rint(py*scale))
    return ox,oy

def transform_points(frame, px, py, scale, target, shift=(0,0)):
    ox,oy=base_offset(px,py,scale,target)
    ox+=int(shift[0]); oy+=int(shift[1])
    xs=np.rint(frame['x']*scale).astype(np.int32)+ox
    ys=np.rint(frame['y']*scale).astype(np.int32)+oy
    return xs,ys,ox,oy

def placement_shift(item,kind,scale):
    px,py=item['pivot']; target=(96,168 if kind=='crop' else 175)
    # Measure the actual post-resample silhouette just as the QA script will:
    # detached effects stay out of the body unless nearest-neighbor packing
    # physically joins them to it.
    points=item['components']
    xs=np.concatenate([p['x'] for p in points]); ys=np.concatenate([p['y'] for p in points])
    ox,oy=base_offset(px,py,scale,target)
    tx=np.rint(xs*scale).astype(np.int32)+ox
    ty=np.rint(ys*scale).astype(np.int32)+oy
    local=np.zeros((192,192),dtype=bool)
    inside=(tx>=0)&(tx<192)&(ty>=0)&(ty<192)
    local[ty[inside],tx[inside]]=True
    labels,count=ndimage.label(local,structure=np.ones((3,3),dtype=np.uint8))
    if count and not (kind=='crop' and item['body']['size']<1500):
        sizes=np.bincount(labels.ravel()); sizes[0]=0
        local=labels==int(np.argmax(sizes))
    uy,ux=np.where(local)
    if not len(ux): return (0,0)
    low=int(uy.max())
    if kind=='crop':
        lower=local & (np.indices(local.shape)[0]>=max(0,low-5))
        center=float(np.where(lower)[1].mean())
    else:
        lower=local & (np.indices(local.shape)[0]==low)
        center=float(np.where(lower)[1].mean())
    return int(np.rint(target[0]-center)),target[1]-low

def save_defringe_preview(rgba, path):
    """Save an atlas composited over the requested dark review color at 3×."""
    sprite=Image.fromarray(rgba,'RGBA')
    background=Image.new('RGBA',sprite.size,(30,30,35,255))
    background.alpha_composite(sprite)
    background.resize((sprite.width*3,sprite.height*3),Image.Resampling.NEAREST).save(path)

def fits(frames, kind, scale):
    target_y=168 if kind=='crop' else 175
    for item in frames:
        px,py=item['pivot']; target=(96,target_y)
        shift=placement_shift(item,kind,scale)
        for comp in item['components']:
            xs,ys,_,_=transform_points(comp,px,py,scale,target,shift)
            if xs.min()<SAFE_MIN or xs.max()>SAFE_MAX or ys.min()<SAFE_MIN or ys.max()>SAFE_MAX:
                return False
        if kind=='crop' and item['row']==2:
            body=item['body']; xs,ys,_,_=transform_points(body,px,py,scale,target)
            if target_y-int(ys.min())+1>150: return False
    return True

def choose_scale(frames,kind):
    low=.6; high=1.0
    if not fits(frames,kind,low): raise ValueError('No common scale s≥0.6 fits all frames inside safe bounds; redraw required')
    while high<8.0 and fits(frames,kind,high):
        low=high; high=min(8.0,high*2)
    if high==8.0 and fits(frames,kind,high): return high
    for _ in range(50):
        mid=(low+high)/2
        if fits(frames,kind,mid): low=mid
        else: high=mid
    return low

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--id',required=True)
    ap.add_argument('--kind',choices=['pot','crop'],required=True)
    ap.add_argument('--raw',default='raw-09.png')
    args=ap.parse_args()
    folder=ROOT/args.id; source=folder/args.raw
    if not source.is_file(): raise SystemExit(f'Missing source sheet: {source}')
    image=Image.open(source).convert('RGB'); rgb=np.asarray(image); h,w=rgb.shape[:2]
    labels,sizes,centers=connected_components(rgb)
    bodies,body_labels=body_components(labels,sizes,centers,w,h)
    groups=assign_components(labels,sizes,centers,bodies,body_labels,w,h)
    all_frames=[]; component_log=[]
    for r in range(N_ROWS):
        for c in range(N_COLS):
            rect=frame_source_rect(r,c,w,h)
            comps=components_for_cell(rgb,labels,sizes,groups[(r,c)])
            body=next(comp for comp in comps if comp['label']==bodies[(r,c)])
            # A giant component usually means the magenta key failed, so stop rather than pack background.
            if body['size']>.55*(w/N_COLS)*(h/N_ROWS):
                raise ValueError(f'Likely key failure at row {r+1}, frame {c+1}: largest component={body["size"]} px')
            px,py=body_pivot(body,args.kind,comps)
            item={'row':r,'col':c,'components':comps,'body':body,'pivot':(px,py),'source_rect':rect}
            all_frames.append(item)
            component_log.append({'row':r+1,'frame':c+1,'source_rect':[round(v,3) for v in rect],
                                  'component_count':len(comps),'body_component_px':body['size'],
                                  'body_bbox_source':body['bbox'],'pivot_source':[round(px,3),round(py,3)]})
    scale=choose_scale(all_frames,args.kind)
    target_y=168 if args.kind=='crop' else 175
    raw_rgba=np.zeros((N_ROWS*192,N_COLS*192,4),dtype=np.uint8)
    pack_frames=[]
    for item in all_frames:
        r,c=item['row'],item['col']; px,py=item['pivot']; target=(96,target_y)
        canvas_rgb=np.zeros((192,192,3),dtype=np.uint8); canvas_a=np.zeros((192,192),dtype=np.uint8)
        shift=placement_shift(item,args.kind,scale)
        for comp in reversed(item['components']):
            xs,ys,ox,oy=transform_points(comp,px,py,scale,target,shift)
            if np.any(xs<0) or np.any(xs>=192) or np.any(ys<0) or np.any(ys>=192):
                raise ValueError(f'Unexpected output clipping at row {r+1}, frame {c+1}')
            rgb_vals=rgb[comp['y'],comp['x']]
            canvas_rgb[ys,xs]=rgb_vals; canvas_a[ys,xs]=255
        y0=r*192; x0=c*192
        raw_rgba[y0:y0+192,x0:x0+192,:3]=canvas_rgb
        raw_rgba[y0:y0+192,x0:x0+192,3]=canvas_a
        body=item['body']; bxs,bys,ox,oy=transform_points(body,px,py,scale,target,shift)
        pack_frames.append({'row':r+1,'frame':c+1,'source_rect':[round(v,3) for v in item['source_rect']],
                            'body_bbox_source':body['bbox'],'body_component_px':body['size'],'pivot_source':[round(px,3),round(py,3)],
                            'pivot_target':list(target),'scale_s':round(scale,8),'offset':[ox,oy],
                            'packed_body_bbox':[int(bxs.min()),int(bys.min()),int(bxs.max()),int(bys.max())],
                            'component_count':len(item['components'])})
    pre_defringe=raw_rgba.copy()
    defringe_frames=[]
    for r in range(N_ROWS):
        for c in range(N_COLS):
            y0=r*192; x0=c*192
            cleaned,stats=defringe_rgba(raw_rgba[y0:y0+192,x0:x0+192])
            raw_rgba[y0:y0+192,x0:x0+192]=cleaned
            defringe_frames.append({'row':r+1,'frame':c+1,**stats})
    save_defringe_preview(pre_defringe,folder/'defringe-before-3x-dark.png')
    totals={key:sum(frame[key] for frame in defringe_frames) for key in
            ('purple_edge_before','purple_edge_after','replaced_pixels')}
    # Apply a single shared ≤60-color palette to all opaque pixels.
    visible=raw_rgba[:,:,:3][raw_rgba[:,:,3]>0]
    palette=Image.fromarray(visible.reshape(1,-1,3),'RGB').quantize(colors=60,method=Image.Quantize.MEDIANCUT)
    final=np.zeros_like(raw_rgba)
    for r in range(N_ROWS):
        for c in range(N_COLS):
            y0=r*192; x0=c*192; cell=raw_rgba[y0:y0+192,x0:x0+192]
            quant=Image.fromarray(cell[:,:,:3],'RGB').quantize(palette=palette).convert('RGB')
            pix=np.asarray(quant).copy(); alpha=cell[:,:,3]; pix[alpha==0]=0
            final[y0:y0+192,x0:x0+192,:3]=pix; final[y0:y0+192,x0:x0+192,3]=alpha
    for frame in defringe_frames:
        r=frame['row']-1; c=frame['frame']-1
        cell=final[r*192:(r+1)*192,c*192:(c+1)*192]
        frame['purple_edge_after_pre_palette']=frame['purple_edge_after']
        frame['purple_edge_after']=purple_edge_count_rgba(cell)
    totals['purple_edge_after_pre_palette']=totals['purple_edge_after']
    totals['purple_edge_after']=sum(frame['purple_edge_after'] for frame in defringe_frames)
    save_defringe_preview(final,folder/'defringe-after-3x-dark.png')
    old=folder/'final.png'
    if old.exists() and not (folder/'final-before-pipeline-v3.png').exists():
        shutil.copy2(old,folder/'final-before-pipeline-v3.png')
    Image.fromarray(final,'RGBA').save(old)
    qa_path=folder/'qa.json'
    try: qa=json.loads(qa_path.read_text(encoding='utf-8'))
    except Exception: qa={}
    qa['packing']={'pipeline':'garden-atlas-pipeline-v3','source_file':args.raw,'source_size_px':[w,h],
                   'connectivity':8,'magenta_key':'R>=130, B>=120, G<=85, abs(R-B)<=100',
                   'cell_assignment':'component centroid nearest nominal 4x5 cell; each source window expanded ±12%',
                   'common_scale_s':round(scale,8),'resampling':'nearest-neighbor','clipped_pixels':0,
                   'frames':pack_frames}
    qa['defringe']={'algorithm':'purple-rim-edge-replace-v1','hue_degrees':[270,345],
                    'saturation_gt':0.2,'replacement':'darkest 8-neighbor opaque non-edge color',
                    'counts':totals,'frames':defringe_frames,
                    'preview_before':'defringe-before-3x-dark.png',
                    'preview_after':'defringe-after-3x-dark.png'}
    qa_path.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'PACKED {args.id}: source={source.name} size={w}x{h}, components={len(centers)}, common_s={scale:.6f}; wrote {old}')
    return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as exc: raise SystemExit(f'PACK FAIL: {exc}')
