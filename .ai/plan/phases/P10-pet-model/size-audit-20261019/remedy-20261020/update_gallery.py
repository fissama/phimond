"""Publish a local evidence index; never changes selections or gameplay."""
import hashlib,html,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[6]
OUT=Path(__file__).resolve().parent
audit=json.loads((OUT.parent/'measurements.json').read_text())['records']
progress=json.loads((OUT/'progress.json').read_text())
states={r['id']:r for r in progress['records']}
owner_file=OUT/'owner-review-20261021.json'
owner_states={r['id']:r for r in json.loads(owner_file.read_text())['records']} if owner_file.exists() else {}
snapshot=OUT/'sources';snapshot.mkdir(exist_ok=True)
cards=[];summary=[]
for r in audit:
    sid=r['id'];src=ROOT/r['path'];dest=snapshot/(sid+'.png')
    if not dest.exists():shutil.copyfile(src,dest)
    assert hashlib.sha256(dest.read_bytes()).hexdigest()==r['sha256']
    state=states.get(sid,{'status':'control_preview_rechecked_pending_owner'})
    candidate=state.get('candidate');after='sources/'+sid+'.png';link='';newh='—'
    if candidate:
        folder=Path(candidate).parent
        evidence=OUT/sid/folder.name
        if (evidence/'after.png').exists():
            after=f'{sid}/{folder.name}/after.png'
            link=f'<a href="{sid}/{folder.name}/">20 frame + playback + so sánh</a>'
            m=json.loads((ROOT/folder/'metadata.json').read_text())
            newh=round(sum(f['opaque_h'] for f in m['metrics']['after'][:4])/4,2)
    status=state['status']
    if sid in owner_states:status=owner_states[sid]['status']
    cards.append(f'''<article><h2>{html.escape(r['name'])} <small>{sid} · {r['star']}★</small></h2><p>{html.escape(status)} · H idle {r['idle_solid_h']} → {newh}px</p><div class="line"><figure><figcaption>Cũ</figcaption><canvas data-src="sources/{sid}.png"></canvas></figure><figure><figcaption>{'Candidate mới' if candidate else 'Nguồn giữ nguyên — xem profile stage'}</figcaption><canvas data-src="{after}"></canvas></figure><figure><figcaption>Linh Tiên chuẩn</figcaption><canvas data-src="sources/species_0144.png"></canvas></figure></div>{link} · <a href="scale-trials/#{sid}">So size hiển thị đề xuất</a></article>''')
    summary.append({'id':sid,'status':status,'candidate':candidate,'old_idle_h':r['idle_solid_h'],'new_idle_h':newh})
(OUT/'gallery.json').write_text(json.dumps({'scope':'56 species preview package; owner and runtime gates pending','runtime_activated':False,'records':summary},ensure_ascii=False,indent=2))
counts={s:sum(r['status']==s for r in summary) for s in sorted(set(r['status'] for r in summary))}
page='''<!doctype html><meta charset="utf-8"><title>Phimond size remedy — tiến độ 56 loài</title><style>body{background:#171f2b;color:#e2eaf4;font:16px system-ui;max-width:1100px;margin:24px auto;padding:16px}a{color:#97d2ff}article{padding:20px;border:1px solid #465468;margin:16px 0}h2{font-size:20px}small{font-size:13px;color:#b1c0d3}figure{margin:8px}.line{display:flex;gap:8px;flex-wrap:wrap}canvas{width:192px;height:192px;image-rendering:pixelated;background:#253041}button,select{font:inherit;padding:6px;margin:8px}.bar{position:sticky;top:0;background:#171f2b;padding:12px;border:1px solid #465468}</style><h1>Size remedy — 56 loài 4★/5★</h1><p><a href="closure-160/">REDRAW160 — CLOSED21/10/2026</a></p><p><a href="species_0147/art-redo-20261021/">Người Tuyết: art vẽ lại theo APK ngày21/10</a></p><p>Gói preview: 3 atlas mới, 29 target scale-only, 24 đối chứng. Chủ game đã duyệt đủ160loài, gồm Người Tuyết attempt13 theo APK; redraw art đóng21/10/2026. Chưa runtime. Canvas bên dưới so pixel atlas; khác biệt scale-only xem ở trang stage.</p><p>COUNTS</p><p><a href="owner-review-20261021.json">Duyệt của chủ game 2026-10-21</a> · <a href="delivery-20261021.md">Báo cáo trước lượt duyệt</a> · <a href="scale-trials/">So size stage 96/192</a> · <a href="scale-trials/playback.html">Playback 56 loài theo nhóm</a> · <a href="gallery.json">Trạng thái / số đo</a> · <a href="ledger.md">Nhật ký</a></p><div class="bar"><label>Ô hiển thị <select id="size"><option>96</option><option selected>192</option><option>281</option></select></label><label>Hàng <select id="row"><option value="0">Idle</option><option value="1">Movement</option><option value="2">Basic</option><option value="3">Skill</option><option value="4">Down</option></select></label><label>Frame <select id="frame"><option value="0">1</option><option value="1">2</option><option value="2">3</option><option value="3">4</option></select></label><button id="bg">Light / dark</button></div>CARDS<script>const size=document.getElementById('size'),row=document.getElementById('row'),frame=document.getElementById('frame');let light=false;const entries=[...document.querySelectorAll('canvas')].map(c=>{const im=new Image();im.src=c.dataset.src;im.onload=draw;return{c,im}});function draw(){const n=+size.value;for(const{c,im}of entries){c.width=c.height=n;c.style.width=c.style.height=n+'px';const x=c.getContext('2d');x.imageSmoothingEnabled=false;x.fillStyle=light?'#dce4ed':'#253041';x.fillRect(0,0,n,n);if(im.complete&&im.naturalWidth)x.drawImage(im,281*(+frame.value),281*(+row.value),281,281,0,0,n,n)}}size.onchange=row.onchange=frame.onchange=draw;document.getElementById('bg').onclick=()=>{light=!light;draw()};draw();</script>'''
(OUT/'index.html').write_text(page.replace('CARDS',''.join(cards)).replace('COUNTS',html.escape(json.dumps(counts,ensure_ascii=False))))
print(json.dumps(counts))
