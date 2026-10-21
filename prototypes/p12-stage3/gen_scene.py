import json,shutil,os,colorsys
from PIL import Image
KZ=1.5
meta=json.load(open('raw/meta.json'))
UP='/mnt/user-data/uploads/phimond/prototypes/p12-stage3/_inputs/'
os.makedirs('shared/tex',exist_ok=True)
GROUND={'1_0'}; SKY={'16_0'}
maps={}
used={}
def tex_for(s):
    key=s['sprite']
    return key
specs={'emerald_forest_main_woods':'rungsau','emerald_forest_deep_woods':'Map2'}
bounds={'emerald_forest_main_woods':[-1.98,20.74],'emerald_forest_deep_woods':[32.54,60.32]}
for mid,root in specs.items():
    L=meta[root]; props=[]; sky=[]; ground=None; bg=None
    for i,s in enumerate(L):
        im=Image.open('raw/'+s['file']).convert('RGBA')
        name=s['sprite']
        if s['sprite']=='Square':
            px=im.getpixel((1,1)); bg=[round(c/255,4) for c in px[:3]]; continue
        # unique texture per (sprite name,size,tint) -> use file hash by sprite name+px size
        fn=f"{name}_{im.width}x{im.height}.png"
        if not os.path.exists('shared/tex/'+fn): im.save('shared/tex/'+fn,optimize=True)
        cx=s['x']+s['w']/2; ybot=s['top']-s['h']
        e=dict(tex=fn,x=round(cx,3),w=round(s['w'],3),h=round(s['h'],3),ybot=round(ybot,3),top=round(s['top'],3),order=s['order'],rot=s['rot'])
        if name in GROUND: 
            e['kind']='ground'; props.append(e)
        elif name in SKY: e['kind']='sky'; props.append(e)
        else: e['kind']='prop'; props.append(e)
    skyp=[p for p in props if p['kind']=='sky']
    if skyp:
        im=Image.open('shared/tex/'+skyp[0]['tex']).convert('RGBA'); px=im.getpixel((im.width//2,im.height-2)); bg=[round(c/255,4) for c in px[:3]]
    maps[mid]=dict(root=root,bg=bg,props=props)
# build 3D layout
out={'version':1,'unitsPerPixel':0.01,'kz':KZ,'maps':{}}
for mid,m in maps.items():
    x0,x1=bounds[mid]
    g=[p for p in m['props'] if p['kind']=='ground']
    gy_top=max(p['top'] for p in g); gy_bot=min(p['ybot'] for p in g)
    zb=-KZ*gy_top; zf=-KZ*gy_bot   # back (neg z), front (pos z)
    ground=dict(tex=g[0]['tex'],x0=x0-1.0,x1=x1+1.0,zBack=round(zb,3),zFront=round(zf,3),tileW=7.49,tileD=round(5.31*KZ,3))
    items=[];sky=[]
    sorted_props=[p for p in m['props'] if p['kind']!='ground']
    for i,p in enumerate(sorted(sorted_props,key=lambda q:(q['order'],q['x']))):
        if p['kind']=='sky':
            sky.append(dict(tex=p['tex'],x=p['x'],w=p['w'],h=p['h'],y=round(p['ybot'],3))); continue
        z=-KZ*p['ybot']
        if p['order']<=-1:  # back wall: spread in depth for parallax
            z-= ((i*0.37)%1.0)*0.9
        sway = 1 if ('10_0' in p['tex'] or '9_0' in p['tex'] or '4_0' in p['tex'] or '6_0' in p['tex'] or '3_0' in p['tex'] or '2_0' in p['tex'] or '5_0' in p['tex'] or '7_0' in p['tex']) else 0
        items.append(dict(tex=p['tex'],x=p['x'],z=round(z,3),w=p['w'],h=p['h'],sway=sway,front=1 if p['order']>=1 else 0))
    out['maps'][mid]=dict(bg=m['bg'],bounds=[x0,x1],zRange=[round(zb+0.4,3),round(zf-0.2,3)],ground=ground,sky=sky,props=items)

import random,math
def decorate(mid,mp):
    rnd=random.Random(hash(mid)%100000 if False else (7 if 'main' in mid else 11))
    x0,x1=mp['bounds']; zb=mp['ground']['zBack']; zf=mp['ground']['zFront']
    size={}
    for mm in out['maps'].values():
        for p in mm['props']: size.setdefault(p['tex'],(p['w'],p['h']))
    def add(tex,x,z,scale=1.0,sway=1,front=0):
        w,h=size[tex]; mp['props'].append(dict(tex=tex,x=round(x,3),z=round(z,3),w=round(w*scale,3),h=round(h*scale,3),sway=sway,front=front,deco=1))
    T_TREE=[t for t in size if t.startswith('10_0') or t.startswith('9_0')]
    T_HEDGE=[t for t in size if t.startswith('15_0')][0]
    T_BUSH=[t for t in size if t.startswith('4_0')][0]
    T_FLOW=[t for t in size if t.startswith('6_0')][0]
    T_FERN=[t for t in size if t.startswith('3_0')][0]
    T_SMALL=[t for t in size if t.startswith('2_0')][0]
    # hàng sau xa: cây lớn mờ sương, tạo chiều sâu rừng
    x=x0-6
    while x<x1+6:
        add(rnd.choice(T_TREE),x,zb-1.6-rnd.random()*1.2,1.35+rnd.random()*0.25); x+=3.4+rnd.random()*1.4
    # hàng rào bụi sát hàng cây gốc, lấp khe hở
    x=x0-3
    while x<x1+3:
        add(T_HEDGE,x,zb+0.2+rnd.random()*0.5,0.95+rnd.random()*0.2); x+=3.3
    # khép mép trái/phải bản đồ
    for edge,sgn in ((x0,-1),(x1,1)):
        z=zb+0.3
        while z<zf+0.4:
            tx=edge+sgn*(0.9+rnd.random()*0.7)
            if z<zb+1.6: add(rnd.choice(T_TREE),tx,z,1.0+rnd.random()*0.3)
            else: add(rnd.choice([T_BUSH,T_BUSH,T_FERN]),tx,z,1.0+rnd.random()*0.35)
            z+=1.0+rnd.random()*0.5
    # rải cây nhỏ trong hai làn rìa lối đi (không chắn đường, cửa, pet)
    avoid=[(d['x'],d['z'],2.2) for d in mp.get('doors',[])]+[(mp['spawn'][0],mp['spawn'][1],1.8)]
    pets=[(q['x'],q['z'],1.8) for q in out['actors']['pets'] if q['map']==mid] if 'actors' in out else []
    n=0;tries=0
    while n<int((x1-x0)*0.9) and tries<2000:
        tries+=1
        x=x0+0.5+rnd.random()*(x1-x0-1.0)
        z=rnd.choice([zb+1.4+rnd.random()*1.0, zf-2.0+rnd.random()*1.2])
        if any(math.hypot(x-ax,(z-az)*0.7)<ar for ax,az,ar in avoid+pets): continue
        tx=rnd.choice([T_FLOW,T_FERN,T_SMALL,T_BUSH]); add(tx,x,z,0.45+rnd.random()*0.3); n+=1
# doors / arrivals (APK 3.2 geometry from Stage 2; x in world units, y in 2D units)
Y=lambda y:round(-KZ*y,3)
out['maps']['emerald_forest_main_woods']['doors']=[dict(id='to_deep',x=19.31,z=Y(0.42),to='emerald_forest_deep_woods',arrive=[37.30,Y(0.92)],label='Rừng Sâu Lục Bảo')]
out['maps']['emerald_forest_deep_woods']['doors']=[
  dict(id='to_main',x=35.62,z=Y(0.52),to='emerald_forest_main_woods',arrive=[17.0,Y(1.0)],label='Bìa Rừng Lục Bảo'),
  dict(id='to_palace_gate',x=58.40,z=Y(0.52),to=None,arrive=None,label='Cổng Hoàng cung (đường về)')]
out['maps']['emerald_forest_main_woods']['spawn']=[-1.0,0.0]  # hall arrival, door edge, left side (Stage 2, owner approved)
out['maps']['emerald_forest_deep_woods']['spawn']=[57.4,Y(0.52)]  # pillar arrival, 1 unit inside Door 2
out['actors']=dict(
  player=dict(tex='player.png',cols=6,rows=2,cell=[64,64],h=1.7,idle=[0,6],run=[6,12],fps=8),
  pets=[dict(id='species_0021',name='Xương Rồng',tex='species_0021.png',map='emerald_forest_main_woods',x=3.0,z=Y(-0.8)),
        dict(id='species_0109',name='Bọ Cạp Sa Mạc',tex='species_0109.png',map='emerald_forest_main_woods',x=6.2,z=Y(0.9)),
        dict(id='species_0071',name='Ưng Đỏ',tex='species_0071.png',map='emerald_forest_deep_woods',x=52.0,z=Y(0.2))],
  petAtlas=dict(cols=4,rows=5,cell=281,size=[1124,1405],idleRow=0,runRow=1,h=2.0,fps=6))
out['actors']['petAtlas']['feet']={}
out['camera']=dict(fov=30,pitchDeg=24,dist=16,follow=4.0)
out['tiers']=dict(low=dict(post=0,bloom=0,tilt=0,particles=0,shafts=0,sway=0),
                  medium=dict(post=1,bloom=0,tilt=1,particles=80,shafts=1,sway=1),
                  high=dict(post=1,bloom=1,tilt=1,particles=240,shafts=1,sway=1))
for mid_,mp_ in out['maps'].items(): decorate(mid_,mp_)
json.dump(out,open('shared/scene.json','w'),ensure_ascii=False,indent=1)
# player atlas 6x2 of 64x64 cells (feet at cell bottom-center)
pl=Image.new('RGBA',(64*6,64*2),(0,0,0,0))
for r,name in enumerate(['idle','run']):
    for i in range(6):
        im=Image.open(f'{UP}boy_{name}_{i}.png').convert('RGBA')
        pl.alpha_composite(im,(i*64+(64-im.width)//2,r*64+64-im.height))
pl.save('shared/tex/player.png')
for k in ['species_0021','species_0109','species_0071']: shutil.copy(UP+k+'.png',f'shared/tex/{k}.png')
print({m:(len(v['props']),len(v['sky'])) for m,v in out['maps'].items()}, os.listdir('shared/tex'))

import numpy as np
feet={}
for k in ['species_0021','species_0109','species_0071']:
    im=np.array(Image.open(f'shared/tex/{k}.png').convert('RGBA')); c=281; pads=[];ws=[]
    for f in range(4):
        ys,xs=np.where(im[0:c,f*c:(f+1)*c,3]>40); pads.append((c-1-ys.max())/c); ws.append((xs.max()-xs.min())/c)
    feet[k]=dict(pad=round(min(pads),4),w=round(float(np.mean(ws)),3))
out['actors']['petAtlas']['feet']=feet
json.dump(out,open('shared/scene.json','w'),ensure_ascii=False,indent=1)
print(feet)
