import os
import sqlite3
from urllib.parse import urlparse
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "movies.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                poster_url TEXT DEFAULT '',
                overview TEXT DEFAULT '',
                release_date TEXT DEFAULT '',
                source_url TEXT DEFAULT '',
                is_upcoming INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        # Mevcut tüm filmleri temizle
        conn.execute("DELETE FROM movies")
        conn.commit()


def is_safe_http_url(url: str) -> bool:
    if not url:
        return False
    parsed = urlparse(url.strip())
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def is_direct_video_url(url: str) -> bool:
    path = urlparse(url.strip()).path.lower()
    return path.endswith((".mp4", ".webm", ".ogg", ".m3u8"))


init_db()


@app.route("/")
@app.route("/makine")
def home():
    tab = request.args.get("tab", "tumu").strip().lower()
    if tab not in ("tumu", "vizyonda"):
        tab = "tumu"
    raw_q = request.args.get("q", "").strip()

    return render_template_string(
        MENU_ONLY_HTML,
        query=raw_q,
        active_tab=tab,
    )


@app.route("/watch/<int:movie_id>")
def watch_movie(movie_id: int):
    return redirect("/")


MENU_ONLY_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MEDUSAFILM</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0d0f14;
      color: #f3f4f6;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      min-height: 100vh;
    }
    header {
      background: #121620;
      border-bottom: 1px solid #222938;
      padding: 14px 18px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }
    .brand {
      font-size: 1.3rem;
      font-weight: 800;
      letter-spacing: 1px;
      color: #f59e0b;
      text-decoration: none;
    }
    .nav-links { display: flex; align-items: center; gap: 10px; }
    .nav-btn {
      text-decoration: none;
      padding: 7px 14px;
      border-radius: 8px;
      font-size: 0.9rem;
      font-weight: 600;
      background: #1d2332;
      color: #e5e7eb;
      border: 1px solid #2c354b;
    }
    .nav-btn.support {
      background: #22c55e;
      color: #07130a;
      border: none;
    }
    .container {
      max-width: 1100px;
      margin: 0 auto;
      padding: 20px 16px 40px;
    }
    .tabs { display: flex; gap: 8px; margin-bottom: 14px; }
    .tab-btn {
      text-decoration: none;
      padding: 8px 16px;
      border-radius: 20px;
      font-size: 0.9rem;
      font-weight: 700;
      background: #181e2b;
      color: #cbd5e1;
      border: 1px solid #283247;
    }
    .tab-btn.active {
      background: #f59e0b;
      color: #111827;
      border-color: #f59e0b;
    }
    .search-form { display: flex; gap: 8px; }
    .search-input {
      flex: 1;
      padding: 11px 14px;
      border-radius: 10px;
      border: 1px solid #283042;
      background: #151a24;
      color: #fff;
      font-size: 1rem;
    }
    .search-btn {
      padding: 11px 18px;
      border-radius: 10px;
      border: none;
      background: #f59e0b;
      color: #111827;
      font-weight: 700;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <header>
    <a class="brand" href="/">MEDUSAFILM</a>
    <div class="nav-links">
      <a class="nav-btn support" href="https://www.instagram.com/ttlewiss21/" target="_blank" rel="noopener">Destek</a>
    </div>
  </header>

  <main class="container">
    <div class="tabs">
      <a class="tab-btn {% if active_tab == 'tumu' %}active{% endif %}" href="/?tab=tumu{% if query %}&q={{ query }}{% endif %}">Tümü</a>
      <a class="tab-btn {% if active_tab == 'vizyonda' %}active{% endif %}" href="/?tab=vizyonda{% if query %}&q={{ query }}{% endif %}">Vizyonda</a>
    </div>

    <form class="search-form" method="get" action="/">
      <input type="hidden" name="tab" value="{{ active_tab }}" />
      <input class="search-input" type="text" name="q" value="{{ query }}" placeholder="Ara..." />
      <button class="search-btn" type="submit">Ara</button>
    </form>
  </main>
</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
