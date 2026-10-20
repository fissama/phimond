"""Local P13 acceptance UI. No game/DB mutations; persisted owner feedback."""
import argparse
from datetime import datetime, timezone
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
from urllib.parse import urlsplit, parse_qs

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PHASE=ROOT/'.ai/plan/phases/P13-skills'
STATUSES={'pending','approved','changes_requested','rejected'}
VERDICTS={'draft','approved','changes_requested','rejected'}
DOCUMENTS={'P13-owner-feedback-v7.md','P13-to-P10-eight-species-prompt.md','P13-roster-review-v6.md','P13-roster-review-v4.md','P13-final-spec.md','P13-source-audit.md','P13-behavior-contract.md','P13-verification.md','P13-owner-feedback-v2.md','P13-owner-feedback-v3.md','README.md'}

class ReviewServer(ThreadingHTTPServer):
    daemon_threads=True
    def __init__(self,address,package,responses):
        self.package_path=Path(package);self.responses=Path(responses);self.lock=threading.RLock()
        super().__init__(address,Handler)
    def package(self):
        raw=self.package_path.read_bytes()
        return json.loads(raw),hashlib.sha256(raw).hexdigest()
    def feedback(self,p,sha):
        path=self.responses/(sha+'.json')
        if path.exists():return json.loads(path.read_text())
        return {'package_hash':sha,'revision':p['revision'],'version':0,'verdict':'draft','notes':'',
                'decisions':{d['id']:{'status':'pending','comment':''} for d in p['decisions']},'history':[],'updated_at':None}
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
        if path in ('/','/index.html','/app.js','/style.css'):
            name='index.html' if path=='/' else path[1:]
            if not (HERE/name).exists():return self.send(404,{'error':'Không tìm thấy giao diện.'})
            return self.send(200,(HERE/name).read_bytes(),{'index.html':'text/html; charset=utf-8','app.js':'text/javascript; charset=utf-8','style.css':'text/css; charset=utf-8'}[name])
        if path=='/api/review':
            with self.server.lock:
                p,sha=self.server.package();return self.send(200,{'package':p,'package_hash':sha,'feedback':self.server.feedback(p,sha)})
        if path=='/healthz':return self.send(200,{'status':'ok','service':'P13 review'})
        if path=='/api/document':
            name=parse_qs(urlsplit(self.path).query).get('name',[''])[0]
            if name in DOCUMENTS and (self.server.package_path.parent/name).is_file():return self.send(200,{'name':name,'text':(self.server.package_path.parent/name).read_text()})
        return self.send(404,{'error':'Không tìm thấy.'})
    def do_POST(self):
        if urlsplit(self.path).path!='/api/feedback':return self.send(404,{'error':'Không tìm thấy.'})
        host=self.headers.get('Host','');port=self.server.server_port
        if host not in {f'127.0.0.1:{port}',f'localhost:{port}'}:return self.send(403,{'error':'Host không hợp lệ.'})
        origin=self.headers.get('Origin')
        if origin and origin!='http://'+host:return self.send(403,{'error':'Origin không hợp lệ.'})
        if self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.send(415,{'error':'Cần JSON.'})
        try:
            n=int(self.headers.get('Content-Length','0'))
            if not 0<n<=512000:raise ValueError('Nội dung quá lớn hoặc rỗng.')
            payload=json.loads(self.rfile.read(n))
            if not isinstance(payload,dict):raise ValueError('Cần một JSON object.')
            status,value=self.server.save(payload);return self.send(status,value)
        except (ValueError,TypeError,KeyError) as e:return self.send(400,{'error':str(e)})
        except OSError:return self.send(500,{'error':'Chưa ghi được file phản hồi. Nội dung trên trang vẫn giữ; hãy thử lại.'})

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--port',type=int,default=8133);ap.add_argument('--package',type=Path,default=PHASE/'review-package.json');ap.add_argument('--responses',type=Path,default=PHASE/'review/responses')
    args=ap.parse_args();s=ReviewServer(('127.0.0.1',args.port),args.package,args.responses)
    print(f'P13 review http://127.0.0.1:{s.server_port} | PID file not needed | responses {s.responses}',flush=True)
    try:s.serve_forever()
    except KeyboardInterrupt:pass
    finally:s.server_close()
if __name__=='__main__':main()
