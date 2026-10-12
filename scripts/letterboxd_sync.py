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
MAX_POSTER_LOOKUPS = 60


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
        # True = ocenu i review smo pročitali iz RSS-a, pa prazan review zaista znači "nema review-a".
        # Starije unose koje RSS više ne vraća nemaju ovo polje: njihov review je nepoznat.
        "detail": True,
    }


def film_page_url(link):
    m = re.match(r"https://letterboxd\.com/[^/]+/film/([^/]+)/", link)
    return f"https://letterboxd.com/film/{m.group(1)}/" if m else None


POSTER_RE = r'https://a\.ltrbxd\.com/resized/film-poster/[^"\'\s<>]+'


def is_real_poster(url):
    """Poster ima proporcije 2:3 (npr. ...-0-600-0-900-crop), backdrop je široka slika
    (npr. ...-1200-1200-675-675-crop ili putanja sa 'backdrop'). Putanja NIJE pouzdana:
    pravi posteri mogu biti i pod /film-poster/ i pod /sm/upload/."""
    if not url or "backdrop" in url:
        return False
    m = re.search(r"-(\d+)-(\d+)-(\d+)-(\d+)-crop", url)
    if not m:
        return "/film-poster/" in url
    x0, w, y0, h = (int(g) for g in m.groups())
    return x0 == 0 and y0 == 0 and w > 0 and 1.3 < h / w < 1.7


def poster_from_page(page):
    """Izvlači POSTER (ne backdrop) iz HTML-a stranice filma. og:image se namerno ignoriše."""
    # JSON-LD blok filma sadrži polje "image" sa posterom
    m = re.search(r'"image"\s*:\s*"(' + POSTER_RE + ')"', page)
    if m:
        return html.unescape(m.group(1).replace("\\/", "/"))
    return None


def lookup_poster(link):
    """Najbolji pokušaj, greške se tiho ignorišu. Vraća (url, metod) ili (None, razlog)."""
    url = film_page_url(link)
    if not url:
        return None, "nevalidan link"
    try:
        page = http_get(url, timeout=20)
    except Exception as e:
        return None, f"stranica nedostupna ({e})"
    p = poster_from_page(page)
    if p:
        return p, "json-ld"
    # rezerva: Letterboxd-ov endpoint za poster
    slug = url.rstrip("/").rsplit("/", 1)[-1]
    try:
        frag = http_get(f"https://letterboxd.com/ajax/poster/film/{slug}/std/230x345/", timeout=20)
        m = re.search(POSTER_RE, frag)
        if m:
            return html.unescape(m.group(0)), "ajax"
    except Exception as e:
        return None, f"ajax nedostupan ({e})"
    return None, "poster nije pronadjen na stranici"


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
    # Posteri za unose bez postera ILI sa slikom koja nije pravi poster (npr. backdrop)
    looked = fixed = 0
    for m in movies.values():
        if is_real_poster(m.get("poster")) or looked >= MAX_POSTER_LOOKUPS:
            continue
        looked += 1
        p, how = lookup_poster(m["link"])
        if p and is_real_poster(p):
            m["poster"] = p
            fixed += 1
            print(f"  poster OK [{how}]: {m['title']}")
        else:
            # pogrešnu sliku radije uklanjamo nego prikazujemo
            m["poster"] = None
            print(f"  poster NIJE nadjen: {m['title']} -> {how}")
        time.sleep(1)
    print(f"Provereno postera: {looked}, ispravljeno/dodato: {fixed}")
    out = sorted(movies.values(), key=lambda m: (m["watched"], m["key"]), reverse=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"Novih: {added}, izmenjenih: {updated}, ukupno: {len(out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
