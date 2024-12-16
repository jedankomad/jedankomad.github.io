---
layout: page
title: TV Shows
subtitle: 20 years in the can
permalink: /tvshows/
---

## Currently watching
<ul>
{% for tvshow in site.tvshows %}
  {% if tvshow.path contains 'current' %}
    <li>
      <a href="{{ tvshow.external_url }}">{{ tvshow.title }}</a>
    </li>
  {% endif %}
{% endfor %}
</ul>

<!-- Razdvajanje lista -->
<hr>

## Most recently completed
<ol>
{% for tvshow in site.tvshows %}
  {% if tvshow.path contains 'completed' %}
    <li>
      <a href="{{ tvshow.external_url }}">{{ tvshow.title }}</a>
    </li>
  {% endif %}
{% endfor %}
</ol>
