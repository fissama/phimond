#!/usr/bin/env python3
"""Mechanical gates for garden-c seeds and thirsty bubble atlases."""
import argparse,json
from pathlib import Path
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
def iou(a,b):
 u=np.count_nonzero(a|b); return 1 if not u else np.count_nonzero(a&b)/u
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--id',choices=['seeds','bubble-thirsty'],required=True);a=ap.parse_args();p=ROOT/a.id
 q={}; im=Image.open(p/'final.png').convert('RGBA');arr=np.asarray(im); masks=[];colors=set(); alpha=sorted(np.unique(arr[:,:,3]).tolist())
 if a.id=='seeds': cols,rows,cell,pivot,safe,total=4,6,64,(32,56),4,60
 else: cols,rows,cell,pivot,safe,total=4,1,64,(32,60),4,24
 checks={};checks['a']=bool(im.size==(cols*cell,rows*cell) and alpha==[0,255] and np.all(arr[arr[:,:,3]==0,:3]==0))
 print(('PASS' if checks['a'] else 'FAIL')+' a: size/alpha/hiddenRGB',im.size,alpha,int(np.count_nonzero(arr[arr[:,:,3]==0,:3])))
 boxes=[]
 for r in range(rows):
  for c in range(cols):
   cellarr=arr[r*cell:(r+1)*cell,c*cell:(c+1)*cell]; m=cellarr[:,:,3]>0;masks.append(m); ys,xs=np.where(m); boxes.append(None if not len(xs) else [int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]);colors.update(map(tuple,cellarr[:,:,:3][m].tolist()))
 frames=[arr[r*cell:(r+1)*cell,c*cell:(c+1)*cell].tobytes() for r in range(rows) for c in range(cols)]
 checks['b']=bool(all(m.any() for m in masks) and len(set(frames))==len(frames));print(('PASS' if checks['b'] else 'FAIL')+f" b: nonempty={sum(m.any() for m in masks)}/{len(masks)}, unique={len(set(frames))}/{len(masks)}")
 violations=[]
 for i,m in enumerate(masks):
  y,x=np.where(m)
  if len(x) and (x.min()<safe or y.min()<safe or x.max()>cell-1-safe or y.max()>cell-1-safe):violations.append((i//cols+1,i%cols+1,boxes[i]))
 checks['c']=bool(not violations);print(('PASS' if checks['c'] else 'FAIL')+f' c: violations={violations}')
 checks['d']=bool(len(colors)<=total);print(('PASS' if checks['d'] else 'FAIL')+f' d: total_colors={len(colors)} (≤{total})')
 if a.id=='seeds':
  per=[];mins=[]
  for r in range(rows):
   rowcolors=set();rowm=masks[r*cols:(r+1)*cols]
   for c in range(cols):
    m=rowm[c];y,x=np.where(m); 
    if len(x):
     # bottom pivot of the mound; exact prescribed target
     low=y.max(); tail=x[y>=max(y.min(),low-5)]; cx=float(tail.mean()); mins.append((r+1,c+1,cx,low))
    rowcolors.update(map(tuple,arr[r*cell:(r+1)*cell,c*cell:(c+1)*cell,:3][m].tolist()))
   per.append(len(rowcolors))
  checks['e']=bool(all(abs(x-pivot[0])<=1 and y==pivot[1] for _,_,x,y in mins));print(('PASS' if checks['e'] else 'FAIL')+f' e: pivot={mins}')
  checks['f']=bool(max(per,default=0)<=24);print(('PASS' if checks['f'] else 'FAIL')+f' f: colors_per_family_row={per} (≤24)')
  vals=[iou(masks[r*cols+c],masks[r*cols+(c+1)%cols]) for r in range(rows) for c in range(cols)];checks['g']=bool(min(vals,default=0)>=.90);print(('PASS' if checks['g'] else 'FAIL')+f' g: minimum_adjacent_IoU={min(vals,default=0):.4f} (≥0.90)')
 else:
  tails=[]; tops=[]
  for c in range(4):
   m=masks[c]; y,x=np.where(m)
   if len(x):
    low=int(y.max()); tail=x[y==low]; tails.append((float(tail.mean()),low));tops.append(int(y.min()))
  checks['e']=bool(len(tails)==4 and all(abs(x-32)<=1 and abs(y-60)<=1 for x,y in tails))
  print(('PASS' if checks['e'] else 'FAIL')+f' e: tail-tip anchors={tails}; intended pivot (32,60), visible tip y=59 due safe margin')
  bob_steps=[abs(tops[i+1]-tops[i]) for i in range(len(tops)-1)]
  checks['f']=bool(len(bob_steps)==3 and all(2<=d<=3 for d in bob_steps))
  print(('PASS' if checks['f'] else 'FAIL')+f' f: adjacent bubble bob steps={bob_steps} px (each 2–3 px), top_y={tops}')
 q={'size_px':list(im.size),'alpha_values':alpha,'hidden_rgb_zero':bool(np.all(arr[arr[:,:,3]==0,:3]==0)),'total_colors':len(colors),'checks':checks,'all_pass':all(checks.values()),'asset_id':a.id}
 (p/'qa.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print('RESULT',a.id, sum(checks.values()),'/',len(checks))
if __name__=='__main__':main()
