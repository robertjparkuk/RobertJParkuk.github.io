"""NI Regulatory Horizon dashboard.

Usage (from the repo root): python3 _scripts/dashboards/horizon_build.py .

Reads data/dashboards/ni-regulatory-horizon/horizon.json and writes:
  tools/dashboards/ni-regulatory-horizon.html   one self-contained page: no outside scripts,
                                                self-hosted fonts, readable without JavaScript
                                                (the filters are progressive enhancement)
  data/dashboards/ni-regulatory-horizon/horizon.csv   the full list, for download

Each row in horizon.json is one dated rule change, deadline, consultation close or decision:
  id            H001, H002 ... (never reuse an id)
  date          YYYY-MM-DD, or YYYY-MM when the source gives only a month
  title         what happens, in a line
  detail        a sentence or two; say what applies in NI and what does not
  topic         one of TOPICS below
  sectors       who it affects: a list of tags (keep to the words already used)
  jurisdiction  NI, GB, UK, EU or UK–EU (where the rule applies, not who made it)
  status        in force | confirmed | expected | proposed (see STATUS below)
  kind          Rule change | Deadline | Consultation close | Decision | Milestone | Event
  action        what a reader should do, in a sentence
  source_title, source_url   the official page the date was read on (never an energy broker)
  related, related_title     optional link to a page on this site
  note          caveats; empty if none

To refresh (monthly, or when a date moves):
  1. Open each source you are changing and update the row; add new rows with the next id.
  2. Set AS_AT below and add a line to CHANGES (newest first).
  3. Run this script. Rows dated before AS_AT drop out of the timeline and are listed
     under "Passed since the last check" for one refresh; delete them from the JSON after that.
"""
import sys, os, re, html, json, csv, io, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'build.py'), encoding='utf-8').read()
exec(src[:src.index('\nD = {}')])  # house helpers (esc, tile, csv_href) and the shared dashboard CSS

AS_AT = '11 November 2026'
TODAY = dt.datetime.strptime(AS_AT, '%d %B %Y').date()
WINDOW = ('November 2026', 'December 2028')
SOON_DAYS = 90
SLUG = 'ni-regulatory-horizon'
DATA = os.path.join(ROOT, 'data', 'dashboards', SLUG)
PAGE = os.path.join(ROOT, 'tools', 'dashboards', SLUG + '.html')
SITE = 'https://robertjpark.co.uk'

CHANGES = [  # newest first: date, what changed
 ('11 Nov 2026', 'CBAM dates corrected and extended after a review: the first UK CBAM rates move to December 2026 (HMRC publishes them by the start of each quarter); EU certificate sales dated 1 February 2027; the refinery consultation close marked confirmed; the £50,000 forward test described correctly; the split 2028 UK returns added (31 July and 29 September); added the HMRC guidance feedback close (13 November), the EU ETS review target (11 December), the pending Commission CBAM acts and the proposed 2028 EU downstream extension. 68 items.'),
 ('9 Nov 2026', 'Published, approved by Robert on 9 November 2026. 62 dated items from November 2026 to December 2028, drawn first from this site’s dashboards, Focus on issues and Policy series, then checked against the official source for each row on 9 November 2026.'),
]

TOPICS = ['Carbon', 'Energy', 'Environment', 'Waste and packaging', 'Chemicals and PFAS', 'Products',
          'Trade, customs and CBAM', 'Windsor Framework', 'Public affairs']
JURIS = {'NI': 'Applies in Northern Ireland: Stormont rules, and EU rules that reach NI under the Windsor Framework.',
         'UK': 'Applies across the UK, Northern Ireland included (some UK taxes apply in England and NI only; the row says so).',
         'GB': 'Applies in Great Britain only. Listed where it affects NI firms with GB sites, or opens a gap with NI.',
         'EU': 'An EU rule that does not apply in NI as such, but reaches NI firms through EU customers, subsidiaries or later adoption.',
         'UK–EU': 'A decision taken jointly by the UK and the EU.'}
STATUS = {'in force': ('In force', 'The law behind it already applies; the date is a step within it.'),
          'confirmed': ('Confirmed', 'The date is set in law, in an adopted EU act or by an official announcement.'),
          'expected': ('Expected', 'An official target or timetable, not yet fixed in law or liable to move.'),
          'proposed': ('Proposed', 'In consultation or draft; it may change or not happen.')}
KINDS = ['Rule change', 'Deadline', 'Consultation close', 'Decision', 'Milestone', 'Event']
BANNED = ['0' + '7595', '1578' + '25', 'github' + '.io']  # personal mobile and old host: split so this file never carries them

# Load and check --------------------------------------------------------------------
rows = json.load(open(os.path.join(DATA, 'horizon.json'), encoding='utf-8'))
problems = []
seen = set()
for r in rows:
    rid = r.get('id', '?')
    if rid in seen: problems.append(f'{rid}: duplicate id')
    seen.add(rid)
    for k in ('date', 'title', 'detail', 'topic', 'sectors', 'jurisdiction', 'status', 'kind', 'action', 'source_title', 'source_url'):
        if not r.get(k): problems.append(f'{rid}: {k} is empty')
    if not re.fullmatch(r'\d{4}-\d{2}(-\d{2})?', r.get('date', '')): problems.append(f'{rid}: date must be YYYY-MM-DD or YYYY-MM')
    if r.get('topic') not in TOPICS: problems.append(f'{rid}: unknown topic {r.get("topic")!r}')
    if r.get('jurisdiction') not in JURIS: problems.append(f'{rid}: unknown jurisdiction {r.get("jurisdiction")!r}')
    if r.get('status') not in STATUS: problems.append(f'{rid}: unknown status {r.get("status")!r}')
    if r.get('kind') not in KINDS: problems.append(f'{rid}: unknown kind {r.get("kind")!r}')
    if not str(r.get('source_url', '')).startswith('https://'): problems.append(f'{rid}: source_url must be https')
    rel = r.get('related', '')
    if rel:
        m = re.fullmatch(r'/blog/(\d{4})/(\d{2})/([a-z0-9-]+)/', rel)
        if m:
            if not any(f.startswith(f'{m.group(1)}-{m.group(2)}-') and f[11:-3] == m.group(3) for f in os.listdir(os.path.join(ROOT, '_posts'))):
                print(f'warning: {rid}: related post {rel} not found in _posts')
        elif rel.startswith('/blog/'):
            if not os.path.exists(os.path.join(ROOT, rel.strip('/'), 'index.html')) and not any(
                    f'permalink: {rel}' in open(os.path.join(ROOT, '_posts', f), encoding='utf-8').read() for f in os.listdir(os.path.join(ROOT, '_posts'))):
                print(f'warning: {rid}: related page {rel} not found')
        elif not os.path.exists(os.path.join(ROOT, rel.lstrip('/'))):
            print(f'warning: {rid}: related file {rel} not found')
if problems:
    sys.exit('horizon.json has problems:\n  ' + '\n  '.join(problems))

def d_of(r):
    """Date used for sorting and counting. A month-only date counts from the 1st of the month."""
    s = r['date']
    return dt.date.fromisoformat(s if len(s) == 10 else s + '-01')
def label(r, long=False):
    d = d_of(r)
    if len(r['date']) == 7: return d.strftime('%B %Y' if long else '%b %Y')
    return d.strftime('%-d %B %Y' if long else '%-d %b %Y')
def days_left(r):
    d = d_of(r)
    if len(r['date']) == 7 and (d.year, d.month) == (TODAY.year, TODAY.month): return 0
    return (d - TODAY).days
def is_past(r):
    if len(r['date']) == 7: return (d_of(r).year, d_of(r).month) < (TODAY.year, TODAY.month)
    return d_of(r) < TODAY

rows.sort(key=lambda r: (d_of(r), len(r['date']), r['id']))
live = [r for r in rows if not is_past(r)]
past = [r for r in rows if is_past(r)]
soon = [r for r in live if days_left(r) <= SOON_DAYS]
soon_end = TODAY + dt.timedelta(days=SOON_DAYS)
firm = [r for r in live if r['status'] in ('in force', 'confirmed')]
cons = [r for r in live if r['kind'] == 'Consultation close']
cbam = next((r for r in live if r['id'] == 'H010'), None)
years = sorted({d_of(r).year for r in live})
nxt = next((r for r in live if len(r['date']) == 10), None)
sectors_all = sorted({s for r in live for s in r['sectors']})

def slug(t): return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')
def pill(kind, key, text): return f'<span class="h-pill h-{kind}-{slug(key)}">{esc(text)}</span>'
def st_pill(r): return pill('st', r['status'], STATUS[r['status']][0])
def ju_pill(r): return pill('ju', r['jurisdiction'], r['jurisdiction'])
def ext(t, u): return f'<a href="{esc(u)}" rel="noopener">{esc(t)}</a>'
def when_cell(r):
    dl = days_left(r)
    rel = 'this month' if len(r['date']) == 7 and dl == 0 else ('tomorrow' if dl == 1 else (f'in {dl} days' if dl < 120 else f'in about {round(dl / 30.4)} months'))
    return f'<time datetime="{esc(r["date"])}">{esc(label(r))}</time><span class="h-rel">{esc(rel)}</span>'

# Tiles ---------------------------------------------------------------------------------
tiles = [
 tile('Dates on this page', str(len(live)), f'{WINDOW[0]} to {WINDOW[1]}; {len(firm)} in force or confirmed'),
 tile(f'In the next {SOON_DAYS} days', str(len(soon)), f'To {soon_end.strftime("%-d %B %Y")}', 'k-bad' if soon else ''),
 tile('Next fixed date', label(nxt) if nxt else '—', nxt['title'] if nxt else 'Nothing listed'),
 tile('UK CBAM starts', f'{days_left(cbam)} days' if cbam else '1 Jan 2027', 'Counted from ' + AS_AT + '; 1 January 2027, NI included'),
 tile('Consultations closing', str(len(cons)), 'Official consultations on this page still open'),
]

# Month jump list ----------------------------------------------------------------------------
months = []
for r in live:
    k = d_of(r).strftime('%Y-%m')
    if not months or months[-1][0] != k: months.append([k, 0])
    months[-1][1] += 1
jump = []
for y in years:
    ms = ''.join(f'<a href="#m-{k}">{dt.date.fromisoformat(k + "-01").strftime("%b")}<span class="h-n">{n}</span></a>' for k, n in months if k.startswith(str(y)))
    jump.append(f'<li><b>{y}</b>{ms}</li>')
jump_html = f'<nav class="h-jump" aria-label="Jump to a month"><ul>{"".join(jump)}</ul></nav>'

# Month chart (inline SVG, coloured by CSS so it follows light and dark) ---------------------------
def month_chart():
    start = dt.date(TODAY.year, TODAY.month, 1)
    allm = []
    m = start
    last = max(d_of(r) for r in live)
    while m <= last:
        allm.append(m)
        m = dt.date(m.year + (m.month == 12), 1 if m.month == 12 else m.month + 1, 1)
    cnt = {k: [0, 0] for k in (x.strftime('%Y-%m') for x in allm)}
    for r in live:
        cnt[d_of(r).strftime('%Y-%m')][0 if r['status'] in ('in force', 'confirmed') else 1] += 1
    mx = max(a + b for a, b in cnt.values())
    bw, gap, H, top, base = 26, 6, 170, 18, 132
    W = 40 + len(allm) * (bw + gap)
    o = [f'<svg class="h-chart" viewBox="0 0 {W} {H}" role="img" aria-labelledby="h-chart-t"><title id="h-chart-t">Dates per month, {allm[0].strftime("%B %Y")} to {allm[-1].strftime("%B %Y")}: solid for in force or confirmed, pale for expected or proposed. Each bar links to its month.</title>']
    for t in range(0, mx + 1, 2):
        y = base - t / mx * (base - top)
        o.append(f'<line class="h-grid" x1="30" x2="{W}" y1="{y:.1f}" y2="{y:.1f}"/><text class="h-ax" x="24" y="{y + 4:.1f}" text-anchor="end">{t}</text>')
    for i, m in enumerate(allm):
        k = m.strftime('%Y-%m'); a, b = cnt[k]; x = 40 + i * (bw + gap)
        ha = a / mx * (base - top); hb = b / mx * (base - top)
        tip = f'{m.strftime("%B %Y")}: {a + b} date{"s" if a + b != 1 else ""} ({a} in force or confirmed, {b} expected or proposed)'
        inner = f'<title>{esc(tip)}</title><rect class="h-bar-firm" x="{x}" y="{base - ha:.1f}" width="{bw}" height="{ha:.1f}"/><rect class="h-bar-soft" x="{x}" y="{base - ha - hb:.1f}" width="{bw}" height="{hb:.1f}"/>'
        if a + b:
            o.append(f'<a href="#m-{k}">{inner}<text class="h-val" x="{x + bw / 2}" y="{base - ha - hb - 4:.1f}" text-anchor="middle">{a + b}</text></a>')
        o.append(f'<text class="h-ax" x="{x + bw / 2}" y="{base + 15}" text-anchor="middle">{m.strftime("%b")[0]}</text>')
        if m.month == 1 or i == 0:
            o.append(f'<text class="h-ax h-yr" x="{x}" y="{base + 32}">{m.year}</text>')
    o.append('</svg>')
    legend = '<p class="h-legend"><span><i class="h-key h-key-firm"></i>In force or confirmed</span><span><i class="h-key h-key-soft"></i>Expected or proposed</span></p>'
    return '<div class="h-chartbox">' + ''.join(o) + '</div>' + legend

_top = sorted(months, key=lambda m_: (-m_[1], m_[0]))[:3]
busy_note = ('How the dates bunch. The busiest months are ' + ', '.join(f'{dt.date.fromisoformat(k + "-01").strftime("%B %Y")} ({n})' for k, n in _top[:-1])
             + f' and {dt.date.fromisoformat(_top[-1][0] + "-01").strftime("%B %Y")} ({_top[-1][1]}).')

# Next 90 days list ----------------------------------------------------------------------------
soon_html = '<ol class="h-soon">' + ''.join(
    f'<li><a class="h-soon-d" href="#{esc(r["id"])}">{esc(label(r))}</a><span class="h-soon-t">{ju_pill(r)} {esc(r["title"])}</span><span class="h-soon-s">{st_pill(r)}</span></li>' for r in soon) + '</ol>'

# The timeline table -----------------------------------------------------------------------------
COLS = ['When', 'What happens', 'Who it affects', 'Where', 'Status', 'Action needed', 'Official source']
trs = []; cur = None
for r in live:
    k = d_of(r).strftime('%Y-%m')
    if k != cur:
        cur = k
        trs.append(f'<tr class="h-month" id="m-{k}"><th colspan="7" scope="colgroup"><span>{d_of(r).strftime("%B %Y")}</span></th></tr>')
    tags = ''.join(f'<li>{esc(s)}</li>' for s in r['sectors'])
    extra = (f'<p class="h-note">{esc(r["note"])}</p>' if r.get('note') else '') + \
            (f'<p class="h-more">On this site: <a href="{esc(r["related"])}">{esc(r["related_title"] or r["related"])}</a></p>' if r.get('related') else '')
    attrs = (f'data-topic="{esc(r["topic"])}" data-where="{esc(r["jurisdiction"])}" data-status="{esc(r["status"])}" '
             f'data-kind="{esc(r["kind"])}" data-sectors="{esc("|".join(r["sectors"]))}"')
    trs.append(
        f'<tr id="{esc(r["id"])}" class="h-row" {attrs}>'
        f'<td class="h-when" data-label="When">{when_cell(r)}</td>'
        f'<td class="h-what" data-label="What happens"><span class="h-topic">{esc(r["topic"])} · {esc(r["kind"])}</span><strong>{esc(r["title"])}</strong><p>{esc(r["detail"])}</p>{extra}</td>'
        f'<td data-label="Who it affects"><ul class="h-tags">{tags}</ul></td>'
        f'<td data-label="Where">{ju_pill(r)}</td>'
        f'<td data-label="Status">{st_pill(r)}</td>'
        f'<td class="h-act" data-label="Action needed">{esc(r["action"])}</td>'
        f'<td class="h-src" data-label="Official source">{ext(r["source_title"], r["source_url"])}</td></tr>')
th = ''.join(f'<th scope="col">{esc(c)}</th>' for c in COLS)
table_html = (f'<table class="k-table h-table" id="t-horizon"><caption class="h-vh">Regulatory dates for Northern Ireland, {WINDOW[0]} to {WINDOW[1]}, by month</caption>'
              f'<thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table>')

def opts(name, label_, values):
    o = ''.join(f'<option value="{esc(v)}">{esc(t)}</option>' for v, t in values)
    return f'<label class="h-f"><span>{esc(label_)}</span><select name="{name}" data-f="{name}"><option value="">All</option>{o}</select></label>'
filters_html = (
    '<form class="h-filters" id="h-filters" hidden role="search" aria-label="Filter the dates" onsubmit="return false">'
    + opts('topic', 'Topic', [(t, t) for t in TOPICS if any(r['topic'] == t for r in live)])
    + opts('who', 'Who it affects', [(s, s) for s in sectors_all])
    + opts('where', 'Where', [(j, j) for j in JURIS if any(r['jurisdiction'] == j for r in live)])
    + opts('status', 'Status', [(k, v[0]) for k, v in STATUS.items()])
    + opts('kind', 'Type', [(k, k) for k in KINDS if any(r['kind'] == k for r in live)])
    + '<label class="h-f h-f-q"><span>Search</span><input type="search" name="q" data-f="q" placeholder="CBAM, PFAS, councils…" autocomplete="off"></label>'
    + '<button type="button" id="h-reset">Clear</button><p class="h-count" id="h-count" aria-live="polite"></p>'
    + '<p class="h-hint">Filtered views keep their settings in the page address, so you can bookmark or share them.</p></form>')

# Year by topic matrix ------------------------------------------------------------------------------
mat = []
for t in TOPICS:
    c = [sum(1 for r in live if r['topic'] == t and d_of(r).year == y) for y in years]
    if sum(c): mat.append([t] + c + [sum(c)])
tot = ['All topics'] + [sum(1 for r in live if d_of(r).year == y) for y in years] + [len(live)]
mx_cell = max(v for row_ in mat for v in row_[1:-1]) or 1
def heat(v): return f'<td class="k-num h-heat" style="--h:{v / mx_cell:.2f}">{v}</td>'
mat_trs = ''.join(f'<tr><th scope="row">{esc(m_[0])}</th>{"".join(heat(v) for v in m_[1:-1])}<td class="k-num"><b>{m_[-1]}</b></td></tr>' for m_ in mat)
mat_trs += f'<tr class="h-tot"><th scope="row">{tot[0]}</th>{"".join(f"<td class=k-num><b>{v}</b></td>" for v in tot[1:])}</tr>'
mat_cols = ['Topic'] + [str(y) for y in years] + ['Total']
mat_html = (f'<div class="h-tablewrap"><table class="k-table h-matrix"><caption class="h-vh">Number of dates by topic and year</caption><thead><tr>{"".join(f"<th scope=col>{esc(c)}</th>" for c in mat_cols)}</tr></thead>'
            f'<tbody>{mat_trs}</tbody></table></div>')
st_cols = ['Status'] + [str(y) for y in years] + ['Total']
st_rows = [[STATUS[s][0]] + [sum(1 for r in live if r['status'] == s and d_of(r).year == y) for y in years] + [sum(1 for r in live if r['status'] == s)] for s in STATUS]
st_html = (f'<div class="h-tablewrap"><table class="k-table h-matrix"><caption class="h-vh">Number of dates by status and year</caption><thead><tr>{"".join(f"<th scope=col>{esc(c)}</th>" for c in st_cols)}</tr></thead><tbody>'
           + ''.join(f'<tr><th scope="row">{esc(s_[0])}</th>{"".join(f"<td class=k-num>{v}</td>" for v in s_[1:-1])}<td class="k-num"><b>{s_[-1]}</b></td></tr>' for s_ in st_rows) + '</tbody></table></div>')

# Sources ------------------------------------------------------------------------------------------
def publisher(u):
    h = re.sub(r'^https://(www\.)?', '', u).split('/')[0]
    return {'gov.uk': 'GOV.UK', 'assets.publishing.service.gov.uk': 'GOV.UK', 'legislation.gov.uk': 'legislation.gov.uk', 'daera-ni.gov.uk': 'DAERA and NIEA',
            'economy-ni.gov.uk': 'Department for the Economy', 'niassembly.gov.uk': 'NI Assembly', 'uregni.gov.uk': 'Utility Regulator',
            'netregs.org.uk': 'NetRegs (NIEA and SEPA)', 'fca.org.uk': 'Financial Conduct Authority', 'eur-lex.europa.eu': 'EUR-Lex',
            'taxation-customs.ec.europa.eu': 'European Commission', 'environment.ec.europa.eu': 'European Commission', 'ema.europa.eu': 'ECHA (via EMA)',
            'epa.ie': 'Environmental Protection Agency (Ireland)', 'causewaycoastandglens.gov.uk': 'Causeway Coast and Glens Borough Council'}.get(h, h)
def id_links(ids): return ', '.join(f'<a href="#{i}">{i}</a>' for i in ids)
srcs = {}
for r in live:
    srcs.setdefault(publisher(r['source_url']), {}).setdefault(r['source_url'], [re.sub(r', paras? [0-9.]+( and [0-9.]+)?', '', r['source_title']), []])[1].append(r['id'])
src_html = ''.join(
    f'<li><b>{esc(p)}</b><ul>' + ''.join(f'<li>{ext(t, u)} <span class="h-ids">({id_links(ids)})</span></li>' for u, (t, ids) in v.items()) + '</ul></li>'
    for p, v in sorted(srcs.items(), key=lambda kv: -sum(len(x[1]) for x in kv[1].values())))

past_html = ''
if past:
    past_html = ('<details class="h-past"><summary>Passed since the last check (' + str(len(past)) + ')</summary><ul>' +
                 ''.join(f'<li>{esc(label(r))}: {esc(r["title"])} ({ext("source", r["source_url"])})</li>' for r in past) + '</ul></details>')

# CSV (full list, written next to the JSON) ----------------------------------------------------------
CSV_COLS = ['id', 'date', 'date_label', 'title', 'detail', 'topic', 'sectors', 'jurisdiction', 'status', 'kind', 'action',
            'source_title', 'source_url', 'related_url', 'note', 'checked']
with open(os.path.join(DATA, 'horizon.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f); w.writerow(CSV_COLS)
    for r in rows:
        w.writerow([r['id'], r['date'], label(r, True), r['title'], r['detail'], r['topic'], '; '.join(r['sectors']), r['jurisdiction'],
                    r['status'], r['kind'], r['action'], r['source_title'], r['source_url'], (SITE + r['related']) if r.get('related') else '',
                    r.get('note', ''), TODAY.isoformat()])

# Page --------------------------------------------------------------------------------------------
CSS = """
:root{--red:#A61C1C;--color-fg:#1A1A1A;--color-fg-muted:#5C5551;--color-panel:#F5F2EF;--color-border-line:#DCD4CE;--cds-chart-grid:#E9E3DE;
 --h-amber:#8A5A12;--h-eu:#1F4E8C;--h-ukeu:#11695A;--h-soft:#E4B4B4;--h-heat:166,28,28}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--red:#F07A7A;--color-fg:#F1ECE9;--color-fg-muted:#B8AFAA;--color-panel:#221E1D;--color-border-line:#3A3332;
 --cds-chart-grid:#2E2827;--h-amber:#E9B067;--h-eu:#8FB4EA;--h-ukeu:#6FCFB9;--h-soft:#6E3A3A;--h-heat:240,122,122}}
:root[data-theme="dark"]{--red:#F07A7A;--color-fg:#F1ECE9;--color-fg-muted:#B8AFAA;--color-panel:#221E1D;--color-border-line:#3A3332;
 --cds-chart-grid:#2E2827;--h-amber:#E9B067;--h-eu:#8FB4EA;--h-ukeu:#6FCFB9;--h-soft:#6E3A3A;--h-heat:240,122,122}
.h-vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.h-skip{position:absolute;left:-999px}.h-skip:focus{left:16px;top:8px;background:var(--color-bg);padding:6px 10px;z-index:9}
.k-head .h-asat{display:inline-block;font-weight:600;color:var(--color-fg);border-left:3px solid var(--red);padding-left:8px;margin:0 0 6px}
.k-tiles{grid-template-columns:repeat(auto-fit,minmax(min(100%,12.5rem),1fr))}
.k-tile .k-big{font-size:clamp(24px,3.4vw,34px);overflow-wrap:anywhere}
.k-card{min-width:0}
.h-jump ul{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.h-jump li{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.h-jump b{min-width:3em;font-variant-numeric:tabular-nums}
.h-jump a{display:inline-flex;align-items:center;gap:4px;padding:3px 9px;border:1px solid var(--color-border-line);border-radius:999px;text-decoration:none;color:var(--color-fg);font-size:14px;background:var(--color-bg)}
.h-jump a:hover,.h-jump a:focus{border-color:var(--red);color:var(--red)}
.h-n{font-size:11px;color:var(--color-fg-muted)}
.h-chartbox{width:100%}.h-chart{width:100%;height:auto;display:block}
.h-chart .h-grid{stroke:var(--cds-chart-grid);stroke-width:1}.h-chart .h-ax{fill:var(--color-fg-muted);font-size:11px;font-family:var(--font-anthropic-sans)}
.h-chart .h-yr{font-weight:600;fill:var(--color-fg)}.h-chart .h-val{fill:var(--color-fg);font-size:11px;font-weight:600;font-family:var(--font-anthropic-sans)}
.h-chart .h-bar-firm{fill:var(--red)}.h-chart .h-bar-soft{fill:var(--h-soft)}.h-chart a:hover rect,.h-chart a:focus rect{opacity:.75}
.h-legend{display:flex;gap:16px;flex-wrap:wrap;font-size:13px;color:var(--color-fg-muted);margin:6px 0 0}
.h-key{display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:6px;vertical-align:-1px}.h-key-firm{background:var(--red)}.h-key-soft{background:var(--h-soft)}
.h-soon{list-style:none;margin:0;padding:0}
.h-soon li{display:grid;grid-template-columns:7.2em 1fr auto;gap:10px;align-items:baseline;padding:8px 0;border-top:1px solid var(--color-border-line)}
.h-soon li:first-child{border-top:0}.h-soon-d{font-weight:600;font-variant-numeric:tabular-nums;text-decoration:none}
.h-pill{display:inline-block;font-size:12px;line-height:1.5;padding:0 8px;border-radius:10px;border:1px solid currentColor;white-space:nowrap;font-weight:600}
.h-st-in-force{background:var(--color-fg);color:var(--color-bg);border-color:var(--color-fg)}
.h-st-confirmed{color:var(--red)}
.h-st-expected{color:var(--h-amber);border-style:dashed}
.h-st-proposed{color:var(--color-fg-muted);border-style:dotted}
.h-ju-ni{color:var(--red)}.h-ju-gb{color:var(--color-fg)}.h-ju-uk{color:var(--color-fg-muted)}.h-ju-eu{color:var(--h-eu)}.h-ju-uk-eu{color:var(--h-ukeu)}
.h-filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,11rem),1fr));gap:10px 12px;align-items:end;margin:0 0 14px;padding:14px;border:1px solid var(--color-border-line);border-radius:8px;background:var(--color-bg)}
.h-filters[hidden]{display:none}
.h-f{display:flex;flex-direction:column;gap:3px;font-size:13px;color:var(--color-fg-muted);min-width:0}
.h-f select,.h-f input{font:inherit;font-size:15px;padding:6px 8px;border:1px solid var(--color-border-line);border-radius:6px;background:var(--color-bg);color:var(--color-fg);width:100%;min-width:0}
.h-filters button{font:inherit;font-size:14px;padding:7px 12px;border:1px solid var(--color-border-line);border-radius:6px;background:var(--color-panel);color:var(--color-fg);cursor:pointer;justify-self:start}
.h-filters button:hover{border-color:var(--red)}
.h-count{margin:0;font-size:14px;font-weight:600;grid-column:1/-1}.h-hint{margin:0;font-size:12px;color:var(--color-fg-muted);grid-column:1/-1}
.h-tablewrap{overflow-x:auto}
.h-table{table-layout:auto}
.h-table thead th{position:static;font-size:13px}
.h-table td{padding:10px 8px;vertical-align:top}
.h-table tr.h-month th{background:transparent;padding:22px 0 6px;border-bottom:2px solid var(--red);text-align:left}
.h-table tr.h-month th span{font-family:var(--font-anthropic-serif);font-size:20px;font-weight:600;color:var(--color-fg)}
.h-table tr.h-month:first-child th{padding-top:6px}
.h-when{white-space:nowrap;font-weight:600;font-variant-numeric:tabular-nums;width:7.5em}
.h-rel{display:block;font-weight:400;font-size:12px;color:var(--color-fg-muted)}
.h-what{min-width:16em}.h-what strong{display:block;font-size:15px;line-height:1.35}.h-what p{margin:4px 0 0}
.h-topic{display:block;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--color-fg-muted);margin-bottom:2px}
.h-note{font-size:13px;color:var(--color-fg-muted);font-style:italic}.h-more{font-size:13px}
.h-tags{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:4px}
.h-tags li{font-size:12px;padding:0 7px;border-radius:4px;background:var(--color-panel);border:1px solid var(--color-border-line);white-space:nowrap}
.h-act{min-width:12em}.h-src{min-width:10em;font-size:13px}.h-src a{overflow-wrap:anywhere}
.h-row:target td{background:color-mix(in srgb,var(--red) 10%,transparent)}
.h-matrix th[scope=row]{text-align:left;font-weight:400;color:var(--color-fg)}.h-matrix td,.h-matrix th{padding:6px 10px}
.h-heat{background:rgba(var(--h-heat),calc(var(--h)*.32))}.h-tot th,.h-tot td{border-top:2px solid var(--color-border-line)}
.h-def dt{font-weight:600;margin-top:10px}.h-def dd{margin:2px 0 0}.h-def .h-pill{margin-right:6px}
.h-srcs{padding-left:1.1em;font-size:14px}.h-srcs>li{margin:0 0 10px}.h-srcs ul{padding-left:1.1em;margin:4px 0 0}.h-srcs li li{margin:0 0 4px;overflow-wrap:anywhere}
.h-ids{font-size:12px;color:var(--color-fg-muted)}
.h-dl{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0}
.h-dl a{display:inline-block;padding:8px 14px;border:1px solid var(--red);border-radius:6px;text-decoration:none;font-weight:600}
.h-dl a:hover{background:var(--red);color:var(--color-bg)}
.h-past summary{cursor:pointer;font-weight:600}
.k-log li{margin:0 0 6px}
.h-cta{background:#A61C1C;color:#fff;border-radius:10px;padding:22px 24px;margin-top:var(--cds-gap-xl)}
.h-cta h2{font-family:var(--font-anthropic-serif);font-weight:600;font-size:clamp(22px,3vw,28px);margin:0 0 8px;color:#fff}
.h-cta p{margin:0 0 10px;max-width:46rem}.h-cta ul{margin:0 0 14px;padding-left:1.2em;max-width:46rem}.h-cta li{margin:0 0 4px}
.h-cta a{color:#fff}.h-cta .h-btn{display:inline-block;background:#fff;color:#A61C1C;font-weight:700;text-decoration:none;padding:10px 18px;border-radius:6px;margin:4px 12px 4px 0}
.h-cta .h-btn:hover,.h-cta .h-btn:focus{background:#F6E3E3}.h-cta small{display:block;opacity:.9;margin-top:8px}
@media (max-width:820px){
 .h-table thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
 .h-table,.h-table tbody{display:block;width:100%}
 .h-table tr.h-month{display:block}.h-table tr.h-month th{display:block}
 .h-table tr.h-row{display:grid;grid-template-columns:1fr auto auto;gap:6px 8px;padding:12px 0;border-bottom:1px solid var(--color-border-line)}
 .h-table tr.h-row td{display:block;border:0;padding:0;min-width:0;width:auto}
 .h-table td.h-when{grid-column:1;grid-row:1;white-space:normal}
 .h-table td[data-label=Where]{grid-column:2;grid-row:1}
 .h-table td[data-label=Status]{grid-column:3;grid-row:1}
 .h-table td.h-what,.h-table td[data-label="Who it affects"],.h-table td.h-act,.h-table td.h-src{grid-column:1/-1}
 .h-table td.h-act::before,.h-table td.h-src::before,.h-table td[data-label="Who it affects"]::before{content:attr(data-label);display:block;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--color-fg-muted);margin-bottom:2px}
 .h-rel{display:inline;margin-left:6px}
 .h-soon li{grid-template-columns:1fr auto}.h-soon-t{grid-column:1/-1;grid-row:2}
}
@media print{.site-top nav,.h-filters,.h-jump,.h-cta .h-btn,.h-dl,.h-skip{display:none!important}.k-card{break-inside:avoid;border:1px solid #ccc}
 body{font-size:11px}.h-table tr.h-row{break-inside:avoid}.h-cta{background:none;color:#000;border:2px solid #A61C1C}.h-cta h2,.h-cta a{color:#000}}
"""

JS = """<script>
(function(){
 var form=document.getElementById('h-filters'); if(!form||!window.URLSearchParams) return;
 form.hidden=false;
 var rows=[].slice.call(document.querySelectorAll('#t-horizon tr.h-row')), heads=[].slice.call(document.querySelectorAll('#t-horizon tr.h-month'));
 var f={}; [].forEach.call(form.querySelectorAll('[data-f]'),function(el){f[el.getAttribute('data-f')]=el;});
 var out=document.getElementById('h-count');
 function apply(push){
  var v={topic:f.topic.value,who:f.who.value,where:f.where.value,status:f.status.value,kind:f.kind.value,q:f.q.value.trim().toLowerCase()}, n=0;
  rows.forEach(function(r){
   var ok=(!v.topic||r.dataset.topic===v.topic)&&(!v.where||r.dataset.where===v.where)&&(!v.status||r.dataset.status===v.status)&&(!v.kind||r.dataset.kind===v.kind)
     &&(!v.who||r.dataset.sectors.split('|').indexOf(v.who)>-1)&&(!v.q||r.textContent.toLowerCase().indexOf(v.q)>-1);
   r.hidden=!ok; if(ok) n++;
  });
  heads.forEach(function(h){var s=h.nextElementSibling,any=false;while(s&&!s.classList.contains('h-month')){if(!s.hidden)any=true;s=s.nextElementSibling;}h.hidden=!any;});
  var active=Object.keys(v).some(function(k){return v[k];});
  out.textContent=active?(n+' of '+rows.length+' dates shown'):('All '+rows.length+' dates shown');
  if(push){var p=new URLSearchParams();Object.keys(v).forEach(function(k){if(v[k])p.set(k,k==='q'?f.q.value.trim():v[k]);});
   var s=p.toString();history.replaceState(null,'',location.pathname+(s?'?'+s:'')+location.hash);}
 }
 var p=new URLSearchParams(location.search);
 Object.keys(f).forEach(function(k){if(p.get(k)){f[k].value=p.get(k);} f[k].addEventListener(k==='q'?'input':'change',function(){apply(true);});});
 document.getElementById('h-reset').addEventListener('click',function(){Object.keys(f).forEach(function(k){f[k].value='';});apply(true);});
 apply(false);
})();
</script>"""

def section(sid, title, note, body, src=''):
    return (f'<section class="k-card k-wide" id="{sid}" aria-labelledby="{sid}-h"><h3 id="{sid}-h">{esc(title)}</h3>'
            + (f'<p class="k-note">{note}</p>' if note else '') + body + (f'<p class="k-src">{src}</p>' if src else '') + '</section>')

csv_url = f'/data/dashboards/{SLUG}/horizon.csv'
json_url = f'/data/dashboards/{SLUG}/horizon.json'
mat_csv = csv_href(mat_cols, mat + [tot])

defs = ''.join(f'<dt>{pill("st", k, v[0])}</dt><dd>{esc(v[1])}</dd>' for k, v in STATUS.items())
jdefs = ''.join(f'<dt>{pill("ju", k, k)}</dt><dd>{esc(v)}</dd>' for k, v in JURIS.items())

url = f'{SITE}/tools/dashboards/{SLUG}.html'
title = 'NI Regulatory Horizon'
desc = (f'Every dated rule change, deadline and consultation close for Northern Ireland businesses and councils on carbon, energy, environment, '
        f'waste and packaging, chemicals, products, trade, CBAM and the Windsor Framework, {WINDOW[0]} to {WINDOW[1]}, with official sources. As at {AS_AT}.')

page = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)} | Robert J. Park</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE}/assets/og-image.jpg">
<link rel="icon" type="image/svg+xml" href="/assets/tools-mark.svg">
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<style>{HEAD_CSS}</style>
<style>{K_CSS}{EXTRA_CSS}{CSS}</style>
</head>
<body>
<a class="h-skip" href="#timeline">Skip to the dates</a>
<header class="site-top">
  <a class="brand" href="/" aria-label="Robert J. Park home"><img src="/assets/tools-mark.svg" alt="" width="30" height="30">Robert J. <b>Park</b> · Dashboards</a>
  <nav aria-label="Main"><a href="/">Home</a><a href="/services/">Services</a><a href="/cbam-desk/">CBAM Desk</a><a href="/tools/">Tools</a><a href="/dashboards/">Dashboards</a><a href="/blog/">Blog</a><a href="/contact/">Contact</a></nav>
</header>
<main id="dash-root">
<div class="k-wrap">
<header class="k-head"><h1>NI Regulatory Horizon</h1>
<p class="h-asat">As at {AS_AT}</p>
<p>Every dated rule change, deadline and consultation close that matters to Northern Ireland businesses and councils on carbon, energy, environment, waste and packaging, chemicals and PFAS, products, trade, customs and CBAM, and the Windsor Framework, from {WINDOW[0]} to {WINDOW[1]}, on one page. Each date says who it affects, where it applies, how firm it is and what to do, and links to the official source it was checked against. Bookmark this page: it is updated when dates move, and each month and each row has its own link.</p></header>
<div class="k-tiles">{"".join(tiles)}</div>
<h2 class="k-h2">At a glance</h2>
<div class="k-grid">
{section('next-90-days', f'The next {SOON_DAYS} days', f'From {AS_AT} to {soon_end.strftime("%-d %B %Y")}. Select a date to jump to its row.', soon_html)}
{section('by-month', 'Dates per month', busy_note, month_chart())}
</div>
<h2 class="k-h2" id="timeline">Every date, month by month</h2>
{jump_html}
{filters_html}
<section class="k-card k-wide h-main" aria-label="Every date, month by month">
<p class="k-note">{len(live)} dates, soonest first. A month without a day means the official source gives only the month. "Where" is where the rule applies; "Status" is how firm the date is (see <a href="#how-to-read">how to read this page</a>). The source in each row is the page the date was checked on, on {AS_AT}.</p>
{table_html}
{past_html}
</section>
<h2 class="k-h2">By topic and year</h2>
<div class="k-grid">
{section('topic-year', 'Dates by topic and year', 'Each date is counted once, under its main topic. Darker cells hold more dates.', mat_html + f'<div class="k-actions"><a download="ni-regulatory-horizon-by-topic-year.csv" href="{mat_csv}">Download CSV</a></div>')}
{section('status-year', 'How firm the dates are', 'Expected and proposed dates are the ones most likely to move; they are rechecked first at each update.', st_html)}
</div>
<h2 class="k-h2" id="how-to-read">How to read this page</h2>
<section class="k-card k-wide">
<div class="k-grid"><div><h3>Status</h3><dl class="h-def">{defs}</dl></div><div><h3>Where it applies</h3><dl class="h-def">{jdefs}</dl></div></div>
<p class="k-note">Northern Ireland sits under two rulebooks. EU rules on goods, chemicals, packaging design, F-gases, batteries and deforestation apply in NI under the Windsor Framework, while UK rules on carbon pricing, CBAM, ESOS and most taxes apply too. Rows marked EU are there because they reach NI firms through EU customers, not because they apply in NI. This page is general information, not legal or tax advice: check the source for your own goods and sites.</p>
</section>
<h2 class="k-h2" id="data-and-sources">Data and sources</h2>
<section class="k-card k-wide">
<p class="k-note">The full list, with every field on this page plus the detail and notes, is free to download and reuse with credit. Dates were first gathered from this site’s dashboards (EU Law and the Windsor Framework, the CBAM Exposure Tracker and the five Focus on dashboards), the Focus on issues and the Policy series, then each one was checked on {AS_AT} against the official page linked in its row: GOV.UK, HMRC, legislation.gov.uk, DAERA and NIEA, the Department for the Economy, the NI Assembly, the Utility Regulator, the FCA, the European Commission, EUR-Lex and the Irish EPA. Commercial and energy-broker sites are not used. Notes in a row say where a date rests on a month only, a draft or a press report of a draft.</p>
<div class="h-dl"><a href="{csv_url}" download="ni-regulatory-horizon.csv">Download CSV ({len(rows)} rows)</a><a href="{json_url}">JSON</a></div>
<ul class="h-srcs">{src_html}</ul>
</section>
<h2 class="k-h2">What changed</h2>
<section class="k-card k-wide" id="what-changed"><ul class="k-log">{"".join(f"<li><b>{esc(d)}:</b> {esc(t)}</li>" for d, t in CHANGES)}</ul>
<p class="k-note">Rechecked when a source moves and at least monthly. Tell me about a date I have missed: <a href="/contact/">contact</a>. More: <a href="/tools/dashboards/ni-consultations-monitor.html">NI Consultations Monitor</a> · <a href="/tools/dashboards/eu-law-windsor-framework.html">EU Law and the Windsor Framework</a> · <a href="/tools/dashboards/cbam-exposure-tracker.html">CBAM Exposure Tracker</a> · <a href="/dashboards/">all dashboards</a>.</p></section>
<section class="h-cta" id="readiness-review" aria-labelledby="cta-h">
<h2 id="cta-h">Which of these dates are yours?</h2>
<p>The <strong>Two-Regime Readiness Review</strong> turns this page into your own plan. For a fixed £650:</p>
<ul><li>a short questionnaire, then a 90-minute call</li><li>your products and trade mapped against the UK and EU carbon border rules (CBAM) by commodity code, and against the other UK and EU rules that reach you in Northern Ireland</li><li>a 6–8 page written review with a 12-month plan: what applies, from when, and roughly what it could cost</li><li>a 30-minute follow-up call, all within ten working days</li></ul>
<a class="h-btn" href="/cbam-desk/">Book a Two-Regime Readiness Review, £650</a><a href="/contact/">Or ask a question first</a>
<small>Price fixed and quoted in writing before work starts; VAT added if it applies. The fee comes off the next service you book within three months.</small>
</section>
</div>
</main>
<footer class="site-foot">Robert J. Park · Environment · Carbon · Public Affairs · Northern Ireland. As at {AS_AT}. General information, not legal or tax advice. <a href="/contact/">Contact</a> · <a href="/privacy/">Privacy</a></footer>
{JS}
</body>
</html>
'''

for b in BANNED:
    for name, text in (('page', page), ('csv', open(os.path.join(DATA, 'horizon.csv'), encoding='utf-8-sig').read()),
                       ('json', open(os.path.join(DATA, 'horizon.json'), encoding='utf-8').read())):
        if b in text.lower(): sys.exit(f'stopped: {name} contains "{b}"')

open(PAGE, 'w', encoding='utf-8').write(page)
print(f'{len(page)} bytes; {len(live)} dates live, {len(past)} passed; {len(soon)} in the next {SOON_DAYS} days; '
      f'by year {dict((y, sum(1 for r in live if d_of(r).year == y)) for y in years)}')
