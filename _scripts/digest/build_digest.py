#!/usr/bin/env python3
"""Weekly regulatory digest, one edition per sector.

Reads the NI Regulatory Horizon and NI Consultations Monitor data, picks what is
coming up for each sector, and asks Claude to write a short, plain-English digest
from those facts only. Every date, link and source comes from the data, not from
Claude. Any sentence from Claude that contains a number not found in the source
item is replaced with the source text.

Writes _digest/YYYY-MM-DD-<sector>.md and digest/<sector>.xml (the feed, once).

Usage:  ANTHROPIC_API_KEY=... python3 _scripts/digest/build_digest.py [--date 2026-11-20] [--dry-run]
        --dry-run writes editions from the source text alone, without calling Claude.
"""
import argparse, calendar, datetime as dt, json, os, re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HORIZON = ROOT / "data/dashboards/ni-regulatory-horizon/horizon.json"
CONSULT = ROOT / "data/dashboards/ni-consultations/consultations.json"
SECTORS = ROOT / "_data/digest_sectors.json"
DASHES = ROOT / "_data/dashboards.yml"
OUT = ROOT / "_digest"
FEEDS = ROOT / "digest"
MODEL = os.environ.get("DIGEST_MODEL", "claude-sonnet-5-5")
AHEAD_DAYS, CONSULT_DAYS = 120, 60
MAX_ITEMS, MAX_CONSULT = 6, 5

def parse_day(s, end=False):
    """'2026-11-20' -> date; '2026-11' -> first (or last) day of the month."""
    if len(s) == 10:
        return dt.date.fromisoformat(s)
    y, m = map(int, s[:7].split("-"))
    return dt.date(y, m, calendar.monthrange(y, m)[1] if end else 1)

def nice(s):
    d = parse_day(s)
    return f"{d.day} {d:%B %Y}" if len(s) == 10 else f"{d:%B %Y}"

def as_at(title):
    try:
        import yaml
        for g in yaml.safe_load(DASHES.read_text(encoding="utf-8")):
            for it in g.get("items", []):
                if it.get("title") == title:
                    return it.get("as_at", "")
    except Exception:
        pass
    return ""

def horizon_for(sector, items, today):
    lo, hi = today, today + dt.timedelta(days=AHEAD_DAYS)
    want = set(sector["horizon"]) | {"All businesses"}
    out = [r for r in items
           if want & set(r.get("sectors", []))
           and parse_day(r["date"], end=True) >= lo and parse_day(r["date"]) <= hi]
    return sorted(out, key=lambda r: parse_day(r["date"]))[:15]

def consult_for(sector, items, today):
    hi = today + dt.timedelta(days=CONSULT_DAYS)
    want = {t.lower() for t in sector["topics"]}
    out = []
    for c in items:
        if c.get("status") not in ("open", "upcoming"):
            continue
        topics = {t.strip().lower() for t in c.get("topics", "").split(";")}
        if not want & topics:
            continue
        closes = c.get("closes") or ""
        if closes and not (today <= dt.date.fromisoformat(closes) <= hi):
            continue
        out.append(c)
    return sorted(out, key=lambda c: c.get("closes") or "9999")[:20]

TOOL = {
    "name": "write_digest",
    "description": "Write this week's sector digest from the supplied items only.",
    "input_schema": {
        "type": "object",
        "properties": {
            "intro": {"type": "string", "description": "Two or three plain sentences on what matters most this week for this sector. No numbers or dates."},
            "items": {"type": "array", "maxItems": MAX_ITEMS, "items": {"type": "object", "properties": {
                "id": {"type": "string"},
                "headline": {"type": "string", "description": "Up to 12 words."},
                "why": {"type": "string", "description": "Up to 40 words: why it matters to this sector."},
                "action": {"type": "string", "description": "Up to 30 words: what to do now."}},
                "required": ["id", "headline", "why", "action"]}},
            "consultations": {"type": "array", "maxItems": MAX_CONSULT, "items": {"type": "object", "properties": {
                "id": {"type": "string"},
                "why": {"type": "string", "description": "Up to 25 words: why this sector might respond."}},
                "required": ["id", "why"]}}
        },
        "required": ["intro", "items", "consultations"]
    }
}

PROMPT = """You write a short weekly regulatory digest for {name} in Northern Ireland, for Robert J. Park, an independent environmental and carbon consultant.

Use only the facts in the items below. Do not add dates, figures, deadlines, laws or claims that are not in them. Choose up to {mi} items that matter most to this sector, most urgent first, and up to {mc} consultations a business in this sector might want to answer (none if none fit).

Style: plain British English, short sentences, active voice, no hype, no exclamation marks, no em dashes. Address the reader as "you". Say what to do in practical terms.

Sector: {name}. {blurb}

Items (JSON):
{items}

Consultations (JSON):
{consults}"""

def call_claude(prompt):
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps({"model": MODEL, "max_tokens": 2000, "tools": [TOOL],
                         "tool_choice": {"type": "tool", "name": TOOL["name"]},
                         "messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01",
                 "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        out = json.load(r)
    for c in out.get("content", []):
        if c.get("type") == "tool_use":
            return c["input"]
    raise RuntimeError("No digest returned")

NUM = re.compile(r"\d[\d,.]*")
def nums(s):
    return {n.strip(".,").replace(",", "") for n in NUM.findall(s or "")}

def safe(text, source):
    """Keep Claude's sentence only if every number in it appears in the source."""
    return text if nums(text) <= nums(source) else None

def build(sector, h_items, c_items, today, dry):
    h_by, c_by = {r["id"]: r for r in h_items}, {c["id"]: c for c in c_items}
    if dry:
        res = {"intro": "", "items": [{"id": r["id"], "headline": r["title"], "why": r["detail"], "action": r["action"]} for r in h_items[:MAX_ITEMS]],
               "consultations": [{"id": c["id"], "why": c.get("summary", "")} for c in c_items[:MAX_CONSULT]]}
    else:
        slim_h = [{k: r.get(k) for k in ("id", "date", "title", "detail", "status", "kind", "jurisdiction", "action")} for r in h_items]
        slim_c = [{k: c.get(k) for k in ("id", "body", "title", "closes", "summary", "topics")} for c in c_items]
        res = call_claude(PROMPT.format(name=sector["name"], blurb=sector["blurb"], mi=MAX_ITEMS, mc=MAX_CONSULT,
                                        items=json.dumps(slim_h, ensure_ascii=False), consults=json.dumps(slim_c, ensure_ascii=False)))
    picked, seen = [], set()
    for it in res.get("items", []):
        r = h_by.get(it.get("id"))
        if not r or r["id"] in seen:
            continue
        seen.add(r["id"])
        src = " ".join(str(r.get(k, "")) for k in ("date", "title", "detail", "action", "kind", "jurisdiction"))
        picked.append({"r": r,
                       "headline": safe(it.get("headline", ""), src) or r["title"],
                       "why": safe(it.get("why", ""), src) or r["detail"],
                       "action": safe(it.get("action", ""), src) or r["action"]})
    cons = []
    for it in res.get("consultations", []):
        c = c_by.get(it.get("id"))
        if c and c["id"] not in {x["c"]["id"] for x in cons}:
            src = " ".join(str(c.get(k, "")) for k in ("title", "summary", "closes", "body"))
            cons.append({"c": c, "why": safe(it.get("why", ""), src) or c.get("summary", "")})
    intro = res.get("intro", "")
    if nums(intro):
        intro = ""
    return intro.strip(), picked, cons

def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)

def render(sector, today, intro, picked, cons, h_asat, c_asat):
    day = f"{today.day} {today:%B %Y}"
    title = f"{sector['name']}: weekly digest, {day}"
    desc = f"What's coming up for {sector['name'].lower()} in Northern Ireland: rule changes, deadlines and consultations, week of {day}."
    L = ["---", "layout: digest", f"title: {yaml_str(title)}", f"description: {yaml_str(desc)}",
         f"sector: {sector['slug']}", f"sector_name: {yaml_str(sector['name'])}", f"date: {today.isoformat()} 16:00:00 +0000",
         f"data_as_at: {yaml_str(h_asat)}", "---", ""]
    if intro:
        L += [intro, ""]
    if picked:
        L += ["## Coming up", ""]
        for p in picked:
            r = p["r"]
            status = {"confirmed": "Confirmed", "expected": "Expected", "proposed": "Proposed", "in force": "In force"}.get(r.get("status"), r.get("status", "").capitalize())
            L += [f"### {p['headline']}", "",
                  f"**{nice(r['date'])}** · {status} · {r.get('jurisdiction', '')}", "",
                  p["why"], "",
                  f"**What to do:** {p['action']}", "",
                  f"Source: [{r['source_title']}]({r['source_url']})" + (f" · Related: [{r['related_title']}]({r['related']})" if r.get("related") else ""), ""]
    if cons:
        L += ["## Consultations you could answer", ""]
        for x in cons:
            c = x["c"]
            closes = f"closes {nice(c['closes'])}" if c.get("closes") else "no closing date given"
            L += [f"- **[{c['title']}]({c['url']})** ({c.get('body_short') or c['body']}, {closes}). {x['why']}"]
        L += [""]
    if not picked and not cons:
        L += ["Nothing new in my trackers for this sector over the next four months. That can change quickly, so check the [Regulatory Horizon](/tools/dashboards/ni-regulatory-horizon.html).", ""]
    return "\n".join(L)

FEED = """---
layout: null
permalink: /digest/{slug}.xml
sector: {slug}
---
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{{{{ site.title | xml_escape }}}}: {name} weekly digest</title>
  <link>{{{{ '/digest/' | absolute_url }}}}</link>
  <atom:link href="{{{{ page.url | absolute_url }}}}" rel="self" type="application/rss+xml"/>
  <description>{blurb}</description>
  <language>en-gb</language>
  {{%- assign eds = site.digest | where: "sector", page.sector | sort: "date" | reverse -%}}
  {{%- for e in eds limit: 12 %}}
  <item>
    <title>{{{{ e.title | xml_escape }}}}</title>
    <link>{{{{ e.url | absolute_url }}}}</link>
    <guid isPermaLink="true">{{{{ e.url | absolute_url }}}}</guid>
    <pubDate>{{{{ e.date | date_to_rfc822 }}}}</pubDate>
    <description>{{{{ e.content | xml_escape }}}}</description>
  </item>
  {{%- endfor %}}
</channel>
</rss>
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    today = dt.date.fromisoformat(a.date) if a.date else dt.date.today()
    if not a.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set")
    horizon = json.loads(HORIZON.read_text(encoding="utf-8"))
    consults = json.loads(CONSULT.read_text(encoding="utf-8"))
    sectors = json.loads(SECTORS.read_text(encoding="utf-8"))
    h_asat, c_asat = as_at("NI Regulatory Horizon"), as_at("NI Consultations Monitor")
    OUT.mkdir(exist_ok=True); FEEDS.mkdir(exist_ok=True)
    written = []
    for s in sectors:
        feed = FEEDS / f"{s['slug']}.xml"
        if not feed.exists():
            feed.write_text(FEED.format(slug=s["slug"], name=s["name"], blurb=s["blurb"]), encoding="utf-8")
        h, c = horizon_for(s, horizon, today), consult_for(s, consults, today)
        if not h and not c:
            print(f"{s['slug']}: nothing to report, skipped"); continue
        intro, picked, cons = build(s, h, c, today, a.dry_run)
        path = OUT / f"{today.isoformat()}-{s['slug']}.md"
        path.write_text(render(s, today, intro, picked, cons, h_asat, c_asat), encoding="utf-8")
        written.append(path.name)
        print(f"{s['slug']}: {len(picked)} items, {len(cons)} consultations -> {path.relative_to(ROOT)}")
    print(f"{len(written)} editions written")

if __name__ == "__main__":
    main()
