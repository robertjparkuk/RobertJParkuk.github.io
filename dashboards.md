---
layout: default
title: Dashboards
permalink: /dashboards/
description: Free dashboards of Northern Ireland environmental, carbon, trade and consultation data, drawn from official statistics, with every table downloadable as CSV.
lead: Northern Ireland environmental, carbon, trade and consultation data, one dashboard per subject, drawn from official statistics. Each is a dated snapshot. Figures are worked out in your browser and every table can be downloaded as CSV.
---
{%- assign count = 0 -%}
{%- for g in site.data.dashboards -%}{%- assign count = count | plus: g.items.size -%}{%- endfor -%}
<div class="wrap page">
  <h1 class="page-title">{{ page.title }}</h1>
  <p class="lead">{{ page.lead }}</p>
  <p class="dash-count">{{ count }} dashboards, free to use. Click a picture or a title to open one.</p>
  {%- for g in site.data.dashboards %}
  <section class="dash-group" aria-labelledby="dg-{{ forloop.index }}">
    <h2 id="dg-{{ forloop.index }}">{{ g.group }}</h2>
    <p class="dash-intro">{{ g.intro }}</p>
    {%- assign n = g.items.size | modulo: 3 -%}
    <ul class="dash-grid{% if n != 0 %} dash-grid--2{% endif %}">
      {%- for d in g.items %}
      <li class="dash-card">
        <a class="dash-thumb" href="{{ d.page | relative_url }}" tabindex="-1" aria-hidden="true"><img src="{{ d.thumb | relative_url }}" alt="" width="640" height="400" loading="lazy"></a>
        <div class="dash-body">
          <h3><a href="{{ d.page | relative_url }}">{{ d.title }}</a></h3>
          <p>{{ d.summary }}</p>
          <p class="dash-meta">{{ d.as_at }}</p>
          <p class="dash-links"><a href="{{ d.page | relative_url }}">Open the dashboard →</a>{% if d.related %}<br><span>Related: <a href="{{ d.related | relative_url }}">{{ d.related_title }}</a></span>{% endif %}</p>
        </div>
      </li>
      {%- endfor %}
    </ul>
  </section>
  {%- endfor %}
  <p class="dash-foot">More dashboards follow alongside each monthly <em>Focus on</em> briefing. Looking for interactive tools such as the Scopes Map or the UK CBAM Countdown? See <a href="{{ '/tools/' | relative_url }}">Tools</a>.</p>
</div>
