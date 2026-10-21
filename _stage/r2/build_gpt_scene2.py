import json,shutil,pathlib,re,sys
sys.path.insert(0,'tools/hd2d_audit'); import size_check
R=pathlib.Path('.').resolve()
art=R/'apps/game-web/art-src/hd2d/batch-11-desert'
tex=R/'apps/game-web/public/scenes/tex'
M={a['id']:a for a in json.load(open(art/'manifest.json'))['assets']}
L=json.load(open(R/'.ai/design/map-layouts/desert/desert_entrance.json'))
def cp(i):
    shutil.copyfile(art/i/'final.png',tex/f'gpt_{i}.png'); return f'gpt_{i}.png'
def W(px,py): return round(px/100,3), round((py-560)/100*1.1,3)
clamped=set();props=[];flats=[];back=[];skipped=[]
for k in range(-1,3):
    back.append(dict(tex=cp('desert-dunes-wall-far'),x=round(6+k*20,3),y=-0.45,z=-3.8,w=20,h=6))
for k in range(-2,4):
    back.append(dict(tex=cp('desert-dunes-mid'),x=4+k*10,y=-0.25,z=-3.4,w=10,h=3))
for k in range(-2,4):
    back.append(dict(tex=cp('desert-ruins-near'),x=4+k*10,y=-0.10,z=-3.0,w=10,h=3))
for p in L['placements']:
    a=M.get(p['asset'])
    if not a: skipped.append(p['asset']); continue
    x,z=W(*p['px']); sc=p.get('scale',1.0)
    if a['category']=='prop':
        rx,r=size_check.cls(a['id'])
        if r:
            k=min(1.0,r[1]/(a['world'][1]*sc),r[2]/(a['world'][0]*sc)); sc*=k*0.92
            clamped.add(a['id'])
    w=round(a['world'][0]*sc,3); h=round(a['world'][1]*sc,3)
    t=cp(a['id'])
    if a['category'] in('decal','shadow'):
        fz=round(z-h*0.2,3) if a['category']=='shadow' else z
        flats.append(dict(tex=t,x=x,z=fz,w=w,d=h))
    elif a['category'].startswith('backdrop') or a['category']=='floor': continue
    else:
        e=dict(tex=t,x=x,z=z,w=w,h=h)
        if p.get('sway'): e['sway']=1
        props.append(e)
ex,ez=W(1220,510)
shutil.copyfile(R/'apps/game-web/art-src/hd2d/batch-05-octopath/player-female/final.png',tex/'gpt_npc.png')
props.append(dict(tex='gpt_npc.png',x=ex,z=ez,w=1.31,h=1.31,bob=1))
props.sort(key=lambda p:p['z']);flats.sort(key=lambda f:f['z'])
S=json.load(open(R/'apps/game-web/public/scenes/desert_entrance_hd2d.json'))
S.update(id='desert_entrance_gpt2',name='desert gpt',flats=flats,back=back,props=props,
 floor=[dict(tex=cp('desert-sand-floor-01'),x0=-10,x1=35,z0=-9,z1=6,tw=4,td=4)])
json.dump(S,open(R/'apps/game-web/public/scenes/desert_entrance_gpt2.json','w'),indent=1)
print('clamped',sorted(clamped));print(len(props),len(flats),'skipped',len(skipped),sorted(set(skipped)))
