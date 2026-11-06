#!/usr/bin/env python3
"""Wraps the built handbook (nextgen-dj-curriculum.html) as a standalone,
offline-capable website in ../docs for GitHub Pages.

Usage: python3 make_site.py <built.html> <out_dir> [domain]
"""
import sys, re, shutil, pathlib, hashlib
from PIL import Image, ImageDraw

SRC = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2])
DOMAIN = sys.argv[3] if len(sys.argv) > 3 else ""
HERE = pathlib.Path(__file__).parent
FONTS = HERE / "fonts"

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "fonts").mkdir(exist_ok=True)
for f in FONTS.glob("*.woff2"):
    shutil.copy(f, OUT / "fonts" / f.name)

body = SRC.read_text()
# drop host-specific and remote font tags
body = re.sub(r'<meta name="claude:[^>]*>\n?', "", body)
body = re.sub(r'<link rel="preconnect"[^>]*>\n?', "", body)
body = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n?', "", body)
title = re.search(r"<title>.*?</title>", body).group(0)
body = body.replace(title, "", 1)

faces = []
for fam, file, w, style in [
    ("Alata", "alata-latin-400-normal", 400, "normal"),
    ("Poppins", "poppins-latin-400-normal", 400, "normal"),
    ("Poppins", "poppins-latin-400-italic", 400, "italic"),
    ("Poppins", "poppins-latin-500-normal", 500, "normal"),
    ("Poppins", "poppins-latin-600-normal", 600, "normal"),
    ("JetBrains Mono", "jetbrains-mono-latin-400-normal", 400, "normal"),
    ("JetBrains Mono", "jetbrains-mono-latin-500-normal", 500, "normal"),
]:
    faces.append(f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{w};font-display:swap;src:url(fonts/{file}.woff2) format('woff2')}}")

version = hashlib.sha1(body.encode()).hexdigest()[:10]

head = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{title}
<meta name="description" content="NextGen Music tutor handbook. Internal reference.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#19263F">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="DJ Curriculum">
<style>
{''.join(faces)}
:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
body{{margin:0;font:14px system-ui,-apple-system,"Segoe UI",sans-serif}}
img{{max-width:100%}}
[hidden]{{display:none!important}}
</style>
</head>
<body>
"""
tail = f"""
<script>
if ('serviceWorker' in navigator) {{
  window.addEventListener('load', function () {{
    navigator.serviceWorker.register('sw.js').catch(function () {{}});
  }});
}}
</script>
</body>
</html>
"""
(OUT / "index.html").write_text(head + body + tail)

sw = f"""// NextGen DJ Curriculum offline support. Build {version}
const CACHE = 'ngdj-{version}';
const CORE = ['./', 'index.html', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png',
{', '.join(repr('fonts/' + f.name) for f in sorted(FONTS.glob('*.woff2')))}];
self.addEventListener('install', e => {{
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
}});
self.addEventListener('activate', e => {{
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
}});
self.addEventListener('fetch', e => {{
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  if (req.mode === 'navigate' || req.destination === 'document') {{
    // Online: always fetch the latest version. Offline: fall back to the saved copy.
    e.respondWith(fetch(req.url, {{cache: 'no-cache'}}).then(r => {{ const copy = r.clone(); caches.open(CACHE).then(c => c.put('index.html', copy)); return r; }})
      .catch(() => caches.match('index.html')));
    return;
  }}
  e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => {{ const copy = r.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return r; }})));
}});
"""
(OUT / "sw.js").write_text(sw)

(OUT / "manifest.webmanifest").write_text("""{
  "name": "NextGen DJ Curriculum",
  "short_name": "DJ Curriculum",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "background_color": "#19263F",
  "theme_color": "#19263F",
  "icons": [
    {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}
  ]
}
""")

logo = Image.open(HERE / "img" / "logo.png").convert("RGBA")
for name, size in [("icon-192.png", 192), ("icon-512.png", 512), ("apple-touch-icon.png", 180)]:
    bg = Image.new("RGBA", (size, size), (25, 38, 63, 255))
    l = logo.copy(); l.thumbnail((int(size * 0.62), int(size * 0.62)))
    bg.paste(l, ((size - l.width) // 2, (size - l.height) // 2), l)
    bg.convert("RGB").save(OUT / name, optimize=True)

(OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
(OUT / ".nojekyll").write_text("")
if DOMAIN:
    (OUT / "CNAME").write_text(DOMAIN + "\n")
print("site written to", OUT, "build", version)
