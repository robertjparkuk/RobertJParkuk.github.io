"""Diagrams for the Learn explainer "Why is everything counted as carbon?" (v0.35.0, 17 Nov 2026).
Writes accessible SVGs to assets/learn/. Brand: red #A61C1C, ink #1A1A1A, grey #8C8C8C.
Usage: python3 _scripts/learn/gases.py <repo_root>

Values: band centres are standard spectroscopy (IPCC AR6 WG1 Ch7, HITRAN, NIST);
lifetimes are IPCC AR6 WG1 Table 7.SM.7 (SF6 1,000 yr, NF3 569, CF4 50,000, CH4 11.8, N2O 109, HFC-134a 14). Checked 17 Nov 2026.
"""
import sys, os, html, math

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
OUT = os.path.join(ROOT, 'assets/learn')
os.makedirs(OUT, exist_ok=True)
RED, INK, GREY, MUTED, RULE, TINT = '#A61C1C', '#1A1A1A', '#8C8C8C', '#5A5A5A', '#E6E2E0', '#FAF3F3'
FONT = "'Source Sans 3','Source Sans Pro',Arial,sans-serif"
e = html.escape

# Atom colours: carbon ink, oxygen red, everything else in greys/tints so the page stays on brand.
ATOM = {'C': (INK, '#fff'), 'O': (RED, '#fff'), 'H': ('#fff', INK), 'N': ('#5A5A5A', '#fff'),
        'F': ('#F2D6D6', INK), 'S': ('#D9D9D9', INK)}
RAD = {'C': 17, 'O': 17, 'N': 17, 'S': 21, 'F': 14, 'H': 11}


def svg(name, w, h, title, desc, body):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" font-family="{FONT}">'
         f'<title id="t">{e(title)}</title><desc id="d">{e(desc)}</desc><rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(s)


def text(x, y, t, size=13, fill=INK, anchor='middle', weight='400', extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {extra}>{e(t)}</text>'


def atom(x, y, el, back=False):
    fill, ink = ATOM[el]
    r = RAD[el]
    op = ' opacity="0.55"' if back else ''
    return (f'<g{op}><circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="1.5"/>'
            + text(x, y + 4.5, el, 12 if r < 15 else 13, ink, weight='700') + '</g>')


def bond(x1, y1, x2, y2, order=1, dashed=False):
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L * 4, dx / L * 4
    dash = ' stroke-dasharray="4 3"' if dashed else ''
    offs = {1: [0], 2: [-1, 1], 3: [-1.6, 0, 1.6]}[order]
    return ''.join(f'<line x1="{x1+nx*o:.1f}" y1="{y1+ny*o:.1f}" x2="{x2+nx*o:.1f}" y2="{y2+ny*o:.1f}" stroke="{INK}" stroke-width="2.2"{dash}/>' for o in offs)


def molecule(cx, cy, centre, ligands, order=1, back=(), dashed=()):
    """ligands: list of (element, angle_deg, length). Angle 0 = right, 90 = up."""
    out, atoms = '', ''
    for i, (el, ang, L) in enumerate(ligands):
        a = math.radians(ang)
        x, y = cx + L * math.cos(a), cy - L * math.sin(a)
        o = order[i] if isinstance(order, (list, tuple)) else order
        out += bond(cx, cy, x, y, o, i in dashed)
        atoms += atom(x, y, el, i in back)
    return out + (atom(cx, cy, centre) if centre else '') + atoms


def panel(x, y, w, h, name, formula, shape, verdict, ghg=True):
    b = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{TINT if ghg else "#f6f6f6"}" stroke="{RED if ghg else GREY}" stroke-width="1.5"/>'
    b += text(x + w / 2, y + 24, name, 15, INK, weight='700')
    b += text(x + w / 2, y + 41, formula, 12, MUTED)
    b += text(x + w / 2, y + h - 30, shape, 12, INK)
    b += text(x + w / 2, y + h - 13, verdict, 11.5, RED if ghg else MUTED, weight='600')
    return b


def molecules():
    w, h = 960, 640
    pw, ph, gap = 222, 268, 14
    x0, y0 = 20, 70
    b = text(20, 30, 'The molecules behind the numbers', 20, INK, 'start', '700')
    b += text(20, 52, 'Simplified 2D models. Bond angles from standard references. Paler atoms sit behind the page.', 13, MUTED, 'start')
    cells = []
    for r in range(2):
        for c in range(4):
            cells.append((x0 + c * (pw + gap), y0 + r * (ph + 20)))

    # 1 N2 and O2 (contrast)
    x, y = cells[0]
    b += panel(x, y, pw, ph, 'Nitrogen and oxygen', 'N₂ and O₂: 99% of dry air', 'Two identical atoms', 'No dipole to shake: not a GHG', ghg=False)
    b += bond(x + 70, y + 110, x + 112, y + 110, 3) + atom(x + 70, y + 110, 'N') + atom(x + 112, y + 110, 'N')
    b += bond(x + 110, y + 175, x + 152, y + 175, 2) + atom(x + 110, y + 175, 'O') + atom(x + 152, y + 175, 'O')

    # 2 CO2 linear
    x, y = cells[1]
    b += panel(x, y, pw, ph, 'Carbon dioxide', 'CO₂', 'Linear, 180°', 'Bends and stretches: absorbs at 15 µm')
    b += molecule(x + pw / 2, y + 140, 'C', [('O', 0, 52), ('O', 180, 52)], 2)

    # 3 H2O bent 104.5
    x, y = cells[2]
    b += panel(x, y, pw, ph, 'Water vapour', 'H₂O', 'Bent, 104.5°', 'Permanent dipole: absorbs widely')
    b += molecule(x + pw / 2, y + 125, 'O', [('H', -90 + 52.25, 50), ('H', -90 - 52.25, 50)])
    b += f'<path d="M{x+pw/2-14:.1f} {y+152:.1f} A 30 30 0 0 0 {x+pw/2+14:.1f} {y+152:.1f}" fill="none" stroke="{RED}" stroke-width="1.5"/>'

    # 4 CH4 tetrahedral
    x, y = cells[3]
    b += panel(x, y, pw, ph, 'Methane', 'CH₄', 'Tetrahedral, 109.5°', 'Absorbs at 3.3 and 7.7 µm')
    b += molecule(x + pw / 2, y + 140, 'C', [('H', 90, 50), ('H', 210, 50), ('H', 330, 50), ('H', 270, 30)], 1, back=(3,), dashed=(3,))

    # 5 N2O linear N-N-O
    x, y = cells[4]
    b += panel(x, y, pw, ph, 'Nitrous oxide', 'N₂O', 'Linear, N–N–O', 'Absorbs at 4.5, 7.8 and 17 µm')
    cx, cy = x + pw / 2, y + 140
    b += bond(cx - 54, cy, cx, cy, 3) + bond(cx, cy, cx + 54, cy, 1)
    b += atom(cx - 54, cy, 'N') + atom(cx, cy, 'N') + atom(cx + 54, cy, 'O')

    # 6 SF6 octahedral
    x, y = cells[5]
    b += panel(x, y, pw, ph, 'Sulphur hexafluoride', 'SF₆', 'Octahedral, 90°', 'Absorbs at 10.5 µm, in the window')
    b += molecule(x + pw / 2, y + 140, 'S', [('F', 90, 56), ('F', 270, 56), ('F', 0, 56), ('F', 180, 56), ('F', 40, 34), ('F', 220, 34)], 1, back=(4, 5), dashed=(4, 5))

    # 7 NF3 trigonal pyramid
    x, y = cells[6]
    b += panel(x, y, pw, ph, 'Nitrogen trifluoride', 'NF₃', 'Pyramid, about 102°', 'Absorbs near 11 µm, in the window')
    b += molecule(x + pw / 2, y + 125, 'N', [('F', 230, 52), ('F', 310, 52), ('F', 270, 30)], 1, back=(2,), dashed=(2,))
    b += f'<circle cx="{x+pw/2:.1f}" cy="{y+93:.1f}" r="5" fill="none" stroke="{MUTED}"/><circle cx="{x+pw/2+9:.1f}" cy="{y+93:.1f}" r="5" fill="none" stroke="{MUTED}"/>'
    b += text(x + pw / 2 + 48, y + 97, 'lone pair', 11, MUTED)

    # 8 CF4 tetrahedral (PFC)
    x, y = cells[7]
    b += panel(x, y, pw, ph, 'Tetrafluoromethane', 'CF₄, a PFC', 'Tetrahedral, 109.5°', 'Absorbs at 7.8 µm; lasts 50,000 years')
    b += molecule(x + pw / 2, y + 140, 'C', [('F', 90, 54), ('F', 210, 54), ('F', 330, 54), ('F', 270, 32)], 1, back=(3,), dashed=(3,))

    svg('gas-molecules.svg', w, h, 'The molecules behind the greenhouse gas numbers',
        'Eight panels of simplified ball-and-stick models. Nitrogen and oxygen, each two identical atoms with no dipole, are not greenhouse gases. '
        'Carbon dioxide is linear and absorbs at 15 micrometres. Water is bent at 104.5 degrees and absorbs widely. Methane is tetrahedral and absorbs at 3.3 and 7.7 micrometres. '
        'Nitrous oxide is linear and absorbs at 4.5, 7.8 and 17 micrometres. Sulphur hexafluoride is octahedral and absorbs at 10.5 micrometres. '
        'Nitrogen trifluoride is a pyramid of about 102 degrees and absorbs near 11 micrometres. Tetrafluoromethane is tetrahedral, absorbs at 7.8 micrometres and lasts about 50,000 years.', b)


def co2_modes():
    w, h = 900, 330
    b = text(20, 30, 'Why carbon dioxide absorbs heat: three ways to wobble', 20, INK, 'start', '700')
    b += text(20, 52, 'Infrared is absorbed only by a vibration that changes the molecule’s electrical balance (its dipole).', 13, MUTED, 'start')
    modes = [
        ('Symmetric stretch', 'Both oxygens move out together', 'No dipole change: infrared-blind', 'Seen only by Raman spectroscopy', False, 'sym'),
        ('Bend', 'The molecule flexes like a hinge', 'Dipole changes: absorbs at 15 µm', '667 cm⁻¹, right where Earth glows', True, 'bend'),
        ('Asymmetric stretch', 'Oxygens shift one way, carbon the other', 'Dipole changes: absorbs at 4.3 µm', '2,349 cm⁻¹', True, 'asym'),
    ]
    pw = 280
    for i, (name, how, verdict, wn, active, kind) in enumerate(modes):
        x = 20 + i * (pw + 10)
        b += f'<rect x="{x}" y="70" width="{pw}" height="240" rx="8" fill="{TINT if active else "#f6f6f6"}" stroke="{RED if active else GREY}" stroke-width="1.5"/>'
        b += text(x + pw / 2, 96, name, 15, INK, weight='700')
        cx, cy = x + pw / 2, 175
        if kind == 'bend':
            b += molecule(cx, cy - 10, 'C', [('O', -15, 58), ('O', 195, 58)], 2)
            b += f'<path d="M{cx-56:.1f} {cy+12:.1f} v22" stroke="{RED}" stroke-width="2.5" marker-end="url(#ar)"/><path d="M{cx+56:.1f} {cy+12:.1f} v22" stroke="{RED}" stroke-width="2.5" marker-end="url(#ar)"/>'
            b += f'<path d="M{cx:.1f} {cy-34:.1f} v-22" stroke="{RED}" stroke-width="2.5" marker-end="url(#ar)"/>'
        else:
            b += molecule(cx, cy, 'C', [('O', 0, 58), ('O', 180, 58)], 2)
            left = -1
            right = 1 if kind == 'sym' else 1
            col = MUTED if kind == 'sym' else RED
            b += f'<path d="M{cx-80:.1f} {cy:.1f} h{-22*1}" stroke="{col}" stroke-width="2.5" marker-end="url(#ar{"g" if kind=="sym" else ""})"/>'
            if kind == 'sym':
                b += f'<path d="M{cx+80:.1f} {cy:.1f} h22" stroke="{col}" stroke-width="2.5" marker-end="url(#arg)"/>'
            else:
                b += f'<path d="M{cx+80:.1f} {cy:.1f} h22" stroke="{col}" stroke-width="2.5" marker-end="url(#ar)" transform="rotate(180 {cx+91:.1f} {cy:.1f})"/>'
                b += f'<path d="M{cx-8:.1f} {cy-26:.1f} h16" stroke="{RED}" stroke-width="2.5" marker-end="url(#ar)"/>'
        b += text(x + pw / 2, 238, how, 12.5, MUTED)
        b += text(x + pw / 2, 262, verdict, 13, RED if active else MUTED, weight='700')
        b += text(x + pw / 2, 284, wn, 12, INK)
    defs = (f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{RED}"/></marker>'
            f'<marker id="arg" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{MUTED}"/></marker></defs>')
    svg('co2-vibrations.svg', w, h, 'The three ways a carbon dioxide molecule vibrates',
        'Symmetric stretch: both oxygens move out together, no change in dipole, so it does not absorb infrared. '
        'Bend: absorbs at 15 micrometres (667 per centimetre), right where Earth emits most heat. Asymmetric stretch: absorbs at 4.3 micrometres (2,349 per centimetre).', defs + b)


# Band centres (µm) and a qualitative strength 1-3 for drawing.
BANDS = [
    ('Water vapour (H₂O)', [(2.7, 3), (6.3, 3), (17, 2), (22, 3), (28, 3)], 'rot'),
    ('Carbon dioxide (CO₂)', [(2.7, 1), (4.3, 3), (15, 3)], ''),
    ('Methane (CH₄)', [(3.3, 2), (7.7, 3)], ''),
    ('Nitrous oxide (N₂O)', [(4.5, 3), (7.8, 2), (17, 1)], ''),
    ('Ozone (O₃)', [(9.6, 3), (14.2, 1)], ''),
    ('CF₄ (a PFC)', [(7.8, 3)], ''),
    ('C₂F₆ (a PFC)', [(8.0, 2), (8.9, 3)], ''),
    ('HFC-134a', [(8.4, 2), (9.0, 2), (11.0, 1)], ''),
    ('Sulphur hexafluoride (SF₆)', [(10.5, 3)], ''),
    ('Nitrogen trifluoride (NF₃)', [(11.0, 3)], ''),
]


def spectrum():
    w, h = 960, 660
    L, R, T = 250, 930, 100
    lo, hi = math.log10(2), math.log10(30)
    X = lambda um: L + (math.log10(um) - lo) / (hi - lo) * (R - L)
    b = text(20, 30, 'Where each gas catches Earth’s heat', 20, INK, 'start', '700')
    b += text(20, 52, 'Main infrared absorption bands (wavelength in micrometres, log scale). Earth radiates most strongly around 10 µm.', 13, MUTED, 'start')
    # Earth emission curve (Planck at 288 K), scaled
    def planck(um, T=288.0):
        l = um * 1e-6
        return 1 / (l ** 5 * (math.exp(1.4388e-2 / (l * T)) - 1))
    pts = [(um, planck(um)) for um in [2 + i * 0.1 for i in range(281)]]
    mx = max(p for _, p in pts)
    top, base = T, T + 70
    path = 'M' + ' L'.join(f'{X(um):.1f} {base - p / mx * 62:.1f}' for um, p in pts)
    # window
    b += f'<rect x="{X(8):.1f}" y="{T-8}" width="{X(14)-X(8):.1f}" height="{h-T-40}" fill="{TINT}"/>'
    b += text((X(8) + X(14)) / 2, T + 2, 'The “atmospheric window”, 8–14 µm', 12.5, RED, weight='700')
    b += f'<path d="{path} L{X(30):.1f} {base} L{X(2):.1f} {base} Z" fill="#ececec" stroke="{GREY}" stroke-width="1.5"/>'
    b += text(L - 10, base - 25, 'Earth’s glow', 12.5, MUTED, 'end', '600')
    b += text(L - 10, base - 9, '(about 15 °C)', 11.5, MUTED, 'end')
    row0, rh = T + 100, 40
    for i, (name, bands, kind) in enumerate(BANDS):
        y = row0 + i * rh
        b += f'<line x1="{L}" y1="{y}" x2="{R}" y2="{y}" stroke="{RULE}"/>'
        b += text(L - 10, y + 4, name, 13, INK, 'end', '600' if i < 5 else '400')
        for um, s in bands:
            hw = {1: 3, 2: 5, 3: 7}[s]
            col = RED if 8 <= um <= 14 else INK
            b += f'<rect x="{X(um)-hw:.1f}" y="{y-9}" width="{2*hw}" height="18" rx="3" fill="{col}" opacity="{0.45 + 0.18*s:.2f}"><title>{e(name)}: about {um} µm</title></rect>'
        if kind == 'rot':
            b += f'<rect x="{X(18):.1f}" y="{y-6}" width="{X(30)-X(18):.1f}" height="12" rx="3" fill="{INK}" opacity="0.35"/>'
            b += text(R, y + 22, 'rotational band, on into microwaves', 11, MUTED, 'end')
    for um in [2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30]:
        b += f'<line x1="{X(um):.1f}" y1="{h-58}" x2="{X(um):.1f}" y2="{h-52}" stroke="{INK}"/>' + text(X(um), h - 38, str(um), 12, INK)
    b += f'<line x1="{L}" y1="{h-58}" x2="{R}" y2="{h-58}" stroke="{INK}"/>'
    b += text((L + R) / 2, h - 16, 'Wavelength (µm). Red bands fall in the window, where little else absorbs.', 12.5, MUTED)
    svg('gas-absorption-bands.svg', w, h, 'Where each greenhouse gas absorbs infrared',
        'A chart of main infrared absorption bands from 2 to 30 micrometres against Earth’s thermal emission, which peaks near 10 micrometres. '
        'Water vapour absorbs at 2.7 and 6.3 micrometres and across a rotational band beyond about 18 micrometres. Carbon dioxide at 4.3 and 15. '
        'Methane at 3.3 and 7.7. Nitrous oxide at 4.5, 7.8 and 17. Ozone at 9.6. The fluorinated gases CF4, C2F6, HFC-134a, sulphur hexafluoride at 10.5 and nitrogen trifluoride at 11 '
        'all absorb inside the 8 to 14 micrometre atmospheric window, where little else does, which is why each molecule is so potent.', b)


def fates():
    w, h = 960, 660
    L, R = 150, 940
    b = text(20, 30, 'Where each gas meets its end', 20, INK, 'start', '700')
    b += text(20, 52, 'Layers not to scale. Lifetimes are IPCC AR6 figures; the longer the climb, the longer the gas lasts.', 13, MUTED, 'start')
    layers = [('Thermosphere', 'above 85 km', 70, 70, '#f6f6f6'),
              ('Mesosphere', '50–85 km', 140, 110, TINT),
              ('Stratosphere', '12–50 km', 250, 150, '#fff'),
              ('Troposphere', '0–12 km', 400, 170, '#f6f6f6')]
    for name, alt, y, hh, fill in layers:
        b += f'<rect x="{L}" y="{y}" width="{R-L}" height="{hh}" fill="{fill}" stroke="{RULE}"/>'
        b += text(L - 10, y + hh / 2, name, 13, INK, 'end', '700') + text(L - 10, y + hh / 2 + 16, alt, 11.5, MUTED, 'end')
    b += f'<rect x="{L}" y="570" width="{R-L}" height="14" fill="#cfcfcf"/>' + text(L - 10, 582, 'Ground', 12, MUTED, 'end')
    cols = [
        ('Water vapour', 'about 9 days', 545, 'Condenses and rains out', 'troposphere'),
        ('HFC-134a', '14 years', 445, 'Hydroxyl radical (OH) pulls off a hydrogen', 'troposphere'),
        ('Methane', '11.8 years', 445, 'OH pulls off a hydrogen → CO → CO₂ + water', 'troposphere'),
        ('Nitrous oxide', '109 years', 300, 'UV splits it; O(¹D) turns some into NO, which eats ozone', 'stratosphere'),
        ('NF₃', '569 years', 290, 'Stratospheric UV and O(¹D)', 'stratosphere'),
        ('SF₆', '1,000 years*', 175, 'Grabs free electrons; Lyman-α UV', 'mesosphere'),
        ('CF₄', '50,000 years', 95, 'Only the hardest UV, or a furnace', 'thermosphere'),
    ]
    cw = (R - L) / len(cols)
    for i, (name, life, yend, how, _) in enumerate(cols):
        x = L + cw * i + cw / 2
        b += f'<line x1="{x:.1f}" y1="570" x2="{x:.1f}" y2="{yend+14}" stroke="{RED}" stroke-width="3" marker-end="url(#up)"/>'
        b += f'<circle cx="{x:.1f}" cy="{yend:.1f}" r="9" fill="{RED}"/>'
        b += text(x, 600, name, 12.5, INK, weight='700') + text(x, 614, life, 11.5, MUTED)
        # wrap "how" into lines of ~16 chars
        words, lines, cur = how.split(), [], ''
        for wd in words:
            if len(cur) + len(wd) + 1 > 17:
                lines.append(cur); cur = wd
            else:
                cur = (cur + ' ' + wd).strip()
        lines.append(cur)
        for j, ln in enumerate(lines):
            b += text(x, yend - 18 - (len(lines) - 1 - j) * 14, ln, 11, INK)
    b += text(R, h - 8, '* IPCC cut SF₆ from 3,200 to 1,000 years in 2021; recent studies range from about 850 to 1,300.', 11, MUTED, 'end')
    defs = f'<defs><marker id="up" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="{RED}"/></marker></defs>'
    svg('gas-fates.svg', w, h, 'Where in the atmosphere each greenhouse gas is destroyed',
        'Water vapour rains out of the lower atmosphere in about nine days. HFC-134a (14 years) and methane (11.8 years) are broken down in the troposphere by the hydroxyl radical, '
        'which pulls off a hydrogen atom; methane ends up as carbon dioxide and water. Nitrous oxide (109 years) and nitrogen trifluoride (569 years) rise to the stratosphere and are split by ultraviolet light '
        'and excited oxygen atoms; some nitrous oxide becomes nitric oxide, which destroys ozone. Sulphur hexafluoride (about 1,000 years; IPCC used 3,200 until 2021) is destroyed only in the mesosphere by free electrons and hard ultraviolet. '
        'CF4 (50,000 years) survives almost everything.', defs + b)


def fingerprint():
    w, h = 900, 400
    b = text(20, 30, 'The fingerprint test: Sun or greenhouse gases?', 20, INK, 'start', '700')
    b += text(20, 52, 'A brighter Sun would warm every layer. Extra CO₂ warms the lower air and cools the upper stratosphere.', 13, MUTED, 'start')
    panels = [('If the Sun were the cause', ['warmer', 'warmer'], 'What we would expect', False),
              ('If greenhouse gases are the cause', ['cooler', 'warmer'], 'What satellites and balloons measure', True)]
    for i, (title, temps, foot, real) in enumerate(panels):
        x = 20 + i * 440
        b += f'<rect x="{x}" y="70" width="420" height="300" rx="8" fill="{TINT if real else "#f6f6f6"}" stroke="{RED if real else GREY}" stroke-width="1.5"/>'
        b += text(x + 210, 98, title, 15, INK, weight='700')
        for j, (layer, alt) in enumerate([('Upper stratosphere', 'about 25–50 km'), ('Troposphere', '0–12 km')]):
            y = 120 + j * 100
            b += f'<rect x="{x+20}" y="{y}" width="380" height="88" rx="6" fill="#fff" stroke="{RULE}"/>'
            b += text(x + 36, y + 38, layer, 14, INK, 'start', '700') + text(x + 36, y + 56, alt, 12, MUTED, 'start')
            warm = temps[j] == 'warmer'
            col = RED if warm else '#4A6A8A'
            ax = x + 300
            if warm:
                b += f'<path d="M{ax} {y+70} v-46" stroke="{col}" stroke-width="5" marker-end="url(#fu)"/>'
            else:
                b += f'<path d="M{ax} {y+18} v46" stroke="{col}" stroke-width="5" marker-end="url(#fd)"/>'
            b += text(ax + 22, y + 50, temps[j], 14, col, 'start', '700')
        b += f'<circle cx="{x+380}" cy="98" r="0" fill="none"/>'
        b += text(x + 210, 350, foot, 13, RED if real else MUTED, weight='700' if real else '400')
    defs = (f'<defs><marker id="fu" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="{RED}"/></marker>'
            f'<marker id="fd" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="#4A6A8A"/></marker></defs>')
    svg('sun-fingerprint.svg', w, h, 'The fingerprint test: Sun or greenhouse gases?',
        'Two panels. If a brighter Sun were warming the planet, both the upper stratosphere and the troposphere would warm. '
        'If greenhouse gases are the cause, the troposphere warms while the upper stratosphere cools, because the extra carbon dioxide traps heat low down and radiates more of it away to space high up. '
        'The second pattern is what satellites and weather balloons measure.', defs + b)


if __name__ == '__main__':
    molecules(); co2_modes(); spectrum(); fates(); fingerprint()
    print('ok')
