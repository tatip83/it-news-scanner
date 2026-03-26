
import feedparser
import os
import sqlite3
import logging
import webbrowser
from urllib.parse import quote
from datetime import datetime

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def init_db():
    conn = sqlite3.connect('news_archive.db')
    cursor = conn.cursor()
    # Link muss UNIQUE sein, um Dubletten in der Datenbank zu verhindern
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles 
                      (quelle TEXT, titel TEXT, link TEXT UNIQUE, datum TEXT)''')
    conn.commit()
    return conn

def run_scanner():
    conn = init_db()
    cursor = conn.cursor()
    
    # Deine Suchbegriffe
    suchbegriffe = ["FIAE", "KI", "Python", "IHK", "Umschulung", "Programmierung"]
    
    # KORREKTUR: Hier müssen die echten RSS-Feed-URLs stehen!
    sources = {
        "Heise Developer": "https://www.heise.de",
        "The Decoder": "https://the-decoder.de",
        "Golem": "https://rss.golem.de",
        "t3n Software": "https://t3n.de"
    }
    
    # Google Suche sicher hinzufügen
    google_queries = ["FIAE", "Künstliche Intelligenz", "Python Programmierung"]
    for b in google_queries:
        sicher = quote(b)
        sources[f"Google: {b}"] = f"https://news.google.com/rss/search?q={sicher}&hl=de&gl=DE&ceid=DE:de"

    new_count = 0
    for name, url in sources.items():
        try:
            logging.info(f"Scanne: {name}...")
            feed = feedparser.parse(url)
            for e in feed.entries:
                titel = getattr(e, 'title', '')
                desc = getattr(e, 'summary', '')
                
                # Check ob Keywords im Titel oder der Beschreibung passen
                if any(w.lower() in (titel + desc).lower() for w in suchbegriffe):
                    link = getattr(e, 'link', '')
                    date_str = datetime.now().strftime("%d.%m.%Y")
                    
                    # In SQL speichern
                    try:
                        cursor.execute("INSERT INTO articles (quelle, titel, link, datum) VALUES (?, ?, ?, ?)", 
                                     (name, titel, link, date_str))
                        new_count += 1
                    except sqlite3.IntegrityError:
                        pass # Artikel schon bekannt
        except Exception as ex:
            logging.error(f"Fehler bei {name}: {ex}")

    conn.commit()
    
    # Dashboard generieren: Die letzten 30 Einträge aus der DB holen
    cursor.execute("SELECT quelle, titel, link, datum FROM articles ORDER BY rowid DESC LIMIT 30")
    rows = cursor.fetchall()
    
    html_datei = "index.html"
    with open(html_datei, "w", encoding="utf-8") as f:
        f.write("<html><head><meta charset='utf-8'><style>")
        f.write("body { font-family: sans-serif; background: #f4f4f9; padding: 40px; }")
        f.write(".card { background: white; padding: 15px; margin: 10px 0; border-left: 5px solid #007bff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }")
        f.write(".meta { font-size: 0.8em; color: #666; }")
        f.write("a { text-decoration: none; color: #007bff; font-weight: bold; font-size: 1.1em; }")
        f.write("</style></head><body>")
        f.write(f"<h1>IT News Archiv</h1><p>Letzter Scan: {datetime.now().strftime('%H:%M:%S')} | {new_count} neue Artikel</p>")
        
        for r in rows:
            # r[0]=Quelle, r[1]=Titel, r[2]=Link, r[3]=Datum
            f.write(f"<div class='card'>")
            f.write(f"<div class='meta'>{r[0]} | {r[3]}</div>")
            f.write(f"<a href='{r[2]}' target='_blank'>{r[1]}</a>")
            f.write(f"</div>")
            
        f.write("</body></html>")
    
    conn.close()
    logging.info(f"Scan abgeschlossen. {new_count} neue Artikel hinzugefügt.")
    
    # Datei automatisch im Browser öffnen
    webbrowser.open(f"file://{os.path.abspath(html_datei)}")

if __name__ == "__main__":
    run_scanner()