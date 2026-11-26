"""Branded A4 PDFs of the eight element briefings, each with the full periodic table.
Text is the blog post itself (front matter and site-only markup removed).
Rendered with Chromium (Playwright) using the site's own fonts.

  python3 _scripts/elements/build_pdfs.py <repo_root>
"""
import sys, os, re, html, glob, asyncio, markdown
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(__file__))
from featured import F, CHECKED
from base import ELEMENTS

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
FONT = 'file://' + os.path.join(ROOT, 'assets/fonts')
LOGO = 'file://' + os.path.join(ROOT, 'assets/brand/logo.svg')
NAMES = {e[1]: (e[0], e[2]) for e in ELEMENTS}
ORDER = ['P', 'N', 'S', 'F', 'Sb', 'Mg', 'C', 'Rn']

CSS = """
@font-face{font-family:'SS3';src:url('%(f)s/source-sans-3.woff')}
@font-face{font-family:'SS3';font-style:italic;src:url('%(f)s/source-sans-3-italic.woff')}
@font-face{font-family:'SS4';src:url('%(f)s/source-serif-4.woff')}
@font-face{font-family:'PM';src:url('%(f)s/ibm-plex-mono-regular.woff')}
@page{size:A4}
body{font-family:'SS3',sans-serif;font-size:9.8pt;line-height:1.48;color:#2b2b2b;margin:0}
.top{display:flex;justify-content:space-between;align-items:flex-start;border-bottom:1px solid #e3dedb;padding-bottom:8px;margin-bottom:10px}
.top img{height:40px}
.meta{font-family:'PM',monospace;font-size:7.8pt;color:#5a5a5a;text-align:right;line-height:1.6}
.eyebrow{font-family:'PM',monospace;font-size:7.6pt;letter-spacing:.12em;text-transform:uppercase;color:#a61c1c;margin:4px 0 4px}
h1{font-family:'SS4',serif;font-weight:600;font-size:21pt;line-height:1.15;color:#1a1a1a;margin:0 0 6px}
.lead{font-family:'SS4',serif;font-size:11.2pt;line-height:1.45;margin:0 0 10px}
.table{margin:4px 0 12px;break-inside:avoid}
.table img{width:100%%;display:block;border:1px solid #e3dedb}
.table p{font-size:7.8pt;color:#5a5a5a;margin:3px 0 0}
h2{font-family:'SS4',serif;font-weight:600;font-size:13pt;color:#1a1a1a;margin:14px 0 5px;padding-top:8px;border-top:1px solid #e3dedb;break-after:avoid}
p{margin:0 0 7px} ul,ol{margin:0 0 7px;padding-left:17px} li{margin:0 0 3px} li::marker{color:#a61c1c}
a{color:#a61c1c;text-decoration:none}
table{border-collapse:collapse;width:100%%;margin:6px 0 10px;font-size:8.6pt;break-inside:avoid}
th{background:#faf3f3;text-align:left;border-bottom:2px solid #a61c1c;padding:4px 6px;font-weight:700}
td{border-bottom:1px solid #e3dedb;padding:4px 6px;vertical-align:top}
h2#safety-and-handling{color:#a61c1c}
h2#sources + ul{font-size:7.8pt;line-height:1.35} h2#sources + ul a{color:#2b2b2b}
.end{font-size:8.2pt;color:#5a5a5a;border-top:1px solid #e3dedb;padding-top:8px;margin-top:12px}
"""

def post_path(sym):
    slug = F[sym]['post'].rstrip('/').split('/')[-1]
    return glob.glob(os.path.join(ROOT, '_posts', f'*-{slug}.md'))[0]

def parts(sym):
    s = open(post_path(sym), encoding='utf-8').read()
    fm, body = s.split('---', 2)[1], s.split('---', 2)[2]
    title = re.search(r'^title: "(.*)"$', fm, re.M).group(1)
    body = re.sub(r'<figure.*?</figure>', '', body, flags=re.S)
    body = re.sub(r"\{\{ '([^']+)' \| relative_url \}\}", r'https://robertjpark.co.uk\1', body)
    body = body.split('\n---\n')[0]
    body = re.sub(r'## Further reading on this site.*?(?=\n## )', '', body, flags=re.S)
    first = re.search(r'^\*(.+)\*\s*$', body.strip().split('\n')[0])
    lead = first.group(1) if first else ''
    if first: body = body.strip().split('\n', 1)[1]
    return title, lead, body

def page(sym, i):
    title, lead, body = parts(sym)
    z, name = NAMES[sym]
    h = markdown.markdown(body, extensions=['tables'])
    for hid in ('Sources', 'Safety and handling'):
        h = h.replace(f'<h2>{hid}</h2>', f'<h2 id="{hid.lower().replace(" ", "-")}">{hid}</h2>')
    svg = 'file://' + os.path.join(ROOT, f'assets/learn/periodic-table-{sym.lower()}.svg')
    url = 'robertjpark.co.uk' + F[sym]['post']
    return f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{CSS % {'f': FONT}}</style></head><body>
<div class="top"><img src="{LOGO}" alt="Robert J. Park"><div class="meta">Elements of the land · briefing {i} of 8<br>{name} (element {z})<br>{CHECKED} · Northern Ireland</div></div>
<div class="eyebrow">Learning briefing · Climate · Soil · Land · Agri-food · Atmosphere</div>
<h1>{html.escape(title)}</h1>
<p class="lead">{html.escape(lead)}</p>
<div class="table"><img src="{svg}" alt="The full periodic table with {name} picked out in red"><p>{name} in the full periodic table. Interactive version with every element: <a href="https://robertjpark.co.uk/tools/periodic-table.html">robertjpark.co.uk/tools/periodic-table.html</a></p></div>
{h}
<div class="end">Online version: <a href="https://{url}">{url}</a><br>
Robert J. Park · Environment · Carbon · Public Affairs · robert@robertjpark.co.uk · 07450 349480 · WhatsApp @robertjpark<br>
General information as at {CHECKED}, not legal, safety or agronomic advice. Work from current safety data sheets and your own COSHH assessment.
AI was used to lay out this document and to generate leads from the consultant's research, knowledge and questioning; figures were checked against the official sources listed.</div>
</body></html>"""

async def main():
    os.makedirs(os.path.join(ROOT, 'assets/briefings/elements'), exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        for i, sym in enumerate(ORDER, 1):
            tmp = f'/tmp/element-{sym}.html'
            open(tmp, 'w', encoding='utf-8').write(page(sym, i))
            await pg.goto('file://' + tmp); await pg.wait_for_timeout(300)
            out = os.path.join(ROOT, F[sym]['pdf'].lstrip('/'))
            await pg.pdf(path=out, format='A4', print_background=True,
                         display_header_footer=True, header_template='<span></span>',
                         footer_template='<div style="font-size:7pt;color:#777;width:100%%;text-align:right;padding-right:15mm">Robert J. Park · <span class="pageNumber"></span>/<span class="totalPages"></span></div>',
                         margin=dict(top='15mm', bottom='17mm', left='15mm', right='15mm'))
            print(out)
        await b.close()

asyncio.run(main())
