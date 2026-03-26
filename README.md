# 🚀 IT & AI News Scanner (Cloud Edition)

An automated news aggregator designed for Software Developers (FIAE) and IT professionals. It specifically scans IT news portals and the web for relevant topics such as vocational training, AI trends, and programming.

## 🌟 Features
- **Multi-Source Scanning:** Scans Heise, Golem, The Decoder, and t3n via RSS feeds.
- **Global Search:** Utilizes Google News RSS parameters for web-wide topic tracking.
- **Smart Filtering:** Automatically filters articles by keywords (AI, FIAE, Python, IHK, etc.).
- **Data Persistence:** Stores all findings in a local SQLite database (`news_archive.db`).
- **Cloud Automation:** Fully automated execution via **GitHub Actions** (runs every morning at 08:00 UTC).
- **Live Dashboard:** Automatically generates an `index.html` accessible via **GitHub Pages**.

## 🛠️ Technology Stack
- **Language:** Python 3.9+
- **Libraries:** `feedparser` (RSS parsing), `sqlite3` (Database), `urllib` (URL encoding).
- **Automation:** GitHub Actions (YAML workflows).
- **Frontend:** HTML5 / CSS3 (Responsive Dashboard).

## 🚀 Installation (Local)
1. Clone the repository:
   ```bash
   git clone https://github.com
   cd it-news-scanner
Verwende Code mit Vorsicht.

Install dependencies:
bash
pip install feedparser
Verwende Code mit Vorsicht.

Run the scanner:
bash
python it_scanner.py