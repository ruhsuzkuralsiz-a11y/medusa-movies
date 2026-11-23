import os
import sqlite3
import time
from functools import wraps
import requests
from flask import (
    Blueprint,
    render_template_string,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)

makine_bp = Blueprint("makine", __name__)

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "").strip()
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "medusa123").strip()
START_DATE = os.environ.get("START_DATE", "2020-01-01").strip()
SYNC_TOKEN = os.environ.get("SYNC_TOKEN", "medusa_gunluk_gizli_anahtar").strip()

DB_PATH = os.environ.get("MAKINE_DB_PATH", "makine_movies.db")
TMDB_DISCOVER_URL = "https://api.themoviedb.org/3/discover/movie"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
TMDB_LOGO_URL = "https://www.themoviedb.org/assets/2/v4/logos/v2/blue_short-8e7b30f73a4020692ccca9c88bafe5dcb6f8a62a4c6bc55cd9ba82bb2cd95f6c.svg"


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
                rating REAL DEFAULT 0.0,
                release_date TEXT,
                status TEXT NOT NULL DEFAULT 'bekliyor',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


init_db()


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("makine_admin_ok"):
            return redirect(url_for("makine.login"))
        return f(*args, **kwargs)

    return decorated


def fetch_tmdb_movies(max_pages=2, delay_seconds=0.35):
    if not TMDB_API_KEY:
        return {"ok": False, "error": "TMDB_API_KEY ayarlanmamış! Render Environment içine ekle."}

    added = 0
    skipped = 0
    pages_fetched = 0

    with get_db() as conn:
        for page in range(1, max_pages + 1):
            params = {
                "api_key": TMDB_API_KEY,
                "language": "tr-TR",
                "sort_by": "popularity.desc",
                "primary_release_date.gte": START_DATE,
                "include_adult": "false",
                "page": page,
            }
            resp = requests.get(TMDB_DISCOVER_URL, params=params, timeout=15)
            if resp.status_code != 200:
                return {
                    "ok": False,
                    "error": f"TMDB hatası (sayfa {page}, kod {resp.status_code}): {resp.text[:200]}",
                }

            data = resp.json()
            results = data.get("results", [])
            pages_fetched += 1
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
                poster_url = f"{TMDB_IMAGE_BASE}{poster_path}" if poster_path else ""
                overview = item.get("overview") or "Özet bulunmuyor."
                rating = round(float(item.get("vote_average") or 0.0), 1)
                release_date = item.get("release_date") or "-"

                conn.execute(
                    """
                    INSERT INTO movies (tmdb_id, title, poster_url, overview, rating, release_date, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'bekliyor')
                    """,
                    (tmdb_id, title, poster_url, overview, rating, release_date),
                )
                added += 1

            conn.commit()
            if page >= data.get("total_pages", 1):
                break
            time.sleep(delay_seconds)

    return {"ok": True, "added": added, "skipped": skipped, "pages": pages_fetched}


TMDB_FOOTER = f"""
<footer style="margin-top:36px;padding:18px;border-top:1px solid #262b3b;text-align:center;color:#9aa0b4;font-size:13px;">
    <div style="display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;">
        <img src="{TMDB_LOGO_URL}" alt="TMDB" style="height:16px;width:auto;">
        <span>Bu ürün TMDB API kullanır ancak TMDB tarafından onaylanmamış veya sertifikalandırılmamıştır.</span>
    </div>
</footer>
"""

STYLE = """
<style>
    * { box-sizing: border-box; font-family: Arial, sans-serif; }
    body { margin: 0; background: #0f1117; color: #f1f3f8; }
    a { color: #58a6ff; text-decoration: none; }
    .wrap { max-width: 1000px; margin: 0 auto; padding: 18px; }
    .bar { display: flex; justify-content: space-between; align-items: center; gap: 10px; flex-wrap: wrap; padding-bottom: 14px; border-bottom: 1px solid #242938; margin-bottom: 20px; }
    .btn { display: inline-block; padding: 8px 13px; border: 0; border-radius: 8px; background: #2563eb; color: #fff; font-weight: bold; cursor: pointer; }
    .green { background: #16a34a; }
    .red { background: #dc2626; }
    .gray { background: #374151; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: 16px; }
    .card { background: #171a24; border: 1px solid #262b3b; border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; }
    .card img { width: 100%; height: 300px; object-fit: cover; background: #0c0e14; }
    .body { padding: 12px; display: flex; flex-direction: column; gap: 7px; flex: 1; }
    .title { margin: 0; font-size: 15px; font-weight: bold; }
    .meta { font-size: 12px; color: #a0a8bd; }
    .desc { font-size: 12px; color: #cbd2e3; max-height: 80px; overflow-y: auto; line-height: 1.35; }
    .msg { padding: 10px 14px; border-radius: 8px; background: #1e293b; border-left: 4px solid #38bdf8; margin-bottom: 14px; }
    .row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: auto; }
    input[type="password"], input[type="number"] { padding: 8px 10px; border-radius: 8px; border: 1px solid #33394d; background: #12151e; color: #fff; }
</style>
"""


@makine_bp.route("/makine")
def vitrin():
    with get_db() as conn:
        movies = conn.execute(
            "SELECT * FROM movies WHERE status = 'onayli' ORDER BY release_date DESC, id DESC"
        ).fetchall()

    cards = ""
    for m in movies:
        poster = m["poster_url"] or "https://via.placeholder.com/500x750?text=Afis+Yok"
        cards += f"""
        <div class="card">
            <img src="{poster}" alt="{m['title']}">
            <div class="body">
                <h3 class="title">{m['title']}</h3>
                <div class="meta">Tarih: {m['release_date']} | ⭐ {m['rating']}</div>
                <div class="desc">{m['overview']}</div>
            </div>
        </div>
        """

    if not cards:
        cards = "<p>Henüz onaylanan film yok.</p>"

    return render_template_string(
        f"""
        <!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Medusa Makine</title>{STYLE}</head>
        <body>
            <div class="wrap">
                <div class="bar">
                    <h2>🎬 Onaylanan Filmler ({START_DATE}+)</h2>
                    <a class="btn gray" href="/makine/panel">Panel</a>
                </div>
                <div class="grid">{cards}</div>
            </div>
            {TMDB_FOOTER}
        </body></html>
        """
    )


@makine_bp.route("/makine/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password", "") == ADMIN_PASSWORD:
            session["makine_admin_ok"] = True
            return redirect(url_for("makine.panel"))
        flash("Şifre hatalı!")

    msgs = "".join(f'<div class="msg">{m}</div>' for m in get_flashed_messages())
    return render_template_string(
        f"""
        <!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Giriş</title>{STYLE}</head>
        <body>
            <div class="wrap" style="max-width:380px;margin-top:50px;">
                <h2>🔐 Makine Panel Girişi</h2>
                {msgs}
                <form method="post" style="display:flex;flex-direction:column;gap:10px;">
                    <input type="password" name="password" placeholder="Şifre" required>
                    <button class="btn" type="submit">Giriş</button>
                </form>
                <p style="margin-top:14px;"><a href="/makine">← Vitrine Dön</a></p>
            </div>
            {TMDB_FOOTER}
        </body></html>
        """
    )


@makine_bp.route("/makine/logout")
def logout():
    session.pop("makine_admin_ok", None)
    return redirect(url_for("makine.login"))


@makine_bp.route("/makine/panel")
@admin_required
def panel():
    with get_db() as conn:
        pending = conn.execute(
            "SELECT * FROM movies WHERE status = 'bekliyor' ORDER BY id DESC"
        ).fetchall()
        approved = conn.execute(
            "SELECT COUNT(*) AS c FROM movies WHERE status = 'onayli'"
        ).fetchone()["c"]

    msgs = "".join(f'<div class="msg">{m}</div>' for m in get_flashed_messages())
    cards = ""
    for m in pending:
        poster = m["poster_url"] or "https://via.placeholder.com/500x750?text=Afis+Yok"
        cards += f"""
        <div class="card">
            <img src="{poster}" alt="{m['title']}">
            <div class="body">
                <label style="display:flex;align-items:center;gap:6px;font-weight:bold;">
                    <input type="checkbox" name="ids" value="{m['id']}"> Seç
                </label>
                <h3 class="title">{m['title']}</h3>
                <div class="meta">{m['release_date']} | ⭐ {m['rating']} | ID:{m['tmdb_id']}</div>
                <div class="desc">{m['overview']}</div>
                <div class="row">
                    <form method="post" action="/makine/durum/{m['id']}/onayli">
                        <button class="btn green" type="submit">Onayla</button>
                    </form>
                    <form method="post" action="/makine/durum/{m['id']}/reddedildi">
                        <button class="btn red" type="submit">Reddet</button>
                    </form>
                </div>
            </div>
        </div>
        """

    if not cards:
        cards = "<p>Bekleyen film yok. Yukarıdan TMDB'den film çekebilirsin.</p>"

    return render_template_string(
        f"""
        <!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Panel</title>{STYLE}</head>
        <body>
            <div class="wrap">
                <div class="bar">
                    <div>
                        <h2>🛠️ Bekleyen: {len(pending)} | Yayında: {approved}</h2>
                        <div class="meta">Başlangıç: <strong>{START_DATE}</strong> (tr-TR)</div>
                    </div>
                    <div class="row" style="margin:0;">
                        <a class="btn gray" href="/makine">Vitrin</a>
                        <a class="btn red" href="/makine/logout">Çıkış</a>
                    </div>
                </div>
                {msgs}
                <form method="post" action="/makine/cek" style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:16px;background:#171a24;padding:12px;border-radius:10px;">
                    <span>Sayfa:</span>
                    <input type="number" name="pages" value="2" min="1" max="10" style="width:68px;">
                    <button class="btn" type="submit">📥 TMDB'den Çek</button>
                </form>
                <form method="post" action="/makine/toplu-onayla">
                    <div style="margin-bottom:14px;">
                        <button class="btn green" type="submit">✅ Seçilenleri Toplu Onayla</button>
                    </div>
                    <div class="grid">{cards}</div>
                </form>
            </div>
            {TMDB_FOOTER}
        </body></html>
        """
    )


@makine_bp.route("/makine/cek", methods=["POST"])
@admin_required
def cek():
    try:
        pages = max(1, min(int(request.form.get("pages", "2")), 10))
    except ValueError:
        pages = 2
    res = fetch_tmdb_movies(max_pages=pages)
    if res["ok"]:
        flash(f"{res['pages']} sayfa tarandı: {res['added']} yeni eklendi, {res['skipped']} atlandı.")
    else:
        flash(res["error"])
    return redirect(url_for("makine.panel"))


@makine_bp.route("/makine/durum/<int:movie_id>/<durum>", methods=["POST"])
@admin_required
def durum_guncelle(movie_id, durum):
    if durum in ("onayli", "reddedildi"):
        with get_db() as conn:
            conn.execute("UPDATE movies SET status = ? WHERE id = ?", (durum, movie_id))
            conn.commit()
        flash("Güncellendi.")
    return redirect(url_for("makine.panel"))


@makine_bp.route("/makine/toplu-onayla", methods=["POST"])
@admin_required
def toplu_onayla():
    ids = request.form.getlist("ids")
    if not ids:
        flash("En az bir film seçmelisin.")
        return redirect(url_for("makine.panel"))
    q = ",".join("?" for _ in ids)
    with get_db() as conn:
        conn.execute(f"UPDATE movies SET status = 'onayli' WHERE id IN ({q})", ids)
        conn.commit()
    flash(f"{len(ids)} film onaylandı!")
    return redirect(url_for("makine.panel"))


@makine_bp.route("/makine/gunluk-cek", methods=["GET", "POST"])
def gunluk_cek():
    token = request.args.get("token") or request.headers.get("X-Sync-Token", "")
    if token != SYNC_TOKEN:
        return jsonify({"ok": False, "error": "Yetkisiz"}), 401
    try:
        pages = max(1, min(int(request.args.get("pages", "2")), 10))
    except ValueError:
        pages = 2
    res = fetch_tmdb_movies(max_pages=pages)
    return jsonify(res), (200 if res["ok"] else 500)
