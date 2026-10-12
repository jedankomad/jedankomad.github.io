#!/usr/bin/env python3
"""Povlači Letterboxd RSS i održava _data/movies.json (poster, ocena, review).

Samo standardna biblioteka. Postojeći unosi se čuvaju (RSS ima samo poslednjih ~50),
a novi / izmenjeni se spajaju po ključu "link|datum gledanja".
"""
import html
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

USERNAME = os.environ.get("LETTERBOXD_USER", "pavlesap")
RSS_URL = f"https://letterboxd.com/{USERNAME}/rss/"
DATA_FILE = os.environ.get("MOVIES_JSON", "_data/movies.json")
UA = "Mozilla/5.0 (compatible; jedankomad-site-sync/1.0)"
NS = {
    "lb": "https://letterboxd.com",
    "tmdb": "https://themoviedb.org",
    "dc": "http://purl.org/dc/elements/1.1/",
}
MAX_POSTER_LOOKUPS = 40


def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def stars_from_title(title):
    m = re.search(r"-\s*([★½]+)\s*$", title or "")
    if not m:
        return None
    s = m.group(1)
    return s.count("★") + (0.5 if "½" in s else 0)


def clean_review(desc_html):
    """Vraća (poster_url, review_text). Review je običan tekst, paragrafi razdvojeni praznim redom."""
    poster = None
    m = re.search(r'<img[^>]+src="([^"]+)"', desc_html or "")
    if m:
        poster = html.unescape(m.group(1))
    body = re.sub(r"<img[^>]*>", "", desc_html or "")
    paras = re.findall(r"<p>(.*?)</p>", body, flags=re.S)
    out = []
    for p in paras:
        p = re.sub(r"<br\s*/?>", "\n", p)
        p = re.sub(r"<[^>]+>", "", p)
        p = html.unescape(p).strip()
        if p:
            out.append(p)
    # Unosi bez review-a imaju samo "Watched on ..." red
    if len(out) == 1 and re.match(r"^Watched on ", out[0]):
        out = []
    return poster, "\n\n".join(out)


def parse_item(item):
    def t(tag, ns=None):
        el = item.find(f"{ns}:{tag}" if ns else tag, NS)
        return el.text.strip() if el is not None and el.text else None

    guid = t("guid") or ""
    title = t("title") or ""
    link = t("link") or ""
    if "letterboxd-list" in guid or "/list/" in link:
        return None  # liste preskačemo
    film_title = t("filmTitle", "lb")
    film_year = t("filmYear", "lb")
    if not film_title:
        m = re.match(r"^(.*), (\d{4})(?: - .*)?$", title)
        if not m:
            return None
        film_title, film_year = m.group(1), m.group(2)
    rating = t("memberRating", "lb")
    rating = float(rating) if rating else stars_from_title(title)
    watched = t("watchedDate", "lb")
    if not watched:
        pub = t("pubDate")
        try:
            watched = datetime.strptime(pub, "%a, %d %b %Y %H:%M:%S %z").date().isoformat()
        except Exception:
            return None
    desc_el = item.find("description")
    poster, review = clean_review(desc_el.text if desc_el is not None else "")
    return {
        "key": f"{link}|{watched}",
        "title": film_title,
        "year": int(film_year) if film_year and film_year.isdigit() else None,
        "rating": rating,
        "watched": watched,
        "rewatch": (t("rewatch", "lb") or "").lower() == "yes",
        "link": link,
        "poster": poster,
        "review": review,
    }


def film_page_url(link):
    m = re.match(r"https://letterboxd\.com/[^/]+/film/([^/]+)/", link)
    return f"https://letterboxd.com/film/{m.group(1)}/" if m else None


def lookup_poster(link):
    """Najbolji pokušaj: og:image sa stranice filma. Greške se tiho ignorišu."""
    url = film_page_url(link)
    if not url:
        return None
    try:
        page = http_get(url, timeout=20)
    except Exception:
        return None
    m = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', page)
    return html.unescape(m.group(1)) if m else None


def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []


def main():
    movies = {m["key"]: m for m in load()}
    try:
        feed = http_get(RSS_URL)
        root = ET.fromstring(feed)
    except Exception as e:
        print(f"RSS nije dostupan ({e}); podaci ostaju nepromenjeni.")
        return 0  # ne rušimo workflow
    added = updated = 0
    for item in root.iter("item"):
        e = parse_item(item)
        if not e:
            continue
        old = movies.get(e["key"])
        if old:
            # RSS je izvor istine, ali poster ne gubimo ako ga feed nema
            e["poster"] = e["poster"] or old.get("poster")
            if old != e:
                updated += 1
        else:
            added += 1
        movies[e["key"]] = e
    # Posteri za stare unose bez postera (best effort)
    looked = 0
    for m in movies.values():
        if not m.get("poster") and looked < MAX_POSTER_LOOKUPS:
            looked += 1
            p = lookup_poster(m["link"])
            if p:
                m["poster"] = p
            time.sleep(1)
    out = sorted(movies.values(), key=lambda m: (m["watched"], m["key"]), reverse=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"Novih: {added}, izmenjenih: {updated}, ukupno: {len(out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
