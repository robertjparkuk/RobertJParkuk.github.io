"""EU law and the Windsor Framework dashboard. Usage: python3 eu_build.py <repo_root>"""
import sys, os, re, html
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'build.py'), encoding='utf-8').read()
exec(src[:src.index('\nD = {}')])  # helpers and CSS only

AS_AT = '30 October 2026'
NIA = 'https://www.niassembly.gov.uk/assembly-business/brexit-and-beyond/eu-law-scrutiny-tracker/'

def cell(c):
    if isinstance(c, tuple):
        t, u = c
        return f'<a href="{esc(u)}" rel="noopener">{esc(t)}</a>'
    return esc(c)

def plain(c): return c[0] if isinstance(c, tuple) else c

def ltable(cols, rows, tag_col=None):
    th = ''.join(f'<th scope="col">{esc(c)}</th>' for c in cols)
    trs = []
    for r in rows:
        tds = []
        for i, c in enumerate(r):
            v = cell(c)
            if i == tag_col:
                t = plain(c); m = re.match(r'(Yes|Partly|No|Possibly|Likely)[:,]?\s*(.*)', t)
                word, rest = (m.group(1), m.group(2)) if m else (t, '')
                cls = {'Yes': 'k-yes', 'Partly': 'k-part', 'No': 'k-no'}.get(word, '')
                v = f'<span class="k-pill {cls}">{esc(word)}</span>' + (f'<br><span class="k-sub">{esc(rest[0].upper() + rest[1:])}</span>' if rest else '')
            tds.append(f'<td>{v}</td>')
        trs.append('<tr>' + ''.join(tds) + '</tr>')
    return f'<div class="k-tablebox"><table class="k-table"><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'

def slug(t): return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')

def timeline_svg(events, as_at):
    import datetime as _dt
    d0 = _dt.datetime.strptime(as_at, '%d %B %Y'); ds = [(_dt.datetime.strptime(d, '%d %b %Y'), j, t) for d, j, t in events]
    d1 = max(x[0] for x in ds); span = (d1 - d0).days + 20
    W, H, L, R = 1200, 150, 40, 40
    X = lambda d: L + (d - d0).days / span * (W - L - R)
    col = {'NI': '#A61C1C', 'GB': '#1A1A1A', 'UK': '#555555', 'UK–EU': '#14806C'}
    o = [f'<svg class="k-tl" viewBox="0 0 {W} {H}" role="img" aria-label="Timeline of {len(events)} dates from {as_at} to {d1.strftime("%B %Y")}">']
    o.append(f'<line x1="{L}" y1="78" x2="{W-R}" y2="78" stroke="#D9A0A0" stroke-width="2"/>')
    m = _dt.datetime(d0.year, d0.month, 1)
    while m <= d1:
        if m >= d0:
            x = X(m); o.append(f'<line x1="{x:.0f}" y1="72" x2="{x:.0f}" y2="84" stroke="#B9B4B0"/><text x="{x:.0f}" y="100" font-size="12" fill="#6B6B6B" text-anchor="middle">{m.strftime("%b")}{" " + m.strftime("%Y") if m.month == 1 else ""}</text>')
        m = _dt.datetime(m.year + (m.month == 12), 1 if m.month == 12 else m.month + 1, 1)
    for i, (d, j, t) in enumerate(ds):
        x = X(d); c = col.get(j, '#1A1A1A'); up = i % 2 == 0; y = 40 if up else 128
        o.append(f'<line x1="{x:.0f}" y1="78" x2="{x:.0f}" y2="{y + (8 if up else -14)}" stroke="{c}" stroke-width="1"/>')
        o.append(f'<circle cx="{x:.0f}" cy="78" r="6" fill="{c}"><title>{esc(d.strftime("%-d %b %Y"))}: {esc(t)}</title></circle>')
        o.append(f'<text x="{x:.0f}" y="{y}" font-size="13" font-weight="600" fill="{c}" text-anchor="middle">{d.strftime("%-d %b")}</text>')
    o.append(f'<text x="{L}" y="18" font-size="12" fill="#6B6B6B">Red: applies in NI · Green: UK–EU · Black: GB or UK-wide. Hover a dot for the event; the list below has them all.</text></svg>')
    return ''.join(o)

FILTER_JS = """<script>document.querySelectorAll('[data-filter]').forEach(function(i){var t=document.getElementById(i.getAttribute('data-filter'));var n=t.closest('section').querySelector('.k-count');i.addEventListener('input',function(){var q=i.value.toLowerCase();var k=0;t.querySelectorAll('tbody tr').forEach(function(r){var s=r.textContent.toLowerCase().indexOf(q)>-1;r.style.display=s?'':'none';if(s)k++});if(n)n.textContent=q?k+' of '+t.querySelectorAll('tbody tr').length+' rows':''})});</script>"""

def lcard(title, note, body, cols, rows, fname, srcnote):
    csvh = csv_href(cols, [[plain(c) for c in r] for r in rows])
    sid = slug(title); tid = 't-' + sid
    body = body.replace('<table class="k-table">', f'<table class="k-table" id="{tid}">', 1)
    filt = (f'<div class="k-filter"><label for="f-{sid}">Filter</label><input id="f-{sid}" type="search" data-filter="{tid}" placeholder="Type a word: packaging, timber, 2027…" autocomplete="off"><span class="k-count" aria-live="polite"></span></div>')
    return (f'<section class="k-card k-wide" id="{sid}" aria-label="{esc(title)}"><h3>{esc(title)}<a class="k-anchor" href="#{sid}" aria-label="Link to this section">#</a></h3><p class="k-note">{note}</p>{filt}{body}'
            f'<div class="k-actions"><a download="{fname}.csv" href="{csvh}">Download CSV</a></div><p class="k-src">{srcnote}</p></section>')

# 1. EU law that applies in NI -------------------------------------------------
APPLIES = [
 (('Deforestation Regulation (EU) 2023/1115 (EUDR)', NIA + 'reg20252650/'), 'Forest-risk goods: cattle, cocoa, coffee, palm oil, rubber, soya, wood', 'Food and drink processors; timber, furniture and paper; printers; anyone importing cattle, cocoa, coffee, palm oil, rubber, soya or wood', 'Yes', 'Large and medium firms 30 Dec 2026; micro and small 30 Jun 2027, except wood products already under the EU Timber Regulation (30 Dec 2026)', 'Amendments 2024/3234 and 2025/2650: no inquiry; no Brake'),
 (('Machinery Regulation (EU) 2023/1230', 'https://commonsbusiness.parliament.uk/Document/106373/Pdf'), 'Machinery', 'Machinery makers, importers and dealers; agricultural and construction equipment', 'Yes', 'Applies 20 Jan 2027, replacing Directive 2006/42', 'Amending act 2026/1744: inquiry report 27 Aug 2026'),
 (('Batteries Regulation (EU) 2023/1542', 'https://www.gov.uk/guidance/eu-batteries-regulations-in-northern-ireland'), 'Batteries', 'Battery and e-bike sellers; electronics; vehicle dealers; waste operators', 'Yes', 'Labels 18 Aug 2026; QR code, passport and removability 18 Feb 2027; due diligence 18 Aug 2027', 'Amendment 2025/1561: no inquiry'),
 (('Packaging and Packaging Waste Regulation (EU) 2025/40 (PPWR)', 'https://www.daera-ni.gov.uk/articles/packaging-and-packaging-waste'), 'Packaging', 'Every business that packs goods for the NI market; food and drink; retail', 'Partly: design, recyclability, labelling, substances and single-use restrictions. Not producer responsibility, deposit return, reuse or recycling targets', 'Applies 12 Aug 2026, phased to 2030 and 2040', 'No inquiry (30 Jan 2025); no Brake'),
 (('CLP revision (EU) 2024/2865', NIA + 'regulation-eu-20252439/'), 'Chemical classification and labelling', 'Chemical makers, formulators, distributors; cleaning products; paints; agri-supplies', 'Yes', 'New label format, advertising and online-sales rules postponed to 1 Jan 2028 by 2025/2439', 'The only Stormont Brake case so far: notified 20 Dec 2024, not applied 20 Jan 2025'),
 (('Construction Products Regulation (EU) 2024/3110', NIA + 'regulation-eu-20243110/'), 'Construction products', 'Builders merchants, manufacturers of construction products, contractors', 'Yes', 'Applies from 8 Jan 2026, alongside 305/2011 until 2040', 'Inquiry report 23 Jan 2025; no Brake'),
 (('Waste Shipments Regulation (EU) 2024/1157', NIA + 'regulation-eu-20241157/'), 'Waste', 'Waste and recycling operators; exporters of plastic, metal and paper waste', 'Yes', 'Most rules from 21 May 2026; plastic waste exports to non-OECD countries banned from 21 Nov 2026', 'Inquiry report 6 Jun 2024'),
 (('F-gas Regulation (EU) 2024/573', NIA + 'regulation-eu-2024573/'), 'F-gases', 'Refrigeration, air-conditioning and heat-pump installers; cold chain; supermarkets', 'Yes', 'In force since 11 Mar 2024; product bans and quota cuts phased in to 2050', 'Notified late; no inquiry decision; no Brake'),
 (('Ecodesign for Sustainable Products Regulation (EU) 2024/1781', NIA + 'regulation-eu-20241781/'), 'Ecodesign', 'Makers and importers of energy-related and consumer products; textiles', 'Yes', 'In force 18 Jul 2024; product rules follow by delegated act', 'No inquiry (11 Jul 2024)'),
 (('General Product Safety Regulation (EU) 2023/988', 'https://www.gov.uk/government/publications/eu-regulation-2023988-on-general-product-safety/eu-regulation-on-general-product-safety-2023988'), 'Consumer product safety', 'Every consumer-product seller and online marketplace supplying NI', 'Yes', 'Since 13 Dec 2024', '—'),
 (('Product Liability Directive (EU) 2024/2853', NIA + 'directive-eu-20242853/'), 'Product liability', 'Manufacturers, importers and online sellers; software and AI products', 'Yes', 'Transposition due 9 Dec 2026', 'Inquiry report 19 Dec 2024'),
 (('Toy Safety Regulation (EU) 2025/2509', NIA + 'reg20252509/'), 'Toys', 'Toy makers, importers and retailers', 'Yes', 'Applies from 1 Aug 2030', 'Inquiry report 22 Jan 2026; Brake window closed 29 Jan 2026 with no notification'),
 (('Detergents and Surfactants Regulation (EU) 2026/405', NIA + 'reg2026405'), 'Chemical products', 'Cleaning-product makers and distributors', 'Yes', 'Adopted 11 Feb 2026', 'Inquiry report 26 Mar 2026'),
 (('Vehicle circularity and end-of-life vehicles (EU) 2026/1738', NIA + 'reg20261738/'), 'Circular economy', 'Vehicle makers, dealers, dismantlers and parts recyclers', 'Yes', 'Adopted 8 Jul 2026', 'Inquiry report 27 Aug 2026'),
 (('Farmers in the food supply chain (EU) 2026/1739', NIA + 'reg20261739/'), 'Agri-food', 'Farmers, processors and retailers in the food supply chain', 'Yes', 'Adopted 8 Jul 2026', 'Inquiry report 27 Aug 2026'),
 (('Union Customs Code recast (EU) 2026/2108', NIA + 'reg20262108/'), 'Customs', 'Every business moving goods into NI from GB or outside the EU; parcel carriers', 'Yes', 'Adopted 16 Sep 2026', 'Inquiry report 22 Oct 2026; Brake window open to 5 Nov 2026'),
 (('REACH (EC) 1907/2006', 'https://www.hse.gov.uk/reach/northern-ireland.htm'), 'Chemicals', 'Chemical makers, importers and downstream users', 'Yes: EU REACH in NI, UK REACH in GB', 'Ongoing', '—'),
 (('EU Emissions Trading System, Directive 2003/87/EC', 'https://www.daera-ni.gov.uk/articles/emissions-trading-schemes'), 'Carbon pricing', 'Electricity generators in NI', 'Partly: NI electricity generators only. Other NI sites are in the UK ETS', 'Since 1 Jan 2021', '—'),
 (('Single Electricity Market rules (Windsor Framework Article 9 and Annex 4)', 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:12020W/TXT'), 'Wholesale electricity', 'Generators, suppliers and large energy users on the all-island market', 'Partly: the all-island wholesale market', 'Ongoing', '—'),
]
NOT_NI = [
 (('EU Carbon Border Adjustment Mechanism (EU) 2023/956', 'https://researchbriefings.files.parliament.uk/documents/CBP-9935/CBP-9935.pdf'), 'No', 'Not applied in NI. The UK CBAM covers NI from 1 Jan 2027'),
 ('Corporate Sustainability Reporting Directive (EU) 2022/2464', 'No', 'Not in the Windsor Framework annexes. NI firms are caught only through EU subsidiaries or EU turnover'),
 ('Corporate Sustainability Due Diligence Directive (EU) 2024/1760', 'No', 'Not in the annexes. Reaches NI firms through EU customers'),
 ('Nature Restoration Regulation (EU) 2024/1991', 'No', 'Not in the annexes'),
 (('Water Framework and Habitats Directives', 'https://nihrc.org/publication/detail/nihrc-briefing-on-the-environment-human-rights-and-the-windsor-framework-independent-research-report'), 'No', 'Not in the annexes. NI keeps its own regulations; the NI Human Rights Commission argues Article 2 protects some pre-2021 standards'),
]

# 2. Stormont Brake and new acts -------------------------------------------------
BRAKE = [
 ('16 May 2024', ('Joint Committee Decision 2/2024 adds the organic pet food rules (EU) 2023/2419', 'https://www.gov.uk/government/publications/decision-no-22024-of-joint-committee-established-by-the-agreement-on-the-withdrawal-of-the-uk-from-the-eu-adding-a-newly-adopted-union-act-to-annex'), 'Article 13(4) addition'),
 ('20 Dec 2024', ('Stormont Brake notified on the CLP revision (EU) 2024/2865 by 35 MLAs', 'https://www.niassembly.gov.uk/globalassets/documents/speaker/correspondence/sp279_24-lt-to-sos-written-notification-of-stormont-brake.pdf'), 'First and only use'),
 ('20 Jan 2025', ('Secretary of State declines to apply the Brake: "significant impact" test not met', 'https://www.gov.uk/government/publications/letter-from-the-secretary-of-state-for-northern-ireland-regarding-stormont-brake-decision'), 'Act applies in NI'),
 ('29 Apr 2025', ('Decisions 1–3/2025 add craft geographical indications, parts of the Critical Raw Materials Act, and Ukraine and Moldova trade measures', 'https://assets.publishing.service.gov.uk/media/68920827486754ec2887847a/TS_33.2025_Joint_Committee_Decisions_Withdrawal_Europe.pdf'), 'Article 13(4) additions. The Assembly did not pass a motion on the craft GI act; the UK went ahead'),
 ('4 Sep 2025', ('Lord Murphy\'s independent review of the Windsor Framework published', 'https://assets.publishing.service.gov.uk/media/68b59ad53f3e5483efdba87d/Independent_Review_of_the_Windsor_Framework_by_the_Rt_Hon_Lord_Murphy.pdf'), 'Government response 16 Dec 2025'),
 ('2 Feb 2026', ('Decision 1/2026 adds road-going non-road mobile machinery (EU) 2025/14', 'https://assets.publishing.service.gov.uk/media/69a86867487f0b64a680d4df/TS_10.2026_Decision_No_1.2026_Joint_Committee_Withdrawal_Agreement.pdf'), 'Article 13(4) addition'),
 ('18 Sep 2026', ('Draft decision to add the common chemicals data platform (EU) 2025/2455 sent to the Council', 'https://data.consilium.europa.eu/doc/document/ST-13391-2026-ADD-1/en/pdf'), 'Pending'),
 ('22 Oct 2026', ('Assembly scrutiny committee reports on the Union Customs Code recast, its 15th inquiry', 'https://www.niassembly.gov.uk/assembly-business/brexit-and-beyond/eu-law-scrutiny-tracker/reg20262108/'), 'Brake window open to 5 Nov 2026'),
]

# 3. GB knock-on effects -----------------------------------------------------------
GB = [
 (('Product safety (GPSR)', 'https://www.gov.uk/government/publications/eu-regulation-2023988-on-general-product-safety/eu-regulation-on-general-product-safety-2023988'), 'Selling into NI', 'GB sellers into NI need a responsible person in NI or the EU on the product', 'Since 13 Dec 2024'),
 (('Deforestation (EUDR)', 'https://www.niassembly.gov.uk/assembly-business/brexit-beyond-newsletters/issue-220--29-june-2026/'), 'Selling into NI', 'GB firms moving cattle, soya, wood and other goods to NI must meet EUDR. Defra proposes a GB regime aligned with it', 'NI from 30 Dec 2026; GB proposal 23 Jun 2026'),
 (('Packaging (PPWR)', 'https://www.niassembly.gov.uk/assembly-business/brexit-beyond-newsletters/issue-221--01-september-2026/'), 'Selling into NI', 'Packaging sold in NI must meet EU design and labelling rules; GB has not decided whether to follow', 'NI from 12 Aug 2026'),
 (('UK Internal Market Scheme', 'https://www.economy-ni.gov.uk/articles/uk-internal-market-scheme'), 'Selling into NI', 'Authorised GB traders can declare goods "not at risk" of entering the EU and move them to NI with simplified information instead of a full customs declaration. Whether a shipment is at risk decides how much of this page applies to it', 'Since 30 Sep 2023'),
 (('"Not for EU" labels', 'https://www.gov.wales/written-statement-marking-retail-goods-regulations-2025'), 'GB follows the EU', 'Labels on food sent to NI shops. A reserve power (SI 2025/790) could extend them GB-wide product by product', 'Power made 1 Jul 2025'),
 (('Plant health import rules', 'https://www.niassembly.gov.uk/assembly-business/brexit-beyond-newsletters/issue-222--07-september-2026/'), 'GB follows the EU', 'GB rules on tomatoes, peppers and ginger aligned with the EU so goods can still go to NI (SI 2026/458)', 'Debated 2 Sep 2026'),
 (('Chemical labelling (CLP)', 'https://consultations.hse.gov.uk/hse/chemicals-legislative-reform-proposals/results/responsereport-chemicalslegislativereformproposals.pdf'), 'GB follows the EU', 'HSE to change GB CLP so one label works UK-wide, in effect following EU changes', 'Response Feb 2026; law to follow'),
 (('Batteries', 'https://www.niassembly.gov.uk/assembly-business/brexit-beyond-newsletters/issue-224--21-september-2026/'), 'GB follows the EU', 'EU rules in NI; UK to consult on an aligned UK-wide regime', 'NI enforcement approved 15 Sep 2026'),
 (('Agri-food (SPS) agreement', 'https://www.niassembly.gov.uk/assembly-business/brexit-beyond-newsletters/issue-216--01-june-2026/'), 'GB follows the EU', 'GB would follow EU food and plant-health rules as they change, removing most GB-to-NI checks', 'Target mid-2027; not yet agreed'),
 (('Emissions trading link', 'https://www.consilium.europa.eu/en/press/press-releases/2025/11/13/eu-uk-relations-council-greenlights-negotiations-on-agri-food-deal-and-linking-emissions-trading-systems/'), 'GB follows the EU', 'Linking UK and EU ETS, with each side exempt from the other\'s CBAM. A deal was reported in October but not confirmed', 'UK–EU summit 20 Nov 2026'),
 (('REACH', 'https://www.hse.gov.uk/reach/northern-ireland.htm'), 'Two regimes', 'EU REACH applies in NI, UK REACH in GB. A GB firm cannot hold an EU REACH registration itself: it needs an EU- or NI-based registrant or only representative', 'Ongoing'),
 (('F-gas', 'https://www.daera-ni.gov.uk/articles/fluorinated-greenhouse-gases'), 'Two regimes', 'GB and NI quotas diverge; GB suppliers to NI must meet EU bans', 'Gap widens 1 Jan 2027'),
 (('Machinery and tumble dryers', 'https://commonsbusiness.parliament.uk/Document/106373/Pdf'), 'Two regimes', 'GB continues to recognise CE marking for machinery, so EU-compliant machinery can still be sold in GB. New GB ecodesign rules ban vented and convector tumble dryers from January 2027', 'NI applies the EU Machinery Regulation from 20 Jan 2027'),
 (('Electricity VAT', 'https://www.gov.uk/government/publications/temporary-zero-rate-of-vat-for-domestic-electricity-in-great-britain/temporary-zero-rate-of-vat-in-great-britain-for-domestic-electricity'), 'Two regimes', 'A temporary zero rate of VAT on GB household electricity does not apply in NI, where EU VAT rules on goods apply. The UK is funding NI households instead this winter', '1 Oct 2026 to 31 Mar 2027'),
 (('Parcel and low-value customs duty', 'https://www.niassembly.gov.uk/assembly-business/brexit-beyond-newsletters/issue-221--01-september-2026/'), 'Two regimes', 'A new EU customs duty on low-value parcels applies in NI, but GB-to-NI goods that are not at risk of entering the EU are exempt', 'From 1 Jul 2026'),
]

# 4. Open consultations --------------------------------------------------------------
HYS = 'https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/'
CONS = [
 ('3 Nov 2026', ('EU ETS and Market Stability Reserve review', HYS + '14549_en'), 'European Commission', 'Partly', 'NI power generators are in the EU ETS; other NI sites are in the UK ETS'),
 ('4 Nov 2026', ('VAT and the circular economy', HYS + '18833_en'), 'European Commission', 'Likely', 'EU VAT rules on goods apply in NI, but not on services such as repair'),
 ('6 Nov 2026', ('Methane reporting templates, energy sector', HYS + '14450_en'), 'European Commission', 'No', 'All-island gas supply chain'),
 ('10 Nov 2026', ('Gas transmission capacity network code', HYS + '15032_en'), 'European Commission', 'No', 'Gas flows into and across the island'),
 ('11 Nov 2026', ('Animal disease contingency plans', HYS + '13638_en'), 'European Commission', 'Yes', 'EU Animal Health Law applies in NI'),
 ('13 Nov 2026', ('Nitrates: RENURE for liquid digestates', HYS + '19475-Nitrates-extending-the-rules-on-recovered-nitrogen-from-manure_en'), 'European Commission', 'No', 'Manure, digestate, Lough Neagh and the NI biomethane strategy'),
 ('16 Nov 2026', ('Battery passport access rights', HYS + '16473_en'), 'European Commission', 'Yes', 'Batteries Regulation applies in NI'),
 ('19 Nov 2026', ('Electricity network tariff structure review, phase 1', 'https://consult.cru.ie/en/consultation/electricity-network-tariff-structure-review-phase-1-consultation-objectives-principles-scope-and'), 'Ireland: CRU', 'No', 'Feeds the all-island electricity market'),
 ('20 Nov 2026', ('EirGrid draft Transmission Development Plan 2026–2035', 'https://consult.cru.ie/en/consultation/draft-transmission-development-plan-2026-2035'), 'Ireland: CRU', 'No', 'Grid on the Irish side of the all-island system'),
 ('14 Dec 2026', ('Data centres: minimum performance standards', HYS + '19293-Data-centres-in-Europe-minimum-performance-standards_en'), 'European Commission', 'No', "Ireland's data-centre load on the shared grid"),
 ('13 Jan 2027', ('Plastic packaging with bio-based feedstock', HYS + '19498-Plastic-packaging-containing-biobased-feedstock-EU-rules/public-consultation_en'), 'European Commission', 'Likely', 'Packaging product rules apply in NI'),
]

# 5. Coming up -------------------------------------------------------------------------
NEXT = [  # date, jurisdiction, what
 ('5 Nov 2026', 'NI', 'Stormont Brake deadline on the Union Customs Code recast (EU) 2026/2108'),
 ('20 Nov 2026', 'UK–EU', 'Summit: agri-food (SPS) agreement and emissions trading link expected on the table'),
 ('21 Nov 2026', 'NI', 'Plastic waste exports to non-OECD countries banned (Waste Shipments Regulation)'),
 ('9 Dec 2026', 'NI', 'Product Liability Directive transposition date'),
 ('30 Dec 2026', 'NI', 'EU deforestation rules apply to large and medium firms, and to wood products from all firms'),
 ('1 Jan 2027', 'UK', 'UK CBAM starts, covering the whole UK including NI'),
 ('20 Jan 2027', 'NI', 'EU Machinery Regulation applies'),
 ('18 Feb 2027', 'NI', 'Battery passport, QR code and removability rules'),
 ('31 Mar 2027', 'GB', 'Temporary zero rate of VAT on household electricity ends'),
 ('30 Jun 2027', 'NI', 'EU deforestation rules apply to micro and small firms'),
 ('1 Jan 2028', 'NI', 'New CLP label format, advertising and online-sales rules apply'),
]

CHANGES = [  # newest first: date, what changed
 ('30 Oct 2026', 'Weekly check. Removed eight consultations that closed between 26 and 30 October (six European Commission, two Irish Government). Countdown tiles and the "as at" date updated. No other changes published this week.'),
 ('25 Oct 2026', 'Published. Same evening: nine corrections after an independent fact-check (Customs Code Brake window to 5 Nov; plastic-waste export ban 21 Nov; EUDR wood-product date; VAT cut is temporary; REACH, machinery and single electricity market rows reworded; two weak sources replaced; one unverified consultation removed). Added: who each law affects, the kind of each GB effect, the UK Internal Market Scheme, parcel duty, the Murphy review, a glossary, filters and this log.'),
]
GLOSSARY = [
 ('Windsor Framework', 'The 2023 UK–EU agreement that replaced the Northern Ireland Protocol. Its annexes list the EU laws on goods, customs, VAT on goods, animal and plant health, state aid and the electricity market that apply in NI.'),
 ('Dynamic alignment (Article 13(3))', 'When the EU amends or replaces a listed law, the new version applies in NI automatically, unless the Stormont Brake is used.'),
 ('New EU acts (Article 13(4))', 'An EU law that is new, not a replacement, applies in NI only if the UK and EU add it by a Joint Committee decision, normally after the Assembly passes an applicability motion.'),
 ('Stormont Brake', 'Thirty MLAs from at least two parties can notify the UK Government that an amended or replacement EU law should not apply in NI. It must be a last resort, and the change must be significantly different and affect everyday life. The Secretary of State decides. Used once, on chemical labelling; not applied.'),
 ('Democratic Scrutiny Committee', 'The Assembly committee that examines each amending or replacement EU act and can hold an inquiry. Its reports and the Brake deadlines are on the Assembly\'s EU law scrutiny tracker.'),
 ('UK Internal Market Scheme and "not at risk" goods', 'Authorised traders moving goods from GB to NI that will not enter the EU use simplified information instead of a customs declaration. Whether goods are "at risk" decides how much EU customs law bites on a shipment.'),
 ('NI Retail Movement Scheme', 'The simplified route for prepacked food and drink moving from GB to NI shops and caterers. Goods carry "Not for EU" labels.'),
]

EXTRA = """
.k-pill.k-yes{border-color:var(--color-ok);color:var(--color-ok)} .k-pill.k-part{border-color:#B7791F;color:#8A5A12}
.k-pill.k-no{border-color:var(--color-fg-muted)} .k-tablebox{max-height:none;overflow-x:auto} .k-table td{vertical-align:top}
.k-time{list-style:none;margin:0;padding:0} .k-time li{display:grid;grid-template-columns:7.5em 1fr;gap:12px;padding:8px 0;border-top:1px solid var(--color-border-line)}
.k-time li:first-child{border-top:0} .k-time b{color:var(--color-accent,#A61C1C)}
.k-filter{display:flex;gap:8px;align-items:center;margin:0 0 10px;font-size:14px} .k-filter input{flex:1;max-width:360px;padding:6px 10px;border:1px solid var(--color-border-line);border-radius:6px;font:inherit;background:var(--color-bg,#fff);color:inherit}
.k-anchor{font-size:12px;color:var(--color-fg-muted);text-decoration:none;margin-left:8px} .k-card h3:hover .k-anchor{color:var(--color-accent,#A61C1C)}
.k-tl{width:100%;height:auto;display:block;margin:6px 0 2px} .k-juris{display:inline-block;min-width:3.4em;font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--color-fg-muted);margin-right:8px}
.k-glos dt{font-weight:600;margin-top:10px} .k-glos dd{margin:2px 0 0}
.k-log li{margin:0 0 6px}
.k-cta{background:var(--color-accent,#A61C1C);color:#fff;border-radius:8px;padding:18px 22px} .k-cta a{color:#fff;font-weight:600} .k-cta p{margin:0 0 6px}
@media print{.site-top nav,.k-filter,.k-actions,.k-anchor,.k-cta{display:none!important}.k-card{break-inside:avoid;border:1px solid #ccc}.k-tablebox{overflow:visible}body{font-size:11px}}
"""

def page_eu(tiles, cards):
    url = 'https://robertjpark.co.uk/tools/dashboards/eu-law-windsor-framework.html'
    title = 'EU law and the Windsor Framework dashboard'
    desc = 'Which EU laws apply in Northern Ireland under the Windsor Framework, Stormont Brake cases, effects on Great Britain, and open Irish and European Commission consultations.'
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
<style>{K_CSS}{EXTRA_CSS}{EXTRA}</style>
</head>
<body>
<header class="site-top">
  <a class="brand" href="/" aria-label="Robert J. Park home"><img src="/assets/tools-mark.svg" alt="" width="30" height="30">Robert J. <b>Park</b> · Dashboards</a>
  <nav aria-label="Main"><a href="/">Home</a><a href="/services/">Services</a><a href="/tools/">Tools</a><a href="/dashboards/">Dashboards</a><a href="/blog/">Blog</a><a href="/contact/">Contact</a></nav>
</header>
<main id="dash-root">
<div class="k-wrap">
<header class="k-head"><h1>EU law and the Windsor Framework</h1>
<p>Which EU laws apply in Northern Ireland, where the Stormont Brake has been tried, how NI rules reach businesses in Great Britain, and which Irish and European Commission consultations are open. As at {AS_AT}.</p></header>
<div class="k-tiles">{''.join(tiles)}</div>
<h2 class="k-h2">The tracker</h2>
<div class="k-grid">{''.join(cards)}</div>
<h2 class="k-h2">What changed</h2>
<section class="k-card" id="what-changed"><ul class="k-log">{''.join(f'<li><b>{esc(d)}:</b> {esc(t)}</li>' for d, t in CHANGES)}</ul><p class="k-note">Updated every Friday by 5pm. Each update is logged here.</p></section>
<h2 class="k-h2">How to read this page</h2>
<section class="k-card" id="glossary"><dl class="k-glos">{''.join(f'<dt>{esc(a)}</dt><dd>{esc(b)}</dd>' for a, b in GLOSSARY)}</dl><p class="k-src">Sources: <a href="https://www.niassembly.gov.uk/assembly-business/committees/2022-2027/windsor-framework-democratic-scrutiny-committee/useful-resources/the-stormont-brake/" rel="noopener">The Stormont Brake (NI Assembly)</a>; <a href="https://www.economy-ni.gov.uk/articles/uk-internal-market-scheme" rel="noopener">UK Internal Market Scheme (Department for the Economy)</a>; <a href="https://www.gov.uk/government/publications/retail-movement-scheme-how-the-scheme-will-work/retail-movement-scheme-how-the-scheme-will-work" rel="noopener">Retail Movement Scheme (GOV.UK)</a>.</p></section>
<section class="k-cta"><p><strong>Caught between the two rulebooks?</strong></p><p>I help Northern Ireland businesses work out which rules apply to what they make and where it goes, respond to consultations, and build a compliance register from pages like this one. <a href="/contact/">Get in touch</a> or see <a href="/services/">what I do</a>.</p></section>
<h2 class="k-h2">About this page</h2>
<section class="k-card"><p class="k-note">A dated snapshot, checked on 30 October 2026 against the NI Assembly's EU law scrutiny tracker and Brexit and Beyond newsletters, GOV.UK, DAERA, the Council of the EU, the European Commission and gov.ie. "Not in the annexes" rows are my reading of the Windsor Framework annexes, not legal advice. Every link is to an official source except where a row says "as reported by"; the NI Assembly's Brexit and Beyond newsletter is used where a GOV.UK page could not be opened. Commission close dates are usually midnight Brussels time; check the consultation page before you rely on one. Nothing on this page is fetched or sent, and every table can be downloaded as CSV.</p></section>
<p class="k-foot">More dashboards: <a href="/dashboards/">all dashboards</a>. Related: <a href="/tools/dashboards/cbam-exposure-tracker.html">CBAM Exposure Tracker</a>.</p>
</div>
</main>
<footer class="site-foot">Robert J. Park · Environment · Carbon · Public Affairs · Northern Ireland. Checked on {AS_AT}. <a href="/contact/">Contact</a> · <a href="/privacy/">Privacy</a></footer>
{FILTER_JS}
</body>
</html>
'''

import datetime as _dt
_asat = _dt.datetime.strptime(AS_AT, '%d %B %Y')
_days = lambda d: (_dt.datetime.strptime(d, '%d %b %Y') - _asat).days
_open_ni = sum(1 for c in CONS if plain(c[3]).split(':')[0] in ('Yes', 'Partly', 'Likely'))
tiles = [
 tile('Days to the deforestation rules', str(_days('30 Dec 2026')), '30 Dec 2026: large and medium firms, and all wood products', 'k-bad'),
 tile('Days to the UK–EU summit', str(_days('20 Nov 2026')), '20 Nov 2026: agri-food deal and ETS link expected'),
 tile('Days to the Brake deadline', str(_days('5 Nov 2026')), '5 Nov 2026: Union Customs Code recast. One Brake used so far, not applied'),
 tile('Consultations you can act on', f'{_open_ni} of {len(CONS)}', 'Open now, where the EU law applies in NI'),
]
c1 = ['EU law', 'Topic', 'Who it affects', 'Applies in NI?', 'Key dates for NI', 'Assembly scrutiny or Brake']
c2 = ['EU law', 'Applies in NI?', 'Why']
c3 = ['Date', 'Event', 'Outcome']
c4 = ['Issue', 'Kind of effect', 'What it means in GB', 'Key date']
c5 = ['Closes', 'Consultation', 'Body', 'Windsor Framework scope', 'Why it matters for NI']
time_html = timeline_svg(NEXT, AS_AT) + '<ul class="k-time">' + ''.join(f'<li><b>{esc(d)}</b><span><span class="k-juris">{esc(j)}</span>{esc(t)}</span></li>' for d, j, t in NEXT) + '</ul>'
cards = [
 f'<section class="k-card k-wide" id="coming-up" aria-label="Coming up"><h3>Coming up<a class="k-anchor" href="#coming-up" aria-label="Link to this section">#</a></h3><p class="k-note">Dates that change what applies, and where. NI means an EU rule reaching Northern Ireland under the Windsor Framework.</p>{time_html}<p class="k-src">Sources: the tables below.</p></section>',
 lcard('EU law that applies in Northern Ireland', 'Selected laws for environment, carbon, products and goods. Each name links to the Assembly tracker or the official guidance.', ltable(c1, APPLIES, tag_col=3), c1, APPLIES, 'eu-law-applying-in-ni', 'Sources: NI Assembly EU law scrutiny tracker; GOV.UK; DAERA; HSE.'),
 lcard('Often assumed, but not applying in NI', 'These are not in the Windsor Framework annexes, though NI firms can still be caught through EU customers.', ltable(c2, NOT_NI, tag_col=1), c2, NOT_NI, 'eu-law-not-applying-in-ni', 'Sources: House of Commons Library; NI Human Rights Commission; Windsor Framework annexes.'),
 lcard('Stormont Brake and new EU acts', 'Every Brake case, every Joint Committee decision adding a new EU act under Article 13(4), and the main oversight events, oldest first.', ltable(c3, BRAKE), c3, BRAKE, 'stormont-brake-and-new-acts', 'Sources: NI Assembly; GOV.UK; Council of the EU.'),
 lcard('How NI rules reach Great Britain', 'Three kinds of effect: GB firms must meet EU rules to sell into NI; GB rules are moved towards the EU to keep goods flowing; or GB and NI run two regimes and firms carry both.', ltable(c4, GB, tag_col=1), c4, GB, 'gb-effects-of-windsor-framework', 'Sources: NI Assembly Brexit and Beyond; GOV.UK; HSE; Welsh Government; Council of the EU; NI Business Info.'),
 lcard('Open consultations: European Commission and Ireland', 'Open on 30 October 2026, soonest first. "Yes" means the EU law in question applies in NI, so NI businesses have a direct stake.', ltable(c5, CONS, tag_col=3), c5, CONS, 'open-consultations-eu-ireland', 'Sources: European Commission Have your say; gov.ie; CRU; Uisce Éireann. The NI Assembly scrutiny committee had no open calls for evidence.'),
]
out = page_eu(tiles, cards)
open(os.path.join(ROOT, 'tools/dashboards/eu-law-windsor-framework.html'), 'w', encoding='utf-8').write(out)
print(len(out))
