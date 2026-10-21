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
out['camera']=dict(fov=30,pitchDeg=24,dist=16,follow=4.0)
out['tiers']=dict(low=dict(post=0,bloom=0,tilt=0,particles=0,shafts=0,sway=0),
                  medium=dict(post=1,bloom=0,tilt=1,particles=80,shafts=1,sway=1),
                  high=dict(post=1,bloom=1,tilt=1,particles=240,shafts=1,sway=1))
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
