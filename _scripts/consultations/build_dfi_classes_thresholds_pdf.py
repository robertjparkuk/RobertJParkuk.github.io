"""Build the branded PDF of Robert's DfI classes-and-thresholds consultation response.
Usage: python3 build_pdf.py <repo_root> <response.md> <out.pdf>
"""
import sys, os, re, html, markdown, asyncio
from playwright.async_api import async_playwright

ROOT, SRC, OUT = [os.path.abspath(a) for a in sys.argv[1:4]]
FONT = 'file://' + os.path.join(ROOT, 'assets/fonts')
LOGO = 'file://' + os.path.join(ROOT, 'assets/brand/logo.svg')
MARK = 'file://' + os.path.join(ROOT, 'assets/brand/mark.svg')

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
h1{font-family:'SS4',serif;font-weight:600;font-size:19pt;line-height:1.2;color:#1a1a1a;margin:0 0 10px}
.lead{font-family:'SS4',serif;font-size:10.5pt;line-height:1.45;color:#5a5a5a;margin:0 0 14px;font-style:italic}
h2{font-family:'SS4',serif;font-weight:600;font-size:13.5pt;color:#1a1a1a;margin:18px 0 6px;padding-top:10px;border-top:1px solid #e3dedb;break-after:avoid}
h3{font-family:'SS3',sans-serif;font-weight:700;font-size:10.5pt;color:#1a1a1a;margin:12px 0 4px;break-after:avoid}
p{margin:0 0 8px}
ul,ol{margin:0 0 8px;padding-left:18px} li{margin:0 0 4px}
li::marker{color:#a61c1c}
em{font-style:italic}
strong{color:#1a1a1a}
a{color:#a61c1c;text-decoration:none}
h2#sources + ul, h2#annex-b-sources + ul{font-size:8pt;line-height:1.35}
h2#sources + ul, h2#annex-b-sources + ul a{color:#2b2b2b}
.summary{border:1px solid #e3dedb;border-top:3px solid #a61c1c;padding:10px 14px 4px;margin:6px 0 14px;break-inside:avoid}
.summary ol{font-size:9.4pt}
.sig{margin-top:14px}
.sig p{margin:0}
"""

def body_md(path):
    s = open(path, encoding='utf-8').read()
    fm, body = s.split('---', 2)[1], s.split('---', 2)[2]
    title = re.search(r'^title: "(.*)"$', fm, re.M).group(1)
    body = body.strip()
    first = body.split('\n')[0]
    lead = first.strip('*') if first.startswith('*') else ''
    if lead: body = body.split('\n', 1)[1]
    return title, lead, body

title, lead, body = body_md(SRC)
h = markdown.markdown(body, extensions=['tables'])
h = h.replace('<h2>Annex B: sources</h2>', '<h2 id="sources">Annex B: sources</h2>')
# box the summary list
h = re.sub(r'(<h2>Summary</h2>\s*<p>.*?</p>\s*)(<ol>.*?</ol>)', r'\1<div class="summary">\2</div>', h, count=1, flags=re.S)
# signature block
h = h.replace('<p>Robert J. Park<br />', '<div class="sig"><p>Robert J. Park<br />').replace('robertjpark.co.uk</p>', 'robertjpark.co.uk</p></div>', 1)

page = f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{CSS % {'f': FONT}}</style></head><body>
<div class="top"><img src="{LOGO}" alt="Robert J. Park"><div class="meta">Consultation response · 6 November 2026<br>Planning · Energy · Waste · Land<br>Northern Ireland</div></div>
<div class="eyebrow">Consultation response · Department for Infrastructure</div>
<h1>{html.escape(title)}</h1>
<p class="lead">{html.escape(lead)}</p>
{h}
</body></html>"""

HTML_OUT = OUT.replace('.pdf', '.html')
open(HTML_OUT, 'w', encoding='utf-8').write(page)

FOOT = f"""<div style="width:100%;font-family:'IBM Plex Mono',monospace;font-size:7pt;color:#5a5a5a;padding:0 16mm;display:flex;justify-content:space-between;align-items:center">
<span><img src="{MARK}" style="height:9px;vertical-align:middle;margin-right:6px">Robert J. Park · Environment · Carbon · Public Affairs · robertjpark.co.uk</span>
<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>"""

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page()
        await pg.goto('file://' + HTML_OUT)
        await pg.wait_for_timeout(300)
        await pg.pdf(path=OUT, format='A4', print_background=True, display_header_footer=True,
                     header_template='<span></span>', footer_template=FOOT,
                     margin={'top': '16mm', 'bottom': '18mm', 'left': '16mm', 'right': '16mm'})
        await b.close()

asyncio.run(main())
print('built', OUT)
