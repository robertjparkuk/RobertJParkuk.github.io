"""Build the SPS deal briefing PDF (21 Nov 2026) from briefing.md (the Claude Doc export) and the charts.
Usage: python3 build_pdf.py <repo_root>"""
import sys, os, re, html, markdown, asyncio
from playwright.async_api import async_playwright
ROOT = os.path.abspath(sys.argv[1]); HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0], ROOT]
src = open(os.path.join(ROOT, '_scripts/briefings/build_thought_pdfs.py')).read()
CSS = re.search(r'CSS = """(.*?)"""', src, re.S).group(1)
FONT = 'file://' + os.path.join(ROOT, 'assets/fonts'); LOGO = 'file://' + os.path.join(ROOT, 'assets/brand/logo.svg')
CH = 'file://' + os.path.join(ROOT, 'assets/briefings/sps-deal/')
OUT = os.path.join(ROOT, 'assets/briefings/2026-11-the-sps-deal-ni-briefing.pdf')
md = open(os.path.join(HERE, 'briefing.md'), encoding='utf-8').read()
title = md.split('\n', 1)[0].lstrip('# ').strip()
md = md.split('\n', 1)[1]
md = re.sub(r'^Nov 21, 2026 · @Robert Park\s*$', '', md, flags=re.M)
fig = lambda f, alt: f'<figure class="ch"><img src="{CH}{f}" alt="{html.escape(alt)}"></figure>'
charts = [('farm-output.svg', 'NI farm output by product, 1990, 2015, 2024'), ('processing-mix.svg', 'NI food processing turnover by subsector'),
          ('farm-emissions.svg', 'NI farm emissions by source'), ('sales-destination.svg', 'Where NI processors sell')]
blocks = re.findall(r'^&#91;embedded content:.*$', md, re.M)
for b, (f, alt) in zip(blocks, charts): md = md.replace(b, fig(f, alt), 1)
md = md.replace('**Inputs: what NI processors buy, and from where (2022)**', fig('bought-and-sold.svg', 'Bought from and sold to GB and the EU, 2022') + '\n\n**Inputs: what NI processors buy, and from where (2022)**', 1)
md = md.replace('&#91;', '[').replace('\\]', ']')
h = markdown.markdown(md, extensions=['tables'])
h = h.replace('<h2>Sources</h2>', '<h2 id="sources">Sources</h2>')
nums = [('1 Mar 2028', 'date the SPS deal is aimed to apply; not yet law'), ('49%', 'of NI processed food sales went to GB in 2022 (£3.16bn)'),
        ('26%', 'went to Ireland and the rest of the EU (£1.71bn)'), ('£886m', 'of inputs NI processors bought from GB; £969m from the EU'),
        ('⅔', 'of NI farm emissions come from cattle, beef and dairy (2024)'), ('2.0%', 'of NI GVA from farming (2024), against 0.6% for the UK; processing adds 2.2%')]
numh = ''.join(f'<div><b>{html.escape(a)}</b><span>{html.escape(b)}</span></div>' for a, b in nums)
extra = 'figure.ch{margin:8px 0 12px;break-inside:avoid}figure.ch img{width:100%}table{border-collapse:collapse;width:100%;font-size:8.6pt;margin:4px 0 10px;break-inside:avoid}th,td{border-bottom:1px solid #e3dedb;padding:3px 5px;text-align:left;vertical-align:top}th{font-weight:700;color:#1a1a1a;background:#faf6f5}h4{font-size:10pt;margin:10px 0 4px;color:#a61c1c}'
doc = f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{CSS % {'f': FONT}}{extra}</style></head><body>
<div class="top"><img src="{LOGO}" alt="Robert J. Park"><div class="meta">Briefing · 21 November 2026<br>SPS · Agri-food · Trade · Carbon<br>Northern Ireland</div></div>
<div class="eyebrow">Briefing · UK–EU summit · Food and farming · Windsor Framework</div>
<h1>{html.escape(title)}</h1>
<p class="lead">What the UK–EU food and farming deal of 20 November 2026 changes for Northern Ireland and Great Britain, who gains and who loses, and the official numbers on what NI farms and food firms make, emit, buy and sell.</p>
<div class="lab">In numbers</div><div class="nums">{numh}</div>
<div class="dash">Read online: <b>robertjpark.co.uk/go/sps/</b></div>
{h}
<p class="end">Robert J. Park is an independent environment, carbon and public affairs consultant based in Larne, Northern Ireland. robert@robertjpark.co.uk · 07450 349480 · robertjpark.co.uk · Status as at 21 November 2026. General information, not legal advice. AI was used to lay out this document and to generate leads from the consultant's research, knowledge and questioning; figures were checked against the official sources listed.</p>
</body></html>"""
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); tmp = os.path.join(HERE, '_tmp.html'); open(tmp, 'w', encoding='utf-8').write(doc)
        pg = await b.new_page(); await pg.goto('file://' + tmp); await pg.wait_for_timeout(600)
        foot = "<div style='font-family:sans-serif;font-size:7pt;color:#5a5a5a;width:100%;padding:0 16mm;display:flex;justify-content:space-between'><span>Robert J. Park · The SPS deal and Northern Ireland · 21 November 2026 · robertjpark.co.uk</span><span><span class='pageNumber'></span> / <span class='totalPages'></span></span></div>"
        await pg.pdf(path=OUT, format='A4', print_background=True, display_header_footer=True, header_template='<div></div>', footer_template=foot,
                     margin={'top': '16mm', 'bottom': '18mm', 'left': '16mm', 'right': '16mm'})
        os.remove(tmp); await b.close(); print(OUT)
asyncio.run(main())
