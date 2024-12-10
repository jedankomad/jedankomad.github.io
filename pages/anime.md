---
layout: page
title: Anime
subtitle: "stagod"
permalink: /anime/
---

<ul>
{% for anime in site.anime %}
  <li>
    <a href="{{ anime.external_url }}">{{ anime.title }}</a>
  </li>
{% endfor %}
</ul>

