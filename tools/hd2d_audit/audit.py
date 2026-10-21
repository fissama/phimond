import json,glob,os,hashlib,sys
import numpy as np
from PIL import Image
root=sys.argv[1]
rows=[]
for bdir in sorted(glob.glob(root+'/batch-*/')):
    b=os.path.basename(bdir.rstrip('/'))
    ms=[]
    for m in ['manifest.json','aux-manifest.json']:
        p=bdir+m
        if os.path.exists(p):
            d=json.load(open(p)); ms+= (d['assets'] if isinstance(d,dict) else d)
    seen=set()
    for a in ms:
        if a['id'] in seen: continue
        seen.add(a['id'])
        r={'batch':b,'id':a['id'],'cat':a.get('category'),'kit':a.get('kit'),'px':a.get('px'),'world':a.get('world'),'frames':a.get('frames'),'tile':a.get('tileable'),'sway':a.get('sway'),'issues':[]}
        f=bdir+a['file']
        if not os.path.exists(f): r['issues'].append('MISSING_FILE'); rows.append(r); continue
        im=Image.open(f); r['mode']=im.mode; r['size']=list(im.size)
        if a.get('px') and list(im.size)!=list(a['px']): r['issues'].append(f"SIZE {im.size} != {a['px']}")
        r['sha']=hashlib.sha256(open(f,'rb').read()).hexdigest()[:16]
        if im.mode!='RGBA': im=im.convert('RGBA')
        arr=np.asarray(im); al=arr[...,3]
        cat=a.get('category') or ''
        full= cat in('floor','backdrop_far','backdrop_mid','backdrop') or a.get('tileable') in('xy','x') or a['id'].startswith(('login','intro','loading-bg')) or 'panorama' in a['id']
        opaque=(al>0)
        r['opaque_frac']=round(float(opaque.mean()),3)
        semi=((al>0)&(al<255)).mean(); r['semi']=round(float(semi),4)
        if semi>0.02 and cat not in('fx',): r['issues'].append(f'SEMI_ALPHA {semi:.3f}')
        ys,xs=np.where(opaque)
        if len(xs):
            m=min(xs.min(),ys.min(),al.shape[1]-1-xs.max(),al.shape[0]-1-ys.max()); r['margin']=int(m)
            if not full and m<8 and a.get('frames',1)==1: r['issues'].append(f'MARGIN {m}')
        else: r['issues'].append('EMPTY')
        px=arr[opaque][:,:3]
        if len(px):
            nc=len(np.unique(px.reshape(-1,3),axis=0)); r['colors']=nc
            if nc>64 and cat not in('floor',): r['issues'].append(f'COLORS {nc}')
        # density
        w=a.get('world'); 
        if w and a.get('px') and cat not in('ui_sprite','ui_9slice','icon','fx','portrait'):
            fp=a.get('frame_px') or a['px']
            d=fp[0]/w[0]; r['density']=round(d,1)
            exp=64 if cat=='backdrop_far' else 128
            if cat in('backdrop','backdrop_far') and abs(d-64)/64<=0.12: exp=64
            if abs(d-exp)/exp>0.12 and cat not in('npc','player'): r['issues'].append(f'DENSITY {d:.0f}')
        # tile seam
        if a.get('tileable') in('xy','x') and len(arr):
            rgb=arr[...,:3].astype(float)
            def seam(e1,e2,n1): return float(np.abs(e1-e2).mean()), float(np.abs(n1-e1).mean())
            sx=seam(rgb[:,0],rgb[:,-1],rgb[:,1]); r['seam_x']=[round(sx[0],1),round(sx[1],1)]; r['seam_x_max']=int(np.abs(rgb[:,0]-rgb[:,-1]).max())
            if sx[0]>max(14,sx[1]*1.6): r['issues'].append(f'SEAM_X {sx[0]:.1f}/{sx[1]:.1f}')
            if a.get('tileable')=='xy':
                sy=seam(rgb[0],rgb[-1],rgb[1]); r['seam_y']=[round(sy[0],1),round(sy[1],1)]; r['seam_y_max']=int(np.abs(rgb[0]-rgb[-1]).max())
                if sy[0]>max(14,sy[1]*1.6): r['issues'].append(f'SEAM_Y {sy[0]:.1f}/{sy[1]:.1f}')
        if a.get('frames',1)>1 and a.get('frame_px'):
            if im.size[0]!=a['frames']*a['frame_px'][0] and im.size[1]!=a['frames']*a['frame_px'][1]: r['issues'].append('FRAMES_MISMATCH')
        r['approved']=a.get('approved')
        r['replaces']=a.get('replaces')
        rows.append(r)
json.dump(rows,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
import collections
print(len(rows),'assets')
for b in sorted(set(r['batch'] for r in rows)):
    R=[r for r in rows if r['batch']==b]; bad=[r for r in R if r['issues']]
    print(b,len(R),'with issues',len(bad), 'approved',sum(1 for r in R if r.get('approved')))
dups=collections.defaultdict(list)
for r in rows:
    if 'sha' in r: dups[r['sha']].append(r['batch']+'/'+r['id'])
print('duplicate-final groups',sum(1 for v in dups.values() if len(v)>1),'dup files',sum(len(v) for v in dups.values() if len(v)>1))
