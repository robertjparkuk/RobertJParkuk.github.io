"""NI Consultations Monitor dashboard.

Usage: python3 consultations_build.py <repo_root>

Reads data/dashboards/ni-consultations/consultations.json and council_access.json
and writes tools/dashboards/ni-consultations-monitor.html: one self-contained page,
no outside scripts, self-hosted fonts, a CSV download per table.

The data files are the same ones behind the private Claude dashboard of the same
name. To refresh: update the JSON (status roll-forward, new consultations,
published responses), set AS_AT, add a line to CHANGES, run this script.
"""
import sys, os, re, html, json, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'build.py'), encoding='utf-8').read()
exec(src[:src.index('\nD = {}')])  # helpers (esc, tile, csv_href) and CSS only

AS_AT = '13 November 2026'
WINDOW_FROM = '22 April 2025'
TODAY = dt.datetime.strptime(AS_AT, '%d %B %Y')
DATA = os.path.join(ROOT, 'data', 'dashboards', 'ni-consultations')
rows = json.load(open(os.path.join(DATA, 'consultations.json'), encoding='utf-8'))
access = json.load(open(os.path.join(DATA, 'council_access.json'), encoding='utf-8'))

CHANGES = [  # newest first: date, what changed
 ('13 Nov 2026', 'Weekly refresh: 11 added (431 in all), including the DfI regulations on pavement and footway parking, a DAERA anchoring ban for the Outer Belfast Lough Marine Conservation Zone and DfC’s draft arts policy; 9 rolled to closed; DAERA’s final Nature Recovery Strategy and consultation report recorded as the response; closing date added for the Ballyclare and Coalisland speed limits and opening date corrected for the Newry Inner City Greenway.'),
 ('6 Nov 2026', 'Weekly refresh: 19 added (420 in all), including the DfI Quay Street car park abandonment in Lisburn, Belfast’s draft playing pitches strategy and the HM Treasury consultation on adding refinery products to the UK CBAM; 3 rolled to closed; responses found for the Lagan Meadows quiet area and Belfast’s Sailortown and Cathedral Quarter masterplans; the Black Paths engagement now opens on 16 November; closing dates filled for 11 records; a duplicate Single Construction Regulator entry removed.'),
 ('5 Nov 2026', 'Correction: the DfI classes and thresholds review was listed twice (the original 9 October close and the 6 November extension). The duplicate is removed; 402 consultations.'),
 ('5 Nov 2026', 'Published. Data first compiled on 22 October 2026 and refreshed on 5 November: 12 consultations that closed between 23 October and 4 November marked closed and awaiting a response; 18 added, including the DfI review of planning classes and thresholds (extended to 6 November), the Eastern Transport Plan engagement, Moving Together, the Black Paths scheme and the Planning Appeals Commission fee regulations.'),
]

LEVELS = ['Council', 'NI Executive', 'UK Government']
STATUS_WORD = {'open': 'Open', 'upcoming': 'Not yet open', 'closed_awaiting_response': 'Closed, awaiting response',
               'closed_response_published': 'Closed, response published', 'closed_unknown_response': 'Closed, no response found'}

def d_iso(s):
    try: return dt.datetime.strptime(s, '%Y-%m-%d')
    except Exception: return None
def d_show(s):
    d = d_iso(s); return d.strftime('%-d %b %Y') if d else '—'
def days_left(s):
    d = d_iso(s); return (d - TODAY).days if d else None
def pill(word, cls=''): return f'<span class="k-pill {cls}">{esc(word)}</span>'
def rel_pill(r):
    return pill(r.capitalize(), {'high': 'k-rel-high', 'medium': 'k-rel-med', 'low': 'k-no'}[r])
def st_pill(s):
    cls = {'open': 'k-yes', 'upcoming': 'k-part', 'closed_response_published': 'k-yes', 'closed_awaiting_response': 'k-part'}.get(s, 'k-no')
    return pill(STATUS_WORD[s], cls)
def a(t, u):
    return f'<a href="{esc(u)}" rel="noopener">{esc(t)}</a>' if u and u.startswith('http') else esc(t)

def tablebox(cols, trs, tid, extra_cls=''):
    th = ''.join(f'<th scope="col">{esc(c)}</th>' for c in cols)
    return f'<div class="k-tablebox {extra_cls}"><table class="k-table" id="{tid}"><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'

def section(sid, title, note, body, csv_cols=None, csv_rows=None, fname=None, srcnote='', filt=False, csv_url=None):
    filt_html = ''
    if filt:
        filt_html = (f'<div class="k-filter"><label for="f-{sid}">Filter</label><input id="f-{sid}" type="search" data-filter="t-{sid}" '
                     f'placeholder="Type a word: planning, DfI, Belfast, waste…" autocomplete="off"><span class="k-count" aria-live="polite"></span></div>')
    act = ''
    if csv_url:
        act = f'<div class="k-actions"><a download="{fname}.csv" href="{csv_url}">Download CSV</a></div>'
    elif csv_cols:
        act = f'<div class="k-actions"><a download="{fname}.csv" href="{csv_href(csv_cols, csv_rows)}">Download CSV</a></div>'
    return (f'<section class="k-card k-wide" id="{sid}" aria-label="{esc(title)}"><h3>{esc(title)}<a class="k-anchor" href="#{sid}" aria-label="Link to this section">#</a></h3>'
            f'<p class="k-note">{note}</p>{filt_html}{body}{act}<p class="k-src">{srcnote}</p></section>')

# Derived sets -----------------------------------------------------------------------
open_rows = [r for r in rows if r['status'] == 'open']
closed_rows = [r for r in rows if r['status'].startswith('closed')]
published = [r for r in closed_rows if r['status'] == 'closed_response_published']
in14 = [r for r in open_rows if r['closes'] and days_left(r['closes']) is not None and 0 <= days_left(r['closes']) <= 14]
high_open = [r for r in open_rows if r['relevance'] == 'high']
share = f'{100 * len(published) / len(closed_rows):.0f}%' if closed_rows else '—'

tiles = [
 tile('Open now', str(len(open_rows)), 'Councils, Stormont departments and UK Government where NI is in scope'),
 tile('Closing in 14 days', str(len(in14)), f'From {AS_AT}. Act on these first', 'k-bad' if in14 else ''),
 tile('High public-realm relevance, open', str(len(high_open)), 'Planning, land, streets, water and infrastructure'),
 tile(f'Closed since {WINDOW_FROM}', str(len(closed_rows)), 'The recent window this page covers'),
 tile('Response published', share, f'Share of the {len(closed_rows)} closed consultations with an outcome report'),
]

# 1. Closing soon ----------------------------------------------------------------------
soon = sorted(open_rows, key=lambda r: r['closes'] or '9999')
trs = []
for r in soon:
    dl = days_left(r['closes'])
    urgent = ' class="k-urgent"' if dl is not None and dl <= 7 else ''
    trs.append(f'<tr><td{urgent}>{esc(d_show(r["closes"]))}</td><td{urgent}>{"—" if dl is None else dl}</td><td>{esc(r["body_short"])}</td>'
               f'<td>{a(r["title"], r["url"])}</td><td>{rel_pill(r["relevance"])}</td></tr>')
c1 = ['Closes', 'Days left', 'Body', 'Consultation', 'Public-realm relevance']
card_soon = section('closing-soon', 'Open consultations by closing date',
    f'Soonest first, counted from {AS_AT}. A dash means the body gives no closing date. Red: a week or less to go.',
    tablebox(c1, trs, 't-closing-soon'), c1 + ['Link'], [[r['closes'], days_left(r['closes']) if r['closes'] else '', r['body_short'], r['title'], r['relevance'], r['url']] for r in soon],
    'ni-consultations-closing-soon', 'Sources: each body’s own consultation page or NI Citizen Space; the link in each row.', filt=True)

# 2. By body -------------------------------------------------------------------------------
by_body = {}
for r in rows:
    o = by_body.setdefault(r['body_short'], {'level': r['level'], 'open': 0, 'awaiting': 0, 'published': 0, 'none': 0, 'total': 0})
    o['total'] += 1
    if r['status'] in ('open', 'upcoming'): o['open'] += 1
    elif r['status'] == 'closed_awaiting_response': o['awaiting'] += 1
    elif r['status'] == 'closed_response_published': o['published'] += 1
    else: o['none'] += 1
lv = {l: i for i, l in enumerate(LEVELS)}
bb = sorted(by_body.items(), key=lambda kv: (lv[kv[1]['level']], -kv[1]['total']))
mx = max(v['total'] for _, v in bb)
trs = []; last = None
for b, v in bb:
    if v['level'] != last:
        trs.append(f'<tr class="k-grp"><th scope="rowgroup" colspan="7">{esc(v["level"])}</th></tr>'); last = v['level']
    seg = ''.join(f'<i class="k-seg k-s-{k}" style="flex:{v[k]} 0 0" title="{esc(n)}: {v[k]}"></i>' for k, n in
                  (('open', 'Open or upcoming'), ('awaiting', 'Closed, awaiting response'), ('published', 'Response published'), ('none', 'No response found')) if v[k])
    trs.append(f'<tr><td>{esc(b)}</td><td class="k-num">{v["total"]}</td><td class="k-num">{v["open"]}</td><td class="k-num">{v["awaiting"]}</td>'
               f'<td class="k-num">{v["published"]}</td><td class="k-num">{v["none"]}</td><td><span class="k-track" style="width:{100 * v["total"] / mx:.0f}%">{seg}</span></td></tr>')
c2 = ['Body', 'Total', 'Open', 'Awaiting response', 'Response published', 'No response found']
legend = ('<p class="k-note k-legend"><i class="k-seg k-s-open"></i> Open or upcoming <i class="k-seg k-s-awaiting"></i> Closed, awaiting response '
          '<i class="k-seg k-s-published"></i> Response published <i class="k-seg k-s-none"></i> No response found</p>')
card_body = section('by-body', 'Consultations by body and status',
    f'Open now plus closed since {WINDOW_FROM}. "No response found" means no outcome report was found on the body’s pages when checked; it may still be in preparation.',
    legend + tablebox(c2 + [''], trs, 't-by-body'), c2, [[b, v['total'], v['open'], v['awaiting'], v['published'], v['none']] for b, v in bb],
    'ni-consultations-by-body', 'Source: the full list below.')

# 3. Response rate by level --------------------------------------------------------------------
trs = []; lvl_rows = []
for l in LEVELS:
    c = [r for r in closed_rows if r['level'] == l]
    p = sum(1 for r in c if r['status'] == 'closed_response_published')
    w = sum(1 for r in c if r['status'] == 'closed_awaiting_response')
    n = len(c) - p - w
    s = f'{100 * p / len(c):.0f}%' if c else '—'
    lvl_rows.append([l, len(c), p, w, n, s])
    trs.append(f'<tr><td>{esc(l)}</td><td class="k-num">{len(c)}</td><td class="k-num">{p}</td><td class="k-num">{w}</td><td class="k-num">{n}</td><td class="k-num"><b>{s}</b></td></tr>')
c3 = ['Level', 'Closed', 'Response published', 'Awaiting', 'None found', 'Published share']
card_level = section('response-gap', 'Have they published a response?',
    f'Closed consultations only, {WINDOW_FROM} to {AS_AT}. Consultations that closed in the two weeks before this check are counted as awaiting a response.',
    tablebox(c3, trs, 't-response-gap'), c3, lvl_rows, 'ni-consultations-response-rate', 'Source: the full list below.')

# 4. Council transparency -------------------------------------------------------------------------
pts = {'Yes': 2, 'Partial': 1, 'No': 0}
tr_rows = []
for x in access:
    c = [r for r in closed_rows if r['body_short'] == x['body_short']]
    p = sum(1 for r in c if r['status'] == 'closed_response_published')
    tr_rows.append((x, pts[x['lists_closed']] + pts[x['shows_dates']] + pts[x['page_works']], (100 * p / len(c)) if c else 0.0, len(c)))
tr_rows.sort(key=lambda t: (-t[1], -t[2]))
trs = []
for x, sc, rr, nc in tr_rows:
    cls = ' class="k-urgent"' if sc <= 2 else ''
    trs.append(f'<tr><td>{a(x["body_short"], x["page"])}</td><td class="k-num"{cls}>{sc}</td><td>{esc(x["lists_closed"])}</td><td>{esc(x["shows_dates"])}</td>'
               f'<td>{esc(x["page_works"])}</td><td class="k-num">{rr:.0f}%</td><td>{esc(x["issue"])}</td></tr>')
c4 = ['Council', 'Score /6', 'Lists closed', 'Shows dates', 'Page works', 'Response rate', 'What was found']
card_tr = section('transparency', 'Council consultation transparency',
    f'How easy each council makes it to find its consultations and their outcomes, as found on 22 October 2026 and rechecked on {AS_AT}. Two points each for listing closed consultations, showing dates and a working consultations page (one point for partly). Response rate is the share of that council’s closed consultations with a published outcome.',
    tablebox(c4, trs, 't-transparency'), c4, [[x['body_short'], sc, x['lists_closed'], x['shows_dates'], x['page_works'], f'{rr:.0f}%', x['issue']] for x, sc, rr, nc in tr_rows],
    'ni-council-consultation-transparency', 'Source: each council’s consultations page, linked in the first column.')

# 5. All consultations ---------------------------------------------------------------------------------
allr = sorted(rows, key=lambda r: (r['closes'] or '0000'), reverse=True)
trs = []
for r in allr:
    det = ''.join(f'<p><b>{esc(k)}:</b> {esc(v)}</p>' for k, v in (('Summary', r['summary']), ('Why it matters', r['relevance_note'])) if v)
    resp = f'<p><b>Response:</b> {a("Outcome report", r["response_url"])}' + (f' ({esc(d_show(r["response_published"]))})' if r['response_published'] else '') + '</p>' if r['response_url'] else ''
    title = f'<details><summary>{esc(r["title"])}</summary>{det}{resp}<p>{a("Open the consultation page", r["url"])}</p></details>' if (det or resp) else a(r['title'], r['url'])
    trs.append(f'<tr><td>{esc(r["id"])}</td><td>{esc(d_show(r["opened"]))}</td><td>{esc(d_show(r["closes"]))}</td><td>{esc(r["body_short"])}</td><td>{title}</td>'
               f'<td>{st_pill(r["status"])}</td><td>{rel_pill(r["relevance"])}</td><td>{esc("Yes" if r["verified"] == "yes" else "No")}</td></tr>')
c5 = ['Ref', 'Opened', 'Closes', 'Body', 'Consultation', 'Status', 'Relevance', 'Verified', 'Link', 'Response link']
card_all = section('all', 'All consultations',
    f'Open, upcoming and closed since {WINDOW_FROM} at the 11 councils, the nine Executive departments and UK Government where NI is in scope: {len(rows)} in all. Newest closing date first. Click a title for its summary and notes. "Verified" means the dates were read on the body’s own page; the rest rest on listings or press reports.',
    tablebox(c5[:8], trs, 't-all'), c5,
    [[r['id'], r['opened'], r['closes'], r['body_short'], r['title'], STATUS_WORD[r['status']], r['relevance'], r['verified'], r['url'], r['response_url']] for r in allr],
    'ni-consultations-all', 'Sources: the 11 council consultation hubs, the nine departments’ consultation pages, NI Citizen Space, the NI Executive consultations list and GOV.UK.', filt=True,
    csv_url='/data/dashboards/ni-consultations/consultations.csv')

# Full CSV written next to the JSON, so the page need not carry it
import csv as _csv
_cols = ['id', 'level', 'body', 'body_short', 'title', 'status', 'status_label', 'opened', 'closes', 'response_published', 'relevance', 'verified', 'url', 'response_url', 'summary', 'topics', 'relevance_note', 'ni_extent', 'devolution_note', 'notes']
with open(os.path.join(DATA, 'consultations.csv'), 'w', encoding='utf-8-sig', newline='') as _f:
    _w = _csv.writer(_f); _w.writerow(_cols); [_w.writerow([r.get(c, '') for c in _cols]) for r in allr]

GLOSSARY = [
 ('What counts', 'Public consultations, calls for evidence, statutory consultations and engagement surveys run by a council, a Stormont department or a UK Government department whose scope includes Northern Ireland. Planning applications are not counted: they are on the NI Planning Portal.'),
 ('Public-realm relevance', 'My judgement of how far each consultation bears on public space, land, streets, water, drainage and infrastructure: high, medium or low. It is a reading aid, not a ranking of importance.'),
 ('Response published', 'An outcome report, summary of responses or ministerial statement on the result was found on the body’s pages. "Awaiting" means the consultation closed recently or the body says a report is coming. "None found" means nothing was found when checked, which may mean it is still in preparation.'),
 ('Verified', 'The opening and closing dates were read on the consulting body’s own page. Unverified rows rest on a listing, a council paper or a press report, and should be checked before you rely on them.'),
]

EXTRA = """
.k-pill.k-yes{border-color:var(--color-ok);color:var(--color-ok)} .k-pill.k-part{border-color:#B7791F;color:#8A5A12} .k-pill.k-no{border-color:var(--color-fg-muted)}
.k-pill.k-rel-high{border-color:var(--color-bad);color:var(--color-bad);font-weight:600} .k-pill.k-rel-med{border-color:#B7791F;color:#8A5A12}
.k-tablebox{max-height:none;overflow-x:auto} .k-table td{vertical-align:top} .k-table td.k-num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.k-urgent{color:var(--color-bad);font-weight:600} .k-table tr.k-grp th{text-align:left;background:var(--color-panel);color:var(--color-fg-muted);font-size:13px;letter-spacing:.04em;text-transform:uppercase;padding-top:14px}
.k-track{display:inline-flex;height:12px;min-width:2px;border-radius:3px;overflow:hidden;vertical-align:middle} .k-seg{display:inline-block;height:12px;width:12px}
.k-track .k-seg{width:auto} .k-s-open{background:#B3121B} .k-s-awaiting{background:#B7791F} .k-s-published{background:#2F7A3B} .k-s-none{background:#A09A96}
.k-legend .k-seg{border-radius:2px;margin:0 4px 0 10px;vertical-align:-1px} .k-legend .k-seg:first-child{margin-left:0}
.k-table details summary{cursor:pointer;font-weight:600} .k-table details p{margin:6px 0 0;font-size:14px;color:var(--color-fg-muted)} .k-table details p b{color:var(--color-fg)}
#t-all td:nth-child(5){min-width:22em} #t-all td:nth-child(1){font-variant-numeric:tabular-nums;color:var(--color-fg-muted)}
.k-filter{display:flex;gap:8px;align-items:center;margin:0 0 10px;font-size:14px} .k-filter input{flex:1;max-width:360px;padding:6px 10px;border:1px solid var(--color-border-line);border-radius:6px;font:inherit;background:var(--color-bg);color:var(--color-fg)} .k-count{color:var(--color-fg-muted)}
.k-anchor{font-size:12px;color:var(--color-fg-muted);text-decoration:none;margin-left:8px} .k-card h3:hover .k-anchor{color:var(--color-accent,#A61C1C)}
.k-glos dt{font-weight:600;margin-top:10px} .k-glos dd{margin:2px 0 0} .k-log li{margin:0 0 6px}
.k-cta{background:var(--color-accent,#A61C1C);color:#fff;border-radius:8px;padding:18px 22px} .k-cta a{color:#fff;font-weight:600} .k-cta p{margin:0 0 6px}
@media print{.site-top nav,.k-filter,.k-actions,.k-anchor,.k-cta{display:none!important}.k-card{break-inside:avoid;border:1px solid #ccc}.k-tablebox{overflow:visible}body{font-size:11px}.k-table details>*{display:block}}
"""
FILTER_JS = """<script>document.querySelectorAll('[data-filter]').forEach(function(i){var t=document.getElementById(i.getAttribute('data-filter'));var n=t.closest('section').querySelector('.k-count');i.addEventListener('input',function(){var q=i.value.toLowerCase();var k=0;t.querySelectorAll('tbody tr').forEach(function(r){if(r.classList.contains('k-grp'))return;var s=r.textContent.toLowerCase().indexOf(q)>-1;r.style.display=s?'':'none';if(s)k++});if(n)n.textContent=q?k+' of '+t.querySelectorAll('tbody tr:not(.k-grp)').length+' rows':''})});</script>"""

def page_cons(tiles, cards):
    url = 'https://robertjpark.co.uk/tools/dashboards/ni-consultations-monitor.html'
    title = 'NI Consultations Monitor'
    desc = 'Every open public consultation at Northern Ireland’s 11 councils, the nine Stormont departments and UK Government where NI is in scope, with closing dates, how often each body publishes a response, and how easy each council makes consultations to find.'
    return f'''<!doctype html>
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
<meta property="og:image" content="https://robertjpark.co.uk/assets/og-image.jpg">
<link rel="icon" type="image/svg+xml" href="/assets/tools-mark.svg">
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<style>{HEAD_CSS}</style>
<style>{K_CSS}{EXTRA_CSS}{EXTRA}</style>
</head>
<body>
<header class="site-top">
  <a class="brand" href="/" aria-label="Robert J. Park home"><img src="/assets/tools-mark.svg" alt="" width="30" height="30">Robert J. <b>Park</b> · Dashboards</a>
  <nav aria-label="Main"><a href="/">Home</a><a href="/services/">Services</a><a href="/tools/">Tools</a><a href="/dashboards/">Dashboards</a><a href="/blog/">Blog</a><a href="/contact/">Contact</a></nav>
</header>
<main id="dash-root">
<div class="k-wrap">
<header class="k-head"><h1>NI Consultations Monitor</h1>
<p>What is open for comment across Northern Ireland’s 11 councils, the nine Stormont departments and the UK Government departments whose rules reach NI, when each one closes, and whether the body ever told respondents what it decided. Checked on {AS_AT}; updated every Friday. Want to respond but short of time? <a href="/public-sector/consultation-responses/">See my own responses</a> or <a href="/contact/">get in touch</a>.</p></header>
<div class="k-tiles">{''.join(tiles)}</div>
<h2 class="k-h2">The monitor</h2>
<div class="k-grid">{''.join(cards)}</div>
<h2 class="k-h2">What changed</h2>
<section class="k-card" id="what-changed"><ul class="k-log">{''.join(f'<li><b>{esc(d)}:</b> {esc(t)}</li>' for d, t in CHANGES)}</ul><p class="k-note">Updated every Friday. Each update is logged here.</p></section>
<h2 class="k-h2">How to read this page</h2>
<section class="k-card" id="glossary"><dl class="k-glos">{''.join(f'<dt>{esc(a_)}</dt><dd>{esc(b_)}</dd>' for a_, b_ in GLOSSARY)}</dl><p class="k-src">Planning applications: <a href="https://planningregister.planningsystemni.gov.uk/" rel="noopener">NI Planning Register</a> (DfI and 10 councils) and <a href="https://www.midulstercouncil.org/planning" rel="noopener">Mid Ulster District Council planning</a>.</p></section>
<section class="k-cta"><p><strong>A consultation you should answer, and no time to write it?</strong></p><p>I draft consultation responses for Northern Ireland businesses, trade bodies and community groups, from planning and environment to carbon and procurement, and I track the outcome afterwards. <a href="/contact/">Get in touch</a> or see <a href="/public-sector/">what I do for the public sector</a>.</p></section>
<h2 class="k-h2">About this page</h2>
<section class="k-card"><p class="k-note">A dated snapshot compiled from each body’s own consultation pages, NI Citizen Space, the NI Executive consultations list and GOV.UK, first on 22 October 2026 and rechecked on {AS_AT}. Relevance ratings are my judgement. Where a council page gives no dates, dates were taken from committee papers, public notices or the press and the row is marked unverified. Nothing on this page is fetched or sent, and every table can be downloaded as CSV. Tell me about a consultation I have missed: <a href="/contact/">contact</a>.</p></section>
<p class="k-foot">More dashboards: <a href="/dashboards/">all dashboards</a>. Related: <a href="/tools/dashboards/eu-law-windsor-framework.html">EU law and the Windsor Framework</a> (open European Commission and Irish consultations) · <a href="/public-sector/consultation-responses/">Consultation responses</a>.</p>
</div>
</main>
<footer class="site-foot">Robert J. Park · Environment · Carbon · Public Affairs · Northern Ireland. Checked on {AS_AT}. <a href="/contact/">Contact</a> · <a href="/privacy/">Privacy</a></footer>
{FILTER_JS}
</body>
</html>
'''

out = page_cons(tiles, [card_soon, card_body, card_level, card_tr, card_all])
open(os.path.join(ROOT, 'tools/dashboards/ni-consultations-monitor.html'), 'w', encoding='utf-8').write(out)
print(len(out), 'bytes;', len(rows), 'rows;', len(open_rows), 'open;', len(in14), 'closing in 14 days;', share, 'published')
