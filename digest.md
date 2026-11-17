---
layout: page
title: Weekly digest
permalink: /digest/
lead: Every Friday, a short briefing for your sector on the Northern Ireland rule changes, deadlines and consultations coming up in the next four months, with what to do about each.
description: "A free weekly briefing for NI manufacturers, importers, food and drink, farming, construction, retail, councils and energy users: rule changes, deadlines and consultations."
---

Each digest is drawn from my [NI Regulatory Horizon]({{ '/tools/dashboards/ni-regulatory-horizon.html' | relative_url }}) and [NI Consultations Monitor]({{ '/tools/dashboards/ni-consultations-monitor.html' | relative_url }}). Every date and source comes from those trackers.

{% if site.digest_signup_url and site.digest_signup_url != "" -%}
**[Sign up to get your sector's digest by email]({{ site.digest_signup_url }}).** You can also follow any sector's feed in a news reader.
{%- else -%}
Follow your sector's feed in any news reader (Feedly, Inoreader, Outlook or your phone's news app) and each Friday's digest arrives on its own.
{%- endif %}

{% for s in site.data.digest_sectors %}
{%- assign eds = site.digest | where: "sector", s.slug | sort: "date" | reverse -%}
## {{ s.name }}

{{ s.blurb }}

{% if eds.size > 0 -%}
**Latest:** [{{ eds[0].date | date: '%-d %B %Y' }}]({{ eds[0].url | relative_url }}){% if eds.size > 1 %} · Earlier: {% for e in eds offset: 1 limit: 3 %}[{{ e.date | date: '%-d %B' }}]({{ e.url | relative_url }}){% unless forloop.last %}, {% endunless %}{% endfor %}{% endif %} · [Feed]({{ '/digest/' | append: s.slug | append: '.xml' | relative_url }})
{%- else -%}
First edition on Friday. [Feed]({{ '/digest/' | append: s.slug | append: '.xml' | relative_url }})
{%- endif %}

{% endfor %}
