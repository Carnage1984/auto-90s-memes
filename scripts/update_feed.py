# scripts/update_feed.py

import glob, os, time
from xml.sax.saxutils import escape

# Build items for the last 7 memes
items = []
for img in sorted(glob.glob("memes/*.jpg"))[-7:]:
    date = os.path.basename(img).split(".")[0]
    url = f"https://raw.githubusercontent.com/Carnage1984/auto-90s-memes/main/{img}"
    items.append(f"""
<item>
  <title>90s Meme for {escape(date)}</title>
  <link>{escape(url)}</link>
  <pubDate>{time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.gmtime())}</pubDate>
</item>""")

feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>Epoch Nostalgia 90s Memes</title>
  <link>https://github.com/Carnage1984/auto-90s-memes</link>
  <description>Daily 90s meme throwback</description>
  {''.join(items)}
</channel></rss>"""

# Write out feed.xml
with open("feed.xml", "w") as f:
    f.write(feed)
