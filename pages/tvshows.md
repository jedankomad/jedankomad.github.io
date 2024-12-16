---
layout: page
title: TV Shows
subtitle: 20 years in the can
permalink: /tvshows/
---

## Currently watching
<ol>
{% for tvshow in site.tvshows %}
  <li>
    <a href="{{ tvshow.external_url }}">{{ tvshow.title }}</a>
  </li>
{% endfor %}
</ol>

## Most recently completed
<ol>
{% for tvshow in site.tvshows %}
  <li>
    <a href="{{ tvshow.external_url }}">{{ tvshow.title }}</a>
  </li>
{% endfor %}
</ol>
