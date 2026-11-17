"""Diagrams for Learn Batch B (v0.37.0, 17 Nov 2026): peat, permafrost, Lough Neagh and cyanobacteria, acid rain to acid seas.
Usage: python3 _scripts/learn/batch_b.py <repo_root>
Reuses helpers from gases.py and batch_a.py. Figures are from the research notes cited on each page.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gases import svg, text, e, RED, INK, GREY, MUTED, RULE, TINT  # noqa: E402
from batch_a import arrow_defs, arr, wrap, cycle, BLUE, GREEN  # noqa: E402

BROWN = '#6B4F3A'
MONO = "font-family=\"'IBM Plex Mono',monospace\""


def panel(x, y, w, h, title, sub='', hot=False):
    b = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{TINT if hot else "#fff"}" stroke="{RED if hot else INK}" stroke-width="1.5"/>'
    b += text(x + w / 2, y + 24, title, 15, INK, weight='700')
    if sub:
        b += text(x + w / 2, y + 42, sub, 12, MUTED)
    return b


def lines(x, y, rows, size=12.5, lh=18, col=INK, anchor='middle', mono=False):
    out = ''
    for i, r in enumerate(rows):
        out += text(x, y + i * lh, r, size, col, anchor, extra=MONO if mono else '')
    return out


# ---------------------------------------------------------------- peat

def peat_wet_dry():
    w, h = 960, 560
    b = arrow_defs(INK, RED, BLUE, GREEN)
    b += text(20, 30, 'A wet bog stores carbon; a drained bog breathes it out', 20, INK, 'start', '700')
    b += text(20, 52, 'The water table decides which microbes win, and so which gas leaves the peat.', 13, MUTED, 'start')
    for k, (x, title, hot) in enumerate([(20, 'Wet, intact bog', False), (490, 'Drained bog', True)]):
        b += panel(x, 70, 450, 470, title, '', hot)
        # sky / surface
        gx = x + 25
        surf = 170
        b += f'<rect x="{gx}" y="{surf}" width="400" height="250" fill="#5a4636" opacity="0.18"/>'
        wt = surf + (12 if k == 0 else 120)
        b += f'<rect x="{gx}" y="{wt}" width="400" height="{surf+250-wt}" fill="{BLUE}" opacity="0.18"/>'
        b += f'<line x1="{gx}" y1="{wt}" x2="{gx+400}" y2="{wt}" stroke="{BLUE}" stroke-width="2" stroke-dasharray="6 4"/>'
        b += text(gx + 396, wt - 6, 'water table', 11.5, BLUE, 'end', '700')
        # moss tufts
        for i in range(10):
            mx = gx + 20 + i * 40
            col = GREEN if k == 0 else '#9a9a6a'
            b += f'<path d="M{mx} {surf} q4 -18 8 0 q4 -14 8 0" fill="none" stroke="{col}" stroke-width="3"/>'
        if k == 0:
            b += arr(gx + 80, 110, gx + 80, surf - 10, 3, GREEN, 2.5) + text(gx + 92, 128, 'CO₂ taken in by Sphagnum moss', 12, GREEN, 'start', '700')
            b += arr(gx + 300, surf - 4, gx + 300, 110, 1, RED, 1.5) + text(gx + 312, 128, 'a little methane', 12, RED, 'start')
            b += lines(gx + 200, 250, ['No oxygen below the water:', 'dead moss barely rots'], 13)
            b += lines(gx + 200, 300, ['Methane-making microbes, slowly:', 'CO₂ + 4H₂ → CH₄ + 2H₂O'], 12.5, mono=False)
            b += lines(gx + 200, 360, ['Peat builds up about 1 mm a year'], 13, col=INK)
            b += text(x + 225, 455, 'Net result', 13, INK, weight='700')
            b += text(x + 225, 475, 'a slow, steady carbon store', 13, GREEN, weight='700')
            b += text(x + 225, 500, 'over thousands of years', 12, MUTED)
        else:
            b += arr(gx + 120, surf - 4, gx + 120, 100, 1, RED, 4) + text(gx + 134, 118, 'CO₂ from rotting peat', 12.5, RED, 'start', '700')
            b += arr(gx + 330, surf + 30, gx + 330, surf + 220, 1, BROWN, 3) + text(gx + 322, surf + 240, 'brown water (dissolved carbon)', 11.5, BROWN, 'end', '700')
            b += lines(gx + 170, 215, ['Air gets in above the water table:'], 13)
            b += lines(gx + 170, 238, ['(CH₂O)ₙ + nO₂ → nCO₂ + nH₂O'], 12.5, mono=True)
            b += lines(gx + 170, 262, ['peat oxidises and the ground sinks'], 12.5, col=MUTED)
            b += lines(gx + 170, 330, ['Dry peat can burn'], 12.5, col=RED)
            b += text(x + 225, 455, 'Net result', 13, INK, weight='700')
            b += text(x + 225, 475, 'a carbon source, year after year', 13, RED, weight='700')
            b += text(x + 225, 500, 'until it is rewetted', 12, MUTED)
    svg('peat-wet-vs-drained.svg', w, h, 'Wet and drained peat compared',
        'Two panels. A wet, intact bog: the water table sits at the surface, Sphagnum moss takes in CO2, dead moss barely rots without oxygen, a little methane is made (CO2 plus hydrogen gives methane and water), and peat builds up about a millimetre a year: a slow carbon store. '
        'A drained bog: air gets in above a lowered water table, peat oxidises (carbohydrate plus oxygen gives CO2 and water), the ground sinks, dissolved carbon leaves as brown water, and dry peat can burn: a carbon source until it is rewetted.', b)


def peat_cycle():
    nodes = [('Moss grows', 'Sphagnum takes in', 'CO₂ from the air', False),
             ('Dies, stays wet', 'no oxygen, acid', 'water: barely rots', False),
             ('Peat builds up', 'about 1 mm a year,', 'metres over millennia', False),
             ('Drain, dig or burn', 'oxygen gets in:', 'thousands of years of', True),
             ]
    cycle('peat-life-cycle.svg', 'The life cycle of a bog', 'Peat is made slowly and lost quickly. Rewetting closes the loop and lets the moss grow again.',
          nodes, ['Rewet it', 'raise the water table', 'and the moss returns'],
          'A loop. Sphagnum moss grows and takes in CO2. It dies and stays wet, so with no oxygen and acid water it barely rots. Peat builds up about a millimetre a year, metres over thousands of years. '
          'Draining, cutting or burning lets oxygen in and releases thousands of years of carbon in decades. Rewetting raises the water table and lets the moss return.',
          w=900, h=580, cx=450, cy=320, R=185)
    # patch the 4th node's third line
    p = os.path.join(sys.argv[1] if len(sys.argv) > 1 else '.', 'assets/learn/peat-life-cycle.svg')
    s = open(p, encoding='utf-8').read().replace('thousands of years of</text>', 'carbon out in decades</text>')
    open(p, 'w', encoding='utf-8').write(s)


# ---------------------------------------------------------------- permafrost

def permafrost_feedback():
    nodes = [('Warmer Arctic', 'warming faster than', 'the world as a whole', True),
             ('Permafrost thaws', 'deeper active layer,', 'collapsing ground', False),
             ('Old carbon rots', 'with air: CO₂', 'without air: methane', True),
             ('More greenhouse gas', 'adds to warming', 'everywhere', False)]
    cycle('permafrost-feedback.svg', 'The permafrost carbon feedback', 'A feedback: warming thaws carbon that causes more warming. Real and irreversible for centuries, but not “runaway” (IPCC).',
          nodes, ['Feedback', 'warming causes', 'more warming'],
          'A four-step feedback loop. A warmer Arctic, warming faster than the global average, thaws permafrost, deepening the active layer and collapsing the ground. Thousands of years of frozen plant carbon starts to rot: with air it gives CO2, without air methane. '
          'The extra greenhouse gas adds to warming everywhere, which thaws more permafrost.',
          w=900, h=560, cx=450, cy=310, R=175)


def permafrost_vs_ice():
    w, h = 960, 440
    b = text(20, 30, 'Ice caps or permafrost: which is worse?', 20, INK, 'start', '700')
    b += text(20, 52, 'They do different damage. Ice sheets raise the sea; permafrost adds carbon to the air.', 13, MUTED, 'start')
    rows = [('', 'Ice sheets (Greenland, Antarctica)', 'Permafrost'),
            ('What melts', 'Ice on land, kilometres thick', 'Frozen soil full of old plants'),
            ('Main harm', 'Sea-level rise', 'CO₂ and methane: more warming'),
            ('Carbon released', 'Almost none', 'Billions of tonnes, over centuries'),
            ('Speed', 'Centuries to millennia', 'Gradual, plus sudden collapses'),
            ('Can it be undone?', 'Not on human timescales', 'Not on human timescales'),
            ('Worse for…', 'coasts and cities', 'the carbon budget')]
    cx = [20, 230, 600]
    cw = [210, 370, 340]
    for i, r in enumerate(rows):
        y = 75 + i * 50
        fill = '#f4f4f4' if i == 0 else ('#fff' if i % 2 else '#faf9f8')
        for j in range(3):
            hot = (j == 2 and i in (3, 6))
            b += f'<rect x="{cx[j]}" y="{y}" width="{cw[j]-4}" height="46" fill="{TINT if hot else fill}" stroke="{RED if hot else RULE}"/>'
            b += text(cx[j] + 12, y + 28, r[j], 13.5 if i == 0 or j == 0 else 13, INK if (i == 0 or j == 0) else (RED if hot else INK), 'start', '700' if (i == 0 or j == 0 or hot) else '400')
    svg('ice-vs-permafrost.svg', w, h, 'Ice sheets and permafrost compared',
        'A comparison table. Ice sheets in Greenland and Antarctica are ice on land kilometres thick; melting them raises the sea, releases almost no carbon, takes centuries to millennia and is worse for coasts and cities. '
        'Permafrost is frozen soil full of old plant remains; thawing it releases CO2 and methane, billions of tonnes over centuries, gradually and in sudden collapses, and is worse for the carbon budget. Neither can be undone on human timescales.', b)


# ---------------------------------------------------------------- Lough Neagh

def phosphorus_cycle():
    w, h = 960, 600
    b = arrow_defs(INK, RED, BLUE, GREEN)
    b += text(20, 30, 'How phosphorus feeds a bloom', 20, INK, 'start', '700')
    b += text(20, 52, 'Phosphorus is the nutrient that usually limits algae in fresh water. Too much of it, plus warm, still water, and cyanobacteria take over.', 13, MUTED, 'start')
    # land
    b += f'<rect x="20" y="80" width="380" height="250" rx="8" fill="#f7f3ee" stroke="{RULE}"/>'
    b += text(210, 104, 'The catchment', 15, INK, weight='700')
    b += lines(210, 134, ['Slurry, manure and fertiliser', 'Septic tanks and wastewater works', 'Phosphorus stored in soils for decades'], 13)
    b += text(210, 214, 'Phosphate binds to soil particles:', 12.5, MUTED)
    b += text(210, 234, 'it moves when soil washes off fields', 12.5, MUTED)
    b += text(210, 254, 'or when soils are saturated with it', 12.5, MUTED)
    b += text(210, 300, 'PO₄³⁻ (phosphate)', 15, RED, weight='700', extra=MONO)
    # arrow to lough
    b += arr(400, 205, 520, 205, 1, RED, 3) + text(460, 195, 'runoff', 12, RED, weight='700') + text(460, 225, 'and rivers', 12, RED)
    # lough
    b += f'<rect x="520" y="80" width="420" height="380" rx="8" fill="#e6eef5" stroke="{BLUE}"/>'
    b += text(730, 104, 'The lough', 15, INK, weight='700')
    b += f'<rect x="540" y="120" width="380" height="60" rx="6" fill="#7aa34a" opacity="0.75"/>'
    b += text(730, 147, 'Bloom: cyanobacteria at the surface', 13, '#fff', weight='700')
    b += text(730, 166, 'shade out other plants; some make toxins', 12, '#fff')
    b += lines(730, 210, ['Warm, calm, sunny water lets them float up', 'Some fix their own nitrogen from the air'], 12.5)
    b += arr(730, 255, 730, 330, 0, INK, 2) + text(742, 290, 'they die and sink', 12, MUTED, 'start')
    b += f'<rect x="540" y="340" width="380" height="100" rx="6" fill="#5a4636" opacity="0.25"/>'
    b += text(730, 362, 'Bed sediment', 13, INK, weight='700')
    b += lines(730, 384, ['Rotting uses up the oxygen', 'Without oxygen, iron lets go of phosphate:', 'FePO₄ + e⁻ → Fe²⁺ + PO₄³⁻ (simplified)'], 12)
    b += f'<path d="M920 390 C 960 330, 960 210, 922 160" fill="none" stroke="{RED}" stroke-width="2.5" stroke-dasharray="6 4" marker-end="url(#a1)"/>'
    b += text(944, 470, 'internal loading:', 11.5, RED, 'end', '700') + text(944, 486, 'the lough feeds itself', 11.5, RED, 'end')
    # bottom note
    b += f'<rect x="20" y="350" width="380" height="230" rx="8" fill="#fff" stroke="{RULE}"/>'
    b += text(210, 374, 'Making it worse', 14, INK, weight='700')
    b += lines(210, 400, ['Warmer summers', 'Clearer water from zebra mussels', '(more light reaches the algae)', 'Legacy phosphorus in fields and mud', 'Wastewater works at capacity'], 12.5, lh=22)
    b += text(730, 520, 'Cut the phosphorus coming in, and wait:', 13, INK, weight='700')
    b += text(730, 540, 'the mud keeps releasing it for years.', 13, INK)
    svg('phosphorus-bloom-cycle.svg', w, h, 'How phosphorus feeds a cyanobacteria bloom',
        'Phosphate from slurry, manure, fertiliser, septic tanks and wastewater, and from phosphorus stored in soils, washes into the lough with soil and runoff. In warm, calm, sunny water cyanobacteria float to the surface as a bloom, shading out other plants; some make toxins and some fix their own nitrogen. '
        'When they die and sink, rotting uses up the oxygen near the bed, and without oxygen iron releases its phosphate back into the water, so the lough feeds itself. Warmer summers, clearer water from zebra mussels, legacy phosphorus and overloaded wastewater works make it worse. '
        'Cutting the phosphorus coming in works, but the mud keeps releasing it for years.', b)


def cyano_timeline():
    w, h = 960, 330
    b = text(20, 30, 'Cyanobacteria: the bacteria that made our air', 20, INK, 'start', '700')
    b += text(20, 52, 'Billions of years of history, from the first oxygen to this decade’s blooms. Not to scale.', 13, MUTED, 'start')
    L, R, y = 50, 910, 170
    b += f'<line x1="{L}" y1="{y}" x2="{R}" y2="{y}" stroke="{INK}" stroke-width="3"/>'
    ev = [(L, 'About 3 billion years ago or more', ['First to split water', 'and release oxygen'], GREEN, -1),
          (L + 190, 'About 2.4 billion years ago', ['The Great Oxidation Event:', 'oxygen builds up in the air'], GREEN, 1),
          (L + 380, 'Much later', ['Swallowed by other cells:', 'they become chloroplasts'], GREEN, -1),
          (L + 570, 'Today', ['Make oxygen, fix nitrogen,', 'feed lake and ocean food webs'], GREEN, 1),
          (R, 'Since 2023', ['Toxic blooms on', 'Lough Neagh'], RED, -1)]
    for x, t, ls, c, d in ev:
        b += f'<circle cx="{x}" cy="{y}" r="9" fill="{c}"/>'
        ty = y - 70 if d < 0 else y + 40
        anc = 'start' if x == L else ('end' if x == R else 'middle')
        b += text(x, ty, t, 13, c, anc, '700') + text(x, ty + 19, ls[0], 12, INK, anc) + text(x, ty + 35, ls[1], 12, INK, anc)
    b += text(20, 315, 'Ages are approximate and debated by geologists; see the page for sources.', 11.5, MUTED, 'start')
    svg('cyanobacteria-timeline.svg', w, h, 'A short history of cyanobacteria',
        'A timeline. About 3 billion years ago or more cyanobacteria became the first organisms to split water and release oxygen. About 2.4 billion years ago the Great Oxidation Event saw oxygen build up in the air. Later they were swallowed by other cells and became chloroplasts, the green engines of plants. '
        'Today they make oxygen, fix nitrogen and feed lake and ocean food webs. Since 2023 they have formed toxic blooms on Lough Neagh.', b)


# ---------------------------------------------------------------- acid seas

def carbonate_chem():
    w, h = 960, 520
    b = arrow_defs(INK, RED, BLUE)
    b += text(20, 30, 'What CO₂ does to seawater', 20, INK, 'start', '700')
    b += text(20, 52, 'The second and third steps release hydrogen ions (H⁺). More H⁺ means lower pH and fewer carbonate ions for shells.', 13, MUTED, 'start')
    b += f'<rect x="20" y="70" width="920" height="70" rx="8" fill="#f1f4f7" stroke="{RULE}"/>'
    b += text(480, 112, 'CO₂ in the air  ⇌  CO₂ dissolved in the sea', 16, INK, weight='700')
    b += arr(480, 140, 480, 170, 0, INK, 2)
    boxes = [(30, 'Carbonic acid', 'CO₂ + H₂O ⇌ H₂CO₃'), (340, 'Bicarbonate', 'H₂CO₃ ⇌ H⁺ + HCO₃⁻'), (650, 'Carbonate', 'HCO₃⁻ ⇌ H⁺ + CO₃²⁻')]
    for i, (x, t, eq) in enumerate(boxes):
        b += f'<rect x="{x}" y="175" width="280" height="90" rx="8" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
        b += text(x + 140, 202, t, 14, INK, weight='700') + text(x + 140, 232, eq, 14, INK, extra=MONO)
        if i < 2:
            b += arr(x + 284, 220, x + 306, 220, 0, INK, 2)
        if i > 0:
            b += text(x + 140, 255, 'releases H⁺', 12, RED, weight='700')
    # the squeeze
    b += f'<rect x="20" y="290" width="450" height="210" rx="8" fill="{TINT}" stroke="{RED}" stroke-width="1.5"/>'
    b += text(245, 316, 'The squeeze on shells', 15, INK, weight='700')
    b += lines(245, 344, ['Extra H⁺ grabs carbonate ions:', 'H⁺ + CO₃²⁻ → HCO₃⁻'], 13)
    b += lines(245, 400, ['Less carbonate is left to build shells:', 'Ca²⁺ + CO₃²⁻ → CaCO₃'], 13)
    b += text(245, 460, 'Oysters, mussels, sea snails and corals pay', 12.5, RED, weight='700')
    b += text(245, 480, 'more energy to build, or their shells thin', 12.5, RED)
    b += f'<rect x="490" y="290" width="450" height="210" rx="8" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
    b += text(715, 316, 'Acid rain and acid seas compared', 15, INK, weight='700')
    b += lines(715, 344, ['Acid rain: sulphur and nitrogen oxides', 'SO₂ → H₂SO₄, NOx → HNO₃', 'Local, fast, and largely fixed'], 12.5, lh=19)
    b += lines(715, 416, ['Acid seas: carbon dioxide', 'CO₂ → H₂CO₃', 'Global, slow, and still rising'], 12.5, lh=19)
    b += text(715, 485, 'The sea is not acid: it is becoming less alkaline.', 12, MUTED)
    svg('ocean-carbonate-chemistry.svg', w, h, 'Ocean acidification chemistry',
        'Carbon dioxide dissolves into seawater and forms carbonic acid (CO2 plus H2O), which splits into bicarbonate and a hydrogen ion, and bicarbonate into carbonate and another hydrogen ion. '
        'The extra hydrogen ions combine with carbonate ions to make more bicarbonate, leaving less carbonate for shell-building (calcium plus carbonate gives calcium carbonate), so oysters, mussels, sea snails and corals must spend more energy or their shells thin. '
        'Compared with acid rain, which came from sulphur and nitrogen oxides, was local and fast and has largely been fixed, ocean acidification comes from CO2, is global and slow, and is still rising. The sea is not acid; it is becoming less alkaline.', b)


def ocean_feedbacks():
    nodes = [('More CO₂ and heat', 'from burning fossil', 'fuels', True),
             ('Ice melts', 'white ice reflects most', 'sunlight; dark sea absorbs it', False),
             ('Fresh water floods in', 'melting ice dilutes', 'the North Atlantic', False),
             ('Circulation may slow', 'less salty water sinks', 'less readily', True),
             ('Seas warm and stratify', 'layers stop mixing;', 'blooms, less oxygen', False),
             ('Seas absorb less CO₂', 'warm water holds', 'less gas', True)]
    cycle('ocean-feedbacks.svg', 'From melting ice to a slower ocean', 'Linked feedbacks in the North Atlantic. Each is expected; how far and how fast they go is still being studied.',
          nodes, ['Ocean feedbacks', 'warming changes', 'the sea, which', 'changes warming'],
          'A six-step loop. More CO2 and heat melt sea ice; white ice reflects most sunlight while dark sea absorbs it. Melting ice adds fresh water that dilutes the North Atlantic, and less salty water sinks less readily, so the overturning circulation is projected to slow. '
          'Seas warm and stratify, so layers stop mixing, with more blooms and less oxygen. Warmer water holds less gas, so the sea absorbs less CO2, adding to warming.',
          w=900, h=640, cx=450, cy=345, R=215)


def permafrost_stock():
    w, h = 900, 330
    L, W = 300, 480
    mx = 1600
    b = text(20, 30, 'Where the carbon is: permafrost soils against the air', 20, INK, 'start', '700')
    b += text(20, 52, 'Billions of tonnes of carbon (GtC). Permafrost region from NOAA and Hugelius et al.; atmosphere from the Global Carbon Budget 2025.', 13, MUTED, 'start')
    rows = [('Permafrost-region soils', 1300, 1600, BROWN, '1,300–1,600'), ('of which permanently frozen', 800, 800, '#9c7f66', 'about 800'), ('The whole atmosphere (2024)', 900, 900, BLUE, 'about 900')]
    for i, (lab, lo, hi, c, t) in enumerate(rows):
        y = 85 + i * 62
        b += text(L - 12, y + 25, lab, 14, INK, 'end', '700' if i != 1 else '400')
        b += f'<rect x="{L}" y="{y+6}" width="{W*lo/mx:.1f}" height="30" rx="4" fill="{c}"/>'
        if hi > lo:
            b += f'<rect x="{L+W*lo/mx:.1f}" y="{y+6}" width="{W*(hi-lo)/mx:.1f}" height="30" rx="4" fill="{c}" opacity="0.45"/>'
        b += text(L + W * hi / mx + 10, y + 27, t, 13.5, INK, 'start', '700')
    b += text(20, 290, 'Even a fraction of the frozen store, released as CO₂ and methane, would make a large dent in the remaining carbon budget.', 12.5, MUTED, 'start')
    b += text(20, 310, 'IPCC AR6: 3–41 billion tonnes of carbon released as CO₂ per °C of warming by 2100 (low confidence).', 12.5, RED, 'start', '600')
    svg('permafrost-carbon-stock.svg', w, h, 'Permafrost carbon compared with the atmosphere',
        'Bars in billions of tonnes of carbon: permafrost-region soils 1,300 to 1,600, of which about 800 is permanently frozen; the whole atmosphere in 2024 about 900. The IPCC projects 3 to 41 billion tonnes of carbon released as CO2 per degree of warming by 2100, with low confidence.', b)


def peat_fluxes():
    w, h = 900, 400
    L, W, mx = 260, 560, 30
    b = text(20, 30, 'One hectare of peat grassland: drained against rewetted', 20, INK, 'start', '700')
    b += text(20, 52, 'Tonnes CO₂e per hectare per year, IPCC 2013 Wetlands Supplement factors, AR5 GWPs. Illustrative arithmetic; real sites vary widely.', 13, MUTED, 'start')
    data = [('Drained (deep, nutrient-rich)', [(22.4, BROWN, 'CO₂ from rotting peat 22.4'), (2.05, RED, 'methane'), (3.4, '#D98C8C', 'N₂O'), (0.9, GREY, 'dissolved carbon')], 'about 29'),
            ('Rewetted', [(1.8, BROWN, 'CO₂'), (8.1, RED, 'methane 8.1'), (0.9, GREY, '')], 'about 11')]
    for i, (lab, parts, tot) in enumerate(data):
        y = 90 + i * 110
        b += text(L - 12, y + 28, lab, 14, INK, 'end', '700')
        x = L
        for v, c, t in parts:
            ww = W * v / mx
            b += f'<rect x="{x:.1f}" y="{y}" width="{ww:.1f}" height="44" fill="{c}"><title>{e(t or "dissolved carbon")}: {v}</title></rect>'
            if ww > 90 and t:
                b += text(x + ww / 2, y + 27, t, 12, '#fff', weight='700')
            x += ww
        b += text(x + 10, y + 28, tot, 15, INK, 'start', '700')
    # legend
    lx = L
    for t, c in [('CO₂ from the peat', BROWN), ('Methane', RED), ('Nitrous oxide', '#D98C8C'), ('Dissolved carbon (as CO₂)', GREY)]:
        b += f'<rect x="{lx}" y="318" width="12" height="12" fill="{c}"/>' + text(lx + 18, 329, t, 12, INK, 'start')
        lx += len(t) * 7 + 40
    b += text(20, 372, 'Rewetting cuts CO₂ sharply and adds some methane. The net saving here is about 18 t CO₂e per hectare a year.', 12.5, RED, 'start', '700')
    svg('peat-drained-vs-rewetted.svg', w, h, 'Emissions from drained and rewetted peat grassland',
        'Stacked bars, tonnes of CO2 equivalent per hectare per year, from IPCC 2013 Wetlands Supplement factors with AR5 GWPs, illustrative: deep-drained nutrient-rich peat grassland about 29, mostly CO2 from rotting peat (22.4) with some methane, nitrous oxide and dissolved carbon; '
        'rewetted about 11, with CO2 down to 1.8 but methane up to 8.1. Net saving about 18 tonnes per hectare a year.', b)


def ni_peat_inventory():
    w, h = 900, 300
    L, W, mx = 330, 470, 3
    b = text(20, 30, 'Northern Ireland, 2024: peat against all land use', 20, INK, 'start', '700')
    b += text(20, 52, 'Million tonnes CO₂e. NI inventory (DAERA and NISRA, 9 June 2026) and devolved inventory report: peat was 108% of net land use.', 13, MUTED, 'start')
    rows = [('Peatland emissions', 2.27, BROWN, 'about 2.3'), ('All land use, net (LULUCF)', 2.1, GREY, '2.1')]
    for i, (lab, v, c, t) in enumerate(rows):
        y = 85 + i * 64
        b += text(L - 12, y + 26, lab, 14, INK, 'end', '700')
        b += f'<rect x="{L}" y="{y+6}" width="{W*v/mx:.1f}" height="32" rx="4" fill="{c}"/>' + text(L + W * v / mx + 10, y + 28, t, 14, INK, 'start', '700')
    b += text(20, 236, 'Peat emits more than the whole land-use sector nets out to: forests and grassland soils absorb some, peat gives more back.', 12.5, INK, 'start')
    b += text(20, 258, 'That is about 12% of NI’s net emissions (my arithmetic: about 2.3 of 18.4).', 12.5, RED, 'start', '700')
    svg('ni-peat-inventory.svg', w, h, 'Northern Ireland peat emissions compared with the whole land-use sector',
        'In 2024 Northern Ireland peatlands emitted about 2.3 million tonnes of CO2 equivalent, 108% of the 2.1 million tonnes net for all land use, because forests and grassland soils absorb some carbon. Peat is about 12% of NI net emissions.', b)


def ln_sources():
    w, h = 900, 300
    L, W = 40, 820
    b = text(20, 30, 'Where Lough Neagh’s phosphorus comes from', 20, INK, 'start', '700')
    b += text(20, 52, 'Provisional source split for the Lough Neagh catchment, Lough Neagh Report and Action Plan (July 2024). Other models differ by a few points.', 13, MUTED, 'start')
    parts = [('Agriculture', 56, RED), ('Wastewater treatment works', 31, INK), ('Septic tanks', 1, '#D98C8C'), ('Other', 12, GREY)]
    x = L
    for name, pct, c in parts:
        ww = W * pct / 100
        b += f'<rect x="{x:.1f}" y="90" width="{max(ww-2,2):.1f}" height="60" fill="{c}"><title>{e(name)}: {pct}%</title></rect>'
        if ww > 90:
            b += text(x + ww / 2, 116, name, 13, '#fff', weight='700') + text(x + ww / 2, 136, f'{pct}%', 13, '#fff')
        x += ww
    b += f'<rect x="{L + W*0.87:.1f}" y="166" width="12" height="12" fill="#D98C8C"/>' + text(L + W * 0.87 + 18, 177, 'Septic tanks 1%', 12, INK, 'start')
    b += text(20, 220, 'A 2021 model gives 61% agriculture, 29% wastewater, 1.3% septic tanks, 9% other.', 12.5, INK, 'start')
    b += text(20, 242, 'Across all of Northern Ireland (2020 estimate) the split is 62% agriculture, 24% wastewater works, 12% septic tanks.', 12.5, INK, 'start')
    b += text(20, 270, 'Phosphorus already stored in soils and in the lough bed keeps feeding blooms for years after inputs fall.', 12.5, RED, 'start', '700')
    svg('lough-neagh-p-sources.svg', w, h, 'Sources of phosphorus reaching Lough Neagh',
        'Provisional split for the Lough Neagh catchment from the July 2024 Lough Neagh Report and Action Plan: agriculture 56%, wastewater treatment works 31%, septic tanks 1%, other sources such as forestry and urban areas 12%. '
        'A 2021 model gives 61, 29, 1.3 and 9%. Across all of Northern Ireland a 2020 estimate gives 62% agriculture, 24% wastewater works and 12% septic tanks. Stored phosphorus in soils and the lough bed keeps feeding blooms for years.', b)


def so2_fall():
    w, h = 900, 300
    L, W, mx = 200, 640, 7000
    b = text(20, 30, 'Acid rain: the problem we fixed', 20, INK, 'start', '700')
    b += text(20, 52, 'UK sulphur dioxide emissions, thousand tonnes. NAEI (1970) and Defra (2024).', 13, MUTED, 'start')
    for i, (lab, v, c) in enumerate([('1970', 6518, INK), ('2024', 84, GREEN)]):
        y = 85 + i * 64
        b += text(L - 12, y + 26, lab, 15, INK, 'end', '700')
        b += f'<rect x="{L}" y="{y+6}" width="{max(W*v/mx,3):.1f}" height="34" rx="4" fill="{c}"/>'
        b += text(L + max(W * v / mx, 3) + 10, y + 29, f'{v:,} kt', 14, INK, 'start', '700')
    b += text(20, 236, 'About a 99% fall (my arithmetic across two inventory editions; Defra reports 98% since 1990).', 12.5, INK, 'start')
    b += text(20, 258, 'How: less coal, low-sulphur fuels, scrubbers on power stations, and international treaties from 1979.', 12.5, GREEN, 'start', '700')
    svg('uk-so2-fall.svg', w, h, 'The fall in UK sulphur dioxide emissions',
        'UK sulphur dioxide emissions fell from 6,518 thousand tonnes in 1970 to 84 thousand tonnes in 2024, about 99%, through less coal, low-sulphur fuels, scrubbers and international treaties from 1979.', b)


def albedo():
    w, h = 900, 300
    L, W = 260, 560
    b = text(20, 30, 'Albedo: how much sunlight a surface reflects', 20, INK, 'start', '700')
    b += text(20, 52, 'Share of sunlight reflected (0 = none, 1 = all). Typical values; they vary with conditions.', 13, MUTED, 'start')
    rows = [('Open ocean', 0.06, 0.06, '#1f3b57', 'about 0.06'), ('Bare sea ice', 0.5, 0.7, '#9fb6c9', '0.5–0.7'), ('Snow-covered sea ice', 0.9, 0.9, '#dfe8ef', 'up to about 0.9')]
    for i, (lab, lo, hi, c, t) in enumerate(rows):
        y = 80 + i * 58
        b += text(L - 12, y + 24, lab, 14, INK, 'end', '700')
        b += f'<rect x="{L}" y="{y+6}" width="{max(W*hi,4):.1f}" height="30" rx="4" fill="{c}" stroke="{GREY}"/>'
        b += text(L + W * hi + 10, y + 27, t, 13.5, INK, 'start', '700')
    b += text(20, 270, 'Replace ice with open sea and the surface absorbs most of the sunlight it used to reflect: the ice–albedo feedback.', 12.5, RED, 'start', '700')
    svg('sea-ice-albedo.svg', w, h, 'Albedo of ocean and sea ice',
        'Typical albedo, the share of sunlight reflected: open ocean about 0.06; bare sea ice 0.5 to 0.7; snow-covered sea ice up to about 0.9. Replacing ice with open sea means most sunlight is absorbed instead of reflected.', b)


if __name__ == '__main__':
    peat_wet_dry(); peat_cycle(); peat_fluxes(); ni_peat_inventory()
    permafrost_feedback(); permafrost_vs_ice(); permafrost_stock()
    phosphorus_cycle(); cyano_timeline(); ln_sources()
    carbonate_chem(); ocean_feedbacks(); so2_fall(); albedo()
    print('ok')
