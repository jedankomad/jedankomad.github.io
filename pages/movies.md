---
layout: page
title: Movies
subtitle: That's a bingo!
permalink: /movies/
--- 

<ul>
{% for movie in site.movies %}
  <li><a href="{{ movie.url }}">{{ movie.title }}</a></li>
{% endfor %}
</ul>