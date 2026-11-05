---
layout: page
title: Policy series
permalink: /policy-series/
description: Seventeen pieces on where environmental, carbon, energy and waste rules stand in Northern Ireland, who decides them, where the parties stand, and what firms and councils should do. Thirteen published on 2 November 2026; four more to follow.
lead: Where the rules stand in Northern Ireland, who decides them, where the parties stand, and what to do about it. Thirteen pieces are live; four more follow once their facts are rechecked.
---

Northern Ireland sits between two rulebooks. Some rules are made in Brussels and reach us through the Windsor Framework. Some are made at Westminster and apply UK-wide. Some are Stormont's alone, and some of those have never been switched on. The result is that a manufacturer in Craigavon, a council in Fermanagh or a farm in Antrim can be living under three regimes at once, with nobody setting out how they fit together.

This series takes one subject at a time. Each piece follows the same shape: the argument in brief, what changed between 2023 and now, where every party and government stands, who actually decides, where the environmental, social and economic aims pull against each other, what it means for firms and councils in Northern Ireland, worked examples, and the author's recommendations. Every claim carries a dated source, and each piece ends with the positions I could not find, so you can see the gaps as well as the evidence.

The pieces set out the arguments on each side. The recommendations are mine. They are written to be useful to anyone making or influencing these decisions, whichever side they come from, and I update them as the rules change.

{% assign pieces = site.categories['policy-series'] %}
{% if pieces and pieces.size > 0 %}
{% assign pieces = pieces | sort: 'date' %}
{% assign themes = pieces | map: 'series_theme' | uniq %}
{% for theme in themes %}
## {{ theme }}
<ul class="post-list">
  {% for p in pieces %}{% if p.series_theme == theme %}
  <li>
    <p class="meta"><time datetime="{{ p.date | date_to_xmlschema }}">{{ p.date | date: '%-d %B %Y' }}</time></p>
    <h3><a href="{{ p.url | relative_url }}">{{ p.title }}</a></h3>
    <p>{{ p.description }}</p>
  </li>
  {% endif %}{% endfor %}
</ul>
{% endfor %}
{% else %}
<p>Thirteen pieces published on 2 November 2026; four more follow as the rules settle.</p>
{% endif %}

## What is coming

Six themes, seventeen pieces, thirteen of them live and four to follow between late November 2026 and January 2027: reporting and finance; energy; carbon pricing and trade; waste and resources; chemicals, land and water; and climate law. Each piece is checked against its sources in the week before it publishes, and updated afterwards when the rules move.

## Use them

The pieces are free to read and share for non-commercial purposes. If you want one adapted for a board paper, a committee submission or a member briefing, or you want the same treatment of a subject that is not covered, [get in touch]({{ '/contact/' | relative_url }}).
