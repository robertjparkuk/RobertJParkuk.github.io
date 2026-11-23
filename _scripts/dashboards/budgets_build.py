"""Build the NI carbon budgets tracker (balancing plan item 29), in the house dashboard style.
Usage: python3 budgets_build.py <repo_root>
"""
import sys, os
ROOT = sys.argv[1]
src = open(os.path.join(ROOT, '_scripts/dashboards/build.py'), encoding='utf-8').read()
exec(src[:src.index('\nD = {}')])  # helpers, SRC, SECTORS, sector cards, page(), brand CSS

SRC.update({
 'cca': ('Climate Change Act (Northern Ireland) 2022 (legislation.gov.uk)', 'https://www.legislation.gov.uk/nia/2022/31/part/2'),
 'cb': ('Consultation on NI\'s fourth carbon budget, with the first three budgets and the 2040 target listed (DAERA)', 'https://www.daera-ni.gov.uk/consultations/consultation-setting-northern-irelands-fourth-carbon-budget-2038-2042'),
 'cb4': ('Summary of responses: NI fourth carbon budget (DAERA, 13 February 2026)', 'https://www.daera-ni.gov.uk/publications/summary-responses-consultation-setting-northern-irelands-fourth-carbon-budget-2038-2042'),
 'ccc4': ('Northern Ireland\'s Fourth Carbon Budget (Climate Change Committee, 19 March 2025)', 'https://www.theccc.org.uk/publication/northern-irelands-fourth-carbon-budget/'),
 'ghgla': ('NI local authority greenhouse gas emissions estimates 2005–2024 (DAERA)', 'https://www.daera-ni.gov.uk/publications/northern-ireland-local-authority-greenhouse-gas-emissions-estimates-2005-2024-statistical-bulletin'),
 'arms': ('Progress on implementing the Climate Change Act (NI Assembly Research and Information Service, 16 March 2026)', 'https://www.assemblyresearchmatters.org/2026/03/16/progress-on-implementing-the-climate-change-act/'),
})

NET_2024 = 18.4                      # DAERA, net MtCO2e, 2024
CUT_2024 = 29.4                      # % below base year (DAERA)
BASE = round(NET_2024 / (1 - CUT_2024 / 100), 1)   # derived base-year emissions
LEVELS = [  # label, % reduction on 1990 baseline (average annual over the period), status
 ('First budget, 2023–27', 33, 'In law (SR 2024/215)'),
 ('Second budget, 2028–32', 48, 'In law (SR 2024/215)'),
 ('Third budget, 2033–37', 62, 'In law (SR 2024/215)'),
 ('2040 target', 77, 'In law (SR 2024/214)'),
 ('Fourth budget, 2038–42', 77, 'Proposed; not yet set'),
 ('2050', 100, 'Net zero (the Act)'),
]
ladder = [('Base year (derived)', BASE, f'{BASE:.1f} Mt'), ('2024 actual', NET_2024, f'{NET_2024:.1f} Mt · −{CUT_2024:.1f}%')]
for lab, pct, st in LEVELS:
    v = round(BASE * (1 - pct / 100), 1)
    ladder.append((lab, v, f'{v:.1f} Mt · −{pct}%'))
first = round(BASE * 0.67, 1)
gap = round(NET_2024 - first, 1)

tiles = [
 tile('NI net emissions, 2024', f'{NET_2024:.1f} Mt', 'MtCO2e. DAERA inventory, published 9 June 2026'),
 tile('Below the base year', f'{CUT_2024:.1f}%', 'Base year is 1990 for most gases'),
 tile('First budget, 2023–27', '33%', f'Average annual cut needed. About {first:.1f} Mt a year (derived)'),
 tile('Gap in 2024', f'{gap:.1f} Mt', 'Above the first budget\'s yearly average (derived)', 'k-bad'),
]
H = ['2024 actual']
cards = [
 card('The budget ladder', f'Each budget is an average annual cut on the 1990 baseline. Levels in MtCO2e are derived from DAERA\'s 2024 figure and its {CUT_2024:.1f}% fall, which gives a base year of about {BASE:.1f} Mt. The legal test is the net emissions account averaged over each five-year period, so read this as an indication, not a compliance verdict.',
      bars(ladder, hi=H, maxv=28), ['ghg', 'cb', 'cca'],
      csv_href(['level', 'mtco2e', 'label'], [list(r) for r in ladder]), 'ni-carbon-budget-ladder', wide=True),
 sector_card(['Agriculture']),
 change_card(['Agriculture']),
 card('What is in law, and what is missing', 'Dated status of the duties under the Climate Change Act (Northern Ireland) 2022, as at 23 November 2026.',
      table(['Item', 'Due', 'Status'], [
        ('First three carbon budgets, 2023–37', 'by 2023 (Act)', 'Set: Assembly approved December 2024'),
        ('2040 emissions target (77%)', 'with the budgets', 'Set: SR 2024/214'),
        ('Fourth carbon budget, 2038–42', '12 years before 2038 (s.23)', 'Consulted Jul–Nov 2025 at 77%; responses published 13 Feb 2026; regulations not found'),
        ('Reporting duties on public bodies', '—', 'Made: 40 bodies, SR 2024/93'),
        ('Just Transition Commission', '—', 'Regulations in operation 29 April 2026'),
      ]), ['cca', 'cb4', 'ccc4', 'arms'], wide=True),
 card('Per council', 'DAERA publishes territorial estimates for each of the eleven councils, 2005 to 2024. Councils with more agriculture have generally seen smaller falls. A council panel will be added from DAERA\'s tables.',
      '<p class="k-note"><a href="/services/#councils-public-bodies-and-trade-bodies">Council carbon baselines and climate plans</a> · <a href="/contact/">Talk to me</a></p>', ['ghgla']),
 card('What this means for a business', 'The Act puts no direct duty on private firms. It reaches them through what government does to close the gap: sector plans for agriculture, transport, buildings and industry, public procurement, grants and regulation. Knowing your own baseline is the first step.',
      '<p class="k-note"><a href="/tools/carbon-ready-reckoner.html">Carbon Ready Reckoner</a> · <a href="/services/#carbon-inventories">Carbon inventories</a></p>', ['cca']),
]
out = page('ni-carbon-budgets', 'NI emissions against its carbon budgets | Robert J. Park',
           "Northern Ireland's emissions against its carbon budgets",
           'Where Northern Ireland\'s emissions stand against the carbon budgets and targets set under the Climate Change Act (Northern Ireland) 2022, which sectors carry the gap, and which duties are still missing.',
           tiles, cards, '/blog/2026/11/the-act-that-outran-its-plan/', 'The Act that outran its plan', '23 November 2026',
           'Northern Ireland\'s greenhouse gas emissions against its legal carbon budgets, by sector, with the dated status of each duty under the Climate Change Act (NI) 2022.')
out = out.replace('The highlighted sector is the one this dashboard covers.', 'Agriculture, highlighted, is the largest source and has risen since the base year.')
out = out.replace('checked on 20–21 October 2026', 'checked on 23 November 2026')
out = out.replace('Figures checked on 21 October 2026, for publication with the issue of 23 November 2026', 'Figures checked on 23 November 2026')
out = out.replace('</style>\n</head>', '.k-tiles{grid-template-columns:repeat(auto-fit,minmax(min(100%,14rem),1fr))}.k-big.k-bad{color:var(--color-bad)}</style>\n</head>')
open(os.path.join(ROOT, 'tools/dashboards/ni-carbon-budgets.html'), 'w', encoding='utf-8').write(out)
print('ok', BASE, first, gap)
