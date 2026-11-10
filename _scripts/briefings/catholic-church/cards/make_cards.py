"""Render share images for the Catholic Church briefing. Run with a local server on the repo root:
python3 -m http.server 8765 & python3 make_cards.py <repo_root>"""
import sys, os
from playwright.sync_api import sync_playwright
ROOT = sys.argv[1]
HEAD = """<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/assets/fonts/fonts.css"><style>
*{box-sizing:border-box}html,body{height:100%}body{margin:0;font-family:'Source Sans 3',sans-serif;color:#1A1A1A;background:#f5f2ef}
.c{position:relative;padding:56px 64px;height:100%}
.ey{font-family:'IBM Plex Mono',monospace;font-size:20px;letter-spacing:.14em;text-transform:uppercase;color:#A61C1C}
h1{font-family:'Source Serif 4',serif;font-weight:600;line-height:1.08;margin:14px 0 0}
.g{display:grid;gap:22px 36px;margin-top:34px}
.g div{border-top:4px solid #A61C1C;padding-top:12px}
.g b{display:block;font-family:'Source Serif 4',serif;font-weight:600;line-height:1}
.g span{display:block;color:#4a4a4a;margin-top:8px;line-height:1.25}
.ft{position:absolute;left:64px;right:64px;bottom:44px;display:flex;justify-content:space-between;align-items:center;font-family:'IBM Plex Mono',monospace;font-size:18px;color:#5a5a5a}
.ft img{height:60px}
.bar{height:46px;background:#e3dedb;border-radius:4px;overflow:hidden;margin:10px 0 4px}.bar i{display:block;height:100%;background:#A61C1C}
.row{font-size:26px;margin-top:18px}.row em{font-style:normal;float:right;font-family:'IBM Plex Mono',monospace}
</style></head><body>"""
FOOT = """<div class="ft"><img src="/assets/brand/logo.svg" alt=""><span>robertjpark.co.uk · sources in the briefing</span></div>"""
CARDS = {
 'share-church-in-numbers.png': (1200, 630, """<div class="c"><div class="ey">Briefing · November 2026</div>
<h1 style="font-size:58px">The Catholic Church in numbers</h1>
<div class="g" style="grid-template-columns:repeat(4,1fr)">
<div><b style="font-size:58px">1.42bn</b><span style="font-size:21px">Catholics, 17.8% of the world</span></div>
<div><b style="font-size:58px">64m</b><span style="font-size:21px">pupils in Catholic schools</span></div>
<div><b style="font-size:58px">5,397</b><span style="font-size:21px">hospitals, among 101,110 health and charity centres</span></div>
<div><b style="font-size:58px">0.44 km²</b><span style="font-size:21px">Vatican City, which reports its emissions to the UN</span></div>
</div>""" + FOOT + "</div>"),
 'vatican-carbon-footprint.png': (1080, 1080, """<div class="c" style="padding:64px"><div class="ey">The world's smallest state, measured</div>
<h1 style="font-size:64px">The Vatican's carbon footprint</h1>
<div class="g" style="grid-template-columns:1fr 1fr">
<div><b style="font-size:84px">15,890 t</b><span style="font-size:24px">CO₂e in 2022, 18% below 2011</span></div>
<div><b style="font-size:84px">−28%</b><span style="font-size:24px">target for 2035; net zero by 2050</span></div></div>
<div style="margin-top:40px;font-family:'IBM Plex Mono',monospace;font-size:20px;letter-spacing:.12em;text-transform:uppercase;color:#5a5a5a">Where it comes from</div>
<div class="row">Vehicles<em>71%</em><div class="bar"><i style="width:71%"></i></div></div>
<div class="row">Heating<em>22%</em><div class="bar"><i style="width:22%;background:#1A1A1A"></i></div></div>
<div class="row">Refrigerant gases<em>7%</em><div class="bar"><i style="width:7%;background:#1A1A1A"></i></div></div>
<p style="font-size:24px;line-height:1.35;margin-top:30px;color:#2b2b2b">Its electricity is imported and reported as renewable. Next: an agrivoltaic plant, solar panels over working farmland near Rome, to supply all of it.</p>
""" + FOOT + "</div>"),
}
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, (w, h, html) in CARDS.items():
        tmp = os.path.join(ROOT, '_card_tmp.html'); open(tmp, 'w', encoding='utf-8').write(HEAD + html + '</body></html>')
        pg = b.new_page(viewport={'width': w, 'height': h}); pg.goto('http://localhost:8765/_card_tmp.html'); pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(ROOT, 'assets/briefings/catholic-church', name)); os.remove(tmp); print(name)
    b.close()
