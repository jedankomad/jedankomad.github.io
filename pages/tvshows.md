---
layout: page
title: TV Shows
subtitle: 20 years in the can
permalink: /tvshows/
---

## Currently watching
<ol id="current">
{% for tvshow in site.tvshows %}
  <li>  
    {% if tvshow.path contains 'current' %}
      <a href="{{ tvshow.external_url }}">{{ tvshow.title }}</a>
    {% endif %}
  </li>
{% endfor %}
</ol>

## Most recently completed
<ol id="completed">
{% for tvshow in site.tvshows %}
  <li>
    {% if tvshow.path contains 'completed' %}
      <a href="{{ tvshow.external_url }}">{{ tvshow.title }}</a>
    {% endif %}
  </li>
{% endfor %}
</ol>
