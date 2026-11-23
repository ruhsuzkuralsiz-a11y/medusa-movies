import os
import sqlite3
from datetime import datetime, timezone
import requests
from flask import (
    Flask,
    render_template_string,
    request,
    redirect,
    url_for,
    jsonify,
    session,
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "medusafilm-gizli-anahtar-degistir")

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "BURAYA_TMDB_API_KEY_YAZ")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "medusa123")
CRON_TOKEN = os.environ.get("CRON_TOKEN", "medusa-cron-gizli-token")
DEFAULT_MIN_DATE = os.environ.get("MIN_RELEASE_DATE", "2020-01-01")

DB_PATH = os.environ.get("DB_PATH", "movies.db")
TMDB_DISCOVER_URL = "https://api.themoviedb.org/3/discover/movie"
IMG_BASE = "https://image.tmdb.org/t/p/w500"


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
                tmdb_id INTEGER UNIQUE NOT NULL,
                title TEXT NOT NULL,
                poster_url TEXT,
                overview TEXT,
                rating REAL DEFAULT 0,
                release_date TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            INSERT OR IGNORE INTO settings (key, value)
            VALUES ('min_release_date', ?)
            """,
            (DEFAULT_MIN_DATE,),
        )
        conn.execute(
            """
            INSERT OR IGNORE INTO settings (key, value)
            VALUES ('last_auto_fetch', '')
            """
        )
        conn.commit()


def get_setting(key: str, default: str = "") -> str:
    with get_db() as conn:
        row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else default


def set_setting(key: str, value: str):
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO settings (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """,
            (key, value),
        )
        conn.commit()


def fetch_from_tmdb(min_date: str | None = None, pages: int = 2) -> dict:
    if not TMDB_API_KEY or TMDB_API_KEY == "BURAYA_TMDB_API_KEY_YAZ":
        return {"ok": False, "error": "TMDB_API_KEY ayarlanmamış.", "added": 0, "skipped": 0}

    date_filter = (min_date or get_setting("min_release_date", DEFAULT_MIN_DATE)).strip()
    now_iso = datetime.now(timezone.utc).isoformat()
    added = 0
    skipped = 0

    try:
        with get_db() as conn:
            for page in range(1, pages + 1):
                resp = requests.get(
                    TMDB_DISCOVER_URL,
                    params={
                        "api_key": TMDB_API_KEY,
                        "language": "tr-TR",
                        "primary_release_date.gte": date_filter,
                        "sort_by": "popularity.desc",
                        "page": page,
                    },
                    timeout=12,
                )
                resp.raise_for_status()
                results = resp.json().get("results", [])
                if not results:
                    break

                for item in results:
                    tmdb_id = item.get("id")
                    if not tmdb_id:
                        continue

                    exists = conn.execute(
                        "SELECT id FROM movies WHERE tmdb_id = ?", (tmdb_id,)
                    ).fetchone()
                    if exists:
                        skipped += 1
                        continue

                    title = item.get("title") or item.get("original_title") or "İsimsiz Film"
                    poster_path = item.get("poster_path")
                    poster_url = f"{IMG_BASE}{poster_path}" if poster_path else ""
                    overview = item.get("overview") or "Özet bilgisi bulunmuyor."
                    rating = round(float(item.get("vote_average") or 0), 1)
                    release_date = item.get("release_date") or "—"

                    conn.execute(
                        """
                        INSERT INTO movies (
                            tmdb_id, title, poster_url, overview, rating, release_date,
                            status, created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, 'pending', ?, ?)
                        """,
                        (
                            tmdb_id,
                            title,
                            poster_url,
                            overview,
                            rating,
                            release_date,
                            now_iso,
                            now_iso,
                        ),
                    )
                    added += 1

            conn.commit()

        set_setting("last_auto_fetch", now_iso)
        return {"ok": True, "added": added, "skipped": skipped, "min_date": date_filter}
    except Exception as exc:
        return {"ok": False, "error": str(exc), "added": added, "skipped": skipped}


def maybe_run_daily_fetch():
    last_fetch_str = get_setting("last_auto_fetch", "")
    now = datetime.now(timezone.utc)
    if not last_fetch_str:
        fetch_from_tmdb(pages=2)
        return
    try:
        last_fetch = datetime.fromisoformat(last_fetch_str)
        if last_fetch.tzinfo is None:
            last_fetch = last_fetch.replace(tzinfo=timezone.utc)
        elapsed_seconds = (now - last_fetch).total_seconds()
        if elapsed_seconds >= 86400:  # 24 saat geçtiyse
            fetch_from_tmdb(pages=2)
    except Exception:
        fetch_from_tmdb(pages=2)


def is_admin() -> bool:
    return session.get("admin_logged_in") is True


init_db()


@app.before_request
def before_any_request():
    if request.endpoint not in ("static",):
        maybe_run_daily_fetch()


@app.route("/")
def home():
    q = request.args.get("q", "").strip().lower()
    with get_db() as conn:
        if q:
            rows = conn.execute(
                """
                SELECT * FROM movies
                WHERE status = 'approved'
                  AND (LOWER(title) LIKE ? OR LOWER(overview) LIKE ?)
                ORDER BY release_date DESC, id DESC
                """,
                (f"%{q}%", f"%{q}%"),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT * FROM movies
                WHERE status = 'approved'
                ORDER BY release_date DESC, id DESC
                """
            ).fetchall()

    return render_template_string(
        PUBLIC_HTML,
        movies=[dict(r) for r in rows],
        query=request.args.get("q", ""),
    )


@app.route("/admin", methods=["GET", "POST"])
def admin_panel():
    message = None
    error = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "login":
            password = request.form.get("password", "")
            if password == ADMIN_PASSWORD:
                session["admin_logged_in"] = True
                return redirect(url_for("admin_panel"))
            error = "Hatalı şifre."

        elif action == "logout":
            session.pop("admin_logged_in", None)
            return redirect(url_for("admin_panel"))

        elif is_admin():
            now_iso = datetime.now(timezone.utc).isoformat()

            if action == "save_date":
                new_date = request.form.get("min_release_date", "").strip()
                if new_date:
                    set_setting("min_release_date", new_date)
                    message = f"Başlangıç tarihi {new_date} olarak güncellendi."

            elif action == "fetch_now":
                new_date = request.form.get("min_release_date", "").strip()
                if new_date:
                    set_setting("min_release_date", new_date)
                res = fetch_from_tmdb(min_date=new_date or None, pages=2)
                if res["ok"]:
                    message = (
                        f"TMDB çekimi tamamlandı ({res['min_date']} sonrası). "
                        f"Yeni eklenen: {res['added']}, Zaten kayıtlı: {res['skipped']}"
                    )
                else:
                    error = f"Çekim hatası: {res.get('error')}"

            elif action == "approve_one":
                movie_id = request.form.get("movie_id")
                with get_db() as conn:
                    conn.execute(
                        "UPDATE movies SET status = 'approved', updated_at = ? WHERE id = ?",
                        (now_iso, movie_id),
                    )
                    conn.commit()
                message = "Film onaylandı ve yayına alındı."

            elif action == "reject_one":
                movie_id = request.form.get("movie_id")
                with get_db() as conn:
                    conn.execute(
                        "UPDATE movies SET status = 'rejected', updated_at = ? WHERE id = ?",
                        (now_iso, movie_id),
                    )
                    conn.commit()
                message = "Film reddedildi."

            elif action == "approve_all":
                with get_db() as conn:
                    cur = conn.execute(
                        "UPDATE movies SET status = 'approved', updated_at = ? WHERE status = 'pending'",
                        (now_iso,),
                    )
                    conn.commit()
                message = f"{cur.rowcount} bekleyen film toplu olarak onaylandı."

    if not is_admin():
        return render_template_string(ADMIN_LOGIN_HTML, error=error)

    with get_db() as conn:
        pending_rows = conn.execute(
            "SELECT * FROM movies WHERE status = 'pending' ORDER BY release_date DESC, id DESC"
        ).fetchall()
        approved_count = conn.execute(
            "SELECT COUNT(*) AS c FROM movies WHERE status = 'approved'"
        ).fetchone()["c"]
        rejected_count = conn.execute(
            "SELECT COUNT(*) AS c FROM movies WHERE status = 'rejected'"
        ).fetchone()["c"]

    return render_template_string(
        ADMIN_PANEL_HTML,
        pending_movies=[dict(r) for r in pending_rows],
        min_release_date=get_setting("min_release_date", DEFAULT_MIN_DATE),
        last_auto_fetch=get_setting("last_auto_fetch", "Henüz çalışmadı"),
        approved_count=approved_count,
        rejected_count=rejected_count,
        message=message,
        error=error,
    )


@app.route("/cron/fetch")
def cron_fetch():
    token = request.args.get("token", "")
    if token != CRON_TOKEN:
        return jsonify({"ok": False, "error": "Yetkisiz token"}), 403
    res = fetch_from_tmdb(pages=2)
    status_code = 200 if res.get("ok") else 500
    return jsonify(res), status_code


PUBLIC_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MEDUSAFILM — Filmler</title>
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
    .nav-links {
      display: flex;
      align-items: center;
      gap: 10px;
    }
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
    .search-form {
      display: flex;
      gap: 8px;
      margin-bottom: 20px;
    }
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
      .grid {
        grid-template-columns: repeat(4, 1fr);
        gap: 18px;
      }
    }
    .card {
      background: #151a24;
      border: 1px solid #232b3c;
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }
    .poster {
      aspect-ratio: 2 / 3;
      background: #0d1017;
    }
    .poster img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
    .card-body {
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      flex: 1;
    }
    .title {
      font-size: 1rem;
      font-weight: 700;
    }
    .meta {
      display: flex;
      justify-content: space-between;
      font-size: 0.82rem;
      color: #9ca3af;
    }
    .overview {
      font-size: 0.85rem;
      color: #cbd5e1;
      line-height: 1.45;
      display: -webkit-box;
      -webkit-line-clamp: 4;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
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
    <form class="search-form" method="get" action="/">
      <input
        class="search-input"
        type="text"
        name="q"
        value="{{ query }}"
        placeholder="Onaylanmış filmlerde ara..."
      />
      <button class="search-btn" type="submit">Ara</button>
    </form>

    {% if movies %}
      <div class="grid">
        {% for m in movies %}
          <article class="card">
            <div class="poster">
              {% if m.poster_url %}
                <img src="{{ m.poster_url }}" alt="{{ m.title }}" loading="lazy" />
              {% endif %}
            </div>
            <div class="card-body">
              <div class="title">{{ m.title }}</div>
              <div class="meta">
                <span>{{ m.release_date }}</span>
                <span>★ {{ m.rating }}</span>
              </div>
              <p class="overview">{{ m.overview }}</p>
            </div>
          </article>
        {% endfor %}
      </div>
    {% else %}
      <p style="color:#9ca3af;">Henüz onaylanmış film bulunmuyor. Yönetim panelinden yeni filmleri çekip onaylayabilirsin.</p>
    {% endif %}
  </main>

  <footer>
    Bu ürün TMDB API kullanır ancak TMDB tarafından onaylanmamış veya sertifikalandırılmamıştır.
  </footer>
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
    <button type="submit">Giriş Yap</button>
  </form>
</body>
</html>
"""

ADMIN_PANEL_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Onay Kuyruğu — MEDUSAFILM</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0d0f14;
      color: #f3f4f6;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      padding: 16px;
    }
    .wrap { max-width: 1200px; margin: 0 auto; }
    .top {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      margin-bottom: 18px;
      padding-bottom: 12px;
      border-bottom: 1px solid #222938;
    }
    .btn {
      padding: 8px 14px;
      border-radius: 8px;
      border: none;
      font-weight: 700;
      cursor: pointer;
      text-decoration: none;
      font-size: 0.9rem;
    }
    .btn-amber { background: #f59e0b; color: #111827; }
    .btn-green { background: #22c55e; color: #07130a; }
    .btn-red { background: #ef4444; color: #fff; }
    .btn-gray { background: #232a3a; color: #e5e7eb; }
    .panel-box {
      background: #151a24;
      border: 1px solid #232b3c;
      border-radius: 12px;
      padding: 16px;
      margin-bottom: 18px;
    }
    .controls {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }
    input[type="date"] {
      padding: 8px 10px;
      border-radius: 8px;
      border: 1px solid #2f394e;
      background: #0e1118;
      color: #fff;
    }
    .stats {
      margin-top: 10px;
      font-size: 0.88rem;
      color: #9ca3af;
    }
    .msg {
      background: #13281c;
      border: 1px solid #22c55e;
      color: #86efac;
      padding: 10px 14px;
      border-radius: 8px;
      margin-bottom: 14px;
    }
    .err {
      background: #2c1518;
      border: 1px solid #ef4444;
      color: #fca5a5;
      padding: 10px 14px;
      border-radius: 8px;
      margin-bottom: 14px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(1, 1fr);
      gap: 14px;
    }
    @media (min-width: 768px) {
      .grid { grid-template-columns: repeat(2, 1fr); }
    }
    .item {
      background: #151a24;
      border: 1px solid #232b3c;
      bo
