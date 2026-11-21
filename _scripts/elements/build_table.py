"""Builds the periodic-table data file and the full-table graphics.

  python3 _scripts/elements/build_table.py <repo_root>

Writes
  data/periodic-table/elements.json          data for tools/periodic-table.html
  assets/learn/periodic-table.svg            full table, no element picked out
  assets/learn/periodic-table-<symbol>.svg   full table with one featured element picked out
Fonts: Source Sans 3 (OFL) embedded so the SVG renders in brand type as an <img>.
"""
import sys, os, json, base64, html
sys.path.insert(0, os.path.dirname(__file__))
from base import ELEMENTS, CATEGORY_LABEL, position, period_group
from contexts import C
from featured import F, CHECKED
from hover import H as HOVER
from briefings_a import B as BA
from briefings_b import B as BB
from briefings_c import B as BC
from briefings_d import B as BD
BRIEF = {**BA, **BB, **BC, **BD}
SHORT_SUPERHEAVY = {
 'Rf':'Superheavy element named after Rutherford; the longest-lived atoms last about an hour.',
 'Db':'Superheavy element named after Dubna; its longest-lived isotope lasts about a day.',
 'Sg':'Superheavy element named after Glenn Seaborg; lasts minutes.',
 'Bh':'Superheavy element named after Niels Bohr; lasts about a minute.',
 'Hs':'Superheavy element named after Hesse; lasts seconds.',
 'Mt':'Superheavy element named after Lise Meitner; lasts seconds.',
 'Ds':'Superheavy element named after Darmstadt; lasts seconds.',
 'Rg':'Superheavy element named after Röntgen; a heavier relative of gold.',
 'Cn':'Superheavy element named after Copernicus; may be volatile like mercury.',
 'Nh':'Superheavy element named after Japan; the first discovered in Asia.',
 'Fl':'Superheavy element named after the Flerov Laboratory; lasts seconds.',
 'Mc':'Superheavy element named after the Moscow region; lasts under a second.',
 'Lv':'Superheavy element named after Livermore; lasts a fraction of a second.',
 'Ts':'Superheavy element named after Tennessee; lasts hundredths of a second.',
 'Og':'Heaviest known element; only a handful of atoms ever made, each lasting under a millisecond.',
}

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
FEATURED = ['P', 'N', 'S', 'F', 'Sb', 'Mg', 'C', 'Rn']

RED, INK, MUTED, RULE = '#a61c1c', '#1a1a1a', '#5a5a5a', '#d6cfcb'
TINT = {  # quiet category tints so the picked-out element stands out in red
 'alkali':'#f3e6d8','alkaline-earth':'#f5efd6','transition':'#e8edf2','post-transition':'#e4ecef',
 'metalloid':'#e7efe2','nonmetal':'#eef3e3','halogen':'#f0e8f3','noble-gas':'#e9e7f4',
 'lanthanide':'#f4e7ec','actinide':'#f1e3e3','unknown':'#eeeeee'}

def data():
    out = []
    for z, sym, name, wt, cat in ELEMENTS:
        r, c = position(z); per, grp = period_group(z)
        s, env, eng, geo, chem, land = C[sym]
        s = HOVER[sym]  # hover line agreed in Robert's review doc, 21 Nov 2026
        e = dict(z=z, symbol=sym, name=name, weight=wt, category=cat, category_label=CATEGORY_LABEL[cat],
                 row=r, col=c, period=per, group=grp, short=s,
                 contexts=dict(environmental=env, engineering=eng, geological=geo, chemical=chem, land=land),
                 briefing_text=BRIEF[sym])
        if sym in F:
            f = F[sym]
            e['featured'] = True
            e['contexts'] = dict(environmental=f['env'], engineering=f['eng'], geological=f['geo'], chemical=f['chem'], land=f['land'])
            e['safety'] = f['safety']; e['compounds'] = f['compounds']
            e['briefing_url'] = f['post']; e['pdf'] = f['pdf']
        out.append(e)
    return out

def font_face():
    b = base64.b64encode(open(os.path.join(ROOT, 'assets/fonts/source-sans-3.woff'), 'rb').read()).decode()
    return f"@font-face{{font-family:'SS3';src:url(data:font/woff;base64,{b}) format('woff');font-weight:400 700}}"

def svg(pick=None, embed_font=True):
    cw, ch, gap = 60, 66, 4
    x0, y0 = 24, 92
    W = x0 * 2 + 18 * cw + 17 * gap
    fy = y0 + 7 * (ch + gap) + 22           # f-block starts below a gap
    H = fy + 2 * (ch + gap) + 84
    els = {e[1]: e for e in ELEMENTS}
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" font-family="SS3, \'Source Sans 3\', Arial, sans-serif">']
    o.append('<style>' + (font_face() if embed_font else '') + '</style>')
    o.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    title = 'The periodic table of the elements'
    o.append(f'<text x="{x0}" y="44" font-size="26" font-weight="700" fill="{INK}">{title}</text>')
    sub = ('Elements of the land · climate, soil, agri-food and the atmosphere' if not pick
           else f'Elements of the land · {html.escape(els[pick][2])} picked out in red; the rest of the series outlined')
    o.append(f'<text x="{x0}" y="70" font-size="15" fill="{MUTED}">{sub}</text>')
    # brand: the actual logo file (assets/brand/logo.svg), embedded
    logo = base64.b64encode(open(os.path.join(ROOT, 'assets/brand/logo.svg'), 'rb').read()).decode()
    o.append(f'<image x="{W - x0 - 264}" y="8" width="264" height="72" href="data:image/svg+xml;base64,{logo}"/>')

    def cell(z, sym, name, wt, cat, x, y):
        picked = sym == pick
        series = sym in FEATURED and not picked and pick is not None
        fill = RED if picked else TINT[cat]
        stroke = RED if (picked or series or (pick is None and sym in FEATURED)) else RULE
        sw = 2.5 if (series or (pick is None and sym in FEATURED)) else 1
        tc = '#ffffff' if picked else INK
        mc = '#ffffff' if picked else MUTED
        g = [f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>',
             f'<text x="{x+5}" y="{y+14}" font-size="11" fill="{mc}">{z}</text>',
             f'<text x="{x+cw/2}" y="{y+40}" font-size="22" font-weight="700" text-anchor="middle" fill="{tc}">{sym}</text>']
        nm = name if len(name) <= 10 else name[:9] + '.'
        g.append(f'<text x="{x+cw/2}" y="{y+57}" font-size="9.5" text-anchor="middle" fill="{mc}">{html.escape(nm)}</text>')
        return ''.join(g)

    for z, sym, name, wt, cat in ELEMENTS:
        r, c = position(z)
        x = x0 + (c - 1) * (cw + gap)
        y = y0 + (r - 1) * (ch + gap) if r <= 7 else fy + (r - 8) * (ch + gap)
        o.append(cell(z, sym, name, wt, cat, x, y))
    # f-block markers in group 3 of periods 6 and 7
    for r, lab in ((6, '57–71'), (7, '89–103')):
        x = x0 + 2 * (cw + gap); y = y0 + (r - 1) * (ch + gap)
        o.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="3" fill="#ffffff" stroke="{RULE}" stroke-dasharray="3 3"/>')
        o.append(f'<text x="{x+cw/2}" y="{y+38}" font-size="12" text-anchor="middle" fill="{MUTED}">{lab}</text>')
    # feature panel in the empty space above the transition metals
    px, py = x0 + 2 * (cw + gap) + 6, y0 + 2
    pw, ph = 10 * (cw + gap) - 12, 2 * (ch + gap) + ch - 8
    if pick:
        z, sym, name, wt, cat = els[pick]
        o.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="#faf3f3" stroke="{RED}"/>')
        o.append(f'<rect x="{px+14}" y="{py+14}" width="118" height="{ph-28}" rx="4" fill="{RED}"/>')
        o.append(f'<text x="{px+24}" y="{py+40}" font-size="16" fill="#fff">{z}</text>')
        o.append(f'<text x="{px+73}" y="{py+118}" font-size="64" font-weight="700" text-anchor="middle" fill="#fff">{sym}</text>')
        o.append(f'<text x="{px+73}" y="{py+150}" font-size="13" text-anchor="middle" fill="#fff">{wt}</text>')
        o.append(f'<text x="{px+150}" y="{py+48}" font-size="30" font-weight="700" fill="{INK}">{name}</text>')
        per, grp = period_group(z)
        where = f'Group {grp}, period {per}' if grp else f'Period {per}'
        o.append(f'<text x="{px+150}" y="{py+74}" font-size="15" fill="{MUTED}">{where} · {CATEGORY_LABEL[cat]}</text>')
        # wrap short line
        words = C[sym][0].split(); lines, cur = [], ''
        for w in words:
            if len(cur) + len(w) + 1 > 52: lines.append(cur); cur = w
            else: cur = (cur + ' ' + w).strip()
        lines.append(cur)
        for i, l in enumerate(lines[:3]):
            o.append(f'<text x="{px+150}" y="{py+108+i*22}" font-size="17" fill="{INK}">{html.escape(l)}</text>')
    else:
        o.append(f'<text x="{px+10}" y="{py+40}" font-size="17" fill="{INK}">Outlined in red: the eight elements in the series —</text>')
        o.append(f'<text x="{px+10}" y="{py+64}" font-size="17" fill="{INK}">phosphorus, nitrogen, sulfur, fluorine, antimony,</text>')
        o.append(f'<text x="{px+10}" y="{py+88}" font-size="17" fill="{INK}">magnesium, carbon and radon.</text>')
    # legend
    ly = H - 52; lx = x0
    for cat in ['alkali','alkaline-earth','transition','post-transition','metalloid','nonmetal','halogen','noble-gas','lanthanide','actinide']:
        lab = CATEGORY_LABEL[cat]
        o.append(f'<rect x="{lx}" y="{ly-11}" width="13" height="13" fill="{TINT[cat]}" stroke="{RULE}"/>')
        o.append(f'<text x="{lx+18}" y="{ly}" font-size="12" fill="{MUTED}">{lab}</text>')
        lx += 30 + len(lab) * 6.1
    o.append(f'<text x="{x0}" y="{ly+26}" font-size="12.5" fill="{MUTED}">Interactive version with every element: robertjpark.co.uk/tools/periodic-table.html · Standard atomic weights from IUPAC; [ ] = mass number of the longest-lived isotope.</text>')
    o.append('</svg>')
    return '\n'.join(o)

if __name__ == '__main__':
    d = data()
    os.makedirs(os.path.join(ROOT, 'data/periodic-table'), exist_ok=True)
    json.dump(dict(checked=CHECKED, elements=d), open(os.path.join(ROOT, 'data/periodic-table/elements.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    out = os.path.join(ROOT, 'assets/learn')
    open(os.path.join(out, 'periodic-table.svg'), 'w').write(svg())
    for s in FEATURED:
        open(os.path.join(out, f'periodic-table-{s.lower()}.svg'), 'w').write(svg(s))
    print('elements:', len(d), 'featured:', sum(1 for e in d if e.get('featured')))
