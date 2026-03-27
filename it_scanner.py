import feedparser
import os
import sqlite3
import logging
import webbrowser
from urllib.parse import quote
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def init_db():
    conn = sqlite3.connect('news_archive.db')
    cursor = conn.cursor()
    # Link must be UNIQUE to prevent duplicate entries in the database
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles 
                      (source TEXT, title TEXT, link TEXT UNIQUE, date TEXT)''')
    conn.commit()
    return conn

def run_scanner():
    conn = init_db()
    cursor = conn.cursor()
    
    # Your search keywords
    keywords = ["FIAE", "AI", "Python", "IHK", "Retraining", "Programming"]
    
    # RSS Feed URLs
    sources = {
        "Heise Developer": "https://www.heise.de",
        "The Decoder": "https://the-decoder.de",
        "Golem": "https://rss.golem.de",
        "t3n Software": "https://t3n.de"
    }
    
    # Add Google Search safely
    google_queries = ["FIAE", "Artificial Intelligence", "Python Programming"]
    for q in google_queries:
        encoded_query = quote(q)
        sources[f"Google: {q}"] = f"https://news.google.com/rss/search?q={encoded_query}&hl=en&gl=US&ceid=US:en"

    new_count = 0
    for name, url in sources.items():
        try:
            logging.info(f"Scanning: {name}...")
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = getattr(entry, 'title', '')
                desc = getattr(entry, 'summary', '')
                
                # Check if keywords match title or description
                if any(word.lower() in (title + desc).lower() for word in keywords):
                    link = getattr(entry, 'link', '')
                    date_str = datetime.now().strftime("%d.%m.%Y")
                    
                    # Save to SQL
                    try:
                        cursor.execute("INSERT INTO articles (source, title, link, date) VALUES (?, ?, ?, ?)", 
                                     (name, title, link, date_str))
                        new_count += 1
                    except sqlite3.IntegrityError:
                        pass # Article already exists
        except Exception as ex:
            logging.error(f"Error at {name}: {ex}")

    conn.commit()
    
    # Generate Dashboard: Fetch last 30 entries from DB
    cursor.execute("SELECT source, title, link, date FROM articles ORDER BY rowid DESC LIMIT 30")
    rows = cursor.fetchall()
    
    html_file = "index.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("<html><head><meta charset='utf-8'><style>")
        f.write("body { font-family: sans-serif; background: #f4f4f9; padding: 40px; }")
        f.write(".card { background: white; padding: 15px; margin: 10px 0; border-left: 5px solid #007bff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }")
        f.write(".meta { font-size: 0.8em; color: #666; }")
        f.write("a { text-decoration: none; color: #007bff; font-weight: bold; font-size: 1.1em; }")
        f.write("</style></head><body>")
        f.write(f"<h1>IT News Archive</h1><p>Last scan: {datetime.now().strftime('%H:%M:%S')} | {new_count} new articles</p>")
        
        for r in rows:
            # r[0]=Source, r[1]=Title, r[2]=Link, r[3]=Date
            f.write(f"<div class='card'>")
            f.write(f"<div class='meta'>{r[0]} | {r[3]}</div>")
            f.write(f"<a href='{r[2]}' target='_blank'>{r[1]}</a>")
            f.write(f"</div>")
            
        f.write("</body></html>")
    
    conn.close()
    logging.info(f"Scan complete. {new_count} new articles added.")
    
    # Automatically open file in browser
    #webbrowser.open(f"file://{os.path.abspath(html_file)}")

if __name__ == "__main__":
    run_scanner()
