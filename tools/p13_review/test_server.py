import json, tempfile, unittest, threading
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from server import ReviewServer

class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.package=self.root/'package.json';self.package.write_text(json.dumps({'decisions':[{'id':'P13-D01'},{'id':'P13-D02'}],'revision':'test'}))
        self.start()
    def start(self):
        self.server=ReviewServer(('127.0.0.1',0),self.package,self.root/'responses')
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.url='http://127.0.0.1:'+str(self.server.server_port)
    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.tmp.cleanup()
    def request(self,path,data=None,headers=None):
        req=Request(self.url+path,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json',**(headers or {})})
        try:
            with urlopen(req) as r:return r.status,json.load(r)
        except HTTPError as e:
            with e:return e.code,json.load(e)
    def current(self):return self.request('/api/review')[1]
    def payload(self,verdict='draft'):
        r=self.current();return {'package_hash':r['package_hash'],'version':r['feedback']['version'],'decisions':{'P13-D01':{'status':'approved','comment':'Đồng ý'},'P13-D02':{'status':'pending','comment':''}},'notes':'Góp ý chung','verdict':verdict}
    def test_feedback_survives_server_restart(self):
        status,result=self.request('/api/feedback',self.payload());self.assertEqual(status,200)
        self.server.shutdown();self.server.server_close();self.start()
        self.assertEqual(self.current()['feedback']['decisions']['P13-D01']['comment'],'Đồng ý')
    def test_stale_tab_cannot_overwrite_feedback(self):
        p=self.payload();self.request('/api/feedback',p)
        self.assertEqual(self.request('/api/feedback',p)[0],409)
    def test_changed_package_rejects_old_hash(self):
        p=self.payload();self.package.write_text(json.dumps({'decisions':[{'id':'P13-D01'}],'revision':'new'}))
        self.assertEqual(self.request('/api/feedback',p)[0],409)
    def test_approval_requires_all_cards_approved(self):
        self.assertEqual(self.request('/api/feedback',self.payload('approved'))[0],400)
    def test_overall_approval_and_edit_reset(self):
        p=self.payload('approved');p['decisions']['P13-D02']['status']='approved'
        self.assertEqual(self.request('/api/feedback',p)[0],200)
        q=self.payload('approved');q['decisions']['P13-D02']['status']='approved';q['notes']='Đổi ý'
        self.assertEqual(self.request('/api/feedback',q)[0],400)
        q['verdict']='draft';self.assertEqual(self.request('/api/feedback',q)[0],200)
        self.assertEqual(self.current()['feedback']['verdict'],'draft')
    def test_rejection_needs_no_global_approvals(self):
        p=self.payload('rejected');p['notes']='Cần thiết kế lại'
        self.assertEqual(self.request('/api/feedback',p)[0],200)
    def test_bad_ids_status_and_cross_origin_rejected(self):
        p=self.payload();p['decisions']['unknown']={'status':'approved','comment':''}
        self.assertEqual(self.request('/api/feedback',p)[0],400)
        p=self.payload();p['decisions']['P13-D01']['status']='fake'
        self.assertEqual(self.request('/api/feedback',p)[0],400)
        self.assertEqual(self.request('/api/feedback',self.payload(),{'Origin':'https://example.com'})[0],403)
    def test_no_repository_file_serve(self):
        self.assertEqual(self.request('/../../.env')[0],404)
        self.assertEqual(self.request('/api/document?name=../../AGENTS.md')[0],404)

if __name__=='__main__':unittest.main()
