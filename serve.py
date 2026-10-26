"""Serve the lab site on localhost:8765. /menu/ -> /cafe/ -> /visit/ is a two-hop 301 chain (issue 9)."""
import http.server, os, sys
ROOT = sys.argv[1]
REDIRECTS = {"/menu/": "/cafe/", "/cafe/": "/visit/", "/menu": "/menu/", "/cafe": "/cafe/"}

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)
    def do_GET(self):
        path = self.path.split("?")[0]
        if path in REDIRECTS:
            self.send_response(301)
            self.send_header("Location", REDIRECTS[path])
            self.end_headers()
            return
        super().do_GET()
    do_HEAD_orig = http.server.SimpleHTTPRequestHandler.do_HEAD
    def do_HEAD(self):
        path = self.path.split("?")[0]
        if path in REDIRECTS:
            self.send_response(301); self.send_header("Location", REDIRECTS[path]); self.end_headers(); return
        super().do_HEAD()
    def log_message(self, *a):
        pass

http.server.ThreadingHTTPServer(("127.0.0.1", 8765), H).serve_forever()
