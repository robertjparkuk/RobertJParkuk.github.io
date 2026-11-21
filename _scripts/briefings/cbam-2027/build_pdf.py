import sys,re,html,markdown,asyncio
sys.argv=['x','/dev/null']
exec(open('/home/claude/brief/pdf/build.py').read().split('docs=[]')[0])
SITE='/home/claude/site'
src=open(SITE+'/_posts/2026-11-21-the-2027-cbam-horizon.md').read().split('---',2)[2]
src=re.sub(r"\{\{ '(/assets/[^']+)' \| relative_url \}\}",lambda m:'file://'+SITE+m.group(1),src)
src=re.sub(r"\{\{ '([^']+)' \| relative_url \}\}",lambda m:'https://robertjpark.co.uk'+m.group(1),src)
src=re.sub(r'\[Download the briefing \(PDF\)\]\([^)]*\) · ','',src)
END=END.replace('20 November','21 November')
body=markdown.markdown(src,extensions=['tables','md_in_html'])
body=body.replace('<div class="answer-box">','<div style="border-left:3px solid #a61c1c;background:#f7f4f2;padding:8px 12px;margin:10px 0">')
body=body.replace('<figure class="page-photo chart">','<figure style="margin:12px 0;break-inside:avoid">').replace('<img ','<img style="width:100%" ')
title="The 2027 CBAM horizon: the transition for Northern Ireland's goods"
lead='From 1 January 2027 UK CBAM charges steel, aluminium, cement, fertiliser and hydrogen entering Northern Ireland, including from Ireland. Eight cases, the switch to GB supply, a flow chart and a route checklist.'
doc=page(title,'Briefing · CBAM · Trade · Northern Ireland','Briefing · 21 November 2026<br>UK and EU CBAM<br>Status as at 21 November 2026',html.escape(lead),
 'Status as at 21 November 2026. The intended UK exemption for EU, EEA and Swiss goods and the ETS link are announced, not law. General information, not legal, tax or customs advice.',body)
doc=doc.replace('</style>','table{font-size:8.6pt}td,th{vertical-align:top}</style>',1)
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); tmp='/home/claude/brief/cbam2027/_t.html'; open(tmp,'w').write(doc)
        pg=await b.new_page(); await pg.goto('file://'+tmp); await pg.wait_for_timeout(800)
        foot="<div style='font-family:sans-serif;font-size:7pt;color:#5a5a5a;width:100%;padding:0 16mm;display:flex;justify-content:space-between'><span>Robert J. Park · Briefing · 21 November 2026 · robertjpark.co.uk</span><span><span class='pageNumber'></span> / <span class='totalPages'></span></span></div>"
        await pg.pdf(path=SITE+'/assets/briefings/2026-11-the-2027-cbam-horizon-briefing.pdf',format='A4',print_background=True,display_header_footer=True,header_template='<div></div>',footer_template=foot,margin={'top':'16mm','bottom':'18mm','left':'16mm','right':'16mm'})
        await b.close()
asyncio.run(main())
