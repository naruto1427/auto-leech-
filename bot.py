import asyncio
import feedparser
from telethon import TelegramClient
from datetime import datetime
import os

# ENV Variables for Render
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION_NAME", "nyaa_userbot")
GROUP_ID = int(os.getenv("GROUP_ID"))  # Target group ID (e.g., -1001234567890)

# Use nyaa.si or nyaa.land
RSS_URL = "https://nyaa.si/?page=rss"

# Only post torrents with "1080p" and avoid reposting
seen_links = set()

client = TelegramClient(SESSION, API_ID, API_HASH)

async def fetch_and_send():
    global seen_links
    while True:
        try:
            feed = feedparser.parse(RSS_URL)
            for entry in feed.entries:
                title = entry.title
                link = entry.link

                if "1080p" in title and link not in seen_links:
                    seen_links.add(link)
                    msg = f"/lx {link}"
                    await client.send_message(GROUP_ID, msg)
            await asyncio.sleep(45)  # 1-minute polling
        except Exception as e:
            print(f"[ERROR] {e}")
            await asyncio.sleep(45)

async def main():
    await client.start()
    print(f"Logged in as {await client.get_me()}")
    await fetch_and_send()

with client:
    client.loop.run_until_complete(main())
