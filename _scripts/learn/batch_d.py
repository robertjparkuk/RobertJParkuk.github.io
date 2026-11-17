"""Diagrams for Learn Batch D (v0.39.0, 17 Nov 2026): fracking; contrails and "chemtrails".
Usage: python3 _scripts/learn/batch_d.py <repo_root>
Reuses helpers from gases.py, batch_a.py, batch_b.py and batch_c.py. Figures come from the research notes cited on each page.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gases import svg, text, e, RED, INK, GREY, MUTED, RULE, TINT  # noqa: E402
from batch_a import arrow_defs, arr, wrap, cycle, BLUE, GREEN  # noqa: E402
from batch_b import panel, lines, MONO  # noqa: E402
from batch_c import hbars, BROWN, SAND  # noqa: E402

SKY = '#EAF1F7'


# ================================================================ fracking

def well_life_cycle():
    nodes = [('Licence and permits', 'petroleum licence,', 'planning, environment', False),
             ('Drill', 'down, then sideways', 'through the shale', False),
             ('Frack', 'water, sand, additives', 'pumped at high pressure', True),
             ('Flowback', 'fluid and gas return;', 'venting or flaring', True),
             ('Produce for years', 'gas to the grid;', 'small leaks add up', True),
             ('Plug and abandon', 'cement plugs;', 'old wells can leak', False)]
    cycle('frack-well-life-cycle.svg', 'The life of a fracked well', 'Methane can escape at almost every stage. The CO₂ from burning the gas comes at the end, wherever it is used.',
          nodes, ['Burned or leaked?', 'burned: CO₂', 'leaked: methane'],
          'A six-step loop. A petroleum licence, planning and environmental permits; drilling down and then sideways through the shale; fracking, with water, sand and additives pumped at high pressure; flowback, when fluid and gas return and gas may be vented or flared; production for years, with small leaks adding up; and plugging and abandonment with cement plugs, after which old wells can leak. '
          'Methane can escape at almost every stage; the CO2 from burning the gas comes wherever it is used.',
          w=920, h=620, cx=460, cy=335, R=215)


def well_section():
    w, h = 960, 600
    b = arrow_defs(INK, RED, BLUE)
    b += text(20, 30, 'Inside a fracked well (not to scale)', 20, INK, 'start', '700')
    b += text(20, 52, 'Shale is usually far below drinking-water aquifers. The main paths for gas to escape are the well itself and the surface equipment.', 13, MUTED, 'start')
    b += '<g transform="translate(0 40)">'
    layers = [(80, 60, '#f3efe6', 'Soil and drift'), (140, 70, '#dbe8f2', 'Aquifer (drinking water)'), (210, 170, '#e9e4dc', 'Overlying rock: hundreds of metres to kilometres'),
              (380, 90, '#cfc6b8', 'Shale (gas held in tight rock)'), (470, 60, '#e9e4dc', '')]
    for y, hh, col, lab in layers:
        b += f'<rect x="20" y="{y}" width="920" height="{hh}" fill="{col}"/>'
        if lab:
            b += text(930, y + 24, lab, 12.5, INK, 'end', '700')
    # well pad
    b += f'<rect x="120" y="62" width="120" height="18" fill="{GREY}"/>' + text(180, 74, 'Well pad', 11, '#fff', weight='700')
    b += f'<rect x="174" y="80" width="12" height="330" fill="{INK}"/>'
    b += f'<path d="M180 405 Q 185 425 230 425 L 760 425" stroke="{INK}" stroke-width="12" fill="none"/>'
    for x in range(300, 760, 70):
        b += f'<line x1="{x}" y1="425" x2="{x-14}" y2="392" stroke="{RED}" stroke-width="2"/><line x1="{x}" y1="425" x2="{x+12}" y2="458" stroke="{RED}" stroke-width="2"/>'
    b += text(520, 492, 'Fractures, held open by sand, release gas from the shale', 12, RED, weight='700')
    # casing note
    b += f'<rect x="196" y="140" width="10" height="70" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="4 3"/>'
    b += text(212, 168, 'Steel casing and cement', 12, BLUE, 'start', '700') + text(212, 184, 'seal the well from the aquifer', 12, BLUE, 'start')
    # leak paths
    b += arr(180, 62, 180, 30, 1, RED, 2) + text(192, 40, 'Leaks and venting at the surface', 12, RED, 'start', '700')
    b += arr(170, 300, 120, 250, 1, RED, 2, dash=True) + text(30, 316, 'Failed casing', 12, RED, 'start', '700') + text(30, 332, 'or cement: gas', 12, RED, 'start') + text(30, 348, 'can rise up the well', 12, RED, 'start')
    b += '</g>'
    b += text(20, 585, 'Typical UK target depths are over a kilometre; the depth of each layer varies by site.', 11.5, MUTED, 'start')
    svg('frack-well-section.svg', w, h, 'Cross-section of a fracked well',
        'A schematic cross-section, not to scale. From the surface down: soil, a drinking-water aquifer, hundreds of metres to kilometres of overlying rock, and the gas-bearing shale. A well drops vertically from a well pad, then turns horizontal through the shale, where fractures are opened and held open by sand. '
        'Steel casing and cement seal the well from the aquifer. The main escape routes for gas are leaks and venting at the surface and failed casing or cement that lets gas migrate up the well.', b)


# ================================================================ contrails

def contrail_formation():
    w, h = 960, 520
    b = arrow_defs(INK, RED, BLUE)
    b += f'<rect x="0" y="0" width="{w}" height="{h}" fill="{SKY}"/>'
    b += text(20, 30, 'How a contrail forms', 20, INK, 'start', '700')
    b += text(20, 52, 'A contrail is a man-made cloud of ice crystals. Whether it lasts seconds or hours depends on the air the plane flies through.', 13, MUTED, 'start')
    steps = [('1. Burn fuel', 'kerosene + air →', 'CO₂ + water vapour + soot', False),
             ('2. Hot, wet exhaust', 'mixes with air', 'at about −40 °C or colder', False),
             ('3. Droplets freeze', 'on soot and other', 'particles: ice crystals', False),
             ('4a. Dry air', 'ice evaporates', 'within seconds or minutes', False),
             ('4b. Ice-supersaturated air', 'crystals grow and spread', 'into contrail cirrus for hours', True)]
    xs = [20, 210, 400, 590, 590]
    ys = [90, 90, 90, 70, 200]
    for i, (t, a, c, hot) in enumerate(steps):
        x, y = xs[i], ys[i]
        bw = 175 if i < 3 else 350
        b += f'<rect x="{x}" y="{y}" width="{bw}" height="92" rx="8" fill="{TINT if hot else "#fff"}" stroke="{RED if hot else INK}" stroke-width="1.5"/>'
        b += text(x + bw / 2, y + 28, t, 14, INK, weight='700') + text(x + bw / 2, y + 52, a, 12, MUTED) + text(x + bw / 2, y + 70, c, 12, MUTED)
    b += arr(197, 136, 208, 136, 0, INK, 2) + arr(387, 136, 398, 136, 0, INK, 2)
    b += arr(577, 120, 588, 112, 0, INK, 2) + arr(577, 150, 588, 230, 0, INK, 2)
    b += text(20, 230, 'Kerosene, roughly:', 13, INK, 'start', '700')
    b += text(20, 254, '2C₁₂H₂₆ + 37O₂ → 24CO₂ + 26H₂O', 15, INK, 'start', extra=MONO) + text(20, 298, '(idealised; real kerosene is a mixture)', 11.5, MUTED, 'start')
    b += text(20, 280, 'Each kg of fuel gives about 3.16 kg CO₂ and 1.2 kg of water.', 12.5, INK, 'start')
    b += f'<rect x="20" y="320" width="920" height="180" rx="8" fill="#fff" stroke="{RULE}"/>'
    b += text(480, 346, 'Why two planes at the same time can look so different', 14, INK, weight='700')
    b += lines(480, 372, ['Contrails need cold enough air (the Schmidt–Appleman criterion). Below that height, no trail.',
                          'They persist only where the air is already saturated with respect to ice: a thin, invisible layer.',
                          'A plane a few hundred metres higher or lower may miss that layer entirely.',
                          'Persistent trails spreading into a sheet of cloud are contrail cirrus: the part that matters for climate.'], 12.5, lh=24)
    svg('contrail-formation.svg', w, h, 'How a contrail forms',
        'Burning kerosene with air gives CO2, water vapour and soot; roughly, two molecules of C12H26 and 37 of oxygen give 24 of CO2 and 26 of water, so each kilogram of fuel gives about 3.16 kg of CO2 and 1.2 kg of water. The hot, wet exhaust mixes with air at about minus 40 degrees or colder, and droplets freeze on soot and other particles into ice crystals. '
        'In dry air the ice evaporates within seconds or minutes. In ice-supersaturated air the crystals grow and spread into contrail cirrus lasting hours. Contrails need cold enough air, the Schmidt-Appleman criterion, and persist only in thin layers saturated with respect to ice, so a plane a few hundred metres higher or lower may leave no lasting trail.', b)


def contrail_day_night():
    w, h = 960, 330
    b = arrow_defs(INK, RED, BLUE)
    b += text(20, 30, 'Contrails by day and by night', 20, INK, 'start', '700')
    b += text(20, 52, 'The same ice cloud can cool or warm. Overall, the warming wins.', 13, MUTED, 'start')
    b += panel(20, 75, 450, 200, 'Daytime', 'two effects pull against each other')
    b += lines(245, 150, ['Reflects some sunlight back to space: cooling', 'Traps heat rising from the ground: warming', 'Net: smaller, depends on sun angle', 'and what lies below'], 13, lh=24)
    b += panel(490, 75, 450, 200, 'Night-time', 'no sunlight to reflect', True)
    b += lines(715, 150, ['Only the heat-trapping effect remains', 'Net: warming', 'Night flights cause a large share', 'of contrail warming'], 13, lh=24)
    b += text(480, 305, 'The same physics as a cloudy night feeling milder than a clear, frosty one.', 13, INK, weight='700')
    svg('contrail-day-night.svg', w, h, 'Contrail warming by day and night',
        'Two panels. By day a contrail reflects some sunlight back to space, which cools, and traps heat rising from the ground, which warms; the net effect is smaller and depends on the sun angle and the surface below. By night there is no sunlight to reflect, so only the heat-trapping effect remains and the net effect is warming; night flights cause a large share of contrail warming. '
        'It is the same physics as a cloudy night feeling milder than a clear, frosty one.', b)


def aviation_erf():
    rows = [('Contrail cirrus', 57.4, RED, '57.4'), ('CO₂ from all flights since 1940', 34.3, INK, '34.3'),
            ('All other effects, net', 9.2, GREY, '9.2'), ('Aviation total, net', 100.9, BLUE, '100.9 (range 55–145)')]
    hbars('aviation-warming-2018.svg', 'What warms the climate in aviation (2018)',
          'mW/m² of effective radiative forcing (Lee et al. 2021). “Other” = NOx, water vapour, soot and sulphate, net (my arithmetic).',
          rows, 150, 'mW/m², effective radiative forcing',
          'Effective radiative forcing from aviation in 2018, in milliwatts per square metre, from Lee and colleagues 2021: contrail cirrus 57.4; CO2 from all flights since 1940, 34.3; all other effects net 9.2; aviation total net 100.9, with a range of 55 to 145. Non-CO2 effects were about two-thirds of the total, but they are much less certain than the CO2 effect.',
          note=['Contrails warmed more than all the CO₂ aviation has ever emitted, but with a much wider uncertainty.',
                'Contrail warming stops within hours if flights stop; CO₂ stays for centuries.'], L=300, W=470, extra_h=85)


def few_flights():
    rows = [('Flights causing 80% of contrail warming', 2, RED, 'about 2% of flights'),
            ('North Atlantic: share of flight distance', 4.9, BLUE, '4.9%'),
            ('North Atlantic: share of contrail warming', 11, RED, '11%')]
    hbars('contrail-few-flights.svg', 'A few flights do most of the damage',
          'Teoh et al. 2020 (Japanese airspace) and Teoh et al. 2024 (global, 2019–2021). Per cent.',
          rows, 20, 'per cent',
          'About 2% of flights caused 80% of contrail warming in a 2020 study by Teoh and colleagues; diverting 1.7% of flights by about 2,000 feet cut contrail forcing by 59% for under 0.1% extra fuel. Globally, the North Atlantic carried 4.9% of flight distance but caused 11% of contrail warming (Teoh and colleagues, 2024).',
          note=['Moving 1.7% of flights about 2,000 ft cut contrail warming by 59% for under 0.1% extra fuel (modelled, Teoh 2020).'], L=380, W=420, extra_h=70)


def burned_vs_leaked():
    rows = [('Burned: CO₂ from combustion', 2.74, INK, '2.74 kg CO₂'), ('Leaked, GWP-100 (AR5, UK reporting)', 28, RED, '28 kg CO₂e'),
            ('Leaked, GWP-100 (AR6, fossil)', 29.8, RED, '29.8 kg CO₂e'), ('Leaked, GWP-20 (AR6, fossil)', 82.5, RED, '82.5 kg CO₂e')]
    hbars('methane-burned-vs-leaked.svg', 'One kilogram of methane: burned or leaked',
          'kg CO₂e. Burning: CH₄ + 2O₂ → CO₂ + 2H₂O (44 ÷ 16). Leaking: GWP values from IPCC AR5 and AR6.',
          rows, 90, 'kg CO₂e per kg of methane',
          'One kilogram of methane burned gives 2.74 kg of CO2. Leaked unburned, it counts as 28 kg of CO2 equivalent on the 100-year AR5 value used in UK reporting, 29.8 kg on the AR6 100-year value for fossil methane, and 82.5 kg on the AR6 20-year value.',
          note=['A leak is ten to thirty times worse than burning the same gas, depending on the time horizon.'], L=330, W=440, extra_h=70)


def leak_share():
    w, h = 900, 400
    L, W, mx = 300, 420, 5.0
    b = text(20, 30, 'Per kg of gas produced: how much do leaks add?', 20, INK, 'start', '700')
    b += text(20, 52, 'kg CO₂e, assuming 2.3% of the gas leaks (Alvarez et al. 2018, US supply chain, 2015). My arithmetic.', 13, MUTED, 'start')
    rows = [('100-year view (AR6, 29.8)', 2.68, 0.69, '+26%'), ('20-year view (AR6, 82.5)', 2.68, 1.90, '+71%')]
    for i, (lab, burn, leak, t) in enumerate(rows):
        y = 90 + i * 80
        b += text(L - 12, y + 30, lab, 14, INK, 'end', '700')
        b += f'<rect x="{L}" y="{y+8}" width="{W*burn/mx:.1f}" height="36" fill="{INK}"/>'
        b += f'<rect x="{L+W*burn/mx:.1f}" y="{y+8}" width="{W*leak/mx:.1f}" height="36" fill="{RED}"/>'
        b += text(L + W * burn / mx / 2, y + 31, f'burned {burn:.2f}', 12, '#fff', weight='700')
        b += text(L + W * (burn + leak) / mx + 10, y + 31, f'+ leaked {leak:.2f} ({t})', 13, INK, 'start', '700')
    b += text(20, 280, 'Burned: 97.7% of 1 kg × 2.74 = 2.68 kg CO₂. Leaked: 2.3% × GWP. Treats the gas as pure methane.', 12.5, INK, 'start')
    b += text(20, 302, 'Global average upstream leakage is lower, about 1% (IEA 2026); some fields are much higher.', 12.5, INK, 'start')
    b += text(20, 336, 'Over 20 years, leaks of this size add most of the warming of burning the gas itself.', 12.5, RED, 'start', '700')
    svg('gas-leak-share.svg', w, h, 'How much leaks add to the footprint of gas',
        'For each kilogram of gas produced, assuming 2.3% leaks as Alvarez and colleagues found for the US supply chain in 2015: burning the rest gives 2.68 kg of CO2. On a 100-year view the leaked methane adds 0.69 kg of CO2 equivalent, 26% more; on a 20-year view it adds 1.90 kg, 71% more. Global average upstream leakage is lower, about 1% according to the IEA in 2026, and some fields are much higher.', b)


if __name__ == '__main__':
    well_life_cycle(); well_section(); burned_vs_leaked(); leak_share()
    contrail_formation(); contrail_day_night(); aviation_erf(); few_flights()
    print('ok')
