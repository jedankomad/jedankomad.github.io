---
layout: page
title: TV Shows
subtitle: 20 years in the can
permalink: /tvshows/
---

## Currently watching
<ol class="current">
{% for tvshow in site.tvshows %}
  <li>  
    {% if tvshow.path contains 'current' %}
      <a href="{{ tvshow.external_url }}">{{ tvshow.title AAAAAAA }}</a>
    {% endif %}
  </li>
{% endfor %}
</ol>

## Most recently completed
<ol class="completed">
{% for tvshow in site.tvshows %}
  <li>
    {% if tvshow.path contains 'completed' %}
      <a href="{{ tvshow.external_url }}">{{ tvshow.title }}</a>
    {% endif %}
  </li>
{% endfor %}
</ol>
