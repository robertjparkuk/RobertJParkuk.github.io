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

# Household recycling rate by council, 2024/25. PROVISIONAL: transcribed from a secondary copy of DAERA's
# 2024/25 table; replace from the DAERA time series CSV (lacts) before go-live.
COUNCILS = [
 ('Mid Ulster', 59.3), ('Antrim and Newtownabbey', 56.9), ('Ards and North Down', 56.1),
 ('Armagh City, Banbridge and Craigavon', 54.6), ('Mid and East Antrim', 50.8),
 ('Causeway Coast and Glens', 50.4), ('Lisburn and Castlereagh', 50.4), ('Newry, Mourne and Down', 48.7),
 ('Derry City and Strabane', 48.4), ('Fermanagh and Omagh', 47.7), ('Belfast', 42.4)]
NI_HH = 51.0
# NI household recycling rate by quarter (DAERA quarterly releases, provisional at release)
QUARTERS = [('Apr–Jun 2024', 54.5), ('Jul–Sep 2024', 53.7), ('Oct–Dec 2024', 48.2), ('Jan–Mar 2025', 46.4),
            ('Apr–Jun 2025', 54.0), ('Oct–Dec 2025', 49.8)]
# Where council-collected waste went (DAERA)
LANDFILL = [('2006/07', 74.0), ('2023/24', 18.4), ('2024/25', 14.0)]
SPLIT = [('Jan–Mar 2025', 46.0, 44.3, 8.3), ('Jul–Sep 2025', None, 41.8, 3.4)]

hi = ['Mid and East Antrim']  # Robert's home council (Larne)
tiles = [
 tile('NI household recycling rate, 2024/25', '51.0%', 'Flat on 2023/24 (51.1%). DAERA, 11 Dec 2025'),
 tile('Council waste to landfill, 2024/25', '14.0%', 'Down from 74.0% in 2006/07 and 18.4% in 2023/24', 'k-ok' if False else ''),
 tile('Spread between councils', '42.4–59.3%', 'Belfast to Mid Ulster, household recycling, 2024/25 (provisional)'),
 tile('Sent for energy recovery', '41.8%', 'Jul–Sep 2025, up from 30.2% a year earlier'),
]
rows = [(c, v, f'{v:.1f}%') for c, v in COUNCILS]
cards = [
 card('Household recycling rate by council, 2024/25',
      f'NI average {NI_HH:.1f}%. Mid and East Antrim is highlighted. <span class="k-pill">Provisional: to be replaced from the DAERA CSV before publication</span>',
      bars(rows, hi=hi, maxv=70), ['lac25', 'lacts'],
      csv_href(['council', 'household_recycling_rate_2024_25_pct'], [list(r) for r in COUNCILS]), 'ni-council-household-recycling-2024-25', wide=True),
 card('NI household recycling rate by quarter',
      'Provisional quarterly figures as first published.',
      bars([(q, v, f'{v:.1f}%') for q, v in QUARTERS], maxv=70), ['lacq'],
      csv_href(['quarter', 'household_recycling_rate_pct'], [list(r) for r in QUARTERS]), 'ni-household-recycling-by-quarter'),
 card('Landfill rate, council-collected waste',
      'The fall since 2006/07 is the biggest change in NI waste. Most of the recent drop has gone to energy recovery, not recycling.',
      bars([(y, v, f'{v:.1f}%') for y, v in LANDFILL], maxv=80), ['lac25'],
      csv_href(['year', 'landfill_rate_pct'], [list(r) for r in LANDFILL]), 'ni-lac-landfill-rate'),
 card('Recycling, energy recovery and landfill',
      'Share of council-collected waste, by route. Recycling held steady while energy recovery replaced landfill.',
      table(['Quarter', 'Recycled', 'Energy recovery', 'Landfill'],
            [(q, '—' if r is None else f'{r:.1f}%', f'{e:.1f}%', f'{l:.1f}%') for q, r, e, l in SPLIT], num_cols=(1, 2, 3)),
      ['lacq'], csv_href(['quarter', 'recycled_pct', 'energy_recovery_pct', 'landfill_pct'], [list(r) for r in SPLIT]), 'ni-lac-routes'),
 card('What this means for a business',
      'Councils are paid from packaging EPR for household packaging, and a deposit return scheme for drinks containers is due in October 2027. '
      'If you make or import packaged goods, your packaging data now drives both your fees and your council\'s income. '
      'If you run a site, the same separation-at-source habits that lift a council\'s rate cut your own waste bill.',
      '<p class="k-note"><a href="/services/#land-water-and-waste">Land, water and waste services</a> · <a href="/contact/">Talk to me</a></p>', ['lac25'], wide=True),
]
out = page('ni-council-waste', 'NI councils compared: waste and recycling | Robert J. Park',
           "Northern Ireland's eleven councils compared: waste and recycling",
           'How much household waste each council recycles, where the rest goes, and how that has changed. Built from DAERA\'s official statistics. <strong>Draft for review: not yet published.</strong>',
           tiles, cards, '/blog/2026/11/northern-irelands-waste-bill/', 'Northern Ireland\'s waste bill', '23 November 2026',
           'Household recycling, landfill and energy recovery for Northern Ireland\'s eleven councils, from DAERA official statistics.')
out = out.replace('checked on 20–21 October 2026', 'checked on 22–23 November 2026')
out = out.replace('Figures checked on 21 October 2026, for publication with the issue of 23 November 2026', 'Figures checked on 23 November 2026. Draft: council rates are provisional until replaced from the DAERA CSV')
out = out.replace('</style>\n</head>', '.k-tiles{grid-template-columns:repeat(auto-fit,minmax(min(100%,14rem),1fr))}</style>\n</head>')
out = out.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"')
open(os.path.join(ROOT, 'tools/dashboards/ni-council-waste.html'), 'w', encoding='utf-8').write(out)
print('ok', len(out))
