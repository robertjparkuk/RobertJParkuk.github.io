"""Build the Christmas decorations briefing PDF, share card and public dashboard (16 Nov 2026).
Run charts.py first. Usage: python3 build.py <repo_root>
Outputs:
  assets/briefings/2026-11-christmas-decorations-briefing.pdf
  assets/briefings/christmas-decorations/christmas-decorations-card.png
  tools/dashboards/christmas-decorations.html
"""
import sys, os, re, html, base64, markdown
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
A = os.path.join(ROOT, 'assets/briefings/christmas-decorations')
POST = os.path.join(ROOT, '_posts/2026-11-16-deck-the-halls-check-the-rules.md')
FONTS = 'file://' + os.path.join(ROOT, 'assets/fonts')
LOGO = 'file://' + os.path.join(ROOT, 'assets/brand/logo.svg')
AS_AT = '16 November 2026'

def b64(path, mime='image/svg+xml'):
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()

BUNTING = os.path.join(A, 'bunting.svg')

KPIS = [('£252.3m', 'UK imports of Christmas articles in 2025; 81.9% from China by value, 91.3% by weight (HMRC)'),
        ('£77,500', "Belfast City Hall's artificial tree: 16.6 m, ten-year stated life (council minutes, Nov 2025)"),
        ('9,371', 'Candle fires in England, nine years to March 2019; the highest severe-casualty rate of any cause (Home Office)'),
        ('17 Oct 2023', 'Loose plastic glitter restricted in NI (EU 2023/2055). Still legal in GB.'),
        ('19 Oct 2026', 'Vans need a permit and a booked slot at Redlands, Larne; 12 visits a year, no Sundays'),
        ('£400 v £5,000', 'Maximum fly-tipping fixed penalty: NI against England (from 1 Sep 2026). Litter: £200 against £750'),
        ('34.15p', 'Power NI unit rate incl. 5% VAT from 1 Jul 2026, against the GB cap of 26.32p (VAT zero-rated)'),
        ('0% to 23%', 'Irish VAT on plain white church candles: zero-rated from 1978, standard-rated since 1 Jan 2022'),
        ('1 Jan 2027', 'UK CBAM starts; aluminium foil (7607) is in scope, NI included')]

CSS = """
@font-face{font-family:'SS3';src:url('%(f)s/source-sans-3.woff')}
@font-face{font-family:'SS3';font-style:italic;src:url('%(f)s/source-sans-3-italic.woff')}
@font-face{font-family:'SS4';src:url('%(f)s/source-serif-4.woff')}
@font-face{font-family:'SS4';font-style:italic;src:url('%(f)s/source-serif-4-italic.woff')}
@font-face{font-family:'PM';src:url('%(f)s/ibm-plex-mono-regular.woff')}
@page{size:A4;margin:24mm 16mm 18mm}
@page:first{margin:0}
:root{--red:#A61C1C;--ink:#1A1A1A;--grey:#5a5a5a;--rule:#e3dedb;--tint:#faf3f3}
body{font-family:'SS3',sans-serif;font-size:10pt;line-height:1.5;color:#2b2b2b;margin:0}
.cover{height:297mm;box-sizing:border-box;padding:0 16mm 16mm;display:flex;flex-direction:column;break-after:page;
  background:linear-gradient(#fff 0,#fff 70%%,var(--tint) 100%%)}
.cover .garland{width:100%%;margin:0 0 6mm}
.cover .logo{height:60px;margin-top:22mm;align-self:flex-start}
.cover .tag{font-family:'PM',monospace;font-size:8pt;color:var(--grey);margin-top:3pt}
.cover .kicker{font-family:'PM',monospace;text-transform:uppercase;letter-spacing:.14em;font-size:8.5pt;color:var(--red);margin:70mm 0 10pt}
.cover h1{font-family:'SS4',serif;font-weight:600;font-size:38pt;line-height:1.1;color:var(--ink);margin:0 0 10pt}
.cover h1 em{color:var(--red);font-style:normal}
.cover .stand{font-family:'SS4',serif;font-size:13pt;max-width:160mm;margin:0 0 10mm}
.cover .baubles{display:flex;gap:14mm;margin:0;position:absolute;top:12mm;right:20mm}
.cover .baubles img{height:120px}
.cover .baubles img:nth-child(2){height:170px}
.cover{position:relative}
.cover .meta{margin-top:auto;font-size:8.5pt;color:var(--grey);border-top:1px solid var(--rule);padding-top:8pt}
h2{font-family:'SS4',serif;font-weight:600;font-size:14pt;color:var(--ink);margin:16pt 0 6pt;padding-top:8pt;border-top:1px solid var(--rule);break-after:avoid}
h3{font-family:'SS4',serif;font-weight:600;font-size:11.5pt;color:var(--ink);margin:12pt 0 4pt;break-after:avoid}
p{margin:0 0 7pt} ul,ol{margin:0 0 8pt;padding-left:18px} li{margin-bottom:4pt} li::marker{color:var(--red)}
a{color:var(--red);text-decoration:none}
figure{margin:8pt 0 10pt;break-inside:avoid} figure img{width:100%%} figcaption{font-size:8.5pt;color:var(--grey);margin-top:3pt}
table{width:100%%;border-collapse:collapse;font-size:8.6pt;margin:6pt 0 10pt;break-inside:avoid}
th,td{text-align:left;padding:4pt 5pt;border-bottom:1px solid var(--rule);vertical-align:top}
th{border-bottom:2px solid var(--ink);color:var(--ink)}
td:first-child{font-weight:700;color:var(--ink)}
.lab{font-family:'PM',monospace;font-size:7.6pt;letter-spacing:.12em;text-transform:uppercase;color:var(--red);margin:0 0 4pt}
.dash h2{border-top:0;padding-top:0;margin-top:0}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:8pt;margin:4pt 0 10pt}
.kpis div{border:1px solid var(--rule);border-top:3px solid var(--red);padding:7pt 9pt;break-inside:avoid}
.kpis b{display:block;font-family:'SS4',serif;font-size:15pt;color:var(--ink);font-weight:600}
.kpis span{font-size:8pt;color:var(--grey);line-height:1.35;display:block}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:8pt 12pt}
.grid2 figure{margin:0}
.carol ol{list-style:none;padding:0;counter-reset:d}
.carol li{background:var(--tint);border-left:3px solid var(--red);padding:6pt 9pt;margin:0 0 6pt;break-inside:avoid}
.sources ul{font-size:7.8pt;line-height:1.35} .sources a{color:#2b2b2b}
.note{font-size:8.5pt;color:var(--grey);font-style:italic}
.end{font-size:8.5pt;color:var(--grey);border-top:1px solid var(--rule);padding-top:8pt;margin-top:12pt}
"""

def post_body():
    s = open(POST, encoding='utf-8').read()
    fm, body = s.split('---', 2)[1], s.split('---', 2)[2]
    title = re.search(r'^title: "(.*)"$', fm, re.M).group(1)
    body = re.sub(r'<figure class="page-photo[^"]*"><img src="\{\{ \'/assets/briefings/christmas-decorations/bunting.svg\'.*?</figure>', '', body, flags=re.S)
    body = re.sub(r"\{\{ '/assets/briefings/christmas-decorations/([^']+)' \| relative_url \}\}", lambda m: 'file://' + os.path.join(A, m.group(1)), body)
    body = re.sub(r"\{\{ '([^']+)' \| relative_url \}\}", r'https://robertjpark.co.uk\1', body)
    body = '\n'.join(l for l in body.split('\n') if not l.startswith('[Download the briefing (PDF)]'))
    body = re.sub(r'\n---\n.*?(?=\n## Sources)', '\n', body, flags=re.S)  # drop author footer
    return title, body

def kpi_html():
    return ''.join(f'<div><b>{html.escape(a)}</b><span>{html.escape(b)}</span></div>' for a, b in KPIS)

def pdf():
    title, body = post_body()
    h = markdown.markdown(body, extensions=['tables'])
    h = h.replace('<h2>The twelve days of regulation</h2>', '<div class="carol"><h2>The twelve days of regulation</h2>')
    h = h.replace('<h2>What I&rsquo;d change</h2>', '</div><h2>What I&rsquo;d change</h2>').replace("<h2>What I'd change</h2>", "</div><h2>What I'd change</h2>")
    h = h.replace('<h2>Sources</h2>', '<div class="sources"><h2>Sources</h2>') + '</div>'
    first_p = re.search(r'<p><em>(.*?)</em></p>', h, re.S)
    status = first_p.group(1) if first_p else ''
    h = h.replace(first_p.group(0), f'<p class="note">{status}</p>', 1) if first_p else h
    bauble = b64(os.path.join(A, 'bauble.svg'))
    def fig(name, alt): return f'<figure><img src="file://{os.path.join(A, name)}" alt="{html.escape(alt)}"></figure>'
    dash = f"""<section class="dash"><div class="lab">Dashboard · as at {AS_AT}</div><h2>Christmas decorations in numbers</h2>
<div class="kpis">{kpi_html()}</div>
<div class="grid2">{fig('imports-christmas-articles.svg','UK imports of Christmas articles 2025')}{fig('lights-season-cost.svg','Cost of running lights for a season')}
{fig('litter-fines.svg','Maximum fixed penalties')}{fig('imports-fresh-trees.svg','UK imports of fresh Christmas trees 2025')}</div>
<p class="note">Full tables, sources and CSV downloads: robertjpark.co.uk/tools/dashboards/christmas-decorations.html</p></section>"""
    garland = b64(BUNTING)
    doc = f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{CSS % {'f': FONTS}}</style></head><body>
<section class="cover">
<img class="logo" src="{LOGO}" alt="Robert J. Park"><div class="tag">Environment · Carbon · Public Affairs</div>
<div class="kicker">Briefing · Christmas · Product safety · Public realm</div>
<h1>Deck the halls, <em>check the rules</em></h1>
<p class="stand">Father Christmas, banned Christmases and decorations from Nuremberg tinsel to the carbon tax on your turkey foil: who makes them, how they are regulated, Belfast's £77,500 artificial tree, van permits at Larne's recycling centre, twelve ways to a better Christmas, and a carol for the regulators. Nollaig Shona daoibh.</p>
<div class="baubles"><img src="{bauble}" alt=""><img src="{bauble}" alt=""><img src="{bauble}" alt=""></div>
<div class="meta">Robert J. Park · Larne, Northern Ireland · {AS_AT}<br>robert@robertjpark.co.uk · 07450 349480 · robertjpark.co.uk<br>Status as at {AS_AT}. Not legal, tax or customs advice.</div></section>
{dash}
{h}
<p class="end">Robert J. Park is an independent environment, carbon and public affairs consultant based in Larne, Northern Ireland. robert@robertjpark.co.uk · robertjpark.co.uk · WhatsApp @robertjpark. Facts checked to {AS_AT}.</p>
</body></html>"""
    tmp = os.path.join(ROOT, '_scripts/briefings/christmas-decorations/_tmp.html')
    open(tmp, 'w', encoding='utf-8').write(doc)
    head = f"<div style='width:100%;padding:0 16mm;margin-top:-2mm'><img src='{garland}' style='width:100%;height:12mm;object-fit:cover;object-position:top'></div>"
    foot = f"<div style='font-family:sans-serif;font-size:7pt;color:#5a5a5a;width:100%;padding:0 16mm;display:flex;justify-content:space-between'><span>Robert J. Park · Deck the halls, check the rules · {AS_AT} · robertjpark.co.uk</span><span><span class='pageNumber'></span> / <span class='totalPages'></span></span></div>"
    out = os.path.join(ROOT, 'assets/briefings/2026-11-christmas-decorations-briefing.pdf')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(); pg.goto('file://' + tmp); pg.wait_for_timeout(600)
        pg.pdf(path=out, format='A4', print_background=True, prefer_css_page_size=True, display_header_footer=True,
               header_template=head, footer_template=foot)
        b.close()
    os.remove(tmp); print(out)

def card():
    bauble = b64(os.path.join(A, 'bauble.svg'))
    doc = f"""<html><head><style>{CSS % {'f': FONTS}} body{{margin:0}}</style></head><body>
<div style="width:1200px;height:630px;box-sizing:border-box;padding:0 60px 40px;display:flex;flex-direction:column;background:linear-gradient(#fff 60%,#faf3f3)">
<img src="{b64(BUNTING)}" style="width:100%">
<div style="font-family:PM;letter-spacing:.14em;text-transform:uppercase;color:#A61C1C;font-size:20px;margin-top:20px">Christmas · Product safety · Public realm</div>
<div style="font-family:SS4;font-weight:600;font-size:70px;line-height:1.05;color:#1A1A1A;margin-top:14px">Deck the halls,<br><span style="color:#A61C1C">check the rules</span></div>
<div style="font-family:SS4;font-size:28px;color:#2b2b2b;margin-top:16px;max-width:900px">Glitter restricted in Larne, legal in Stranraer. Twelve ways to a better Christmas. Nollaig Shona daoibh.</div>
<div style="margin-top:auto;display:flex;align-items:flex-end;justify-content:space-between"><img src="{LOGO}" style="height:52px"><div style="display:flex;gap:18px"><img src="{bauble}" style="height:130px"><img src="{bauble}" style="height:100px"></div></div>
</div></body></html>"""
    tmp = os.path.join(ROOT, '_scripts/briefings/christmas-decorations/_card.html'); open(tmp, 'w').write(doc)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1200, 'height': 630}); pg.goto('file://' + tmp); pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(A, 'christmas-decorations-card.png')); b.close()
    os.remove(tmp)

MATRIX = [
 ('Loose plastic glitter', 'Restricted since 17 Oct 2023 (EU 2023/2055)', 'Legal; no restriction decided (16 Mar 2026)', 'Restricted since 17 Oct 2023'),
 ('General product safety', 'EU GPSR 2023/988 since 13 Dec 2024', 'GPSR 2005; new framework consulted on, Mar–Jun 2026', 'EU GPSR since 13 Dec 2024'),
 ('Fairy lights marking', 'CE only, not UKCA', 'UKCA or CE', 'CE'),
 ('Packaging design and labels', 'EU PPWR from 12 Aug 2026, plus UK packaging EPR', 'UK packaging EPR', 'EU PPWR from 12 Aug 2026'),
 ('Generic "eco" claims', 'Case by case, DMCC Act (from 6 Apr 2025)', 'Case by case, DMCC Act', 'Banned unless proven from 27 Sep 2026 (Directive 2024/825)*'),
 ('Cut Christmas tree from GB', 'Retail scheme, or certificate and notification', 'Within GB: none under 3 m; UK plant passport over 3 m', 'Phytosanitary certificate'),
 ('VAT on a candle', '20%', '20%', '23% (white church candles were 0% from 1978 to 2021)'),
 ('Maximum fly-tipping fixed penalty', '£400', '£5,000 in England (since 1 Sep 2026)', 'Not checked'),
 ('Maximum litter fixed penalty', '£200 (since 30 Dec 2022)', '£750 in England (since 1 Sep 2026)', 'Not checked'),
 ('Aluminium foil (CBAM)', 'UK CBAM from 1 Jan 2027', 'UK CBAM from 1 Jan 2027', 'EU CBAM, definitive since 1 Jan 2026'),
 ('Electricity price', 'Power NI 34.15p/kWh incl. 5% VAT (regulated tariff)', 'Ofgem cap 26.32p/kWh, VAT zero-rated to 31 Mar 2027', 'Not compared')]

def dashboard():
    def inline(name):
        k = name[:-4]
        return open(os.path.join(A, name)).read().replace('aria-labelledby="t d"', f'aria-labelledby="{k}-t {k}-d"').replace('id="t"', f'id="{k}-t"').replace('id="d"', f'id="{k}-d"')
    import csv as _csv, io
    buf = io.StringIO(); w = _csv.writer(buf); w.writerow(['issue', 'northern_ireland', 'great_britain', 'ireland_eu']); [w.writerow(r) for r in MATRIX]
    open(os.path.join(ROOT, 'data/dashboards/christmas-decorations/rules-matrix.csv'), 'w').write(buf.getvalue())
    rows = ''.join(f'<tr><th scope="row">{html.escape(a)}</th><td>{html.escape(b)}</td><td>{html.escape(c)}</td><td>{html.escape(d)}</td></tr>' for a, b, c, d in MATRIX)
    fonts = '../../assets/fonts'
    doc = f"""<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Christmas decorations: rules, costs and carbon in Northern Ireland | Robert J. Park</title>
<meta name="description" content="Dashboard: Christmas decorations in Northern Ireland. Glitter, product safety, packaging, litter fines, CBAM on foil, tree carbon and the cost of running lights, as at {AS_AT}.">
<link rel="icon" href="../../assets/favicon.png">
<style>
@font-face{{font-family:'SS3';src:url('{fonts}/source-sans-3.woff')}}@font-face{{font-family:'SS4';src:url('{fonts}/source-serif-4.woff')}}@font-face{{font-family:'PM';src:url('{fonts}/ibm-plex-mono-regular.woff')}}
:root{{--red:#A61C1C;--ink:#1A1A1A;--muted:#5a5a5a;--rule:#e6e2e0;--tint:#faf3f3}}
body{{font-family:'SS3',sans-serif;color:#2b2b2b;margin:0;line-height:1.5}}
main{{max-width:1100px;margin:0 auto;padding:0 1rem 3rem}}
header{{max-width:1100px;margin:0 auto;padding:1rem}} header a{{color:var(--ink);text-decoration:none;font-family:'SS4',serif;font-weight:600}}
.garland{{width:100%;display:block}}
h1{{font-family:'SS4',serif;font-weight:600;font-size:2rem;color:var(--ink);margin:.5rem 0}}
h2{{font-family:'SS4',serif;font-weight:600;color:var(--ink);border-top:1px solid var(--rule);padding-top:1rem;margin-top:2rem}}
.eyebrow{{font-family:'PM',monospace;text-transform:uppercase;letter-spacing:.12em;font-size:.8rem;color:var(--red)}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.75rem}}
.kpis div{{border:1px solid var(--rule);border-top:4px solid var(--red);padding:.75rem 1rem}}
.kpis b{{display:block;font-family:'SS4',serif;font-size:1.6rem;color:var(--ink)}} .kpis span{{font-size:.9rem;color:var(--muted)}}
.charts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(460px,1fr));gap:1rem}}
.charts figure{{margin:0;border:1px solid var(--rule);padding:.75rem}} .charts svg{{width:100%;height:auto}}
table{{width:100%;border-collapse:collapse;font-size:.95rem}} th,td{{text-align:left;padding:.5rem;border-bottom:1px solid var(--rule);vertical-align:top}}
thead th{{border-bottom:2px solid var(--ink)}} tbody th{{color:var(--ink)}}
a{{color:var(--red)}} .note{{font-size:.9rem;color:var(--muted)}}
@media (max-width:520px){{.charts{{grid-template-columns:1fr}} table{{font-size:.85rem}}}}
</style></head><body>
<img class="garland" src="../../assets/briefings/christmas-decorations/bunting.svg" alt="">
<header><a href="/">Robert J. Park</a> · <a href="/dashboards/">Dashboards</a></header>
<main>
<p class="eyebrow">Dashboard · as at {AS_AT}</p>
<h1>Christmas decorations: rules, costs and carbon</h1>
<p>How the decorations in Northern Ireland's homes, shops and streets are regulated, what they cost to run and what they emit, and where the rules in Northern Ireland, Great Britain and the EU differ. Read the commentary: <a href="/blog/2026/11/deck-the-halls-check-the-rules/">Deck the halls, check the rules</a>. Not legal, tax or customs advice.</p>
<h2>Headline figures</h2><div class="kpis">{kpi_html()}</div>
<h2>Charts</h2><p class="note">Hover or tap a bar for its value.</p>
<div class="charts">
<figure>{inline('imports-christmas-articles.svg')}</figure><figure>{inline('imports-fresh-trees.svg')}</figure>
<figure>{inline('lights-season-cost.svg')}</figure><figure>{inline('litter-fines.svg')}</figure>
<figure>{inline('tree-cumulative-carbon.svg')}</figure><figure>{inline('tree-breakeven-studies.svg')}</figure>
<figure>{inline('tree-carbon.svg')}</figure><figure>{inline('fires-1959.svg')}</figure>
</div>
<h2>One decoration, three rulebooks</h2>
<table><caption class="note" style="text-align:left">Status as at {AS_AT}. *Application in NI not confirmed by an official source.</caption>
<thead><tr><th scope="col">Issue</th><th scope="col">Northern Ireland</th><th scope="col">Great Britain</th><th scope="col">Ireland / EU</th></tr></thead><tbody>{rows}</tbody></table>
<h2>Data and sources</h2>
<ul>
<li><a href="../../data/dashboards/christmas-decorations/rules-matrix.csv">Rules matrix (CSV)</a></li>
<li><a href="../../data/dashboards/christmas-decorations/hmrc-imports-2025.csv">UK imports of Christmas articles, lights and trees (CSV)</a>: HMRC Overseas Trade Statistics, calendar 2025, retrieved 16 November 2026; sums of monthly figures. EU imports are recorded by country of dispatch, so the China share is probably understated.</li>
<li>Candle fires: Home Office, In-depth review of fire-related fatalities and severe casualties in England, 2010/11 to 2018/19. Belfast tree: council working group minutes, 18 November 2025. Redlands: Mid and East Antrim Borough Council. Irish candle VAT: S.I. 146 of 1978 and Revenue.</li>
<li><a href="../../data/dashboards/christmas-decorations/lights-season-cost.csv">Cost of running lights (CSV)</a>: 240 hours; Power NI 34.15p/kWh incl. VAT from 1 Jul 2026 (Utility Regulator, Power NI); Ofgem cap 26.32p/kWh, 1 Oct–31 Dec 2026, with GB domestic electricity VAT zero-rated to 31 Mar 2027. Bulb ratings: Yukon Government and US EPA Energy Star; the 40 W mini-light rating is an assumption.</li>
<li><a href="../../data/dashboards/christmas-decorations/tree-carbon.csv">Tree carbon over 20 years (CSV)</a>: 40, 16 and 3.5 kg CO2e as quoted by the British Christmas Tree Growers Association (trade body), attributed to the Carbon Trust but not on the Carbon Trust's own page. The Carbon Trust's own advice is 7 to 20 years of reuse.</li>
<li>Litter fines: SR 2012/35 reg 3 as amended by SR 2022/302 (NI); S.I. 2026/816 (England, from 1 September 2026). Fly-tipping: Waste and Contaminated Land (NI) Order 1997 art. 4A; GOV.UK, 15 July 2026. Fires 1959: Hansard, 8 December 1960.</li>
<li>Full source list: <a href="/blog/2026/11/deck-the-halls-check-the-rules/#sources">the article</a> and the <a href="../../assets/briefings/2026-11-christmas-decorations-briefing.pdf">briefing PDF</a>.</li>
</ul>
<p class="note">Robert J. Park · Environment · Carbon · Public Affairs · Larne, Northern Ireland · robert@robertjpark.co.uk · 07450 349480</p>
</main></body></html>"""
    open(os.path.join(ROOT, 'tools/dashboards/christmas-decorations.html'), 'w', encoding='utf-8').write(doc)

card(); dashboard(); pdf()
