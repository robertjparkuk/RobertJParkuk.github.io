"""Build the dashboards that accompany two thought pieces (2 Nov 2026):
NI Screen, and the public realm / drains and floods piece.
Reuses the helpers and styling of build.py. Every figure is taken from the sources
cited in the posts; derived figures are labelled.
Usage: python3 build_thought.py <repo_root>
"""
import sys, os, re
ROOT = sys.argv[1]
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build.py'), encoding='utf-8').read()
exec(_src[:_src.index('D = {}')])

SRC.update({
 'scr_ec': ('Committee for the Economy response on the 2026–27 budget (NI Assembly, 17 April 2026)', 'https://www.niassembly.gov.uk/globalassets/documents/committees/2022-2027/finance/reports/2025-26-draft-executive-budget/written-submissions/20260417-economy-committee-response---2026-27-budget.pdf'),
 'scr_be': ('Northern Ireland Screen delivers £477 million for local economy (Business Eye)', 'https://www.businesseye.co.uk/news/northern-ireland-screen-delivers-477-million-for-local-economy/'),
 'scr_in': ('NI-made cinema and TV blockbusters bring in nearly £500m (Irish News, April 2026)', 'https://www.irishnews.com/news/business/northern-ireland-made-cinema-and-tv-blockbusters-rake-in-nearly-500m-SQXEMHCCFFFJJJHSEMTMS4QGMQ/'),
 'scr_bfi': ('Official BFI statistics for 2025 (BFI, 5 February 2026)', 'https://www.bfi.org.uk/news/official-bfi-statistics-2025'),
 'scr_481': ('Revenue eBrief 068/26 on the Section 481 film relief (Revenue, 30 March 2026)', 'https://www.revenue.ie/en/tax-professionals/ebrief/2026/no-0682026.aspx'),
 'scr_it': ("Why now is a really important moment for Ireland's screen industry (Irish Times, 14 October 2026)", 'https://www.irishtimes.com/special-reports/2026/10/14/why-now-is-a-really-important-moment-for-irelands-screen-industry/'),
 'scr_sim': ('Ireland funds cross-border production (Screen Global Production, 12 December 2025)', 'https://www.screenglobalproduction.com/news/2025/12/12/ireland-fund-production-cross-border'),
 'scr_sus': ('Northern Ireland Screen launches Sustainability Support scheme (Business Eye, January 2025)', 'https://www.businesseye.co.uk/news/northern-ireland-screen-launches-sustainability-support-scheme/'),
 'scr_su1': ('Studio Ulster virtual production facility opens (Screen Global Production, 20 June 2025)', 'https://www.screenglobalproduction.com/news/2025/06/20/studio-ulster-virtual-production-wall-belfast-opens'),
 'scr_su2': ('Studio Ulster to expand in response to demand (Irish News, March 2026)', 'https://www.irishnews.com/news/business/studio-ulster-belfasts-new-72m-virtual-production-facility-to-expand-in-response-to-growing-demand-2GJU6IQZ3BE73O2AE3FPZPOLLY/'),
 'scr_gam': ('Games Development Call, summer 2026 (nibusinessinfo)', 'https://www.nibusinessinfo.co.uk/content/games-development-call-summer-2026'),
 'scr_bl': ('Blue Lights boosted the NI economy by £20m (Advanced Television, 15 November 2024)', 'https://www.advanced-television.com/2024/11/15/report-blue-lights-boosted-northern-ireland-economy-by-20m/'),
 'scr_bp': ('Northern Ireland Screen Business Plan 2024/25 (via NIOPA)', 'https://niopa.qub.ac.uk/bitstream/NIOPA/16352/20/Business-Plan-24-25.pdf'),
 'scr_lang': ('Irish Language and Ulster-Scots Broadcast Funds, written answer HL3344 (23 December 2024)', 'https://parallelparliament.co.uk/question/HL3344/irish-language-broadcast-fund-and-ulster-scots-b'),
 'pr_niao_w': ('Funding water infrastructure in Northern Ireland (NI Audit Office, 28 March 2024)', 'https://www.niauditoffice.gov.uk/files/niauditoffice/documents/2024-03/NI%20Audit%20Office%20Media%20Release%20-%20Funding%20water%20infrastructure%20in%20NI.pdf'),
 'pr_cap': ('Capacity information (NI Water)', 'https://www.niwater.com/capacity-information'),
 'pr_so': ('Storm overflows (NI Water)', 'https://niwater.com/storm/overflow'),
 'pr_wm': ("Stormont urged to unblock Northern Ireland's wastewater crisis (Water Magazine, 18 June 2026)", 'https://www.watermagazine.co.uk/2026/06/18/stormont-urged-to-unblock-northern-irelands-wastewater-crisis/'),
 'pr_ur': ('Utility Regulator price control decision (August 2026)', 'https://www.uregni.gov.uk/node/8589'),
 'pr_niao_f': ('Flood Risk Management in Northern Ireland (NI Audit Office, 16 June 2026)', 'https://www.niauditoffice.gov.uk/files/niauditoffice/documents/2026-06/NI%20Audit%20Office%20Media%20Release%20-%20Flood%20Risk%20Management%20in%20Northern%20Ireland.pdf'),
 'pr_dfe': ('Flood support programme for businesses (Department for the Economy, 21 February 2024)', 'https://www.economy-ni.gov.uk/news/murphy-announces-details-flood-support-programme-businesses'),
 'pr_itv': ('Details of £15m flood support allocation (ITV News, 9 November 2023)', 'https://www.itv.com/news/utv/2023-11-09/details-of-15m-flood-support-allocation-revealed'),
 'pr_road': ('Road maintenance funding shortfall (agendaNi, 22 April 2026)', 'https://www.agendani.com/road-maintenance-funding-shortfall/'),
 'pr_dfi': ('Update on road infrastructure projects (Department for Infrastructure, 9 December 2025)', 'https://www.infrastructure-ni.gov.uk/news/council-receives-update-road-infrastructure-projects-fermanagh-and-omagh-district-council-2025'),
 'pr_ln': ('Action being taken to address issues at Lough Neagh (DAERA, updated 11 August 2026)', 'https://www.daera-ni.gov.uk/articles/action-being-taken-address-issues-lough-neagh'),
 'pr_ccc': ('Adapting to climate change: progress in Northern Ireland (Climate Change Committee, 20 April 2023)', 'https://www.theccc.org.uk/publication/adapting-to-climate-change-progress-in-northern-ireland/'),
 'pr_niccap': ("Northern Ireland's third Climate Change Adaptation Programme published (DAERA, 19 March 2026)", 'https://www.daera-ni.gov.uk/news/northern-irelands-third-climate-change-adaptation-programme-published'),
 'pr_obr': ('Public sector net investment (Office for Budget Responsibility, March 2020)', 'https://obr.uk/box/public-sector-net-investment/'),
 'pr_ippr': ('Investment in UK lowest in G7 (IPPR, 18 June 2024)', 'https://ippr.org/media-office/revealed-investment-in-uk-is-lowest-in-g7-for-third-year-in-a-row-new-data-shows'),
 'pr_gb': ('Green Book Review 2025: one year on (HM Treasury, 30 June 2026)', 'https://www.gov.uk/government/publications/green-book-review-2025-one-year-on/green-book-review-2025-one-year-on'),
 'pr_mhclg': ('The value and incidence of developer contributions in England 2018/19 (MHCLG, August 2020)', 'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/907203/The_Value_and_Incidence_of_Developer_Contributions_in_England_201819.pdf'),
 'pr_xr': ('Paying for Crossrail: business rate supplement (Greater London Authority)', 'https://www.london.gov.uk/paying-crossrail-business-rate-supplement'),
 'pr_dc': ('Consultation responses report: developer contributions for wastewater infrastructure (DfI, 19 March 2026)', 'https://www.infrastructure-ni.gov.uk/publications/consultation-reponses-report-developer-contributions-wastewater-infrastructure'),
})

D = {}

# NI Screen ---------------------------------------------------------------------
scr_spend = [('Target, 2022–26 strategy', 442, '£442m'), ('Achieved, 2022–26 strategy', 477, '£477m')]
scr_grant = [('2018/19', 14, 'about £14m'), ('2025/26', 20, 'about £20m')]
scr_dfe = [('DfE resource budget 2025/26', 814.5, '£814.5m'), ('DfE resource budget 2026/27', 798.4, '£798.4m'), ('Pressures to absorb, 2026/27', 134, 'about £134m')]
scr_depth = [('Crew living in NI', 88, '88%'), ('Heads of department living in NI', 73, '73%'), ('Trainees in work a year on', 73, '73%'), ('Blue Lights series 1–2 budget spent in NI', 80, 'over 80%')]
scr_ire = [('Section 481 credit rate', '32%', 'Cap €125m a project; 40% uplift for smaller features; new credits for visual effects and unscripted'),
           ('Irish production spend, 2025', '€544m', 'A record; industry asking for a regional uplift outside Dublin and Wicklow'),
           ('Shared Island Media Fund, 2026–28', '€14m', 'Irish Government fund for cross-border film, TV and radio')]
scr_assets = [('Studio Ulster virtual production facility', '£72m; opened June 2025', 'Said in March 2026 that demand was beating forecasts'),
              ('NI Screen games development calls', 'Up to £15,000 a project', 'A start-up sum, not a scale-up one'),
              ('NI Screen sustainability support (2025)', 'Top-up funding', 'Carbon reporting through albert, HVO instead of diesel, a sustainability adviser from week one'),
              ('Studio renewable energy data', 'None published', 'No published renewable energy figures found for any NI studio'),
              ('Irish Language and Ulster-Scots broadcast funds', 'Short-term settlements', 'No confirmed allocation found for the current year')]
scr_scen = [('1. Squeezed', 'Grant cut by a fifth', 'Big productions protected; training, games and local work cut first; spend slips as crews drift to Dublin and Manchester'),
            ('2. Steady', 'About £20m a year, year by year', 'Repeats the last four years; studio decisions and language funds wait on each budget'),
            ('3. Grown', 'Four-year envelope', 'Mix shifts to clean-power stages, local IP, games and animation, and one locations service')]
D['ni-screen-industry'] = dict(
 title='Northern Ireland Screen Industry dashboard', h1='Northern Ireland screen industry',
 desc='Dashboard of Northern Ireland Screen funding and results, local crew depth, the Irish incentives next door and the assets that could grow the sector. By Robert J. Park.',
 lead='NI Screen received about <b>£73m</b> from the Department for the Economy in 2022–26, and the productions it backed spent <b>£477m</b> in Northern Ireland. This page sets out the money, the competition and what would make the spend stay.',
 tiles=[tile('DfE funding, Apr 2022–Mar 2026', '≈£73m', 'To NI Screen over the strategy'), tile('Local production spend', '£477m', 'Against a £442m target', 'k-good'),
        tile('Local spend per £ of DfE money', '≈£6.50', 'Derived; DfE money also paid for skills'), tile('Crew living in NI', '88%', 'Major productions, last strategy', 'k-good'),
        tile('UK film and HETV spend, 2025', '£6.8bn', '85% of it inward investment'), tile('DfE resource budget, 2026/27', '−£16.1m', '£814.5m to £798.4m, with ≈£134m of pressures', 'k-bad')],
 cards=[
  card('Spend against target, 2022–26', 'Production spend in Northern Ireland by NI Screen-backed productions.', bars(scr_spend, hi=['Achieved, 2022–26 strategy']), ['scr_be', 'scr_in'], csv_href(['measure', 'gbp_m'], [[a, b] for a, b, c in scr_spend]), 'ni-screen-spend-vs-target'),
  card("NI Screen's grant from the Department", 'Approximate annual grant-in-aid.', bars(scr_grant, hi=['2025/26']), ['scr_ec'], csv_href(['year', 'gbp_m_approx'], [[a, b] for a, b, c in scr_grant]), 'ni-screen-grant'),
  card('The budget around it', 'Department for the Economy day-to-day budget, and the pressures it has to absorb.', bars(scr_dfe, hi=['Pressures to absorb, 2026/27']), ['scr_ec'], csv_href(['measure', 'gbp_m'], [[a, b] for a, b, c in scr_dfe]), 'dfe-budget-2026-27'),
  card('Local depth', 'Share of crew, heads of department and trainees based or working in NI, from the last strategy; and one series.', bars(scr_depth, maxv=100), ['scr_be', 'scr_bl'], csv_href(['measure', 'pct'], [[a, b] for a, b, c in scr_depth]), 'ni-screen-local-depth'),
  card('Next door: the Irish offer', 'What a production weighs up when it looks south of the border.', table(['Measure', 'Figure', 'Detail'], scr_ire), ['scr_481', 'scr_it', 'scr_sim'], csv_href(['measure', 'figure', 'detail'], scr_ire), 'ireland-screen-incentives', wide=True),
  card('What stays when the cameras leave', 'Assets and gaps that decide whether production spend becomes lasting business.', table(['Item', 'Status', 'Note'], scr_assets), ['scr_su1', 'scr_su2', 'scr_gam', 'scr_sus', 'scr_lang'], csv_href(['item', 'status', 'note'], scr_assets), 'ni-screen-assets', wide=True),
  card('Three scenarios for 2026–30', 'Illustrative, built on the last strategy\'s results. Not forecasts.', table(['Scenario', 'Funding', 'What happens'], scr_scen), ['scr_ec', 'scr_bp'], csv_href(['scenario', 'funding', 'what_happens'], scr_scen), 'ni-screen-scenarios', wide=True),
 ], issue='/blog/2026/11/northern-ireland-screen-how-do-we-grow-it/', issue_title='Northern Ireland Screen is fantastic. So how do we grow it?', date='2 November 2026')

# Public realm: drains and floods ---------------------------------------------
pr_ww = [('Areas where development is restricted', 100, 'about 100'), ('Sewer networks under constraint', 107, 'about 107'), ('Treatment works at or over capacity', 66, 'about 66')]
pr_roads = [('Structural maintenance needed a year', 190, '£190m'), ('Routine maintenance needed a year', 60, '£60m'), ('Opening budget this year (all maintenance)', 68, '£68m')]
pr_inv = [('Up to the 1970s', 4.0, 'about 4% of GDP'), ('This century, average', 1.0, 'about 1% of GDP'), ('Now, rising to', 2.5, 'about 2.5% of GDP')]
pr_ln = [('Actions complete', 23, '23'), ('Actions still open (derived)', 14, '14')]
pr_so = [('Storm overflows', '2,458', 'NI Water'), ('Modelled so far', 'About half', 'NI Water'), ('Unsatisfactory, of those modelled', 'About 37%', 'NI Water'), ('Monitored by spring 2027', 'About 30%', 'NI Water')]
pr_flood = [('Properties in floodplains', 'About 45,000', 'NI Audit Office, June 2026'), ('Flood spending, last four years', '+73%', 'NI Audit Office'), ('Flood schemes finishing on time', '1 in 5', 'NI Audit Office'),
            ('Emergency support after Oct 2023 floods', '£15m', 'Plus grants of up to £100,000 a business'), ('Wastewater investment needed', 'About £7bn', 'NI Water estimate'), ('Homes held back by wastewater limits', 'About 15,000', 'Department for Infrastructure'),
            ('Belfast Living With Water programme', '£1.9bn, largely on hold', 'Water Magazine, 2026')]
pr_lvc = [('England: developer contributions, 2018/19', 'About £7bn', 'Planning agreements and Community Infrastructure Levy'), ('London: Crossrail', 'About £7bn', 'Business rate supplement and mayoral levy'),
          ('Northern Ireland', 'No Community Infrastructure Levy', 'Case-by-case Section 76 agreements'), ('NI wastewater contributions', 'Policy in development', 'DfI consulted in 2025; responses report 19 March 2026')]
pr_scen = [('1. Patch and pay', 'Year-by-year budgets; capital goes to whatever broke last winter', 'The bill is paid anyway, in emergency grants, insurance, lost homes and investment'),
           ('2. Capital catch-up', 'One-off settlement for NI Water and flood defences', 'Helps, then decays without a duty and a stable source of money'),
           ('3. Duty and entitlement', 'Continuous improvement duty, minimum entitlements, better appraisal, land value capture', 'What the Public Realm Bill sets out to do')]
D['ni-public-realm-water-roads'] = dict(
 title='NI Public Realm: Water, Roads and Floods dashboard', h1='Northern Ireland public realm: water, roads and floods',
 desc='Dashboard of Northern Ireland wastewater capacity, storm overflows, roads, flood risk, Lough Neagh, UK public investment and how other places pay for infrastructure. By Robert J. Park.',
 lead='Around <b>100</b> places in Northern Ireland can\'t take new homes because the sewers are full, roads get about <b>a quarter</b> of the maintenance money they need, and NI Water puts its wastewater need at <b>£7bn</b>. This page brings the figures together.',
 tiles=[tile('Homes held back', '≈15,000', 'By wastewater limits (DfI)', 'k-bad'), tile('Wastewater investment needed', '≈£7bn', 'NI Water estimate', 'k-bad'),
        tile('Storm overflows unsatisfactory', '≈37%', 'Of those modelled, out of 2,458', 'k-bad'), tile('Road maintenance funded', '≈27%', 'Derived: £68m against £250m a year needed', 'k-bad'),
        tile('Properties in floodplains', '≈45,000', 'Flood spending up 73% in four years'), tile('Lough Neagh actions complete', '23 of 37', 'Lough supplies about 40% of drinking water')],
 cards=[
  card('Wastewater: where the system is full', 'Development restricted (about 100 areas, including 25 cities and towns), networks constrained and treatment works at capacity.', bars(pr_ww, hi=['Areas where development is restricted']), ['pr_niao_w', 'pr_cap'], csv_href(['measure', 'count'], [[a, b] for a, b, c in pr_ww]), 'ni-wastewater-capacity'),
  card('Roads: need against budget', '£ million a year. The opening budget covers all maintenance.', bars(pr_roads, hi=['Opening budget this year (all maintenance)']), ['pr_road', 'pr_dfi'], csv_href(['measure', 'gbp_m'], [[a, b] for a, b, c in pr_roads]), 'ni-roads-need-vs-budget'),
  card('Storm overflows', 'What is known about NI Water\'s overflows.', table(['Measure', 'Figure', 'Source'], pr_so), ['pr_so'], csv_href(['measure', 'figure', 'source'], pr_so), 'ni-storm-overflows'),
  card('Lough Neagh action plan', 'DAERA\'s 37 actions. Recovery will take decades, the Minister has said.', bars(pr_ln, hi=['Actions still open (derived)'], maxv=37), ['pr_ln'], csv_href(['measure', 'count'], [[a, b] for a, b, c in pr_ln]), 'lough-neagh-actions'),
  card('UK public investment', 'Public sector net investment as a share of GDP. IPPR found UK total investment the lowest in the G7 in 24 of the 30 years to 2022.', bars(pr_inv, hi=['This century, average'], maxv=4.0), ['pr_obr', 'pr_ippr'], csv_href(['period', 'pct_gdp'], [[a, b] for a, b, c in pr_inv]), 'uk-public-investment'),
  card('Flooding and the cost of catching up', 'The admitted under-investment, in official figures.', table(['Measure', 'Figure', 'Source'], pr_flood), ['pr_niao_f', 'pr_itv', 'pr_dfe', 'pr_wm'], csv_href(['measure', 'figure', 'source'], pr_flood), 'ni-flood-and-water-figures', wide=True),
  card('Who pays elsewhere: land value capture', 'How other places fund infrastructure from the value it creates.', table(['Where', 'Figure', 'How'], pr_lvc), ['pr_mhclg', 'pr_xr', 'pr_dc'], csv_href(['where', 'figure', 'how'], pr_lvc), 'land-value-capture', wide=True),
  card('Three scenarios to the mid-2030s', 'Illustrative, based on the work behind the Public Realm Bill. Not forecasts.', table(['Scenario', 'What it means', 'Outcome'], pr_scen), ['pr_ur', 'pr_gb', 'pr_ccc', 'pr_niccap'], csv_href(['scenario', 'means', 'outcome'], pr_scen), 'public-realm-scenarios', wide=True),
 ], issue='/blog/2026/11/we-dont-fund-the-drains-then-we-pay-for-the-flood/', issue_title="We don't fund the drains. Then we pay for the flood.", date='2 November 2026')

for slug, d in D.items():
    out = page(slug, d['title'], d['h1'], d['lead'], d['tiles'], d['cards'], d['issue'], d['issue_title'], d['date'], d['desc'])
    out = out.replace('checked on 20–21 October 2026', 'checked against the sources cited in the accompanying piece, as at 2 November 2026')
    out = out.replace('Figures checked on 21 October 2026, for publication with the issue of', 'Figures as at 2 November 2026, published with the piece of')
    out = out.replace('<p class="k-foot">Commentary:', '<p class="k-foot">Read the piece:')
    open(os.path.join(ROOT, 'tools/dashboards', slug + '.html'), 'w', encoding='utf-8').write(out)
    print(slug, len(out))
