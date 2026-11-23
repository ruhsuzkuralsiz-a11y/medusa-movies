import os
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

AVATAR_SVG = "data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='12' fill='%23dc2626'/%3E%3Ccircle cx='50' cy='38' r='16' fill='%23ffffff'/%3E%3Cpath d='M22 84c2-16 14-26 28-26s26 10 28 26' fill='%23ffffff'/%3E%3C/svg%3E"

GUEST_AVATAR_SVG = "data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='12' fill='%232563eb'/%3E%3Ccircle cx='50' cy='38' r='16' fill='%23ffffff'/%3E%3Cpath d='M22 84c2-16 14-26 28-26s26 10 28 26' fill='%23ffffff'/%3E%3C/svg%3E"

# İçerikler şimdilik boş bırakıldı; önce arayüz ve iskelet oturacak, sonra ekleyeceğiz.
CATALOG = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MEDUSAFILM</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #141414;
      color: #ffffff;
      font-family: system-ui, -apple-system, sans-serif;
      min-height: 100vh;
    }

    /* Profil Seçim Ekranı */
    .profile-screen {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 24px;
      background: radial-gradient(circle at top, #261010 0%, #141414 65%);
    }
    .profile-screen.hidden { display: none; }
    .profile-title {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 24px;
      text-align: center;
    }
    .profiles {
      display: flex;
      gap: 20px;
      flex-wrap: wrap;
      justify-content: center;
    }
    .profile-card {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
      cursor: pointer;
    }
    .profile-card img {
      width: 92px;
      height: 92px;
      border-radius: 10px;
      object-fit: cover;
      border: 2px solid transparent;
    }
    .profile-card:hover img { border-color: #ffffff; }
    .profile-name { color: #b3b3b3; font-size: 0.92rem; font-weight: 600; }

    /* Ana Platform Ekranı */
    .app-screen { display: none; padding-bottom: 40px; }
    .app-screen.active { display: block; }

    header {
      position: sticky;
      top: 0;
      z-index: 30;
      background: rgba(20, 20, 20, 0.95);
      border-bottom: 1px solid #262626;
      padding: 12px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }
    .logo {
      color: #e50914;
      font-weight: 900;
      font-size: 1.2rem;
      letter-spacing: 1px;
    }
    .nav-links {
      display: flex;
      gap: 12px;
      overflow-x: auto;
    }
    .nav-links button {
      background: none;
      border: 0;
      color: #b3b3b3;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
    }
    .nav-links button.active { color: #ffffff; }
    .right-box {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .top-avatar {
      width: 32px;
      height: 32px;
      border-radius: 6px;
      object-fit: cover;
      cursor: pointer;
    }

    .hero {
      margin: 14px 16px;
      padding: 22px 18px;
      border-radius: 12px;
      background: linear-gradient(90deg, rgba(20,20,20,0.95) 20%, rgba(229,9,20,0.22) 100%), #1f1f1f;
      border: 1px solid #2d2d2d;
    }
    .hero-badge {
      display: inline-block;
      background: #e50914;
      color: #fff;
      font-size: 0.7rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
      margin-bottom: 10px;
    }
    .hero h1 { font-size: 1.35rem; margin-bottom: 8px; }
    .hero p { font-size: 0.88rem; color: #d4d4d8; line-height: 1.45; }

    .search-bar {
      padding: 0 16px 12px;
      display: flex;
      gap: 8px;
    }
    .search-bar input {
      width: 100%;
      background: #222222;
      border: 1px solid #363636;
      color: #fff;
      border-radius: 8px;
      padding: 9px 12px;
      font-size: 0.9rem;
    }

    .section-title {
      padding: 6px 16px 10px;
      font-size: 1rem;
      font-weight: 700;
    }

    .empty-state {
      margin: 10px 16px;
      padding: 24px 16px;
      border-radius: 10px;
      background: #1b1b1b;
      border: 1px dashed #3a3a3a;
      text-align: center;
      color: #b3b3b3;
      font-size: 0.9rem;
      line-height: 1.5;
    }

    .grid {
      padding: 0 16px;
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
    }
    .card {
      background: #1e1e1e;
      border-radius: 8px;
      overflow: hidden;
      cursor: pointer;
    }
    .card img {
      width: 100%;
      aspect-ratio: 2 / 3;
      object-fit: cover;
      display: block;
    }
    .card-title {
      padding: 7px 8px;
      font-size: 0.8rem;
      font-weight: 700;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .modal {
      display: none;
      position: fixed;
      inset: 0;
      z-index: 60;
      background: rgba(0, 0, 0, 0.88);
      padding: 16px;
      align-items: center;
      justify-content: center;
    }
    .modal.open { display: flex; }
    .modal-box {
      width: 100%;
      max-width: 540px;
      background: #1c1c1c;
      border: 1px solid #333;
      border-radius: 12px;
      padding: 14px;
    }
    .close-btn {
      float: right;
      background: #e50914;
      color: #fff;
      border: 0;
      border-radius: 6px;
      padding: 5px 10px;
      font-weight: 700;
      cursor: pointer;
    }
    video {
      width: 100%;
      max-height: 260px;
      border-radius: 8px;
      background: #000;
      margin-top: 12px;
    }
  </style>
</head>
<body>

  <!-- Profil Ekranı -->
  <div class="profile-screen" id="profileScreen">
    <div class="logo" style="font-size:1.6rem;margin-bottom:14px;">MEDUSAFILM</div>
    <div class="profile-title">Kim izliyor?</div>
    <div class="profiles">
      <div class="profile-card" onclick="selectProfile('Medusa', '{{ avatar_url }}')">
        <img src="{{ avatar_url }}" alt="Medusa" />
        <span class="profile-name">Medusa</span>
      </div>
      <div class="profile-card" onclick="selectProfile('Misafir', '{{ guest_avatar_url }}')">
        <img src="{{ guest_avatar_url }}" alt="Misafir" />
        <span class="profile-name">Misafir</span>
      </div>
    </div>
  </div>

  <!-- Ana Platform -->
  <div class="app-screen" id="appScreen">
    <header>
      <div class="logo">MEDUSAFILM</div>
      <div class="nav-links" id="categoryTabs">
        <button class="active" data-cat="">Tümü</button>
        <button data-cat="Diziler">Diziler</button>
        <button data-cat="Filmler">Filmler</button>
        <button data-cat="Animasyon">Animasyon</button>
      </div>
      <div class="right-box">
        <span id="activeProfileLabel" style="font-size:0.8rem;color:#ccc;">Medusa</span>
        <img class="top-avatar" id="topAvatar" src="{{ avatar_url }}" alt="Profil" onclick="showProfiles()" title="Profil Değiştir" />
      </div>
    </header>

    <section class="hero">
      <div class="hero-badge">ALTYAPI HAZIR</div>
      <h1>Netflix Tarzı Vitrin İskeleti</h1>
      <p>Arayüz, profil seçimi, kategori filtreleme ve oynatıcı penceresi hazır. Şimdi ilk olarak tasarımın nasıl durduğuna bakalım; ardından içerikleri ekleyeceğiz.</p>
    </section>

    <div class="search-bar">
      <input id="searchInput" type="text" placeholder="Ara..." />
    </div>

    <div class="section-title" id="sectionTitle">Katalog</div>
    <div class="empty-state" id="emptyState">
      Katalog şu an boş (0 içerik). Önce arayüz yapısını kurduk; bir sonraki adımda ekleyeceğimiz içerik ve kaynaklarla burası dolacak.
    </div>
    <div class="grid" id="grid"></div>
  </div>

  <!-- Oynatıcı Penceresi -->
  <div class="modal" id="playerModal">
    <div class="modal-box">
      <button class="close-btn" id="closeModal">Kapat</button>
      <h3 id="modalTitle"></h3>
      <p id="modalMeta" style="font-size:0.8rem;color:#b3b3b3;margin-top:4px;"></p>
      <video id="videoPlayer" controls playsinline></video>
    </div>
  </div>

  <script>
    let items = {{ items|tojson }};
    let selectedCategory = "";

    const profileScreen = document.getElementById("profileScreen");
    const appScreen = document.getElementById("appScreen");
    const grid = document.getElementById("grid");
    const emptyState = document.getElementById("emptyState");
    const searchInput = document.getElementById("searchInput");
    const modal = document.getElementById("playerModal");
    const videoPlayer = document.getElementById("videoPlayer");

    function selectProfile(name, avatar) {
      document.getElementById("activeProfileLabel").textContent = name;
      document.getElementById("topAvatar").src = avatar;
      profileScreen.classList.add("hidden");
      appScreen.classList.add("active");
      renderItems();
    }

    function showProfiles() {
      appScreen.classList.remove("active");
      profileScreen.classList.remove("hidden");
    }

    function renderItems() {
      const q = searchInput.value.trim().toLowerCase();
      const filtered = items.filter(item => {
        const matchCat = !selectedCategory || item.category === selectedCategory;
        const matchQ = !q || (item.title || "").toLowerCase().includes(q);
        return matchCat && matchQ;
      });

      if (filtered.length === 0) {
        grid.innerHTML = "";
        emptyState.style.display = "block";
        return;
      }

      emptyState.style.display = "none";
      grid.innerHTML = filtered.map(item => `
        <div class="card" onclick="openPlayer(${item.id})">
          <img src="${item.poster}" alt="${item.title}" />
          <div class="card-title">${item.title}</div>
        </div>
      `).join("");
    }

    function openPlayer(id) {
      const item = items.find(x => x.id === id);
      if (!item) return;
      document.getElementById("modalTitle").textContent = item.title;
      document.getElementById("modalMeta").textContent = item.category || "";
      videoPlayer.src = item.video_url || "";
      modal.classList.add("open");
      if (item.video_url) videoPlayer.play().catch(() => {});
    }

    document.getElementById("closeModal").onclick = () => {
      videoPlayer.pause();
      videoPlayer.removeAttribute("src");
      modal.classList.remove("open");
    };

    searchInput.addEventListener("input", renderItems);

    document.querySelectorAll("#categoryTabs button").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll("#categoryTabs button").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        selectedCategory = btn.dataset.cat;
        document.getElementById("sectionTitle").textContent = selectedCategory || "Katalog";
        renderItems();
      });
    });
  </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(
        HTML_TEMPLATE,
        items=CATALOG,
        avatar_url=AVATAR_SVG,
        guest_avatar_url=GUEST_AVATAR_SVG,
    )


@app.route("/api/catalog")
def api_catalog():
    return jsonify({"count": len(CATALOG), "items": CATALOG})


@app.route("/health")
def health():
    return jsonify({"status": "ok", "count": len(CATALOG)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
