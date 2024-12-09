import feedparser
import os
from datetime import datetime

# Postavke
RSS_FEED_URL = "https://letterboxd.com/pavlesap/rss"  # Promeni sa tvojim RSS URL-om
POSTS_DIR = "_posts"
SEEN_FILE = "scripts/seen_reviews.txt"

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

# Generisanje Markdown fajla
def generate_markdown(entry):
    title = entry.title.replace(" ", "-").lower()
    date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z").date()
    filename = f"{date}-{title}.md"
    filepath = os.path.join(POSTS_DIR, filename)
    
    content = f"""---
layout: post
title: "{entry.title}"
date: {date}
---

[Review]({entry.link}).
"""
    with open(filepath, "w") as file:
        file.write(content)
    print(f"Generated post: {filepath}")

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
