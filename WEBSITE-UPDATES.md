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

- [ ] Point the custom domain at GitHub Pages, set `url:` in `_config.yml`, and tick Enforce HTTPS
- [ ] Add a "Free tools" band to the home page linking to `/tools/`
- [ ] Wheel: decide which routes in are your own services and which go to partners, then add a "How I help" line to each issue
- [ ] Puzzles: Scope Sort, Pillar Clash, acronym match-up
- [ ] Blog post introducing the wheel, embedding it with the snippet in `_snippets/embed.html`
- [ ] Watch: EU Parliament vote on car CO2 standards, 23 November 2026; update the tracker
- [ ] Watch: SEAC final opinion on the EU universal PFAS restriction (expected end of 2026); update the wheel
- [ ] Watch: NI final Climate Action Plan; update the tracker and wheel

## Fact-check rule

Cite primary and official sources only: legislation, DAERA, NIEA, HMRC, Defra, the European Commission, ECHA and the NI Assembly. Do not cite energy broker websites.
