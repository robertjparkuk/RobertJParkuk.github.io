"""Builds one deep-dive page per element at /learn/elements/<name>/ and the index
at /learn/elements/. Elements without deep-dive text yet get no page; the index
lists them as coming.

  python3 _scripts/elements/build_deep.py <repo_root>

Readers' notes: approved contributions go in _data/element_notes.yml, keyed by
symbol, and appear on the page under "From readers".
"""
import sys, os, re, html, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from base import ELEMENTS, CATEGORY_LABEL, period_group
from hover import H
from briefings_a import B as BA
from briefings_b import B as BB
from briefings_c import B as BC
from briefings_d import B as BD
from featured import F
from deep_a import D as DA
from deep_b import D as DB
from deep_c import D as DC
from deep_supp import S as SUPP

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
BRIEF = {**BA, **BB, **BC, **BD}
DEEP = {**DA, **DB, **DC}
for _k, _v in SUPP.items():
    DEEP[_k] = {**DEEP[_k], **_v}
CHECKED = '21 November 2026'
OUT = os.path.join(ROOT, 'learn', 'elements')

def slug(name): return name.lower()

def esc(t): return t.replace('|', '\\|')

def page(z, sym, name, wt, cat):
    d = DEEP[sym]; b = BRIEF[sym]
    per, grp = period_group(z)
    where = f'group {grp}, period {per}' if grp else f'period {per} (f-block)'
    subject = f'{name}: what I know'
    body = (f"Element: {name} ({sym})\n\nWhat I know or have seen (where, when, how you know it):\n\n\n"
            "Source or evidence, if any:\n\nName to credit (or 'anonymous'):\n")
    mail = 'mailto:robert@robertjpark.co.uk?subject=' + urllib.parse.quote(subject) + '&body=' + urllib.parse.quote(body)
    comp = '\n'.join(f'| {esc(a)} | {esc(c)} |' for a, c in d['compounds'])
    feat = ''
    if sym in F:
        feat = (f"\n**Full briefing:** {name} is one of the eight *Elements of the land* briefings, with COSHH, exposure limits, UN numbers "
                f"and the rules in Northern Ireland. [Download the PDF]({{{{ '{F[sym]['pdf']}' | relative_url }}}}).\n")
    ni = f"\n## In Northern Ireland\n\n{d['ni']}\n" if d.get('ni') else ''
    extra = ''.join(f"\n## {h}\n\n{d[k]}\n" for k, h in (('engineering', 'Engineering'), ('politics', 'Politics and trade'), ('commerce', 'Commerce')) if d.get(k))
    quirk = f"\n## Quirks\n\n{d['quirks']}\n" if d.get('quirks') else ''
    return f"""---
layout: page
title: "{name} ({sym})"
permalink: /learn/elements/{slug(name)}/
lead: "{H[sym].replace('"', "'")}"
description: "{name} and the climate, carbon, land, soil, water and health: a plain-English deep dive for Northern Ireland, with remarkable compounds."
element: {sym}
---

| Atomic number | Symbol | Atomic weight | Type | Place in the table |
|---|---|---|---|---|
| {z} | {sym} | {wt} | {CATEGORY_LABEL[cat]} | {where.capitalize()} |

[See {name} in the interactive periodic table]({{{{ '/tools/periodic-table.html#{sym.lower()}' | relative_url }}}}) · [All element deep dives]({{{{ '/learn/elements/' | relative_url }}}})
{feat}
## Climate and carbon

{d['climate']}

## Land, soil and water

{d['land']}

## Health and safety

{d['health']} {b['hazards']}

## Industry and supply

{d['industry']}
{extra}{ni}{quirk}
## Remarkable compounds

| Compound | Why it is remarkable |
|---|---|
{comp}

## Discovery

{b['discovery']}

{{% assign notes = site.data.element_notes['{sym}'] %}}
{{% if notes %}}
## From readers

{{% for n in notes %}}
<blockquote class="reader-note"><p>{{{{ n.text }}}}</p><footer>— {{{{ n.by }}}}{{% if n.date %}}, {{{{ n.date }}}}{{% endif %}}</footer></blockquote>
{{% endfor %}}
{{% endif %}}

<aside class="post-cta" markdown="1">
**Add what you know about {name}.** Farmers, engineers, teachers, chemists and anyone who has worked with it: tell me what you have seen, measured or learned. I check every contribution against a source before adding it here, and credit you by name if you want. [Email your note about {name}]({mail}). See the [privacy notice]({{{{ '/privacy/' | relative_url }}}}) for how I handle what you send.
</aside>

*General information as at {CHECKED}, not legal, safety or agronomic advice. Hazard notes are headline classifications only: always work from the supplier's safety data sheet. Created with assistive technology including AI and re-checked against the official sources listed.*
"""

def index():
    rows = []
    for z, sym, name, wt, cat in ELEMENTS:
        link = f"[{name}]({{{{ '/learn/elements/{slug(name)}/' | relative_url }}}})" if sym in DEEP else f"{name} *(coming soon)*"
        rows.append(f"| {z} | {sym} | {link} | {esc(H[sym])} |")
    n = len(DEEP)
    return f"""---
layout: page
title: "The elements: a deep dive on each"
permalink: /learn/elements/
lead: "A plain-English page on each element: what it means for climate and carbon, land, soil and water, health and safety, engineering, politics and trade, and commerce, with its quirks and most remarkable compounds."
description: "Deep dives on the chemical elements for Northern Ireland: climate, carbon, land, soil, water, health and remarkable compounds, with a way to add what you know."
---

{n} of 118 pages are up so far, starting with the elements most tied to climate, land, soil and health. The rest follow in batches. For a quick look at every element, use the [interactive periodic table]({{{{ '/tools/periodic-table.html' | relative_url }}}}).

**Know something about an element?** Every page has a box to send in what you have seen, measured or learned. Contributions are checked against a source before they go up, and credited by name if you want.

| No. | Symbol | Element | In one line |
|---|---|---|---|
""" + '\n'.join(rows) + f"""

*Checked {CHECKED}. Created with assistive technology including AI and re-checked against the official sources listed.*
"""

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for z, sym, name, wt, cat in ELEMENTS:
        if sym in DEEP:
            open(os.path.join(OUT, f'{slug(name)}.md'), 'w', encoding='utf-8').write(page(z, sym, name, wt, cat))
    open(os.path.join(OUT, 'index.md'), 'w', encoding='utf-8').write(index())
    import json
    json.dump({sym: f'/learn/elements/{slug(name)}/' for z, sym, name, wt, cat in ELEMENTS if sym in DEEP},
              open(os.path.join(ROOT, 'data/periodic-table/deep.json'), 'w'), indent=0)
    print('pages:', len(DEEP))
