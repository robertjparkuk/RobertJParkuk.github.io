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
