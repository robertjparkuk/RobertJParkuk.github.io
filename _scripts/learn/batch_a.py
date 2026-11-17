"""Diagrams for Learn Batch A (v0.36.0, 17 Nov 2026): hydrogen, carbon capture, nitrogen and fertiliser, offsets.
Usage: python3 _scripts/learn/batch_a.py <repo_root>
Reuses helpers from gases.py. Figures are from the research notes cited on each page.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gases import svg, text, atom, bond, molecule, e, RED, INK, GREY, MUTED, RULE, TINT  # noqa: E402

BLUE = '#4A6A8A'
GREEN = '#4E7D4E'


def arrow_defs(*cols):
    out = '<defs>'
    for i, c in enumerate(cols):
        out += (f'<marker id="a{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0 0L10 5L0 10z" fill="{c}"/></marker>')
    return out + '</defs>'


def box(x, y, w, h, title, lines=(), fill='#fff', stroke=RULE, tcol=INK, size=14, lh=16):
    b = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    b += text(x + w / 2, y + 22, title, size, tcol, weight='700')
    for i, ln in enumerate(lines):
        b += text(x + w / 2, y + 22 + lh * (i + 1), ln, 12, MUTED)
    return b


def arr(x1, y1, x2, y2, m=0, col=RED, w=2.2, dash=False):
    d = ' stroke-dasharray="5 4"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}" marker-end="url(#a{m})"{d}/>'


def wrap(t, n):
    out, cur = [], ''
    for wd in t.split():
        if len(cur) + len(wd) + 1 > n:
            out.append(cur); cur = wd
        else:
            cur = (cur + ' ' + wd).strip()
    out.append(cur)
    return out


def cycle(name, title, sub, nodes, centre, desc, w=900, h=600, cx=450, cy=330, R=200, notes=None):
    """nodes: list of (label, line1, line2, highlight). Drawn clockwise from the top."""
    b = text(20, 30, title, 20, INK, 'start', '700') + text(20, 52, sub, 13, MUTED, 'start')
    b += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{RULE}" stroke-width="12"/>'
    n = len(nodes)
    for i in range(n):
        a0 = math.radians(90 - (i + 0.5) * 360 / n)
        x, y = cx + R * math.cos(a0), cy - R * math.sin(a0)
        rot = 90 - math.degrees(a0)
        b += f'<path d="M-8 -7 L8 0 L-8 7 z" fill="{RED}" transform="translate({x:.1f} {y:.1f}) rotate({rot:.1f})"/>'
    bw, bh = 176, 74
    for i, (lab, l1, l2, hot) in enumerate(nodes):
        a = math.radians(90 - i * 360 / n)
        x, y = cx + R * math.cos(a), cy - R * math.sin(a)
        b += f'<rect x="{x-bw/2:.1f}" y="{y-bh/2:.1f}" width="{bw}" height="{bh}" rx="8" fill="{TINT if hot else "#fff"}" stroke="{RED if hot else GREY}" stroke-width="1.8"/>'
        b += text(x, y - 12, lab, 14, INK, weight='700') + text(x, y + 7, l1, 11.5, MUTED) + text(x, y + 22, l2, 11.5, MUTED)
    for i, ln in enumerate(centre):
        b += text(cx, cy - 10 * (len(centre) - 1) + 20 * i, ln, 15 if i == 0 else 12, INK if i == 0 else MUTED, weight='700' if i == 0 else '400')
    if notes:
        b += notes
    svg(name, w, h, title, desc, b)


# ---------------------------------------------------------------- hydrogen

def hydrogen_routes():
    w, h = 960, 640
    b = arrow_defs(INK, RED)
    b += text(20, 30, 'Hydrogen by colour: one molecule, many routes', 20, INK, 'start', '700')
    b += text(20, 52, 'The colour names are informal. What matters is the emissions per kilogram, shown in the next chart.', 13, MUTED, 'start')
    rows = [
        ('Grey', 'Natural gas + steam', 'Steam methane reforming', 'CH₄ + 2H₂O → CO₂ + 4H₂', 'CO₂ to air', GREY),
        ('Blue', 'Natural gas + steam', 'Reforming with carbon capture', 'CH₄ + 2H₂O → CO₂ + 4H₂', 'Most CO₂ stored', BLUE),
        ('Brown / black', 'Lignite or coal', 'Gasification', 'C + H₂O → CO + H₂ (+ shift)', 'Most CO₂ of all', '#6B4F3A'),
        ('Turquoise', 'Natural gas', 'Methane pyrolysis', 'CH₄ → C (solid) + 2H₂', 'Solid carbon', '#3E8E8E'),
        ('Green', 'Water + renewable power', 'Electrolysis', '2H₂O → 2H₂ + O₂', 'Oxygen only', GREEN),
        ('Pink', 'Water + nuclear power', 'Electrolysis', '2H₂O → 2H₂ + O₂', 'Oxygen only', '#C77C9A'),
        ('White / gold', 'Rocks underground', 'Natural (geological) hydrogen', 'Drilled, like gas', 'One well (Mali)', '#B0A060'),
    ]
    cols = [(20, 130), (165, 190), (370, 210), (595, 210), (820, 125)]
    hdr = ['Colour', 'Feedstock', 'Process', 'Overall reaction', 'By-product']
    for (x, cw), hd in zip(cols, hdr):
        b += text(x + 4, 86, hd, 12, MUTED, 'start', '700')
    for i, (col, feed, proc, rx, by, c) in enumerate(rows):
        y = 100 + i * 74
        b += f'<rect x="20" y="{y}" width="920" height="64" rx="6" fill="{"#fff" if i % 2 else "#faf9f8"}" stroke="{RULE}"/>'
        b += f'<rect x="20" y="{y}" width="10" height="64" fill="{c}"/>'
        b += text(42, y + 37, col, 15, INK, 'start', '700')
        b += text(169, y + 37, feed, 13, INK, 'start')
        b += text(374, y + 37, proc, 13, INK, 'start')
        b += text(599, y + 37, rx, 12, RED if 'CO₂' in rx else INK, 'start', '600', extra="font-family=\"'IBM Plex Mono',monospace\"")
        b += text(824, y + 37, by, 12, MUTED, 'start')
        for k in range(1, 4):
            b += arr(cols[k][0] - 18, y + 32, cols[k][0] - 4, y + 32, 0, INK, 1.4)
    b += text(940, h - 12, 'Reforming: CH₄ + H₂O → CO + 3H₂, then the water–gas shift CO + H₂O → CO₂ + H₂.', 11.5, MUTED, 'end')
    svg('hydrogen-routes.svg', w, h, 'How each colour of hydrogen is made',
        'Seven rows. Grey: natural gas and steam reformed, CH4 plus 2 H2O gives CO2 plus 4 H2, with the CO2 released. Blue: the same with most CO2 captured and stored. '
        'Brown or black: coal or lignite gasified, the most CO2 of any route. Turquoise: methane pyrolysis, CH4 gives solid carbon and 2 H2. '
        'Green: water split by electrolysis using renewable power, 2 H2O gives 2 H2 and O2. Pink: the same using nuclear power. White or gold: natural hydrogen drilled from rocks; one producing well, in Mali.', b)


def hydrogen_intensity():
    w, h = 960, 470
    L, R = 300, 920
    mx = 28
    X = lambda v: L + v / mx * (R - L)
    b = text(20, 30, 'Emissions per kilogram of hydrogen', 20, INK, 'start', '700')
    b += text(20, 52, 'kg CO₂e per kg H₂ at production (IEA ranges). The dashed lines are the UK and EU “low-carbon” ceilings.', 13, MUTED, 'start')
    bars = [('Coal gasification (brown/black)', 22, 26, '#6B4F3A'),
            ('Unabated gas reforming (grey)', 10, 12, GREY),
            ('Reforming, about 60% captured (blue)', 5, 8, BLUE),
            ('Reforming, over 90% captured (blue)', 0.8, 6, BLUE),
            ('Renewable electrolysis (green)*', 0.4, 2.7, GREEN)]
    for i, (lab, lo, hi, c) in enumerate(bars):
        y = 105 + i * 58
        b += text(L - 12, y + 22, lab, 13, INK, 'end', '600')
        b += f'<rect x="{X(lo):.1f}" y="{y+6}" width="{max(X(hi)-X(lo),3):.1f}" height="26" rx="4" fill="{c}"><title>{e(lab)}: {lo} to {hi}</title></rect>'
        b += text(max(X(hi), X(4.2)) + 8, y + 24, f'{lo}–{hi}', 12.5, INK, 'start', '700')
    for v, lab, col, anc, dx in [(2.4, 'UK ceiling 2.4', RED, 'end', -5), (3.38, 'EU ceiling about 3.4', INK, 'start', 5)]:
        b += f'<line x1="{X(v):.1f}" y1="80" x2="{X(v):.1f}" y2="395" stroke="{col}" stroke-width="2" stroke-dasharray="6 4"/>'
        b += text(X(v) + dx, 92, lab, 12, col, anc, '700')
    for v in range(0, 29, 4):
        b += f'<line x1="{X(v):.1f}" y1="395" x2="{X(v):.1f}" y2="401" stroke="{INK}"/>' + text(X(v), 416, str(v), 12, INK)
    b += f'<line x1="{L}" y1="395" x2="{R}" y2="395" stroke="{INK}"/>'
    b += text((L + R) / 2, 438, 'kg CO₂e per kg of hydrogen', 12.5, MUTED)
    b += text(20, h - 10, '* Green hydrogen is zero at the electrolyser; 0.4–2.7 is the share of building the wind or solar kit, which most standards leave out.', 11.5, MUTED, 'start')
    svg('hydrogen-intensity.svg', w, h, 'Emissions per kilogram of hydrogen by production route',
        'Horizontal ranges in kilograms of CO2 equivalent per kilogram of hydrogen: coal gasification 22 to 26; unabated gas reforming 10 to 12; reforming with about 60% capture 5 to 8; '
        'reforming with over 90% capture 0.8 to 6; renewable electrolysis 0.4 to 2.7, from building the generating equipment. The UK Low Carbon Hydrogen Standard ceiling is 2.4 and the EU ceiling about 3.4.', b)


def hydrogen_leak():
    nodes = [('Hydrogen leaks', 'from pipes, valves', 'and storage', True),
             ('Mops up OH', 'H₂ + OH → H₂O + H', 'the air’s “detergent”', False),
             ('Methane lasts longer', 'less OH to break', 'it down', True),
             ('More ozone and', 'stratospheric water', 'vapour', False)]
    cycle('hydrogen-indirect-warming.svg', 'Hydrogen is not a greenhouse gas, but a leak still warms',
          'It competes with methane for the hydroxyl radical (OH). Estimated 100-year GWP: 11.6 ± 2.8 (Sand et al. 2023).',
          nodes, ['Indirect warming', 'about 12 × CO₂ per tonne', 'over 100 years'],
          'A four-step loop. Hydrogen leaks from pipes, valves and storage. It reacts with the hydroxyl radical, H2 plus OH gives water and a hydrogen atom, using up the atmosphere’s main cleaning agent. '
          'With less OH, methane lasts longer. The chemistry also produces more ozone and stratospheric water vapour. The result: hydrogen has an estimated 100-year global warming potential of about 11.6, plus or minus 2.8.',
          w=900, h=560, cx=450, cy=310, R=175)


# ---------------------------------------------------------------- nitrogen

def nitrogen_cycle():
    w, h = 960, 660
    b = arrow_defs(INK, RED, GREEN, BLUE)
    b += text(20, 30, 'The nitrogen cycle on a Northern Ireland farm', 20, INK, 'start', '700')
    b += text(20, 52, 'Black arrows: the useful cycle. Red arrows: losses to air and water, and where nitrous oxide is made.', 13, MUTED, 'start')
    # air band
    b += f'<rect x="20" y="70" width="920" height="80" rx="8" fill="#f1f4f7" stroke="{RULE}"/>'
    b += text(480, 100, 'The air: 78% nitrogen gas (N₂), held by a triple bond', 15, INK, weight='700')
    b += text(480, 122, 'Plants cannot use N₂ until it is “fixed” into ammonia or nitrate', 12.5, MUTED)
    # ground band
    b += f'<rect x="20" y="430" width="920" height="210" rx="8" fill="#f7f3ee" stroke="{RULE}"/>'
    b += text(36, 452, 'Soil and water', 13, MUTED, 'start', '700')
    nodes = {
        'hb': (130, 230, 'Haber–Bosch', ['N₂ + 3H₂ → 2NH₃', '400–500 °C, iron catalyst']),
        'clover': (330, 230, 'Clover', ['Bacteria in root nodules', 'about 150 kg N/ha a year']),
        'nh4': (230, 510, 'Ammonium NH₄⁺', ['from fertiliser, slurry,', 'rotting plants']),
        'no3': (520, 510, 'Nitrate NO₃⁻', ['the form most plants', 'take up']),
        'crop': (520, 230, 'Grass and crops', ['protein in silage,', 'grain, milk, meat']),
        'denit': (800, 510, 'Wet, airless soil', ['NO₃⁻ → NO₂⁻ → NO', '→ N₂O → N₂']),
    }
    bw, bh = 180, 70
    for k, (x, y, t, ls) in nodes.items():
        hot = k in ('denit',)
        b += f'<rect x="{x-bw/2}" y="{y-bh/2}" width="{bw}" height="{bh}" rx="8" fill="{TINT if hot else "#fff"}" stroke="{RED if hot else INK}" stroke-width="1.6"/>'
        b += text(x, y - 12, t, 13.5, INK, weight='700') + text(x, y + 6, ls[0], 11.5, MUTED) + text(x, y + 21, ls[1], 11.5, MUTED)
    # fixation from air
    b += arr(130, 150, 130, 193, 0, INK) + arr(330, 150, 330, 193, 0, GREEN)
    b += arr(150, 267, 215, 473, 0, INK) + arr(310, 267, 245, 473, 0, GREEN)
    b += text(178, 330, 'spread as', 11.5, MUTED, 'start') + text(178, 344, 'fertiliser', 11.5, MUTED, 'start')
    # nitrification
    b += arr(322, 510, 428, 510, 0, INK)
    b += text(375, 495, 'Nitrification', 12, INK, weight='700') + text(375, 572, 'NH₄⁺ → NO₂⁻ → NO₃⁻', 11.5, MUTED)
    b += text(375, 588, 'leaks some N₂O', 11.5, RED, weight='600')
    # uptake
    b += arr(520, 473, 520, 267, 0, INK) + text(530, 380, 'uptake', 11.5, MUTED, 'start')
    # crop back to ammonium (manure / residues)
    b += arr(470, 267, 255, 473, 0, INK, 1.6, True) + text(408, 330, 'manure, slurry,', 11.5, MUTED, 'start') + text(408, 344, 'crop residues', 11.5, MUTED, 'start')
    # denitrification
    b += arr(612, 510, 708, 510, 1, RED)
    b += arr(800, 473, 800, 152, 1, RED) + text(790, 300, 'N₂O (a greenhouse gas)', 12, RED, 'end', '700') + text(790, 316, 'and N₂ back to the air', 11.5, MUTED, 'end')
    # losses
    b += f'<polyline points="140,525 30,525 30,160" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#a1)"/>' + text(38, 320, 'Ammonia', 12, RED, 'start', '700') + text(38, 335, 'NH₃ gas', 11, MUTED, 'start') + text(38, 348, 'from urea', 11, MUTED, 'start') + text(38, 361, 'and slurry', 11, MUTED, 'start')
    b += arr(520, 547, 520, 610, 1, RED) + text(530, 600, 'Leaching: nitrate to rivers and loughs', 12, RED, 'start', '700')
    # crop to food
    b += arr(612, 230, 690, 230, 0, INK) + text(760, 222, 'Food leaves', 12, INK, weight='700') + text(760, 238, 'the farm', 12, INK, weight='700')
    svg('nitrogen-cycle.svg', w, h, 'The nitrogen cycle on a farm, with the losses',
        'Nitrogen gas in the air is fixed into ammonia by the Haber–Bosch process (N2 plus 3 H2 gives 2 NH3, at 400 to 500 °C with an iron catalyst) or by bacteria in clover root nodules, about 150 kg of nitrogen per hectare a year. '
        'It reaches the soil as ammonium, which bacteria turn into nitrate (nitrification), leaking some nitrous oxide. Grass and crops take up nitrate and turn it into protein; manure and residues return it to the soil. '
        'Losses, in red: ammonia gas escapes from urea and slurry; nitrate leaches to rivers and loughs; in wet, airless soil, bacteria turn nitrate back through nitrite, nitric oxide and nitrous oxide to nitrogen gas (denitrification), releasing nitrous oxide, a greenhouse gas.', b)


def fertiliser_chain():
    w, h = 960, 470
    b = arrow_defs(INK, RED)
    b += text(20, 30, 'The life cycle of a bag of nitrogen fertiliser', 20, INK, 'start', '700')
    b += text(20, 52, 'Where the emissions are, and which part a carbon border tax counts.', 13, MUTED, 'start')
    st = [('Natural gas', ['the hydrogen', 'source'], 'Methane leaks'),
          ('Hydrogen', ['CH₄ + 2H₂O', '→ CO₂ + 4H₂'], 'CO₂ (the biggest)'),
          ('Ammonia', ['N₂ + 3H₂', '→ 2NH₃'], 'Energy for heat and pressure'),
          ('Nitric acid', ['NH₃ + 2O₂', '→ HNO₃ + H₂O'], 'N₂O (unless abated)'),
          ('Fertiliser', ['ammonium nitrate,', 'CAN or urea'], 'Electricity'),
          ('Ship and lorry', ['to the', 'merchant'], 'Fuel'),
          ('The field', ['spread on', 'grass or crops'], 'N₂O and ammonia')]
    bw, gap, x0, y = 118, 16, 20, 120
    for i, (t, ls, em) in enumerate(st):
        x = x0 + i * (bw + gap)
        field = i == 6
        b += f'<rect x="{x}" y="{y}" width="{bw}" height="92" rx="8" fill="{TINT if field else "#fff"}" stroke="{RED if field else INK}" stroke-width="1.6"/>'
        b += text(x + bw / 2, y + 24, t, 13, INK, weight='700') + text(x + bw / 2, y + 48, ls[0], 11.5, MUTED, extra="font-family=\"'IBM Plex Mono',monospace\"" if '→' in ls[1] else '') + text(x + bw / 2, y + 64, ls[1], 11.5, MUTED, extra="font-family=\"'IBM Plex Mono',monospace\"" if '→' in ls[1] else '')
        b += arr(x + bw / 2, y + 96, x + bw / 2, y + 140, 1, RED, 2)
        for j, ln in enumerate(wrap(em, 16)):
            b += text(x + bw / 2, y + 158 + j * 15, ln, 12, RED, weight='600')
        if i < 6:
            b += arr(x + bw + 2, y + 46, x + bw + gap - 2, y + 46, 0, INK, 1.8)
    # brackets
    def br(x1, x2, yy, lab, sub, col):
        return (f'<path d="M{x1} {yy} v-8 H{x2} v8" fill="none" stroke="{col}" stroke-width="2.5"/>' + text((x1 + x2) / 2, yy - 16, lab, 13, col, weight='700')
                + (text((x1 + x2) / 2, yy - 32, sub, 11.5, MUTED) if sub else ''))
    xs = x0 + (bw + gap)
    xe = x0 + 5 * (bw + gap) - gap
    b += br(xs, xe, 108, 'Counted by CBAM: emissions at the plants (CO₂, N₂O); EU CBAM also counts electricity', '', RED)
    b += f'<path d="M{x0} 360 v8 H{x0 + 7*(bw+gap) - gap} v-8" fill="none" stroke="{INK}" stroke-width="2.5"/>'
    b += text(x0 + (7 * (bw + gap) - gap) / 2, 388, 'Cradle to field: what a farm or food carbon footprint should include', 13, INK, weight='700')
    b += text(20, 430, 'Neither CBAM counts methane leaks in gas supply or anything that happens on the field.', 12, MUTED, 'start')
    b += text(20, 448, 'EU CBAM also counts the electricity used (indirect emissions) for fertilisers; UK CBAM counts direct emissions only from 1 January 2027.', 12, MUTED, 'start')
    svg('fertiliser-life-cycle.svg', w, h, 'The life cycle of nitrogen fertiliser and what CBAM counts',
        'Seven stages left to right: natural gas, with methane leaks in supply; hydrogen made by steam reforming, releasing the most CO2; ammonia made by Haber–Bosch, needing energy; nitric acid, which releases nitrous oxide unless abated; '
        'ammonium nitrate, CAN or urea, using electricity; shipping and haulage, using fuel; and the field, where nitrous oxide and ammonia are released. '
        'The carbon border taxes count the emissions at the production plants, from hydrogen to finished fertiliser, for CO2 and nitrous oxide; EU CBAM also counts electricity, UK CBAM direct emissions only. Neither counts methane leaks in gas supply or emissions on the field. A farm or food footprint should include all seven stages.', b)


def fertiliser_regions():
    w, h = 900, 380
    L, R = 270, 840
    mx = 12
    X = lambda v: L + v / mx * (R - L)
    b = text(20, 30, 'Same bag, different footprint: ammonium nitrate by where it was made', 20, INK, 'start', '700')
    b += text(20, 52, 'kg CO₂e per kg of nitrogen, cradle to gate. Industry-published figures from 2013–14 data: the gap matters more than the exact values.', 13, MUTED, 'start')
    data = [('European average', 3.32, RED), ('North America', 6.71, GREY), ('Russia and neighbours', 7.11, GREY), ('Middle East', 7.15, GREY), ('China (coal-based)', 10.88, INK)]
    for i, (lab, v, c) in enumerate(data):
        y = 80 + i * 48
        b += text(L - 12, y + 22, lab, 13.5, INK, 'end', '600')
        b += f'<rect x="{L}" y="{y+6}" width="{X(v)-L:.1f}" height="26" rx="4" fill="{c}"><title>{e(lab)}: {v}</title></rect>'
        b += text(X(v) + 8, y + 24, f'{v:.2f}', 13, INK, 'start', '700')
    for v in range(0, 13, 2):
        b += f'<line x1="{X(v):.1f}" y1="320" x2="{X(v):.1f}" y2="326" stroke="{INK}"/>' + text(X(v), 342, str(v), 12, INK)
    b += f'<line x1="{L}" y1="320" x2="{R}" y2="320" stroke="{INK}"/>'
    b += text(20, 370, 'The main difference: most European nitric acid plants now destroy their nitrous oxide; elsewhere many do not.', 12, MUTED, 'start')
    svg('fertiliser-by-region.svg', w, h, 'Carbon footprint of ammonium nitrate by region of production',
        'Kilograms of CO2 equivalent per kilogram of nitrogen, cradle to gate, from an industry-published study using 2013–14 data: European average 3.32; North America 6.71; Russia and neighbouring states 7.11; Middle East 7.15; China, coal-based, 10.88. '
        'The main difference is that most European nitric acid plants abate their nitrous oxide.', b)

# ---------------------------------------------------------------- carbon capture

def storage_durations():
    w, h = 960, 500
    L, R = 300, 920
    lo, hi = 1, 5  # log10 years
    X = lambda yrs: L + (math.log10(yrs) - lo) / (hi - lo) * (R - L)
    b = text(20, 30, 'How long does each method lock carbon away?', 20, INK, 'start', '700')
    b += text(20, 52, 'Typical storage time, years (log scale). Source: IPCC AR6 Working Group III factsheet on carbon dioxide removal.', 13, MUTED, 'start')
    rows = [('Trees and new woodland', 10, 300, GREEN, 'Natural'), ('Soil carbon on farms', 10, 300, GREEN, 'Natural'),
            ('Restored peat and wetlands', 10, 300, GREEN, 'Natural'), ('Biochar dug into soil', 100, 3000, '#6B4F3A', 'Engineered'),
            ('Rock weathering and mineralisation', 10000, 100000, INK, 'Engineered'), ('Bioenergy with CCS (BECCS)', 10000, 100000, RED, 'Engineered'),
            ('Direct air capture with storage', 10000, 100000, RED, 'Engineered')]
    for i, (lab, a, z, c, kind) in enumerate(rows):
        y = 85 + i * 50
        b += text(L - 12, y + 21, lab, 13, INK, 'end', '600')
        b += f'<rect x="{X(a):.1f}" y="{y+6}" width="{X(z)-X(a):.1f}" height="24" rx="4" fill="{c}" opacity="0.9"><title>{e(lab)}</title></rect>'
        if z >= 100000:
            b += f'<path d="M{X(z)-2:.1f} {y+6} l14 12 l-14 12 z" fill="{c}"/>'
    labels = [(10, 'decades'), (100, 'centuries'), (1000, 'millennia'), (10000, '10,000 years'), (100000, '100,000')]
    for v, t in labels:
        b += f'<line x1="{X(v):.1f}" y1="440" x2="{X(v):.1f}" y2="446" stroke="{INK}"/>' + text(X(v), 462, t, 12, INK)
        b += f'<line x1="{X(v):.1f}" y1="80" x2="{X(v):.1f}" y2="440" stroke="{RULE}"/>'
    b += f'<line x1="{L}" y1="440" x2="{R}" y2="440" stroke="{INK}"/>'
    b += text(20, 490, 'Natural stores (green) can be reversed by fire, felling, drainage or ploughing. Geological and mineral stores are close to permanent.', 12, MUTED, 'start')
    svg('storage-durations.svg', w, h, 'How long each carbon removal method stores carbon',
        'Typical storage times on a log scale: trees and new woodland, soil carbon and restored peat and wetlands, decades to centuries; biochar, centuries to millennia; '
        'rock weathering and mineralisation, bioenergy with carbon capture and storage, and direct air capture with geological storage, 10,000 years or more. Natural stores can be reversed by fire, felling, drainage or ploughing.', b)


def ab_vs_ad():
    w, h = 960, 470
    b = arrow_defs(INK, RED)
    b += text(20, 30, 'Absorption or adsorption? Two ways to catch CO₂', 20, INK, 'start', '700')
    b += text(20, 52, 'Absorption takes the gas into the whole liquid. Adsorption holds it on the surface of a solid.', 13, MUTED, 'start')
    # left panel: liquid
    x0 = 20
    b += f'<rect x="{x0}" y="70" width="450" height="380" rx="8" fill="{TINT}" stroke="{RED}" stroke-width="1.5"/>'
    b += text(x0 + 225, 96, 'Absorption: like a sponge', 16, INK, weight='700')
    b += f'<rect x="{x0+60}" y="130" width="330" height="150" rx="6" fill="#dde6ee" stroke="{BLUE}"/>'
    b += text(x0 + 225, 150, 'Amine solvent, about 40 °C', 12, BLUE, weight='700')
    import random
    rnd = random.Random(3)
    for k in range(26):
        cx, cy = x0 + 80 + rnd.random() * 290, 165 + rnd.random() * 100
        b += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="{RED}" opacity="0.85"/>'
    b += text(x0 + 225, 305, '2 RNH₂ + CO₂ ⇌ RNHCOO⁻ + RNH₃⁺', 13, INK, weight='600', extra="font-family=\"'IBM Plex Mono',monospace\"")
    b += text(x0 + 225, 325, 'amine + CO₂ → carbamate', 12, MUTED)
    b += text(x0 + 225, 360, 'Heat to 100–120 °C and the CO₂ comes back out,', 12.5, INK)
    b += text(x0 + 225, 378, 'pure enough to compress and store.', 12.5, INK)
    b += text(x0 + 225, 410, 'Used in gas processing and power stations; now coming to cement.', 12.5, MUTED)
    b += text(x0 + 225, 428, 'The heat is the cost: a 10–40% energy penalty.', 12.5, RED, weight='600')
    # right panel: solid surface
    x1 = 490
    b += f'<rect x="{x1}" y="70" width="450" height="380" rx="8" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
    b += text(x1 + 225, 96, 'Adsorption: like Velcro', 16, INK, weight='700')
    # porous solid
    b += f'<rect x="{x1+60}" y="200" width="330" height="80" fill="#e8e4df" stroke="{GREY}"/>'
    for k in range(7):
        px = x1 + 80 + k * 45
        b += f'<path d="M{px} 200 v40 h18 v-40" fill="#fff" stroke="{GREY}"/>'
        b += f'<circle cx="{px+9}" cy="{232}" r="5" fill="{RED}"/>'
        b += f'<circle cx="{px+9}" cy="{193}" r="5" fill="{RED}"/>'
    for k in range(6):
        b += f'<circle cx="{x1+100+k*50}" cy="{150 + (k%2)*18}" r="5" fill="{RED}" opacity="0.5"/>'
    b += text(x1 + 225, 135, 'CO₂ in the passing air', 12, MUTED)
    b += text(x1 + 225, 300, 'Porous solid: zeolite, metal–organic framework,', 12, INK)
    b += text(x1 + 225, 316, 'or silica coated with amines', 12, INK)
    b += text(x1 + 225, 360, 'CO₂ sticks to the inner surfaces. Release it with', 12.5, INK)
    b += text(x1 + 225, 378, 'heat, a vacuum or a pressure drop.', 12.5, INK)
    b += text(x1 + 225, 410, 'Used in many direct air capture machines.', 12.5, MUTED)
    b += text(x1 + 225, 428, 'Huge surface in a small space: a gram can hide a football pitch.*', 12.5, MUTED)
    b += text(940, 465, '* Typical of the most porous frameworks; varies widely.', 10.5, MUTED, 'end')
    svg('absorption-vs-adsorption.svg', w, h, 'Absorption and adsorption compared',
        'Left, absorption: carbon dioxide dissolves into a liquid amine solvent at about 40 °C and reacts, 2 RNH2 plus CO2 giving a carbamate; heating to 100 to 120 °C releases pure CO2 for storage. '
        'Used in gas processing and power stations and now coming to cement, with a 10 to 40% energy penalty. Right, adsorption: carbon dioxide sticks to the inner surfaces of a porous solid such as a zeolite, a metal–organic framework or amine-coated silica, '
        'and is released by heat, vacuum or a pressure drop. Used in many direct air capture machines.', b)


def carbonate_cycle():
    nodes = [('Limestone CaCO₃', 'shells and corals', 'turned to rock', False),
             ('Kiln: lime and cement', 'CaCO₃ → CaO + CO₂', '0.52 t CO₂ per t clinker', True),
             ('Mortar and concrete', 'slowly re-absorb CO₂', 'Ca(OH)₂ + CO₂ → CaCO₃', False),
             ('Captured CO₂ in rock', 'basalt + CO₂ + water', '→ carbonate in <2 years', True)]
    cycle('carbonate-cycle.svg', 'Turning carbon back into stone', 'The carbonate cycle links seashells, cement kilns, lime mortar and the newest way to store CO₂: mineralisation.',
          nodes, ['Carbonate minerals', 'made, broken and', 'made again'],
          'A four-step cycle. Limestone, calcium carbonate made from ancient shells and corals, is heated in a kiln to make lime and cement, releasing CO2: CaCO3 gives CaO plus CO2, about 0.52 tonnes of CO2 per tonne of clinker. '
          'Lime mortar and concrete slowly re-absorb some CO2 as calcium hydroxide turns back into calcium carbonate. Captured CO2 pumped into basalt with water turns into carbonate rock in under two years, as at CarbFix in Iceland, and so back to stone.',
          w=900, h=600, cx=450, cy=330, R=190)


# ---------------------------------------------------------------- offsets

def offset_cycle():
    nodes = [('Project starts', 'trees planted, bog', 'rewetted, stoves sold', False),
             ('Validated', 'checked against a code', 'before any claim', False),
             ('Pending units', 'a promise of future', 'carbon (WCC: PIUs)', True),
             ('Verified units', 'carbon measured on', 'the ground', False),
             ('Retired and claimed', 'one tonne, used once,', 'by one buyer', False),
             ('Monitored for decades', 'fire, felling, drainage', 'can reverse it', True)]
    cycle('offset-life-cycle.svg', 'The life cycle of a carbon credit', 'From project to claim, and why the story does not end when you buy it.',
          nodes, ['20% buffer pool', 'set aside to cover', 'losses (UK codes)'],
          'A six-step cycle: a project starts, such as planting trees or rewetting a bog; it is validated against a code; it issues pending units, a promise of future carbon; '
          'carbon is measured and pending units become verified units; a buyer retires them and makes a claim, each tonne used once; the project is monitored for decades because fire, felling or drainage can reverse it. '
          'Under the UK Woodland Carbon Code and Peatland Code 20% of units go into a buffer pool to cover losses.',
          w=900, h=640, cx=450, cy=345, R=215)


def offset_ladder():
    w, h = 960, 560
    b = text(20, 30, 'Offsets: the good, the ugly and the harmful', 20, INK, 'start', '700')
    b += text(20, 52, 'A quality ladder. Higher rungs are more likely to be real, extra and lasting. Evidence from the studies cited on the page.', 13, MUTED, 'start')
    rungs = [('Durable removals', 'Direct air capture, BECCS, mineralisation', 'Stored for 10,000+ years; expensive and scarce', GREEN, 'Good'),
             ('Verified UK woodland and peat units', 'Woodland Carbon Code, Peatland Code', 'Checked on site by verifiers; 20% buffer; lasts decades to centuries', GREEN, 'Good'),
             ('Pending UK units', 'Promises of future carbon', 'Cannot yet be used to report emissions', '#B0A060', 'Ugly'),
             ('Renewable energy credits', 'Wind and solar abroad', 'Often built anyway; not eligible for the ICVCM quality label', '#C98B3A', 'Ugly'),
             ('Over-credited avoidance', 'Some forest protection (REDD+) and cookstove credits', 'Studies: about 6% of REDD+ credits real; cookstoves over-credited about 9 times', RED, 'Harmful')]
    for i, (t, ex, ev, c, tag) in enumerate(rungs):
        y = 80 + i * 92
        inset = i * 36
        b += f'<rect x="{20+inset}" y="{y}" width="{920-2*inset}" height="78" rx="8" fill="#fff" stroke="{c}" stroke-width="2.5"/>'
        b += f'<rect x="{20+inset}" y="{y}" width="96" height="78" rx="8" fill="{c}"/>'
        b += text(68 + inset, y + 45, tag, 15, '#fff', weight='700')
        b += text(132 + inset, y + 26, t, 15, INK, 'start', '700')
        b += text(132 + inset, y + 46, ex, 12.5, MUTED, 'start')
        b += text(132 + inset, y + 64, ev, 12.5, INK, 'start')
    svg('offset-quality-ladder.svg', w, h, 'A quality ladder for carbon offsets',
        'Five rungs from best to worst. Good: durable removals such as direct air capture, bioenergy with carbon capture and mineralisation, stored for 10,000 years or more but expensive and scarce. '
        'Good: verified UK woodland and peat units, checked on site by independent verifiers with a 20% buffer, lasting decades to centuries. Ugly: pending UK units, promises of future carbon that cannot yet be used to report emissions. '
        'Ugly: renewable energy credits, often for projects that would have been built anyway and not eligible for the ICVCM quality label. '
        'Harmful: over-credited avoidance credits; studies found about 6% of REDD+ forest credits represented real reductions and cookstove credits were over-credited about nine times.', b)


def wcc_units():
    w, h = 900, 300
    b = text(20, 30, 'UK woodland carbon: promised versus delivered', 20, INK, 'start', '700')
    b += text(20, 52, 'Units on the UK Land Carbon Registry at 31 March 2026 (Woodland Carbon Code statistics).', 13, MUTED, 'start')
    L, W = 230, 640
    mx = 14_171_000
    for i, (lab, v, c, note) in enumerate([('Pending Issuance Units', 14_171_000, GREY, '14,171,000: a promise of future carbon'),
                                           ('Woodland Carbon Units', 12_700, GREEN, '12,700: verified, usable now')]):
        y = 90 + i * 80
        b += text(L - 12, y + 26, lab, 14, INK, 'end', '700')
        ww = max(W * v / mx, 2)
        b += f'<rect x="{L}" y="{y}" width="{ww:.1f}" height="40" rx="4" fill="{c}"/>'
        b += text(L + (ww + 10 if ww < 300 else 14), y + 26, note, 13, '#fff' if ww > 300 else INK, 'start', '700')
    b += text(20, 270, 'Fewer than 1 in 1,000 units is verified. Only verified units can be counted against UK emissions today.', 13, RED, 'start', '700')
    svg('woodland-units.svg', w, h, 'Pending against verified UK woodland carbon units',
        'At 31 March 2026 the UK Land Carbon Registry held 14,171,000 Pending Issuance Units, promises of future carbon, against 12,700 verified Woodland Carbon Units. Fewer than one in a thousand units is verified; only verified units can be counted against UK emissions.', b)

if __name__ == '__main__':
    hydrogen_routes(); hydrogen_intensity(); hydrogen_leak()
    nitrogen_cycle(); fertiliser_chain(); fertiliser_regions()
    storage_durations(); ab_vs_ad(); carbonate_cycle()
    offset_cycle(); offset_ladder(); wcc_units()
    print('ok')
