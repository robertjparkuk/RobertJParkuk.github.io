"""Turns the eight briefing templates in _scripts/elements/posts/ into blog posts,
adding the periodic-table figure, the safety panel and the compounds table from
featured.py so the post, the PDF and the website tool all say the same thing.

  python3 _scripts/elements/build_posts.py <repo_root>
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
from featured import F, CHECKED
from base import ELEMENTS

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
ORDER = [('P', '2026-11-24'), ('N', '2026-11-25'), ('S', '2026-11-26'), ('F', '2026-11-27'),
         ('Sb', '2026-11-28'), ('Mg', '2026-11-29'), ('C', '2026-11-30'), ('Rn', '2026-12-01')]
NAMES = {e[1]: e[2] for e in ELEMENTS}

def figure(sym):
    n = NAMES[sym]
    return (f"<figure class=\"learn-figure\"><img src=\"{{{{ '/assets/learn/periodic-table-{sym.lower()}.svg' | relative_url }}}}\" "
            f"alt=\"The full periodic table of 118 elements, coloured by type. {n} is picked out in red with its atomic number, symbol, "
            f"atomic weight and a one-line description. The other seven elements in this series (phosphorus, nitrogen, sulfur, fluorine, "
            f"antimony, magnesium, carbon and radon) are outlined in red.\" loading=\"lazy\"><figcaption>{n} in the full periodic table. "
            f"<a href=\"{{{{ '/tools/periodic-table.html' | relative_url }}}}\">Open the interactive table</a> to explore every element.</figcaption></figure>")

def safety(sym):
    s = F[sym]['safety']
    o = [s['coshh'], '', '| Form | Classification (CLP) |', '|---|---|']
    o += [f'| {a} | {b} |' for a, b in s['classes']]
    o += ['', '| Substance | Workplace exposure limit (EH40/2005) |', '|---|---|']
    o += [f'| {a} | {b} |' for a, b in s['wels']]
    o += ['', '| UN number | Proper shipping name | Class |', '|---|---|---|']
    o += [f'| {a} | {b} | {c} |' for a, b, c in s['un']]
    o += ['', f"**Risks of the element itself.** {s['risks']}", '',
          '*Classification and limits change. Always work from the supplier\'s current safety data sheet and your own COSHH assessment.*']
    return '\n'.join(o)

def compounds(sym):
    c = F[sym]['compounds']
    o = ['| Where you meet it | Compound | Why it matters |', '|---|---|---|']
    for key, label in (('nature', 'Nature'), ('manufacturing', 'Manufacturing'), ('climate', 'Climate')):
        for i, (a, b) in enumerate(c[key]):
            o.append(f"| {label if i == 0 else ''} | {a} | {b} |")
    return '\n'.join(o)

def footer(sym):
    n = NAMES[sym]
    pdf = F[sym]['pdf']
    return (f"*Robert J. Park is an environment, carbon and public affairs consultant based in Larne, Northern Ireland. "
            f"Download the briefing, [*{n}* (PDF)]({{{{ '{pdf}' | relative_url }}}}), with the full periodic table, the safety panel and the sources. "
            f"This is one of eight learning briefings on the elements that shape climate, soil, land, agri-food and the atmosphere; "
            f"the others are linked from the [interactive periodic table]({{{{ '/tools/periodic-table.html' | relative_url }}}}). "
            f"This is general information as at {CHECKED}, not legal, safety or agronomic advice. "
            f"AI was used to lay out this document and to generate leads from the consultant's research, knowledge and questioning; figures were checked against the official sources listed.*")

if __name__ == '__main__':
    for sym, date in ORDER:
        t = open(os.path.join(os.path.dirname(__file__), 'posts', f'{sym.lower()}.md.tmpl'), encoding='utf-8').read()
        slug = F[sym]['post'].rstrip('/').split('/')[-1]
        t = t.replace('{{DATE}}', f'{date} 07:30:00 +0000')
        t = t.replace('{{FIGURE}}', figure(sym)).replace('{{SAFETY}}', safety(sym))
        t = t.replace('{{COMPOUNDS}}', compounds(sym)).replace('{{FOOTER}}', footer(sym))
        out = os.path.join(ROOT, '_posts', f'{date}-{slug}.md')
        open(out, 'w', encoding='utf-8').write(t)
        print(out, len(re.sub(r'<[^>]+>|\|', ' ', t).split()), 'words')
