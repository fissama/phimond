#!/usr/bin/env python3
"""Máy chủ tĩnh cho benchmark P12 Stage 3. Chạy: python3 serve.py [port]
- Phục vụ thư mục này (three/, godot/, shared/).
- Nhận POST /__result?engine=..&tier=.. và lưu JSON vào results/ (để kết quả từ iPhone về thẳng máy Mac).
- Đúng MIME .wasm/.pck; không cần COOP/COEP (Godot build nothreads).
- Nghe 0.0.0.0 để iPhone cùng Wi-Fi truy cập http://<IP-Mac>:<port>/three/ hoặc /godot/.
"""
import http.server, json, os, socket, sys, time
from urllib.parse import urlparse, parse_qs
ROOT = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(ROOT, 'results'); os.makedirs(RES, exist_ok=True)
class H(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, '.wasm': 'application/wasm', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.pck': 'application/octet-stream', '.png': 'image/png'}
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store'); super().end_headers()
    def do_POST(self):
        u = urlparse(self.path)
        if u.path != '/__result': self.send_error(404); return
        q = parse_qs(u.query); n = int(self.headers.get('content-length', 0)); body = self.rfile.read(n)
        try: json.loads(body)
        except Exception: self.send_error(400, 'bad json'); return
        name = f"{q.get('engine',['x'])[0]}-{q.get('tier',['x'])[0]}-{time.strftime('%Y%m%d-%H%M%S')}-{self.client_address[0].replace(':','_')}.json"
        with open(os.path.join(RES, name), 'wb') as f: f.write(body)
        self.send_response(204); self.end_headers(); print('saved', name)
    def log_message(self, fmt, *a):
        if '/__result' in (a[0] if a else ''): super().log_message(fmt, *a)
if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    ip = socket.gethostbyname(socket.gethostname()) if False else None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(('10.255.255.255', 1)); ip = s.getsockname()[0]; s.close()
    except Exception: ip = '127.0.0.1'
    print(f'Mac:    http://127.0.0.1:{port}/three/   http://127.0.0.1:{port}/godot/')
    print(f'iPhone: http://{ip}:{port}/three/   http://{ip}:{port}/godot/   (cùng Wi-Fi)')
    http.server.ThreadingHTTPServer(('0.0.0.0', port), H).serve_forever()
