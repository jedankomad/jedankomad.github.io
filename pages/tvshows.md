---
layout: page
title: TV Shows
subtitle: Most recently completed
permalink: /tvshows/
---

<ol>
{% for tvshow in site.tvshows %}
  <li>
    <a href="{{ tvshow.external_url }}">{{ tvshow.title }}</a>
  </li>
{% endfor %}
</ol>
