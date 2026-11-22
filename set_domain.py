#!/usr/bin/env python3
"""Put your own web address into every text file of this folder (replaces the placeholder).

    python3 set_domain.py my-site.example.com        (or https://my-site.example.com)
    python3 set_domain.py my-site.example.com --cname   (also writes a CNAME file for GitHub Pages custom domains)

It is safe to run again, e.g. after a typo: it finds the address currently in the files and replaces that.
"""
import io, os, re, sys
PLACE = "https://YOUR-DOMAIN"
args = [x for x in sys.argv[1:] if not x.startswith("--")]
if len(args) != 1:
    sys.exit(__doc__)
d = args[0].strip().rstrip("/")
host = d.split("://", 1)[-1]
url = d if "://" in d else "https://" + d
here = os.path.dirname(os.path.abspath(__file__))
# The address now in the files = the canonical link of index.html (the placeholder on a fresh copy).
cur = PLACE
try:
    m = re.search(r'<link rel="canonical" href="([^"]*?)/?"', io.open(os.path.join(here, "index.html"), encoding="utf-8").read())
    if m and m.group(1):
        cur = m.group(1)
except (IOError, OSError):
    pass
olds = [cur] if cur == PLACE else [cur, PLACE]
n = 0
for root, _, files in os.walk(here):
    for f in files:
        if f.endswith((".html", ".xml", ".txt", ".md")):
            p = os.path.join(root, f)
            s = io.open(p, encoding="utf-8").read()
            t = s
            for old in olds:
                t = t.replace(old, url)
            for oh in set(o.split("://", 1)[-1] for o in olds):
                t = t.replace("var SITE_HOST='%s'" % oh, "var SITE_HOST='%s'" % host)
            if t != s:
                io.open(p, "w", encoding="utf-8", newline="\n").write(t)
                n += 1
if "--cname" in sys.argv:
    io.open(os.path.join(here, "CNAME"), "w").write(host + "\n")
if n == 0 and cur == url:
    print("nothing to change: the files already use %s" % url)
else:
    print("done: replaced the domain in %d file(s) -> %s" % (n, url))
