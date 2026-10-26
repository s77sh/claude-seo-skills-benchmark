"""Serve lab v2 on localhost:8766: /coffee/ijen/ 301 (issue 2), /coffee/kintamani/ 302 (issue 4), X-Robots-Tag noindex on /subscriptions/ (issue 1)."""
import http.server, sys
ROOT = sys.argv[1]
REDIRECTS = {"/coffee/ijen/": ("/coffee/java-ijen/", 301), "/coffee/kintamani/": ("/coffee/bali-kintamani/", 302)}
HEADERS = {"/subscriptions/": ("X-Robots-Tag", "noindex")}

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)
    def redirect(self):
        path = self.path.split("?")[0]
        if path in REDIRECTS:
            to, code = REDIRECTS[path]
            self.send_response(code); self.send_header("Location", to); self.end_headers()
            return True
    def end_headers(self):
        h = HEADERS.get(self.path.split("?")[0])
        if h:
            self.send_header(*h)
        super().end_headers()
    def do_GET(self):
        if not self.redirect():
            super().do_GET()
    def do_HEAD(self):
        if not self.redirect():
            super().do_HEAD()
    def log_message(self, *a):
        pass

http.server.ThreadingHTTPServer(("127.0.0.1", 8766), H).serve_forever()
