# 🚀 IT & KI News-Scanner (Cloud Edition)

Ein automatisierter News-Aggregator für Fachinformatiker (FIAE), der gezielt IT-Fachportale und das Internet nach relevanten Themen wie Ausbildung, KI-Trends und Programmierung durchsucht.

## 🌟 Features
- **Multi-Source Scanning:** Durchsucht Heise, Golem, The Decoder und t3n via RSS.
- **Global Search:** Nutzt Google News RSS-Parameter für eine webweite Suche.
- **Smart Filtering:** Filtert Artikel nach Keywords (KI, FIAE, Python, IHK etc.).
- **Persistence:** Speichert alle Funde in einer lokalen SQLite-Datenbank (`news_archive.db`).
- **Cloud Automation:** Vollautomatische Ausführung via **GitHub Actions** (jeden Morgen um 08:00 Uhr).
- **Live Dashboard:** Generiert automatisch eine `index.html`, die über **GitHub Pages** erreichbar ist.

## 🛠️ Technologie-Stack
- **Sprache:** Python 3.9+
- **Bibliotheken:** `feedparser` (RSS-Parsing), `sqlite3` (Datenbank), `urllib` (URL-Encoding).
- **Automatisierung:** GitHub Actions (YAML-Workflows).
- **Frontend:** HTML5 / CSS3 (Responsives Dashboard).

## 🚀 Installation (Lokal)
1. Repository klonen:
   ```bash
   git clone https://github.com
   cd it-news-scanner
