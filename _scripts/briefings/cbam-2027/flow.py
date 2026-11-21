"""Flow chart for 'The 2027 CBAM horizon' (21 Nov 2026). Usage: python3 flow.py <repo_root>"""
import sys, os, html
ROOT = os.path.abspath(sys.argv[1]); OUT = os.path.join(ROOT, 'assets/briefings/cbam-2027'); os.makedirs(OUT, exist_ok=True)
FONT = "font-family=\"'Source Sans 3','Segoe UI',Arial,sans-serif\""
RED, INK, GREY, AMBER, GREEN = '#a61c1c', '#1a1a1a', '#5a5a5a', '#d9822b', '#3b7a57'
esc = html.escape
W = 900

def wrap(t, n):
    out, line = [], ''
    for w in t.split():
        if len(line) + len(w) + 1 > n: out.append(line); line = w
        else: line = (line + ' ' + w).strip()
    return out + [line]

def box(o, x, y, w, h, text, kind):
    fill, stroke, col = {'q': ('#fff', INK, INK), 'start': (INK, INK, '#fff'),
                         'out': ('#eef5f0', GREEN, INK), 'pay': ('#fbeaea', RED, INK), 'warn': ('#fdf1e4', AMBER, INK)}[kind]
    rx = 22 if kind == 'q' else 6
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    lines = wrap(text, int(w / 7.6)); ty = y + h / 2 - (len(lines) - 1) * 9 + 5
    for i, l in enumerate(lines):
        o.append(f'<text x="{x + w/2}" y="{ty + i*18}" font-size="14.5" text-anchor="middle" fill="{col}" font-weight="{700 if kind in ("start","q") else 400}">{esc(l)}</text>')

def arrow(o, x1, y1, x2, y2, label=None, lx=None, ly=None):
    o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GREY}" stroke-width="2" marker-end="url(#arr)"/>')
    if label: o.append(f'<text x="{lx if lx is not None else (x1+x2)/2 + 6}" y="{ly if ly is not None else (y1+y2)/2 + 4}" font-size="13" font-weight="700" fill="{RED}">{label}</text>')

def build(nodes, edges, H, title, sub, fn, note):
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}" {FONT}>',
         '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#5a5a5a"/></marker></defs>',
         f'<rect width="{W}" height="{H}" fill="#fff"/>',
         f'<text x="24" y="34" font-size="21" font-weight="700" fill="{INK}">{esc(title)}</text>',
         f'<text x="24" y="58" font-size="14" fill="{GREY}">{esc(sub)}</text>']
    import re
    logo = open(os.path.join(ROOT, 'assets/brand/logo-compact.svg')).read()
    inner = re.sub(r'(?s)^.*?<svg[^>]*>', '', logo).rsplit('</svg>', 1)[0]
    o.append(f'<svg x="{W-196}" y="10" width="160" height="48" viewBox="0 0 400 120">{inner}</svg>')
    o.append(f'<rect x="24" y="70" width="{W-48}" height="2" fill="{RED}"/>')
    for e in edges: arrow(o, *e)
    for n in nodes: box(o, *n)
    for i, l in enumerate(wrap(note, 118)):
        o.append(f'<text x="24" y="{H - 34 + i*16}" font-size="12" fill="{GREY}">{esc(l)}</text>')
    o.append('</svg>'); open(os.path.join(OUT, fn), 'w').write('\n'.join(o))

if __name__ == '__main__':
    import json
    spec = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow.json')))
    for c in spec: build([tuple(n) for n in c['nodes']], [tuple(e) for e in c['edges']], c['H'], c['title'], c['sub'], c['fn'], c['note'])
    print('ok')
