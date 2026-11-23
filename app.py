import os
import sqlite3
from datetime import datetime, timezone
from urllib.parse import urlparse
from flask import (
    Flask,
    render_template_string,
    request,
    redirect,
    session,
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "medusafilm-gizli-anahtar-degistir")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "medusa123").strip()
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
                release_date TEXT DEFAULT 'Yakında',
                source_url TEXT DEFAULT '',
                is_upcoming INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def is_safe_http_url(url: str) -> bool:
    if not url:
        return False
    parsed = urlparse(url.strip())
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def is_direct_video_url(url: str) -> bool:
    path = urlparse(url.strip()).path.lower()
    return path.endswith((".mp4", ".webm", ".ogg", ".m3u8"))


def is_admin() -> bool:
    return session.get("admin_logged_in") is True


init_db()


def filter_and_rank(items: list[dict], raw_q: str) -> list[dict]:
    q_norm = " ".join(raw_q.lower().split())
    terms = [t for t in q_norm.split(" ") if t]
    if not terms:
        return items

    matched = []
    for item in items:
        title_l = " ".join((item.get("title") or "").lower().split())
        overview_l = " ".join((item.get("overview") or "").lower().split())

        if all((t in title_l) or (t in overview_l) for t in terms):
            if title_l == q_norm:
                score = 0
            elif title_l.startswith(q_norm):
                score = 1
            elif all(t in title_l for t in terms):
                score = 2
            else:
                score = 3
            copy_item = dict(item)
            copy_item["_score"] = score
            matched.append(copy_item)

    matched.sort(
        key=lambda x: (x["_score"], x.get("id") or 0),
        reverse=False,
    )
    for m in matched:
        m.pop("_score", None)
    return matched


@app.route("/")
@app.route("/makine")
def home():
    tab = request.args.get("tab", "tumu").strip().lower()
    if tab not in ("tumu", "vizyonda"):
        tab = "tumu"

    raw_q = request.args.get("q", "").strip()

    with get_db() as conn:
        if tab == "vizyonda":
            rows = conn.execute(
                """
                SELECT * FROM movies
                WHERE is_upcoming = 1
                ORDER BY id DESC
                """
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT * FROM movies
                ORDER BY id DESC
                """
            ).fetchall()

    movies = []
    for r in rows:
        item = dict(r)
        raw_url = (item.get("source_url") or "").strip()
        item["valid_source"] = is_safe_http_url(raw_url)
        item["is_video_file"] = is_direct_video_url(raw_url) if item["valid_source"] else False
        movies.append(item)

    movies = filter_and_rank(movies, raw_q)

    return render_template_string(
        PUBLIC_HTML,
        movies=movies,
        query=raw_q,
        active_tab=tab,
    )


@app.route("/watch/<int:movie_id>")
def watch_movie(movie_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM movies WHERE id = ?", (movie_id,)).fetchone()

    if not row:
        return redirect("/")

    movie = dict(row)
    raw_url = (movie.get("source_url") or "").strip()
    movie["valid_source"] = is_safe_http_url(raw_url)
    movie["is_video_file"] = is_direct_video_url(raw_url) if movie["valid_source"] else False

    return render_template_string(WATCH_HTML, movie=movie)


@app.route("/admin", methods=["GET", "POST"])
@app.route("/makine/panel", methods=["GET", "POST"])
def admin_panel():
    message = None
    error = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "login":
            password = request.form.get("password", "")
            if password == ADMIN_PASSWORD:
                session["admin_logged_in"] = True
                return redirect(request.path)
            error = "Hatalı şifre."

        elif action == "logout":
            session.pop("admin_logged_in", None)
            return redirect(request.path)

        elif is_admin():
            now_iso = datetime.now(timezone.utc).isoformat()

            if action == "add_item":
                title = request.form.get("title", "").strip()
                poster_url = request.form.get("poster_url", "").strip()
                release_date = request.form.get("release_date", "").strip() or "Yakında"
                overview = request.form.get("overview", "").strip()
                source_url = request.form.get("source_url", "").strip()
                is_upcoming = 1 if request.form.get("is_upcoming") == "1" else 0

                if not title:
                    error = "Başlık girmelisin."
                elif poster_url and not is_safe_http_url(poster_url):
                    error = "Afiş URL'si http:// veya https:// ile başlamalı."
                elif source_url and not is_safe_http_url(source_url):
                    error = "Kaynak URL'si http:// veya https:// ile başlamalı."
                else:
                    with get_db() as conn:
                        conn.execute(
                            """
                            INSERT INTO movies (
                                title, poster_url, overview, release_date,
                                source_url, is_upcoming, created_at, updated_at
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                title,
                                poster_url,
                                overview,
                                release_date,
                                source_url,
                                is_upcoming,
                                now_iso,
                                now_iso,
                            ),
                        )
                        conn.commit()
                    message = f"'{title}' eklendi."

            elif action == "update_item":
                movie_id = request.form.get("movie_id")
                title = request.form.get("title", "").strip()
                source_url = request.form.get("source_url", "").strip()
                is_upcoming = 1 if request.form.get("is_upcoming") == "1" else 0
                if not title:
                    error = "Başlık boş olamaz."
                elif source_url and not is_safe_http_url(source_url):
                    error = "Kaynak URL'si http:// veya https:// ile başlamalı."
                else:
                    with get_db() as conn:
                        conn.execute(
                            """
                            UPDATE movies
                            SET title = ?, source_url = ?, is_upcoming = ?, updated_at = ?
                            WHERE id = ?
                            """,
                            (title, source_url, is_upcoming, now_iso, movie_id),
                        )
                        conn.commit()
                    message = "Güncellendi."

            elif action == "delete_item":
                movie_id = request.form.get("movie_id")
                with get_db() as conn:
                    conn.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
                    conn.commit()
                message = "Kayıt silindi."

            elif action == "clear_all":
                with get_db() as conn:
                    conn.execute("DELETE FROM movies")
                    conn.commit()
                message = "Tüm kayıtlar temizlendi."

    if not is_admin():
        return render_template_string(ADMIN_LOGIN_HTML, error=error)

    with get_db() as conn:
        rows = conn.execute("SELECT * FROM movies ORDER BY id DESC").fetchall()

    return render_template_string(
        ADMIN_PANEL_HTML,
        items=[dict(r) for r in rows],
        message=message,
        error=error,
    )


PUBLIC_HTML = """
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
      display: flex;
      flex-direction: column;
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
      max-width: 1200px;
      width: 100%;
      margin: 0 auto;
      padding: 20px 16px 40px;
      flex: 1;
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
    .search-form { display: flex; gap: 8px; margin-bottom: 20px; }
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
    .grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 14px;
    }
    @media (min-width: 768px) {
      .grid { grid-template-columns: repeat(4, 1fr); gap: 18px; }
    }
    .card {
      background: #151a24;
      border: 1px solid #232b3c;
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      position: relative;
    }
    .badge-upcoming {
      position: absolute;
      top: 8px;
      left: 8px;
      background: rgba(245, 158, 11, 0.94);
      color: #111827;
      font-size: 0.72rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
      z-index: 2;
    }
    .poster { aspect-ratio: 2 / 3; background: #0d1017; }
    .poster img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .card-body { padding: 12px; display: flex; flex-direction: column; gap: 8px; flex: 1; }
    .title { font-size: 1rem; font-weight: 700; }
    .meta { font-size: 0.82rem; color: #9ca3af; }
    .overview {
      font-size: 0.85rem;
      color: #cbd5e1;
      line-height: 1.45;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .watch-btn {
      margin-top: auto;
      display: inline-block;
      text-align: center;
      text-decoration: none;
      padding: 8px 10px;
      border-radius: 8px;
      font-size: 0.86rem;
      font-weight: 700;
      background: #f59e0b;
      color: #111827;
    }
    .watch-btn.promo { background: #2563eb; color: #fff; }
    .watch-btn.disabled { background: #222938; color: #9ca3af; }
    footer {
      border-top: 1px solid #222938;
      background: #121620;
      padding: 16px;
      text-align: center;
      font-size: 0.88rem;
      color: #9ca3af;
    }
  </style>
</head>
<body>
  <header>
    <a class="brand" href="/">MEDUSAFILM</a>
    <div class="nav-links">
      <a class="nav-btn" href="/admin">Yönetim Paneli</a>
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

    {% if movies %}
      <div class="grid">
        {% for m in movies %}
          <article class="card">
            {% if m.is_upcoming %}
              <span class="badge-upcoming">VİZYONDA</span>
            {% endif %}
            <a class="poster" href="/watch/{{ m.id }}">
              {% if m.poster_url %}
                <img src="{{ m.poster_url }}" alt="{{ m.title }}" loading="lazy" />
              {% endif %}
            </a>
            <div class="card-body">
              <div class="title">{{ m.title }}</div>
              <div class="meta">{{ m.release_date }}</div>
              {% if m.overview %}
                <p class="overview">{{ m.overview }}</p>
              {% endif %}
              {% if m.valid_source %}
                <a class="watch-btn" href="/watch/{{ m.id }}">Aç</a>
              {% elif m.is_upcoming %}
                <a class="watch-btn promo" href="/watch/{{ m.id }}">Tanıtım</a>
              {% else %}
                <a class="watch-btn disabled" href="/watch/{{ m.id }}">Detay</a>
              {% endif %}
            </div>
          </article>
        {% endfor %}
      </div>
    {% else %}
      <p style="color:#9ca3af;">Henüz içerik eklenmemiş.</p>
    {% endif %}
  </main>

  <footer>MEDUSAFILM</footer>
</body>
</html>
"""

WATCH_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{{ movie.title }} — MEDUSAFILM</title>
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
      justify-content: space-between;
      align-items: center;
    }
    .brand { color: #f59e0b; font-weight: 800; text-decoration: none; font-size: 1.2rem; }
    .back-btn {
      color: #e5e7eb;
      background: #1d2332;
      border: 1px solid #2c354b;
      padding: 7px 13px;
      border-radius: 8px;
      text-decoration: none;
      font-size: 0.9rem;
    }
    .wrap { max-width: 960px; margin: 0 auto; padding: 20px 16px 40px; }
    .player-box {
      background: #07090d;
      border: 1px solid #232b3c;
      border-radius: 12px;
      overflow: hidden;
      aspect-ratio: 16 / 9;
      margin-bottom: 14px;
    }
    .player-box video, .player-box iframe {
      width: 100%;
      height: 100%;
      border: 0;
      display: block;
    }
    .promo-banner {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 20px;
      text-align: center;
      background: linear-gradient(135deg, #171c29, #0d1017);
      gap: 8px;
    }
    .actions { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 18px; }
    .ext-btn {
      background: #22c55e;
      color: #07130a;
      text-decoration: none;
      padding: 9px 14px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.9rem;
    }
    .info-box {
      background: #151a24;
      border: 1px solid #232b3c;
      border-radius: 12px;
      padding: 16px;
    }
    .title { font-size: 1.35rem; font-weight: 800; margin-bottom: 6px; }
    .meta { color: #9ca3af; font-size: 0.9rem; margin-bottom: 12px; }
    .desc { color: #cbd5e1; line-height: 1.55; }
  </style>
</head>
<body>
  <header>
    <a class="brand" href="/">MEDUSAFILM</a>
    <a class="back-btn" href="/">← Geri Dön</a>
  </header>

  <main class="wrap">
    <div class="player-box">
      {% if movie.valid_source and movie.is_video_file %}
        <video controls autoplay playsinline src="{{ movie.source_url }}"></video>
      {% elif movie.valid_source %}
        <iframe src="{{ movie.source_url }}" allowfullscreen referrerpolicy="no-referrer"></iframe>
      {% else %}
        <div class="promo-banner">
          <h2 style="font-size:1.25rem;">{{ movie.title }}</h2>
          <p style="color:#9ca3af;">{{ movie.release_date }}</p>
        </div>
      {% endif %}
    </div>

    {% if movie.valid_source %}
      <div class="actions">
        <a class="ext-btn" href="{{ movie.source_url }}" target="_blank" rel="noopener noreferrer">
          Yeni Sekmede Aç
        </a>
      </div>
    {% endif %}

    <div class="info-box">
      <h1 class="title">{{ movie.title }}</h1>
      <div class="meta">{{ movie.release_date }}</div>
      {% if movie.overview %}
        <p class="desc">{{ movie.overview }}</p>
      {% endif %}
    </div>
  </main>
</body>
</html>
"""

ADMIN_LOGIN_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Yönetim Girişi — MEDUSAFILM</title>
  <style>
    body {
      background: #0d0f14;
      color: #f3f4f6;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 16px;
    }
    .box {
      background: #151a24;
      border: 1px solid #262f42;
      border-radius: 12px;
      padding: 24px;
      width: 100%;
      max-width: 380px;
    }
    h1 { font-size: 1.25rem; margin-bottom: 14px; color: #f59e0b; }
    input {
      width: 100%;
      padding: 11px 12px;
      border-radius: 8px;
      border: 1px solid #2d374c;
      background: #0e1118;
      color: #fff;
      margin-bottom: 12px;
      font-size: 1rem;
    }
    button {
      width: 100%;
      padding: 11px;
      border: none;
      border-radius: 8px;
      background: #f59e0b;
      color: #111827;
      font-weight: 700;
      font-size: 1rem;
      cursor: pointer;
    }
    .err { color: #f87171; font-size: 0.9rem; margin-bottom: 10px; }
  </style>
</head>
<body>
  <form class="box" method="post">
    <h1>MEDUSAFILM Admin Giriş</h1>
    {% if error %}<div class="err">{{ error }}</div>{% endif %}
    <input type="hidden" name="action" value="login" />
    <input type="password" name="password" placeholder="Yönetim şifresi" required />
    <button type="submit">Gi
