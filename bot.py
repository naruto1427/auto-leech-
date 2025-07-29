import asyncio
import feedparser
from telethon import TelegramClient
from datetime import datetime
import os

# ======== ENV VARIABLES =========
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "nyaa_userbot")
GROUP_ID = int(os.getenv("GROUP_ID"))              # Your target group (where /lx goes)
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))  # Your logging channel ID

# ======== NYAA RSS CONFIG =========
RSS_URL = "https://nyaa.si/?page=rss&c=1_2"  # Anime - English-translated category

# Store seen torrent links
seen_links = set()

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

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

                    # Send /lx link to group
                    await client.send_message(GROUP_ID, f"/lx {link}")

                    # Log nicely in the log channel
                    log_msg = (
                        "✅ **Posted New Torrent**\n"
                        f"📝 **Title:** `{title}`\n"
                        f"🔗 **Link:** [Open Torrent]({link})"
                    )
                    await client.send_message(LOG_CHANNEL_ID, log_msg, link_preview=False)

                    print(f"[{datetime.now().isoformat()}] Sent: {title}")
            await asyncio.sleep(60)
        except Exception as e:
            err = f"[ERROR] {datetime.now().isoformat()} - {e}"
            print(err)
            await client.send_message(LOG_CHANNEL_ID, f"❌ Error:\n`{str(e)}`")
            await asyncio.sleep(45)

async def main():
    await client.start()
    print("Logged in as:", (await client.get_me()).username)
    await fetch_and_send()

with client:
    client.loop.run_until_complete(main())
