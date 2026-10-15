"""Trích NPC (container AllNpc) của 17 map trong APK 3.2, chỉ đọc.
Cần UnityPy==1.25.3, attrs>=23. Dùng: python3 02_extract_npcs.py <APK 3.2> <portal-geometry-draft.json> <đầu ra npcs-raw.json>"""
import zipfile,os,sys,json,UnityPy,collections
APK,GEOM,OUT=sys.argv[1:4]
z=zipfile.ZipFile(APK)
env=UnityPy.load(z.read('assets/bin/Data/data.unity3d'))
g=json.load(open(GEOM,encoding='utf-8'))
vb={r['map_id']:(r['serialized_file'],r['visual_bounds']) for r in g['map_visual_records'] if r['map_id'].startswith(('city_','emerald','treasure_beach','summoning','middle_corridor'))}
byf=collections.defaultdict(dict)
for o in env.objects: byf[o.assets_file.name][o.path_id]=o
res=[]
for f in ['level2','level3','level4','level5','level11']:
    objs=byf[f]; tr={};go={}
    for pid,o in objs.items():
        if o.type.name=='Transform':
            d=o.read(); tr[pid]=(d.m_GameObject.path_id,d.m_Father.path_id,(d.m_LocalPosition.x,d.m_LocalPosition.y),(d.m_LocalScale.x,d.m_LocalScale.y))
        elif o.type.name=='GameObject':
            d=o.read(); go[pid]=(d.m_Name,[c.component.path_id for c in d.m_Component],d.m_IsActive)
    def world(t):
        chain=[]
        while t in tr and t: chain.append(t); t=tr[t][1]
        px=py=0;sx=sy=1
        for c in reversed(chain):
            lp,ls=tr[c][2],tr[c][3]; px+=lp[0]*sx; py+=lp[1]*sy; sx*=ls[0]; sy*=ls[1]
        return px,py
    def spr(gid):
        for c in go[gid][1]:
            o=objs.get(c)
            if o and o.type.name=='SpriteRenderer':
                try:
                    d=o.read(); return d.m_Sprite.read().m_Name if d.m_Sprite else None
                except Exception as e: return 'ERR'
    kids=collections.defaultdict(list)
    for t,v in tr.items(): kids[v[1]].append(t)
    an=[t for t,v in tr.items() if go[v[0]][0]=='AllNpc'][0]
    st=list(kids[an])
    while st:
        t=st.pop(0); gid=tr[t][0]; x,y=world(t)
        m=[k for k,(ff,b) in vb.items() if ff==f and b[0]-1<=x<=b[2]+1 and b[1]-1<=y<=b[3]+1]
        res.append(dict(file=f,name=go[gid][0],active=go[gid][2],sprite=spr(gid),xy=[round(x,2),round(y,2)],map=m,types=sorted({objs[c].type.name for c in go[gid][1] if c in objs}-{'Transform','GameObject'}),depth_children=len(kids[t])))
        st+=kids[t]
json.dump(res,open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
# bản lọc: chỉ NPC thật (có collider + script, nằm trong 17 map), dùng cho gen_npc_roster.py
flt=[r for r in res if 'CapsuleCollider2D' in r['types'] and r['map']]
json.dump(flt,open(os.path.join(os.path.dirname(os.path.abspath(OUT)),'npcs.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(res),'object trong AllNpc')
