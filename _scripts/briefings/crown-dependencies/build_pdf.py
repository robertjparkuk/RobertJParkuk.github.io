"""Builds the branded PDF of the Crown Dependencies briefing from the post.
Run from the repo root:  python3 _scripts/briefings/crown-dependencies/build_pdf.py
Needs: python markdown, google-chrome. Fonts and logo come from assets/."""
import re, html, subprocess, sys, os, markdown
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
SITE = 'https://robertjpark.co.uk'

CSS = """
@font-face{font-family:'Source Sans 3';src:url('file://%(r)s/assets/fonts/source-sans-3.woff');font-weight:200 900}
@font-face{font-family:'Source Sans 3';font-style:italic;src:url('file://%(r)s/assets/fonts/source-sans-3-italic.woff');font-weight:200 900}
@font-face{font-family:'Source Serif 4';src:url('file://%(r)s/assets/fonts/source-serif-4.woff');font-weight:200 900}
@font-face{font-family:'IBM Plex Mono';src:url('file://%(r)s/assets/fonts/ibm-plex-mono-regular.woff')}
@page{size:A4;margin:16mm 16mm 18mm 16mm;
  @bottom-left{content:"Robert J. Park \\00B7  %(foot)s \\00B7  robertjpark.co.uk";font:7pt 'Source Sans 3',sans-serif;color:#5a5a5a}
  @bottom-right{content:counter(page) " / " counter(pages);font:7pt 'Source Sans 3',sans-serif;color:#5a5a5a}}
*{box-sizing:border-box}
body{margin:0;font:9.6pt/1.45 'Source Sans 3',sans-serif;color:#2b2b2b}
.top{display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid #a61c1c;padding-bottom:8px;margin-bottom:12px}
.top img{height:34px}
.meta{font:7.4pt/1.5 'IBM Plex Mono',monospace;color:#5a5a5a;text-align:right;letter-spacing:.02em}
.eyebrow{font:7.4pt 'IBM Plex Mono',monospace;color:#a61c1c;letter-spacing:.14em;text-transform:uppercase;margin:0 0 4px}
h1{font:700 21pt/1.15 'Source Serif 4',serif;color:#1a1a1a;margin:0 0 6px}
.lead{font:12pt/1.4 'Source Serif 4',serif;color:#2b2b2b;margin:0 0 10px}
.status{border-left:3px solid #a61c1c;background:#f7f4f2;padding:7px 11px;margin:8px 0 12px;font-size:8.6pt;color:#444}
.box{border-left:3px solid #a61c1c;background:#f7f4f2;padding:8px 12px;margin:10px 0;break-inside:avoid}
.box .answer-label{font:700 8pt 'Source Sans 3';letter-spacing:.1em;text-transform:uppercase;color:#a61c1c;margin:0 0 4px}
h2{font:700 13pt/1.25 'Source Serif 4',serif;color:#1a1a1a;margin:16px 0 5px;break-after:avoid}
h3{font:700 10.5pt 'Source Sans 3';margin:12px 0 4px;break-after:avoid}
p{margin:0 0 7px} ul,ol{margin:0 0 8px;padding-left:16px} li{margin:0 0 4px}
a{color:#a61c1c;text-decoration:none}
table{border-collapse:collapse;width:100%%;margin:8px 0 10px;font-size:8.6pt;break-inside:avoid}
th{background:#1a1a1a;color:#fff;text-align:left;padding:5px 7px;font-weight:600}
td{border-bottom:1px solid #e6e2e0;padding:5px 7px;vertical-align:top}
.prov{margin-top:14px;padding-top:8px;border-top:1px solid #e6e2e0;font-size:8pt;color:#5a5a5a}
"""

def page(title, eyebrow, meta, lead, status, body, foot):
    return ("<!doctype html><html lang='en-GB'><head><meta charset='utf-8'><title>%s</title><style>%s</style></head><body>"
            "<div class='top'><img src='file://%s/assets/brand/logo.svg' alt='Robert J. Park: Environment, Carbon, Public Affairs'><div class='meta'>%s</div></div>"
            "<p class='eyebrow'>%s</p><h1>%s</h1><p class='lead'>%s</p><div class='status'>%s</div>%s</body></html>"
            % (html.escape(title), CSS % {'r': ROOT, 'foot': foot}, ROOT, meta, eyebrow, html.escape(title), lead, status, body))

def liquid(src):
    src = re.sub(r"\{% post_url \d{4}-\d{2}-\d{2}-([a-z0-9-]+) %\}", lambda m: SITE + '/blog/2026/11/' + m.group(1) + '/', src)
    src = re.sub(r"\{\{ '([^']+)' \| relative_url \}\}", lambda m: SITE + m.group(1), src)
    return src

def pdf(doc, out):
    tmp = '/tmp/_briefing.html'; open(tmp, 'w', encoding='utf-8').write(doc)
    subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                    '--virtual-time-budget=3000', '--print-to-pdf=' + out, 'file://' + tmp], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == '__main__':
    post = open(ROOT + '/_posts/2026-11-24-crown-dependencies-ferries-and-carbon.md', encoding='utf-8').read().split('---', 2)[2]
    post = re.sub(r'<figure class="page-photo">.*?</figure>\s*', '', post, flags=re.S)
    post = re.sub(r'\[Download the briefing \(PDF\)\]\([^)]*\)\s*', '', post)
    m = re.search(r'^\*(Rules checked.*?)\*\s*$', post, flags=re.M); status = m.group(1); post = post.replace(m.group(0), '', 1)
    post = re.sub(r'^\*(?:Created with assistive technology|AI was used to lay out this document).*?\*\s*$', '', post, flags=re.M)
    body = markdown.markdown(liquid(post), extensions=['tables', 'md_in_html'])
    body = body.replace('<div class="answer-box">', '<div class="box">')
    body += "<p class='prov'>AI was used to lay out this document and to generate leads from the consultant's research, knowledge and questioning; figures were checked against the official sources listed. Robert J. Park &middot; Environment &middot; Carbon &middot; Public Affairs &middot; robert@robertjpark.co.uk &middot; 07450 349480</p>"
    doc = page("Crown Dependencies, ferries and carbon: the Isle of Man, Jersey and Guernsey under the UK ETS and CBAM",
               "Briefing &middot; UK ETS &middot; EU ETS &middot; CBAM &middot; Northern Ireland",
               "Briefing &middot; 24 November 2026<br>Islands, ferries and carbon<br>Status as at 24 November 2026",
               "How the UK and EU carbon markets and the UK carbon border charge treat ferries and goods moving through the Isle of Man, Jersey and Guernsey, and what changes in 2028.",
               html.escape(status), body, "Briefing \\00B7  24 November 2026")
    out = sys.argv[1] if len(sys.argv) > 1 else ROOT + '/assets/briefings/2026-11-crown-dependencies-ferries-and-carbon-briefing.pdf'
    pdf(doc, out); print('wrote', out)
