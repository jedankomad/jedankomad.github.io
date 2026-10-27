---
layout: page
title: Projects
subtitle: 'HelloWorld("print")'
permalink: /projects/
---

<style>
  .pj-list { list-style:none; margin:8px 0 0; padding:0; display:grid; gap:14px; }
  .pj { display:flex; align-items:center; gap:16px; padding:16px 18px; border-radius:12px; background:var(--surface-col);
    border:1px solid var(--line-col); color:var(--text-col); text-decoration:none;
    transition:transform .18s ease, border-color .18s ease, box-shadow .18s ease; }
  .pj:hover, .pj:focus-visible { transform:translateY(-3px); border-color:var(--gold-col);
    box-shadow:0 8px 20px rgba(0,0,0,.45); color:var(--text-col); text-decoration:none; }
  .pj img, .pj-ico { width:56px; height:56px; border-radius:12px; flex:none; }
  .pj-ico { display:flex; align-items:center; justify-content:center; background:var(--line-col);
    color:var(--gold-col); font-family:var(--header-font); font-size:1.6rem; font-weight:700; }
  .pj-text { flex:1; min-width:0; }
  .pj-text b { display:block; font-family:var(--header-font); font-size:1.15rem; }
  .pj-text span { display:block; color:var(--muted-col); font-size:.85rem; font-family:var(--header-font); }
  .pj-go { color:var(--accent-col); font-size:1.3rem; transition:color .18s ease, transform .18s ease; }
  .pj:hover .pj-go { color:var(--gold-col); transform:translateX(3px); }
</style>

<ul class="pj-list">
{%- for p in site.data.projects %}
  <li>
    <a class="pj" href="{{ p.url }}">
      {%- if p.icon %}
      <img src="{{ p.icon }}" alt="" width="56" height="56">
      {%- else %}
      <span class="pj-ico" aria-hidden="true">{{ p.name | slice: 0 }}</span>
      {%- endif %}
      <span class="pj-text"><b>{{ p.name }}</b><span>{% if p.description %}{{ p.description }}{% else %}{{ p.url | remove_first: "https://" | remove_first: "http://" | split: "/" | join: "/" }}{% endif %}</span></span>
      <span class="pj-go" aria-hidden="true">→</span>
    </a>
  </li>
{%- endfor %}
</ul>
