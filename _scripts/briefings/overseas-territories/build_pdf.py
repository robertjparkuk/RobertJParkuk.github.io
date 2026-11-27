"""Builds the branded PDF of the Overseas Territories briefing from the post.
Run from the repo root:  python3 _scripts/briefings/overseas-territories/build_pdf.py"""
import re, html, sys, os, markdown
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'crown-dependencies'))
import build_pdf as b
post = open(b.ROOT + '/_posts/2026-11-25-overseas-territories-and-carbon.md', encoding='utf-8').read().split('---', 2)[2]
post = re.sub(r'<figure class="page-photo">.*?</figure>\s*', '', post, flags=re.S)
post = re.sub(r'\[Download the briefing \(PDF\)\]\([^)]*\)\s*', '', post)
m = re.search(r'^\*(Rules checked.*?)\*\s*$', post, flags=re.M); status = m.group(1); post = post.replace(m.group(0), '', 1)
post = re.sub(r'^\*Created with assistive technology.*?\*\s*$', '', post, flags=re.M)
body = markdown.markdown(b.liquid(post), extensions=['tables', 'md_in_html']).replace('<div class="answer-box">', '<div class="box">')
body += "<p class='prov'>Created with assistive technology including AI and re-checked against the official sources listed. Robert J. Park &middot; Environment &middot; Carbon &middot; Public Affairs &middot; robert@robertjpark.co.uk &middot; 07450 349480</p>"
doc = b.page("Overseas Territories and carbon: Gibraltar, the Falklands and the rest under the UK ETS and CBAM",
             "Briefing &middot; UK ETS &middot; EU ETS &middot; CBAM &middot; Overseas Territories",
             "Briefing &middot; 25 November 2026<br>Overseas Territories and carbon<br>Status as at 25 November 2026",
             "How the UK and EU carbon markets and the UK carbon border charge treat ships, flights and goods moving between the UK and the British Overseas Territories.",
             html.escape(status), body, "Briefing \\00B7  25 November 2026")
out = sys.argv[1] if len(sys.argv) > 1 else b.ROOT + '/assets/briefings/2026-11-overseas-territories-and-carbon-briefing.pdf'
b.pdf(doc, out); print('wrote', out)
