"""Thumbnails for the /tools/ grid. Usage: python3 _scripts/tools_thumbs.py <repo_root> [slug ...]

Reads _data/tools.yml and, for each card whose thumb is in assets/tools/, opens the page in a
1280x800 light-mode browser, takes the top of the page and saves a 640x400 JPEG (the same size as
the dashboard thumbnails). Standalone pages (tools/, puzzles/, guides/) are shot as they are.
Pages built by Jekyll (.md with a permalink) are shot from a close preview: the Markdown rendered
inside the site header, title and lead, with the real style sheet and fonts.
Needs Playwright with Chromium, Pillow, PyYAML and Markdown. Serves the repo on port 8765 while it runs.
"""
import sys, os, re, io, glob, threading, functools, http.server, socketserver
import yaml, markdown
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
ONLY = set(sys.argv[2:])
PORT = 8765
TMP = os.path.join(ROOT, '_thumb_preview.html')   # removed at the end; underscore keeps Jekyll off it


def find_md(permalink):
    for f in glob.glob(os.path.join(ROOT, '**/*.md'), recursive=True):
        if '/_site' in f or '/vendor/' in f:
            continue
        head = open(f, encoding='utf-8').read(2000)
        if re.search(r'^permalink:\s*' + re.escape(permalink) + r'\s*$', head, re.M):
            return f
    return None


def preview(md_path):
    """A close stand-in for the Jekyll page layout, good enough for a thumbnail."""
    t = open(md_path, encoding='utf-8').read()
    _, fm, body = t.split('---', 2)
    fm = yaml.safe_load(fm)
    body = re.sub(r"\{\{\s*'([^']+)'\s*\|\s*relative_url\s*\}\}", r'\1', body)
    body = re.sub(r'\{%.*?%\}|\{\{.*?\}\}', '', body, flags=re.S)
    html = markdown.markdown(body, extensions=['tables', 'attr_list', 'md_in_html'])
    nav = ''.join(f'<a href="#">{n}</a>' for n in ['Home', 'Services', 'CBAM Desk', 'Public sector', 'Tools',
                                                    'Dashboards', 'About', 'Learn', 'Blog', 'Contact'])
    lead = f'<p class="lead">{fm["lead"]}</p>' if fm.get('lead') else ''
    return f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="/assets/fonts/fonts.css"><link rel="stylesheet" href="/assets/style.css"></head>
<body><header class="site-header"><div class="wrap header-inner"><a class="brand" href="#">
<img src="/assets/logo-header.png" alt="" width="551" height="119"></a><nav class="site-nav">{nav}</nav></div></header>
<main><article class="wrap page"><h1 class="page-title">{fm["title"]}</h1>{lead}<div class="prose">{html}</div></article></main></body></html>'''


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    h = functools.partial(Quiet, directory=ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    s = socketserver.TCPServer(('127.0.0.1', PORT), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def main():
    cards = [c for g in yaml.safe_load(open(os.path.join(ROOT, '_data/tools.yml'), encoding='utf-8')) for c in g['items']]
    cards = [c for c in cards if c['thumb'].startswith('/assets/tools/')]
    os.makedirs(os.path.join(ROOT, 'assets/tools'), exist_ok=True)
    srv = serve()
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={'width': 1280, 'height': 800}, color_scheme='light', reduced_motion='reduce')
            for c in cards:
                slug = os.path.splitext(os.path.basename(c['thumb']))[0]
                if ONLY and slug not in ONLY:
                    continue
                page = c['page']
                local = os.path.join(ROOT, page.lstrip('/'))
                if page.endswith('/') and os.path.exists(os.path.join(local, 'index.html')):
                    url = page + 'index.html'
                elif page.endswith('.html') and os.path.exists(local):
                    url = page
                else:
                    md = find_md(page)
                    if not md:
                        sys.exit(f'No source found for {page}')
                    open(TMP, 'w', encoding='utf-8').write(preview(md))
                    url = '/' + os.path.basename(TMP)
                pg.goto(f'http://127.0.0.1:{PORT}{url}', wait_until='networkidle')
                pg.wait_for_timeout(700)
                png = pg.screenshot(clip={'x': 0, 'y': 0, 'width': 1280, 'height': 800})
                im = Image.open(io.BytesIO(png)).convert('RGB').resize((640, 400), Image.LANCZOS)
                out = os.path.join(ROOT, c['thumb'].lstrip('/'))
                im.save(out, 'JPEG', quality=82, optimize=True, progressive=True)
                print('wrote', os.path.relpath(out, ROOT), os.path.getsize(out) // 1024, 'KB')
            b.close()
    finally:
        srv.shutdown()
        if os.path.exists(TMP):
            os.remove(TMP)


if __name__ == '__main__':
    main()
