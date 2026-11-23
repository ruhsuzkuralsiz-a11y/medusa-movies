import os
from urllib.parse import urlparse
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# Vizyonda sekmesinde gösterilecek çıkacak filmlerin tanıtım / afiş kartları
# Kendi istediğin filmleri ve afiş (poster) URL'lerini buradan ekleyip güncelleyebilirsin.
UPCOMING_PROMOS = [
    {
        "title": "Avengers: Doomsday",
        "release_date": "Yakında Vizyonda",
        "poster_url": "https://image.tmdb.org/t/p/w500/8x53328533285332853328533.jpg",
        "overview": "Henüz vizyona girmemiş yapım — yeni tanıtım ve afiş vitrini.",
        "trailer_url": "",
    },
    {
        "title": "Spider-Man: Brand New Day",
        "release_date": "Yakında Vizyonda",
        "poster_url": "",
        "overview": "Vizyona çıkacak yeni yapım tanıtım kartı.",
        "trailer_url": "",
    },
    {
        "title": "Dune: Messiah",
        "release_date": "Yakında Vizyonda",
        "poster_url": "",
        "overview": "Yaklaşan sinema projesi afiş vitrini.",
        "trailer_url": "",
    },
    {
        "title": "The Batman Part II",
        "release_date": "Yakında Vizyonda",
        "poster_url": "",
        "overview": "Vizyon takvimindeki yeni film tanıtımı.",
        "trailer_url": "",
    },
]


def is_safe_http_url(url: str) -> bool:
    if not url:
        return False
    parsed = urlparse(url.strip())
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


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
            raw_poster = (item.get("poster_url") or "").strip()
            raw_trailer = (item.get("trailer_url") or "").strip()
            item["valid_poster"] = is_safe_http_url(raw_poster)
            item["valid_trailer"] = is_safe_http_url(raw_trailer)
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
      background: linear-gradient(160deg, #1b2232, #0d1017);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 12px;
      text-align: center;
    }
    .poster img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
    .poster-placeholder {
      color: #94a3b8;
      font-size: 0.85rem;
      font-weight: 700;
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
                {% if c.valid_poster %}
                  <img src="{{ c.poster_url }}" alt="{{ c.title }}" loading="lazy" />
                {% else %}
                  <span class="poster-placeholder">{{ c.title }}</span>
                {% endif %}
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
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
