---
layout: page
title: Anime
subtitle: Believe in me who believes in you!
permalink: /anime/
---

# Anime Reviews

<ul>
  {% for post in site.posts %}
    {% if post.url contains '/anime/' %}
      <li>
        <a href="{{ post.url }}">{{ post.title }}</a>
      </li>
    {% endif %}
  {% endfor %}
</ul>
