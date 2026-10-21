import json,sys,zipfile
from pathlib import Path
from collections import defaultdict
import UnityPy
from PIL import Image, ImageChops
out=Path('raw'); out.mkdir(exist_ok=True)
with zipfile.ZipFile('sbw32.apk') as z:
    env=UnityPy.load(z.read('assets/bin/Data/data.unity3d'))
groups=defaultdict(list); skipped=[]
for obj in env.objects:
    if obj.type.name!='SpriteRenderer' or obj.assets_file.name!='level4': continue
    d=obj.read()
    if not d.m_Enabled or not d.m_Sprite.path_id: continue
    go=d.m_GameObject.read()
    tr=next((c.component.read() for c in go.m_Component if c.component.type.name=='Transform'),None)
    if tr is None: continue
    chain=[tr]
    while chain[-1].m_Father.path_id: chain.append(chain[-1].m_Father.read())
    root=chain[-1].m_GameObject.read().m_Name
    if root in ('AllNpc','AllEnemy','BOX','Door'): continue
    rot=any(abs(t.m_LocalRotation.z)>.0001 or abs(t.m_LocalRotation.x)>.0001 or abs(t.m_LocalRotation.y)>.0001 for t in chain)
    x=y=0; sx=sy=1
    for t in reversed(chain):
        x+=t.m_LocalPosition.x*sx; y+=t.m_LocalPosition.y*sy; sx*=t.m_LocalScale.x; sy*=t.m_LocalScale.y
    sp=d.m_Sprite.read(); im=sp.image.convert('RGBA'); ppu=sp.m_PixelsToUnits
    w,h=im.width/ppu*abs(sx),im.height/ppu*abs(sy)
    fx=bool(d.m_FlipX)!=(sx<0); fy=bool(d.m_FlipY)!=(sy<0)
    px=1-sp.m_Pivot.x if fx else sp.m_Pivot.x; py=1-sp.m_Pivot.y if fy else sp.m_Pivot.y
    if fx: im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if fy: im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    tint=tuple(round(getattr(d.m_Color,c)*255) for c in 'rgba')
    im=ImageChops.multiply(im,Image.new('RGBA',im.size,tint))
    path='/'.join(t.m_GameObject.read().m_Name for t in reversed(chain))
    groups[root].append(dict(im=im,layer=d.m_SortingLayer,order=d.m_SortingOrder,x=x-w*px,top=y+h*(1-py),w=w,h=h,name=go.m_Name,path=path,rot=rot,draw=int(d.m_DrawMode),sprite=sp.m_Name))
meta={}
for root,L in groups.items():
    print(root,len(L),'rot',sum(s['rot'] for s in L),'tiled',sum(1 for s in L if s['draw']!=0))
    L.sort(key=lambda s:(s['layer'],s['order']))
    rows=[]
    for i,s in enumerate(L):
        fn=f'{root}_{i:03d}.png'; (out/root).mkdir(exist_ok=True)
        s['im'].save(out/root/fn)
        rows.append({k:v for k,v in s.items() if k!='im'}|{'file':f'{root}/{fn}','px':s['im'].size})
    meta[root]=rows
json.dump(meta,open('raw/meta.json','w'),ensure_ascii=False,indent=1)
