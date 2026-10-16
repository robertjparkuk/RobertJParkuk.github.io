# Website updates

This file logs every change to the Robert J. Park website. It lives in the root of the repo and is kept off the public site by `_config.yml`. Add a new entry at the top each time something goes live.

- **Repo:** https://github.com/robertjparkuk/RobertJParkuk.github.io (Jekyll on GitHub Pages, branch `main`, folder `/`)
- **Live address:** https://robertjparkuk.github.io (custom domain to follow)
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
- [ ] Merge pull requests #1 (v0.3.0), #2 (v0.4.0) and #3 (v0.5.0), in that order. Each merge goes live within a couple of minutes.
- [ ] Register the domain (e.g. robertjpark.co.uk), add it under Settings → Pages, set `url:` in `_config.yml`, tick Enforce HTTPS
- [ ] Wheel: decide which routes in are your own services and which go to partners; then add a "How I help" line to each issue
- [ ] Carbon Jigsaw: confirm the flight distance and commuting assumptions (1,040 / 2,000 / 11,000 km return; 46 working weeks)
- [ ] Ask NIEA to confirm its position on POPs in WEEE plastics (the e-waste guide currently cites regulator guidance generally)
- [ ] Mark the remaining 62 stock images "Keep Downloaded" in iCloud so they can be reviewed
- [ ] Blur or crop the school bus number plate, or drop that photo

### Ready to build next
- [ ] Puzzles: Scope Sort, Pillar Clash, acronym match-up
- [ ] Blog posts introducing the Carbon Jigsaw, Scopes Map and e-waste guide, embedding them with `_snippets/embed.html`
- [ ] Add photos to the services and public sector pages
- [ ] A Tools index card image for each tool

### Later
- [ ] Carbon Jigsaw phase 2: bill upload with automatic reading (needs a back end; not possible on GitHub Pages alone)
- [ ] Replace the Carbon Jigsaw's 2026 factors when DESNZ publishes the 2027 set (June 2027)

### Watch list (update pages when these land)
- [ ] EU Circular Economy Act proposal, expected 11 November 2026: e-waste and circular economy guides
- [ ] EU Parliament plenary vote on car CO2 standards, 23 November 2026: ESG Regime Tracker
- [ ] SEAC final opinion on the EU universal PFAS restriction, expected end of 2026: Joined-Up Wheel
- [ ] England's Circular Economy Growth Plan and NI's final Circular Economy Strategy: circular economy guide
- [ ] NI final Climate Action Plan: tracker and wheel
- [ ] GHG Protocol Scope 2 revision (consultation closed 31 January 2026): Scopes Map
- [ ] UK CBAM go-live, 1 January 2027: tracker, jigsaw, NI manufacturers card

## Fact-check rule

Cite primary and official sources only: legislation, DAERA, NIEA, HMRC, Defra, the European Commission, ECHA and the NI Assembly. Do not cite energy broker websites.
