import feedparser
import os
from datetime import datetime

# Postavke za MyAnimeList RSS
RSS_FEED_URL = "https://myanimelist.net/rss.php?type=rw&u=JedanKomad"  # Zameni USERNAME sa svojim MAL username-om
POSTS_DIR = "pages/anime"  # Novi direktorijum za anime postove
SEEN_FILE = "scripts/seen_mal_reviews.txt"  # Fajl za praćenje već viđenih linkova

# Funkcija za učitavanje već obrađenih linkova
def load_seen_links():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r") as file:
        return set(file.read().splitlines())

# Funkcija za čuvanje novih linkova
def save_seen_links(links):
    with open(SEEN_FILE, "w") as file:
        file.write("\n".join(links))

# Generisanje Markdown fajla za anime postove
def generate_markdown(entry):
    title = entry.title.replace(" ", "-").lower()
    date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z").date()
    filename = f"{date}-{title}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    # Proveri da li folder postoji, ako ne postoji - kreiraj ga
    os.makedirs(POSTS_DIR, exist_ok=True)

    content = f"""---
layout: post
title: "{entry.title}"
date: {date}
permalink: /anime/{date}-{title}/
---

# [{entry.title}]({entry.link})
"""

    with open(filepath, "w") as file:
        file.write(content)
    print(f"Generated anime post: {filepath}")

# Glavna logika
def main():
    feed = feedparser.parse(RSS_FEED_URL)
    seen_links = load_seen_links()
    new_links = set()

    for entry in feed.entries:
        if entry.link not in seen_links:
            generate_markdown(entry)
            new_links.add(entry.link)

    # Sačuvaj nove linkove
    save_seen_links(seen_links.union(new_links))

if __name__ == "__main__":
    main()
