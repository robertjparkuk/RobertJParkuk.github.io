---
layout: page
title: "The law on every element"
permalink: /learn/elements/law/
lead: "For each of the 118 elements: where it comes from, how it must be handled, how it forms compounds, and its effects on climate, carbon and the environment, with the law on each in Northern Ireland."
description: "A legal briefing on each chemical element for Northern Ireland: mineral rights, REACH and CLP, COSHH, transport, compounds law, water and air standards, waste, UK ETS and UK CBAM, with the Windsor Framework position."
---

Northern Ireland sits across two systems. Under the Windsor Framework, EU rules on chemicals and products, such as REACH, CLP, persistent organic pollutants, F-gases, mercury, batteries and RoHS, apply here, while GB follows the UK versions. Workplace, transport, planning and environmental law is mostly Northern Ireland's own. UK CBAM applies in Northern Ireland from 1 January 2027; EU CBAM does not.

These are research notes as at 22 November 2026, not legal advice. Each briefing lists its sources and anything not yet verified. Always work from the supplier's safety data sheet, and for any customs or commodity-code question a customs specialist is needed. Corrections are welcome: [robert@robertjpark.co.uk](mailto:robert@robertjpark.co.uk?subject=Element%20law%3A%20correction).

<nav class="element-law-index" aria-label="Elements"><p>{% assign els = site.data.element_law %}{% for e in els %}<a href="#{{ e[0] | downcase }}">{{ e[0] }}</a>{% unless forloop.last %} · {% endunless %}{% endfor %}</p></nav>

{% for e in els %}{% assign sym = e[0] %}{% assign law = e[1] %}{% assign deep = site.pages | where: "element", sym | first %}
<section class="element-law" id="{{ sym | downcase }}" aria-labelledby="h-{{ sym | downcase }}">
<h2 id="h-{{ sym | downcase }}">{{ law.z }}. {{ law.name }} ({{ sym }})</h2>
{% if deep %}<p><a href="{{ deep.url | relative_url }}">The {{ law.name | downcase }} deep dive</a> · <a href="{{ '/tools/periodic-table.html#' | append: sym | downcase | relative_url }}">In the periodic table</a></p>{% else %}<p><a href="{{ '/tools/periodic-table.html#' | append: sym | downcase | relative_url }}">{{ law.name }} in the periodic table</a></p>{% endif %}
{{ law.html }}
</section>
{% endfor %}

*General information as at 22 November 2026, not legal, safety or customs advice. Created with assistive technology including AI and re-checked against the official sources listed.*
