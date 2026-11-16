"""Measure alpha components only. Never edits image pixels."""
from pathlib import Path
import json,sys
import numpy as np
from PIL import Image
p=Path(__file__).resolve().parent
names=sys.argv[1:] or [a['id'] for a in json.loads((p/'manifest.json').read_text())['assets'] if a.get('category')=='prop']
for n in names:
 d=p/n;a=np.asarray(Image.open(d/'final.png'))[:,:,3]>0;seen=np.zeros_like(a);counts=[];H,W=a.shape
 for y,x in zip(*np.where(a)):
  if seen[y,x]:continue
  seen[y,x]=1;todo=[(y,x)];count=0
  while todo:
   yy,xx=todo.pop();count+=1
   for dy,dx in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
    ny,nx=yy+dy,xx+dx
    if 0<=ny<H and 0<=nx<W and a[ny,nx] and not seen[ny,nx]:seen[ny,nx]=1;todo.append((ny,nx))
  counts.append(count)
 q=json.loads((d/'qa.json').read_text());q['connected_components_8way']=sorted(counts,reverse=True);q['stray_components_below12']=sum(1 for v in counts if v<12);q['failures']=[x for x in q['failures'] if x!='STRAY_COMPONENTS_LT12']
 if q['stray_components_below12']:q['failures'].append('STRAY_COMPONENTS_LT12')
 (d/'qa.json').write_text(json.dumps(q,indent=2));print(n,'small components',q['stray_components_below12'],q['failures'])
