"""Timeline image for 'Twelve dates to Easter'. Needs a local server on the repo root (port 8765).
Usage: python3 make_timeline.py <repo_root>"""
import sys, os
from playwright.sync_api import sync_playwright
ROOT = sys.argv[1]
D = [('20 Nov', 'UK–EU summit', 'uk'), ('9 Dec', 'EU product liability, NI', 'ni'), ('30 Dec', 'EU deforestation, NI', 'ni'),
     ('31 Dec', 'ESOS phase 4 cut-off', 'uk'), ('1 Jan', 'UK CBAM starts', 'key'), ('1 Jan', 'EU F-gas bans, NI', 'ni'),
     ('Jan', 'First UK CBAM rates', 'uk'), ('20 Jan', 'EU machinery rules, NI', 'ni'), ('Feb', 'EU CBAM certificates on sale', 'eu'),
     ('18 Feb', 'Battery passports, NI', 'ni'), ('31 Mar', 'Quarter-end CBAM certificates', 'eu'), ('1 Apr', 'GB levy relief (NI undated)', 'uk')]
COL = {'ni': '#A61C1C', 'uk': '#1A1A1A', 'eu': '#6b6b6b', 'key': '#A61C1C'}
items = ''.join(f'''<div class="it {k}"><div class="dot" style="background:{COL[k]}"></div><div class="d">{d}</div><div class="t">{t}</div></div>''' for d, t, k in D)
html = f"""<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/assets/fonts/fonts.css"><style>
*{{box-sizing:border-box}}html,body{{height:100%;margin:0}}body{{font-family:'Source Sans 3',sans-serif;background:#f5f2ef;color:#1A1A1A}}
.c{{position:relative;height:100%;padding:48px 60px}}
.ey{{font-family:'IBM Plex Mono',monospace;font-size:18px;letter-spacing:.14em;text-transform:uppercase;color:#A61C1C}}
h1{{font-family:'Source Serif 4',serif;font-weight:600;font-size:52px;margin:10px 0 0;line-height:1.05}}
.line{{position:absolute;left:60px;right:60px;top:300px;height:4px;background:#1A1A1A}}
.row{{position:absolute;left:60px;right:60px;top:240px;display:grid;grid-template-columns:repeat(12,1fr)}}
.it{{position:relative;height:200px}}
.dot{{position:absolute;left:50%;top:52px;width:20px;height:20px;border-radius:50%;transform:translateX(-50%);border:3px solid #f5f2ef}}
.it.key .dot{{width:34px;height:34px;top:45px}}
.d{{position:absolute;top:0;left:0;right:0;text-align:center;font-family:'IBM Plex Mono',monospace;font-size:17px}}
.t{{position:absolute;top:92px;left:-4px;right:-4px;text-align:center;font-size:17px;line-height:1.2}}
.it:nth-child(even) .t{{top:158px}}
.it:nth-child(even)::after{{content:'';position:absolute;left:50%;top:76px;height:78px;border-left:1px dashed #9a9a9a}}
.t{{left:-30px !important;right:-30px !important}}
.it.key .t{{font-weight:700;color:#A61C1C}}
.lg{{position:absolute;left:60px;bottom:44px;font-size:18px;display:flex;gap:22px;align-items:center}}
.lg i{{display:inline-block;width:14px;height:14px;border-radius:50%;margin-right:6px;vertical-align:-1px}}
.ft{{position:absolute;right:60px;bottom:36px;display:flex;gap:18px;align-items:center;font-family:'IBM Plex Mono',monospace;font-size:16px;color:#5a5a5a}}
.ft img{{height:56px}}
</style></head><body><div class="c"><div class="ey">November 2026 to April 2027</div><h1>Twelve dates to Easter for NI firms</h1>
<div class="line"></div><div class="row">{items}</div>
<div class="lg"><span><i style="background:#A61C1C"></i>EU rules applying in NI</span><span><i style="background:#1A1A1A"></i>UK-wide</span><span><i style="background:#6b6b6b"></i>EU customers</span></div>
<div class="ft"><span>robertjpark.co.uk</span><img src="/assets/brand/logo.svg" alt=""></div></div></body></html>"""
tmp = os.path.join(ROOT, '_tl_tmp.html'); open(tmp, 'w', encoding='utf-8').write(html)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1200, 'height': 630})
    pg.goto('http://localhost:8765/_tl_tmp.html'); pg.wait_for_timeout(400)
    pg.screenshot(path=os.path.join(ROOT, 'assets/briefings/twelve-dates/twelve-dates-to-easter.png')); b.close()
os.remove(tmp); print('ok')
