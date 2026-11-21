"""Build the SPS deal dashboard (21 Nov 2026): tools/dashboards/ni-sps-food-trade.html.
Reuses the site wrapper and k- styles from ni-screen-industry.html. Data: assets/dashboards/sps-deal/*.csv
(DAERA, NAEI), charts: assets/briefings/sps-deal/*.svg (built by _scripts/briefings/sps-deal/charts.py).
Usage: python3 build_sps.py <repo_root>"""
import sys, os, csv, html
ROOT = os.path.abspath(sys.argv[1])
tpl = open(os.path.join(ROOT, 'tools/dashboards/ni-screen-industry.html'), encoding='utf-8').read()
head = tpl[:tpl.index('</head>')]
TITLE = 'NI food, farming and the SPS deal: the numbers'
DESC = 'Where Northern Ireland food and drink processors sell and buy, what NI farms produce and emit, carbon intensity by industry, and the trend to 2035, for the UK–EU SPS deal of 20 November 2026. By Robert J. Park.'
URL = 'https://robertjpark.co.uk/tools/dashboards/ni-sps-food-trade.html'
import re
head = re.sub(r'<title>.*?</title>', f'<title>{html.escape(TITLE)}</title>', head)
head = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + html.escape(DESC), head)
head = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + html.escape(DESC), head)
head = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + html.escape(TITLE), head)
head = head.replace('https://robertjpark.co.uk/tools/dashboards/ni-screen-industry.html', URL)
head = head.replace('/assets/og-image.jpg', '/assets/dashboards/ni-sps-food-trade.jpg')
head += '<style>.k-chart img{width:100%;height:auto;display:block;background:#fff;border-radius:6px}.k-chart{padding:var(--cds-pad-md)}.k-dl{font-size:13px}.k-terms{font-size:var(--cds-font-size-caption);color:var(--color-fg-muted)}</style>\n'
D = os.path.join(ROOT, 'assets/dashboards/sps-deal')
rd = lambda f: list(csv.DictReader(open(os.path.join(D, f))))
dest = rd('sales_destination.csv'); purch = rd('purchases_origin_2022.csv'); inten = rd('intensity.csv'); proj = rd('projection.csv')
em = rd('farm_emissions.csv')
d22 = {r['destination']: float(r['gbp_m']) for r in dest if r['year'] == '2022'}
t22 = sum(d22.values()); gb = d22['Great Britain']; eu = d22['Ireland'] + d22['Rest of EU']
p = {r['origin']: float(r['gbp_m']) for r in purch}
emt = lambda y: sum(float(r['kt_co2e']) for r in em if r['year'] == y)
d90 = {r['destination']: float(r['gbp_m']) for r in dest if r['year'] == '1990'}
f0 = lambda v: f'{v:,.0f}'
def tile(lab, big, sub): return f'<div class="k-tile"><div class="k-lab">{lab}</div><div class="k-big">{big}</div><div class="k-sub">{sub}</div></div>'
def chart(img, title, note, alt, csvf):
    return (f'<section class="k-card k-wide" aria-label="{html.escape(title)}"><h3>{html.escape(title)}</h3><p class="k-note">{note}</p>'
            f'<div class="k-chart"><img src="/assets/briefings/sps-deal/{img}" alt="{html.escape(alt)}" loading="lazy" width="900"></div>'
            f'<p class="k-dl"><a href="/assets/dashboards/sps-deal/{csvf}" download>Download the data (CSV)</a></p></section>')
def table(title, note, cols, rows, csvf):
    th = ''.join(f'<th scope="col">{c}</th>' for c, _ in cols)
    tr = ''.join('<tr>' + ''.join(f'<td class="{"" if i == 0 else "k-num"}">{html.escape(fn(r) if fn else r[k])}</td>' for i, (k, fn) in enumerate([(c[1][0], c[1][1]) for c in cols])) + '</tr>' for r in rows)
    return (f'<section class="k-card k-wide" aria-label="{html.escape(title)}"><h3>{html.escape(title)}</h3><p class="k-note">{note}</p>'
            f'<div class="k-tablebox"><table class="k-table"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
            f'<p class="k-dl"><a href="/assets/dashboards/sps-deal/{csvf}" download>Download the data (CSV)</a></p></section>')
num = lambda k, f='{:,.0f}': (k, lambda r: f.format(float(r[k])))
txt = lambda k: (k, None)
ptot = {k: sum(float(r[k]) for r in proj) for k in ('y2015', 'y2022', 'y2030', 'y2035')}
body = f'''<body>
<header class="site-top">
  <a class="brand" href="/" aria-label="Robert J. Park home"><img src="/assets/tools-mark.svg" alt="" width="30" height="30">Robert J. <b>Park</b> · Dashboards</a>
  <nav aria-label="Main"><a href="/">Home</a><a href="/services/">Services</a><a href="/tools/">Tools</a><a href="/dashboards/">Dashboards</a><a href="/blog/">Blog</a><a href="/contact/">Contact</a></nav>
</header>
<main id="dash-root">
<div class="k-wrap">
<header class="k-head"><h1>{html.escape(TITLE)}</h1>
<p>Northern Ireland (NI) food and drink processors sell <b>{gb/t22*100:.0f}%</b> of their output to Great Britain (GB) and <b>{eu/t22*100:.0f}%</b> to the European Union (EU). The UK–EU sanitary and phytosanitary (SPS) deal on food, animal and plant health, due to apply from 1 March 2028, removes most food checks on GB processors selling into the EU, though, unlike NI firms, they still face customs. Status as at 21 November 2026. General information, not legal advice.</p></header>
<div class="k-tiles">
{tile("Sold to GB, 2022", f"£{f0(gb)}m", "NI food and drink processors")}
{tile("Sold to Ireland and rest of EU, 2022", f"£{f0(eu)}m", "NI food and drink processors")}
{tile("Inputs bought from GB, 2022", f"£{f0(p['Great Britain'])}m", "Livestock, milk, packaging and other goods")}
{tile("Inputs bought from the EU, 2022", f"£{f0(p['Ireland']+p['Rest of EU'])}m", "Ireland and rest of EU")}
{tile("NI farm emissions, 2024", f"{f0(emt('2024'))} kt", f"Kilotonnes of carbon dioxide equivalent (CO2e); {100*(emt('2024')/emt('1990')-1):+.0f}% since 1990")}
</div>
<h2 class="k-h2">Where NI food goes, and where its inputs come from</h2>
<div class="k-grid">
{chart("sales-destination.svg", "Half of NI processed food goes to GB, a quarter to the EU", "Share of sales by value, 1990, 2015 and 2022; centre figure is total sales, current prices.", "Donut charts: 1990 NI 44%, GB 33%, Ireland 7%, rest of EU 6%, EU intervention stores 7%; 2015 GB 48%, NI 26%, Ireland 14%, rest of EU 9%; 2022 GB 49%, NI 22%, Ireland 17%, rest of EU 10%.", "sales_destination.csv")}
<section class="k-card k-wide" aria-label="EU intervention stores"><h3>What were "EU intervention stores"?</h3>
<p>Under the old Common Agricultural Policy (CAP) of the European Community, when market prices fell below a set floor, each member state's intervention agency had to buy beef, butter, skimmed milk powder and cereals at a guaranteed price and keep them in cold store until prices recovered. The agencies were national and the Community paid; the EU did not exist until 1993. In the UK the buyer was the Intervention Board for Agricultural Produce, with the Department of Agriculture for Northern Ireland, and from August 1990 the Livestock Marketing Commission for Northern Ireland, supervising work here.</p>
<p>In 1990 NI processors sold <b>£{f0(d90['EU intervention stores'])}m</b> to intervention, 7% of their sales and more than they sold to Ireland (£{f0(d90['Ireland'])}m) or the rest of the EU (£{f0(d90['Rest of EU'])}m). Beef was the main product. By June 1991 the Community held about 760,000 tonnes of beef, 235,000 tonnes of it in Ireland. The 1992 MacSharry reforms cut support prices and limited buying; by 2015 DAERA records no NI processing sales to intervention. It survives in EU law as a safety net, mainly for butter and skimmed milk powder.</p>
<p class="k-src">Sources: Hansard written answers of 26 April 1985, 16 March 1990, 22 October 1990, 6 June 1991 and 3 April 1996; Dáil Éireann, 4 July 1991; Commission Regulations (EEC) No 1166/90 and 2722/90.</p></section>
{chart("bought-and-sold.svg", "Bought in from GB and the EU, made in NI, sold back to both", "2022, £m. Purchases are Department of Agriculture, Environment and Rural Affairs (DAERA) experimental statistics.", "Bars: GB, bought £886m, sold £3,162m; Ireland and rest of EU, bought £969m, sold £1,710m.", "purchases_origin_2022.csv")}
</div>
<h2 class="k-h2">What NI farms and food firms produce</h2>
<div class="k-grid">
{chart("farm-output.svg", "Milk has overtaken cattle as the biggest earner on NI farms", "Share of gross agricultural output, current prices; 2024 as revised by DAERA in August 2026. In 2025 (provisional) cattle output rose 37% on higher prices.", "Donut charts: 1990 total £931m, cattle 30%, milk 24%; 2015 £1,781m, milk 27%, cattle 23%; 2024 £3,215m, milk 34%, cattle 20%.", "farm_output.csv")}
{chart("processing-mix.svg", "Beef and dairy are half of NI food processing, as in 1990", "Share of food and drink processing turnover, current prices; firms over £250,000 turnover.", "Donut charts: 1990 £1,745m, milk 26%, beef and sheepmeat 24%; 2015 £4,417m, beef 28%, milk 20%; 2022 £6,516m, beef 26%, milk 24%.", "processing.csv")}
</div>
<h2 class="k-h2">Emissions and carbon intensity</h2>
<div class="k-grid">
{chart("farm-emissions.svg", "Cattle make two thirds of NI farm emissions; dairy is the part still growing", "Agricultural greenhouse gas emissions by source, kt CO2e. Livestock is enteric fermentation plus manure management. Source: National Atmospheric Emissions Inventory (NAEI).", "Donut charts: 1990 5,238 kt, beef and other cattle 43%, dairy 18%; 2015 5,694 kt, beef 43%, dairy 24%; 2024 5,762 kt, beef 42%, dairy 26%.", "farm_emissions.csv")}
{table("Carbon intensity by industry", "Direct emissions from the animals and their manure, and kilograms of CO2e per £ of farm output, current prices. Beef and other cattle includes dairy replacement heifers, and cattle output includes dairy culls and calves, so the beef and dairy split is approximate. On 2025 prices beef falls to about 2.7 because cattle prices rose, not because emissions fell. Pigs and poultry look low mainly because they produce little methane.",
 [("Industry", txt('industry')), ("kt CO2e 1990", num('kt_1990')), ("2015", num('kt_2015')), ("2024", num('kt_2024')), ("kg per £, 2024 prices", num('kg_per_gbp_2024', '{:.2f}')), ("2024 emissions on 2025 prices", num('kg_per_gbp_2025_prices', '{:.2f}'))], inten, "intensity.csv")}
</div>
<h2 class="k-h2">Where the trend points</h2>
<div class="k-grid">
{table(f"Up to £{ptot['y2035']/1000:.1f}bn by 2035, in 2015 prices", f"If each subsector keeps its 2015–22 real growth rate, food processing turnover rises from £{f0(ptot['y2022'])}m in 2022 to £{f0(ptot['y2030'])}m by 2030 and £{f0(ptot['y2035'])}m by 2035. Growing the total at its own 3.0% a year gives about £6.9bn and £8.0bn instead. A trend, not a forecast, and probably an overstatement: 2022 was a milk price spike and the gross domestic product (GDP) deflator lagged food prices; GB competition in the EU from 2028 bears hardest on beef and dairy; NI carbon budgets may cap cattle numbers.",
 [("Subsector", txt('subsector')), ("2015", num('y2015')), ("2022", num('y2022')), ("Real growth a year, %", num('growth_pct', '{:+.1f}')), ("2030 trend", num('y2030')), ("2035 trend", num('y2035'))], proj, "projection.csv")}
</div>
<h2 class="k-h2">Sources</h2>
<section class="k-card"><p class="k-note">Every figure comes from these official sources, checked on 21 November 2026. Derived figures (shares, intensities, projections) are Robert J. Park's arithmetic. This is a dated snapshot: nothing is fetched or sent.</p><ul>
<li>DAERA, <a href="https://www.daera-ni.gov.uk/sites/default/files/2026-08/Account%20Summary%20for%20Press%20Release%202025.pdf">2025 agricultural account summary</a>, 19 August 2026, and Aggregate Agricultural Account (Table 2.1), January 2026</li>
<li>DAERA, <a href="https://www.daera-ni.gov.uk/news/report-northern-ireland-food-and-drinks-processing-report-2022">NI Food and Drinks Processing Report 2022</a> and time series 1989–2022, April 2025</li>
<li>DAERA, <a href="https://www.daera-ni.gov.uk/sites/default/files/2025-11/25.26.108%20Stats%20Review%202024_1.pdf">Statistical Review of NI Agriculture 2024</a>, November 2025</li>
<li>Department for Energy Security and Net Zero, <a href="https://naei.energysecurity.gov.uk/">NAEI</a>, devolved administration greenhouse gas inventories 1990–2024, June 2026</li>
<li>Cabinet Office, <a href="https://www.gov.uk/government/publications/ukeu-summit-2026-key-documents/uk-eu-summit-2026-explainer-sps-html">UK-EU Summit 2026 Explainer: SPS</a>, 20 November 2026</li>
</ul><p class="k-terms">Terms: CAP, Common Agricultural Policy; CO2e, carbon dioxide equivalent; DAERA, Department of Agriculture, Environment and Rural Affairs; EU, European Union; GB, Great Britain; GDP, gross domestic product; kt, kilotonnes; NAEI, National Atmospheric Emissions Inventory; NI, Northern Ireland; SPS, sanitary and phytosanitary (food safety, animal health and plant health).</p></section>
<p class="k-foot">Read the piece: <a href="/blog/2026/11/the-sps-deal-what-it-means-for-northern-ireland/">The SPS deal: what Northern Ireland gains, what it gives away</a>, and <a href="/assets/briefings/2026-11-the-sps-deal-ni-briefing.pdf">the full briefing (PDF)</a>. More dashboards: <a href="/dashboards/">all dashboards</a>.</p>
</div>
</main>
<footer class="site-foot">Robert J. Park · Environment · Carbon · Public Affairs · Northern Ireland. Figures as at 21 November 2026. <a href="/contact/">Contact</a> · <a href="/privacy/">Privacy</a></footer>
</body>
</html>
'''
open(os.path.join(ROOT, 'tools/dashboards/ni-sps-food-trade.html'), 'w', encoding='utf-8').write(head + '</head>\n' + body)
print('ok')
