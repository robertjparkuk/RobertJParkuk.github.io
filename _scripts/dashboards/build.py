"""Build the five Focus on dashboards as static, self-contained HTML pages.
Every figure comes from a source checked on 20-21 October 2026; derived figures are labelled.
Usage: python3 build.py <repo_root>
"""
import sys, html, csv, io, urllib.parse, re, os

ROOT = sys.argv[1]
AG = open(os.path.join(ROOT, 'tools/dashboards/ni-agriculture-land-carbon.html'), encoding='utf-8').read()
HEAD_CSS = AG[AG.index('<style>') + 7: AG.index('</style>')]
K_CSS = re.search(r'<style>(\.k-wrap.*?)</style>', AG, re.S).group(1)
K_CSS = K_CSS[:K_CSS.index('.sc-flow')]
EXTRA_CSS = """
.k-bar-row.k-hi .k-bar-label{font-weight:600}
.k-div{position:relative;height:14px;background:var(--cds-chart-grid);border-radius:7px}
.k-div .k-mid{position:absolute;left:50%;top:-3px;bottom:-3px;width:1px;background:var(--color-fg-muted)}
.k-div .k-bar{position:absolute;top:0;height:100%}
.k-bar.k-pos{background:var(--color-bad)} .k-bar.k-neg{background:var(--color-ok)}
.k-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:var(--cds-gap-md);font-size:13px}
.k-src{font-size:13px;color:var(--color-fg-muted);margin-top:var(--cds-gap-sm)}
.k-wide{grid-column:1/-1}
.k-tiles{grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr))}
.k-pill{display:inline-block;font-size:12px;padding:1px 8px;border-radius:10px;border:1px solid var(--color-border-line);color:var(--color-fg-muted)}
"""

SRC = {
 'ghg': ('NI greenhouse gas inventory 1990–2024 statistical bulletin (DAERA/NISRA)', 'https://datavis.nisra.gov.uk/daera/northern-ireland-greenhouse-gas-inventory-1990-2024-statistical-bulletin.html'),
 'ghg_notes': ('NI GHG inventory user notes: sector definitions (NISRA)', 'https://explore.nisra.gov.uk/northern-ireland-greenhouse-gas-inventory/user-notes.html'),
 'fd2022': ('NI food and drinks processing sector 2022 (NISRA, 10 April 2025)', 'https://www.nisra.gov.uk/news/total-gross-turnover-northern-ireland-food-and-drinks-processing-sector-2022-reaches-ps6516'),
 'fd2020': ('NI food and drinks processing sector 2019–2020 (DAERA, 25 August 2022)', 'https://www.daera-ni.gov.uk/news/report-northern-ireland-food-and-drinks-processing-sector-daera-10'),
 'irishnews': ('NI-produced food sales top £7bn (Irish News, 10 April 2025)', 'https://ie.irishnews.com/news/business/northern-ireland-produced-food-still-on-the-menu-worldwide-as-sales-top-7bn-mark-3JR6R5LTF5BMTDRLSWDXJO75JY/'),
 'eudr': ('Deforestation-free products in NI (GOV.UK, updated 27 August 2026)', 'https://www.gov.uk/guidance/moving-exporting-or-placing-deforestation-free-products-on-the-market-in-northern-ireland'),
 'packuk': ('PackUK Year 2 (letsrecycle, 4 March 2026)', 'https://www.letsrecycle.com/news/packuk-confirms-shortfall-as-63m-announces-year-2-recovery-target/'),
 'drs': ('Deposit Return Scheme (DAERA)', 'https://www.daera-ni.gov.uk/articles/extended-producer-responsibility-deposit-return-scheme-single-use-drinks-containers'),
 'foodwaste': ('Food Waste Regulations (NI) 2015', 'https://www.legislation.gov.uk/nisr/2015/14/note/made'),
 'esos': ('ESOS phase 4 guidance (GOV.UK)', 'https://www.gov.uk/government/publications/comply-with-the-energy-savings-opportunity-scheme-esos-phase-4/how-to-comply-with-the-energy-savings-opportunity-scheme-esos-phase-4'),
 'cbam': ('CBAM for Northern Ireland businesses (April 2026)', 'https://www.sustainableni.org/assets/cms/downloads/Carbon-Border-Adjustment-Mechanism-CBAM-for-Northern-Ireland-businesses-April-2026.pdf'),
 'tour': ('Northern Ireland tourism statistics 2025 (NISRA)', 'https://datavis.nisra.gov.uk/tourism/tourism25.html'),
 'elec': ('Electricity consumption and renewable generation, year ending June 2026 (DfE, 3 September 2026)', 'https://www.economy-ni.gov.uk/news/electricity-consumption-and-renewable-generation-northern-ireland-year-ending-june-2026'),
 'eecg': ('Energy Efficiency Capital Grant (Invest NI)', 'https://www.investni.com/support-for-business/reduce-waste-and-save-energy/energy-efficiency-capital-grant'),
 'recg': ('Resource Efficiency Capital Grant (Invest NI)', 'https://www.investni.com/support-for-business/reduce-waste-and-save-energy/resource-efficiency-capital-grant'),
 'fgas': ('Fluorinated greenhouse gases (DAERA)', 'https://www.daera-ni.gov.uk/articles/fluorinated-greenhouse-gases'),
 'fgas27': ('EU F-gas Regulation 2027 bans (Projet Celsius, September 2026)', 'https://projetcelsius.com/en/blog/f-gas-regulation-2027-bans/'),
 'trade': ('NI Economic Trade Statistics 2024 (DfE/NISRA, 11 March 2026)', 'https://www.economy-ni.gov.uk/news/northern-ireland-economic-trade-statistics-2024-northern-ireland-annual-business-inquiry-2024'),
 'tradeni': ('NI Economic Trade Statistics (NISRA)', 'https://www.nisra.gov.uk/statistics/business/ni-economic-trade'),
 'mni': ('Manufacturing and the Northern Ireland Economy (Manufacturing NI, May 2025)', 'https://www.manufacturingni.org/wp-content/uploads/2025/05/Manufacturing-and-the-Northern-Ireland-Economy.pdf'),
 'ets': ('ETS linkage agreed, The Day in Trade (Institute of Export & International Trade, 8 October 2026)', 'https://www.export.org.uk/insights/trade-news/the-day-in-trade-emissions-trading-scheme-linkage-agreed-burnham-in-berlin-and-french-minister-says-uk-can-come-back-anytime-to-eu/'),
 'ev': ('Public EV charging infrastructure statistics, 1 July 2026 (DfT)', 'https://www.gov.uk/government/statistics/electric-vehicle-charging-infrastructure-statistics-1-july-2026/public-electric-vehicle-charging-infrastructure-statistics-1-july-2026'),
 'evatt': ('Attitudes towards electric vehicles in NI 2023/24 (DfI/NISRA)', 'https://datavis.nisra.gov.uk/infrastructure/electricvehiclereport.html'),
 'pt': ('Public transport statistics NI 2024-25 (DfI, 10 September 2025)', 'https://www.infrastructure-ni.gov.uk/news/public-transport-statistics-northern-ireland-2024-25-statistical-report-has-been-published-today'),
 'ecg': ('Electric Car Grant open in NI (DfI, 25 July 2025)', 'https://www.infrastructure-ni.gov.uk/news/kimmins-welcomes-grant-scheme-purchase-zero-emission-vehicles'),
 'ecg2': ('Electric Car Grant: funding and price cap (RAC, April 2026)', 'https://www.rac.co.uk/drive/electric-cars/choosing/electric-car-grant/'),
 'bik': ('Company car tax rates (Fleet News; PayFit)', 'https://www.fleetnews.co.uk/news/budget-fuel-duty-frozen-and-new-company-car-tax-rates-published'),
 'maritime': ('UK ETS expands to maritime from 1 July 2026 (DNV)', 'https://www.dnv.com/news/2026/the-uk-ets-expands-to-maritime-from-1-july-2026/'),
 'zegv': ('Zero emission goods vehicles screening form (DfI, May 2026)', 'https://www.infrastructure-ni.gov.uk/publications/proposals-changes-regulations-support-uptake-zero-emission-goods-vehicles-northern-ireland-screening-form'),
 'con1': ('NI Quarterly Construction Bulletin, Q1 2026 (NISRA, 25 June 2026)', 'https://datavis.nisra.gov.uk/economy-and-labour-market/construction-bulletin-northern-ireland-quarter-1-2026.html'),
 'con2': ('Construction output statistics, Q2 2026 (NISRA, 24 September 2026)', 'https://www.nisra.gov.uk/statistics/economic-output/construction-output-statistics'),
 'bres': ('NI Business Register and Employment Survey 2024 (DfE/NISRA, 8 October 2026)', 'https://www.economy-ni.gov.uk/news/northern-ireland-business-register-and-employment-survey-statistics-2024'),
 'niw': ('NI Water update to Belfast City Council (Water Magazine, 29 January 2026)', 'https://www.watermagazine.co.uk/2026/01/29/ni-water-updates-belfast-city-council-on-current-state-of-investment-and-wastewater-capacity-pressures/'),
 'wms': ('Developer contributions for wastewater infrastructure (DfI Written Ministerial Statement, 19 March 2026)', 'https://www.niassembly.gov.uk/assembly-business/official-report/written-ministerial-statements/department-for-infrastructure-developer-contributions-for-wastewater-infrastructure'),
 'cland': ('Contaminated land (DAERA)', 'https://www.daera-ni.gov.uk/articles/contaminated-land-daera'),
 'ukgbc': ('Whole Life Carbon Roadmap FAQs (UK Green Building Council)', 'https://ukgbc.org/news/the-whole-life-carbon-roadmap-answering-your-data-faqs-received-to-date/'),
}

SECTORS = [  # TES sector, base year Mt, 2024 Mt, share 2024 %, change since base %
 ('Agriculture', 5.2, 5.8, 31.4, 10.0), ('Domestic transport', 3.6, 3.9, 21.3, 9.2),
 ('Buildings and product uses', 4.5, 2.8, 15.5, -36.7), ('Land use (LULUCF)', 2.6, 2.1, 11.7, -18.2),
 ('Electricity supply', 5.3, 2.0, 10.8, -62.6), ('Industry', 3.3, 1.0, 5.5, -69.4), ('Waste', 1.5, 0.7, 3.8, -52.9)]

def esc(s): return html.escape(str(s), quote=True)
def link(k): t, u = SRC[k]; return f'<a href="{esc(u)}" rel="noopener">{esc(t)}</a>'

def csv_href(cols, rows):
    b = io.StringIO(); w = csv.writer(b); w.writerow(cols); [w.writerow(r) for r in rows]
    return 'data:text/csv;charset=utf-8,' + urllib.parse.quote('﻿' + b.getvalue())

def fmt(v, unit=''):
    if isinstance(v, float) and abs(v) < 1000: s = f'{v:,.1f}'
    elif isinstance(v, (int, float)): s = f'{v:,.0f}'
    else: s = str(v)
    return s.replace('-', '−') + unit

def tile(lab, big, sub, tone=''):
    return f'<div class="k-tile"><div class="k-lab">{esc(lab)}</div><div class="k-big {tone}">{esc(big)}</div><div class="k-sub">{esc(sub)}</div></div>'

def card(title, note, body, src_keys, csv=None, fname=None, wide=False):
    act = ''
    if csv:
        act = f'<div class="k-actions"><a download="{esc(fname)}.csv" href="{csv}">Download CSV</a></div>'
    srcs = '; '.join(link(k) for k in src_keys)
    return (f'<section class="k-card{" k-wide" if wide else ""}" aria-label="{esc(title)}"><h3>{esc(title)}</h3>'
            f'<p class="k-note">{note}</p>{body}{act}<p class="k-src">Source: {srcs}</p></section>')

def bars(rows, unit='', hi=None, maxv=None):
    """rows: (label, value, display or None)."""
    m = maxv or max(abs(r[1]) for r in rows)
    out = ['<div class="k-bars" role="list">']
    for lab, v, disp in rows:
        w = 0 if not m else abs(v) / m * 100
        h = ' k-hi' if hi and lab in hi else ''
        acc = ' k-accent' if hi and lab in hi else ''
        out.append(f'<div class="k-bar-row{h}" role="listitem"><span class="k-bar-label">{esc(lab)}</span>'
                   f'<span class="k-bar-track" aria-hidden="true"><span class="k-bar{acc}" style="width:{w:.1f}%"></span></span>'
                   f'<span class="k-bar-val">{esc(disp if disp is not None else fmt(v, unit))}</span></div>')
    return ''.join(out) + '</div>'

def divbars(rows, unit='%', hi=None, good_when_negative=True):
    m = max(abs(r[1]) for r in rows)
    out = ['<div class="k-bars" role="list">']
    for lab, v in rows:
        w = abs(v) / m * 50
        cls = ('k-neg' if v < 0 else 'k-pos') if good_when_negative else ('k-pos' if v < 0 else 'k-neg')
        left = 50 - w if v < 0 else 50
        h = ' k-hi' if hi and lab in hi else ''
        sign = '+' if v > 0 else ''
        out.append(f'<div class="k-bar-row{h}" role="listitem"><span class="k-bar-label">{esc(lab)}</span>'
                   f'<span class="k-div" aria-hidden="true"><span class="k-mid"></span><span class="k-bar {cls}" style="left:{left:.1f}%;width:{w:.1f}%"></span></span>'
                   f'<span class="k-bar-val">{esc((sign + fmt(v)).replace("-", chr(8722)) + unit)}</span></div>')
    return ''.join(out) + '</div>'

def table(cols, rows, num_cols=()):
    th = ''.join(f'<th scope="col">{esc(c)}</th>' for c in cols)
    trs = ''.join('<tr>' + ''.join(f'<td class="k-num">{esc(c)}</td>' if i in num_cols else f'<td>{esc(c)}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
    return f'<div class="k-tablebox"><table class="k-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'

def sector_card(hi):
    rows = [(s[0], s[2], f'{s[2]:.1f} Mt · {s[3]:.1f}%') for s in SECTORS]
    body = bars(rows, hi=hi, maxv=6.0)
    csvh = csv_href(['sector', 'base_year_mtco2e', 'y2024_mtco2e', 'share_2024_pct', 'change_since_base_pct'], [list(s) for s in SECTORS])
    return card('NI emissions by sector, 2024', 'Net emissions 18.4 MtCO2e. The highlighted sector is the one this dashboard covers.', body, ['ghg'], csvh, 'ni-emissions-by-sector-2024')

def change_card(hi):
    body = divbars([(s[0], s[4]) for s in SECTORS], hi=hi)
    return card('Change since the base year', 'Percentage change in each sector, base year (1990 for most gases) to 2024. Red is a rise, green a fall.', body, ['ghg'])

def page(slug, title, h1, lead, tiles, cards, issue_url, issue_title, issue_date, desc):
    srcs_used = []
    for c in cards:
        for k in re.findall(r'href="([^"]+)" rel="noopener"', c):
            if k not in srcs_used: srcs_used.append(k)
    rev = {u: t for t, u in SRC.values()}
    src_list = ''.join(f'<li><a href="{esc(u)}" rel="noopener">{esc(rev[html.unescape(u)] if html.unescape(u) in rev else u)}</a></li>' for u in srcs_used)
    url = f'https://robertjpark.co.uk/tools/dashboards/{slug}.html'
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://robertjpark.co.uk/assets/og-image.jpg">
<link rel="icon" type="image/svg+xml" href="/assets/tools-mark.svg">
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<style>{HEAD_CSS}</style>
<style>{K_CSS}{EXTRA_CSS}</style>
</head>
<body>
<header class="site-top">
  <a class="brand" href="/" aria-label="Robert J. Park home"><img src="/assets/tools-mark.svg" alt="" width="30" height="30">Robert J. <b>Park</b> · Dashboards</a>
  <nav aria-label="Main"><a href="/">Home</a><a href="/services/">Services</a><a href="/tools/">Tools</a><a href="/dashboards/">Dashboards</a><a href="/blog/">Blog</a><a href="/contact/">Contact</a></nav>
</header>
<main id="dash-root">
<div class="k-wrap">
<header class="k-head"><h1>{esc(h1)}</h1>
<p>{lead}</p></header>
<div class="k-tiles">{''.join(tiles)}</div>
<h2 class="k-h2">The figures</h2>
<div class="k-grid">{''.join(cards)}</div>
<h2 class="k-h2">Sources</h2>
<section class="k-card"><p class="k-note">Every figure on this page comes from these sources, checked on 20–21 October 2026. Figures marked "derived" are worked out from the published numbers. This is a dated snapshot: nothing is fetched or sent, and every chart can be downloaded as CSV.</p><ul>{src_list}</ul></section>
<p class="k-foot">Commentary: <a href="{issue_url}">{esc(issue_title)}</a>. More dashboards: <a href="/dashboards/">all dashboards</a>.</p>
</div>
</main>
<footer class="site-foot">Robert J. Park · Environment · Carbon · Public Affairs · Northern Ireland. Figures checked on 21 October 2026, for publication with the issue of {esc(issue_date)}; see <a href="{issue_url}">{esc(issue_title)}</a> for the commentary. <a href="/contact/">Contact</a> · <a href="/privacy/">Privacy</a></footer>
</body>
</html>
'''

D = {}

# 1 Food & drink processing ----------------------------------------------------
fd_turn = [('2020', 5424, '£5,424m'), ('2022', 6516, '£6,516m'), ('2023 (provisional)', 7128, '£7,128m')]
fd_dest = [('Great Britain', 3160, '£3.2bn · 48.5%'), ('Northern Ireland (derived)', 1402, '≈£1.4bn'), ('Republic of Ireland', 1100, '£1.1bn'), ('Rest of EU', 631, '£631m'), ('Rest of world', 223.1, '£223m')]
eudr_rows = [
 ('Cattle', 'Beef, hides, leather', 'DAERA'), ('Cocoa', 'Chocolate, cocoa butter and powder', 'DAERA'),
 ('Coffee', 'Roasted and green beans', 'DAERA'), ('Oil palm', 'Palm oil and derivatives', 'DAERA'),
 ('Soya', 'Soya beans, meal and oil (animal feed)', 'DAERA'), ('Wood', 'Timber, furniture, pallets, paper and cartons', 'OPSS'),
 ('Rubber', 'Tyres and rubber goods', 'OPSS')]
fd_dead = [('Nov 2026', 'Packaging EPR fees recalculated for 2026/27', 'Packaging producers'),
 ('30 Dec 2026', 'EUDR applies in NI (medium and large businesses)', 'First placers of in-scope products'),
 ('31 Dec 2026', 'ESOS phase 4 qualification date', '250+ staff, or >£44m turnover and >£38m balance sheet'),
 ('1 Jan 2027', 'UK CBAM starts, including fertiliser imports', 'Importers; costs pass down the chain'),
 ('30 Jun 2027', 'EUDR applies to most micro and small businesses', 'Smaller processors'),
 ('Oct 2027', 'Deposit return scheme goes live', 'Drinks producers and retailers'),
 ('5 Dec 2027', 'ESOS phase 4 notification deadline', 'ESOS-qualifying businesses')]
D['ni-food-drink-processing'] = dict(
 title='NI Food and Drink Processing dashboard', h1='NI food and drink processing',
 desc='Dashboard of Northern Ireland food and drink processing: turnover, markets, jobs, industry emissions, deforestation rules and deadlines. By Robert J. Park.',
 lead='Northern Ireland food and drink processors turned over an estimated <b>£7.1bn</b> in 2023, with almost half of sales going to Great Britain. Industry emissions, where factory fuel is counted, are down <b>69%</b> since 1990. The pressures now are customers, deforestation rules, packaging fees and deposit return.',
 tiles=[tile('Turnover, 2023 (provisional)', '£7.1bn', 'Up 9.4% on 2022'), tile('Share of sales to GB', '48.5%', '2022; the largest market'),
        tile('Jobs, 2022', '25,508', 'Full-time equivalents; 30.1% of NI manufacturing jobs'), tile('NI industry emissions change', '−69%', 'Base year to 2024; includes all manufacturing', 'k-good'),
        tile('EUDR starts in NI', '30 Dec 2026', 'Medium and large businesses'), tile('Food waste threshold', '5 kg', 'A week; above this it must be collected separately')],
 cards=[
  card('Turnover', 'Gross turnover of the sector, £ million. 2021 is not shown because only a provisional estimate was published.', bars(fd_turn, hi=['2023 (provisional)']), ['fd2020', 'fd2022'], csv_href(['year', 'turnover_gbp_m'], [[r[0], r[1]] for r in fd_turn]), 'ni-food-drink-turnover'),
  card('Where sales go, 2022', 'Sales by destination. The NI figure is derived as total turnover less the published external markets, so treat it as approximate.', bars(fd_dest, hi=['Great Britain']), ['fd2022', 'irishnews'], csv_href(['destination', 'sales_gbp_m', 'note'], [[r[0], r[1], 'derived' if 'derived' in r[0] else ''] for r in fd_dest]), 'ni-food-drink-markets-2022'),
  sector_card(['Industry']), change_card(['Industry']),
  card('EU deforestation rules: what is in scope', 'Commodities covered by the EU Deforestation Regulation in NI and who enforces. Scope depends on the commodity code.', table(['Commodity', 'Examples', 'Enforcer'], eudr_rows), ['eudr'], csv_href(['commodity', 'examples', 'enforcer'], eudr_rows), 'eudr-scope-ni'),
  card('Deadlines', 'Dates that affect processors in the next 14 months.', table(['When', 'What', 'Who'], fd_dead), ['eudr', 'packuk', 'drs', 'esos', 'cbam', 'foodwaste'], csv_href(['when', 'what', 'who'], fd_dead), 'food-drink-deadlines', wide=True),
 ], issue='/blog/focus-on-food-and-drink-processing-october-2026/', issue_title='Focus on Food & Drink Processing, 23 October 2026', date='23 October 2026')

# 2 Hospitality, retail and leisure ------------------------------------------
trips = [('NI residents', 1.76, '1.76m · +12%'), ('Great Britain', 1.48, '1.48m · +4%'), ('Republic of Ireland', 1.30, '1.30m · +15%'), ('Outside UK and ROI', 0.553, '0.55m · −3%')]
occ = [('Hotels 2024', 68, '68%'), ('Hotels 2025', 65, '65%'), ('Guest houses and B&Bs 2024', 40, '40%'), ('Guest houses and B&Bs 2025', 41, '41%')]
fgas_rows = [('1 Jan 2025', 'Split systems under 3 kg (≤12 kW)', 'GWP above 750'), ('1 Jan 2027', 'Self-contained (plug-in) units up to 50 kW', 'GWP 150 or more'),
 ('1 Jan 2027', 'Split air-to-water heat pumps ≤12 kW; chillers ≤12 kW', 'GWP 150 or more'), ('1 Jan 2027', 'Chillers above 12 kW', 'GWP 750 or more'),
 ('1 Jan 2029', 'Split air-to-air (air conditioning) ≤12 kW', 'GWP 150 or more'), ('1 Jan 2029', 'Split above 12 kW (VRF)', 'GWP 750 or more')]
hr_dead = [('30 Dec 2026', 'EUDR applies in NI (medium and large businesses)', 'Coffee, cocoa, palm-oil, beef and timber buyers'),
 ('31 Dec 2026', 'ESOS phase 4 qualification date', 'Large groups'), ('1 Jan 2027', 'EU F-gas limits on new cooling kit; HFC quota roughly halves', 'Anyone buying cooling in NI'),
 ('30 Jun 2027', 'EUDR applies to most micro and small businesses', 'Independent cafés and shops'), ('Oct 2027', 'Deposit return scheme goes live', 'Drinks retailers, pubs, hotels, venues')]
grants = [('Energy Efficiency Capital Grant', 'Paused for review; no reopening date', 'Heating, cooling, motors, lighting, renewables; min £4,000 spend'),
          ('Resource Efficiency Capital Grant', 'Closed; no new applications after 27 March 2026', 'Up to £50k; 30% small, 20% medium, 10% large')]
D['ni-hospitality-retail-leisure'] = dict(
 title='NI Hospitality, Retail and Leisure dashboard', h1='NI hospitality, retail and leisure',
 desc='Dashboard of Northern Ireland tourism, occupancy, building emissions, refrigerant rules, grants and deadlines for hospitality, retail and leisure. By Robert J. Park.',
 lead='Overnight trips in Northern Ireland rose <b>9%</b> to 5.1 million in 2025 and spend reached <b>£1.2bn</b>, but hotel occupancy fell to <b>65%</b>. Heating and refrigeration sit in the buildings sector of the NI inventory, which still emits 2.8 MtCO2e a year.',
 tiles=[tile('Overnight trips, 2025', '5.1m', 'Up 9% on 2024'), tile('Visitor spend, 2025', '£1.2bn', 'Up 9% on 2024'),
        tile('Hotel room occupancy, 2025', '65%', 'Down from 68% in 2024', 'k-bad'), tile('Buildings and product uses, 2024', '2.8 Mt', '15.5% of NI emissions; up 5% on 2023'),
        tile('Renewable electricity', '50%', 'Year to June 2026; target 80% by 2030'), tile('Deposit return starts', 'Oct 2027', 'PET, steel and aluminium, 150ml to 3 litres')],
 cards=[
  card('Overnight trips by market, 2025', 'Trips and change on 2024. Visitors from the Republic of Ireland grew fastest.', bars(trips, hi=['Republic of Ireland']), ['tour'], csv_href(['market', 'trips_m', 'label'], [list(r) for r in trips]), 'ni-trips-by-market-2025'),
  card('Occupancy', 'Room occupancy for hotels and bed-space occupancy for guest houses and B&Bs.', bars(occ, hi=['Hotels 2025'], maxv=100), ['tour'], csv_href(['measure', 'pct'], [[r[0], r[1]] for r in occ]), 'ni-occupancy-2024-2025'),
  sector_card(['Buildings and product uses']), change_card(['Buildings and product uses']),
  card('Refrigerant limits on new equipment (EU F-gas Regulation 2024/573, applies in NI)', 'Bans on placing new equipment on the market. Kit placed before the date can still be installed and serviced. Great Britain has different rules.', table(['From', 'Equipment', 'Banned refrigerants'], fgas_rows), ['fgas', 'fgas27'], csv_href(['from', 'equipment', 'banned'], fgas_rows), 'eu-fgas-equipment-bans', wide=True),
  card('Grant support', 'Invest NI capital grants for energy and resource efficiency, as at October 2026.', table(['Scheme', 'Status', 'What it covered'], grants), ['eecg', 'recg'], csv_href(['scheme', 'status', 'covers'], grants), 'invest-ni-grants-status'),
  card('Deadlines', 'Dates that affect hospitality, retail and leisure.', table(['When', 'What', 'Who'], hr_dead), ['eudr', 'esos', 'fgas27', 'drs'], csv_href(['when', 'what', 'who'], hr_dead), 'hospitality-deadlines'),
 ], issue='/blog/focus-on-hospitality-retail-leisure-october-2026/', issue_title='Focus on Hospitality, Retail & Leisure, 30 October 2026', date='30 October 2026')

# 3 Metals and manufacturing ---------------------------------------------------
dest = [('Within Northern Ireland', 69.5, '£69.5bn'), ('Great Britain', 20.1, '£20.1bn · +14.2%'), ('Republic of Ireland', 10.5, '£10.5bn · +19.6%'), ('Rest of the world (derived)', 5.5, '≈£5.5bn'), ('Rest of the EU', 3.6, '£3.6bn · +23.5%')]
cbam_goods = [('Iron and steel', 'Yes', 'Yes'), ('Aluminium', 'Yes', 'Yes'), ('Cement', 'Yes', 'Yes'), ('Fertilisers', 'Yes', 'Yes'), ('Hydrogen', 'Yes', 'Yes'), ('Electricity', 'Yes', 'No'), ('Glass and ceramics', 'No', 'No (excluded at start)')]
cbam_dates = [('1 Jan 2026', 'EU CBAM definitive period begins', 'EU importers'), ('1 Jan 2027', 'UK CBAM starts', 'Importers from outside the UK and EU'),
 ('1 Feb 2027', 'EU CBAM certificate sales open for 2026 imports', 'EU importers; NI DDP sellers'), ('30 Sep 2027', 'First EU CBAM annual declaration and surrender', 'EU importers; NI DDP sellers'),
 ('5 Dec 2027', 'ESOS phase 4 notification deadline', 'Large businesses'), ('31 Jan 2028', 'UK CBAM registration deadline for 2027', 'Importers past £50,000'),
 ('31 May 2028', 'First UK CBAM return and payment', 'Registered importers')]
D['ni-metals-manufacturing'] = dict(
 title='NI Metals and Manufacturing dashboard', h1='NI metals and manufacturing',
 desc='Dashboard of Northern Ireland manufacturing: industry emissions, sales by market, UK and EU CBAM scope and dates, and renewable electricity. By Robert J. Park.',
 lead='NI industry emissions fell from <b>3.3</b> to <b>1.0</b> MtCO2e between the base year and 2024. NI businesses sold <b>£20.1bn</b> to Great Britain and <b>£14.1bn</b> to the EU in 2024. From 1 January 2027 the UK carbon border levy applies to imported steel, aluminium, cement, fertiliser and hydrogen.',
 tiles=[tile('Industry emissions, 2024', '1.0 Mt', 'Down from 3.3 Mt in the base year'), tile('Change since base year', '−69.4%', 'Largest fall of any NI sector', 'k-good'),
        tile('Sales to the EU, 2024', '£14.1bn', 'ROI £10.5bn + rest of EU £3.6bn'), tile('Sales to GB, 2024', '£20.1bn', 'Up 14.2% on 2023'),
        tile('Manufacturing share of jobs', '10.5%', 'Workforce jobs, Sept 2023; UK 7.1%'), tile('UK CBAM registration', '£50,000', 'Covered imports a year')],
 cards=[
  card('Where NI sales go, 2024', 'All NI businesses, not manufacturing alone. Rest of world is derived as exports outside the UK (£19.6bn) less ROI and rest of EU.', bars(dest, hi=['Republic of Ireland', 'Rest of the EU']), ['trade', 'tradeni'], csv_href(['destination', 'sales_gbp_bn', 'label'], [list(r) for r in dest]), 'ni-sales-by-destination-2024'),
  sector_card(['Industry']), change_card(['Industry']),
  card('Goods covered by CBAM', 'UK CBAM from 1 January 2027 and EU CBAM. Indirect emissions are out of UK CBAM until 2029 at the earliest.', table(['Goods', 'EU CBAM', 'UK CBAM'], cbam_goods), ['cbam'], csv_href(['goods', 'eu_cbam', 'uk_cbam'], cbam_goods), 'cbam-goods'),
  card('CBAM and ESOS dates', 'Key dates for NI manufacturers. UK–EU emissions trading linking, reported as agreed in October 2026, would exempt goods covered by both schemes once in force.', table(['When', 'What', 'Who'], cbam_dates), ['cbam', 'esos', 'ets'], csv_href(['when', 'what', 'who'], cbam_dates), 'cbam-esos-dates', wide=True),
  card('Renewable share of NI electricity', 'Share of gross final electricity consumption from renewables, year to June, against the 2030 target. Cleaner electricity lowers Scope 2.', bars([('Year to June 2025', 44, '44%'), ('Year to June 2026', 50, '50%'), ('2030 target', 80, '80%')], hi=['Year to June 2026'], maxv=100), ['elec'], csv_href(['period', 'renewable_share_pct'], [['Year to June 2025', 44], ['Year to June 2026', 50], ['2030 target', 80]]), 'ni-renewable-electricity'),
 ], issue='/blog/focus-on-metals-manufacturing-november-2026/', issue_title='Focus on Metals & Manufacturing, 6 November 2026', date='6 November 2026')

# 4 Transport and fleet -------------------------------------------------------
chg = [('London', 345.1), ('Scotland', 231.6), ('Wales', 185.5), ('United Kingdom', 174.9), ('West Midlands', 164.0), ('South East', 159.4), ('South West', 156.7), ('North East', 150.2), ('East of England', 150.2), ('East Midlands', 121.5), ('North West', 112.1), ('Yorkshire and the Humber', 110.7), ('Northern Ireland', 60.0)]
rapid = [('Scotland', 59.1), ('South West', 49.5), ('East of England', 48.8), ('East Midlands', 46.7), ('West Midlands', 45.7), ('Wales', 42.8), ('United Kingdom', 41.7), ('North West', 40.0), ('South East', 39.7), ('North East', 37.1), ('Yorkshire and the Humber', 36.6), ('London', 27.9), ('Northern Ireland', 19.3)]
journeys = [('Bus 2019-20', 68.3, '68.3m'), ('Bus 2023-24', 64.4, '64.4m'), ('Bus 2024-25', 67.8, '67.8m'), ('Rail 2019-20', 15.1, '15.1m'), ('Rail 2023-24', 13.8, '13.8m'), ('Rail 2024-25', 13.3, '13.3m')]
intent = [('2021/22', 38, '38%'), ('2022/23', 33, '33%'), ('2023/24', 25, '25%')]
barriers = [('Purchase price', 75, '75%'), ('Need to recharge', 49, '49%'), ('Public charge points', 44, '44%'), ('Range per charge', 40, '40%')]
bik = [('2025/26', '3%', '—'), ('2026/27', '4%', '—'), ('2027/28', '5%', '—'), ('2028/29', '7%', '18%'), ('2029/30', '9%', '19%')]
D['ni-transport-fleet'] = dict(
 title='NI Transport and Fleet dashboard', h1='NI transport and fleet',
 desc='Dashboard of Northern Ireland transport emissions, EV charging, public transport, EV attitudes and company car tax. By Robert J. Park.',
 lead='Domestic transport emitted <b>3.9 MtCO2e</b> in 2024, <b>21%</b> of NI emissions and 9% more than in 1990. NI has <b>60</b> public chargers per 100,000 people, the fewest in the UK, and interest in buying an EV has fallen.',
 tiles=[tile('Transport emissions, 2024', '3.9 Mt', '21.3% of NI emissions'), tile('Change since base year', '+9.2%', 'One of three sectors that rose', 'k-bad'),
        tile('Public chargers per 100,000', '60', 'UK 174.9; 1 July 2026', 'k-bad'), tile('Rapid chargers per 100,000', '19.3', 'UK 41.7; 50 kW and above', 'k-bad'),
        tile('Translink journeys, 2024-25', '81.1m', '2.7% below 2019-20'), tile('Would consider an EV next', '25%', 'Of drivers, 2023/24; 38% in 2021/22', 'k-bad')],
 cards=[
  card('Public EV chargers per 100,000 people', 'All public EV chargers, 1 July 2026. Northern Ireland is lowest.', bars([(a, b, None) for a, b in chg], hi=['Northern Ireland']), ['ev'], csv_href(['area', 'chargers_per_100k'], [list(r) for r in chg]), 'ev-chargers-per-100k-jul-2026'),
  card('Rapid chargers per 100,000 people', '50 kW and above, 1 July 2026.', bars([(a, b, None) for a, b in rapid], hi=['Northern Ireland']), ['ev'], csv_href(['area', 'rapid_per_100k'], [list(r) for r in rapid]), 'ev-rapid-per-100k-jul-2026'),
  sector_card(['Domestic transport']), change_card(['Domestic transport']),
  card('Translink passenger journeys', 'Millions of journeys. Bus is close to pre-COVID; rail is 12% below.', bars(journeys, hi=['Bus 2024-25', 'Rail 2024-25']), ['pt'], csv_href(['mode_year', 'journeys_m'], [[r[0], r[1]] for r in journeys]), 'translink-journeys'),
  card('Drivers who would consider an EV next', 'Share saying they would definitely or strongly consider an EV as their next car.', bars(intent, hi=['2023/24'], maxv=100), ['evatt'], csv_href(['survey_year', 'pct'], [[r[0], r[1]] for r in intent]), 'ni-ev-intent'),
  card('Barriers to buying an EV, 2023/24', 'Share of drivers citing each barrier; more than one answer allowed.', bars(barriers, maxv=100), ['evatt'], csv_href(['barrier', 'pct'], [[r[0], r[1]] for r in barriers]), 'ni-ev-barriers'),
  card('Company car tax (benefit-in-kind)', 'Appropriate percentage for zero emission cars and plug-in hybrids emitting 1–50 g/km. Tax years start 6 April.', table(['Tax year', 'Zero emission', 'Plug-in hybrid 1–50 g/km'], bik), ['bik'], csv_href(['tax_year', 'zero_emission', 'phev_1_50'], bik), 'company-car-bik'),
  card('What else has changed', 'Policies affecting fleets and freight in NI.', table(['Item', 'Detail'], [('Electric Car Grant', 'Open in NI; up to £3,750 on eligible cars up to £37,000; funded to 2030'), ('UK ETS for shipping', 'Since 1 July 2026: ships 5,000 GT and above on domestic voyages, including GB–NI sailings'), ('GB ZEV mandate', 'Made under an Order covering Great Britain only'), ('Zero emission goods vehicles', 'DfI regulation changes screened April 2026')]), ['ecg', 'ecg2', 'maritime', 'zegv'], wide=True),
 ], issue='/blog/focus-on-transport-fleet-november-2026/', issue_title='Focus on Transport & Fleet, 13 November 2026', date='13 November 2026')

# 5 Construction and building --------------------------------------------------
cidx = [('All construction', 116.5, 10.1), ('New work', 117.9, 18.6), ('Housing', 131.8, 27.4), ('Infrastructure', 101.6, 3.9), ('Other work', 113.2, 0.7), ('Repair and maintenance', 111.9, -2.5)]
con_rules = [('UK CBAM', '1 Jan 2027', 'Imported iron, steel, aluminium and cement from outside the UK and EU, once covered imports pass £50,000 a year'),
 ('EUDR (timber)', '30 Dec 2026', 'First placers of wood and wood products on the NI market; most micro and small businesses from 30 Jun 2027'),
 ('Contaminated land regime', 'Not commenced', 'Part 3 of the 1997 Order not in force; contamination handled through planning'),
 ('Wastewater developer contributions', 'Voluntary scheme planned', 'Announced 19 March 2026; compulsory levy still under consideration')]
D['ni-construction-building'] = dict(
 title='NI Construction and Building dashboard', h1='NI construction and building',
 desc='Dashboard of Northern Ireland construction output, housing, wastewater capacity, building emissions and rules on imported materials. By Robert J. Park.',
 lead='NI construction output in early 2026 was <b>10%</b> above a year earlier and housing <b>27%</b> above. NI Water says around <b>£7bn</b> is needed for wastewater, and capacity limits decide where homes can connect.',
 tiles=[tile('Construction output, Q1 2026', '116.5', 'Index, 2023 = 100; +10.1% on a year earlier'), tile('Housing output, Q1 2026', '+27.4%', 'On a year earlier; index 131.8'),
        tile('Output, Q2 2026', '−1.7%', 'On the quarter; +3.5% on the year'), tile('Wastewater investment needed', '£7bn', 'NI Water estimate', 'k-bad'),
        tile('Belfast storm overflows unsatisfactory', '156 of 192', 'NI Water, January 2026', 'k-bad'), tile('Homes unlocked since autumn 2024', '5,300', 'By £30m extra wastewater funding', 'k-good')],
 cards=[
  card('Output by type of work, Q1 2026', 'Volume index, 2023 average = 100. Provisional.', bars([(a, b, f'{b:.1f}') for a, b, c in cidx], hi=['Housing']), ['con1'], csv_href(['type', 'index_q1_2026', 'change_on_year_pct'], [list(r) for r in cidx]), 'ni-construction-q1-2026'),
  card('Change on a year earlier, Q1 2026', 'Percentage change in volume. Green is growth.', divbars([(a, c) for a, b, c in cidx], hi=['Housing'], good_when_negative=False), ['con1']),
  sector_card(['Industry', 'Buildings and product uses']), change_card(['Industry', 'Buildings and product uses']),
  card('Rules on materials, land and connections', 'What applies to NI contractors, developers and merchants.', table(['Rule', 'When', 'What it means'], con_rules), ['cbam', 'eudr', 'cland', 'wms'], csv_href(['rule', 'when', 'detail'], con_rules), 'construction-rules', wide=True),
  card('Context', 'Wider figures behind the issue.', table(['Measure', 'Figure'], [('Construction jobs, year to Sept 2024', '+2,040 (+5.5%)'), ('Output vs pre-pandemic (Q4 2019), Q2 2026', '+17.5%'), ('UK emissions the built environment is directly responsible for', 'About a quarter (UKGBC, UK-wide)'), ('Share of built environment emissions from construction and refurbishment', 'About a fifth (UKGBC)')]), ['bres', 'con2', 'ukgbc', 'niw'], wide=True),
 ], issue='/blog/focus-on-construction-building-november-2026/', issue_title='Focus on Construction & Building, 20 November 2026', date='20 November 2026')

for slug, d in D.items():
    out = page(slug, d['title'], d['h1'], d['lead'], d['tiles'], d['cards'], d['issue'], d['issue_title'], d['date'], d['desc'])
    open(os.path.join(ROOT, 'tools/dashboards', slug + '.html'), 'w', encoding='utf-8').write(out)
    print(slug, len(out))
