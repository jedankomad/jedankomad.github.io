---
layout: page
title: Manga
subtitle: Most recently completed
permalink: /manga/
---

<ul>
{% for manga in site.manga %}
  <li>
    <a href="{{ manga.external_url }}">{{ manga.title }}</a>
  </li>
{% endfor %}
</ul>

