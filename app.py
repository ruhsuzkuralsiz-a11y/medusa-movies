import os
from urllib.parse import urlparse
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

SUPPORT_URL = os.environ.get("SUPPORT_URL", "https://www.instagram.com/ttlewiss21/").strip()

ITEMS = [
    {
        "tab": "paketler",
        "badge": "TEKİL İŞ",
        "title": "Özel Görsel, Afiş & Duyuru Kartı",
        "tag": "Sipariş / Hazırlık",
        "summary": "Yayın afişi, etkinlik duyurusu veya profil/kapak görseli hazırlanır. İsteğini ve tarzını yazarak hızlıca fiyat ve teslim süresi alabilirsin.",
        "action_label": "Sipariş Ver",
        "action_url": SUPPORT_URL,
    },
    {
        "tab": "paketler",
        "badge": "PAKET",
        "title": "Yayıncı & Oyuncu Görsel Paketi",
        "tag": "Çoklu Parça",
        "summary": "Profil görseli, banner/afiş ve duyuru/kural kartı düzeni tek pakette hazırlanır. Tek tek uğraşmak yerine bütünlüklü görünüm isteyenler için uygundur.",
        "action_label": "Paket Sor",
        "action_url": SUPPORT_URL,
    },
    {
        "tab": "paketler",
        "badge": "ÖZEL İSTEK",
        "title": "Kişiye Özel Düzen & Ek Talepler",
        "tag": "Birebir Çalışma",
        "summary": "Mevcut görsel düzenleme, özel tema veya ekstra parça talepleri netleştirilir. Önce ne istediğini yaz, ona göre net dönüş yapalım.",
        "action_label": "Detay Yaz",
        "action_url": SUPPORT_URL,
    },
    {
        "tab": "kurallar",
        "badge": "KURAL",
        "title": "Sipariş & Yayın Kuralları",
        "tag": "Net İşleyiş",
        "summary": "Özel işlerde önce istek ve detaylar netleşir. Yayında ve sohbetlerde spam, hakaret ve gereksiz oyalama yapılmaması esastır.",
        "action_label": "",
        "action_url": "",
    },
    {
        "tab": "kurallar",
        "badge": "İLETİŞİM",
        "title": "Doğrudan İletişim & Destek",
        "tag": "Tek Kanal",
        "summary": "Fiyat sormak, özel iş vermek veya yayın desteği konuşmak için tek iletişim bağlantısı üzerinden doğrudan mesaj bırakabilirsin.",
        "action_label": "Mesaj Gönder",
        "action_url": SUPPORT_URL,
    },
]


def is_safe_http_url(url: str) -> bool:
    if not url:
        return False
    parsed = urlparse(url.strip())
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def filter_items(items: list[dict], tab: str, raw_q: str) -> list[dict]:
    q_norm = " ".join(raw_q.lower().split())
    terms = [t for t in q_norm.split(" ") if t]

    result = []
    for item in items:
        if tab != "tumu" and item.get("tab") != tab:
            continue

        haystack = " ".join([
            item.get("title", ""),
            item.get("tag", ""),
            item.get("badge", ""),
            item.get("summary", ""),
        ]).lower()
        haystack = " ".join(haystack.split())

        if all(t in haystack for t in terms):
            copy_item = dict(item)
            copy_item["has_action"] = is_safe_http_url(copy_item.get("action_url", ""))
            result.append(copy_item)

    return result


@app.route("/")
@app.route("/makine")
def home():
    tab = request.args.get("tab", "paketler").strip().lower()
    if tab not in ("paketler", "kurallar", "tumu"):
        tab = "paketler"

    raw_q = request.args.get("q", "").strip()
    cards = filter_items(ITEMS, tab, raw_q)

    return render_template_string(
        HUB_HTML,
        query=raw_q,
        active_tab=tab,
        cards=cards,
        support_url=SUPPORT_URL if is_safe_http_url(SUPPORT_URL) else "#",
    )


@app.route("/watch/<int:movie_id>")
def watch_movie(movie_id: int):
    return redirect("/")


@app.errorhandler(404)
def not_found_redirect(e):
    return redirect("/")


HUB_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MEDUSA MERKEZ</title>
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
      font-size: 1.25rem;
      font-weight: 800;
      letter-spacing: 0.8px;
      color: #f59e0b;
      text-decoration: none;
    }
    .nav-btn.support {
      text-decoration: none;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 0.9rem;
      font-weight: 700;
      background: #22c55e;
      color: #07130a;
    }
    .container {
      max-width: 1000px;
      margin: 0 auto;
      padding: 20px 16px 40px;
    }
    .hero {
      background: #151a24;
      border: 1px solid #232b3c;
      border-radius: 12px;
      padding: 16px;
      margin-bottom: 16px;
    }
    .hero h1 {
      font-size: 1.15rem;
      margin-bottom: 6px;
      color: #fff;
    }
    .hero p {
      font-size: 0.9rem;
      color: #cbd5e1;
      line-height: 1.45;
    }
    .tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 14px;
    }
    .tab-btn {
      text-decoration: none;
      padding: 8px 15px;
      border-radius: 20px;
      font-size: 0.88rem;
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
      font-size: 0.98rem;
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
      grid-template-columns: 1fr;
      gap: 14px;
    }
    @media (min-width: 720px) {
      .grid { grid-template-columns: repeat(2, 1fr); gap: 16px; }
    }
    .card {
      background: #151a24;
      border: 1px solid #232b3c;
      border-radius: 12px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .card-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .badge {
      background: rgba(245, 158, 11, 0.16);
      color: #f59e0b;
      border: 1px solid rgba(245, 158, 11, 0.35);
      font-size: 0.72rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
    }
    .tag {
      font-size: 0.78rem;
      color: #94a3b8;
      font-weight: 600;
    }
    .title {
      font-size: 1.05rem;
      font-weight: 700;
      color: #fff;
    }
    .summary {
      font-size: 0.88rem;
      color: #cbd5e1;
      line-height: 1.5;
    }
    .card-btn {
      margin-top: auto;
      align-self: flex-start;
      text-decoration: none;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 0.86rem;
      font-weight: 700;
      background: #2563eb;
      color: #fff;
    }
  </style>
</head>
<body>
  <header>
    <a class="brand" href="/">MEDUSA MERKEZ</a>
    <a class="nav-btn support" href="{{ support_url }}" target="_blank" rel="noopener">Destek & İletişim</a>
  </header>

  <main class="container">
    <section class="hero">
      <h1>Özel Görsel, Afiş & Düzen Sipariş Merkezi</h1>
      <p>Yayın ve profil görselleri, afişler ve özel düzen talepleri için tek merkez. İsteğini seçip doğrudan yazabilirsin.</p>
    </section>

    <div class="tabs">
      <a class="tab-btn {% if active_tab == 'paketler' %}active{% endif %}" href="/?tab=paketler{% if query %}&q={{ query }}{% endif %}">Paketler & İşler</a>
      <a class="tab-btn {% if active_tab == 'kurallar' %}active{% endif %}" href="/?tab=kurallar{% if query %}&q={{ query }}{% endif %}">Kurallar & İletişim</a>
      <a class="tab-btn {% if active_tab == 'tumu' %}active{% endif %}" href="/?tab=tumu{% if query %}&q={{ query }}{% endif %}">Tümü</a>
    </div>

    <form class="search-form" method="get" action="/">
      <input type="hidden" name="tab" value="{{ active_tab }}" />
      <input class="search-input" type="text" name="q" value="{{ query }}" placeholder="Paket, afiş veya iletişim ara..." />
      <button class="search-btn" type="submit">Ara</button>
    </form>

    {% if cards %}
      <div class="grid">
        {% for c in cards %}
          <article class="card">
            <div class="card-top">
              <span class="badge">{{ c.badge }}</span>
              <span class="tag">{{ c.tag }}</span>
            </div>
            <div class="title">{{ c.title }}</div>
            <p class="summary">{{ c.summary }}</p>
            {% if c.has_action %}
              <a class="card-btn" href="{{ c.action_url }}" target="_blank" rel="noopener noreferrer">{{ c.action_label }}</a>
            {% endif %}
          </article>
        {% endfor %}
      </div>
    {% else %}
      <p style="color:#9ca3af;">Aramanla eşleşen bir kayıt bulunamadı.</p>
    {% endif %}
  </main>
</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
