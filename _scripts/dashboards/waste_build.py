"""Build the NI council waste comparator (balancing plan item 17).
Reuses the helpers and brand styling of build.py. Draft: not linked from /dashboards/ until Robert approves.
Usage: python3 waste_build.py <repo_root>
"""
import sys, os
ROOT = sys.argv[1]
src = open(os.path.join(ROOT, '_scripts/dashboards/build.py'), encoding='utf-8').read()
exec(src[:src.index('\nD = {}')])  # helpers, SRC, page(), brand CSS

SRC.update({
 'lac25': ('NI LAC municipal waste management statistics 2024/25, annual report (DAERA, 11 December 2025)', 'https://www.daera-ni.gov.uk/news/northern-ireland-local-authority-collected-municipal-waste-management-statistics-released-111225'),
 'lacq': ('NI LAC municipal waste management statistics, quarterly releases (DAERA, 2024–2026)', 'https://www.daera-ni.gov.uk/news/northern-ireland-local-authority-collected-municipal-waste-management-statistics-released-april-26'),
 'lacts': ('LAC municipal waste time series, CSV, Open Government Licence (DAERA via OpenDataNI)', 'https://www.daera-ni.gov.uk/publications/northern-ireland-local-authority-collected-municipal-waste-management-statistics-time-series-data'),
})

# All figures computed from DAERA's LAC municipal waste time series (OpenDataNI, Open Government Licence),
# saved in data/dashboards/ni-council-waste/. Annual rate = sum of four quarters' tonnes / sum of arisings.
import pandas as pd
CSV = os.path.join(ROOT, 'data/dashboards/ni-council-waste/lac-municipal-waste-timeseries.csv')
df = pd.read_csv(CSV, encoding='latin-1')
num = lambda s: pd.to_numeric(s.astype(str).str.replace(',', ''), errors='coerce')
C = {'hh': 'Household waste arisings (tonnes)', 'hhr': 'Household waste preparing for reuse, dry recycling and composting (tonnes)',
     'lac': 'Local authority collected municipal waste arisings (tonnes), KPI(j)',
     'lacr': 'Local authority collected municipal waste preparing for reuse, dry recycling and composting (tonnes)',
     'er': 'Local authority collected municipal waste energy recovery for mixed residual (tonnes)',
     'er2': 'Local authority collected municipal waste energy recovery for specific streams e.g. wood (tonnes)',
     'lf': 'Local authority collected municipal waste landfilled (tonnes)'}
for k, c in C.items(): df[k] = num(df[c])
df['hhr'] = df['hhr'].fillna(num(df['Household waste dry recycling and composting (tonnes)']))
df['lacr'] = df['lacr'].fillna(num(df['Local authority collected municipal waste dry recycling and composting (tonnes)']))
status = df.groupby('FinancialYear')['DataStatus'].agg(lambda s: 'Finalised' if (s == 'Finalised').all() else 'Provisional')
nq = df.groupby('FinancialYear')['QuarterCode'].nunique()
g = df.groupby(['FinancialYear', 'AreaName'])[list(C)].sum(min_count=1)
g['hh_rate'] = g.hhr / g.hh * 100
g['lac_rate'] = g.lacr / g.lac * 100
g['er_rate'] = (g.er.fillna(0) + g.er2.fillna(0)) / g.lac * 100
g['lf_rate'] = g.lf / g.lac * 100
LATEST = max(y for y in status.index if status[y] == 'Finalised')
PREV = sorted(status.index)[sorted(status.index).index(LATEST) - 1]
FULL_PROV = [y for y in status.index if status[y] == 'Provisional' and nq[y] == 4]
NAMES = {n: n.replace(' & ', ' and ') for n in g.loc[LATEST].index}
cur = g.loc[LATEST].drop('Northern Ireland'); prev = g.loc[PREV]
COUNCILS = sorted(((NAMES[n], round(r, 1)) for n, r in cur.hh_rate.items()), key=lambda x: -x[1])
NI_HH = round(g.loc[(LATEST, 'Northern Ireland'), 'hh_rate'], 1)
ni = g.xs('Northern Ireland', level='AreaName')
YEARS = [y for y in sorted(ni.index) if nq[y] == 4]
TREND = [(y + (' (provisional)' if status[y] == 'Provisional' else ''), round(ni.loc[y, 'hh_rate'], 1)) for y in YEARS]
ROUTES = [(y + (' (provisional)' if status[y] == 'Provisional' else ''), round(ni.loc[y, 'lac_rate'], 1), round(ni.loc[y, 'er_rate'], 1), round(ni.loc[y, 'lf_rate'], 1)) for y in YEARS]
COUNCIL_ROUTES = sorted(((NAMES[n], round(r.lac_rate, 1), round(r.er_rate, 1), round(r.lf_rate, 1)) for n, r in cur.iterrows()), key=lambda x: x[3])
CHANGE = sorted(((NAMES[n], round(cur.loc[n, 'hh_rate'] - prev.loc[n, 'hh_rate'], 1)) for n in cur.index), key=lambda x: -x[1])
FIRST = YEARS[0]
hi = ['Mid and East Antrim']  # Robert's home council (Larne)
lo, hi_ = COUNCILS[-1], COUNCILS[0]
ni_l = ni.loc[LATEST]; ni_p = ni.loc[PREV]
tiles = [
 tile(f'NI household recycling rate, {LATEST}', f'{NI_HH:.1f}%', f'{PREV}: {ni_p.hh_rate:.1f}%. Finalised DAERA figures'),
 tile(f'Council waste to landfill, {LATEST}', f'{ni_l.lf_rate:.1f}%', f'Down from {ni.loc[FIRST].lf_rate:.1f}% in {FIRST}'),
 tile(f'Sent for energy recovery, {LATEST}', f'{ni_l.er_rate:.1f}%', f'Up from {ni_p.er_rate:.1f}% in {PREV}'),
 tile('Spread between councils', f'{lo[1]:.1f}–{hi_[1]:.1f}%', f'{lo[0]} to {hi_[0]}, household recycling, {LATEST}'),
]
if FULL_PROV:
    y = FULL_PROV[-1]
    tiles[0] = tile(f'NI household recycling rate, {LATEST}', f'{NI_HH:.1f}%', f'{PREV}: {ni_p.hh_rate:.1f}%. {y} provisional: {ni.loc[y].hh_rate:.1f}%')
H = ['Mid and East Antrim']
cards = [
 card(f'Household recycling rate by council, {LATEST}',
      f'Preparing for reuse, dry recycling and composting as a share of household waste. NI rate {NI_HH:.1f}%. Mid and East Antrim is highlighted.',
      bars([(c, v, f'{v:.1f}%') for c, v in COUNCILS], hi=H, maxv=70), ['lacts', 'lac25'],
      csv_href(['council', f'household_recycling_rate_{LATEST.replace("/", "_")}_pct'], [list(r) for r in COUNCILS]), 'ni-council-household-recycling', wide=True),
 card(f'Change since {PREV}', f'Percentage points, household recycling rate, {PREV} to {LATEST}. Green is a rise.',
      divbars(CHANGE, unit=' pts', hi=H, good_when_negative=False), ['lacts'],
      csv_href(['council', 'change_pct_points'], [list(r) for r in CHANGE]), 'ni-council-recycling-change'),
 card(f'Where each council\'s waste went, {LATEST}',
      'All council-collected waste, by route, sorted by landfill rate. Councils that still landfill a third of their waste sit alongside councils that landfill almost none.',
      table(['Council', 'Recycled', 'Energy recovery', 'Landfill'], [(c, f'{r:.1f}%', f'{e:.1f}%', f'{l:.1f}%') for c, r, e, l in COUNCIL_ROUTES], num_cols=(1, 2, 3)),
      ['lacts'], csv_href(['council', 'recycled_pct', 'energy_recovery_pct', 'landfill_pct'], [list(r) for r in COUNCIL_ROUTES]), 'ni-council-waste-routes'),
 card(f'NI household recycling rate, {FIRST} onwards',
      f'Whole financial years. The rate rose from {TREND[0][1]:.1f}% in {FIRST} to about half by 2018/19, and has stayed at around half since.',
      bars([(y, v, f'{v:.1f}%') for y, v in TREND], maxv=70), ['lacts'],
      csv_href(['financial_year', 'household_recycling_rate_pct'], [list(r) for r in TREND]), 'ni-household-recycling-trend', wide=True),
 card('Landfill replaced by energy recovery, not recycling',
      'All council-collected waste in NI, by route and year.',
      table(['Year', 'Recycled', 'Energy recovery', 'Landfill'], [(y, f'{r:.1f}%', f'{e:.1f}%', f'{l:.1f}%') for y, r, e, l in ROUTES], num_cols=(1, 2, 3)),
      ['lacts'], csv_href(['financial_year', 'recycled_pct', 'energy_recovery_pct', 'landfill_pct'], [list(r) for r in ROUTES]), 'ni-lac-routes-by-year', wide=True),
 card('What this means for a business',
      'Councils are paid from packaging EPR for household packaging, and a deposit return scheme for drinks containers is due in October 2027. '
      'If you make or import packaged goods, your packaging data now drives both your fees and your council\'s income. '
      'If you run a site, the same separation-at-source habits that lift a council\'s rate cut your own waste bill.',
      '<p class="k-note"><a href="/services/#land-water-and-waste">Land, water and waste services</a> · <a href="/contact/">Talk to me</a></p>', ['lac25'], wide=True),
]
out = page('ni-council-waste', 'NI councils compared: waste and recycling | Robert J. Park',
           "Northern Ireland's eleven councils compared: waste and recycling",
           f'How much household waste each council recycles, where the rest goes, and how that has changed since {FIRST}. Calculated from DAERA\'s official time series ({LATEST} finalised). <strong>Draft for review: not yet published.</strong>',
           tiles, cards, '/blog/2026/11/northern-irelands-waste-bill/', 'Northern Ireland\'s waste bill', '23 November 2026',
           'Household recycling, landfill and energy recovery for Northern Ireland\'s eleven councils, from DAERA official statistics.')
out = out.replace('checked on 20–21 October 2026', 'checked on 22–23 November 2026')
out = out.replace('Figures checked on 21 October 2026, for publication with the issue of 23 November 2026', 'Figures calculated on 23 November 2026 from DAERA\'s LAC municipal waste time series (Open Government Licence)')
out = out.replace('</style>\n</head>', '.k-tiles{grid-template-columns:repeat(auto-fit,minmax(min(100%,14rem),1fr))}</style>\n</head>')
out = out.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"')
open(os.path.join(ROOT, 'tools/dashboards/ni-council-waste.html'), 'w', encoding='utf-8').write(out)
print('ok', len(out))
