---
layout: page
title: Consultation responses
permalink: /public-sector/consultation-responses/
lead: A selection of my responses to public consultations by Stormont departments, councils and the UK Government, published once each consultation has closed.
---

Responding to consultations is a large part of public affairs work. I publish a selection of my own responses here so that clients, officials and elected representatives can see the arguments I make and the evidence behind them. Each entry gives the consulting body, the closing date, a short summary and the full response as a PDF. I add the consulting body's outcome when it is published.

These are my personal responses, made as an individual. They are not written for or endorsed by the consulting body, and they do not represent any client.

{% assign responses = site.categories['consultation-responses'] %}
{% if responses and responses.size > 0 %}
<ul class="post-list">
  {% for r in responses %}
  <li>
    <p class="meta">{{ r.consulting_body }} · closed {{ r.closed | date: '%-d %B %Y' }} · outcome: {{ r.outcome | default: 'awaited' }}</p>
    <h2><a href="{{ r.url | relative_url }}">{{ r.title }}</a></h2>
    <p>{{ r.excerpt | strip_html | truncatewords: 40 }}</p>
  </li>
  {% endfor %}
</ul>
{% else %}
<p>The first responses will appear here shortly.</p>
{% endif %}

## Help with your own response

If your business, council or trade body wants to respond to a consultation, I can help gather the evidence, draft the response and follow it up with officials. [Get in touch]({{ '/contact/' | relative_url }}).
