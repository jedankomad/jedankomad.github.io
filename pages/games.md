---
layout: page
title: Games
subtitle: Nanomachines, son.
permalink: /games/
---

## Currently playing
<ul>
{% for game in site.games reversed %}
  {% if game.path contains 'current' %}
    <li>
      <a href="{{ game.external_url }}">{{ game.title }}</a>
    </li>
  {% endif %}
{% endfor %}
</ul>

<!-- Razdvajanje lista -->
<hr>

## Completed, unordered
<ol>
{% for game in site.games reversed %}
  {% if game.path contains 'completed' %}
    <li>
      <a href="{{ game.external_url }}">{{ game.title }}</a>
    </li>
  {% endif %}
{% endfor %}
</ol>
