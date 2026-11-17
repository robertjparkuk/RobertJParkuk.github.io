"""Diagrams for the Learn section (v0.34.0, 17 Nov 2026).
Writes accessible SVGs to assets/learn/. Brand: red #A61C1C, ink #1A1A1A, grey #8C8C8C.
Usage: python3 _scripts/learn/diagrams.py <repo_root>
"""
import sys, os, html, math

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
OUT = os.path.join(ROOT, 'assets/learn')
os.makedirs(OUT, exist_ok=True)
RED, INK, GREY, MUTED, RULE, TINT = '#A61C1C', '#1A1A1A', '#8C8C8C', '#5A5A5A', '#E6E2E0', '#FAF3F3'
FONT = "'Source Sans 3','Source Sans Pro',Arial,sans-serif"
e = html.escape


def svg(name, w, h, title, desc, body):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" font-family="{FONT}">'
         f'<title id="t">{e(title)}</title><desc id="d">{e(desc)}</desc><rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>')
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(s)


def text(x, y, t, size=13, fill=INK, anchor='middle', weight='400', style=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {style}>{e(t)}</text>'


def bracket(x1, x2, y, label, colour, up=True, sub=''):
    d = -1 if up else 1
    p = f'<path d="M{x1} {y} v{8*d} H{x2} v{-8*d}" fill="none" stroke="{colour}" stroke-width="2.5"/>'
    ty = y + (22 if not up else -14) * (1 if not up else 1) * (1 if not up else 1)
    ty = y - 16 if up else y + 26
    p += text((x1 + x2) / 2, ty, label, 14, colour, weight='700')
    if sub:
        p += text((x1 + x2) / 2, ty + (16 if not up else -16 if False else 16) if not up else ty - 16, sub, 12, MUTED)
    return p


def modules():
    # Life cycle stages (EN 15978 / EN 15804 module letters)
    w, h = 900, 470
    left, top, bh = 30, 190, 74
    stages = [('A1–A3', 'Product', 'Raw materials, transport to factory, manufacture', 145),
              ('A4–A5', 'Construction', 'Transport to site, building or installing', 115),
              ('B1–B5', 'Use: upkeep', 'Use, maintenance, repair, replacement, refurbishment', 155),
              ('B6–B7', 'Use: running', 'Energy and water used to run it', 115),
              ('C1–C4', 'End of life', 'Demolition, transport, waste processing, disposal', 150),
              ('D', 'Beyond', 'Reuse, recovery, recycling: reported separately', 115)]
    xs, x = [], left
    for st in stages:
        xs.append((x, x + st[3])); x += st[3] + 6
    b = text(left, 30, 'The carbon life cycle, stage by stage', 20, INK, 'start', '700')
    b += text(left, 52, 'Module letters as used in the European standards for buildings and construction products (EN 15978, EN 15804)', 13, MUTED, 'start')
    for (x1, x2), (code, name, d, _) in zip(xs, stages):
        op = code == 'B6–B7'
        fill = '#fff' if op else (TINT if code != 'D' else '#f4f4f4')
        stroke = GREY if op else (RED if code != 'D' else GREY)
        dash = ' stroke-dasharray="5 4"' if code == 'D' else ''
        b += f'<rect x="{x1}" y="{top}" width="{x2-x1}" height="{bh}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}><title>{e(code)} {e(name)}: {e(d)}</title></rect>'
        b += text((x1 + x2) / 2, top + 27, code, 17, INK, weight='700')
        b += text((x1 + x2) / 2, top + 48, name, 13, MUTED)
    # brackets above
    a1, a5 = xs[0][0], xs[1][1]
    b += bracket(a1, xs[0][1], top - 12, 'Cradle to gate', INK, True)
    b += bracket(a1, a5, top - 62, 'Upfront carbon (A1–A5)', RED, True)
    # embodied: A1-B5 and C1-C4 (two arms joined by a dashed bridge over B6-B7)
    yb = top + bh + 18
    b += f'<path d="M{a1} {yb} v10 H{xs[2][1]} v-10" fill="none" stroke="{RED}" stroke-width="2.5"/>'
    b += f'<path d="M{xs[4][0]} {yb} v10 H{xs[4][1]} v-10" fill="none" stroke="{RED}" stroke-width="2.5"/>'
    b += f'<path d="M{xs[2][1]} {yb+10} H{xs[4][0]}" fill="none" stroke="{RED}" stroke-width="1.5" stroke-dasharray="3 4"/>'
    b += text((a1 + xs[4][1]) / 2, yb + 32, 'Embodied carbon: everything except running the building or product (B6–B7)', 14, RED, weight='700')
    b += f'<path d="M{xs[3][0]} {yb+50} v10 H{xs[3][1]} v-10" fill="none" stroke="{GREY}" stroke-width="2.5"/>'
    b += text((xs[3][0] + xs[3][1]) / 2, yb + 78, 'Operational carbon', 14, MUTED, weight='700')
    b += f'<path d="M{a1} {yb+100} v10 H{xs[4][1]} v-10" fill="none" stroke="{INK}" stroke-width="2.5"/>'
    b += text((a1 + xs[4][1]) / 2, yb + 128, 'Cradle to grave = whole-life carbon (A to C)', 14, INK, weight='700')
    b += text(xs[5][0] + (xs[5][1]-xs[5][0]) / 2, yb + 128, '+ D: cradle to cradle', 13, MUTED)
    b += text(left, h - 14, 'Robert J. Park · robertjpark.co.uk/learn · Simplified; see the standards for the full module definitions.', 12, MUTED, 'start')
    svg('life-cycle-stages.svg', w, h, 'The carbon life cycle, stage by stage',
        'Six blocks from left to right: A1 to A3 product stage; A4 to A5 construction; B1 to B5 upkeep in use; B6 to B7 energy and water used in operation; C1 to C4 end of life; D reuse and recycling beyond the system boundary, reported separately. Cradle to gate covers A1 to A3. Upfront carbon covers A1 to A5. Embodied carbon covers everything from A to C except B6 and B7. Operational carbon is B6 and B7. Cradle to grave, or whole-life carbon, covers A to C. Adding D gives cradle to cradle.', b)


def nested():
    w, h = 900, 520
    b = text(30, 30, 'Embedded, cradle-to-gate and embodied: three boundaries, one product', 20, INK, 'start', '700')
    b += text(30, 52, 'Each box counts everything inside it. The CBAM box is the narrowest and the only one with a price on it.', 13, MUTED, 'start')
    boxes = [(30, 75, 840, 410, '#fff', GREY, 'Embodied carbon (whole life, except running it)',
              'Adds transport to site, installation, maintenance, replacement, demolition and disposal'),
             (60, 150, 580, 305, '#fff', INK, 'Cradle to gate (A1–A3): a product carbon footprint',
              'All emissions to the factory gate, including bought-in electricity and transport of materials'),
             (90, 225, 330, 210, TINT, RED, 'CBAM embedded (EU) or embodied (UK) emissions',
              'Set processes, plus precursors')]
    for x, y, bw, bh, fill, stroke, lab, sub in boxes:
        b += f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>'
        b += text(x + 16, y + 26, lab, 15, stroke if stroke != GREY else INK, 'start', '700')
        b += text(x + 16, y + 46, sub, 12.5, MUTED, 'start')
    items = [(110, 300, 'Direct emissions at the plant'), (110, 324, 'Emissions in key inputs'), (110, 348, '(precursors, e.g. the aluminium'),
             (110, 366, 'in foil, the clinker in cement)'), (110, 394, 'Electricity: EU counts it for cement and'), (110, 412, 'fertiliser only; UK not before 2029')]
    for x, y, t in items:
        b += text(x, y, t, 13, INK, 'start')
    b += text(445, 300, 'Upstream mining and refining', 13, INK, 'start')
    b += text(445, 324, 'not already in a precursor', 13, INK, 'start')
    b += text(445, 352, 'Transport of raw materials', 13, INK, 'start')
    b += text(445, 380, 'Packaging, overheads', 13, INK, 'start')
    b += text(668, 230, 'Transport to customer', 13, INK, 'start')
    b += text(668, 256, 'Installation', 13, INK, 'start')
    b += text(668, 282, 'Maintenance and repair', 13, INK, 'start')
    b += text(668, 308, 'Demolition, waste,', 13, INK, 'start')
    b += text(668, 326, 'disposal', 13, INK, 'start')
    b += text(30, h - 14, 'Robert J. Park · robertjpark.co.uk/learn · Simplified. What CBAM counts is set by law for each good; check the rules for your product.', 12, MUTED, 'start')
    svg('embodied-vs-embedded.svg', w, h, 'Embedded, cradle-to-gate and embodied carbon compared',
        'Three nested boxes. The innermost, CBAM embedded emissions, covers direct emissions from the defined production processes and the emissions in precursors such as the aluminium in foil, with electricity counted only for cement and fertiliser under the EU CBAM and not at all under the UK CBAM before 2029. The middle box, cradle to gate, adds upstream mining and refining, transport of raw materials, bought-in electricity, packaging and overheads. The outer box, embodied carbon, adds transport to the customer, installation, maintenance and repair, demolition, waste and disposal, but excludes the energy and water used to run the building or product.', b)


def loop():
    w, h = 900, 650
    cx, cy, r = 450, 325, 165
    stages = [('Extract', 'Mining, quarrying, felling, farming'), ('Make', 'Refining, smelting, manufacture'),
              ('Move', 'Shipping, haulage, delivery'), ('Use', 'Installation, running, upkeep'),
              ('End of life', 'Demolition, landfill, burning'), ('Recover', 'Reuse, repair, recycling')]
    b = text(30, 30, 'The carbon life cycle as a loop', 20, INK, 'start', '700')
    b += text(30, 52, 'Carbon is released at every stage. The loop closes only if materials come back round.', 13, MUTED, 'start')
    pts = []
    for i in range(6):
        a = -math.pi / 2 + i * 2 * math.pi / 6
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    for i in range(6):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % 6]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
        sx, sy, ex, ey = x1 + ux * 62, y1 + uy * 62, x2 - ux * 66, y2 - uy * 66
        col = GREY if i == 5 else RED
        dash = ' stroke-dasharray="6 5"' if i == 5 else ''
        b += f'<line x1="{sx:.0f}" y1="{sy:.0f}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="{col}" stroke-width="3"{dash}/>'
        ang = math.degrees(math.atan2(uy, ux))
        b += f'<path d="M0 -7 L12 0 L0 7 Z" fill="{col}" transform="translate({ex:.0f} {ey:.0f}) rotate({ang:.0f})"/>'
    for (x, y), (n, d) in zip(pts, stages):
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="58" fill="{TINT if n != "Recover" else "#f4f4f4"}" stroke="{RED if n != "Recover" else GREY}" stroke-width="2.5"/>'
        b += text(x, y + 5, n, 16, INK, weight='700')
        side = 'start' if x > cx + 10 else ('end' if x < cx - 10 else 'middle')
        ox = 70 if side == 'start' else (-70 if side == 'end' else 0)
        oy = 0 if side != 'middle' else (-72 if y < cy else 80)
        b += text(x + ox, y + oy + 5, d, 13, MUTED, side)
        # emission puff
        if n != 'Recover':
            px, py = x + (38 if x >= cx else -38), y - 46
            b += f'<g opacity="0.85"><circle cx="{px:.0f}" cy="{py:.0f}" r="11" fill="{GREY}"/><circle cx="{px+10:.0f}" cy="{py-6:.0f}" r="8" fill="{GREY}"/>'
            b += f'<text x="{px+2:.0f}" y="{py+4:.0f}" font-size="9" fill="#fff" text-anchor="middle" font-weight="700">CO₂</text></g>'
    b += text(cx, cy - 6, 'Each stage', 14, MUTED)
    b += text(cx, cy + 14, 'emits carbon', 14, MUTED)
    b += text(30, h - 14, 'Robert J. Park · robertjpark.co.uk/learn · The dashed arrow is the step most products miss.', 12, MUTED, 'start')
    svg('life-cycle-loop.svg', w, h, 'The carbon life cycle as a loop',
        'Six stages in a circle, each releasing carbon: extract (mining, quarrying, felling, farming); make (refining, smelting, manufacture); move (shipping, haulage, delivery); use (installation, running, upkeep); end of life (demolition, landfill, burning); recover (reuse, repair, recycling), which feeds materials back to make. The arrow from recover back to make is dashed because most products never complete the loop.', b)


modules(); nested(); loop()
print('diagrams written to', OUT)
