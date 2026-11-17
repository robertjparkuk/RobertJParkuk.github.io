"""House brand for the standalone pages listed on /tools/ (tools/, puzzles/, guides/).

    python3 _scripts/tools_brand.py <repo_root>      # check and fix every page in place

Puts in the real split-circle mark (not the old half-filled circle or the jigsaw), brand red #A61C1C
and ink #1A1A1A (reverse red #E0484A and white in dark mode), the brand mark as favicon, and Source
Sans 3 for headings, as on the main site. Safe to run more than once. Generators that write a tool
page (eu_rules_tool.py) call apply() on their output so a rebuild keeps the brand.
"""
import re, sys, pathlib

ARC_R = 'M53.67 10C26.05 10 3.67 32.39 3.67 60s22.38 50 50 50v-8.67C30.84 101.33 12.33 82.83 12.33 60S30.84 18.67 53.67 18.67Z'
ARC_K = 'M60 97c20.43 0 37-16.57 37-37S80.43 23 60 23v8.67c15.65 0 28.33 12.68 28.33 28.33S75.65 88.33 60 88.33Z'
LINE = 'M56 115h2V5.33h-2Z'

def mark(h):
    w = round(h * 100 / 120)
    return (f'<svg class="rjp-mark" width="{w}" height="{h}" viewBox="0 0 100 120" aria-hidden="true" focusable="false">'
            f'<path class="r" d="{ARC_R}"/><path class="k" d="{ARC_K}"/><path class="r" d="{LINE}"/></svg>')

BRAND_STYLE = """<style id="rjp-brand">
/* Brand: split-circle mark, red #A61C1C and ink #1A1A1A (reverse: #E0484A and white), Source Sans 3 headings */
.rjp-mark{flex:none;display:block}
.rjp-mark .r{fill:#A61C1C}.rjp-mark .k{fill:#1A1A1A}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .rjp-mark .r{fill:#E0484A}:root:not([data-theme="light"]) .rjp-mark .k{fill:#FFFFFF}}
:root[data-theme="dark"] .rjp-mark .r{fill:#E0484A}:root[data-theme="dark"] .rjp-mark .k{fill:#FFFFFF}
h1{font-weight:700!important;letter-spacing:-0.005em}h2{letter-spacing:-0.005em}
</style>
"""

SANS = "'Source Sans 3','Segoe UI',system-ui,sans-serif"
FONT_SUBS = [
    (r"""--display:\s*['"]Fraunces['"][^;]*""", f"--display:{SANS}"),
    (r"""--serif:\s*['"]Fraunces['"][^;]*""", f"--serif:{SANS}"),
    (r"""--font-anthropic-serif:\s*['"]Fraunces['"][^;]*""", f"--font-anthropic-serif:{SANS}"),
]
COLOUR_SUBS = [(r'#B3121B', '#A61C1C'), (r'#1B1817', '#1A1A1A'), (r'#E5484D', '#E0484A')]

OLD_CIRCLE = re.compile(r'<svg width="26" height="26" viewBox="0 0 44 44" aria-hidden="true"><path d="M22 2a20 20 0 0 0 0 40z" fill="currentColor"/><path d="M22 2a20 20 0 0 1 0 40z" fill="#B3121B"/></svg>')
OLD_ESG = re.compile(r'<svg class="mark" viewBox="0 0 54 54" aria-hidden="true">.*?</svg>', re.S)
OLD_IMG = re.compile(r'<img src="/assets/tools-mark\.svg" alt="" width="30" height="30">')
ICON = '<link rel="icon" type="image/svg+xml" href="/assets/brand/mark.svg">'


def apply(t, farm=False):
    """Return (html, notes) with the house brand applied."""
    notes = []
    if not farm:
        t, n1 = OLD_CIRCLE.subn(mark(26), t)
        t, n2 = OLD_IMG.subn(mark(30), t)
        t, n3 = OLD_ESG.subn(mark(54), t)
        if n1 + n2 + n3: notes.append(f'mark x{n1+n2+n3}')
        if re.search(r'href="/assets/tools-mark\.svg"', t) and 'rel="icon"' in t:
            t = re.sub(r'<link rel="icon" type="image/svg\+xml" href="/assets/tools-mark\.svg">', ICON, t); notes.append('favicon')
        elif 'rel="icon"' not in t:
            t = t.replace('<title>', ICON + '\n<title>', 1); notes.append('favicon added')
        for a, b in COLOUR_SUBS:
            t, n = re.subn(a, b, t, flags=re.I)
            if n: notes.append(f'{a}->{b} x{n}')
        if 'id="rjp-brand"' not in t:
            t = t.replace('</head>', BRAND_STYLE + '</head>', 1); notes.append('brand style')
    for a, b in FONT_SUBS:
        t, n = re.subn(a, b, t)
        if n: notes.append('headings -> Source Sans 3')
    return t, notes


def pages(root):
    root = pathlib.Path(root)
    return sorted(list(root.glob('tools/*.html')) + [root / 'tools/farm-data-checker/index.html']
                  + list(root.glob('puzzles/*.html')) + list(root.glob('guides/*.html')))


if __name__ == '__main__':
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    bad = []
    for f in pages(root):
        o = f.read_text(encoding='utf-8')
        t, notes = apply(o, farm='farm-data-checker' in str(f))
        if t != o: f.write_text(t, encoding='utf-8')
        left = [k for k in ('tools-mark', 'Fraunces', '#B3121B') if k.lower() in t.lower()]
        if left: bad.append(f'{f.relative_to(root)}: {left}')
        print(f'{f.relative_to(root)}: {", ".join(notes) or "already on brand"}')
    if bad: sys.exit('Off-brand items left:\n' + '\n'.join(bad))
