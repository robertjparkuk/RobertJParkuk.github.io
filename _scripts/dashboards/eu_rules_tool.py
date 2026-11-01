"""'Which EU rules apply to me?' tool. Usage: python3 eu_rules_tool.py <repo_root>

Reads the data lists in eu_build.py (APPLIES, NOT_NI, GB, NEXT, AS_AT), so it stays in step with the
EU law dashboard. Run it straight after eu_build.py whenever the dashboard is updated. Writes
tools/which-eu-rules-apply.html. The page is static: nothing the visitor ticks is sent anywhere.
"""
import sys, os, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
_eu = open(os.path.join(HERE, 'eu_build.py'), encoding='utf-8').read()
exec(_eu[:_eu.index('\ndef page_eu')])  # helpers, CSS and data lists only

TAGS = [
 ('food', 'Food, drink or farm produce'),
 ('forest', 'Timber, paper or furniture, or goods made with cattle, cocoa, coffee, palm oil, rubber or soya'),
 ('packaging', 'Anything sold in packaging'),
 ('machinery', 'Machinery or equipment, including farm and construction machinery'),
 ('batteries', 'Batteries, electronics, e-bikes or vehicles'),
 ('chemicals', 'Chemicals, cleaning products, paints or agri-supplies'),
 ('construction', 'Construction products'),
 ('consumer', 'Consumer products sold to the public, including online'),
 ('toys', 'Toys'),
 ('cooling', 'Refrigeration, air conditioning or heat pumps (selling, installing or running them)'),
 ('waste', 'Waste, scrap or recycling'),
 ('energy', 'Generating electricity, or using a lot of it'),
]
PRODUCTS = ['food', 'forest', 'packaging', 'machinery', 'batteries', 'chemicals', 'construction', 'consumer', 'toys', 'cooling']

# Which tags each row concerns: matched on the start of the law's name in eu_build.py.
# 'ALL' means every business moving goods. A row with no match here is not shown, and the build stops.
APPLIES_TAGS = {
 'Deforestation': ['food', 'forest'],
 'Machinery': ['machinery'],
 'Batteries': ['batteries'],
 'Packaging': ['packaging', 'food'],
 'CLP': ['chemicals'],
 'Construction Products': ['construction'],
 'Waste Shipments': ['waste'],
 'F-gas': ['cooling'],
 'Ecodesign': ['consumer', 'batteries', 'machinery'],
 'General Product Safety': ['consumer', 'toys'],
 'Product Liability': PRODUCTS,
 'Toy Safety': ['toys'],
 'Detergents': ['chemicals'],
 'Vehicle circularity': ['batteries', 'waste'],
 'Farmers in the food': ['food'],
 'Union Customs Code': ['ALL'],
 'REACH': ['chemicals'],
 'EU Emissions Trading': ['energy'],
 'Single Electricity Market': ['energy'],
}
GB_TAGS = {
 'Product safety': ['consumer', 'toys'],
 'Deforestation': ['food', 'forest'],
 'Packaging': ['packaging', 'food'],
 'UK Internal Market Scheme': ['ALL'],
 '"Not for EU" labels': ['food'],
 'Plant health': ['food'],
 'Chemical labelling': ['chemicals'],
 'Batteries': ['batteries'],
 'Agri-food (SPS)': ['food'],
 'Emissions trading link': ['energy'],
 'REACH': ['chemicals'],
 'F-gas': ['cooling'],
 'Machinery': ['machinery', 'consumer'],
 'Electricity VAT': ['energy'],
 'Parcel and low-value': ['consumer'],
}
NOT_NI_EU = ('Corporate Sustainability Reporting', 'Corporate Sustainability Due Diligence', 'EU Carbon Border')

def name_link(c):
    return (c[0], c[1]) if isinstance(c, tuple) else (c, '')

def tags_for(name, table):
    for k, v in table.items():
        if name.startswith(k) or k in name:
            return v
    raise SystemExit(f'eu_rules_tool.py: no tags for "{name}". Add it to the tag tables before publishing.')

rows = []
for r in APPLIES:
    n, u = name_link(r[0])
    rows.append({'g': 'ni', 'n': n, 'u': u, 'tags': tags_for(n, APPLIES_TAGS), 'topic': r[1], 'who': r[2], 'applies': plain(r[3]), 'dates': r[4]})
for r in GB:
    n, u = name_link(r[0])
    rows.append({'g': 'gb', 'kind': r[1], 'n': n, 'u': u, 'tags': tags_for(n, GB_TAGS), 'what': r[2], 'dates': r[3]})
for r in NOT_NI:
    n, u = name_link(r[0])
    if n.startswith(NOT_NI_EU):
        rows.append({'g': 'eu', 'n': n, 'u': u, 'tags': ['ALL'], 'why': r[2]})

DATA = json.dumps({'rows': rows, 'tags': TAGS}, ensure_ascii=False).replace('</', '<\\/')

TOOL_CSS = """
.w-q{border:1px solid var(--color-rule,#e4e0dc);border-radius:10px;padding:16px 18px;margin:0 0 14px;background:#fff}
.w-q legend{font-weight:700;font-size:1.05rem;padding:0 6px}
.w-q .w-hint{margin:2px 0 10px;color:#555;font-size:.95rem}
.w-opts{display:grid;gap:6px 18px;grid-template-columns:1fr}
@media(min-width:760px){.w-opts{grid-template-columns:1fr 1fr}}
.w-opts label{display:flex;gap:8px;align-items:flex-start;line-height:1.35;cursor:pointer;padding:4px 0}
.w-opts input{margin-top:3px;width:18px;height:18px;flex:0 0 auto;accent-color:#A61C1C}
.w-btns{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 22px}
.w-btns button{font:inherit;font-weight:600;border-radius:6px;padding:10px 18px;cursor:pointer;border:2px solid #A61C1C}
.w-go{background:#A61C1C;color:#fff} .w-reset{background:#fff;color:#A61C1C}
.w-res h2{margin-top:28px}
.w-item{border-left:4px solid #A61C1C;background:#fff;border-radius:0 8px 8px 0;padding:12px 16px;margin:0 0 10px}
.w-item h3{margin:0 0 4px;font-size:1.05rem}
.w-item p{margin:4px 0;font-size:.97rem}
.w-item .w-tag{display:inline-block;font-size:.8rem;font-weight:600;background:#f7f5f4;border:1px solid #e4e0dc;border-radius:4px;padding:1px 6px;margin-right:6px}
.w-note{background:#f7f5f4;border-radius:8px;padding:12px 16px;margin:0 0 12px}
.w-empty{color:#555}
#w-atrisk[hidden]{display:none}
"""

def page():
    url = 'https://robertjpark.co.uk/tools/which-eu-rules-apply.html'
    title = 'Which EU rules apply to me? Northern Ireland and the Windsor Framework'
    desc = 'Three questions about what you make and where it goes, and a list of the EU and UK rules that matter to your business in Northern Ireland, with dates and official sources.'
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://robertjpark.co.uk/assets/og-image.jpg">
<link rel="icon" type="image/svg+xml" href="/assets/tools-mark.svg">
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<style>{HEAD_CSS}</style>
<style>{K_CSS}{EXTRA_CSS}{EXTRA}{TOOL_CSS}</style>
</head>
<body>
<header class="site-top">
  <a class="brand" href="/" aria-label="Robert J. Park home"><img src="/assets/tools-mark.svg" alt="" width="30" height="30">Robert J. <b>Park</b> · Tools</a>
  <nav aria-label="Main"><a href="/">Home</a><a href="/services/">Services</a><a href="/tools/">Tools</a><a href="/dashboards/">Dashboards</a><a href="/blog/">Blog</a><a href="/contact/">Contact</a></nav>
</header>
<main id="dash-root">
<div class="k-wrap">
<header class="k-head"><h1>Which EU rules apply to me?</h1>
<p>Answer three questions about what you make and where it goes. You get the EU and UK rules from the <a href="/tools/dashboards/eu-law-windsor-framework.html">EU law and the Windsor Framework dashboard</a> that matter to you, with dates and official sources. As at {AS_AT}. Nothing you tick leaves your browser.</p></header>

<form id="w-form" novalidate>
<fieldset class="w-q"><legend>1. What do you make, sell or handle?</legend><p class="w-hint">Tick all that apply.</p>
<div class="w-opts">{''.join(f'<label><input type="checkbox" name="tag" value="{k}">{esc(v)}</label>' for k, v in TAGS)}</div></fieldset>

<fieldset class="w-q"><legend>2. Where do your goods go?</legend><p class="w-hint">Tick all that apply.</p>
<div class="w-opts">
<label><input type="checkbox" name="route" value="ni">We sell or use goods in Northern Ireland</label>
<label><input type="checkbox" name="route" value="gb2ni">We move goods from Great Britain into Northern Ireland</label>
<label><input type="checkbox" name="route" value="ni2gb">We are in Northern Ireland and sell into Great Britain</label>
<label><input type="checkbox" name="route" value="eu">We sell into Ireland or elsewhere in the EU</label>
</div></fieldset>

<fieldset class="w-q" id="w-atrisk" hidden><legend>3. Are the goods you bring from Great Britain "at risk" of moving on into the EU?</legend>
<p class="w-hint">Goods are "not at risk" when an authorised trader under the UK Internal Market Scheme declares they will stay in the UK.</p>
<div class="w-opts">
<label><input type="radio" name="risk" value="no">Not at risk: they stay in Northern Ireland or the UK</label>
<label><input type="radio" name="risk" value="yes">At risk: some may go on to Ireland or the EU</label>
<label><input type="radio" name="risk" value="unsure" checked>Not sure</label>
</div></fieldset>

<div class="w-btns"><button type="submit" class="w-go">Show my rules</button><button type="reset" class="w-reset">Start again</button></div>
</form>

<div id="w-res" class="w-res" aria-live="polite"></div>

<section class="k-cta"><p><strong>Want this turned into a compliance register?</strong></p><p>I help Northern Ireland businesses work out which rules apply to what they make and where it goes, and what to do first. <a href="/contact/">Get in touch</a> or see <a href="/services/">what I do</a>.</p></section>
<h2 class="k-h2">About this tool</h2>
<section class="k-card"><p class="k-note">A guide, not legal advice. It covers the selected laws on the EU law dashboard (environment, carbon, products and goods), not every EU law that applies in Northern Ireland, and it does not cover tax, employment or data rules. It is rebuilt from the dashboard's data each time the dashboard is updated, every Friday. Check the official source on each result before you act.</p></section>
<p class="k-foot">Related: <a href="/tools/dashboards/eu-law-windsor-framework.html">EU law and the Windsor Framework dashboard</a> · <a href="/tools/dashboards/cbam-exposure-tracker.html">CBAM Exposure Tracker</a>.</p>
</div>
</main>
<footer class="site-foot">Robert J. Park · Environment · Carbon · Public Affairs · Northern Ireland. Checked on {AS_AT}. <a href="/contact/">Contact</a> · <a href="/privacy/">Privacy</a></footer>
<script id="w-data" type="application/json">{DATA}</script>
<script>
(function(){{
var D=JSON.parse(document.getElementById('w-data').textContent);
var f=document.getElementById('w-form'),out=document.getElementById('w-res'),risk=document.getElementById('w-atrisk');
function vals(n){{return Array.prototype.map.call(f.querySelectorAll('input[name="'+n+'"]:checked'),function(i){{return i.value}})}}
function e(s){{var d=document.createElement('div');d.textContent=s==null?'':String(s);return d.innerHTML}}
function link(r){{return r.u?'<a href="'+e(r.u)+'" rel="noopener">'+e(r.n)+'</a>':e(r.n)}}
function hit(r,tags){{return r.tags.indexOf('ALL')>-1||r.tags.some(function(t){{return tags.indexOf(t)>-1}})}}
f.addEventListener('change',function(){{risk.hidden=vals('route').indexOf('gb2ni')<0}});
f.addEventListener('reset',function(){{setTimeout(function(){{risk.hidden=true;out.innerHTML=''}},0)}});
f.addEventListener('submit',function(ev){{
 ev.preventDefault();
 var tags=vals('tag'),routes=vals('route'),rk=(vals('risk')[0]||'unsure'),h='';
 if(!tags.length||!routes.length){{out.innerHTML='<p class="w-note">Tick at least one answer to question 1 and one to question 2.</p>';out.focus&&out.focus();return}}
 var inNI=routes.indexOf('ni')>-1||routes.indexOf('gb2ni')>-1,gb2ni=routes.indexOf('gb2ni')>-1,ni2gb=routes.indexOf('ni2gb')>-1,eu=routes.indexOf('eu')>-1;
 if(inNI){{
  var a=D.rows.filter(function(r){{return r.g==='ni'&&hit(r,tags)&&(r.tags.indexOf('ALL')<0||gb2ni)}});
  h+='<h2>EU rules that apply to your goods in Northern Ireland ('+a.length+')</h2>';
  if(gb2ni&&rk==='no')h+='<p class="w-note">Goods declared not at risk under the UK Internal Market Scheme move with simplified paperwork, but product rules still apply once they are sold in Northern Ireland.</p>';
  if(gb2ni&&rk==='yes')h+='<p class="w-note">Goods at risk of moving into the EU need a full customs declaration, and EU duties can apply.</p>';
  h+=a.length?a.map(function(r){{return '<div class="w-item"><h3>'+link(r)+'</h3><p><span class="w-tag">'+e(r.applies)+'</span>'+e(r.topic)+'</p><p><b>Key dates:</b> '+e(r.dates)+'</p><p><b>Who:</b> '+e(r.who)+'</p></div>'}}).join(''):'<p class="w-empty">None of the laws on the dashboard matches these answers.</p>';
 }}
 if(gb2ni){{
  var b=D.rows.filter(function(r){{return r.g==='gb'&&r.kind==='Selling into NI'&&hit(r,tags)}});
  if(rk==='no')b=b.concat(D.rows.filter(function(r){{return r.g==='gb'&&r.n.indexOf('Parcel')===0&&hit(r,tags)}}));
  h+='<h2>Moving goods from Great Britain into Northern Ireland ('+b.length+')</h2>'+(b.length?b.map(function(r){{return '<div class="w-item"><h3>'+link(r)+'</h3><p>'+e(r.what)+'</p><p><b>Key date:</b> '+e(r.dates)+'</p></div>'}}).join(''):'<p class="w-empty">Nothing extra on the dashboard for these goods.</p>');
 }}
 if(inNI||ni2gb){{
  var c=D.rows.filter(function(r){{return r.g==='gb'&&r.kind!=='Selling into NI'&&hit(r,tags)}});
  h+='<h2>Where GB and NI rules differ ('+c.length+')</h2>';
  if(ni2gb)h+='<p class="w-note">Qualifying Northern Ireland goods have unfettered access to the GB market. Where GB rules differ, check which ones you must meet for what you sell in GB.</p>';
  h+=c.length?c.map(function(r){{return '<div class="w-item"><h3>'+link(r)+'</h3><p><span class="w-tag">'+e(r.kind)+'</span>'+e(r.what)+'</p><p><b>Key date:</b> '+e(r.dates)+'</p></div>'}}).join(''):'<p class="w-empty">No differences on the dashboard for these goods.</p>';
 }}
 if(eu){{
  var d=D.rows.filter(function(r){{return r.g==='eu'}});
  h+='<h2>Rules that reach you through EU customers ('+d.length+')</h2><p class="w-note">These EU laws do not apply in Northern Ireland, but EU customers may ask you for data or terms because of them.</p>'+d.map(function(r){{return '<div class="w-item"><h3>'+link(r)+'</h3><p>'+e(r.why)+'</p></div>'}}).join('');
 }}
 h+='<p class="w-note">This list covers the laws on the <a href="/tools/dashboards/eu-law-windsor-framework.html">EU law dashboard</a> only. It is a starting point, not legal advice.</p>';
 out.innerHTML=h;out.setAttribute('tabindex','-1');out.focus();
}});
}})();
</script>
</body>
</html>
'''

out_path = os.path.join(ROOT, 'tools/which-eu-rules-apply.html')
open(out_path, 'w', encoding='utf-8').write(page())
print('wrote', out_path, len(rows), 'rows')
