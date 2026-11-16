"""Charts and data for 'Deck the halls, check the rules' (16 Nov 2026).
Writes SVG charts to assets/briefings/christmas-decorations/ and CSVs to
data/dashboards/christmas-decorations/. Brand: red #A61C1C, ink #1A1A1A, grey #8C8C8C.
Every bar and point carries a <title> so it shows a tooltip on hover.
Usage: python3 charts.py <repo_root>
"""
import sys, os, csv, html

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
OUT = os.path.join(ROOT, 'assets/briefings/christmas-decorations')
DATA = os.path.join(ROOT, 'data/dashboards/christmas-decorations')
os.makedirs(OUT, exist_ok=True); os.makedirs(DATA, exist_ok=True)
RED, INK, GREY, MUTED, RULE = '#A61C1C', '#1A1A1A', '#8C8C8C', '#5A5A5A', '#E6E2E0'
FONT = "'Source Sans 3','Source Sans Pro',Arial,sans-serif"
NI_P, GB_P = 34.15, 26.32  # p/kWh incl VAT: Power NI from 1 Jul 2026; Ofgem cap 1 Oct-31 Dec 2026
HOURS = 240  # 6 hours a day for 40 days

def esc(s): return html.escape(str(s))

def svg_open(w, h, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" '
            f'font-family="{FONT}"><title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>'
            f'<rect width="{w}" height="{h}" fill="#fff"/>')

def hbar(name, title, desc, rows, unit_fmt, colour=RED, note='', w=720, maxv=None):
    """rows: (label, value, display_label, highlight)"""
    lab_w, top, bh, gap = 260, 56, 26, 12
    h = top + len(rows) * (bh + gap) + 40
    maxv = maxv or max(r[1] for r in rows)
    plot_w = w - lab_w - 175
    s = [svg_open(w, h, title, desc),
         f'<text x="0" y="22" font-size="17" font-weight="700" fill="{INK}">{esc(title)}</text>']
    for i, (lab, v, disp, hi) in enumerate(rows):
        y = top + i * (bh + gap)
        bw = max(2, plot_w * v / maxv)
        c = colour if hi else GREY
        s.append(f'<text x="{lab_w-10}" y="{y+bh*0.68}" font-size="13" text-anchor="end" fill="{INK}">{esc(lab)}</text>')
        s.append(f'<g><title>{esc(lab)}: {esc(disp)}</title><rect x="{lab_w}" y="{y}" width="{bw:.1f}" height="{bh}" rx="4" fill="{c}"/></g>')
        s.append(f'<text x="{lab_w+bw+8:.1f}" y="{y+bh*0.68}" font-size="13" fill="{INK}" font-weight="600">{esc(disp)}</text>')
    s.append(f'<line x1="{lab_w}" y1="{top-6}" x2="{lab_w}" y2="{h-34}" stroke="{INK}" stroke-width="1"/>')
    if note:
        s.append(f'<text x="0" y="{h-10}" font-size="11" fill="{MUTED}">{esc(note)}</text>')
    s.append('</svg>')
    open(os.path.join(OUT, name), 'w').write(''.join(s))

def line_chart():
    w, h, l, r, t, b = 720, 380, 60, 190, 56, 64
    years = list(range(1, 21))
    series = [('Artificial tree, kept', [40 for y in years], INK, '0'),
              ('Real tree each year, chipped', [3.5 * y for y in years], RED, '0'),
              ('Real tree each year, landfilled', [16 * y for y in years], GREY, '6 4')]
    ymax = 160
    X = lambda y: l + (w - l - r) * (y - 1) / 19
    Y = lambda v: t + (h - t - b) * (1 - min(v, ymax) / ymax)
    s = [svg_open(w, h, 'One artificial tree or a new real tree every year: cumulative carbon (kg CO2e)',
                  'Line chart over 20 years. An artificial tree is 40 kg CO2e once. A real tree that is chipped adds 3.5 kg a year and passes 40 kg after 11.4 years. A landfilled real tree adds 16 kg a year and passes 40 kg after 2.5 years.'),
         f'<text x="0" y="22" font-size="17" font-weight="700" fill="{INK}">Cumulative carbon over the years you keep it (kg CO2e)</text>']
    for v in range(0, ymax + 1, 40):
        s.append(f'<line x1="{l}" y1="{Y(v)}" x2="{w-r}" y2="{Y(v)}" stroke="{RULE}"/><text x="{l-8}" y="{Y(v)+4}" font-size="12" text-anchor="end" fill="{MUTED}">{v}</text>')
    for y in (1, 5, 10, 15, 20):
        s.append(f'<text x="{X(y)}" y="{h-b+20}" font-size="12" text-anchor="middle" fill="{MUTED}">{y}</text>')
    s.append(f'<text x="{(l+w-r)/2}" y="{h-b+42}" font-size="12" text-anchor="middle" fill="{MUTED}">Years</text>')
    for name, vals, c, dash in series:
        pts = ' '.join(f'{X(y):.1f},{Y(v):.1f}' for y, v in zip(years, vals) if v <= ymax)
        s.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="2.5" stroke-dasharray="{dash}"/>')
        for y, v in zip(years, vals):
            if v <= ymax:
                s.append(f'<g><title>{esc(name)}, year {y}: {v:g} kg</title><circle cx="{X(y):.1f}" cy="{Y(v):.1f}" r="7" fill="transparent"/></g>')
        ly = max(y for y, v in zip(years, vals) if v <= ymax)
        v = vals[years.index(ly)]
        dy = 16 if 'chipped' in name else 4
        s.append(f'<text x="{X(ly)+8}" y="{Y(v)+dy}" font-size="12" fill="{INK}">{esc(name)}</text>')
    for be, lab in ((40 / 3.5, '11.4 years'), (2.5, '2.5 years')):
        s.append(f'<circle cx="{X(be):.1f}" cy="{Y(40):.1f}" r="5" fill="#fff" stroke="{INK}" stroke-width="2"/>'
                 f'<text x="{X(be):.1f}" y="{Y(40)-12:.1f}" font-size="12" text-anchor="middle" fill="{INK}" font-weight="600">{lab}</text>')
    s.append(f'<text x="0" y="{h-6}" font-size="11" fill="{MUTED}">Carbon Trust figures as quoted by the growers\' trade body (BCTGA); not on the Carbon Trust\'s own page.</text></svg>')
    open(os.path.join(OUT, 'tree-cumulative-carbon.svg'), 'w').write(''.join(s))

def studies_chart():
    rows = [('Ellipsos, Canada (2009)', 20, 20, 'Funder not stated', False),
            ('Carbon Trust\'s own advice (2023)', 7, 20, 'Carbon Trust', False),
            ('Dovetail review (2018), climate only', 15, 20, 'Non-profit review', False),
            ('Quoted figures, chipped (computed)', 11.4, 11.4, 'BCTGA, attributed to Carbon Trust', False),
            ('PE Americas (2010)', 4, 9, 'Paid for by artificial-tree trade body', True),
            ('WAP Sustainability (2018)', 5, 5, 'Paid for by artificial-tree trade body', True)]
    w, lab_w, top, bh, gap = 720, 300, 56, 24, 22
    h = top + len(rows) * (bh + gap) + 60
    X = lambda v: lab_w + (w - lab_w - 130) * v / 20
    s = [svg_open(w, h, 'Years an artificial tree must be reused to beat a real tree on climate, by study',
                  'Ellipsos 2009: about 20 years. Carbon Trust advice 2023: 7 to 20 years. Dovetail 2018: 15 to 20 years on climate alone. Figures quoted by BCTGA and attributed to the Carbon Trust: 11.4 years against a chipped real tree. PE Americas 2010 (paid for by the American Christmas Tree Association): 4 to 9 years. WAP Sustainability 2018 (same funder): 5 years.'),
         f'<text x="0" y="22" font-size="17" font-weight="700" fill="{INK}">Years of reuse before an artificial tree beats a real one</text>']
    for v in (0, 5, 10, 15, 20):
        s.append(f'<line x1="{X(v)}" y1="{top-8}" x2="{X(v)}" y2="{h-50}" stroke="{RULE}"/><text x="{X(v)}" y="{h-34}" font-size="12" text-anchor="middle" fill="{MUTED}">{v}</text>')
    for i, (lab, lo, hi, who, trade) in enumerate(rows):
        y = top + i * (bh + gap)
        c = RED if trade else INK
        s.append(f'<text x="{lab_w-10}" y="{y+bh*0.55}" font-size="13" text-anchor="end" fill="{INK}">{esc(lab)}</text>')
        s.append(f'<text x="{lab_w-10}" y="{y+bh*0.55+14}" font-size="11" text-anchor="end" fill="{MUTED}">{esc(who)}</text>')
        disp = f'{lo:g}' if lo == hi else f'{lo:g}–{hi:g}'
        if lab.startswith('Ellipsos'): disp = 'about 20'
        s.append(f'<g><title>{esc(lab)}: {disp} years ({esc(who)})</title><rect x="{X(lo)-5:.1f}" y="{y}" width="{X(hi)-X(lo)+10:.1f}" height="{bh}" rx="4" fill="{c}"/></g>')
        s.append(f'<text x="{X(hi)+10:.1f}" y="{y+bh*0.68}" font-size="13" font-weight="600" fill="{INK}">{disp} yrs</text>')
    s.append(f'<text x="0" y="{h-8}" font-size="11" fill="{MUTED}">Red: paid for by the American Christmas Tree Association, the artificial-tree makers\' body.</text></svg>')
    open(os.path.join(OUT, 'tree-breakeven-studies.svg'), 'w').write(''.join(s))

LIGHTS = [('C9 bulbs, 25 × 7 W', 175, True), ('C7 bulbs, 25 × 5 W', 125, True),
          ('Mini incandescent, 100 bulbs (≈40 W)*', 40, True), ('LED, 100 bulbs (Energy Star ceiling 20 W)', 20, False),
          ('LED, 70 bulbs (2 W)', 2, False)]

def lights():
    rows = []
    for lab, wt, inc in LIGHTS:
        kwh = wt * HOURS / 1000
        rows.append((lab, kwh * NI_P / 100, f'£{round(kwh*NI_P/100+1e-9,2):.2f} (GB £{round(kwh*GB_P/100+1e-9,2):.2f})', inc))
    hbar('lights-season-cost.svg', 'Running one string of lights for the season, Northern Ireland prices',
         'Cost of 240 hours (6 hours a day for 40 days) at the Power NI unit rate of 34.15p per kWh including VAT, with the GB price cap rate of 26.32p in brackets. C9 incandescent string £14.34; C7 £10.25; mini incandescent £3.28; LED 100-bulb £1.64; LED 70-bulb £0.16.',
         rows, None, note='240 hours. Power NI 34.15p/kWh incl. VAT (from 1 Jul 2026); GB cap 26.32p (1 Oct–31 Dec 2026). *Assumed.')
    with open(os.path.join(DATA, 'lights-season-cost.csv'), 'w', newline='') as f:
        c = csv.writer(f); c.writerow(['string', 'watts', 'hours', 'kwh', 'cost_ni_gbp', 'cost_gb_gbp'])
        for lab, wt, _ in LIGHTS:
            k = wt * HOURS / 1000; c.writerow([lab, wt, HOURS, round(k, 2), round(k * NI_P / 100, 2), round(k * GB_P / 100, 2)])

IMPORTS = """group,year,country,value_gbp,netmass_kg
Christmas articles 950510,2025,TOTAL,252342033,48519816
Christmas articles 950510,2025,China,206706892,44291712
Christmas articles 950510,2025,Netherlands,15202642,1494099
Christmas articles 950510,2025,India,5322795,381315
Christmas articles 950510,2025,Hong Kong,3665837,619550
Christmas articles 950510,2025,Poland,3622652,87587
Christmas articles 950510,2025,Vietnam,2606210,547954
Christmas articles 950510,2025,Denmark,2495848,83859
Christmas articles 950510,2025,United States,1408499,57388
Christmas articles 950510,2024,TOTAL,243945119,64514516
Christmas articles 950510,2024,China,203772717,60621766
of which glass 95051010,2025,TOTAL,17521182,1685175
of which glass 95051010,2025,China,10616332,1198218
of which glass 95051010,2025,Netherlands,3622782,316438
Christmas lighting strings 94053100+94053900,2025,TOTAL,63280815,8467358
Christmas lighting strings 94053100+94053900,2025,China,57375336,8046762
Christmas lighting strings 94053100+94053900,2024,TOTAL,59386066,6820044
Fresh Christmas trees 06042020,2025,TOTAL,19486725,16536124
Fresh Christmas trees 06042020,2025,Denmark,10180135,8653047
Fresh Christmas trees 06042020,2025,Ireland,4188854,4673864
Fresh Christmas trees 06042020,2025,Netherlands,3841611,1948553
Fresh Christmas trees 06042020,2025,Belgium,563124,684787
Fresh Christmas trees 06042020,2024,TOTAL,19081138,16914705
"""

def main():
    hbar('tree-carbon.svg', 'Carbon footprint of a 2 m Christmas tree (kg CO2e)',
         'Artificial PVC tree about 40 kg CO2e; real tree landfilled about 16 kg; real tree chipped about 3.5 kg.',
         [('Artificial (PVC), made once', 40, '≈40 kg', False), ('Real, sent to landfill', 16, '≈16 kg', True), ('Real, chipped or burned', 3.5, '≈3.5 kg', True)],
         None, note='As quoted by the British Christmas Tree Growers Association (trade body), attributed to the Carbon Trust. Unverified at source.')
    line_chart(); studies_chart(); lights()
    hbar('litter-fines.svg', 'Maximum fixed penalties: Northern Ireland and England',
         'Fly-tipping: England up to £5,000 since 1 September 2026; Northern Ireland up to £400. Dropping litter: England up to £750 since 1 September 2026; Northern Ireland up to £200 since 30 December 2022.',
         [('Fly-tipping, England', 5000, '£5,000', False), ('Fly-tipping, Northern Ireland', 400, '£400', True),
          ('Litter, England', 750, '£750', False), ('Litter, Northern Ireland', 200, '£200', True)],
         None, note='England: S.I. 2026/816, from 1 Sep 2026 (GOV.UK, 15 Jul 2026). NI: SR 2012/35 as amended; 1997 Order, art. 4A.')
    hbar('imports-christmas-articles.svg', 'UK imports of Christmas articles, 2025, by country (£ million)',
         'China 206.7; Netherlands 15.2; India 5.3; Hong Kong 3.7; Poland 3.6; Vietnam 2.6; Denmark 2.5; all others 12.7. Total 252.3 million pounds. China is 81.9 per cent by value and 91.3 per cent by weight.',
         [('China', 206.7, '£206.7m (81.9%)', True), ('Netherlands', 15.2, '£15.2m', False), ('India', 5.3, '£5.3m', False), ('Hong Kong', 3.7, '£3.7m', False),
          ('Poland', 3.6, '£3.6m', False), ('Vietnam', 2.6, '£2.6m', False), ('Denmark', 2.5, '£2.5m', False), ('All others', 12.7, '£12.7m', False)],
         None, note='HMRC Overseas Trade Statistics, code 9505 10, calendar 2025 (total £252.3m; 48,520 tonnes). EU figures are by country of dispatch.')
    hbar('imports-fresh-trees.svg', 'UK imports of fresh Christmas trees, 2025, by country (£ million)',
         'Denmark 10.2; Ireland 4.2; Netherlands 3.8; Belgium 0.6; all others 0.7. Total 19.5 million pounds.',
         [('Denmark', 10.2, '£10.2m (52%)', True), ('Ireland', 4.2, '£4.2m (21.5%)', True), ('Netherlands', 3.8, '£3.8m (19.7%)', True), ('Belgium', 0.6, '£0.6m', True), ('All others', 0.7, '£0.7m', False)],
         None, note='HMRC Overseas Trade Statistics, code 0604 20 20, calendar 2025 (total £19.5m; 16,536 tonnes).')
    hbar('fires-1959.svg', 'Fires involving Christmas decorations, England and Wales, 24–31 December 1959',
         'Fourteen fires: naked lights 5, electrical faults 4, decorations falling on fires 4, soot 1.',
         [('Naked lights (candles, matches)', 5, '5', True), ('Electrical faults', 4, '4', True), ('Decorations fell on fires', 4, '4', True), ('Soot', 1, '1', True)],
         None, note='Hansard, written answer, 8 December 1960.')
    with open(os.path.join(DATA, 'tree-carbon.csv'), 'w', newline='') as f:
        c = csv.writer(f); c.writerow(['years', 'artificial_kept_kg', 'real_chipped_kg', 'real_landfilled_kg'])
        for y in range(1, 21): c.writerow([y, 40, round(3.5 * y, 1), 16 * y])
    open(os.path.join(DATA, 'hmrc-imports-2025.csv'), 'w').write(IMPORTS)
    print('charts written to', OUT)

main()
