---
layout: page
title: TV Shows
subtitle: 20 years in the can.
permalink: /tvshows/
---

<ul>
{% for anime in site.anime %}
  <li>
    <a href="{{ anime.external_url }}">{{ anime.title }}</a>
  </li>
{% endfor %}
</ul>
