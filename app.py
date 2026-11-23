import os
import sqlite3
from datetime import datetime, timezone
from urllib.parse import urlparse
import requests
from flask import (
    Flask,
    render_template_string,
    request,
    redirect,
    jsonify,
    session,
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "medusafilm-gizli-anahtar-degistir")

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "").strip()
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "medusa123").strip()
CRON_TOKEN = os.environ.get("CRON_TOKEN", "medusa-cron-gizli-token").strip()
DEFAULT_MIN_DATE = os.environ.get("MIN_RELEASE_DATE", "2020-01-01").strip()

DB_PATH = os.environ.get("DB_PATH", "movies.db")
TMDB_DISCOVER_URL = "https://api.themoviedb.org/3/discover/movie"
TMDB_UPCOMING_URL = "https://api.themoviedb.org/3/movie/upcoming"
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
                source_url TEXT DEFAULT '',
                is_upcoming INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        cols = [r["name"] for r in conn.execute("PRAGMA table_info(movies)").fetchall()]
        if "source_url" not in cols:
            conn.execute("ALTER TABLE movies ADD COLUMN source_url TEXT DEFAULT ''")
        if "is_upcoming" not in cols:
            conn.execute("ALTER TABLE movies ADD COLUMN is_upcoming INTEGER NOT NULL DEFAULT 0")

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


def is_safe_http_url(url: str) -> bool:
    if not url:
        return False
    parsed = urlparse(url.strip())
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def is_direct_video_url(url: str) -> bool:
    path = urlparse(url.strip()).path.lower()
    return path.endswith((".mp4", ".webm", ".ogg", ".m3u8"))


def fetch_from_tmdb(min_date: str | None = None, pages: int = 2) -> dict:
    if not TMDB_API_KEY:
        return {"ok": False, "error": "TMDB_API_KEY ayarlanmamış.", "added": 0, "skipped": 0}

    date_filter = (min_date or get_setting("min_release_date", DEFAULT_MIN_DATE)).strip()
    now_iso = datetime.now(timezone.utc).isoformat()
    added = 0
    skipped = 0

    try:
        with get_db() as conn:
            # 1) Genel popüler filmler
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
                for item in resp.json().get("results", []):
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
                            source_url, is_upcoming, status, created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, '', 0, 'pending', ?, ?)
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

            # 2) Yakında vizyona girecek filmler (Vizyonda reklam sekmesi için)
            up_resp = requests.get(
                TMDB_UPCOMING_URL,
                params={
                    "api_key": TMDB_API_KEY,
                    "language": "tr-TR",
                    "page": 1,
                },
                timeout=12,
            )
            if up_resp.ok:
                for item in up_resp.json().get("results", [])[:12]:
                    tmdb_id = item.get("id")
                    if not tmdb_id:
                        continue
                    exists = conn.execute(
                        "SELECT id FROM movies WHERE tmdb_id = ?", (tmdb_id,)
                    ).fetchone()
                    if exists:
                        conn.execute(
                            "UPDATE movies SET is_upcoming = 1, updated_at = ? WHERE id = ?",
                            (now_iso, exists["id"]),
                        )
                        continue

                    title = item.get("title") or item.get("original_title") or "Yakında Vizyonda"
                    poster_path = item.get("poster_path")
                    poster_url = f"{IMG_BASE}{poster_path}" if poster_path else ""
                    overview = item.get("overview") or "Yakında vizyona girecek film tanıtımı."
                    rating = round(float(item.get("vote_average") or 0), 1)
                    release_date = item.get("release_date") or "Yakında"

                    conn.execute(
                        """
                        INSERT INTO movies (
                            tmdb_id, title, poster_url, overview, rating, release_date,
                            source_url, is_upcoming, status, created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, '', 1, 'pending', ?, ?)
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
        if (now - last_fetch).total_seconds() >= 86400:
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
        key=lambda x: (x["_score"], x.get("release_date") or "", x.get("id") or 0),
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
                WHERE status = 'approved' AND is_upcoming = 1
                ORDER BY release_date ASC, id DESC
                """
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT * FROM movies
                WHERE status = 'approved'
                ORDER BY release_date DESC, id DESC
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
        row = conn.execute(
            "SELECT * FROM movies WHERE id = ? AND status = 'approved'",
            (movie_id,),
        ).fetchone()

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

            if action == "add_promo":
                title = request.form.get("promo_title", "").strip()
                poster_url = request.form.get("promo_poster", "").strip()
                release_date = request.form.get("promo_date", "").strip() or "Yakında"
                overview = request.form.get("promo_overview", "").strip() or "Vizyona çıkacak özel tanıtım."
                source_url = request.form.get("promo_source", "").strip()

                if not title:
                    error = "Tanıtım için film adı girmelisin."
                elif poster_url and not is_safe_http_url(poster_url):
                    error = "Afiş URL'si http:// veya https:// ile başlamalı."
                elif source_url and not is_safe_http_url(source_url):
                    error = "Fragman/Kaynak URL'si http:// veya https:// ile başlamalı."
                else:
                    fake_tmdb_id = -int(datetime.now(timezone.utc).timestamp() * 1000)
                    with get_db() as conn:
                        conn.execute(
                            """
                            INSERT INTO movies (
                                tmdb_id, title, poster_url, overview, rating, release_date,
                                source_url, is_upcoming, status, created_at, updated_at
                            ) VALUES (?, ?, ?, ?, 0, ?, ?, 1, 'approved', ?, ?)
                            """,
                            (
                                fake_tmdb_id,
                                title,
                                poster_url,
                                overview,
                                release_date,
                                source_url,
                                now_iso,
                                now_iso,
                            ),
                        )
                        conn.commit()
                    message = f"'{title}' Vizyonda tanıtım kartı olarak eklendi."

            elif action == "save_date":
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
                source_url = request.form.get("source_url", "").strip()
                is_upcoming = 1 if request.form.get("is_upcoming") == "1" else 0
                if source_url and not is_safe_http_url(source_url):
                    error = "Kaynak bağlantısı http:// veya https:// ile başlamalı."
                else:
                    with get_db() as conn:
                        conn.execute(
                            """
                            UPDATE movies
                            SET status = 'approved', source_url = ?, is_upcoming = ?, updated_at = ?
                            WHERE id = ?
                            """,
                            (source_url, is_upcoming, now_iso, movie_id),
                        )
                        conn.commit()
                    message = "Film onaylandı."

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

            elif action == "update_source":
                movie_id = request.form.get("movie_id")
                source_url = request.form.get("source_url", "").strip()
                is_upcoming = 1 if request.form.get("is_upcoming") == "1" else 0
                if source_url and not is_safe_http_url(source_url):
                    error = "Kaynak bağlantısı http:// veya https:// ile başlamalı."
                else:
                    with get_db() as conn:
                        conn.execute(
                            "UPDATE movies SET source_url = ?, is_upcoming = ?, updated_at = ? WHERE id = ?",
                            (source_url, is_upcoming, now_iso, movie_id),
                        )
                        conn.commit()
                    message = "Film ayarları güncellendi."

    if not is_admin():
        return render_template_string(ADMIN_LOGIN_HTML, error=error)

    with get_db() as conn:
        pending_rows = conn.execute(
            "SELECT * FROM movies WHERE status = 'pending' ORDER BY release_date DESC, id DESC"
        ).fetchall()
        approved_rows = conn.execute(
            "SELECT * FROM movies WHERE status = 'approved' ORDER BY id DESC LIMIT 30"
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
        approved_movies=[dict(r) for r in approved_rows],
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
  <title>MEDUSAFILM</titl
