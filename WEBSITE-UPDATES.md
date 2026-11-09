# Website updates

This file logs every change to the Robert J. Park website. It lives in the root of the repo and is kept off the public site by `_config.yml`. Add a new entry at the top each time something goes live.

- **Repo:** https://github.com/robertjparkuk/RobertJParkuk.github.io (Jekyll on GitHub Pages, branch `main`, folder `/`)
- **Live address:** https://robertjpark.co.uk (robertjparkuk.github.io redirects)
- **Other guides:** `README.md` covers set-up and the domain; `HOW-TO-POST.md` covers blog posts

## Versioning

Versions take the form `v0.MINOR.PATCH` until the custom domain is live, then `v1.0.0`.

- **MINOR:** a new page, tool or section.
- **PATCH:** fixes, fact updates and wording changes.

Each release gets a branch named after it (e.g. `v0.2.0-tools`), merged into `main` once checked.

## How a page is built here

- **Pages and posts** (`.md` files with front matter at the top) use the site layout, with header, navigation and footer.
- **Tools** (`tools/*.html`, `puzzles/*.html`) are self-contained HTML files with no front matter, so Jekyll copies them as they are. Each one carries its own branding, and its brand line links back to the home page.
- **`_snippets/`** holds copy-and-paste code for links and embeds. Jekyll doesn't publish folders whose names start with an underscore.

---

## Changelog

### v0.27.2 — 9 November 2026: personal number out of the public repo

- `.github/workflows/pr-check.yml`: the personal mobile number was written out in full in the PR check's patterns, so it was readable in the public repository. The check now stores only a salted SHA-256 hash and compares every UK mobile-shaped number in the built site and the PDFs against it. (The number remains in older commits' history; only rewriting history would remove it.)
- `poppins-0.1.0-py3-none-any.whl`: a stray third-party Python package file at the site root, served publicly, removed.

### v0.27.1 — 9 November 2026: ESG Regime Tracker UK CBAM card corrected

- **Removed** the card "UK CBAM: NI outward-processing carve-out". It merged two separate rules into one exemption ("goods that leave NI for processing in the EU and return within three years in the same state are exempt"). It also wrongly said no equivalent applies elsewhere in the UK, and it cited a non-official source (an accountancy blog).
- **Added** three Northern Ireland cards, each dated "As at 9 November 2026" and citing official sources only:
  - **UK CBAM in NI: returned goods relief for Union goods.** Goods that leave NI for the EU as Union goods and come back unaltered within three years carry no UK CBAM (Finance Act 2026, s.147(2)(d)). These goods do not count towards the £50,000 threshold. GB gets the same result through ordinary returned goods relief (s.147(2)(b) and (c)).
  - **UK CBAM in NI: goods processed in the EU and returned.** These goods are not exempt. They are handled like outward processing. CBAM is due if the returning good is a CBAM good, but not on emissions from UK-origin inputs (s.147(3)). A UK carbon price already paid can reduce the liability. Only the value added abroad counts towards the threshold.
  - **UK CBAM in NI: scope, origin and carbon price relief.** CBAM applies across the whole UK, including NI. Goods of UK origin, including goods made in NI, are out of scope. EU goods entering NI count as imports unless Treasury regulations exclude them (s.144(5)(a)), and some goods moving from NI to GB have a separate import point (s.144(6)). Carbon price relief is available for a qualifying carbon price paid elsewhere. HMRC says no jurisdiction is currently exempt.
- The tracker now lists 33 regimes, up from 31. The filters, the count and search are unaffected because cards have no ids and the count is worked out from the data.

Sources:
- HM Treasury and HMRC, Carbon Border Adjustment Mechanism (CBAM): policy summary, GOV.UK (updated 2 November 2026): https://www.gov.uk/government/publications/carbon-border-adjustment-mechanism-cbam-policy-summary/carbon-border-adjustment-mechanism-cbam-policy-summary
- HMRC, Imported CBAM goods that may not contribute towards the registration threshold, GOV.UK (updated 25 September 2026): https://www.gov.uk/guidance/imported-carbon-border-adjustment-cbam-goods-that-may-not-contribute-towards-the-registration-threshold
- Finance Act 2026 (c. 11), Part 5, ss.144, 147 and 150: https://www.legislation.gov.uk/ukpga/2026/11/contents
- The Carbon Border Adjustment Mechanism (Calculation of CBAM Rate and Determination of Carbon Price Relief) Regulations 2026 (SI 2026/809): https://www.legislation.gov.uk/uksi/2026/809

### v0.27.1 — 9 November 2026: correction to the DfI response page

- `_posts/2026-11-06-response-planning-classes-and-thresholds.md`: ask 17 said EU Connecting Europe money funds links to France and not Great Britain. Corrected to the narrower, accurate point (the €530m works grant went to the Celtic Interconnector; links to GB can qualify as projects of mutual interest, e.g. MaresConnect, listed Dec 2025, but nothing comparable has been funded) and added a dated correction note linking the maritime piece. The submitted PDF is unchanged, as a record of what was sent.

### v0.27.0 — 9 November 2026: Robert's decisions of 9 November

*From the decisions pane signed off by Robert at 19:17 on 9 November.*

- Policy series: "Fertiliser: a small tax, a big bill and a lough" (was 2 December) and "The Act that outran its plan" (was 25 January 2027) published now, re-dated to 9 November, with notes that Fertiliser is updated in December with the agriculture dashboard and the Act piece in January 2027; the Act piece gains a short "Where I stand". `policy-series.md` counts updated. "The Irish Sea carbon bill" (25 Nov) and "Carbon borders as industrial policy" (30 Nov) stay scheduled for after the 20 November UK–EU summit.
- Offer: the £620 **Two-Regime Readiness Review** replaces the £495 UK CBAM Exposure Check as the entry product (questionnaire, 90-minute call, 6–8 page review with a 12-month plan, 30-minute follow-up, ten working days; fee credited against the next service within three months). Changed in `cbam-desk.md`, `services.md`, the home hero button, the Metals issue page, the CBAM Exposure Tracker and the UK CBAM Countdown.

### Focus on Construction & Building — 9 November 2026

*Signed off by Robert and published on 9 November, eleven days early (was due Friday 20 November); dated 9 November throughout (page, PDF file name, header and footer, post, dashboard). Built from the signed-off draft in "Focus on series: five final drafts"; wording kept except where facts had changed.*

**Added**
- `blog/focus-on-construction-building-november-2026/index.html`: the issue as a web page, with three charts, the PDF reader, the dashboard and Land Repair Helix links. Self-contained, self-hosted fonts, no outside scripts; canonical and Open Graph on robertjpark.co.uk; BlogPosting JSON-LD dated 2026-11-09.
- `assets/focus-on-construction/2026-11/`: charts (`01-output.png` change in output by type of work, Q1 2026; `02-sectors.png` sector emissions, base year and 2024; `03-deadlines.png` five dates to January 2028) and the 6-page PDF `Focus-on-Construction-and-Building-9-November-2026.pdf`.
- `_posts/2026-11-09-focus-on-construction-building-november-2026.md`: summary post (18:50, 9 November).
- `tools/dashboards/ni-construction-building.html` (from branch `focus-on-dashboards`, updated as below), and its entry in `dashboards.md`.

**Changed from the signed-off draft (checked 9 November)**
- Blocker fixed, UK CBAM: the draft said supplies from the EU were outside the levy and the deadline table said "importers from outside the UK and EU". HMRC's policy summary (updated 2 November 2026) says the charge applies to goods originating outside the UK and "there are currently no jurisdictions exempt"; relief covers only a carbon price actually paid. Text, deadline table, chart and dashboard now say any non-UK origin, EU included (Republic of Ireland cement and steel too). GB-stockholder point added (their import, not yours). Threshold worded as £50,000 "in any 12 months", matching HMRC.
- UK CBAM default values: one sentence added from Budget 2026 (HC 726, para 6.217): global defaults in 2027 and 2028, country-specific from 2029.
- EUDR: the draft said most micro and small businesses have until 30 June 2027. For timber that is wrong: the European Commission and GOV.UK say micro and small operators placing products covered by the old EU Timber Regulation must comply from 30 December 2026; 30 June 2027 is for other commodities. Paragraph corrected, 30 June 2027 row removed from the deadline table, 30 December row now says all business sizes; dashboard rules table and CSV corrected.
- "Two rules arrive within six weeks" became "within eight weeks" (publication moved from 20 November to 9 November).
- Care note: "Q3 2026 figures are due in December" corrected to 14 January 2027 (GOV.UK release calendar, confirmed).
- Care notes added: housing supply (new dwelling starts 1,502 in April to June 2026, 746 fewer than a year earlier; completions 1,571; DoF/NISRA, 19 August 2026; July to September due 18 November) and a CBAM/EUDR checked-on and not-advice line, with the Republic of Ireland movement point.
- Sources: NI Water's own 28 January 2026 release replaces the Water Magazine report; added NISRA Q2 2026 output, GOV.UK release announcement, DoF new dwelling statistics, DfI news release (19 March 2026), HMRC CBAM policy summary, Budget 2026 Red Book, European Commission EUDR page.
- Land Repair Helix link moved from the github.io address to robertjpark.co.uk (relative link on the page).
- Checked and unchanged: Q1 2026 output figures (NISRA, 25 June 2026), Q2 2026 (−1.7% on the quarter, +17.5% on pre-pandemic; NISRA, 24 September 2026), NI Water £7bn and 156 of 192 overflows, DfI voluntary developer contributions and 5,300 homes (19 March 2026), DAERA contaminated land status (Part III uncommenced; study "may be completed in 2027").

**Dashboard (`tools/dashboards/ni-construction-building.html`)**
- Rules table and CSV: UK CBAM now any non-UK origin, EU included, with the 31 January 2028 registration date; EUDR micro and small timber businesses from 30 December 2026.
- Context table: new dwelling starts and completions, April to June 2026, added.
- Sources: HMRC policy summary, European Commission EUDR page, DoF/NISRA new dwelling statistics and the Q3 release date added; NI Water primary source replaces Water Magazine. Checked-on note and footer now say updated 9 November 2026; commentary links say 9 November 2026. No github.io links.

### Focus on Transport & Fleet — 9 November 2026

*Signed off by Robert and published on Monday 9 November, four days early (was due Friday 13 November); re-dated to 9 November throughout (page, PDF file name and footer, post, dashboard).*

**Added**
- `blog/focus-on-transport-fleet-november-2026/index.html`: the issue as a web page, with three charts, the PDF reader and links to the dashboard and the Scopes Map.
- `assets/focus-on-transport/2026-11/`: charts (`01-chargers.png` public chargers per 100,000 by nation and region; `02-sectors.png` sector emissions, base year and 2024; `03-journeys.png` Translink bus and rail journeys) and the 5-page PDF `Focus-on-Transport-and-Fleet-9-November-2026.pdf`.
- `_posts/2026-11-09-focus-on-transport-fleet-november-2026.md`: summary post (18:45, 9 November).
- `tools/dashboards/ni-transport-fleet.html` (from branch `focus-on-dashboards`, updated), and its entry in `dashboards.md`.

**Changed from the signed-off draft, checked 9 November against official sources**
- Scopes Map link moved from the github.io address to robertjpark.co.uk.
- UK ETS shipping: the 50% surrender deduction for GB–NI voyages (either direction) is confirmed by the UK ETS Authority's main response on domestic maritime (GOV.UK, November 2025), which replaces the interim response as the source; port stays count in full (DNV). The same response confirms the first surrender, for 2026 and 2027 emissions, is due by 30 April 2028, so that date (left out of the draft pending this check) is now in the deadlines table.
- EV chargers: no newer DfT release. The 1 July 2026 statistics (published 27 August) remain the latest; the 1 October release is due on 25 November. NI figures unchanged (60.0 and 19.3 per 100,000).
- Public transport: DfI published 2025-26 statistics on 16 September 2026. Journeys rose to 84.0m, above 2019-20 (83.4m); rail 15.9m (4.9% above 2019-20), bus 68.1m (0.2% below). Stat tile, intro sentence, section heading ("Rail has recovered, buses nearly"), paragraph, chart and dashboard updated; the draft's "rail use has not recovered" was no longer true.
- EV attitudes: the 2024/25 survey (DfI/NISRA, 4 December 2025) replaces 2023/24: 19% would consider an EV next (25% in 2023/24, 38% in 2021/22); barriers price 75%, recharging 54%, public chargers 44%, range 43%.
- Zero emission goods vehicles: the draft said DfI was preparing changes; since 1 August 2026 category B drivers with two years' licence can drive ZEGVs up to 4,250 kg (5,000 kg with specialist equipment for disabled users) (DfI, 30 July 2026).
- Sources: RAC and Fleet News replaced by GOV.UK (DfT Electric Car Grant statements of 15 July and 3 December 2025; HMRC company car tax policy paper for 2028–30). Figures re-checked with no change: inventory (3.9 Mt, 21.3%, +9.2%), Electric Car Grant (£3,750, £37,000 cap, £1.3bn to 2030), BIK 4/5/7/9%.
- Dashboard: as-at date 9 November 2026; Translink, EV intent and barriers charts and tiles updated; shipping and ZEGV rows updated; sources moved to GOV.UK/DfI; footer and commentary links re-dated.

### v0.26.0 — 9 November 2026: thought piece on maritime and subsea-cable security

- `_posts/2026-11-09-ireland-europes-weak-flank.md`: "Ireland is Europe's weak flank, and the cables, cash and freight all land there" (agreed 5 November), signed off by Robert on 9 November and published the same evening (was due 16 November), in the Latest thinking strip until 23 November. Evidence-led; no motive claims. Corrections to the brief: the Yantar entered Ireland's zone in November 2024, not 2025; the EU-funding point is framed as the post-Brexit "project of mutual interest" mechanism, not a snub; Ireland ordered primary radar in September 2026 (full capability end of 2028).

### v0.25.2 — 9 November 2026: Policy series checks on the live pieces

The 13 Policy series pieces went live on 2 November before their pre-publication checks. The open checks were run on 9 November against official sources; these were corrected:

- ESOS: Invest NI's Energy Efficiency Capital Grant is paused and not taking applications (it was listed as able to fund follow-through); SI 2026/701 link now points to the `/made` version Parliament's record gives.
- Digital waste tracking: the Assembly's AERA Committee lists the Digital Waste Tracking Regulations (NI) 2026 (no made rule yet); the Waste Crime Action Plan statement now links to Parliament's record (HCWS1430), not a mirror.
- Closed for booking: NI legal basis for free household waste deposit added (1997 Order, Art. 25(1)(b)).
- Land law: ELD and Soil Monitoring Directive described as not on DAERA's Windsor Framework Annex 2 list (3 Apr 2026); CL:AIRE's own page replaces the LexisNexis summary.
- Lough Neagh: Utility Regulator's PC21 extension decision (21 Aug 2026) added as the source for £693m and 3.4%; Water Framework and Nitrates Directives described as not on DAERA's Annex 2 list.

Checked with no change needed: VAT zero rate still GB only; no NI BICS details yet; no DESNZ SECR/ESOS consultation; no Defra HFC next-steps report; no Year 2 PackUK fees; no final NI waste strategy; no England PFAS drinking-water consultation. Not verifiable from here (Hansard and legislation.gov.uk pages would not open): the DfE official's remark date, two Hansard link swaps, the Lough Neagh JR outcome.

### v0.25.1 — 9 November 2026: public realm post describes the revised Bill

- `_posts/2026-10-17-improving-the-public-realm.md`: "The law is part of the problem" now describes the reworked, shorter framework Bill (old amenity laws left to a Law Commission consolidation; definition, stewardship and continuous improvement, minimum and enhanced entitlements, appraisal; devolved adoption and the NI position). The live post still described the August draft (215 clauses, 26 Schedules, 37 enactments). The text was written on 17 October on branch `v0.7.0-content` but never merged; front matter kept as on main.

### v0.25.0 — 9 November 2026: put the priced offer where a buyer can see it

*From the commissioning-client review of 5 November. Approved by Robert on 9 November.*

- `_layouts/default.html`: "CBAM Desk" added to the main navigation after Services; same link in the self-contained navs of the UK CBAM Countdown and the CBAM Exposure Tracker.
- `index.html`: second hero button is now "UK CBAM Exposure Check, £495" (was "See services"); the tools band shows four tiles (Countdown, Exposure Tracker, Consultations Monitor, Carbon Jigsaw) instead of sixteen; puzzles, guides and classroom material stay on the tools page.
- Metals issue page, Countdown and Exposure Tracker: closing lines now point to the £495 check rather than "get in touch".
- `services.md`: ESOS section rewritten for the thresholds (250 staff, £44m/£38m; Phase 4 qualification 31 December 2026, notify by 5 December 2027) and says plainly that smaller firms are out of scope and get a carbon inventory and contract review instead.

### v0.24.3 — 7 November 2026: links to the Consultations Monitor

- `public-sector.md`: new "NI Consultations Monitor" section above Consultation responses, with a link to the dashboard (shown whether or not any responses are published).
- `public-sector/consultation-responses.md`: links to the monitor in the introduction and in "Help with your own response".
- `_posts/2026-11-05-when-did-your-voice-on-a-consultation-last-get-heard.md`: fix 2 ("A public consultation tracker") now points to the monitor, says what it covers and that it cannot count responses.

### v0.24.2 — 6 November 2026: Consultations Monitor weekly refresh

- `data/dashboards/ni-consultations/consultations.json`: 19 consultations added (C404–C422; 420 in all). One is high relevance (DfI Quay Street car park abandonment, Lisburn, closes 15 Dec), two medium (Belfast draft playing pitches strategy; DfT zero emission vehicle mandate review, closed), the rest low (UK Government items with NI in scope, including HMT/HMRC CBAM refinery products).
- Status roll-forward: 3 records closed and awaiting a response (C038, C372, C373). Responses found for 2 (C115 Lagan Meadows quiet area; C225 Belfast masterplan SPGs). 83 open, 2 not yet open.
- Corrections: C388 Black Paths engagement now opens 16 Nov (not yet open; no closing date given); closing dates filled for 11 records; opening dates fixed for C042, C372, C394, C402; better links for 13 records; duplicate C403 (Single Construction Regulator, already C202) removed.
- `_scripts/dashboards/consultations_build.py`: AS_AT 6 November 2026 and a changes line; page and CSV rebuilt.

### v0.24.1 — 5 November 2026: corrections from the three-reviewer hard review

- `working-with.md`: the professional indemnity line now says cover for the work Robert manages is being arranged and a certificate is supplied before any paid work starts.
- `assets/focus-on-agriculture/2026-10/Focus-on-Agriculture-October-2026.pdf`: the footer (page 1), contact line (page 6) and the farm-data-checker link now use robertjpark.co.uk; the old github.io address is gone from every public asset.
- Consultations Monitor: the DfI classes and thresholds review was listed twice (original 9 October close and the 6 November extension). Duplicate removed; 402 consultations; dashboard rebuilt; `dashboards.md` and the v0.24.0 entry corrected.
- "We don't fund the drains": the £68m road maintenance figure is the 2025–26 opening structural maintenance budget, not "this year"; relabelled in the post and the public realm dashboard tile, with the Highways Magazine source added.
- A "general information, not tax, legal or financial advice" line added to eight CBAM, ESOS and finance posts (including the three held pieces).
- `policy-series.md`: no longer says the first piece "publishes on 16 November" or "two a week". `dashboards.md`: "weekly" *Focus on* → monthly. `cbam-desk.md`: who it is for now reflects that goods dispatched from NI do not trigger EU CBAM.
- `_posts/2026-10-15-the-report-is-the-by-product.md`: date added to the front matter. Changelog filename for the Metals post corrected.
- `pr-check.yml`: now also fails if any PDF under `assets/` carries the old address or the personal mobile, or if a data file lists the same body and title twice.

### v0.24.0 — 5 November 2026: NI Consultations Monitor dashboard

- `tools/dashboards/ni-consultations-monitor.html`: new dashboard of every open, upcoming and recently closed public consultation at the 11 councils, nine departments and UK Government where NI is in scope (402 since 22 April 2025), with closing dates, response-publication rates by level and body, a council transparency score, and a filterable full list with summaries. Static, no outside scripts, self-hosted fonts.
- `data/dashboards/ni-consultations/`: the data behind it (`consultations.json`, `council_access.json`) and a full `consultations.csv` for download, following the 22 October review's data-folder pattern.
- `_scripts/dashboards/consultations_build.py`: builds the page from the data. Refresh: update the JSON, set `AS_AT`, add a `CHANGES` line, run `python3 _scripts/dashboards/consultations_build.py .`
- `dashboards.md`: entry added; lead line widened to mention consultations.

### Focus on Metals & Manufacturing — 5 November 2026 (branch `publish/metals-2026-11-06`)

*Signed off by Robert at 12:55 on 5 November and published straight away, a day early; re-dated to 5 November throughout (page, PDF file name and footer, post, dashboard).*

**Added**
- `blog/focus-on-metals-manufacturing-november-2026/index.html`: the issue as a web page, with three charts and the PDF.
- `assets/focus-on-metals/2026-11/`: charts (sales by destination, sector emissions, six deadlines) and the 6-page PDF.
- `_posts/2026-11-05-focus-on-metals-manufacturing-november-2026.md`: summary post (12:00, 5 November).
- `tools/dashboards/ni-metals-manufacturing.html`, and its entry in `dashboards.md`.

**Changed after a three-reviewer check on 5 November (scientist, engineer, Big Four consultant)**
- Blocker fixed: the draft said goods from the EU were outside UK CBAM. HMRC's policy summary (2 Nov 2026) says no jurisdiction is exempt and the levy applies to goods of any non-UK origin; carbon price relief covers only a carbon price actually paid, and free allowances do not count. Text, table, action points, stat tile, dashboard and charts all corrected.
- Industry emissions: the inventory attributes the fall to food and drink, chemicals and cement; the coal-and-oil-to-gas explanation belongs to electricity supply, so the heading and paragraph were rewritten. "1990" is now "the 1990 base year" (1995 for F-gases).
- Energy section rewritten for fabrication shops (welding and cutting plant, compressors, high-bay lighting, space heating on oil or LPG; LEDs, leak repair, VSDs, destratification).
- Product data advice: direct production emissions per tonne by product, precursors included, which is the shape of a CBAM request; corporate Scope 1 and 2 kept separate.
- Records to keep from 1 January, default values when the mill can't supply data, stockholder and freight-forwarder liability, ESOS thresholds, the Finance Act 2026 Part 5 citation, and a not-tax-advice line added.
- DDP point corrected: goods dispatched from NI do not trigger EU CBAM; exposure is shipping from GB or outside the EU direct to an EU customer.
- Rest-of-world sales are published (£5.5bn, +1.5%), not derived. Sources: Clifford Chance replaced by HMRC's own pages.

**Changed from the draft, checked 5 November (first pass)**
- ETS linking: still reported, not confirmed; the summit is on 20 November. The paragraph says so and promises an update after it.
- UK CBAM: the Emissions and Verification Regulations 2026 (SI 2026/995) are made and in force from 1 January 2027. Registration threshold is £50,000 in any 12 months (or expected within 30 days); HMRC registration opens 1 January 2028; 2027 importers have until 31 January 2028 (as reported by Clifford Chance). Budget 2026 default values (global 2027–28, country-specific from 2029) added.
- EU CBAM: "not formally extended to NI, under review" replaced with "does not apply in NI", matching the CBAM tracker and the EU law dashboard. The DDP point is softened to "check with your customs agent".
- Tool links moved from the github.io address to robertjpark.co.uk.
- `_scripts/dashboards/build.py`: metals dashboard dates and notes updated to match; new sources (HMRC, SI 2026/995, Budget 2026, Clifford Chance).

### v0.23.2 — 5 November 2026: DfI response marked as submitted

- `_posts/2026-11-06-response-planning-classes-and-thresholds.md`: Robert submitted the response to DfI on 5 November; `submitted` front matter and the page's details list now say so (closing date 6 November unchanged). Still publishes at 17:00 on Friday 6 November.

### v0.23.1 — 6 November 2026: consultation response on planning classes and thresholds

*Robert's instruction, 5 Nov 00:10: find the DfI consultation and draft a full response.*

- `_posts/2026-11-06-response-planning-classes-and-thresholds.md`: second entry on the Consultation responses page, Robert's response to DfI's Review of the Classes and Thresholds in the Schedule to the Planning (Development Management) Regulations (NI) 2015 (closed 6 November 2026, extended from 9 October). Better-regulation framing (second pass, 5 Nov 00:30): opens with the consultation response numbers (224, 100, 59, 67) and an open question on why they are tolerated; eighteen asks tagged by remit, context and five positions in Annex A; reviewed twice on 5 Nov by five agents (planning law, EU/trade law, science, business, finance) plus a US political/FDI/security reviewer in round two, with legal and factual corrections applied (nuclear is Class 2 not Class 1; reg 2(1)(b) already covers extensions; s.26(7) bars a deemed notice; NI tariffs just below the GB cap; dispatch-down 29.6%/22%; Celtic 2028), with a section on the EU and GB rules NI carries under the Windsor Framework without prior scrutiny (SMRs kept open, storage against dispatch-down, demand reduction with vouchers and training, no offshoring of production, energy equipment inside the carbon border and judged on the whole of ESG, with an embodied-carbon and supply-chain statement on major energy applications), including 20 MW for generation to match Scotland, Scotland's extensions rule, a fuel-production description, COMAH instead of GWh for chemical storage, NIFRS as consultee rather than major status for batteries, a hazardous-waste de minimis, a 28-day clock on section 26 referrals, and application numbers for the RIA. Scheduled for 17:00 on Friday 6 November, the moment the consultation closes; a 17:05 UTC Friday rebuild was added to `publish-scheduled-posts.yml`.
- `assets/consultations/2026-11-dfi-development-management-classes-thresholds-response.pdf`: the full response, 14 pages, built with the site fonts and logo (`_scripts/consultations/build_dfi_classes_thresholds_pdf.py` from `_scripts/consultations/dfi-classes-thresholds-response.md`).

### v0.23.0 — 2 November 2026: two thought pieces live with briefings and dashboards; Focus on Agriculture November

*Robert's instructions, 2 Nov 01:03–01:05.*

**Added**
- `_posts/2026-11-02-focus-on-agriculture-november-2026.md` at /blog/focus-on-agriculture-november-2026/, from the approved Claude Doc (sources opened 1 Nov 2026).
- Briefing 04 `assets/briefings/2026-11-ni-screen-how-do-we-grow-it-briefing.pdf` and Briefing 05 `assets/briefings/2026-11-who-pays-for-the-public-realm-briefing.pdf`: the full pieces with an "In numbers" panel and sources (built by `_scripts/briefings/build_thought_pdfs.py`).
- Dashboards `tools/dashboards/ni-screen-industry.html` and `tools/dashboards/ni-public-realm-water-roads.html` (built by `_scripts/dashboards/build_thought.py` from the figures cited in each piece; listed on `dashboards.md`).

**Changed**
- "Northern Ireland Screen is fantastic. So how do we grow it?" and "We don't fund the drains. Then we pay for the flood." moved from 10 and 12 Nov to publish now (files renamed to 2026-11-02-*), each with links to its briefing and dashboard.

### v0.22.0 — 2 November 2026: 13 policy pieces published now; four held

*Robert's instruction, 2 Nov 01:04, following his 1 Nov sign-off.*

**Changed**
- 13 approved Policy series pieces moved from the 16 Nov–20 Jan schedule to publish now (dated 2 Nov 2026, 00:01–00:13; files renamed to 2026-11-02-*; home-page `hero_until` 9 Nov): One data set, many requests; The price of a separate grid; ESOS and the audit that pays only if you act; Two refrigerant rulebooks; Green money, fewer rules; Northern Ireland's waste bill; Brown bins, black holes; The end of the paper trail; Gold in the bin; Closed for booking; Forever chemicals, two rulebooks; The land law Stormont never switched on; Lough Neagh and the price of clean water.
- Green money, fewer rules: grants line corrected. The Energy Efficiency Capital Grant is paused for review with no reopening date; the Resource Efficiency Capital Grant closed to new applications on 27 March 2026.
- Held with `published: false` (Robert's 1 Nov decision): The Irish Sea carbon bill (until after the 20 Nov UK–EU summit), Carbon borders as industrial policy (CBAM), Fertiliser: a small tax, a big bill and a lough, The Act that outran its plan (NICCA).

### v0.21.0 — 1 November 2026: Halloween pumpkins post and Briefing 03

**Added**
- `_posts/2026-11-01-carved-binned-and-smashed-the-full-cost-of-halloween-pumpkins.md`: *Carved, binned and smashed: the full cost of Halloween pumpkins in Northern Ireland*. Estimates for NI (about 818,000 carved, 425,000 uneaten, ~911 t of flesh, 21–41 t of seed), rats, hedgehogs and woodland, public realm harm, and a "design the after-party, not the ban" approach with seven recommendations. NI figures are pro-rata estimates from Hubbub UK data.
- `assets/briefings/2026-11-halloween-pumpkins-full-cost-briefing.pdf`: Briefing 03, four pages, in the Briefing 01 house style.

### v0.20.0 — 1 November 2026: "Which EU rules apply to me?" (decision 10)

**Added**
- `tools/which-eu-rules-apply.html`: three questions (what you make or handle, where your goods go, and whether goods from GB are "at risk") that return the matching rows from the EU law dashboard in four groups: EU rules for your goods in NI, moving goods from GB into NI, where GB and NI rules differ, and rules that reach you through EU customers. Runs in the browser; nothing is sent.
- `_scripts/dashboards/eu_rules_tool.py`: builds the tool from the data lists in `eu_build.py`, so the two never drift. Each law is mapped to the questions in two small tables; the build stops if a new law has no mapping, so the weekly update can't publish a law the tool doesn't know about. Run it after `eu_build.py`.

**Changed**
- EU law dashboard: links to the tool in the introduction and footer (no data change).
- `tools.md` and `public-sector.md`: links to the tool.
### v0.19.1 — 1 November 2026: check every push to main (decision 11, part 1)

**Changed**
- `.github/workflows/pr-check.yml`: also runs on every push to `main`, not only on pull requests, so a direct push that breaks a house rule (personal number, github.io address, Google Fonts, external script, broken front matter, rotating hero) shows a failed check and GitHub emails Robert.

**Still to do (Robert, in GitHub settings):** the branch ruleset on `main` that stops direct pushes and requires the PR check to pass. The tools Claude uses cannot change repository settings.

### v0.19.0 — 1 November 2026: one fixed home-page hero (decision 6)

**Changed**
- `index.html`: the rotating hero is gone. The home page always opens on "Carbon and environmental compliance for manufacturers working across two regimes" (Robert's decision 6, confirmed 1 Nov). The random-rotation script is removed.
- Thought pieces and Policy series posts with `hero_title` now appear in a "Latest thinking" strip under the hero instead: up to three, newest first, each shown only once published and until its `hero_until` date. Front matter is unchanged, so `hero_eyebrow`, `hero_title`, `hero_lead` and `hero_until` keep working as before; `hero_button` and `hero_button2` are no longer used.
- `assets/style.css`: `.latest-thinking` strip, three columns on wide screens.
- `.github/workflows/publish-scheduled-posts.yml`: extra daily rebuild at 07:35 UTC. Policy series posts are dated 07:30, but the site only rebuilt at 11:05 and 12:05 UTC, so they would have gone live about four and a half hours late.
- `.github/workflows/pr-check.yml`: the hero-script check is replaced by a check for exactly one h1, the fixed hero line, and no rotation script.

### v0.18.1 — 1 November 2026: build fix

**Fixed**
- `policy-series.md`: sorting ran before the empty-state check, so the live Pages build (future posts hidden) failed on a null list. Sort now happens inside the check.
- `cbam-desk.md`, `about.md`, `tools.md` and `privacy.md`: unquoted colons in `description` broke their front matter since v0.17.0 (Jekyll warned but built). Quoted.
- `.github/workflows/pr-check.yml`: the PR check now also builds with future posts hidden, as Pages does, and fails on front matter that does not parse.

### v0.18.0 — 1 November 2026: Policy series (17 scheduled pieces)

**Added**
- `policy-series.md` (/policy-series/): index page for the series, grouped by theme, listing each piece once it is live, with an empty state before 16 November.
- 17 scheduled posts in `_posts/` with `categories: [policy-series]` and `series_theme`, publishing at 07:30 on Mondays and Wednesdays from 16 November 2026 to 25 January 2027 (no posts in the Christmas fortnight): One data set, many requests (16 Nov); The price of a separate grid (18 Nov); ESOS and the audit that pays only if you act (23 Nov); The Irish Sea carbon bill (25 Nov); Carbon borders as industrial policy (30 Nov); Fertiliser: a small tax, a big bill and a lough (2 Dec); Two refrigerant rulebooks, one small market (7 Dec); Green money, fewer rules (9 Dec); Northern Ireland's waste bill (14 Dec); Brown bins, black holes (16 Dec); The end of the paper trail (4 Jan); Gold in the bin (6 Jan); Closed for booking (11 Jan); Forever chemicals, two rulebooks (13 Jan); The land law Stormont never switched on (18 Jan); Lough Neagh and the price of clean water (20 Jan); The Act that outran its plan (25 Jan). Time-sensitive pieces (consultations closing 30 Nov, ESOS 5 Dec, CBAM and F-gas 1 Jan) go first.
- `assets/policy-series/<slug>-lifecycle.png`: the lifecycle diagram from each piece (17 files, 2.8 MB in all).
- Each post carries a one-week home-page hero headline (`hero_until` = publish date + 7 days) pointing to the piece and to the series index.

**Changed**
- `public-sector.md`: "Policy series" paragraph linking the index, shown once the first piece is live.

**Source and process**
- Text taken unchanged from the 17 final drafts Robert approved on 1 November 2026 (Claude Docs, dated 30 October). Removed from each: the author chip line, the "final draft for review" line (replaced by "Facts checked to 30 October 2026") and the "Checks before publishing" list. Those checks are collected in the project doc `claude/policy-series-checks.md` for the week before each piece publishes.

### v0.17.0 — 1 November 2026: review actions, CBAM Desk and Who I work with (signed off 1 Nov)

*Merged on top of v0.16.0. On merge: the offsets post's description rewritten to match its new title; descriptions added to the two posts published since this branch was opened (Crystals in Confinement, Focus on Hospitality, Retail & Leisure), so every post has one.*

*Actions from the 22 October deep review. Not merged until Robert signs off; CBAM Desk prices are a recommendation awaiting his decision.*

**Added**
- `cbam-desk.md` (/cbam-desk/): fixed-price CBAM offer — free first call, £495 Exposure Check, £1,250 UK CBAM Importer Readiness, Supplier Data Pack from £1,750 per site, £250-a-month CBAM Desk. Prices benchmarked against published UK CBAM fees (October 2026).
- `working-with.md` (/working-with/): how each service is delivered, the registered specialists brought in (by category, no firm names yet), the Imperial associate roles, and consortium working.
- Home page: CBAM Exposure Tracker, Farm Carbon Data Checker and Dashboards tiles; structured business data (ProfessionalService, Larne, Co. Antrim; no street address).
- `assets/style.css`: `.update-box` for dated updates at the top of posts.

**Changed**
- Main menu: Dashboards added.
- Unique meta descriptions for Services, Public sector, Tools, About, Contact, Privacy, Blog and every published post.
- `_config.yml`: `locale: en_GB`.
- About: "sales management at Vodafone" corrected to "Dot Mobile, a Vodafone subsidiary".
- CBAM and CSRD post: dated update box (ETS link status and the 20 November summit, UK CBAM regulations, illustrative rate, indirect emissions deferred to 2029, NI outside the EU CBAM); "into GB" corrected to "into the UK, including Northern Ireland".
- Services and Public sector: links to CBAM Desk and Who I work with; "accredited partners" reworded to "registered and accredited specialists".
### v0.16.0 — 30 October 2026: Budget 2026 briefing and post

**Added**
- `_posts/2026-10-30-budget-2026-what-it-means-for-northern-ireland-businesses.md`: *Budget 2026: what it means for Northern Ireland businesses on energy, carbon and CBAM*, with a hero headline. Lead: the GB electricity discount, the 0% VAT on electricity and the end of Carbon Price Support all stop at the Irish Sea; NI is "funded to deliver a comparable scheme" with no design or date. Also covers UK CBAM default values (global 2027–28, country-specific from 2029), refined products proposed for CBAM scope, the energy-from-waste UK ETS delay, Landfill Tax, Plastic Packaging Tax certification, capital allowances, tariff suspensions and self-employed measures. Every claim paragraph-referenced to the Red Book (HC 726) or gov.uk guidance.
- `assets/briefings/2026-10-budget-2026-northern-ireland-business-briefing.pdf`: Briefing 02, six pages, in the Briefing 01 house style.

**Still to do** (from the Budget review of 28 October): CBAM countdown and CBAM Exposure Tracker need the global-default caveat for 2027–28; ESG regime tracker needs the Carbon Price Support, CCL, BICS, energy-from-waste and PPT entries and Red Book citations; CBAM and CSRD post needs a paragraph on default values and scope; the 2 November agriculture post should mention the fertiliser tariff suspension.

### v0.15.0 — 27 October 2026: Crystals in Confinement and the UK CBAM countdown

*Released ahead of v0.14.0 (review actions, CBAM Desk), which is still awaiting sign-off in PR 10.*

**Added**
- `_posts/2026-10-27-crystals-in-confinement.md` at /research/crystals-in-confinement/: a web article version of the Crystals in Confinement positioning paper, with facts rechecked on 27 October 2026. DAERA's cost and resource study received no tenders (DAERA says it may be completed in 2027), so the "report commissioned" line from v4 of the paper is corrected. The PFAS Plan land guidance is no longer given a date. The PDF is not linked until the updated paper is cleared.
- `tools/uk-cbam-countdown.html`: a live countdown to the UK CBAM on 1 January 2027, with the UK and EU dates that follow and a five-point checklist. Listed on `tools.md`.

**Changed**
- `about.md`: Vodafone corrected to Dot Mobile, a Vodafone subsidiary. Doctoral research described accurately (no degree awarded) and linked to the new article. Qualifications updated: CISL High Impact Leadership in Sustainability, Chartered IIA Certificate in Internal Audit modules, CIPR since 2014, FRSA, IoD.
- `_posts/2026-10-16-contaminated-land-in-northern-ireland.md`: links to the new article.

### v0.13.0 — 27 October 2026: spicy headlines and four thought pieces (for sign-off)

*Rebased on v0.12.0 (Storm Boelo). The public realm piece now builds on the Largs post rather than repeating its flood evidence: new title, banner and opening, with a link through to Largs.*

**Changed**
- `index.html`: the home-page hero rotation now reads extra headlines from post front matter (`hero_eyebrow`, `hero_title`, `hero_lead`, `hero_button`, `hero_button2`, optional `hero_until`). A post's headline joins the rotation only once the post is live, so the banner never links to an unpublished page. The three standing messages (manufacturers, suppliers, public sector) are unchanged; the manufacturers message stays the no-JavaScript default.
- `_posts/2026-10-17-improving-the-public-realm.md`: its old hard-coded hero message moved into front matter, with `hero_until` set to 12 November 2026 at 12:00, when the new public realm piece replaces it.

**Added** (scheduled posts, each with a hero headline)
- `_posts/2026-11-02-save-local-agriculture-stop-offshoring-our-food.md`: "If we want to save local agriculture, stop the regulations that offshore our food". Monday 2 November, 12:00.
- `_posts/2026-11-05-when-did-your-voice-on-a-consultation-last-get-heard.md`: "When did you last have your voice on a Stormont or EU consultation heard?" Thursday 5 November, 12:00.
- `_posts/2026-11-10-northern-ireland-screen-how-do-we-grow-it.md`: "Northern Ireland Screen is fantastic. So how do we grow it?" Tuesday 10 November, 12:00.
- `_posts/2026-11-12-we-dont-fund-the-drains-then-we-pay-for-the-flood.md`: public realm failure on investment and climate, drawing on the Public Realm Bill. Thursday 12 November, 12:00.

Each piece has three illustrative scenarios, practical fixes, the strongest counter-argument, "what would change my mind" and a source list (official sources first; no energy broker sites).
### v0.12.0 — 26 October 2026: Storm Boelo post and first briefing PDF

**Added**
- Blog post: *Largs flooded this morning. Nobody is to blame. That is the problem.* (`_posts/2026-10-26-largs-flooded-nobody-to-blame.md`), drawing on a UK/EU evidence review of public-realm under-investment and climate impacts, with a section on Kilroot and Ballylumford.
- First branded briefing PDF, *Built for Yesterday's Weather* (Briefing 01), at `assets/briefings/2026-10-built-for-yesterdays-weather-briefing.pdf`, linked from the post. New `assets/briefings/` folder for future briefings.

### v0.11.1 — 23 October 2026: response PDF rebranded

**Changed**
- `assets/consultations/2026-10-dfc-historic-environment-policy-response.pdf`: rebuilt with the official logo files (full lockup in the header, mark in the footer) and brand red #A61C1C. Text unchanged.

### v0.11.0 — 24 October 2026: Consultation responses

**Added**
- `public-sector/consultation-responses.md` (/public-sector/consultation-responses/): a section for selected consultation responses, listing every post in the `consultation-responses` category with consulting body, closing date and outcome.
- `_posts/2026-10-24-response-historic-environment-policy.md`: first entry, Robert's response to the DfC Historic Environment Policy consultation (closed 23 October 2026), with the eight asks and a link to the full response. Scheduled for 12:00 on 24 October 2026.
- `assets/consultations/2026-10-dfc-historic-environment-policy-response.pdf`: the branded 14-page response as submitted. The file is on the server from the merge but is not linked anywhere until the post publishes.
- `_posts/2026-10-24-publishing-my-consultation-responses.md`: blog post announcing the section. Scheduled for 12:01 on 24 October 2026.
- `.github/workflows/publish-scheduled-posts.yml`: asks GitHub Pages to rebuild at 11:05 and 12:05 UTC every day (falls back to an empty commit if the request is refused), so future-dated posts go live on time. Can also be run by hand from the Actions tab.

**Changed**
- `public-sector.md`: new "Consultation responses" paragraph linking the section. It only shows once at least one response has published.
- `HOW-TO-POST.md`: how to schedule a post and how to add a consultation response.

**Checked:** DfC's privacy notice for the consultation places no restriction on respondents publishing their own responses; DfC may publish responses itself, with personal data removed.

### v0.10.0 — 22 October 2026: CBAM Exposure Tracker

**Added**
- `tools/dashboards/cbam-exposure-tracker.html`: the CBAM Exposure Tracker, rebuilt from Robert's working dashboard as a fixed snapshot (figures as at 22 October 2026). One self-contained page: four data tables (EU certificate prices, NI goods trade, where an NI business stands, EU and UK rules), self-hosted fonts, no outside scripts, nothing stored. Unlike the agriculture dashboard, the tables and figures are written into the HTML, so the page reads without JavaScript; the script only adds the CSV downloads and the days-to-go count for the UK CBAM. Skip link, `:focus-visible`, scrollable labelled tables, dark mode.
- New "Where an NI business stands" table: six common situations (selling NI goods to the EU, importing CBAM goods into NI, outward processing, returned goods, an EU group company, GB goods via NI), with what applies under each regime and what to do.

**Checked against primary sources, and corrected**
- EU certificate prices (Q1 €75.36, Q2 €75.28, Q3 €82.32) and publication dates: match the Commission's price page.
- HMRC NI trade, year to June 2026 (£7.4bn exports to the EU, +6.7%, etc.): match the Q2 2026 commentary, published 17 September 2026. Now labelled as all goods, not CBAM goods.
- UK CBAM rules: match the GOV.UK policy summary updated 16 October 2026.
- **Northern Ireland row was wrong.** The working copy said EU CBAM treatment of NI goods should be checked case by case, and its intro said NI suppliers face data requests "from both sides". Corrected: goods produced in, or released for free circulation in, NI are outside the EU CBAM (UK Government written answer HL12132, 3 December 2025; Commission FAQ update, October 2026). The UK CBAM applies in NI from 1 January 2027.
- Removed the unverified "unused 2026 certificates cancelled 1 Nov 2027"; now "repurchased within limits, the rest cancelled".
- Added rows for emissions data and default values, and the UK–EU ETS link (Council mandate November 2025; no exemption in force).

**Changed**
- `dashboards.md`: CBAM Exposure Tracker entry, listed first.
- `tools.md`: Dashboards entry names both dashboards and links the tracker.
- `services.md`: link to the tracker under CBAM and CSRD. (There is no CBAM Desk offer page yet; link it from there when it exists.)

**Refresh due:** Q4 2026 EU price on 4 January 2027; first UK CBAM sector rates from 1 January 2027.

### v0.9.1 — 21 October 2026: custom domain and new email

**Changed**
- `CNAME`: the site now serves at https://robertjpark.co.uk (www redirects to it). GoDaddy DNS: four A records for @ to GitHub Pages (185.199.108.153, .109, .110, .111) and a CNAME for www to robertjparkuk.github.io. Old robertjparkuk.github.io links redirect automatically.
- `_config.yml`: `url` set to https://robertjpark.co.uk; `email` now robert@robertjpark.co.uk (Microsoft 365 Business Basic, tenant RobertJPark.onmicrosoft.com).
- `contact.md`, Planet Check, the farm checker, the agriculture briefing and dashboard: hard-coded addresses and email updated.

**Not changed:** the Focus on Agriculture PDF still prints robertjparkuk.github.io; that address redirects, so it can wait for the November issue.

### v0.9.0 — 20 October 2026: Dashboards

**Added**
- `tools/dashboards/ni-agriculture-land-carbon.html`: the NI Agriculture and Land Carbon dashboard, copied from Robert's working dashboard as a fixed snapshot (figures as at 18 October 2026). Self-contained: the ten data tables are inside the page, with no d3 or other outside script, and it uses the self-hosted fonts, so it contacts no third party and stores nothing. A Data and sources section lists every table's source and offers a CSV download for each.
- `dashboards.md` at `/dashboards/`: index of public dashboards.
- `_snippets/embed.html`: dashboard links.

**Changed**
- `tools.md`: Dashboards entry.
- `blog/focus-on-agriculture-october-2026/index.html`: a second call-out linking the briefing to its dashboard.

**How to add the next dashboard:** export its data and page from the working copy, rebuild it as a single file in `tools/dashboards/`, add it to `dashboards.md`, and keep private research (for example the NI Business Succession Screen) off the site. Refreshing figures means replacing the file; nothing updates by itself on GitHub Pages.

**Watch:** when the custom domain goes live, update the canonical and `og:` URLs in the dashboard as well as the two Focus on Agriculture pages.

### v0.8.1 — 19 October 2026: agriculture briefing review fixes

**Fixed**
- Removed `foa-website/`, a duplicate of the uploaded files that would have published a second copy of the briefing, tool and PDF under `/foa-website/`.
- Both new pages loaded Google Fonts (Poppins), breaking the privacy promise that no page contacts an outside service. They now use the self-hosted Fraunces, Source Sans 3 and Source Serif 4.
- Briefing page: main navigation (Home, Services, Tools, Blog, Contact) and a Privacy link in the footer.
- Farm Carbon Data Checker: logo links home like the other tools; Privacy link and "Facts as at" line; leftover `claude:viewport-fit-sides` meta tag removed.
- Farm Carbon Data Checker wording, to match the GHG Protocol and the Scopes Map: contractor fuel moved to Scope 3; a renewable tariff lowers only market-based Scope 2; exported power cannot be subtracted from Scope 2; land carbon is reported alongside emissions, not netted off.

**Added**
- `_posts/2026-10-18-focus-on-agriculture-october-2026.md`: a short summary post so the briefing appears in the Blog list, on the home page and in the RSS feed. Its `link:` sends listings straight to the full briefing; `blog/index.html` and `index.html` now honour `post.link`.
- `tools.md`: Farm Carbon Data Checker entry. `privacy.md`: the checker added to the local storage table.

### v0.8.0 — 18 October 2026: Focus on Agriculture and the Farm Carbon Data Checker

**Added**
- `blog/focus-on-agriculture-october-2026/index.html`: the October briefing (standalone page, embeds the PDF).
- `assets/focus-on-agriculture/2026-10/`: five infographics and the 7-page PDF.
- `tools/farm-data-checker/index.html`: checklist of 24 records for a farm Scope 1, 2 and 3 report, with NI sources, copy and CSV download; saves to local storage.
- `assets/brand/`: logo and mark as SVG and PNG, colour and reverse.

**Watch:** monthly series. When the custom domain goes live, update the hard-coded canonical and `og:` URLs in both standalone pages.

### v0.7.1 — 17 October 2026: post dates fix

**Fixed**
- The two 17 October posts were timed 09:00 and 10:00, so Jekyll treated them as future posts and left them off the site. Times moved to 00:10 and 00:20 so they publish on the next build. Note for future posts: never give a post a time later than when it's merged.

### v0.7.0 — 17 October 2026: self-hosted fonts, three puzzles, tool logos, rotating headlines, two posts

**Added**
- `assets/fonts/`: self-hosted Fraunces, Source Sans 3, Source Serif 4 and IBM Plex Mono (WOFF, Latin subset, SIL Open Font Licence files included), loaded from `assets/fonts/fonts.css`. Google Fonts links removed from the layout and every standalone page, so no page contacts a third party.
- `puzzles/scope-sort.html`: Scope Sort. 22 activities to sort into Scope 1, 2, 3 or "not counted", each with the reason.
- `puzzles/pillar-clash.html`: Pillar Clash. Ten ESG dilemmas with environmental, social and governance gauges.
- `puzzles/acronym-match.html`: Acronym Match. 33 acronyms, Core and Everything levels, six pairs per round.
- `assets/icons/`: 13 small logos, one per tool, puzzle and guide, in the same split ink-and-red style as the jigsaw mark.
- `assets/photos/`: 14 more licensed stock photos (bins collection, wind turbines, plant room, EV charging, shipping containers, net zero, forest, reuse jars, boardroom, CO2 compass, energy costs, farm panorama, packaging line, Giant's Causeway).
- `puzzles/planet-check-worksheet.pdf`: printable Planet Check worksheet, answers on separate pages; a Print button in the quiz.
- `tools/site-plans/`: six printable Land Repair Helix site plans (farm, verge, brownfield, factory, park, river); a Print site plan button in the tool.
- `_posts/2026-10-17-improving-the-public-realm.md` and `_posts/2026-10-17-offsets-are-a-scam.md`.

**Changed**
- `index.html`: four hero headlines (manufacturers; public realm guardianship; suppliers to manufacturers; public sector and trade bodies), one picked at random on each visit. Without JavaScript the manufacturers headline shows. The tools band is now a grid of logo tiles.
- `tools.md`: logo beside every entry; three new puzzles; links to the printables.
- `tools/land-repair-helix.html`: five new pairs (now 22): invasive plants, litter and fly-tipping, misconnected drains, light pollution, low soil carbon.
- Logos added to the headers of the other tools and guides.
- Photos added to `services.md`, `public-sector.md` and `about.md`.
- `tools/joined-up-wheel.html`: a "How I help" block on each issue, saying what Robert leads and where partners come in ("Led by me" means Robert is client manager and project lead; policy is delivered by Robert alone; outsourced carbon accountants, with the Qualifying Explanatory Statement (QES) verified by a UKAS-accredited verifier, for carbon; ESOS assessors and Lead Assessor sign-off for energy; multidisciplinary teams for environmental health and land; collaboration for water and waste).
- `privacy.md`: fonts are now self-hosted, so the only outside party is GitHub's hosting.

**Not used:** the school bus photo. A blurred copy is in Robert's Assets/web folder, but the image looks like a broadcast screen grab, so it stays off the site.

### v0.6.0 — 16 October 2026: privacy policy and three new tools

**Added**
- `privacy.md` at `/privacy/`, linked from every page footer. It states that the site collects no data: no analytics, no tracking, no cookies, no forms, and tool inputs stay on the visitor's device. It discloses the two third-party contacts: GitHub Pages logs IP addresses for security, and fonts load from Google. It also lists the two tools that use browser local storage (Carbon Jigsaw, Carbon Crossword) and how to clear it.
- `tools/incoterms.html`: Incoterms Chooser. Four questions lead to one of the 11 Incoterms® 2020 rules, with seller and buyer duties, warnings, copyable contract wording, a who-does-what matrix, and notes on GB–NI, NI–EU, DDP and CBAM, and Scope 3 freight.
- `puzzles/planet-check.html`: Planet Check, a 28-question GCSE quiz tagged to AQA Chemistry 4.9 and 4.10 and Biology 4.7, plus a Real world NI set. It has topic filters, explanations and a retry-missed option, and stores nothing.
- `tools/land-repair-helix.html`: The Land Repair Helix. Seventeen problem–fix base pairs across soil, water, contamination, PFAS, spills, rewilding and air, with a site-type filter, a starter plan builder and NI rules on each pair.

**Changed**
- `_layouts/default.html`: Privacy link in the footer.
- `tools.md`: added the three new tools.

**Audit (16 Oct 2026):** no analytics, tracking scripts, cookies, forms or data-sending code anywhere in the repo. External requests go only to Google Fonts. Browser storage is used only by the Carbon Jigsaw and the Carbon Crossword.

### v0.5.0 — 16 October 2026: home page tools band and photos

**Added**
- `assets/photos/`: 11 web-sized photos (max 1600 px). Five are licensed Adobe Stock images held by Robert J. Park: solar roof factory, food manufacturing, logistics and freight, warehouse, customs declaration. Six are Robert's own: LPG cylinders, NI Railways train, paint reuse container, young tree, weather station, artichoke with bee.
- Home page (`index.html`): a "Free tools and guides" band after the public sector band, linking the Carbon Jigsaw, Scopes Map, Joined-Up Wheel and both guides, illustrated with the solar roof photo.
- `assets/style.css`: styles for the tools band.
- `guides/circular-economy.html`: two photos illustrating the technical loop (paint reuse) and the biological loop (bee on artichoke).

**Changed**
- `tools/carbon-jigsaw.html`: UK CBAM flag now states the registration test correctly: £50,000 of CBAM goods over the past 12 months, or expected within the next 30 days. Iron and steel is named explicitly.

### v0.4.0 — 16 October 2026: e-waste and circular economy guides

**Added**
- `guides/e-waste.html`: E-waste Unpacked. Covers precious, critical/rare and hazardous materials; the six-stage treatment line with audit points (weighbridge, batch de-pollution tests to EN 50625, mass balance, downstream records, evidence notes); why shredders must know their input (permits, contamination, POPs plastics, evidence); the economics of reuse versus recycling and of design choices; the rules table (WEEE 2013 and 2025 amendments, POPs, RoHS, EU Battery Regulation in NI, UK Critical Minerals Strategy, EU Circular Economy Act); actions for NI businesses; and the environment-versus-social lens on exported e-waste.
- `guides/circular-economy.html`: Circular Economy Reality Check. Covers the roots of the theory (Boulding to the 9R ladder), technical and biological loops, an NI-focused scorecard by material, the barriers, a dated road ahead to 2035, the critical lens and practical steps.

**Changed**
- `tools.md`: new Guides section linking both.

**Watch:** the EU Circular Economy Act proposal (expected 11 November 2026), England's Circular Economy Growth Plan, and NI's final Circular Economy Strategy. Update both guides when these land.

### v0.3.0 — 16 October 2026: Carbon Jigsaw and Scopes Map

**Added**
- `tools/carbon-jigsaw.html`: The Carbon Jigsaw, a rough carbon checker with 12 pieces: boundary, electricity, gas, oil and LPG, vehicles, refrigerants, solar and wind, water, waste, business travel, commuting, and goods and freight (locked: needs a full inventory). It gives Scope 1, location-based Scope 2 and partial Scope 3, intensity per employee and per £1m turnover, and flags for ESOS, UK CBAM and customer requests. Everything runs in the browser and nothing is sent or stored on a server. It opens on a worked example that matches the sample bills.
- `tools/sample-bills/`: six SAMPLE bills (electricity, gas, heating oil, water and sewerage, waste, rates) from invented NI-style suppliers, with the figures the checker needs highlighted.
- `tools/scopes-map.html`: The Scopes Map. A value-chain diagram of Scope 1, Scope 2 and all 15 Scope 3 categories with GHG Protocol definitions, 15 "where the lines blur" cases (gas before and after the meter, LPG and butane, water sources, vehicles, home EV charging, refrigerants, freight, biomass, farm emissions, leased premises, welding CO₂ and SF₆, CHP exports, goods versus capital goods, flight contrails), and which gases count.
- Carbon Jigsaw water piece: asks where the water comes from (mains, borehole, rainwater, river) and where wastewater goes (sewer or on-site treatment). Only mains supply and sewer volumes take the Scope 3 water factors, and notes explain why.
- `assets/tools-mark.svg`: Tools logo, a jigsaw piece split ink/red to match the brand mark.

**Changed**
- `tools.md`: added the logo, the Carbon Jigsaw (first) and the Scopes Map.

**Factors:** UK Government GHG Conversion Factors for Company Reporting 2026 (DESNZ, published 11 June 2026). Location-based UK grid electricity 0.13096 kg CO2e/kWh and T&D 0.01299; natural gas 0.18231/kWh (gross CV); burning oil 2.54016/L. Full list in the script header. **Update every June** when DESNZ publishes the new set.

### v0.2.0 — 16 October 2026: interactive tools

**Added**
- `tools/joined-up-wheel.html`: The Joined-Up Wheel. Eight environmental issues around six business goals, showing triggers, current rules, routes in and overlaps. Deep links work, e.g. `/tools/joined-up-wheel.html#pfas` or `#tenders`.
- `tools/esg-regime-tracker.html`: ESG Regime Tracker. Shows regulation then (2023) and now (2026) by market, with filters for NI manufacturers and for councils/public bodies.
- `puzzles/carbon-crossword.html`: The Carbon Crossword. 24 terms with easy and hard clues and a UK/NI lean. The Print button prints the grid and clues, with answers on page 2.
- `tools.md`: the Tools page at `/tools/`, listing all three.
- `_snippets/embed.html`: link and iframe snippets for using the tools in blog posts.
- `WEBSITE-UPDATES.md`: this file.

**Changed**
- `_layouts/default.html`: added **Tools** to the main navigation, between Public sector and About.
- `_config.yml`: excluded `WEBSITE-UPDATES.md` from the public site.

**Facts as at:** 16 October 2026, shown in each tool's footer.

### v0.1.0 — 15–16 October 2026: launch

- Site launched on GitHub Pages with Home, Services, Public sector, About, Blog and Contact.
- First seven blog posts published.

---

## Backlog

### Waiting on Robert
- [ ] Merge pull request #5 (v0.7.0)
- [ ] Register the domain (e.g. robertjpark.co.uk), add it under Settings → Pages, set `url:` in `_config.yml`, tick Enforce HTTPS
- [x] Wheel "How I help" lines agreed and added (17 Oct 2026)
- [ ] Ask NIEA to confirm its position on POPs in WEEE plastics
- [ ] Planet Check: ask a GCSE science or geography teacher to sense-check the questions against CCEA specifications
- [ ] Read the two new posts and the NED one-pager for voice and accuracy, especially the Public Realm Bill figures
- [x] Carbon Jigsaw assumptions confirmed (17 Oct 2026)
- [x] Stock images kept downloaded and reviewed (17 Oct 2026)

### Ready to build next
- [ ] Blog posts launching the Carbon Jigsaw, Scopes Map, Incoterms Chooser, Land Repair Helix, puzzles and guides
- [ ] Printable versions of Scope Sort and Acronym Match for workshops
- [ ] Social share images (Open Graph) for posts and tools
- [ ] WOFF2 fonts (smaller files) when a converter is available

### Later
- [ ] Carbon Jigsaw phase 2: bill upload with automatic reading (needs a back end; not possible on GitHub Pages alone)
- [ ] Replace the Carbon Jigsaw's 2026 factors when DESNZ publishes the 2027 set (June 2027)

### Watch list (update pages when these land)
- [ ] EU Circular Economy Act proposal, expected 11 November 2026: e-waste and circular economy guides
- [ ] EU Parliament plenary vote on car CO2 standards, 23 November 2026: ESG Regime Tracker
- [ ] SEAC final opinion on the EU universal PFAS restriction, expected end of 2026: Joined-Up Wheel, Land Repair Helix
- [ ] England's Circular Economy Growth Plan and NI's final Circular Economy Strategy: circular economy guide
- [ ] NI final Climate Action Plan: tracker and wheel
- [ ] GHG Protocol Scope 2 revision (consultation closed 31 January 2026): Scopes Map
- [ ] UK CBAM go-live, 1 January 2027: tracker, jigsaw, Incoterms Chooser, NI manufacturers card
- [ ] New Nutrients Action Programme rules: Land Repair Helix
- [ ] Any new edition of the Incoterms rules from the ICC: Incoterms Chooser

## Fact-check rule

Cite primary and official sources only: legislation, DAERA, NIEA, HMRC, Defra, the European Commission, ECHA and the NI Assembly. Do not cite energy broker websites.
