---
layout: page
title: Learn
permalink: /learn/
lead: Plain-English explainers on carbon, from the terms people mix up to the rules that put a price on them. Each one has a diagram, worked examples from different sectors, and the standards and laws behind it, with the date they were last checked.
description: "Plain-English carbon explainers for Northern Ireland businesses, councils and students: embodied carbon, life cycles, greenhouse gases, hydrogen, carbon capture, fertiliser and nitrogen, offsets, and the rules behind them."
---

## Explainers

{% assign theme_order = "Carbon basics|Energy and industry|Land, food and water|Materials and buildings|Claims, credits and markets|Is it true?" | split: "|" %}
{% assign items = site.learn | sort: "order" %}
{% for theme in theme_order %}
{% assign in_theme = items | where: "theme", theme %}
{% if in_theme.size > 0 %}
<h3 class="learn-theme">{{ theme }}</h3>
<ul class="learn-list">
{% for item in in_theme %}
  <li>
    <h4><a href="{{ item.url | relative_url }}">{{ item.title }}</a></h4>
    <p>{{ item.answer }}</p>
    {% if item.level or item.read_time %}<p class="small">{{ item.level }}{% if item.level and item.read_time %} · {% endif %}{% if item.read_time %}{{ item.read_time }} read{% endif %}</p>{% endif %}
  </li>
{% endfor %}
</ul>
{% endif %}
{% endfor %}

More explainers are on the way. If there is a term you keep meeting and want explained, [tell me]({{ '/contact/' | relative_url }}).

## Practise

Test yourself once you have read the explainers. All of these run in your browser and store nothing.

- [Scope Sort]({{ '/puzzles/scope-sort.html' | relative_url }}): sort 22 everyday activities into Scope 1, 2, 3 or "not counted".
- [The Carbon Crossword]({{ '/puzzles/carbon-crossword.html' | relative_url }}): 24 carbon terms with easy and hard clues.
- [Acronym Match]({{ '/puzzles/acronym-match.html' | relative_url }}): 33 acronyms, from CBAM to SBTi.
- [Pillar Clash]({{ '/puzzles/pillar-clash.html' | relative_url }}): ten dilemmas where environmental, social and governance goals pull apart.
- [Planet Check]({{ '/puzzles/planet-check.html' | relative_url }}): a 28-question GCSE quiz, with a [printable worksheet (PDF)]({{ '/puzzles/planet-check-worksheet.pdf' | relative_url }}).

## Go further

- [The Scopes Map]({{ '/tools/scopes-map.html' | relative_url }}): Scope 1, 2 and 3 on one diagram, with all fifteen Scope 3 categories.
- [Is my part or chemical a CBAM good?]({{ '/cbam-desk/is-it-a-cbam-good/' | relative_url }}): the commodity codes that most often catch NI manufacturers.
- [All tools]({{ '/tools/' | relative_url }}) and [dashboards]({{ '/dashboards/' | relative_url }}).
