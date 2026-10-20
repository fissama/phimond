"""Read-only APK/JAR audit; writes only P13 evidence. Existing UnityPy env."""
import hashlib, io, json, struct, zipfile, gzip
from pathlib import Path
import UnityPy
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'.ai/plan/phases/P13-skills/evidence'
DOWNLOADS=Path('/Users/phileanh/Downloads')

def audit_apk(filename, version):
    path=DOWNLOADS/filename
    with zipfile.ZipFile(path) as outer:
        apk=zipfile.ZipFile(io.BytesIO(outer.read('com.HCGame.SpiritBeastWorld.apk'))) if filename.endswith('.xapk') else outer
        metadata=apk.read('assets/bin/Data/Managed/Metadata/global-metadata.dat')
        env=UnityPy.load(apk.read('assets/bin/Data/data.unity3d'))
    objects=[]
    for obj in env.objects:
        if obj.type.name!='MonoBehaviour':continue
        try:
            if obj.read(check_read=False).m_Script.read().m_ClassName=='DataSkill':objects.append(obj)
        except Exception:continue
    assert len(objects)==1
    obj=objects[0]; blob=obj.get_raw_data(); pos=28
    def integer():
        nonlocal pos
        value=struct.unpack_from('<i',blob,pos)[0];pos+=4;return value
    def string():
        nonlocal pos
        size=integer();assert 0<=size<=len(blob)-pos
        value=blob[pos:pos+size].decode('utf8');pos=(pos+size+3)//4*4;return value
    name=string();count=integer();rows=[]
    for _ in range(count):
        row={'offset':pos,'id':string(),'name':string()}
        for k in ('TypeChoose','TypesSkill','HeSkill','TypeCombat','TypeLoai','BuffType'):row[k]=integer()
        n=integer();assert 0<=n<=200
        row['requirements']=[{k:integer() for k in ('levelHoc','Mana','Gia','Dame')} for _ in range(n)]
        row['description']=string();rows.append(row)
    assert pos==len(blob)
    assert len({r['id'] for r in rows})==count
    return {'version':version,'source':str(path),'sha256':hashlib.file_digest(path.open('rb'),'sha256').hexdigest(),
            'metadata_version':struct.unpack_from('<I',metadata,4)[0], 'asset':obj.assets_file.name,'path_id':obj.path_id,
            'asset_name':name,'byte_length':len(blob),'bytes_consumed':pos,'record_count':count,'rows':rows,
            'limits':['Client requirement fields are raw serialized values. Encoding/units/runtime/server behavior not recovered; do not treat Mana1029 or Dame120 as certified costs/formulas.']}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    reports=[]
    for f,v in [('Spirit Beast World 3.2.apk','3.2'),('Spirit Beast World 8.4 (1).xapk','8.4')]:
        r=audit_apk(f,v);reports.append(r)
        (OUT/f'apk{v.replace(".","")}-skills.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    a,b=reports;old={r['id']:r for r in a['rows']};diff=[]
    for r in b['rows']:
        before=old[r['id']];changes={k:{'apk32':before[k],'apk84':r[k]} for k in r if k!='offset' and before[k]!=r[k]}
        if changes:diff.append({'id':r['id'],'changes':changes})
    jar=DOWNLOADS/'Pokezoo 100.jar'
    with zipfile.ZipFile(jar) as z:
        probes=[]
        for name,texts in [('l.class',['ngủ say','hỗn loạn','trầm lặng','kỹ năng chủng tộc']),('ui_learnskill.ui',['Kỹ năng đã đầy','Quên kỹ năng','Đang mua dung lượng kỹ năng']),('ui_newplayerhelp.ui',['kỹ năng sát thương tập thể'])]:
            raw=z.read(name)
            if raw.startswith(b'\x1f\x8b'):raw=gzip.decompress(raw)
            for text in texts:probes.append({'entry':name,'text':text,'offset':raw.find(text.encode('utf8'))})
        manifest=z.read('META-INF/MANIFEST.MF').decode('utf8')
    out={'apk_versions':[{'version':r['version'],'sha256':r['sha256'],'rows':r['record_count'],'byte_length':r['byte_length'],'bytes_consumed':r['bytes_consumed']} for r in reports],
         'same_source_ids':set(old)=={r['id'] for r in b['rows']},'changed_records':len(diff),'differences':diff,
         'jar':{'path':str(jar),'sha256':hashlib.file_digest(jar.open('rb'),'sha256').hexdigest(),'manifest':manifest,'byte_probes':probes},
         'classification':{'catalog':'observed client serialization','race_signatures':'observed client descriptions','server_formulas':'unknown','phimond_candidate':'authored pending owner acceptance'}}
    (OUT/'source-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'apk_rows':[r['record_count'] for r in reports],'changed_records':len(diff),'jar_probes':len(probes),'all_probes_found':all(p['offset']>=0 for p in probes)}))

if __name__=='__main__':main()
