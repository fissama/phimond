#!/usr/bin/env python3
"""Generalized magenta-keyed atlas packer for garden-c. Pixel generation is prohibited."""
import argparse, json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT=Path(__file__).resolve().parents[1]

def magenta(a):
    x=a.astype(np.int16)
    return (x[:,:,0]>=130)&(x[:,:,2]>=120)&(x[:,:,1]<=85)&(np.abs(x[:,:,0]-x[:,:,2])<=100)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--id',required=True); ap.add_argument('--raw',required=True)
    ap.add_argument('--cols',required=True,type=int); ap.add_argument('--rows',required=True,type=int)
    ap.add_argument('--cell',required=True,type=int); ap.add_argument('--canvas',required=True,help='WIDTHxHEIGHT')
    ap.add_argument('--pivot',required=True,help='X,Y'); ap.add_argument('--safe',required=True,help='MIN,MAX')
    ap.add_argument('--colors',type=int,default=60); ap.add_argument('--scale',type=float,default=None,help='Optional shared nearest-neighbor scale if it fits every frame')
    a=ap.parse_args(); wout,hout=map(int,a.canvas.lower().split('x')); px,py=map(int,a.pivot.split(',')); smin,smax=map(int,a.safe.split(','))
    folder=ROOT/a.id; src=folder/a.raw
    rgb=np.asarray(Image.open(src).convert('RGB')); H,W=rgb.shape[:2]
    labels,n=ndimage.label(~magenta(rgb),structure=np.ones((3,3),dtype=np.uint8)); sizes=np.bincount(labels.ravel(),minlength=n+1); sizes[0]=0
    yy,xx=np.indices(labels.shape); sx=np.bincount(labels.ravel(),weights=xx.ravel(),minlength=n+1); sy=np.bincount(labels.ravel(),weights=yy.ravel(),minlength=n+1)
    centers={i:(sx[i]/sizes[i],sy[i]/sizes[i]) for i in range(1,n+1) if sizes[i]}
    cw,ch=W/a.cols,H/a.rows; groups=[]
    for r in range(a.rows):
      for c in range(a.cols):
        candidates=[i for i,(cx,cy) in centers.items() if int(cx/cw)==c and int(cy/ch)==r]
        if not candidates: raise SystemExit(f'FAIL: empty source cell row={r+1} frame={c+1}')
        body=max(candidates,key=lambda i:sizes[i]); bc=centers[body]
        attached=[i for i,(cx,cy) in centers.items() if i==body or ((cx/cw-c-.5)**2+(cy/ch-r-.5)**2 < (0.55**2))]
        groups.append((r,c,body,attached))
    # Build per-cell source point arrays and find the largest common integer scale that fits.
    frames=[]; scale=.05
    for r,c,body,ids in groups:
      parts=[]
      for lab in ids:
        y,x=np.where(labels==lab); parts.append((x,y,lab))
      yb,xb=np.where(labels==body); low=yb.max(); tail=xb[yb>=max(yb.min(),low-5)]
      pivot=(float(tail.mean()),float(low)); frames.append((r,c,parts,pivot))
    def fits(k):
      for r,c,parts,(pivx,pivy) in frames:
        for x,y,_ in parts:
          tx=np.rint((x-pivx)*k).astype(int)+px; ty=np.rint((y-pivy)*k).astype(int)+py
          if tx.min()<smin or ty.min()<smin or tx.max()>smax or ty.max()>smax:return False
      return True
    if not fits(.05): raise SystemExit('FAIL: source content cannot fit even at scale .05')
    if a.scale is not None:
      if not fits(a.scale): raise SystemExit(f'FAIL: requested common scale {a.scale} clips outside safe area')
      scale=a.scale
    else:
      lo,hi=.05,2.0
      for _ in range(40):
        mid=(lo+hi)/2
        if fits(mid):lo=mid
        else:hi=mid
      scale=lo
    raw=np.zeros((hout,wout,4),dtype=np.uint8); logs=[]
    for r,c,parts,(pivx,pivy) in frames:
      cell=np.zeros((a.cell,a.cell,4),dtype=np.uint8)
      for x,y,lab in parts:
        tx=np.rint((x-pivx)*scale).astype(int)+px; ty=np.rint((y-pivy)*scale).astype(int)+py
        cell[ty,tx,:3]=rgb[y,x]; cell[ty,tx,3]=255
      low=int(np.where(cell[:,:,3]>0)[0].max())
      yy2,xx2=np.where((cell[:,:,3]>0)&(np.indices(cell.shape[:2])[0]>=max(0,low-5)))
      dx=int(np.rint(px-float(xx2.mean()))) if len(xx2) else 0
      dy=py-low
      shifted=np.zeros_like(cell)
      ys0=max(0,-dy);ys1=min(a.cell,a.cell-dy);xs0=max(0,-dx);xs1=min(a.cell,a.cell-dx)
      shifted[ys0+dy:ys1+dy,xs0+dx:xs1+dx]=cell[ys0:ys1,xs0:xs1]
      cell=shifted
      raw[r*a.cell:(r+1)*a.cell,c*a.cell:(c+1)*a.cell]=cell
      logs.append({'row':r+1,'frame':c+1,'source_components':[int(l) for _,_,l in parts], 'pivot_source':[round(pivx,2),round(pivy,2)],'pivot_target':[px,py],'raster_shift':[dx,dy],'scale_s':round(scale,7)})
    out=np.zeros_like(raw)
    per_row=max(1,min(24,a.colors//a.rows)) if a.id=='seeds' else a.colors
    for r in range(a.rows):
      y0=r*a.cell; row=raw[y0:y0+a.cell]
      visible=row[:,:,:3][row[:,:,3]>0]
      pal=Image.fromarray(visible.reshape(1,-1,3),'RGB').quantize(colors=per_row,method=Image.Quantize.MEDIANCUT)
      for c in range(a.cols):
        x0=c*a.cell; cell=row[:,x0:x0+a.cell]
        q=np.asarray(Image.fromarray(cell[:,:,:3],'RGB').quantize(palette=pal).convert('RGB')).copy(); q[cell[:,:,3]==0]=0
        out[y0:y0+a.cell,x0:x0+a.cell,:3]=q;out[y0:y0+a.cell,x0:x0+a.cell,3]=cell[:,:,3]
    Image.fromarray(out,'RGBA').save(folder/'final.png')
    meta={'pipeline':'garden-c-generalized-packer-v1','source':a.raw,'source_size_px':[W,H],'cols':a.cols,'rows':a.rows,'cell_px':a.cell,'canvas_px':[wout,hout],'pivot':[px,py],'safe':[smin,smax],'common_scale':round(scale,7),'resampling':'nearest-neighbor','clipped_pixels':0,'frames':logs}
    try:q=json.loads((folder/'qa.json').read_text())
    except Exception:q={}
    q['packing']=meta;(folder/'qa.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    print(f'PACKED {a.id}: raw={W}x{H}, frames={len(frames)}, scale={scale:.6f}')
if __name__=='__main__':main()
