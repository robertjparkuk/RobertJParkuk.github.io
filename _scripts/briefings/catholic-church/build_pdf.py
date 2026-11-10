"""Render briefing.html to a branded A4 PDF. Usage: python3 build_pdf.py <repo-root>"""
import sys, pathlib
from playwright.sync_api import sync_playwright
here = pathlib.Path(__file__).resolve().parent
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
out = root / "assets/briefings/2026-11-catholic-church-science-business-environment-briefing.pdf"
out.parent.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto((here / "briefing.html").as_uri())
    pg.pdf(path=str(out), format="A4", print_background=True, prefer_css_page_size=True,
           display_header_footer=True, header_template="<span></span>",
           footer_template='<div style="font-size:7pt;color:#777;width:100%;text-align:center;font-family:sans-serif">Robert J. Park · Faith, reason and the common home · <span class="pageNumber"></span>/<span class="totalPages"></span></div>')
    b.close()
print(out)
