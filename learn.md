---
layout: page
title: Learn
permalink: /learn/
lead: Plain-English explainers on carbon, from the terms people mix up to the rules that put a price on them. Each one has a diagram, worked examples from different sectors, and the standards and laws behind it, with the date they were last checked.
description: "Plain-English carbon explainers for Northern Ireland businesses, councils and students: embodied carbon, life cycles, greenhouse gases, hydrogen, carbon capture, fertiliser and nitrogen, offsets, the rules behind them, and an interactive periodic table of every element."
---

## The elements

<figure class="learn-figure"><a href="{{ '/tools/periodic-table.html' | relative_url }}"><img src="{{ '/assets/learn/periodic-table.svg' | relative_url }}" alt="The full periodic table of 118 elements, coloured by type, with phosphorus, nitrogen, sulfur, fluorine, antimony, magnesium, carbon and radon outlined in red" loading="lazy"></a><figcaption>Click the table to open the interactive version.</figcaption></figure>

The [interactive periodic table]({{ '/tools/periodic-table.html' | relative_url }}) has a short briefing on all 118 elements, from hydrogen to oganesson. Hover over an element for what it means for climate, greenhouse gases, the air, land, soil, water and health. Click it for where it occurs in nature, its part in pollution, how it is made and used, its health effects and hazards, and how it was discovered.

Eight elements have a full briefing of their own, with safety and COSHH notes, UN numbers and the compounds you meet in nature, manufacturing and the climate. Download them as PDFs:

- [Phosphorus]({{ '/assets/briefings/elements/phosphorus-briefing.pdf' | relative_url }}): the nutrient behind Lough Neagh's algal blooms
- [Nitrogen]({{ '/assets/briefings/elements/nitrogen-briefing.pdf' | relative_url }}): ammonia, nitrate and nitrous oxide
- [Sulfur]({{ '/assets/briefings/elements/sulfur-briefing.pdf' | relative_url }}): from acid rain to crop nutrient and slurry gas
- [Fluorine]({{ '/assets/briefings/elements/fluorine-briefing.pdf' | relative_url }}): F-gases, PFAS and fluoride
- [Antimony]({{ '/assets/briefings/elements/antimony-briefing.pdf' | relative_url }}): the critical mineral nobody has heard of
- [Magnesium]({{ '/assets/briefings/elements/magnesium-briefing.pdf' | relative_url }}): chlorophyll, grass tetany and rock weathering
- [Carbon]({{ '/assets/briefings/elements/carbon-briefing.pdf' | relative_url }}): the element we count
- [Radon]({{ '/assets/briefings/elements/radon-briefing.pdf' | relative_url }}): the gas from the ground a tighter house can trap

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

- [The interactive periodic table]({{ '/tools/periodic-table.html' | relative_url }}): every element, with its environmental, engineering, geological, chemical and land context.
- [The Scopes Map]({{ '/tools/scopes-map.html' | relative_url }}): Scope 1, 2 and 3 on one diagram, with all fifteen Scope 3 categories.
- [Is my part or chemical a CBAM good?]({{ '/cbam-desk/is-it-a-cbam-good/' | relative_url }}): the commodity codes that most often catch NI manufacturers.
- [All tools]({{ '/tools/' | relative_url }}) and [dashboards]({{ '/dashboards/' | relative_url }}).
