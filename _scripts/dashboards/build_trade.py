"""Build the two static dashboards that go with "Friends with benefits" (16 November 2026):
the UK–EU sausage dashboard and the trade diversion dashboard.
Data: HMRC Overseas Trade Statistics, pulled from api.uktradeinfo.com on 16 November 2026,
saved as CSV in data/dashboards/uk-eu-trade/. Derived figures (shares, changes, ratios) are worked out here.
Reuses the helpers and styling of build.py.
Usage: python3 build_trade.py <repo_root>
"""
import sys, os, csv as _csv
ROOT = sys.argv[1]
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build.py'), encoding='utf-8').read()
exec(_src[:_src.index('D = {}')])

DATA = os.path.join(ROOT, 'data/dashboards/uk-eu-trade')
def rows(name): return list(_csv.DictReader(open(os.path.join(DATA, name), encoding='utf-8')))
def raw(name): return open(os.path.join(DATA, name), encoding='utf-8').read()
def data_href(name): return '/data/dashboards/uk-eu-trade/' + name

SRC.update({
 'ots': ('HMRC Overseas Trade Statistics (uktradeinfo), retrieved 16 November 2026', 'https://www.uktradeinfo.com/trade-data/'),
 'otsmeth': ('Overseas trade statistics: methodology and quality reports (HMRC, GOV.UK)', 'https://www.gov.uk/government/statistics/overseas-trade-statistics-methodologies'),
 'wf': ('The Windsor Framework (GOV.UK)', 'https://www.gov.uk/government/publications/the-windsor-framework'),
})

LINE_CSS = """
.k-line{width:100%;height:auto;display:block}
.k-line .ax{stroke:var(--cds-chart-axis,#bbb);stroke-width:1}
.k-line .gr{stroke:var(--cds-chart-grid,#eee);stroke-width:1}
.k-line text{font-size:14px;fill:var(--color-fg-muted,#5a5a5a)}
.k-line .ref{stroke:#888;stroke-dasharray:4 4}
.k-line circle{fill:transparent;stroke:none}
.k-line circle:hover{fill:currentColor}
.k-legend{display:flex;gap:16px;flex-wrap:wrap;font-size:13px;color:var(--color-fg-muted)}
.k-legend i{display:inline-block;width:14px;height:3px;margin-right:6px;vertical-align:middle}
"""
COLS = ['#A61C1C', '#1A1A1A']

def line(series, years, label, fmtv, refs=(), ymin=None):
    """series: [(name, [values aligned with years])]. Static SVG; each point has a <title> for hover and tap."""
    W, H, L, R, T, B = 720, 340, 56, 16, 16, 34
    vals = [v for _, s in series for v in s if v is not None]
    lo = 0 if ymin is None else ymin
    raw_hi = max(vals) * 1.05
    import math
    step = 10 ** math.floor(math.log10(raw_hi / 4)); step = next(m * step for m in (1, 2, 2.5, 5, 10) if m * step * 4 >= raw_hi - lo)
    hi = lo + step * 4
    x = lambda y: L + (y - years[0]) / (years[-1] - years[0]) * (W - L - R)
    yv = lambda v: H - B - (v - lo) / (hi - lo) * (H - T - B)
    out = [f'<svg class="k-line" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}"><title>{esc(label)}</title>']
    for i in range(5):
        g = lo + (hi - lo) * i / 4
        out.append(f'<line class="gr" x1="{L}" x2="{W-R}" y1="{yv(g):.1f}" y2="{yv(g):.1f}"/><text x="{L-6}" y="{yv(g)+4:.1f}" text-anchor="end">{esc(fmtv(g))}</text>')
    for y in years:
        if y % 5 == 0: out.append(f'<text x="{x(y):.1f}" y="{H-12}" text-anchor="middle">{y}</text>')
    out.append(f'<line class="ax" x1="{L}" x2="{W-R}" y1="{H-B}" y2="{H-B}"/>')
    for ry, rl in refs:
        out.append(f'<line class="ref" x1="{x(ry):.1f}" x2="{x(ry):.1f}" y1="{T}" y2="{H-B}"/><text x="{x(ry)+4:.1f}" y="{T+12}">{esc(rl)}</text>')
    for (name, s), c in zip(series, COLS):
        pts = ' '.join(f'{x(y):.1f},{yv(v):.1f}' for y, v in zip(years, s) if v is not None)
        out.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="2.5"/>')
        for y, v in zip(years, s):
            if v is None: continue
            out.append(f'<circle cx="{x(y):.1f}" cy="{yv(v):.1f}" r="7" style="color:{c}"><title>{esc(name)}, {y}{" (Jan–Sep)" if y == 2026 else ""}: {esc(fmtv(v))}</title></circle>')
    out.append('</svg>')
    leg = ''.join(f'<span><i style="background:{c}"></i>{esc(n)}</span>' for (n, _), c in zip(series, COLS)) if len(series) > 1 else ''
    return (f'<div class="k-legend">{leg}</div>' if leg else '') + ''.join(out)

def card2(title, note, body, src_keys, csvname=None, wide=True):
    c = card(title, note, body, src_keys, None, None, True)
    if csvname:
        c = c.replace('<p class="k-src">', f'<div class="k-actions"><a download href="{data_href(csvname)}">Download CSV</a></div><p class="k-src">', 1)
    return c

def finish(out, issue_date_note):
    out = out.replace('<style>' + K_CSS + EXTRA_CSS + '</style>', '<style>' + K_CSS + EXTRA_CSS + LINE_CSS + '</style>')
    out = out.replace('checked on 20–21 October 2026', 'retrieved from HMRC on 16 November 2026')
    out = out.replace('Figures checked on 21 October 2026, for publication with the issue of', issue_date_note)
    out = out.replace('<p class="k-foot">Commentary:', '<p class="k-foot">Read the article:')
    out = out.replace('every chart can be downloaded as CSV', 'every chart\'s data can be downloaded as CSV. Hover over or tap a point on a line for its value')
    return out

POST = '/blog/2026/11/friends-with-benefits/'
REFS = [(2016, 'Referendum'), (2021, 'Transition ends')]
pct = lambda v: f'{v:.1f}%'
chg = lambda a, b: f'{(b / a - 1) * 100:+.0f}%'.replace('-', '−')

# ---------------------------------------------------------------- sausage
sa = rows('sausage_annual.csv')
yrs = [int(r['year']) for r in sa]
get = lambda r, k: float(r[k])
by = {int(r['year']): r for r in sa}
b15, b25 = by[2015], by[2025]
x15, x25 = get(b15, 'eu_exports_gbp'), get(b25, 'eu_exports_gbp')
m15, m25 = get(b15, 'eu_imports_gbp'), get(b25, 'eu_imports_gbp')
t15, t25 = get(b15, 'eu_exports_tonnes'), get(b25, 'eu_exports_tonnes')
full = [r for r in sa if int(r['year']) <= 2025]
pk = max(full, key=lambda r: get(r, 'eu_exports_gbp'))
gbpm = lambda v: f'£{v:,.1f}m'

pp = rows('sausage_partner_year.csv')
ptab = {}
for r in pp:
    y = int(r['year'])
    if y not in (2015, 2025): continue
    o = ptab.setdefault(r['partner'], {'x2015': None, 'x2025': None, 'm2015': None, 'm2025': None})
    o[('x' if r['dir'] == 'X' else 'm') + str(y)] = float(r['value_gbp']) / 1e6
porder = sorted(ptab.items(), key=lambda kv: -((kv[1]['m2025'] or 0) + (kv[1]['x2025'] or 0)))
f1 = lambda v: '' if v is None else f'{v:,.1f}'
prow = [[k, f1(o['x2015']), f1(o['x2025']), f1(o['m2015']), f1(o['m2025'])] for k, o in porder]

ev = rows('sausage_events.csv')
import datetime
evrows = [[datetime.date.fromisoformat(r['date']).strftime('%-d %b %Y'), r['event'], r['detail']] for r in ev]

tiles = [tile('Exports to EU, 2025', gbpm(x25 / 1e6), f'{chg(x15, x25)} on 2015 (derived)'),
         tile('Imports from EU, 2025', gbpm(m25 / 1e6), f'{chg(m15, m25)} on 2015 (derived)'),
         tile('Imports per £1 of exports', f'£{m25 / x25:,.0f}', 'EU trade, 2025 (derived)'),
         tile('Tonnes exported to EU, 2025', f'{t25:,.0f}', f'{chg(t15, t25)} on 2015 (derived)'),
         tile('Peak year for EU exports', pk['year'], gbpm(get(pk, 'eu_exports_gbp') / 1e6))]
cards = [
 card2('UK sausage exports: EU and rest of world', '£ million a year. 2026 is January to September only, so the lines dip at the end. Exports outside the EU in 2018 and 2019 were lifted by sales to Qatar.',
       line([('To EU', [get(r, 'eu_exports_gbp') / 1e6 for r in sa]), ('To non-EU', [get(r, 'non_eu_exports_gbp') / 1e6 for r in sa])], yrs,
            'UK sausage exports to EU and non-EU countries, £ million, 2000 to 2026', lambda v: f'£{v:,.1f}m', REFS), ['ots'], 'sausage_annual.csv', wide=True),
 card2('UK sausage imports from the EU', '£ million a year. From January 2022 HMRC counts Great Britain\'s EU imports from customs declarations instead of the Intrastat survey; HMRC found a break of about 6% by value across all goods between 2021 and 2022. Part of the jump after 2021 may be down to that change.',
       line([('From EU', [get(r, 'eu_imports_gbp') / 1e6 for r in sa])], yrs, 'UK sausage imports from the EU, £ million, 2000 to 2026',
            lambda v: f'£{v:,.0f}m', [(2016, 'Referendum'), (2022, 'Method change')]), ['ots', 'otsmeth'], 'sausage_annual.csv'),
 card2('Exports to the EU by weight', 'Tonnes a year.', line([('Tonnes to EU', [get(r, 'eu_exports_tonnes') for r in sa])], yrs,
       'UK sausage exports to the EU in tonnes, 2000 to 2026', lambda v: f'{v:,.0f} t', REFS), ['ots'], 'sausage_annual.csv'),
 card2('Who buys and who sells: 2015 and 2025', '£ million. Top ten partners each way over 2010 to 2025; the rest are grouped as "Other". A blank means the country is outside that top ten.',
       table(['Country', 'UK exports 2015', 'UK exports 2025', 'UK imports 2015', 'UK imports 2025'], prow, num_cols=(1, 2, 3, 4)), ['ots'], 'sausage_partner_year.csv', wide=True),
 card2('What happened to the British sausage', 'Compiled by Robert J. Park from public records; not an official dataset. The 20 November 2026 entry is expected, not confirmed.',
       table(['Date', 'Event', 'What it meant'], evrows), ['wf'], 'sausage_events.csv', wide=True),
 card2('Notes on the data', 'Code 1601 covers all sausages: fresh, cooked, dried and cured, so it includes salami and chorizo as well as the fresh British banger. The EU ban since 2021 applies to chilled fresh sausages and other meat preparations from Great Britain, which are only part of this code. From 2021 Northern Ireland\'s trade with the EU is recorded differently from Great Britain\'s. Trade between Great Britain and Northern Ireland is not in these figures at all, so the "sausage war" over GB-to-NI supply does not show here. Values are in cash terms, not adjusted for inflation.', '', ['ots', 'otsmeth'], None, wide=True),
]
slug = 'uk-eu-sausage-trade'
out = page(slug, 'The sausage dashboard: UK–EU sausage trade, 2000 to 2026 | Robert J. Park', 'The sausage dashboard',
           f'UK trade in sausages and similar products (commodity code 1601), by value and weight, 2000 to September 2026. In 2025 the UK sold <b>{gbpm(x25 / 1e6)}</b> of sausages to the EU and bought <b>{gbpm(m25 / 1e6)}</b> from it: about <b>£{m25 / x25:,.0f}</b> of imports for every £1 of exports. Source: HMRC. Not adjusted for inflation.',
           tiles, cards, POST, 'Friends with benefits', '16 November 2026',
           'Dashboard of UK sausage trade with the EU and the rest of the world, 2000 to 2026, from HMRC trade statistics: values, tonnes, partner countries and the post-Brexit timeline. By Robert J. Park.')
out = finish(out, 'Figures as at 16 November 2026, published with the article of')
open(os.path.join(ROOT, 'tools/dashboards', slug + '.html'), 'w', encoding='utf-8').write(out)
print(slug, len(out))

# ---------------------------------------------------------------- trade diversion
ta = rows('trade_annual.csv')
tyrs = [int(r['year']) for r in ta]
def share(r, a, b): return 100 * float(r[a]) / (float(r[a]) + float(r[b]))
sh = {int(r['year']): {
    'x': share(r, 'goods_eu_exports_gbp_m', 'goods_non_eu_exports_gbp_m'), 'm': share(r, 'goods_eu_imports_gbp_m', 'goods_non_eu_imports_gbp_m'),
    'fx': share(r, 'food_eu_exports_gbp_m', 'food_non_eu_exports_gbp_m'), 'fm': share(r, 'food_eu_imports_gbp_m', 'food_non_eu_imports_gbp_m')} for r in ta}
open(os.path.join(DATA, 'eu_share_by_year.csv'), 'w', encoding='utf-8', newline='').write(
    'year,eu_share_goods_exports_pct,eu_share_goods_imports_pct,eu_share_food_exports_pct,eu_share_food_imports_pct,period\n' +
    ''.join(f"{y},{s['x']:.2f},{s['m']:.2f},{s['fx']:.2f},{s['fm']:.2f},{r['period']}\n" for (y, s), r in zip(sh.items(), ta)))
ppt = lambda a, b: f'{b - a:+.1f} points on 2015 (derived)'.replace('-', '−')
gp = rows('goods_partner_year.csv')
gt = {}
for r in gp:
    y = int(r['year'])
    if y not in (2015, 2025): continue
    o = gt.setdefault(r['partner'], {'x2015': None, 'x2025': None, 'm2015': None, 'm2025': None})
    o[('x' if r['dir'] == 'X' else 'm') + str(y)] = float(r['value_gbp_m']) / 1000
c0 = lambda a, b: '' if not a or not b else f'{(b / a - 1) * 100:+.0f}%'.replace('-', '−')
gorder = sorted(gt.items(), key=lambda kv: -((kv[1]['x2025'] or 0) + (kv[1]['m2025'] or 0)))
grow = [[k, f1(o['x2015']), f1(o['x2025']), c0(o['x2015'], o['x2025']), f1(o['m2015']), f1(o['m2025']), c0(o['m2015'], o['m2025'])] for k, o in gorder]
s00, s15, s25 = sh[2000], sh[2015], sh[2025]
tiles = [tile('EU share of goods exports, 2025', pct(s25['x']), ppt(s15['x'], s25['x'])),
         tile('EU share of goods imports, 2025', pct(s25['m']), ppt(s15['m'], s25['m'])),
         tile('EU share of food exports, 2025', pct(s25['fx']), ppt(s15['fx'], s25['fx'])),
         tile('EU share of food imports, 2025', pct(s25['fm']), ppt(s15['fm'], s25['fm']))]
gb = lambda v: f'£{v:,.0f}bn'
cards = [
 card2('EU share of UK goods trade', 'Per cent of the value of all UK goods exports and imports. Shares are not affected by 2026 being a part year.',
       line([('Exports to EU', [sh[y]['x'] for y in tyrs]), ('Imports from EU', [sh[y]['m'] for y in tyrs])], tyrs,
            'EU share of UK goods exports and imports, per cent, 2000 to 2026', lambda v: f'{v:.0f}%', REFS), ['ots'], 'eu_share_by_year.csv'),
 card2('EU share of UK food and drink trade', 'Per cent. Food and drink means commodity chapters 01 to 24, which also takes in live animals, animal feed and tobacco.',
       line([('Exports to EU', [sh[y]['fx'] for y in tyrs]), ('Imports from EU', [sh[y]['fm'] for y in tyrs])], tyrs,
            'EU share of UK food and drink exports and imports, per cent, 2000 to 2026', lambda v: f'{v:.0f}%', REFS), ['ots'], 'eu_share_by_year.csv'),
 card2('UK goods exports: EU and rest of world', '£ billion a year. 2026 is January to September only, so the lines dip at the end.',
       line([('To EU', [float(r['goods_eu_exports_gbp_m']) / 1000 for r in ta]), ('To non-EU', [float(r['goods_non_eu_exports_gbp_m']) / 1000 for r in ta])], tyrs,
            'UK goods exports to EU and non-EU countries, £ billion, 2000 to 2026', gb, REFS), ['ots'], 'trade_annual.csv'),
 card2('UK goods imports: EU and rest of world', '£ billion a year. 2026 is January to September only.',
       line([('From EU', [float(r['goods_eu_imports_gbp_m']) / 1000 for r in ta]), ('From non-EU', [float(r['goods_non_eu_imports_gbp_m']) / 1000 for r in ta])], tyrs,
            'UK goods imports from EU and non-EU countries, £ billion, 2000 to 2026', gb, REFS), ['ots'], 'trade_annual.csv'),
 card2('Largest partners: 2015 and 2025', '£ billion, with the change in cash terms. Top twelve partners each way over 2010 to 2025. A blank means the country is outside that top twelve.',
       table(['Country', 'UK exports 2015', 'UK exports 2025', 'Change', 'UK imports 2015', 'UK imports 2025', 'Change'], grow, num_cols=(1, 2, 3, 4, 5, 6)), ['ots'], 'goods_partner_year.csv', wide=True),
 card2('What this can and cannot show', 'The EU\'s share of UK exports was already falling before 2016, as faster-growing markets took more. So the change since 2015 mixes a long-run trend with the effect of new barriers from 2021, the pandemic and the 2022 energy price spike. These totals include gold and other erratic items, which swing the non-EU figures (trade with Switzerland is mostly gold). The EU is counted with its membership at the time. Two changes of method break the series: from January 2021 HMRC counts Great Britain\'s exports to the EU from customs declarations instead of the Intrastat survey, and from January 2022 it does the same for Great Britain\'s imports from the EU; Northern Ireland\'s EU trade is still collected by Intrastat. HMRC found a break of about 6% by value in EU imports between 2021 and 2022. Goods only: services are not included. Values are in cash terms, not adjusted for inflation.', '', ['ots', 'otsmeth'], None, wide=True),
]
slug = 'uk-trade-diversion'
out = page(slug, 'Trade diversion dashboard: the EU\'s share of UK trade, 2000 to 2026 | Robert J. Park', 'Trade diversion dashboard',
           f'Trade diversion means trade shifting from one partner to another because barriers changed, not because price or quality did. The EU took <b>{pct(s25["x"])}</b> of UK goods exports in 2025, against <b>{pct(s15["x"])}</b> in 2015 and <b>{pct(s00["x"])}</b> in 2000. It supplied <b>{pct(s25["m"])}</b> of UK goods imports in 2025, against <b>{pct(s15["m"])}</b> in 2015. Source: HMRC. A falling share on its own does not prove diversion: see the notes.',
           tiles, cards, POST, 'Friends with benefits', '16 November 2026',
           'Dashboard of the EU\'s share of UK goods and food trade, 2000 to 2026, with exports and imports by partner, from HMRC trade statistics. By Robert J. Park.')
out = finish(out, 'Figures as at 16 November 2026, published with the article of')
open(os.path.join(ROOT, 'tools/dashboards', slug + '.html'), 'w', encoding='utf-8').write(out)
print(slug, len(out))
print('check', round(s00['x'], 1), round(s15['x'], 1), round(s25['x'], 1), round(s15['fx'], 1), round(s25['fx'], 1), round(s15['fm'], 1), round(s25['fm'], 1), round(m25 / x25), round((t25 / t15 - 1) * 100))
