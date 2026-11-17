"""Diagrams for Learn Batch C (v0.38.0, 17 Nov 2026): walls (block, lime, brick, prefab), the circular economy,
fish guts and seashells, medicines and fossil fuels.
Usage: python3 _scripts/learn/batch_c.py <repo_root>
Reuses helpers from gases.py, batch_a.py and batch_b.py. Figures come from the research notes cited on each page.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gases import svg, text, e, RED, INK, GREY, MUTED, RULE, TINT  # noqa: E402
from batch_a import arrow_defs, arr, wrap, cycle, BLUE, GREEN  # noqa: E402
from batch_b import panel, lines, MONO  # noqa: E402

BROWN = '#7A5A3A'
SAND = '#C9B79C'


def hbars(name, title, sub, rows, mx, unit, desc, note='', w=900, L=330, W=440, rh=46, top=80, extra_h=60):
    """rows: (label, value, colour, value_text). Horizontal bars on one linear axis."""
    h = top + rh * len(rows) + extra_h
    b = text(20, 30, title, 20, INK, 'start', '700') + text(20, 52, sub, 13, MUTED, 'start')
    for i, (lab, v, c, t) in enumerate(rows):
        y = top + i * rh
        b += text(L - 12, y + 24, lab, 13.5, INK, 'end', '700')
        bw = max(W * v / mx, 2)
        b += f'<rect x="{L}" y="{y+6}" width="{bw:.1f}" height="28" rx="4" fill="{c}"/>'
        b += text(L + bw + 10, y + 26, t, 13.5, INK, 'start', '700')
    b += f'<line x1="{L}" y1="{top}" x2="{L}" y2="{top + rh*len(rows)}" stroke="{INK}" stroke-width="1"/>'
    b += text(L, top + rh * len(rows) + 18, unit, 12, MUTED, 'start')
    if note:
        for i, ln in enumerate(note if isinstance(note, list) else [note]):
            b += text(20, top + rh * len(rows) + 42 + i * 19, ln, 12.5, RED if i == 0 else INK, 'start', '700' if i == 0 else '400')
    svg(name, w, h, title, desc, b)


# ================================================================ walls

def lime_cycle():
    nodes = [('Limestone', 'CaCO₃, quarried', 'e.g. Antrim chalk', False),
             ('Burn in a kiln', 'about 900 °C', 'CaCO₃ → CaO + CO₂', True),
             ('Slake with water', 'quicklime to lime putty', 'CaO + H₂O → Ca(OH)₂', False),
             ('Mortar sets in air', 'takes CO₂ back slowly:', 'Ca(OH)₂+CO₂→CaCO₃+H₂O', True)]
    cycle('lime-cycle.svg', 'The lime cycle', 'Air lime goes back to the stone it came from. The fuel burned to heat the kiln is never paid back.',
          nodes, ['Back to stone', 'process CO₂ partly', 'reabsorbed over years'],
          'A four-step loop. Limestone, calcium carbonate, is quarried. It is burned in a kiln at about 900 degrees, giving quicklime, calcium oxide, and releasing CO2. '
          'Quicklime is slaked with water to give calcium hydroxide, lime putty. As lime mortar sets in air it slowly takes CO2 back and turns into calcium carbonate again. '
          'The process CO2 is partly reabsorbed over years; the fuel burned to heat the kiln is not.',
          w=900, h=580, cx=450, cy=320, R=185)


def cement_vs_lime():
    w, h = 960, 545
    b = arrow_defs(INK, RED, GREEN)
    b += text(20, 30, 'Cement, lime and fired clay: where the CO₂ comes from', 20, INK, 'start', '700')
    b += text(20, 52, 'Two sources in every kiln: the fuel that heats it, and (for cement and lime) the CO₂ driven out of the stone itself.', 13, MUTED, 'start')
    cols = [(20, 'Portland cement', 'for concrete block and mortar', [
        'Limestone + clay, heated to about 1,450 °C', 'CaCO₃ → CaO + CO₂', 'CaO reacts with clay to make clinker', 'Clinker ground with gypsum = cement'],
        ['Process CO₂ from the stone', 'plus fuel for the hottest kiln'], 'Sets by reacting with water.', 'Takes back only a fraction of its CO₂.', True),
        (335, 'Lime', 'for mortar, render, hempcrete', [
         'Limestone heated to about 900 °C', 'CaCO₃ → CaO + CO₂', 'Slaked: CaO + H₂O → Ca(OH)₂', 'Hydraulic limes also set with water'],
         ['Process CO₂ from the stone', 'plus fuel, at a lower temperature'], 'Air lime sets by taking CO₂ back.', 'Soft mortar lets bricks be reused.', False),
        (650, 'Fired clay brick', 'for facing and walls', [
         'Clay shaped and dried', 'Fired at about 1,000 °C', 'Minerals fuse into a hard body', 'No limestone, little process CO₂'],
         ['Almost all CO₂ from fuel', '(mostly natural gas)'], 'Lasts centuries.', 'Reusable if laid in lime mortar.', False)]
    for x, t, s, steps, src, e1, e2, hot in cols:
        b += panel(x, 75, 290, 425, t, s, hot)
        for i, st in enumerate(steps):
            mono = '→' in st
            b += text(x + 145, 140 + i * 30, st, 13 if mono else 12.5, INK, extra=MONO if mono else '')
        b += f'<rect x="{x+15}" y="275" width="260" height="70" rx="6" fill="{TINT}" stroke="{RED}"/>'
        b += text(x + 145, 300, src[0], 13, RED, weight='700') + text(x + 145, 322, src[1], 12.5, RED)
        b += text(x + 145, 390, e1, 12.5, INK) + text(x + 145, 412, e2, 12.5, INK)
    b += text(20, 528, 'Kiln temperatures are typical values; see the sources on the page.', 11.5, MUTED, 'start')
    svg('cement-lime-brick.svg', w, h, 'Where the CO2 comes from in cement, lime and brick',
        'Three panels. Portland cement: limestone and clay heated to about 1,450 degrees; calcium carbonate gives calcium oxide and CO2; the oxide reacts with clay to make clinker, ground with gypsum into cement. CO2 comes from the stone itself plus fuel for the hottest kiln; cement sets with water and takes back only a fraction of its CO2. '
        'Lime: limestone heated to about 900 degrees, giving calcium oxide and CO2, then slaked to calcium hydroxide; process CO2 plus fuel; air lime sets by taking CO2 back, and soft lime mortar lets bricks be reused. '
        'Fired clay brick: clay shaped, dried and fired at about 1,000 degrees; no limestone, so almost all its CO2 comes from fuel, mostly natural gas; it lasts centuries and can be reused if laid in lime mortar.', b)


def wall_life_cycle():
    nodes = [('Quarry and forest', 'stone, clay, sand,', 'timber, iron ore', False),
             ('Make the product', 'kilns, mills, sawmills:', 'most of the carbon', True),
             ('Build', 'transport, site', 'waste, offcuts', False),
             ('Use: 60+ years', 'heating, repairs,', 'replacement', False),
             ('Take down', 'demolish, or', 'dismantle carefully', False),
             ('Reuse, recycle or tip', 'whole bricks and beams,', 'crushed hardcore, landfill', True)]
    cycle('wall-life-cycle.svg', 'The life cycle of a wall', 'Embodied carbon is mostly paid on the first day. How the wall is put together decides whether it can be used again.',
          nodes, ['Stages A to C', 'cradle to grave', '(BS EN 15978)'],
          'A six-step loop. Raw materials are quarried or felled: stone, clay, sand, timber and iron ore. Making the products in kilns, mills and sawmills is where most of the embodied carbon is released. '
          'Building adds transport and site waste. In use, over sixty years or more, come heating, repairs and replacements. At the end the wall is demolished or carefully dismantled, then reused, recycled as crushed hardcore, or tipped. '
          'These are life-cycle stages A to C in the standard BS EN 15978.',
          w=920, h=620, cx=460, cy=335, R=215)


# ================================================================ circular economy

def linear_vs_circular():
    w, h = 960, 640
    b = arrow_defs(INK, RED, GREEN, BLUE)
    b += text(20, 30, 'Linear, recycling and circular', 20, INK, 'start', '700')
    b += text(20, 52, 'The tighter the loop, the more of the original effort (and carbon) is kept. Recycling is the outermost loop, not the first.', 13, MUTED, 'start')
    y = 82
    b += text(20, y + 28, 'Linear:', 14, RED, 'start', '700')
    for i, s in enumerate(['Take', 'Make', 'Sell', 'Use', 'Bin']):
        x = 110 + i * 168
        b += f'<rect x="{x}" y="{y}" width="120" height="44" rx="6" fill="{"#f4f4f4" if i < 4 else TINT}" stroke="{GREY if i < 4 else RED}" stroke-width="1.5"/>'
        b += text(x + 60, y + 28, s, 15, INK, weight='700')
        if i < 4:
            b += arr(x + 122, y + 22, x + 166, y + 22, 0, INK, 2)
    b += text(20, 170, 'Circular:', 14, GREEN, 'start', '700')
    cy, cx = 450, 480
    loops = [(70, 'Maintain, repair, share', GREEN, 'keeps almost everything', 2),
             (125, 'Reuse, refurbish', GREEN, 'keeps the product', 2),
             (180, 'Remanufacture', BLUE, 'keeps the parts', 3),
             (235, 'Recycle', GREY, 'keeps only the material', 0)]
    for r, lab, c, keep, m in loops:
        b += f'<path d="M{cx-90} {cy} C {cx-90-r*1.6} {cy-r*1.3}, {cx+90+r*1.6} {cy-r*1.3}, {cx+90} {cy}" fill="none" stroke="{c}" stroke-width="3" marker-end="url(#a{m})"/>'
        b += text(cx, cy - r * 0.975 - 22, lab, 13.5, INK, weight='700')
        b += text(cx, cy - r * 0.975 - 7, keep, 11.5, MUTED)
    b += f'<rect x="{cx-90}" y="{cy-30}" width="180" height="60" rx="8" fill="{INK}"/>'
    b += text(cx, cy - 4, 'Product in use', 15, '#fff', weight='700') + text(cx, cy + 16, 'by a customer', 12, '#fff')
    b += text(cx, cy + 56, 'Smaller loops come first: they keep the energy and carbon already spent.', 13, INK, weight='700')
    b += f'<rect x="20" y="530" width="920" height="90" rx="8" fill="#f6f9f5" stroke="{GREEN}"/>'
    b += text(480, 556, 'The biological loop runs alongside it', 14, INK, weight='700')
    b += text(480, 578, 'Food, wood and other living materials: eat or use first, then feed animals, then compost or anaerobic digestion,', 12.5, INK)
    b += text(480, 598, 'returning nutrients to the soil. Fish guts, shells, food waste and timber offcuts sit here.', 12.5, INK)
    svg('linear-vs-circular.svg', w, h, 'Linear economy against circular loops',
        'At the top, the linear economy: take, make, sell, use, bin. Below, a product in use sits at the centre of four loops, from the tightest to the widest: maintain, repair and share, which keeps almost everything; reuse and refurbish, which keeps the product; remanufacture, which keeps the parts; and recycle, which keeps only the material. '
        'Smaller loops come first because they keep the energy and carbon already spent. A biological loop runs alongside: food, wood and other living materials are used, then fed to animals, then composted or digested, returning nutrients to the soil.', b)


def waste_hierarchy():
    w, h = 960, 500
    b = text(20, 30, 'The waste hierarchy', 20, INK, 'start', '700')
    b += text(20, 52, 'The order of preference in waste law (in NI, the Waste Regulations (NI) 2011, reg. 17). Departing from it needs a life-cycle reason.', 13, MUTED, 'start')
    tiers = [('Prevention', 'use less, design out waste', GREEN, 760),
             ('Preparing for reuse', 'check, clean, repair', GREEN, 660),
             ('Recycling', 'including composting', BLUE, 560),
             ('Other recovery', 'e.g. energy from waste', GREY, 460),
             ('Disposal', 'landfill; burning without recovery', RED, 380)]
    c = 400
    for i, (t, s, col, tw) in enumerate(tiers):
        y = 75 + i * 80
        x = c - tw / 2
        b += f'<path d="M{x} {y} L{x+tw} {y} L{x+tw-50} {y+72} L{x+50} {y+72} z" fill="{col}" opacity="0.9"/>'
        b += text(c, y + 34, t, 16, '#fff', weight='700') + text(c, y + 54, s, 12.5, '#fff')
    b += text(800, 115, '↑ Most preferred', 13, GREEN, 'start', '700')
    b += text(800, 435, '↓ Least preferred', 13, RED, 'start', '700')
    b += text(800, 260, 'NI 2024/25:', 12.5, INK, 'start', '700')
    b += lines(800, 280, ['recycling 50.4%', 'energy recovery 34.3%', 'landfill 14.0%', '(council-collected waste)'], 12, lh=18, anchor='start')
    svg('waste-hierarchy.svg', w, h, 'The waste hierarchy',
        'An inverted pyramid, from most to least preferred: prevention, meaning using less and designing out waste; preparing for reuse, meaning checking, cleaning and repairing; recycling, including composting; other recovery such as energy from waste; and disposal, meaning landfill or burning without energy recovery. '
        'In Northern Ireland the duty sits in regulation 17 of the Waste Regulations (NI) 2011. In 2024/25 NI councils recycled 50.4% of the waste they collected, sent 34.3% to energy recovery and 14.0% to landfill.', b)


# ================================================================ fish and shells

def fish_flow():
    w, h = 960, 540
    b = arrow_defs(INK, RED, GREEN)
    b += text(20, 30, 'One fish, many products', 20, INK, 'start', '700')
    b += text(20, 52, 'A skinless fillet is about a third of a cod or haddock. What happens to the rest decides whether it is waste or a resource.', 13, MUTED, 'start')
    b += f'<rect x="20" y="210" width="170" height="90" rx="8" fill="{INK}"/>'
    b += text(105, 248, 'Whole fish', 16, '#fff', weight='700') + text(105, 270, 'or prawns', 12.5, '#fff')
    parts = [('Fillet', 'food', GREEN), ('Heads and frames', 'fishmeal, oil, garden fertiliser', GREEN), ('Guts (viscera)', 'oil, silage, enzymes', GREEN),
             ('Skin and scales', 'collagen, gelatine, leather', GREEN), ('Shells (shellfish)', 'lime, grit, chitin', GREEN)]
    for i, (p, u, c) in enumerate(parts):
        y = 80 + i * 90
        b += f'<path d="M190 255 C 250 255, 250 {y+30}, 300 {y+30}" fill="none" stroke="{INK}" stroke-width="2" marker-end="url(#a0)"/>'
        b += f'<rect x="302" y="{y}" width="230" height="60" rx="8" fill="{"#f6f9f5" if i == 0 else "#fff"}" stroke="{GREY}" stroke-width="1.5"/>'
        b += text(417, y + 26, p, 14, INK, weight='700') + text(417, y + 46, u, 12, MUTED)
        if i > 0:
            b += arr(534, y + 30, 600, y + 30, 2, GREEN, 2)
    b += f'<rect x="604" y="160" width="336" height="200" rx="8" fill="{TINT}" stroke="{RED}" stroke-width="1.5"/>'
    b += text(772, 186, 'Or, if nobody takes them', 14, INK, weight='700')
    b += lines(772, 214, ['Rendering or incineration: a cost', 'Fish waste must not be landfilled', 'Animal by-products rules apply', 'Value and nutrients lost'], 12.5, lh=22, col=INK)
    b += text(772, 330, 'The same tonne can earn or cost money.', 12.5, RED, weight='700')
    b += f'<rect x="604" y="380" width="336" height="130" rx="8" fill="#f6f9f5" stroke="{GREEN}"/>'
    b += text(772, 406, 'The higher-value routes', 14, INK, weight='700')
    b += lines(772, 432, ['Food and supplements first,', 'then feed, then fertiliser and energy:', 'the biological loop of the', 'circular economy.'], 12.5, lh=19)
    svg('fish-by-products.svg', w, h, 'One fish, many products',
        'A whole fish or prawn splits into five streams: the fillet, used as food; heads and frames, used for fishmeal, oil and garden fertiliser such as blood, fish and bone; guts, used for oil, silage and enzymes; skin and scales, used for collagen, gelatine and leather; and shells from shellfish, used for lime, grit and chitin. '
        'If nobody takes them, by-products go to rendering or incineration at a cost; fish waste must not be landfilled, and animal by-products rules apply. The higher-value order is food and supplements first, then feed, then fertiliser and energy.', b)


def shell_chemistry():
    w, h = 960, 555
    b = arrow_defs(INK, RED, BLUE, GREEN)
    b += text(20, 30, 'Is a seashell a carbon store?', 20, INK, 'start', '700')
    b += text(20, 52, 'Shells are calcium carbonate, but making them releases CO₂ in seawater, and burning them releases the rest.', 13, MUTED, 'start')
    b += panel(20, 75, 450, 220, 'Building a shell (in the sea)', 'calcification')
    b += text(245, 150, 'Ca²⁺ + 2HCO₃⁻ → CaCO₃ + CO₂ + H₂O', 15, INK, weight='700', extra=MONO)
    b += lines(245, 185, ['Seawater bicarbonate becomes shell,', 'releasing CO₂. In seawater, about 0.6 CO₂', 'is released per CaCO₃ at 25 °C, more', 'in cold water (Frankignoulle et al. 1994).'], 12.5, lh=19)
    b += panel(490, 75, 450, 220, 'Burning shells for lime', 'calcination, about 900 °C', True)
    b += text(715, 150, 'CaCO₃ → CaO + CO₂', 15, INK, weight='700', extra=MONO)
    b += lines(715, 185, ['Same reaction as burning limestone:', '0.44 kg CO₂ per kg of carbonate,', 'plus the fuel for the kiln.', 'Shell lime is not carbon-free lime.'], 12.5, lh=19)
    b += panel(20, 315, 450, 220, 'Crushing shells unburned', 'liming, grit, aggregate, filters')
    b += lines(245, 395, ['Spread on acid soil, carbonate neutralises acid:', 'CaCO₃ + 2H⁺ → Ca²⁺ + CO₂ + H₂O', 'Replaces quarried limestone that would', 'release the same CO₂ on the same field.'], 12.5, lh=20)
    b += panel(490, 315, 450, 220, 'Tipping shells', 'where it is allowed', True)
    b += lines(715, 395, ['The carbonate stays put,', 'but any attached flesh rots,', 'it costs money (over £80 a tonne in 2016),', 'and a usable material is lost.'], 12.5, lh=20)
    svg('shell-chemistry.svg', w, h, 'Seashell chemistry and carbon',
        'Four panels. Building a shell in the sea: calcium plus two bicarbonate ions give calcium carbonate, CO2 and water, so calcification releases CO2: in seawater about 0.6 CO2 per carbonate at 25 degrees, more in cold water. '
        'Burning shells for lime at about 900 degrees: calcium carbonate gives calcium oxide and CO2, 0.44 kilograms of CO2 per kilogram of carbonate plus kiln fuel, the same as limestone. '
        'Crushing shells unburned for liming, grit or aggregate: on acid soil carbonate neutralises acid and releases CO2, replacing quarried limestone that would release the same. '
        'Tipping shells, where allowed: the carbonate stays put, but attached flesh rots, it costs money, and a usable material is lost.', b)


def chitin_scheme():
    w, h = 960, 380
    b = arrow_defs(INK, RED)
    b += text(20, 30, 'From prawn shell to chitosan', 20, INK, 'start', '700')
    b += text(20, 52, 'Crustacean shell is a composite: chitin fibres, protein and calcium carbonate. Separating them takes acid, alkali and energy.', 13, MUTED, 'start')
    steps = [('Prawn and crab shell', 'chitin + protein', '+ calcium carbonate', False),
             ('Demineralise', 'dilute hydrochloric acid', 'dissolves CaCO₃, frees CO₂', False),
             ('Deproteinise', 'dilute NaOH (or enzymes)', 'removes protein', False),
             ('Chitin', 'a sugar polymer like cellulose,', 'with –NHCOCH₃ groups', False),
             ('Deacetylate', 'hot concentrated NaOH', '–NHCOCH₃ → –NH₂', True)]
    bw = 166
    for i, (t, l1, l2, hot) in enumerate(steps):
        x = 20 + i * (bw + 22)
        b += f'<rect x="{x}" y="90" width="{bw}" height="120" rx="8" fill="{TINT if hot else "#fff"}" stroke="{RED if hot else INK}" stroke-width="1.5"/>'
        b += text(x + bw / 2, 120, t, 13.5, INK, weight='700')
        b += text(x + bw / 2, 148, l1, 11.5, MUTED)
        b += text(x + bw / 2, 168, l2, 11 if '→' in l2 else 11.5, INK if '→' in l2 else MUTED, extra=MONO if '→' in l2 else '')
        if i < len(steps) - 1:
            b += arr(x + bw + 2, 150, x + bw + 20, 150, 0, INK, 2)
    b += f'<rect x="20" y="235" width="920" height="120" rx="8" fill="#f6f9f5" stroke="{GREEN}"/>'
    b += text(480, 262, 'Chitosan: the product', 15, INK, weight='700')
    b += text(480, 288, 'Positively charged in mild acid, so it binds fats, dyes, metals and fine particles.', 13, INK)
    b += text(480, 310, 'Uses: water treatment, wound dressings, food coatings, cosmetics, seed treatments.', 13, INK)
    b += text(480, 334, 'The chemicals and heat have their own footprint: check the process, not just the shell.', 12.5, RED, weight='700')
    svg('chitin-to-chitosan.svg', w, h, 'Making chitosan from crustacean shells',
        'A five-step process. Prawn and crab shell is chitin, protein and calcium carbonate. Dilute hydrochloric acid dissolves the carbonate, releasing CO2. Dilute sodium hydroxide or enzymes remove the protein. What is left is chitin, a sugar polymer like cellulose with acetyl-amino groups. '
        'Hot concentrated sodium hydroxide removes the acetyl groups to give chitosan, which is positively charged in mild acid and binds fats, dyes, metals and fine particles. It is used in water treatment, wound dressings, food coatings, cosmetics and seed treatments. The chemicals and heat have their own footprint.', b)


# ================================================================ medicines

def feedstock_tree():
    w, h = 960, 600
    b = arrow_defs(INK, RED, GREY)
    b += text(20, 30, 'From oil and gas to the medicine cabinet', 20, INK, 'start', '700')
    b += text(20, 52, 'Most synthetic medicines, and almost all medical plastics, start from a handful of petrochemical building blocks.', 13, MUTED, 'start')
    b += f'<rect x="20" y="80" width="200" height="440" rx="8" fill="#f4f4f4" stroke="{GREY}"/>'
    b += text(120, 106, 'Crude oil and', 14, INK, weight='700') + text(120, 124, 'natural gas', 14, INK, weight='700')
    b += lines(120, 160, ['Refining and', 'steam cracking', '', 'Reforming'], 12.5)
    blocks = [('Benzene, toluene', 'aromatic rings', 110), ('Ethylene, propylene', 'small building blocks', 210),
              ('Methanol, ammonia', 'from natural gas', 310), ('Solvents', 'acetone, toluene, DMF…', 410)]
    for t, s, y in blocks:
        b += arr(222, y + 25, 290, y + 25, 0, INK, 2)
        b += f'<rect x="292" y="{y}" width="210" height="58" rx="8" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
        b += text(397, y + 25, t, 13.5, INK, weight='700') + text(397, y + 44, s, 11.5, MUTED)
    outs = [('Phenol', 'via cumene', 90, 110), ('Aspirin, paracetamol', 'and many more APIs', 160, 110),
            ('Plastics', 'syringes, IV bags, blister packs', 240, 210), ('Building blocks', 'for many active ingredients', 320, 310),
            ('Used, then recovered or burned', 'often the biggest mass in the process', 420, 410)]
    for t, s, y, fy in outs:
        b += f'<path d="M504 {fy+29} C 545 {fy+29}, 545 {y+25}, 585 {y+25}" fill="none" stroke="{INK}" stroke-width="2" marker-end="url(#a0)"/>'
        hot = t.startswith('Aspirin')
        b += f'<rect x="588" y="{y}" width="352" height="56" rx="8" fill="{TINT if hot else "#fff"}" stroke="{RED if hot else GREY}" stroke-width="1.5"/>'
        b += text(764, y + 24, t, 13.5, INK, weight='700') + text(764, y + 43, s, 11.5, MUTED)
    b += arr(764, 146, 764, 158, 0, INK, 2)
    b += text(480, 560, 'The carbon in the molecule is small. The energy, solvents and waste needed to make it are not.', 13, RED, weight='700')
    svg('medicine-feedstocks.svg', w, h, 'From oil and gas to medicines',
        'Crude oil and natural gas are refined, cracked and reformed into building blocks: benzene and toluene, which are aromatic rings; ethylene and propylene; methanol and ammonia from natural gas; and solvents such as acetone, toluene and DMF. '
        'Benzene leads via cumene to phenol, which leads to aspirin, paracetamol and many other active ingredients. Ethylene and propylene make plastics for syringes, IV bags and blister packs. Methanol and ammonia are building blocks for many active ingredients. Solvents are used and then recovered or burned, often the biggest mass in the process. '
        'The carbon in the molecule is small; the energy, solvents and waste needed to make it are not.', b)


def aspirin_paracetamol():
    w, h = 960, 470
    b = arrow_defs(INK, RED)
    b += text(20, 30, 'Two everyday medicines, from benzene', 20, INK, 'start', '700')
    b += text(20, 52, 'Simplified textbook routes; manufacturers vary them. Each arrow is a reactor, energy, solvent and waste.', 13, MUTED, 'start')
    rows = [(90, 'Aspirin', [('Benzene', 'C₆H₆'), ('Cumene process', '+ propylene, air'), ('Phenol', 'C₆H₅OH'),
                              ('Kolbe–Schmitt', '+ NaOH, CO₂, heat'), ('Salicylic acid', ''), ('Acetylate', '+ acetic anhydride')], ('Aspirin', 'acetylsalicylic acid')),
            (260, 'Paracetamol', [('Benzene', 'C₆H₆'), ('Cumene process', '+ propylene, air'), ('Phenol', 'C₆H₅OH'),
                                  ('Nitrate, reduce', 'via 4-nitrophenol'), ('4-aminophenol', ''), ('Acetylate', '+ acetic anhydride')], ('Paracetamol', 'acetaminophen in the US'))]
    for y, name, steps, prod in rows:
        b += text(20, y - 10, name, 15, RED, 'start', '700')
        for i, (t, s) in enumerate(steps):
            x = 20 + i * 132
            reag = i % 2 == 1
            b += f'<rect x="{x}" y="{y}" width="118" height="62" rx="8" fill="{"#f4f4f4" if reag else "#fff"}" stroke="{GREY if reag else INK}" stroke-width="1.5"/>'
            b += text(x + 59, y + 27, t, 12, INK, weight='700') + text(x + 59, y + 46, s, 10.5, MUTED)
            b += arr(x + 119, y + 31, x + 131, y + 31, 0, INK, 2)
        b += f'<rect x="812" y="{y}" width="128" height="62" rx="8" fill="{TINT}" stroke="{RED}" stroke-width="1.5"/>'
        b += text(876, y + 27, prod[0], 13.5, INK, weight='700') + text(876, y + 46, prod[1], 10.5, MUTED)
    b += f'<rect x="20" y="360" width="920" height="90" rx="8" fill="#fff" stroke="{RULE}"/>'
    b += text(480, 386, 'Paracetamol: 8 carbon atoms, all from fossil feedstocks. Aspirin: 9, one of them from the CO₂ in Kolbe–Schmitt.', 13, INK, weight='700')
    b += text(480, 408, 'Bio-based phenol and acetic acid exist, and could replace some fossil carbon,', 12.5, INK)
    b += text(480, 428, 'but most of the footprint is process energy and solvents, not the atoms in the tablet.', 12.5, INK)
    svg('aspirin-paracetamol-routes.svg', w, h, 'Industrial routes to aspirin and paracetamol',
        'Aspirin: benzene is turned into phenol by the cumene process using propylene and air; phenol is turned into salicylic acid by the Kolbe-Schmitt reaction with sodium hydroxide, CO2 and heat; salicylic acid is acetylated with acetic anhydride to give aspirin. '
        'Paracetamol: benzene to phenol by the cumene process; phenol is nitrated and reduced to 4-aminophenol, which is acetylated with acetic anhydride to give paracetamol. Paracetamol has 8 carbon atoms, all from fossil feedstocks on this route; aspirin has 9, one of which comes from the CO2 used in the Kolbe-Schmitt step. '
        'Bio-based phenol and acetic acid exist, but most of the footprint is process energy and solvents, not the atoms in the tablet.', b)


def medicine_life_cycle():
    nodes = [('Feedstocks', 'oil, gas, plants,', 'fermentation', False),
             ('Make the ingredient', 'many steps and solvents:', 'often tens of kg per kg', True),
             ('Formulate and pack', 'tablets, inhalers,', 'blister packs', False),
             ('Distribute', 'cold chain for', 'some products', False),
             ('Use', 'inhaler propellants and', 'anaesthetic gases emitted', True),
             ('After use', 'unused stock wasted;', 'residues reach water', False)]
    cycle('medicine-life-cycle.svg', 'The life cycle of a medicine', 'Two hotspots: making the active ingredient, and the few products whose propellants or gases escape when used.',
          nodes, ['Patient need', 'comes first', ''],
          'A six-step loop. Feedstocks come from oil, gas, plants or fermentation. Making the active ingredient takes many steps and solvents, often tens of kilograms of material per kilogram of product, and is a hotspot. '
          'Then formulation and packing into tablets, inhalers and blister packs; distribution, with a cold chain for some products; use, where inhaler propellants and anaesthetic gases are emitted, the second hotspot; and after use, when unused stock is wasted and residues reach water.',
          w=920, h=620, cx=460, cy=335, R=215)


# ---------------------------------------------------------------- data charts

def wall_house_compare():
    rows = [('Brick-clad cavity wall', 526, GREY, '526'),
            ('Rendered block cavity wall', 496, GREY, '496'),
            ('Single-leaf block + external insulation', 492, GREY, '492'),
            ('Timber frame, cellulose insulation*', 369, GREEN, '369')]
    hbars('house-embodied-by-wall.svg', 'One small house, four ways to build it',
          'kg CO₂e per m² of floor, embodied carbon (stages as reported), 84 m² Irish social home. AECB study for the Passive House Association of Ireland, 2021.',
          rows, 600, 'kg CO₂e per m² of floor area',
          'Embodied carbon of an 84 square metre social home in Ireland by wall type: brick-clad cavity 526 kg CO2e per square metre of floor; rendered block cavity 496; 215 mm single-leaf block with external insulation 492; '
          'timber frame with cellulose insulation, insulated foundations and 50% GGBS cement replacement 369. From an AECB study for the Passive House Association of Ireland, reported in 2021.',
          note=['The timber house is 25–30% lower. The three masonry options are within 7% of each other.',
                '* also with insulated foundations and 50% GGBS in the concrete, so not only the wall changed.'], L=380, W=440, extra_h=85)


def material_factors():
    rows = [('Fired clay brick', 0.213, GREY, '0.21'), ('Softwood (studs), excl. stored carbon', 0.263, GREEN, '0.26'),
            ('Lightweight concrete block', 0.28, GREY, '0.28'), ('Cross-laminated timber (CLT)', 0.437, GREEN, '0.25–0.44'),
            ('Lime, process CO₂ only', 0.75, SAND, '0.75 + fuel'), ('Steel sections, world average', 1.55, BLUE, '1.55')]
    hbars('wall-material-factors.svg', 'Kilogram for kilogram: cradle-to-gate factors',
          'kg CO₂e per kg of material (A1–A3). ICE database v3 via IStructE (2020); CLT range IStructE 2021; lime from IPCC 2006 process factor.',
          rows, 1.8, 'kg CO₂e per kg',
          'Cradle-to-gate factors in kilograms of CO2 equivalent per kilogram: fired clay brick 0.21; softwood studs 0.26 excluding stored carbon; lightweight concrete block 0.28; cross-laminated timber 0.25 to 0.44; lime 0.75 for the process CO2 alone, plus fuel; world-average steel sections 1.55. '
          'Per kilogram comparisons mislead because walls use very different weights of each material; compare per square metre of wall or floor.',
          note=['Per kg is not the whole story: a block wall weighs several times a timber-frame wall.',
                'Compare per m² of wall or floor at the same insulation level, as in the house chart.'], L=360, W=430, extra_h=85)


def ni_waste_chart():
    rows = [('Recycled (incl. composting)', 50.4, GREEN, '50.4%'), ('Energy recovery', 34.3, GREY, '34.3%'),
            ('Landfill', 14.0, RED, '14.0%'), ('Statutory target: recycled by 2030', 70, None, '70%')]
    w, L, W, top, rh = 900, 330, 470, 80, 50
    h = top + rh * len(rows) + 100
    b = text(20, 30, 'Northern Ireland: where council-collected waste went, 2024/25', 20, INK, 'start', '700')
    b += text(20, 52, 'Per cent of local-authority collected municipal waste. DAERA, released 11 December 2025.', 13, MUTED, 'start')
    for i, (lab, v, c, t) in enumerate(rows):
        y = top + i * rh
        b += text(L - 12, y + 26, lab, 13.5, INK, 'end', '700')
        if c:
            b += f'<rect x="{L}" y="{y+8}" width="{W*v/100:.1f}" height="28" rx="4" fill="{c}"/>'
        else:
            b += f'<rect x="{L}" y="{y+8}" width="{W*v/100:.1f}" height="28" rx="4" fill="none" stroke="{GREEN}" stroke-width="2" stroke-dasharray="6 4"/>'
        b += text(L + W * v / 100 + 10, y + 28, t, 13.5, INK, 'start', '700')
    b += f'<line x1="{L}" y1="{top}" x2="{L}" y2="{top+rh*4}" stroke="{INK}"/>'
    b += text(20, top + rh * 4 + 30, 'Recycling has been flat at about 50% for years. Landfill fell, but energy recovery took its place: waste moved', 12.5, RED, 'start', '700')
    b += text(20, top + rh * 4 + 50, 'down the hierarchy, not up. The 70% target (Climate Change Act (NI) 2022, s.18) still needs defining, says DAERA.', 12.5, INK, 'start')
    svg('ni-waste-2024-25.svg', w, h, 'Northern Ireland municipal waste routes 2024/25',
        'Of the municipal waste collected by Northern Ireland councils in 2024/25, 50.4% was recycled or composted, 34.3% went to energy recovery and 14.0% to landfill (DAERA, 11 December 2025). The Climate Change Act (Northern Ireland) 2022 requires at least 70% of waste to be recycled by 2030. '
        'Recycling has been flat at about 50%; landfill fell but energy recovery took its place, so waste moved down the hierarchy rather than up.', b)


def bags_chart():
    rows = [('Paper bag', 3, SAND, '3 uses'), ('“Bag for life” (LDPE)', 4, GREY, '4'), ('Non-woven polypropylene', 11, BLUE, '11'), ('Cotton bag', 131, GREEN, '131')]
    hbars('carrier-bag-break-even.svg', 'Reuse only pays if you actually reuse',
          'Times each bag must be used to have a lower carbon footprint than a single-use plastic bag used once. Environment Agency, 2011 (2006 bags).',
          rows, 140, 'number of uses',
          'Environment Agency life-cycle study of carrier bags, 2011: to beat a single-use plastic carrier on climate impact, a paper bag must be used 3 times, a plastic bag for life 4 times, a non-woven polypropylene bag 11 times and a cotton bag 131 times. If every plastic carrier is reused as a bin liner the numbers rise to 7, 9, 26 and 327.',
          note=['If every single-use bag is reused as a bin liner, the numbers rise to 7, 9, 26 and 327.',
                'Climate only, and old data: the point is the shape, not the decimals.'], L=330, W=470, extra_h=85)


def fillet_yield():
    rows = [('Whiting', 32, GREY, '32%'), ('Atlantic cod', 34, GREY, '34%'), ('Haddock', 35, GREY, '35%'),
            ('Atlantic herring', 46, BLUE, '46%'), ('Atlantic mackerel', 54, BLUE, '54%')]
    hbars('fillet-yields.svg', 'How much of a fish is fillet?',
          'Skinless fillet as a share of whole fish weight. FAO Fisheries Technical Paper 309. Yields vary widely with size, season and skill.',
          rows, 100, 'per cent of whole weight that is fillet; the rest is heads, frames, guts, skin',
          'Skinless fillet yield as a share of the whole fish, from FAO: whiting 32%, Atlantic cod 34%, haddock 35%, Atlantic herring 46%, Atlantic mackerel 54%. The rest, about half to two-thirds, is heads, frames, guts and skin. FAO says yields vary widely.',
          note=['For whitefish about two-thirds of the catch is not fillet. FAO puts by-products at 30–70% of the fish.'], L=250, W=520, extra_h=70)


def nhs_footprint():
    rows = [('Non-medical supply chain', 42, GREY, '42%'), ('Medicines and chemicals', 25, RED, '25%'), ('Buildings and estates', 15, GREY, '15%'),
            ('Travel', 14, GREY, '14%'), ('Food', 6, GREY, '6%'), ('Inhalers', 3, RED, '3%'), ('Anaesthetic gases', 2, RED, '2%')]
    hbars('nhs-footprint.svg', 'Where the NHS footprint comes from (England)',
          'Share of NHS England emissions by area, as NHS England reports them. Greener NHS, from Delivering a “Net Zero” NHS (2020, updated 2022).',
          rows, 50, 'per cent of NHS England emissions (categories overlap; they do not sum to 100)',
          'NHS England reports these shares of its emissions: non-medical supply chain 42%; medicines and chemicals 25%; buildings and estates 15%; travel 14%; food 6%; inhalers 3%; anaesthetic gases 2%. The categories come from different footprint scopes and do not sum to 100. No equivalent figure was found for Health and Social Care in Northern Ireland.',
          note=['A quarter of the NHS footprint is medicines. No equivalent figure is published for HSC in Northern Ireland.'], L=290, W=520, rh=42, extra_h=70)


def pmi_chart():
    w, h = 900, 330
    L, W = 220, 520
    b = text(20, 30, 'How much material goes into 1 kg of a drug?', 20, INK, 'start', '700')
    b += text(20, 52, 'Process mass intensity (kg of everything in per kg of product), sildenafil. Cespi et al., Green Chemistry, about 2015. Log scale.', 13, MUTED, 'start')
    import math as _m
    X = lambda v: L + W * (_m.log10(v) - 1) / (_m.log10(20000) - 1)
    for v, t in [(10, '10'), (100, '100'), (1000, '1,000'), (10000, '10,000')]:
        b += f'<line x1="{X(v):.1f}" y1="75" x2="{X(v):.1f}" y2="230" stroke="{RULE}"/>' + text(X(v), 248, t, 12, MUTED)
    rows = [('First lab route', 17675, GREY, '17,675 kg'), ('Optimised lab route', 116, BLUE, '116 kg'), ('Commercial route', 60, GREEN, '60 kg')]
    for i, (lab, v, c, t) in enumerate(rows):
        y = 85 + i * 48
        b += text(L - 12, y + 22, lab, 13.5, INK, 'end', '700')
        b += f'<rect x="{L}" y="{y+4}" width="{X(v)-L:.1f}" height="28" rx="4" fill="{c}"/>' + text(X(v) + 10, y + 24, t, 13.5, INK, 'start', '700')
    b += text(20, 282, 'Solvents and water were about four-fifths of the mass. Redesigning the route cut it by more than 99%.', 12.5, RED, 'start', '700')
    b += text(20, 302, 'One worked example, not an industry average.', 12.5, INK, 'start')
    svg('drug-process-mass.svg', w, h, 'Process mass intensity of sildenafil',
        'Kilograms of material used per kilogram of sildenafil, on a log scale: the first laboratory route 17,675; the optimised laboratory route 116; the commercial route 60. Solvents and water were about four-fifths of the mass. One worked example from Cespi and colleagues in Green Chemistry, not an industry average.', b)


def bloom_carbon_nitrogen():
    nodes = [('Bloom grows', 'photosynthesis takes CO₂;', 'faster when warm', False),
             ('Some fix nitrogen', 'e.g. Dolichospermum:', 'N₂ → NH₃ in heterocysts', False),
             ('Toxins', 'microcystins (liver),', 'anatoxin-a (nerves)', True),
             ('Dies and sinks', 'leaks nitrogen and', 'phosphorus into the water', False),
             ('Rots', 'with oxygen: CO₂ back;', 'without: methane (CH₄)', True),
             ('Next bloom', 'fed by the nutrients', 'and phosphorus from the mud', False)]
    cycle('bloom-carbon-nitrogen.svg', 'A bloom’s carbon and nitrogen', 'The carbon is only borrowed, and some comes back as methane. Fixed nitrogen and recycled phosphorus feed the next bloom.',
          nodes, ['Borrowed carbon', 'a greener lake is a', 'bigger methane source'],
          'A six-step loop. A bloom grows, taking CO2 from the water by photosynthesis, and from the air when the water runs short; it grows faster in warm water. Some species, such as Dolichospermum and Aphanizomenon, fix nitrogen gas into ammonia in heterocysts; Microcystis cannot. Some make toxins: microcystins attack the liver, anatoxin-a the nerves. '
          'The bloom dies and sinks, leaking nitrogen and phosphorus into the water. It rots: with oxygen back to CO2, without oxygen to methane. The nutrients, with phosphorus released from the mud, feed the next bloom. The carbon is only borrowed, and a greener lake is a bigger methane source.',
          w=920, h=620, cx=460, cy=335, R=215)


if __name__ == '__main__':
    lime_cycle(); cement_vs_lime(); wall_life_cycle()
    linear_vs_circular(); waste_hierarchy()
    fish_flow(); shell_chemistry(); chitin_scheme()
    feedstock_tree(); aspirin_paracetamol(); medicine_life_cycle()
    bloom_carbon_nitrogen()
    wall_house_compare(); material_factors(); ni_waste_chart(); bags_chart(); fillet_yield(); nhs_footprint(); pmi_chart()
    print('ok')
