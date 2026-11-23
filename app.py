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


@app.route("/overlay")
def overlay():
    return render_template_string(OVERLAY_HTML)


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
      <a class="tab-btn" href="/overlay">Yayın Banner</a>
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

OVERLAY_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MEDUSA - Yayın Banner</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', Arial, sans-serif;
    }
    body {
      width: 100vw;
      height: 100vh;
      background: transparent;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      color: #ffffff;
    }
    .top-banner {
      height: 21vh;
      min-height: 125px;
      background: linear-gradient(135deg, rgba(10, 14, 12, 0.96), rgba(18, 34, 24, 0.96));
      border-bottom: 3px solid #39ff14;
      box-shadow: 0 6px 25px rgba(57, 255, 20, 0.25);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 10px 16px;
      text-align: center;
    }
    .brand-title {
      font-size: clamp(2.1rem, 8vw, 3.8rem);
      font-weight: 900;
      letter-spacing: 6px;
      color: #39ff14;
      text-shadow: 0 0 18px rgba(57, 255, 20, 0.65);
      line-height: 1.05;
    }
    .sub-tag {
      margin-top: 6px;
      font-size: 0.9rem;
      font-weight: 700;
      letter-spacing: 2px;
      color: #e6ffe6;
      background: rgba(57, 255, 20, 0.12);
      border: 1px solid rgba(57, 255, 20, 0.45);
      padding: 4px 14px;
      border-radius: 999px;
    }
    .game-area {
      flex: 1;
      background: transparent;
      pointer-events: none;
    }
    .bottom-banner {
      height: 24vh;
      min-height: 152px;
      background: linear-gradient(180deg, rgba(14, 18, 16, 0.96), rgba(8, 10, 9, 0.99));
      border-top: 3px solid #39ff14;
      box-shadow: 0 -6px 25px rgba(57, 255, 20, 0.2);
      padding: 12px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }
    .bottom-left {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 6px;
      min-width: 0;
    }
    .channel-name {
      font-size: clamp(1.2rem, 5vw, 1.55rem);
      font-weight: 900;
      color: #ffffff;
      white-space: nowrap;
    }
    .channel-name span {
      color: #39ff14;
    }
    .live-note {
      font-size: 0.88rem;
      color: #b9c7bc;
      line-height: 1.3;
    }
    .action-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      width: 44%;
      max-width: 190px;
      flex-shrink: 0;
    }
    .action-btn {
      background: rgba(24, 28, 26, 0.95);
      border: 1.5px solid rgba(57, 255, 20, 0.65);
      border-radius: 10px;
      padding: 8px 10px;
      font-size: 0.85rem;
      font-weight: 800;
      color: #ffffff;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .dot {
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: #39ff14;
      box-shadow: 0 0 8px #39ff14;
      flex-shrink: 0;
    }
    .edit-toggle {
      position: fixed;
      top: 10px;
      right: 10px;
      z-index: 50;
      background: rgba(15, 20, 17, 0.9);
      color: #39ff14;
      border: 1px solid rgba(57, 255, 20, 0.6);
      border-radius: 8px;
      padding: 5px 10px;
      font-size: 0.75rem;
      font-weight: 700;
    }
    .panel {
      display: none;
      position: fixed;
      top: 44px;
      right: 10px;
      z-index: 50;
      width: 240px;
      background: rgba(12, 16, 14, 0.98);
      border: 1.5px solid #39ff14;
      border-radius: 12px;
      padding: 12px;
    }
    .panel.open {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .panel input {
      width: 100%;
      padding: 7px 9px;
      border-radius: 7px;
      border: 1px solid rgba(57, 255, 20, 0.4);
      background: #080b09;
      color: #fff;
      font-size: 0.8rem;
    }
    .panel button {
      padding: 7px;
      border: none;
      border-radius: 7px;
      background: #39ff14;
      color: #000;
      font-weight: 800;
      font-size: 0.8rem;
    }
  </style>
</head>
<body>
  <button class="edit-toggle" onclick="togglePanel()">DÜZENLE</button>
  <div class="panel" id="editPanel">
    <input type="text" id="inTitle" value="MEDUSA" />
    <input type="text" id="inSub" value="CANLI YAYIN • İYİ SEYİRLER" />
    <input type="text" id="inChannel" value="@MEDUSA" />
    <input type="text" id="inNote" value="Desteğin için teşekkürler!" />
    <button onclick="applyChanges()">UYGULA</button>
  </div>

  <header class="top-banner">
    <div class="brand-title" id="outTitle">MEDUSA</div>
    <div class="sub-tag" id="outSub">CANLI YAYIN • İYİ SEYİRLER</div>
  </header>

  <main class="game-area"></main>

  <footer class="bottom-banner">
    <div class="bottom-left">
      <div class="channel-name" id="outChannel"><span>@</span>MEDUSA</div>
      <div class="live-note" id="outNote">Desteğin için teşekkürler!</div>
    </div>
    <div class="action-list">
      <div class="action-btn"><span class="dot"></span>TAKİP ET</div>
      <div class="action-btn"><span class="dot"></span>BEĞEN</div>
      <div class="action-btn"><span class="dot"></span>YORUM YAP</div>
    </div>
  </footer>

  <script>
    function togglePanel() {
      document.getElementById('editPanel').classList.toggle('open');
    }
    function applyChanges() {
      const title = document.getElementById('inTitle').value.trim() || 'MEDUSA';
      const sub = document.getElementById('inSub').value.trim() || 'CANLI YAYIN • İYİ SEYİRLER';
      const rawChannel = document.getElementById('inChannel').value.trim() || '@MEDUSA';
      const note = document.getElementById('inNote').value.trim() || 'Desteğin için teşekkürler!';

      document.getElementById('outTitle').textContent = title;
      document.getElementById('outSub').textContent = sub;
      document.getElementById('outNote').textContent = note;
      document.getElementById('outChannel').innerHTML = `<span>@</span>${rawChannel.replace(/^@+/, '')}`;
      togglePanel();
    }
  </script>
</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
