import html
import os
from urllib.parse import quote, urlparse
import requests
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

TMDB_KEY = os.environ.get("TMDB_KEY", "").strip()
IMG_BASE = "https://image.tmdb.org/t/p/w500"

UPCOMING_PROMOS = [
    {
        "title": "Avengers: Doomsday",
        "year": 2026,
        "release_date": "18 Aralık 2026",
        "poster_url": "",
        "accent": "#ef4444",
        "overview": "MCU'nun yeni büyük buluşması ve yaklaşan vizyon filmi.",
        "trailer_url": "",
    },
    {
        "title": "Dune: Part Three",
        "year": 2026,
        "release_date": "18 Aralık 2026",
        "poster_url": "",
        "accent": "#f59e0b",
        "overview": "Arrakis destanının devamı ve vizyona girecek yeni film.",
        "trailer_url": "",
    },
    {
        "title": "The Angry Birds Movie 3",
        "year": 2026,
        "release_date": "23 Aralık 2026",
        "poster_url": "",
        "accent": "#22c55e",
        "overview": "Animasyon serisinin yaklaşan yeni vizyon yapımı.",
        "trailer_url": "",
    },
    {
        "title": "Jumanji: Open World",
        "year": 2026,
        "release_date": "25 Aralık 2026",
        "poster_url": "",
        "accent": "#10b981",
        "overview": "Macera serisinin vizyona girecek yeni filmi.",
        "trailer_url": "",
    },
    {
        "title": "The Beekeeper 2",
        "year": 2027,
        "release_date": "15 Ocak 2027",
        "poster_url": "",
        "accent": "#eab308",
        "overview": "Aksiyon devam filmi vizyon takviminde.",
        "trailer_url": "",
    },
    {
        "title": "Ice Age: Boiling Point",
        "year": 2027,
        "release_date": "5 Şubat 2027",
        "poster_url": "",
        "accent": "#38bdf8",
        "overview": "Buz Devri serisinin yaklaşan yeni macerası.",
        "trailer_url": "",
    },
    {
        "title": "Sonic the Hedgehog 4",
        "year": 2027,
        "release_date": "19 Mart 2027",
        "poster_url": "",
        "accent": "#3b82f6",
        "overview": "Sonic serisinin vizyona çıkacak yeni filmi.",
        "trailer_url": "",
    },
    {
        "title": "Godzilla x Kong: Supernova",
        "year": 2027,
        "release_date": "26 Mart 2027",
        "poster_url": "",
        "accent": "#f97316",
        "overview": "MonsterVerse'ün yaklaşan yeni dev kapışması.",
        "trailer_url": "",
    },
    {
        "title": "Avengers: Secret Wars",
        "year": 2027,
        "release_date": "17 Aralık 2027",
        "poster_url": "",
        "accent": "#a855f7",
        "overview": "Çoklu evren finaline doğru yaklaşan büyük yapım.",
        "trailer_url": "",
    },
    {
        "title": "The Batman: Part II",
        "year": 2028,
        "release_date": "Şubat 2028",
        "poster_url": "",
        "accent": "#94a3b8",
        "overview": "Gotham evreninin beklenen devam filmi.",
        "trailer_url": "",
    },
]

POSTER_CACHE = {}


def is_safe_http_url(url: str) -> bool:
    if not url:
        return False
    parsed = urlparse(url.strip())
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def get_poster(title: str, year=None):
    if not TMDB_KEY or not title:
        return None

    cache_key = f"{title.strip().lower()}|{year or ''}"
    if cache_key in POSTER_CACHE:
        return POSTER_CACHE[cache_key]

    try:
        params = {
            "api_key": TMDB_KEY,
            "query": title,
            "language": "tr-TR",
        }
        if year:
            params["year"] = year

        r = requests.get(
            "https://api.themoviedb.org/3/search/movie",
            params=params,
            timeout=10,
        )
        r.raise_for_status()
        results = r.json().get("results", [])
        for m in results:
            if m.get("poster_path"):
                url = IMG_BASE + m["poster_path"]
                POSTER_CACHE[cache_key] = url
                return url
    except Exception:
        pass

    POSTER_CACHE[cache_key] = None
    return None


def build_svg_poster(title: str, release_date: str, accent: str) -> str:
    safe_title = html.escape(title)
    safe_date = html.escape(release_date)
    safe_accent = accent if accent.startswith("#") and len(accent) in (4, 7) else "#f59e0b"

    words = safe_title.split()
    lines = []
    current = ""
    for w in words:
        test = f"{current} {w}".strip()
        if len(test) <= 14:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    lines = lines[:4]

    start_y = 195 - (len(lines) - 1) * 18
    tspans = "".join(
        f'<tspan x="200" dy="{0 if idx == 0 else 36}">{line}</tspan>'
        for idx, line in enumerate(lines)
    )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="600" viewBox="0 0 400 600">'
        f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="#1b2234"/>'
        f'<stop offset="55%" stop-color="#10141f"/>'
        f'<stop offset="100%" stop-color="#090b10"/>'
        f'</linearGradient></defs>'
        f'<rect width="400" height="600" fill="url(#bg)"/>'
        f'<circle cx="200" cy="215" r="115" fill="{safe_accent}" fill-opacity="0.16"/>'
        f'<rect x="28" y="28" width="344" height="544" rx="18" fill="none" stroke="{safe_accent}" stroke-opacity="0.45" stroke-width="2"/>'
        f'<text x="200" y="{start_y}" text-anchor="middle" fill="#ffffff" font-family="Arial,sans-serif" font-size="30" font-weight="800">{tspans}</text>'
        f'<rect x="95" y="455" width="210" height="34" rx="17" fill="{safe_accent}" fill-opacity="0.22"/>'
        f'<text x="200" y="477" text-anchor="middle" fill="{safe_accent}" font-family="Arial,sans-serif" font-size="15" font-weight="700">{safe_date}</text>'
        f'<text x="200" y="535" text-anchor="middle" fill="#94a3b8" font-family="Arial,sans-serif" font-size="13" font-weight="700" letter-spacing="2">MEDUSAFILM</text>'
        f'</svg>'
    )
    return "data:image/svg+xml;utf8," + quote(svg)


def rank_promos(items: list[dict], raw_q: str) -> list[dict]:
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

    matched.sort(key=lambda x: x["_score"])
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

    promo_cards = []
    if tab == "vizyonda":
        prepared = []
        for p in UPCOMING_PROMOS:
            item = dict(p)
            manual_poster = (item.get("poster_url") or "").strip()
            tmdb_poster = manual_poster if is_safe_http_url(manual_poster) else get_poster(item.get("title", ""), item.get("year"))
            fallback_svg = build_svg_poster(
                item.get("title", ""),
                item.get("release_date", ""),
                item.get("accent", "#f59e0b"),
            )
            item["display_poster"] = tmdb_poster if is_safe_http_url(tmdb_poster or "") else fallback_svg
            item["fallback_poster"] = fallback_svg
            item["valid_trailer"] = is_safe_http_url((item.get("trailer_url") or "").strip())
            prepared.append(item)
        promo_cards = rank_promos(prepared, raw_q)

    return render_template_string(
        MENU_HTML,
        query=raw_q,
        active_tab=tab,
        promo_cards=promo_cards,
    )


@app.route("/watch/<int:movie_id>")
def watch_movie(movie_id: int):
    return redirect("/")


MENU_HTML = """
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
    .badge {
      position: absolute;
      top: 8px;
      left: 8px;
      background: rgba(245, 158, 11, 0.95);
      color: #111827;
      font-size: 0.72rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
      z-index: 2;
    }
    .poster {
      aspect-ratio: 2 / 3;
      background: #0d1017;
      overflow: hidden;
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
      gap: 6px;
      flex: 1;
    }
    .title { font-size: 0.98rem; font-weight: 700; }
    .meta { font-size: 0.8rem; color: #f59e0b; font-weight: 600; }
    .overview {
      font-size: 0.82rem;
      color: #cbd5e1;
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .promo-link {
      margin-top: auto;
      display: inline-block;
      text-align: center;
      text-decoration: none;
      padding: 7px 10px;
      border-radius: 8px;
      font-size: 0.84rem;
      font-weight: 700;
      background: #2563eb;
      color: #fff;
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

    {% if active_tab == 'vizyonda' %}
      {% if promo_cards %}
        <div class="grid">
          {% for c in promo_cards %}
            <article class="card">
              <span class="badge">YAKINDA VİZYONDA</span>
              <div class="poster">
                <img src="{{ c.display_poster }}" alt="{{ c.title }}" loading="lazy" onerror="this.onerror=null; this.src='{{ c.fallback_poster }}';" />
              </div>
              <div class="card-body">
                <div class="title">{{ c.title }}</div>
                <div class="meta">{{ c.release_date }}</div>
                {% if c.overview %}
                  <p class="overview">{{ c.overview }}</p>
                {% endif %}
                {% if c.valid_trailer %}
                  <a class="promo-link" href="{{ c.trailer_url }}" target="_blank" rel="noopener noreferrer">Tanıtımı Aç</a>
                {% endif %}
              </div>
            </article>
          {% endfor %}
        </div>
      {% else %}
        <p style="color:#9ca3af;">Aramanla eşleşen vizyon tanıtımı bulunamadı.</p>
      {% endif %}
    {% endif %}
  </main>
</body>
</html>
