#!/usr/bin/env python3
import glob
import os
import time
from xml.sax.saxutils import escape

# ── Channel metadata ───────────────────────────────────────
TITLE       = "Epoch Nostalgia 90s Memes"
LINK        = "https://github.com/Carnage1984/auto-90s-memes"
DESCRIPTION = "Daily 90s meme throwback"

# ── Build the <item> list ──────────────────────────────────
items = []
# grab the last 7 .jpg filenames under memes/
for img in sorted(glob.glob("memes/*.jpg"))[-7:]:
    name     = os.path.splitext(os.path.basename(img))[0]
    raw_url  = f"https://raw.githubusercontent.com/Carnage1984/auto-90s-memes/main/{img}"
    pub_date = time.strftime(
        "%a, %d %b %Y %H:%M:%S +0000",
        time.gmtime(os.path.getmtime(img))  # use the file’s own mtime
    )
    items.append(
        "  <item>\n"
        f"    <title>90s Meme: {escape(name)}</title>\n"
        f"    <link>{escape(raw_url)}</link>\n"
        f"    <pubDate>{pub_date}</pubDate>\n"
        "  </item>"
    )

# ── Write out feed.xml ─────────────────────────────────────
with open("feed.xml", "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<rss version="2.0">\n')
    f.write("<channel>\n")
    f.write(f"  <title>{escape(TITLE)}</title>\n")
    f.write(f"  <link>{escape(LINK)}</link>\n")
    f.write(f"  <description>{escape(DESCRIPTION)}</description>\n")
    f.write("\n".join(items))
    f.write("\n</channel>\n")
    f.write("</rss>\n")
