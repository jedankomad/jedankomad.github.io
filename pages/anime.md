---
layout: page
title: Anime
subtitle: "Most recently completed"
permalink: /anime/
---

<ul>
{% for anime in site.anime %}
  <li>
    <a href="{{ anime.external_url }}">{{ anime.title }}</a>
  </li>
{% endfor %}
</ul>

