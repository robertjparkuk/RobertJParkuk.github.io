"""Diagrams for the Learn explainer "CO2e and global warming potential, in detail" (v0.37.2, 17 Nov 2026).
Usage: python3 _scripts/learn/gwp.py <repo_root>
Lifetimes and GWPs: IPCC AR6 WG1 Table 7.SM.7. CO2 decay: the Joos et al. (2013) impulse-response fit used in IPCC AR5 (illustrative).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gases import svg, text, e, RED, INK, GREY, MUTED, RULE, TINT  # noqa: E402
from batch_a import arrow_defs, arr, BLUE, GREEN  # noqa: E402

MONO = "font-family=\"'IBM Plex Mono',monospace\""


def co2_frac(t):
    a = [0.2173, 0.2240, 0.2824, 0.2763]
    tau = [394.4, 36.54, 4.304]
    return a[0] + sum(a[i + 1] * math.exp(-t / tau[i]) for i in range(3))


def decay():
    w, h = 960, 500
    L, R, T, B = 90, 760, 80, 420
    X = lambda t: L + t / 100 * (R - L)
    Y = lambda f: B - f * (B - T)
    b = text(20, 30, 'What is left of one kilogram, year by year', 20, INK, 'start', '700')
    b += text(20, 52, 'Share of a one-off release still in the air. Lifetimes from IPCC AR6; CO₂ uses the carbon-cycle fit from IPCC AR5 (illustrative).', 13, MUTED, 'start')
    for f in [0, 0.25, 0.5, 0.75, 1]:
        b += f'<line x1="{L}" y1="{Y(f):.1f}" x2="{R}" y2="{Y(f):.1f}" stroke="{RULE}"/>' + text(L - 8, Y(f) + 4, f'{int(f*100)}%', 12, MUTED, 'end')
    for t in range(0, 101, 20):
        b += text(X(t), B + 20, str(t), 12, INK)
    b += text((L + R) / 2, B + 42, 'Years after release', 12.5, MUTED)
    series = [('Carbon dioxide', co2_frac, INK, 'centuries+; about a fifth lasts millennia'),
              ('Nitrous oxide', lambda t: math.exp(-t / 109), '#D98C8C', '109 years'),
              ('Methane', lambda t: math.exp(-t / 11.8), RED, '11.8 years'),
              ('HFO-1234yf', lambda t: math.exp(-t / 0.033), BLUE, '12 days')]
    for name, fn, col, life in series:
        pts = ' '.join(f'{X(t):.1f},{Y(fn(t)):.1f}' for t in [i * 0.25 for i in range(401)])
        b += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="3"/>'
    ly = 100
    for name, fn, col, life in series:
        b += f'<rect x="785" y="{ly-11}" width="14" height="14" fill="{col}"/>' + text(806, ly, name, 13.5, INK, 'start', '700') + text(806, ly + 17, life, 12, MUTED, 'start')
        ly += 56
    b += text(785, 320, 'HFO-1234yf drops to nothing', 12, BLUE, 'start') + text(785, 336, 'within weeks: its line sits on the axis.', 12, BLUE, 'start')
    b += text(785, 365, 'After 100 years: about 40% of', 12, INK, 'start') + text(785, 381, 'the CO₂ is still there; almost', 12, INK, 'start') + text(785, 397, 'none of the methane.', 12, INK, 'start')
    svg('gwp-decay-curves.svg', w, h, 'How much of a one-kilogram release remains over 100 years',
        'Curves of the share of a one-off release still in the air over 100 years. HFO-1234yf, lifetime 12 days, vanishes almost at once. Methane, lifetime 11.8 years, is mostly gone within 30 to 40 years. Nitrous oxide, 109 years, falls to about 40%. '
        'Carbon dioxide drops quickly at first as oceans and plants take some up, then levels off: about 40% remains after 100 years and about a fifth lasts for millennia.', b)


def area():
    w, h = 960, 470
    b = text(20, 30, 'What a GWP actually measures', 20, INK, 'start', '700')
    b += text(20, 52, 'GWP = the heat trapped over a set period by 1 kg of a gas, divided by the heat trapped by 1 kg of CO₂ over the same period.', 13, MUTED, 'start')
    for k, (title, col, fn, peak, note) in enumerate([
            ('1 kg of methane', RED, lambda t: math.exp(-t / 11.8), 1.0, 'Traps far more heat per kg at first (tall), but most is gone in a few decades (short)'),
            ('1 kg of CO₂', INK, co2_frac, 1 / 120.0, 'Traps little heat per kg (very low), but stays for centuries (long)')]):
        x0 = 30 + k * 470
        L, R, T, B = x0 + 40, x0 + 420, 90, 330
        X = lambda t: L + t / 100 * (R - L)
        b += f'<rect x="{x0}" y="70" width="440" height="330" rx="8" fill="{TINT if k == 0 else "#fff"}" stroke="{col}" stroke-width="1.5"/>'
        b += text(x0 + 220, 94, title, 15, INK, weight='700')
        scale = 200
        hgt = lambda t: fn(t) * (scale if k == 0 else 120 * 200 / 120 / 120 * 1.0)
        ys = [(t, B - (fn(t) * 200 if k == 0 else fn(t) * 200 / 120 * 30)) for t in [i * 0.5 for i in range(201)]]
        poly = f'{X(0):.1f},{B} ' + ' '.join(f'{X(t):.1f},{y:.1f}' for t, y in ys) + f' {X(100):.1f},{B}'
        b += f'<polygon points="{poly}" fill="{col}" opacity="0.35" stroke="{col}" stroke-width="2"/>'
        b += f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{INK}"/>' + text(R, B + 18, '100 years', 12, MUTED, 'end') + text(L, B + 18, '0', 12, MUTED, 'start')
        b += text(L - 6, T + 20, 'heat', 11.5, MUTED, 'end') + text(L - 6, T + 34, 'trapped', 11.5, MUTED, 'end')
        words = note.split(', ')
        b += text(x0 + 220, 360, words[0] + ',', 12, INK) + text(x0 + 220, 377, words[1], 12, INK)
    b += text(480, 430, 'Shaded area for methane ÷ shaded area for CO₂ over 100 years ≈ 28 (AR5) or 27.9 (AR6). Over 20 years ≈ 81. (CO₂ drawn 30 times taller than true scale.)', 12.5, RED, weight='700')
    b += text(480, 452, 'Change the period and the ratio changes: that is why every GWP needs a time horizon.', 12.5, INK)
    svg('gwp-area-explained.svg', w, h, 'How a global warming potential is calculated',
        'Two panels. One kilogram of methane traps far more heat at first but most has gone within a few decades, so its curve is tall and short. One kilogram of CO2 traps much less heat but stays for centuries, so its curve is low and long. '
        'The GWP is the area under the gas curve divided by the area under the CO2 curve over the chosen period: about 28 for methane over 100 years and about 81 over 20 years.', b)


def gwp_bars():
    w, h = 960, 520
    L, R = 250, 900
    lo, hi = -1, 5
    X = lambda v: L + (math.log10(max(v, 0.1)) - lo) / (hi - lo) * (R - L)
    b = text(20, 30, 'Same gas, two numbers: GWP over 20 and 100 years', 20, INK, 'start', '700')
    b += text(20, 52, 'IPCC AR6 values, log scale. Short-lived gases fall sharply between 20 and 100 years; long-lived ones hold or rise.', 13, MUTED, 'start')
    data = [('HFO-1234yf (12 days)', 1.81, 0.501), ('Methane (11.8 years)', 81.2, 27.9), ('HFC-32 (5.4 years)', 2690, 771),
            ('HFC-134a (14 years)', 4140, 1530), ('Nitrous oxide (109 years)', 273, 273), ('CF₄ (50,000 years)', 5300, 7380), ('SF₆ (1,000 years)', 18200, 24300)]
    for i, (lab, g20, g100) in enumerate(data):
        y = 85 + i * 58
        b += text(L - 12, y + 22, lab, 13, INK, 'end', '700')
        b += f'<rect x="{L}" y="{y}" width="{X(g20)-L:.1f}" height="18" fill="{RED}" opacity="0.85"><title>{e(lab)} GWP-20 {g20}</title></rect>'
        b += f'<rect x="{L}" y="{y+21}" width="{X(g100)-L:.1f}" height="18" fill="{INK}"><title>{e(lab)} GWP-100 {g100}</title></rect>'
        b += text(X(g20) + 6, y + 14, f'{g20:,}'.rstrip('0').rstrip('.') if isinstance(g20, float) and g20 < 10 else f'{g20:,}', 11.5, RED, 'start', '700')
        b += text(X(g100) + 6, y + 35, f'{g100}' if g100 < 10 else f'{g100:,}', 11.5, INK, 'start', '700')
    for v, t in [(0.1, '0.1'), (1, '1'), (10, '10'), (100, '100'), (1000, '1,000'), (10000, '10,000'), (100000, '100,000')]:
        b += f'<line x1="{X(v):.1f}" y1="490" x2="{X(v):.1f}" y2="496" stroke="{INK}"/>' + text(X(v), 512, t, 11.5, INK)
    b += f'<line x1="{L}" y1="490" x2="{R}" y2="490" stroke="{INK}"/>'
    b += f'<rect x="700" y="62" width="12" height="12" fill="{RED}"/>' + text(718, 73, 'GWP-20', 12, INK, 'start') + f'<rect x="790" y="62" width="12" height="12" fill="{INK}"/>' + text(808, 73, 'GWP-100', 12, INK, 'start')
    svg('gwp-20-vs-100.svg', w, h, 'GWP over 20 and 100 years for seven gases',
        'IPCC AR6 values. HFO-1234yf, 12 days: 1.81 over 20 years, 0.501 over 100. Methane, 11.8 years: 81.2 and 27.9. HFC-32, 5.4 years: 2,690 and 771. HFC-134a, 14 years: 4,140 and 1,530. Nitrous oxide, 109 years: 273 and 273. '
        'CF4, 50,000 years: 5,300 and 7,380. SF6, 1,000 years: 18,200 and 24,300. Short-lived gases fall between 20 and 100 years; long-lived ones hold or rise.', b)


def methane_fates():
    w, h = 960, 540
    b = arrow_defs(INK, RED, GREEN, BLUE)
    b += text(20, 30, 'One kilogram of methane: vent it, burn it or use it', 20, INK, 'start', '700')
    b += text(20, 52, 'Burning turns a potent gas into a weaker one. Using it to replace fossil fuel does better still.', 13, MUTED, 'start')
    b += f'<rect x="20" y="210" width="190" height="110" rx="8" fill="{TINT}" stroke="{RED}" stroke-width="1.8"/>'
    b += text(115, 240, '1 kg methane', 16, INK, weight='700') + text(115, 262, 'from landfill, slurry,', 12, MUTED) + text(115, 278, 'a gas leak or a mine', 12, MUTED)
    rows = [(90, 'Vented to air', '28 kg CO₂e', 'GWP-100, AR5 (non-fossil)', RED, 'CH₄ escapes unchanged'),
            (240, 'Flared', '2.75 kg CO₂', 'about 90% less warming*', '#C98B3A', 'CH₄ + 2O₂ → CO₂ + 2H₂O'),
            (390, 'Burned for heat or power', '2.75 kg CO₂ and', 'fossil gas not burned', GREEN, 'same reaction, useful energy')]
    for y, t, big, sub, col, eq in rows:
        b += arr(212, 265, 420, y + 45, 1 if col == RED else (2 if col == GREEN else 0), col, 2.5)
        b += f'<rect x="425" y="{y}" width="510" height="95" rx="8" fill="#fff" stroke="{col}" stroke-width="2"/>'
        b += text(445, y + 28, t, 15, INK, 'start', '700') + text(445, y + 52, eq, 13, MUTED, 'start', extra=MONO if '→' in eq else '')
        b += text(915, y + 34, big, 17, col, 'end', '700') + text(915, y + 58, sub, 12, MUTED, 'end')
    b += text(20, 512, '* 16 g of methane burns to 44 g of CO₂, so 1 kg becomes 2.75 kg. If the methane is biogenic (landfill, slurry), inventories count that CO₂ as zero and the saving is close to 100%.', 11.5, MUTED, 'start')
    b += text(20, 530, 'Flares are not perfect: some methane slips through unburned, which is why EU rules set flare-efficiency requirements.', 11.5, MUTED, 'start')
    svg('methane-vent-flare-use.svg', w, h, 'What happens to one kilogram of methane if it is vented, flared or used',
        'One kilogram of methane vented to the air counts as 28 kilograms of CO2 equivalent (GWP-100, AR5). Flared, it burns (methane plus two oxygen gives CO2 and two water) to 2.75 kilograms of CO2, about 90% less warming. '
        'Burned for heat or power, it gives the same 2.75 kilograms but replaces fossil fuel that would otherwise be burned. If the methane is biogenic, inventories count the CO2 as zero. Flares are not perfect and some methane slips through.', b)


def capture_by_gas():
    w, h = 960, 430
    b = text(20, 30, 'Can we capture it? Gas by gas', 20, INK, 'start', '700')
    b += text(20, 52, '“Capture” means different things for different gases. For most, the answer is: stop it at source, or destroy it.', 13, MUTED, 'start')
    cols = [('Carbon dioxide', INK, ['Capture from chimneys (CCS)', 'Capture from air (DACCS)', 'Store in rock or use', 'Plants and soils too'], 'Yes: capture and store'),
            ('Methane', RED, ['Collect from landfill, digesters,', 'slurry stores, coal mines', 'Burn for energy or flare', 'Feed additives cut cow methane'], 'Collect and burn it'),
            ('Nitrous oxide', '#B05A5A', ['Factories: catalysts split it', '2N₂O → 2N₂ + O₂', 'Fields: no capture; use', 'inhibitors and less N'], 'Destroy at source'),
            ('F-gases', BLUE, ['Recover from equipment', 'at service and end of life', 'Reclaim, reuse or destroy', 'at high temperature'], 'Recover and destroy')]
    for i, (name, col, ls, verdict) in enumerate(cols):
        x = 20 + i * 232
        b += f'<rect x="{x}" y="75" width="222" height="330" rx="8" fill="#fff" stroke="{col}" stroke-width="2"/>'
        b += f'<rect x="{x}" y="75" width="222" height="44" rx="8" fill="{col}"/>'
        b += text(x + 111, 104, name, 15, '#fff', weight='700')
        for j, ln in enumerate(ls):
            b += text(x + 111, 160 + j * 30, ln, 12.5, INK, extra=MONO if '→' in ln else '')
        b += f'<rect x="{x+12}" y="330" width="198" height="56" rx="6" fill="{TINT}"/>'
        b += text(x + 111, 364, verdict, 13.5, col, weight='700')
    svg('capture-by-gas.svg', w, h, 'Capture options for each greenhouse gas',
        'Four columns. Carbon dioxide: captured from chimneys (CCS) or the air (DACCS) and stored or used; plants and soils too. Methane: collected from landfill, digesters, slurry stores and coal mines and burned for energy or flared; feed additives cut cow methane. '
        'Nitrous oxide: in factories, catalysts split it into nitrogen and oxygen (2 N2O gives 2 N2 plus O2); on fields there is no capture, only inhibitors and using less nitrogen. F-gases: recovered from equipment at service and end of life, then reclaimed, reused or destroyed at high temperature.', b)


def natural_vs_human():
    w, h = 960, 500
    L, W = 250, 540
    b = text(20, 30, 'How much of each gas is natural, and how much have we added?', 20, INK, 'start', '700')
    b += text(20, 52, 'Share of today’s concentration that was there before industry (grey) and that people have added (red).', 13, MUTED, 'start')
    rows = [('Carbon dioxide', 65, '426.8 ppm in 2025; 153% of 1750'),
            ('Methane', 37, '1,948 ppb in 2025; 267% of 1750'),
            ('Nitrous oxide', 79, '339.1 ppb in 2025; 126% of 1750'),
            ('CF₄ (a PFC)', 41, '34 ppt natural (rocks); 83 ppt in 2016'),
            ('SF₆', 0, '12.2 ppt in 2025; man-made'),
            ('C₂F₆, NF₃, HFCs', 0, 'Entirely man-made')]
    for i, (lab, nat, note) in enumerate(rows):
        y = 85 + i * 62
        b += text(L - 12, y + 24, lab, 14, INK, 'end', '700')
        b += f'<rect x="{L}" y="{y+6}" width="{W*nat/100:.1f}" height="28" fill="{GREY}"/>'
        b += f'<rect x="{L+W*nat/100:.1f}" y="{y+6}" width="{W*(100-nat)/100:.1f}" height="28" fill="{RED}"/>'
        if nat:
            b += text(L + W * nat / 200, y + 25, f'{nat}% natural', 12, '#fff', weight='700')
        b += text(L + W * (100 + nat) / 200, y + 25, f'{100-nat}% added', 12, '#fff', weight='700')
        b += text(L + W + 12, y + 18, note.split('; ')[0], 11, MUTED, 'start')
        if '; ' in note:
            b += text(L + W + 12, y + 32, note.split('; ')[1], 11, MUTED, 'start')
    b += text(20, 470, 'From WMO 2025 concentrations as a share of 1750 levels (my arithmetic). CF₄ from Trudinger et al. 2016 and AGAGE. Rounded.', 11.5, MUTED, 'start')
    svg('ghg-natural-vs-added.svg', w, h, 'Natural and human-added shares of each greenhouse gas',
        'Share of today’s concentration that was there before industry: carbon dioxide about 65% (426.8 ppm in 2025, 153% of 1750); methane about 37% (1,948 ppb, 267% of 1750); nitrous oxide about 79% (339.1 ppb, 126% of 1750); '
        'CF4 about 41% (34 ppt natural background from rocks, 83 ppt by 2016); SF6, C2F6, NF3 and HFCs entirely man-made.', b)


def carbon_reservoirs():
    w, h = 960, 520
    L, R = 300, 900
    lo, hi = 2, 10
    X = lambda v: L + (math.log10(v) - lo) / (hi - lo) * (R - L)
    b = text(20, 30, 'Where Earth’s carbon is: from the air to the mantle', 20, INK, 'start', '700')
    b += text(20, 52, 'Billions of tonnes of carbon (GtC), log scale: each step is ten times the last. Estimates for the deep Earth are uncertain.', 13, MUTED, 'start')
    rows = [('Atmosphere', 900, 900, BLUE, 'about 900'),
            ('Land plants', 450, 450, GREEN, 'about 450'),
            ('Soils (top metre)', 1500, 2400, '#6B4F3A', '1,500–2,400'),
            ('Permafrost region', 1300, 1600, '#9c7f66', '1,300–1,600'),
            ('Oceans', 38000, 38000, '#1f3b57', 'about 38,000'),
            ('Everything above the surface', 43500, 43500, GREY, 'about 43,500'),
            ('Crust, mantle and core', 1.85e9, 1.85e9, INK, 'about 1,850,000,000 (over 99.99%)')]
    for i, (lab, a, z, c, t) in enumerate(rows):
        y = 80 + i * 56
        b += text(L - 12, y + 22, lab, 13.5, INK, 'end', '700')
        b += f'<rect x="{L}" y="{y+6}" width="{X(z)-L:.1f}" height="26" rx="3" fill="{c}"/>'
        if z > a:
            b += f'<rect x="{X(a):.1f}" y="{y+6}" width="{X(z)-X(a):.1f}" height="26" fill="#fff" opacity="0.35"/>'
        tx = X(z) + 8
        anc = 'start'
        if tx > 760:
            tx, anc, col = X(z) - 8, 'end', '#fff'
        else:
            col = INK
        b += text(tx, y + 24, t, 12.5, col, anc, '700')
    for v, t in [(100, '100'), (1e3, '1,000'), (1e4, '10,000'), (1e5, '100,000'), (1e6, '1 million'), (1e7, '10 million'), (1e8, '100 million'), (1e9, '1 billion'), (1e10, '10 billion')]:
        b += f'<line x1="{X(v):.1f}" y1="474" x2="{X(v):.1f}" y2="480" stroke="{INK}"/>' + text(X(v), 495, t, 11, INK)
    b += f'<line x1="{L}" y1="474" x2="{R}" y2="474" stroke="{INK}"/>'
    b += text(20, 515, 'The air holds about 0.00005% of Earth’s carbon. Fossil fuels are a small slice of the crust’s store, moved to the air in two centuries.', 11.5, RED, 'start', '700')
    svg('earth-carbon-reservoirs.svg', w, h, 'Where Earth’s carbon is stored',
        'Billions of tonnes of carbon on a log scale: atmosphere about 900; land plants about 450; soils in the top metre 1,500 to 2,400; permafrost region 1,300 to 1,600; oceans about 38,000; everything above the surface about 43,500; '
        'crust, mantle and core about 1.85 billion, over 99.99%. The air holds about 0.00005% of Earth’s carbon.', b)


if __name__ == '__main__':
    decay(); area(); gwp_bars(); methane_fates(); capture_by_gas(); natural_vs_human(); carbon_reservoirs()
    print('ok')
