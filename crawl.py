"""Crawl the lab like Screaming Frog (start at / plus the sitemap) and write crawl.csv."""
import csv, re, sys, urllib.request, urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
ORIGIN = "http://localhost:8765"
BLOCKED = ["/assets/css/", "/cart/"]

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None
opener = urllib.request.build_opener(NoRedirect)

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.title = ""; self.in_title = False; self.desc = ""; self.robots = ""
        self.canon = ""; self.h1 = []; self.in_h1 = False; self.links = []; self.text = []; self.skip = 0
        self.imgs = []; self.css = []
    def handle_starttag(self, t, a):
        a = dict(a)
        if t == "title": self.in_title = True
        if t == "meta" and a.get("name") == "description": self.desc = a.get("content", "")
        if t == "meta" and a.get("name") == "robots": self.robots = a.get("content", "")
        if t == "link" and a.get("rel") == "canonical": self.canon = a.get("href", "")
        if t == "link" and a.get("rel") == "stylesheet": self.css.append(a["href"])
        if t == "h1": self.in_h1 = True; self.h1.append("")
        if t == "a" and "href" in a: self.links.append(a["href"])
        if t == "img": self.imgs.append((a.get("src"), a.get("alt")))
        if t in ("script", "style", "nav", "footer"): self.skip += 1
    def handle_endtag(self, t):
        if t == "title": self.in_title = False
        if t == "h1": self.in_h1 = False
        if t in ("script", "style", "nav", "footer"): self.skip -= 1
    def handle_data(self, d):
        if self.in_title: self.title += d
        if self.in_h1: self.h1[-1] += d
        if not self.skip and not self.in_title: self.text.append(d)

def fetch(path):
    try:
        r = opener.open(ORIGIN + path)
        return r.status, r.headers.get("Content-Type", ""), r.read(), ""
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", ""), b"", e.headers.get("Location", "") or ""

sitemap = re.findall(r"<loc>https://kopikita.test(.*?)</loc>", fetch("/sitemap.xml")[2].decode())
queue, seen, rows, inlinks, alts = ["/"] + sitemap, set(), {}, {}, {}
while queue:
    u = queue.pop(0)
    if u in seen: continue
    seen.add(u)
    if any(u.startswith(b) for b in BLOCKED):
        rows[u] = dict(Address=u, **{"Status Code": "", "Status": "Blocked by robots.txt", "Content Type": "text/css",
                                     "Indexability": "Non-Indexable", "Indexability Status": "Blocked by robots.txt"})
        continue
    code, ctype, body, loc = fetch(u)
    row = {"Address": u, "Status Code": code, "Content Type": ctype.split(";")[0], "Size (bytes)": len(body),
           "Redirect URL": loc}
    if code in (301, 302):
        row["Status"] = "Moved Permanently"; row["Indexability"] = "Non-Indexable"; row["Indexability Status"] = "Redirected"
        queue.append(loc); inlinks.setdefault(loc, set()).add(u)
    elif code == 404:
        row["Status"] = "Not Found"; row["Indexability"] = "Non-Indexable"; row["Indexability Status"] = "Client Error"
    elif "html" in ctype:
        p = P(); p.feed(body.decode())
        words = len(re.findall(r"[A-Za-z0-9']+", " ".join(p.text)))
        canon = p.canon.replace("https://kopikita.test", "")
        idx, why = "Indexable", ""
        if "noindex" in p.robots: idx, why = "Non-Indexable", "noindex"
        elif canon and canon != u: idx, why = "Non-Indexable", "Canonicalised"
        row.update({"Status": "OK", "Indexability": idx, "Indexability Status": why, "Title 1": p.title,
                    "Title 1 Length": len(p.title), "Meta Description 1": p.desc,
                    "Meta Description 1 Length": len(p.desc), "H1-1": p.h1[0] if p.h1 else "",
                    "H1-2": p.h1[1] if len(p.h1) > 1 else "", "Meta Robots 1": p.robots,
                    "Canonical Link Element 1": p.canon, "Word Count": words})
        for h in p.links + p.css + [s for s, _ in p.imgs]:
            t = urlparse(urljoin(u, h)).path
            if t != u: inlinks.setdefault(t, set()).add(u)
            queue.append(t)
        for s, a in p.imgs: alts.setdefault(urlparse(urljoin(u, s)).path, a)
    else:
        row["Status"] = "OK"; row["Indexability"] = "Indexable"
    rows[u] = row

for u, r in rows.items():
    r["Inlinks"] = len(inlinks.get(u, ()))
    if u in alts: r["Alt Text"] = alts[u] if alts[u] is not None else "(missing)"
    r["In Sitemap"] = "Yes" if u in sitemap else "No"
cols = ["Address", "Content Type", "Status Code", "Status", "Indexability", "Indexability Status", "Redirect URL",
        "Title 1", "Title 1 Length", "Meta Description 1", "Meta Description 1 Length", "H1-1", "H1-2",
        "Meta Robots 1", "Canonical Link Element 1", "Word Count", "Size (bytes)", "Alt Text", "Inlinks", "In Sitemap"]
with open(sys.argv[1], "w", newline="") as f:
    w = csv.DictWriter(f, cols, extrasaction="ignore"); w.writeheader()
    for u in sorted(rows): w.writerow({"Address": "https://kopikita.test" + u, **{k: v for k, v in rows[u].items() if k != "Address"}})
print(len(rows), "rows")
