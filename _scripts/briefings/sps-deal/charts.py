"""SVG charts for the SPS deal briefing (21 Nov 2026). Data: data.json (DAERA, NAEI).
Usage: python3 charts.py <repo_root>"""
import sys, os, json, math, html
ROOT = os.path.abspath(sys.argv[1]); HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, 'data.json')))
OUT = os.path.join(ROOT, 'assets/briefings/sps-deal')
PAL = ['#a61c1c', '#2b2b2b', '#d9822b', '#3b7a57', '#4a6fa5', '#8e6c8a', '#c9a227', '#6b9ac4', '#b8b0a8', '#7d5a50']
FONT = "font-family=\"'Source Sans 3','Segoe UI',Arial,sans-serif\""
esc = html.escape

def donuts(fn, title, sub, years, series, centre, note, order=None, colours=None):
    groups = order or list(dict.fromkeys(g for y in years for g in series[y]))
    col = colours or {g: PAL[i % len(PAL)] for i, g in enumerate(groups)}
    W, R, r0, cy = 900, 105, 60, 215
    rows = math.ceil(len(groups) / 3)
    H = 360 + rows * 24 + 30
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}" {FONT}>',
         f'<rect width="{W}" height="{H}" fill="#fff"/>',
         f'<text x="24" y="34" font-size="21" font-weight="700" fill="#1a1a1a">{esc(title)}</text>',
         f'<text x="24" y="58" font-size="14" fill="#5a5a5a">{esc(sub)}</text>']
    for i, y in enumerate(years):
        cx = 150 + i * 300; d = {g: v for g, v in series[y].items() if v > 0}; tot = sum(d.values()); a = 0
        for g in groups:
            if g not in d: continue
            f = d[g] / tot; a0, a1 = a, a + f * 2 * math.pi; a = a1
            p = lambda ang, rad: (cx + rad * math.sin(ang), cy - rad * math.cos(ang))
            x1, y1 = p(a0, R); x2, y2 = p(a1, R); x3, y3 = p(a1, r0); x4, y4 = p(a0, r0); big = 1 if a1 - a0 > math.pi else 0
            o.append(f'<path d="M{x1:.1f} {y1:.1f}A{R} {R} 0 {big} 1 {x2:.1f} {y2:.1f}L{x3:.1f} {y3:.1f}A{r0} {r0} 0 {big} 0 {x4:.1f} {y4:.1f}Z" fill="{col[g]}" stroke="#fff" stroke-width="1.5"><title>{esc(g)}, {y}: {round(100*f)}%</title></path>')
            if f >= 0.06:
                mx, my = p((a0 + a1) / 2, R + 20)
                o.append(f'<text x="{mx:.1f}" y="{my + 5:.1f}" text-anchor="middle" font-size="14" fill="#1a1a1a">{round(100*f)}%</text>')
        o.append(f'<text x="{cx}" y="{cy - 2}" text-anchor="middle" font-size="22" font-weight="700" fill="#1a1a1a">{y}</text>')
        o.append(f'<text x="{cx}" y="{cy + 20}" text-anchor="middle" font-size="14" fill="#5a5a5a">{esc(centre(tot))}</text>')
    for j, g in enumerate(groups):
        lx, ly = 24 + (j % 3) * 290, 370 + (j // 3) * 24
        o.append(f'<rect x="{lx}" y="{ly - 12}" width="14" height="14" rx="2" fill="{col[g]}"/><text x="{lx + 22}" y="{ly}" font-size="14" fill="#2b2b2b">{esc(g)}</text>')
    o.append(f'<text x="24" y="{H - 12}" font-size="12" fill="#5a5a5a">{esc(note)}</text></svg>')
    open(os.path.join(OUT, fn), 'w').write('\n'.join(o)); print(fn)

gbm = lambda t: f'£{t:,.0f}m'
d = A['dest']
donuts('sales-destination.svg', 'Half of NI processed food now goes to GB, a quarter to the EU',
       'Where NI food and drink processors sell, share of sales by value; centre = total sales, current prices',
       ['1990', '2015', '2022'], d, gbm, 'Source: DAERA, NI Food and Drinks Processing Report 2022, time series (April 2025). Robert J. Park, robertjpark.co.uk',
       order=['Northern Ireland', 'Great Britain', 'Ireland', 'Rest of EU', 'Rest of world', 'EU intervention stores'],
       colours={'Northern Ireland': '#b8b0a8', 'Great Britain': '#a61c1c', 'Ireland': '#3b7a57', 'Rest of EU': '#4a6fa5', 'Rest of world': '#2b2b2b', 'EU intervention stores': '#c9a227'})
farm = {y: {} for y in ['1990', '2015', '2024']}
for k, v in A['farm'].items():
    for i, y in enumerate(farm): farm[y][k] = v[i]
for i, y in enumerate(farm): farm[y]['Other'] = A['gross'][i] - sum(v[i] for v in A['farm'].values())
donuts('farm-output.svg', 'Milk has overtaken cattle as the biggest earner on NI farms',
       'Share of NI gross agricultural output; centre = total, current prices; 2024 as revised August 2026',
       list(farm), farm, gbm, 'Source: DAERA, Aggregate Agricultural Account (Table 2.1), January 2026; 2024 revised in the 2025 account, August 2026.')
proc = {y: {} for y in ['1990', '2015', '2022']}
for k, v in A['proc'].items():
    for i, y in enumerate(proc): proc[y][k.replace('&', 'and')] = v[i]
donuts('processing-mix.svg', 'Beef and dairy are half of NI food processing, as in 1990',
       'Share of NI food and drink processing turnover; centre = total, current prices',
       list(proc), proc, gbm, 'Source: DAERA, NI Food and Drinks Processing Report 2022, time series (April 2025). Firms over £250,000 turnover.')
em = {y: {} for y in ['1990', '2015', '2024']}
for i, y in enumerate(em):
    for k, v in A['em'].items(): em[y][k] = v[i]
    em[y]['Soils and fertiliser'] = A['shared']['Soils and fertiliser'][i]
    em[y]['Other farm (fuel, indirect)'] = A['derived']['ag_total'][i] - sum(em[y].values())
donuts('farm-emissions.svg', 'Cattle make two thirds of NI farm emissions; dairy is the part still growing',
       'Share of NI agricultural greenhouse gas emissions by source; centre = total, kt CO2e',
       list(em), em, lambda t: f'{t:,.0f} kt', 'Source: NAEI, devolved administration GHG inventories 1990–2024 (June 2026). Livestock = enteric plus manure.',
       order=['Beef and other cattle', 'Dairy', 'Sheep', 'Pigs', 'Poultry', 'Soils and fertiliser', 'Other farm (fuel, indirect)'])

# Flows: bought from vs sold to, GB and EU, 2022
dd = A['dest']['2022']; pp = A['purch']
rows = [('Great Britain', pp['Great Britain'], dd['Great Britain']), ('Ireland and rest of EU', pp['Ireland'] + pp['Rest of EU'], dd['Ireland'] + dd['Rest of EU'])]
W, H = 900, 330; mx = max(max(b, s) for _, b, s in rows); sc = lambda v: v / mx * 560
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="NI processors bought £886m from GB and £969m from the EU in 2022, and sold £3,162m to GB and £1,710m to the EU" {FONT}>',
     f'<rect width="{W}" height="{H}" fill="#fff"/>',
     '<text x="24" y="34" font-size="21" font-weight="700" fill="#1a1a1a">Bought in from GB and the EU, made in NI, sold back to both</text>',
     '<text x="24" y="58" font-size="14" fill="#5a5a5a">NI food and drink processors, 2022, £m: inputs bought from, and sales to, each market</text>']
y = 95
for name, b, s in rows:
    o.append(f'<text x="24" y="{y}" font-size="16" font-weight="700" fill="#1a1a1a">{name}</text>')
    o.append(f'<text x="24" y="{y + 30}" font-size="14" fill="#5a5a5a">Bought from</text><rect x="140" y="{y + 14}" width="{sc(b):.1f}" height="24" fill="#b8b0a8"/><text x="{148 + sc(b):.1f}" y="{y + 31}" font-size="14" fill="#1a1a1a">£{b:,.0f}m</text>')
    o.append(f'<text x="24" y="{y + 62}" font-size="14" fill="#5a5a5a">Sold to</text><rect x="140" y="{y + 46}" width="{sc(s):.1f}" height="24" fill="#a61c1c"/><text x="{148 + sc(s):.1f}" y="{y + 63}" font-size="14" fill="#1a1a1a">£{s:,.0f}m</text>')
    y += 105
o.append(f'<text x="24" y="{H - 12}" font-size="12" fill="#5a5a5a">Source: DAERA, NI Food and Drinks Processing Report 2022, Tables 11b and 16b (purchases are experimental statistics). robertjpark.co.uk</text></svg>')
open(os.path.join(OUT, 'bought-and-sold.svg'), 'w').write('\n'.join(o)); print('bought-and-sold.svg')
