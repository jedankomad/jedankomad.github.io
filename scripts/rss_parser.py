import feedparser
import os
from datetime import datetime

# Postavke
RSS_FEED_URL = "https://letterboxd.com/pavlesap/rss"  # Promeni sa tvojim RSS URL-om
POSTS_DIR = "pages/movies"
SEEN_FILE = "scripts/seen_reviews.txt"

# Proveri da li folder postoji, ako ne postoji - kreiraj ga
os.makedirs(POSTS_DIR, exist_ok=True)
# Promeni prava ako je potrebno
#os.chmod(POSTS_DIR, 0o777)

# Putanja do movies direktorijuma
#directory = 'pages/movies'
# Provera prava pristupa
#if os.access(directory, os.W_OK):
#    print(f"Možete da pišete u {directory}")
#else:
#    print(f"Nemate pravo pisanja u {directory}")

# Funkcija za učitavanje već obrađenih linkova
def load_seen_links():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r") as file:
        return set(file.read().splitlines())

# Funkcija za čuvanje novih linkova
def save_seen_links(links):
    with open(SEEN_FILE, "a") as file:
        file.write("\n".join(links) + "\n")
    print(f"Saved links to {SEEN_FILE}: {links}")  # Test print

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
permalink: /movies/{date}-{title}/
---

# [Review]({entry.link})

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
            #save_seen_links(entry.link)
    
    # Sačuvaj nove linkove
    save_seen_links(seen_links.union(new_links))

if __name__ == "__main__":
    main()
