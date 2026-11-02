"""Build branded briefing PDFs from two thought-piece posts (2 Nov 2026).
Text is the post itself (front matter and site-only markup removed), with an
'In numbers' panel. Rendered with Chromium (Playwright) using the site's own fonts.
Usage: python3 build_thought_pdfs.py <repo_root>
"""
import sys, os, re, html, markdown, glob, asyncio
from playwright.async_api import async_playwright

ROOT = os.path.abspath(sys.argv[1])
FONT = 'file://' + os.path.join(ROOT, 'assets/fonts')
LOGO = 'file://' + os.path.join(ROOT, 'assets/brand/logo.svg')

PIECES = [
 dict(post='_posts/2026-11-02-northern-ireland-screen-how-do-we-grow-it.md',
      out='assets/briefings/2026-11-ni-screen-how-do-we-grow-it-briefing.pdf',
      num='04', eyebrow='Briefing · Screen industry · Skills · Public affairs', tags='Screen · Skills · Economy',
      dash='robertjpark.co.uk/tools/dashboards/ni-screen-industry.html',
      numbers=[('≈£73m', 'DfE funding to NI Screen, April 2022 to March 2026'), ('£477m', 'local production spend, against a £442m target'),
               ('≈£6.50', 'local spend per £1 of DfE money (derived; DfE money also paid for skills)'), ('88%', 'of crew on major productions lived in NI'),
               ('32%', "Ireland's Section 481 credit; Irish spend hit a record €544m in 2025"), ('£798.4m', 'DfE day-to-day budget 2026/27, down from £814.5m, with ≈£134m of pressures')]),
 dict(post='_posts/2026-11-02-we-dont-fund-the-drains-then-we-pay-for-the-flood.md',
      out='assets/briefings/2026-11-who-pays-for-the-public-realm-briefing.pdf',
      num='05', eyebrow='Briefing · Public realm · Water · Climate adaptation', tags='Water · Roads · Floods',
      dash='robertjpark.co.uk/tools/dashboards/ni-public-realm-water-roads.html',
      numbers=[('≈100', 'places where new homes are restricted because the sewers are full'), ('≈15,000', 'homes held back by wastewater limits (DfI)'),
               ('≈£7bn', 'NI Water estimate of wastewater investment needed'), ('£68m', 'road maintenance budget against ≈£250m a year needed'),
               ('≈45,000', 'properties in floodplains; only 1 flood scheme in 5 on time'), ('23 of 37', 'Lough Neagh actions complete; the lough supplies ≈40% of drinking water')]),
]

CSS = """
@font-face{font-family:'SS3';src:url('%(f)s/source-sans-3.woff')}
@font-face{font-family:'SS3';font-style:italic;src:url('%(f)s/source-sans-3-italic.woff')}
@font-face{font-family:'SS4';src:url('%(f)s/source-serif-4.woff')}
@font-face{font-family:'PM';src:url('%(f)s/ibm-plex-mono-regular.woff')}
@page{size:A4;margin:16mm 16mm 18mm}
body{font-family:'SS3',sans-serif;font-size:10pt;line-height:1.5;color:#2b2b2b;margin:0}
.top{display:flex;justify-content:space-between;align-items:flex-start;border-bottom:1px solid #e3dedb;padding-bottom:10px;margin-bottom:14px}
.top img{height:38px}
.meta{font-family:'PM',monospace;font-size:8pt;color:#5a5a5a;text-align:right;line-height:1.6}
.eyebrow{font-family:'PM',monospace;font-size:7.6pt;letter-spacing:.12em;text-transform:uppercase;color:#a61c1c;margin:6px 0 4px}
h1{font-family:'SS4',serif;font-weight:600;font-size:22pt;line-height:1.15;color:#1a1a1a;margin:0 0 8px}
.lead{font-family:'SS4',serif;font-size:11.5pt;line-height:1.45;color:#2b2b2b;margin:0 0 14px}
.nums{display:grid;grid-template-columns:repeat(3,1fr);gap:10px 16px;border:1px solid #e3dedb;border-top:3px solid #a61c1c;padding:12px 14px;margin:6px 0 16px;break-inside:avoid}
.nums b{display:block;font-family:'SS4',serif;font-size:16pt;color:#1a1a1a;font-weight:600}
.nums span{font-size:8.2pt;color:#5a5a5a;line-height:1.35;display:block}
.lab{font-family:'PM',monospace;font-size:7.6pt;letter-spacing:.12em;text-transform:uppercase;color:#a61c1c}
h2{font-family:'SS4',serif;font-weight:600;font-size:13.5pt;color:#1a1a1a;margin:18px 0 6px;padding-top:10px;border-top:1px solid #e3dedb;break-after:avoid}
h3{font-family:'SS3',sans-serif;font-weight:700;font-size:10.5pt;color:#1a1a1a;margin:12px 0 4px;break-after:avoid}
p{margin:0 0 8px}
ul,ol{margin:0 0 8px;padding-left:18px} li{margin:0 0 4px}
li::marker{color:#a61c1c}
em{font-style:italic}
a{color:#a61c1c;text-decoration:none}
h2#sources + ul{font-size:8pt;line-height:1.35}
h2#sources + ul a{color:#2b2b2b}
.dash{background:#faf3f3;border-left:3px solid #a61c1c;padding:8px 12px;font-size:9pt;margin:12px 0;break-inside:avoid}
.end{font-size:8.5pt;color:#5a5a5a;border-top:1px solid #e3dedb;padding-top:8px;margin-top:14px}
"""

def body_md(path):
    s = open(path, encoding='utf-8').read()
    fm, body = s.split('---', 2)[1], s.split('---', 2)[2]
    title = re.search(r'^title: "(.*)"$', fm, re.M).group(1)
    body = re.sub(r'<figure.*?</figure>', '', body, flags=re.S)
    body = re.sub(r"\{\{ '([^']+)' \| relative_url \}\}", r'https://robertjpark.co.uk\1', body)
    body = body.split('\n---\n')[0]  # drop the author footer
    body = '\n'.join(l for l in body.split('\n') if not l.startswith(('[Download the full briefing', '**Go further:**')))
    first = re.search(r'^\*(.+)\*\s*$', body.strip().split('\n')[0])
    lead = first.group(1) if first else ''
    if first: body = body.strip().split('\n', 1)[1]
    return title, lead, body

def build(p):
    title, lead, body = body_md(os.path.join(ROOT, p['post']))
    h = markdown.markdown(body, extensions=['tables'])
    h = h.replace('<h2>Sources</h2>', '<h2 id="sources">Sources</h2>')
    nums = ''.join(f'<div><b>{html.escape(a)}</b><span>{html.escape(b)}</span></div>' for a, b in p['numbers'])
    return f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{CSS % {'f': FONT}}</style></head><body>
<div class="top"><img src="{LOGO}" alt="Robert J. Park"><div class="meta">Briefing {p['num']} · 2 November 2026<br>{html.escape(p['tags'])}<br>Northern Ireland</div></div>
<div class="eyebrow">{html.escape(p['eyebrow'])}</div>
<h1>{html.escape(title)}</h1>
<p class="lead">{html.escape(lead)}</p>
<div class="lab">In numbers</div><div class="nums">{nums}</div>
<div class="dash">The figures behind this briefing, with every table downloadable as CSV: <b>{p['dash']}</b></div>
{h}
<p class="end">Robert J. Park is an independent environment, carbon and public affairs consultant based in Larne, Northern Ireland. robert@robertjpark.co.uk · robertjpark.co.uk · Facts checked to 2 November 2026. Scenarios are illustrative, not forecasts.</p>
</body></html>"""

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for p in PIECES:
            doc = build(p)
            tmp = os.path.join(ROOT, '_scripts/briefings/_tmp.html'); open(tmp, 'w', encoding='utf-8').write(doc)
            pg = await b.new_page(); await pg.goto('file://' + tmp); await pg.wait_for_timeout(400)
            foot = f"<div style='font-family:sans-serif;font-size:7pt;color:#5a5a5a;width:100%;padding:0 16mm;display:flex;justify-content:space-between'><span>Robert J. Park · Briefing {p['num']} · 2 November 2026 · robertjpark.co.uk</span><span><span class='pageNumber'></span> / <span class='totalPages'></span></span></div>"
            await pg.pdf(path=os.path.join(ROOT, p['out']), format='A4', print_background=True, display_header_footer=True,
                         header_template='<div></div>', footer_template=foot, margin={'top': '16mm', 'bottom': '18mm', 'left': '16mm', 'right': '16mm'})
            os.remove(tmp); print(p['out'])
        await b.close()
asyncio.run(main())
