---
layout: default
title: Tools
permalink: /tools/
description: "Free, private carbon and environmental tools for NI businesses and councils: Carbon Jigsaw, Scopes Map, CBAM tools, farm data checker, puzzles and guides."
lead: Free, interactive tools for Northern Ireland businesses, councils and anyone working on carbon and environmental compliance. Everything runs in your browser and nothing you type is stored on a server.
---
{%- assign count = 0 -%}
{%- for g in site.data.tools -%}{%- assign count = count | plus: g.items.size -%}{%- endfor -%}
<div class="wrap page">
  <h1 class="page-title">{{ page.title }}</h1>
  <p class="lead">{{ page.lead }}</p>
  <p class="dash-count">{{ count }} tools, puzzles and guides, free to use. Click a picture or a title to open one. New to carbon? Start with the plain-English explainers in <a href="{{ '/learn/' | relative_url }}">Learn</a>.</p>
  {%- for g in site.data.tools %}
  <section class="dash-group" aria-labelledby="tg-{{ forloop.index }}">
    <h2 id="tg-{{ forloop.index }}">{{ g.group }}</h2>
    <p class="dash-intro">{{ g.intro }}</p>
    {%- assign n = g.items.size | modulo: 3 -%}
    <ul class="dash-grid{% if n != 0 %} dash-grid--2{% endif %}">
      {%- for d in g.items %}
      <li class="dash-card">
        <a class="dash-thumb" href="{{ d.page | relative_url }}" tabindex="-1" aria-hidden="true"><img src="{{ d.thumb | relative_url }}" alt="" width="640" height="400" loading="lazy"></a>
        <div class="dash-body">
          <h3><a href="{{ d.page | relative_url }}">{{ d.title }}</a></h3>
          <p>{{ d.summary }}</p>
          <p class="dash-meta">{{ d.meta }}</p>
          <p class="dash-links"><a href="{{ d.page | relative_url }}">{{ d.cta }} →</a>{% if d.extra %}<br><span>{{ d.extra_label | default: "Also" }}: {% for x in d.extra %}<a href="{{ x.url | relative_url }}">{{ x.title }}</a>{% unless forloop.last %} · {% endunless %}{% endfor %}</span>{% endif %}</p>
        </div>
      </li>
      {%- endfor %}
    </ul>
  </section>
  {%- endfor %}
  <p class="dash-foot">These tools are for general information and are not legal or tax advice. If you'd like to talk through what any of this means for your business or organisation, <a href="{{ '/contact/' | relative_url }}">get in touch</a>.</p>
</div>
