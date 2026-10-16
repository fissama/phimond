"""Local P12 owner review UI. No game/DB mutations; persisted owner feedback."""
import argparse
from datetime import datetime, timezone
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import re
from pathlib import Path
import threading
from urllib.parse import urlsplit, parse_qs

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PHASE=ROOT/'.ai/plan/phases/P12-world'
STATUSES={'pending','approved','changes_requested','rejected'}
VERDICTS={'draft','approved','changes_requested','rejected'}
DOCUMENTS={'P12-closure-checklist.md','stage4/P12-S4-design.md','stage4/P12-S4-npc-roster.md','stage4/P12-S4-portal-matrix.md','README.md'}

class ReviewServer(ThreadingHTTPServer):
    daemon_threads=True
    def __init__(self,address,package,responses,images=None):
        self.package_path=Path(package);self.responses=Path(responses);self.lock=threading.RLock()
        self.images=Path(images) if images else None;self.portal_pkg=self.package_path.parent/'portal-package.json';self.portal_edit=self.package_path.parent/'portal-edits'/'portal-graph.json'
        super().__init__(address,Handler)
    def package(self):
        raw=self.package_path.read_bytes()
        return json.loads(raw),hashlib.sha256(raw).hexdigest()
    def feedback(self,p,sha):
        path=self.responses/(sha+'.json')
        if path.exists():return json.loads(path.read_text())
        return {'package_hash':sha,'revision':p['revision'],'version':0,'verdict':'draft','notes':'',
                'decisions':{d['id']:{'status':'pending','comment':''} for d in p['decisions']},'history':[],'updated_at':None}
    def portal_base(self):
        raw=self.portal_pkg.read_bytes();return json.loads(raw),hashlib.sha256(raw).hexdigest()
    def portal_state(self):
        pkg,h=self.portal_base()
        if self.portal_edit.exists():
            e=json.loads(self.portal_edit.read_text(encoding='utf-8'));return {'maps':pkg['maps'],'package_hash':h,'version':e['version'],'graph':e['graph'],'base_changed':e['base_hash']!=h,'updated_at':e.get('updated_at'),'notes':pkg.get('notes','')}
        return {'maps':pkg['maps'],'package_hash':h,'version':0,'graph':{'ports':pkg['ports'],'links':pkg['links']},'base_changed':False,'updated_at':None,'notes':pkg.get('notes','')}
    def save_portals(self,payload):
        with self.lock:
            st=self.portal_state()
            if type(payload.get('version')) is not int or payload['version']!=st['version']:return 409,{'error':'Một tab khác đã lưu đồ thị mới. Tải lại trang trước khi sửa tiếp.'}
            g=payload.get('graph');pkg,h=self.portal_base();mids={m['id'] for m in pkg['maps']}
            if not isinstance(g,dict) or not isinstance(g.get('ports'),list) or not isinstance(g.get('links'),list) or len(g['ports'])>2000 or len(g['links'])>2000:return 400,{'error':'Đồ thị không hợp lệ.'}
            pid=set()
            for p in g['ports']:
                if not isinstance(p,dict) or not isinstance(p.get('id'),str) or p['id'] in pid or p.get('map') not in mids or p.get('kind') not in {'door','pillar','arrival'}:return 400,{'error':'Điểm dịch chuyển không hợp lệ.'}
                xy=p.get('xy')
                if not isinstance(xy,list) or len(xy)!=2 or any(type(v) not in (int,float) for v in xy):return 400,{'error':'Tọa độ không hợp lệ.'}
                if not isinstance(p.get('label'),str) or len(p['label'])>200:return 400,{'error':'Nhãn không hợp lệ.'}
                pid.add(p['id'])
            lid=set()
            for l in g['links']:
                if not isinstance(l,dict) or not isinstance(l.get('id'),str) or l['id'] in lid or l.get('a') not in pid or l.get('b') not in pid or l['a']==l['b']:return 400,{'error':'Liên kết không hợp lệ.'}
                if l.get('status') not in STATUSES or not isinstance(l.get('comment'),str) or len(l['comment'])>5000 or type(l.get('oneway')) is not bool:return 400,{'error':'Trạng thái liên kết không hợp lệ.'}
                lid.add(l['id'])
            new={'version':st['version']+1,'base_hash':h,'updated_at':datetime.now(timezone.utc).isoformat(),'source':'owner_web_review','graph':g}
            if self.portal_edit.exists():
                hist=self.portal_edit.parent/'history';hist.mkdir(parents=True,exist_ok=True);(hist/f"v{st['version']:04d}.json").write_text(self.portal_edit.read_text(encoding='utf-8'),encoding='utf-8')
            self.portal_edit.parent.mkdir(parents=True,exist_ok=True);tmp=self.portal_edit.with_suffix('.tmp')
            tmp.write_text(json.dumps(new,ensure_ascii=False,indent=1)+'\n',encoding='utf-8');tmp.replace(self.portal_edit)
            return 200,{'saved':True,'version':new['version'],'updated_at':new['updated_at']}
    def save(self,payload):
        with self.lock:
            p,sha=self.package()
            if payload.get('package_hash')!=sha:return 409,{'error':'Bản thiết kế đã đổi. Tải lại trang để xem phiên bản mới; phản hồi cũ vẫn được giữ.'}
            old=self.feedback(p,sha)
            if type(payload.get('version')) is not int or payload['version']!=old['version']:return 409,{'error':'Một tab khác đã lưu phản hồi mới. Tải lại trang trước khi sửa tiếp.'}
            ids={d['id'] for d in p['decisions']};dec=payload.get('decisions')
            if not isinstance(dec,dict) or set(dec)!=ids:return 400,{'error':'Danh sách quyết định không hợp lệ.'}
            for x in dec.values():
                if not isinstance(x,dict) or set(x)!={'status','comment'} or x['status'] not in STATUSES or not isinstance(x['comment'],str) or len(x['comment'])>10000:return 400,{'error':'Trạng thái hoặc góp ý không hợp lệ.'}
            notes=payload.get('notes');verdict=payload.get('verdict')
            if not isinstance(notes,str) or len(notes)>20000 or verdict not in VERDICTS:return 400,{'error':'Kết luận hoặc góp ý chung không hợp lệ.'}
            if verdict=='approved' and any(x['status']!='approved' for x in dec.values()):return 400,{'error':'Cần duyệt tất cả nhóm quyết định trước khi nghiệm thu toàn bộ.'}
            changed=dec!=old['decisions'] or notes!=old['notes']
            if old['verdict']!='draft' and changed and verdict!='draft':return 400,{'error':'Nội dung phản hồi đã sửa. Lưu nháp trước rồi gửi lại kết luận.'}
            history=list(old.get('history',[]))
            if old['verdict']!='draft' and (changed or verdict!=old['verdict']):
                history.append({k:v for k,v in old.items() if k!='history'})
            new={'package_hash':sha,'revision':p['revision'],'version':old['version']+1,'verdict':verdict,'notes':notes,
                 'decisions':dec,'updated_at':datetime.now(timezone.utc).isoformat(),'source':'owner_web_review','history':history}
            self.responses.mkdir(parents=True,exist_ok=True);path=self.responses/(sha+'.json');tmp=path.with_suffix('.tmp')
            tmp.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n');tmp.replace(path)
            return 200,{'saved':True,'feedback':new}

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def send(self,status,value,mime='application/json; charset=utf-8'):
        raw=json.dumps(value,ensure_ascii=False).encode() if isinstance(value,(dict,list)) else value
        self.send_response(status);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(raw)))
        self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'")
        self.end_headers();self.wfile.write(raw)
    def do_GET(self):
        host=self.headers.get('Host','');port=self.server.server_port
        if host not in {f'127.0.0.1:{port}',f'localhost:{port}'}:return self.send(403,{'error':'Host không hợp lệ.'})
        path=urlsplit(self.path).path
        if path in ('/','/index.html','/app.js','/style.css','/portals.html','/portals.js','/portals.css'):
            name='index.html' if path=='/' else path[1:]
            if not (HERE/name).exists():return self.send(404,{'error':'Không tìm thấy giao diện.'})
            return self.send(200,(HERE/name).read_bytes(),{'index.html':'text/html; charset=utf-8','app.js':'text/javascript; charset=utf-8','style.css':'text/css; charset=utf-8','portals.html':'text/html; charset=utf-8','portals.js':'text/javascript; charset=utf-8','portals.css':'text/css; charset=utf-8'}[name])
        if path=='/api/review':
            with self.server.lock:
                p,sha=self.server.package();return self.send(200,{'package':p,'package_hash':sha,'feedback':self.server.feedback(p,sha)})
        if path=='/api/portals':
            with self.server.lock:return self.send(200,self.server.portal_state())
        if path.startswith('/map-images/') and path.endswith('.png'):
            mid=path[12:-4]
            if self.server.images and re.fullmatch(r'[a-z0-9_]+',mid) and (self.server.images/(mid+'.png')).is_file():return self.send(200,(self.server.images/(mid+'.png')).read_bytes(),'image/png')
            return self.send(404,{'error':'Không có ảnh map.'})
        if path=='/healthz':return self.send(200,{'status':'ok','service':'P12 review'})
        if path=='/api/document':
            name=parse_qs(urlsplit(self.path).query).get('name',[''])[0]
            if name in DOCUMENTS and (PHASE/name).is_file():return self.send(200,{'name':name,'text':(PHASE/name).read_text(encoding='utf-8')})
        return self.send(404,{'error':'Không tìm thấy.'})
    def do_POST(self):
        route=urlsplit(self.path).path
        if route not in ('/api/feedback','/api/portals'):return self.send(404,{'error':'Không tìm thấy.'})
        host=self.headers.get('Host','');port=self.server.server_port
        if host not in {f'127.0.0.1:{port}',f'localhost:{port}'}:return self.send(403,{'error':'Host không hợp lệ.'})
        origin=self.headers.get('Origin')
        if origin and origin!='http://'+host:return self.send(403,{'error':'Origin không hợp lệ.'})
        if self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.send(415,{'error':'Cần JSON.'})
        try:
            n=int(self.headers.get('Content-Length','0'))
            if not 0<n<=(2000000 if route=='/api/portals' else 512000):raise ValueError('Nội dung quá lớn hoặc rỗng.')
            payload=json.loads(self.rfile.read(n))
            if not isinstance(payload,dict):raise ValueError('Cần một JSON object.')
            status,value=(self.server.save_portals if route=='/api/portals' else self.server.save)(payload);return self.send(status,value)
        except (ValueError,TypeError,KeyError) as e:return self.send(400,{'error':str(e)})
        except OSError:return self.send(500,{'error':'Chưa ghi được file phản hồi. Nội dung trên trang vẫn giữ; hãy thử lại.'})

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--port',type=int,default=8134);ap.add_argument('--package',type=Path,default=PHASE/'review/review-package.json');ap.add_argument('--images',type=Path,default=next((Path(p).expanduser() for p in ('~/Downloads/Phimond-P12-Review/map-images','~/mnt/Downloads/Phimond-P12-Review/map-images') if Path(p).expanduser().exists()),None));ap.add_argument('--responses',type=Path,default=PHASE/'review/responses')
    args=ap.parse_args();s=ReviewServer(('127.0.0.1',args.port),args.package,args.responses,args.images)
    print(f'P12 review http://127.0.0.1:{s.server_port} | PID file not needed | responses {s.responses}',flush=True)
    try:s.serve_forever()
    except KeyboardInterrupt:pass
    finally:s.server_close()
if __name__=='__main__':main()
