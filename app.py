import os
import random
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

AVATAR_SVG = "data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='12' fill='%23dc2626'/%3E%3Ccircle cx='50' cy='38' r='16' fill='%23ffffff'/%3E%3Cpath d='M22 84c2-16 14-26 28-26s26 10 28 26' fill='%23ffffff'/%3E%3C/svg%3E"

GUEST_AVATAR_SVG = "data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='12' fill='%232563eb'/%3E%3Ccircle cx='50' cy='38' r='16' fill='%23ffffff'/%3E%3Cpath d='M22 84c2-16 14-26 28-26s26 10 28 26' fill='%23ffffff'/%3E%3C/svg%3E"

# İsteğe bağlı destek veya yayın bağlantısı (boş bırakılırsa bilgilendirme uyarısı verir)
SUPPORT_URL = ""

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

    /* E-Posta Doğrulama Ekranı */
    .verify-screen {
      display: none;
      min-height: 100vh;
      align-items: center;
      justify-content: center;
      padding: 20px;
      background: radial-gradient(circle at top, #221012 0%, #141414 70%);
    }
    .verify-screen.active { display: flex; }
    .verify-box {
      width: 100%;
      max-width: 420px;
      background: #1c1c1e;
      border: 1px solid #2e2e34;
      border-radius: 14px;
      padding: 22px 18px;
    }
    .verify-box h2 { font-size: 1.2rem; margin-bottom: 6px; }
    .verify-box p { font-size: 0.85rem; color: #b3b3b3; line-height: 1.45; margin-bottom: 14px; }
    .field {
      width: 100%;
      background: #121214;
      border: 1px solid #35353d;
      color: #fff;
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 0.92rem;
      margin-bottom: 10px;
    }
    .btn-red {
      width: 100%;
      background: #e50914;
      color: #fff;
      border: 0;
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 0.9rem;
      font-weight: 700;
      cursor: pointer;
    }
    .btn-ghost {
      width: 100%;
      margin-top: 8px;
      background: transparent;
      color: #b3b3b3;
      border: 1px solid #33333b;
      border-radius: 8px;
      padding: 9px 12px;
      font-size: 0.84rem;
      cursor: pointer;
    }
    .code-hint {
      margin-top: 10px;
      padding: 10px 12px;
      border-radius: 8px;
      background: #232329;
      border: 1px solid #3b3b47;
      font-size: 0.82rem;
      color: #fbbf24;
      display: none;
    }
    .err-msg {
      margin-top: 8px;
      font-size: 0.82rem;
      color: #f87171;
      min-height: 18px;
    }

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
      gap: 10px;
    }
    .logo {
      color: #e50914;
      font-weight: 900;
      font-size: 1.15rem;
      letter-spacing: 1px;
    }
    .nav-links {
      display: flex;
      gap: 10px;
      overflow-x: auto;
    }
    .nav-links button {
      background: none;
      border: 0;
      color: #b3b3b3;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
    }
    .nav-links button.active { color: #ffffff; }
    .right-box {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .support-btn {
      background: #26262c;
      color: #fff;
      border: 1px solid #3a3a44;
      border-radius: 6px;
      padding: 5px 8px;
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
      white-space: nowrap;
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
      padding: 20px 18px;
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
    .hero h1 { font-size: 1.3rem; margin-bottom: 8px; }
    .hero p { font-size: 0.86rem; color: #d4d4d8; line-height: 1.45; }

    .search-bar {
      padding: 0 16px 12px;
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
      padding: 22px 16px;
      border-radius: 10px;
      background: #1b1b1b;
      border: 1px dashed #3a3a3a;
      text-align: center;
      color: #b3b3b3;
      font-size: 0.88rem;
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

  <!-- 1. Profil Ekranı -->
  <div class="profile-screen" id="profileScreen">
    <div class="logo" style="font-size:1.6rem;margin-bottom:14px;">MEDUSAFILM</div>
    <div class="profile-title">Kim izliyor?</div>
    <div class="profiles">
      <div class="profile-card" onclick="startVerification('Medusa', '{{ avatar_url }}')">
        <img src="{{ avatar_url }}" alt="Medusa" />
        <span class="profile-name">Medusa</span>
      </div>
      <div class="profile-card" onclick="startVerification('Misafir', '{{ guest_avatar_url }}')">
        <img src="{{ guest_avatar_url }}" alt="Misafir" />
        <span class="profile-name">Misafir</span>
      </div>
    </div>
  </div>

  <!-- 2. E-Posta Doğrulama Ekranı -->
  <div class="verify-screen" id="verifyScreen">
    <div class="verify-box">
      <div class="logo" style="font-size:1.15rem;margin-bottom:8px;">MEDUSAFILM</div>
      <h2>E-Posta Doğrulama</h2>
      <p id="verifyDesc">Devam etmek için e-posta adresini gir ve doğrulama kodunu onayla.</p>

      <input class="field" id="emailInput" type="email" placeholder="ornek@eposta.com" />
      <button class="btn-red" id="sendCodeBtn" onclick="requestCode()">Doğrulama Kodu Oluştur</button>

      <div class="code-hint" id="codeHint"></div>

      <div id="codeStep" style="display:none;margin-top:12px;">
        <input class="field" id="codeInput" type="text" inputmode="numeric" maxlength="6" placeholder="6 haneli doğrulama kodu" />
        <button class="btn-red" onclick="verifyCode()">Kodu Onayla ve Giriş Yap</button>
      </div>

      <div class="err-msg" id="verifyError"></div>
      <button class="btn-ghost" onclick="backToProfiles()">Profil Ekranına Dön</button>
    </div>
  </div>

  <!-- 3. Ana Platform -->
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
        <button class="support-btn" onclick="openSupport()">Destek</button>
        <span id="activeProfileLabel" style="font-size:0.78rem;color:#ccc;">Medusa</span>
        <img class="top-avatar" id="topAvatar" src="{{ avatar_url }}" alt="Profil" onclick="showProfiles()" title="Profil Değiştir" />
      </div>
    </header>

    <section class="hero">
      <div class="hero-badge">DOĞRULANMIŞ GİRİŞ</div>
      <h1 id="welcomeHeading">Hoş Geldin</h1>
      <p id="verifiedUserInfo">E-posta doğrulaması aktif. Katalog ve oynatıcı altyapısı hazır.</p>
    </section>

    <div class="search-bar">
      <input id="searchInput" type="text" placeholder="Ara..." />
    </div>

    <div class="section-title" id="sectionTitle">Katalog</div>
    <div class="empty-state" id="emptyState">
      Katalog şu an boş (0 içerik). Doğrulama akışı eklendi; sıradaki adımda istediğin içerikleri ekleyebiliriz.
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
    const ITEMS = {{ items|tojson }};
    const SUPPORT_URL = {{ support_url|tojson }};
    let selectedCategory = "";
    let pendingProfile = { name: "Medusa", avatar: "{{ avatar_url }}" };
    let generatedCode = "";

    const profileScreen = document.getElementById("profileScreen");
    const verifyScreen = document.getElementById("verifyScreen");
    const appScreen = document.getElementById("appScreen");
    const grid = document.getElementById("grid");
    const emptyState = document.getElementById("emptyState");
    const searchInput = document.getElementById("searchInput");
    const modal = document.getElementById("playerModal");
    const videoPlayer = document.getElementById("videoPlayer");

    function startVerification(name, avatar) {
      pendingProfile = { name, avatar };
      generatedCode = "";
      document.getElementById("verifyDesc").textContent = `"${name}" profili için e-posta adresini gir ve kodu doğrula.`;
      document.getElementById("emailInput").value = "";
      document.getElementById("codeInput").value = "";
      document.getElementById("codeHint").style.display = "none";
      document.getElementById("codeStep").style.display = "none";
      document.getElementById("verifyError").textContent = "";
      profileScreen.classList.add("hidden");
      verifyScreen.classList.add("active");
    }

    function backToProfiles() {
      verifyScreen.classList.remove("active");
      profileScreen.classList.remove("hidden");
    }

    async function requestCode() {
      const email = document.getElementById("emailInput").value.trim();
      const errEl = document.getElementById("verifyError");
      errEl.textContent = "";

      if (!email || !email.includes("@") || !email.includes(".")) {
        errEl.textContent = "Lütfen geçerli bir e-posta adresi gir.";
        return;
      }

      const res = await fetch("/api/send-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, profile: pendingProfile.name })
      });
      const data = await res.json();
      if (!data.ok) {
        errEl.textContent = data.error || "Kod oluşturulamadı.";
        return;
      }

      generatedCode = data.code;
      const hint = document.getElementById("codeHint");
      hint.innerHTML = `Doğrulama kodu oluşturuldu: <strong>${generatedCode}</strong><br><span style="color:#d4d4d8;">(Harici e-posta sunucusu bağlı olmadığından kod test/ekran modunda gösteriliyor.)</span>`;
      hint.style.display = "block";
      document.getElementById("codeStep").style.display = "block";
    }

    async function verifyCode() {
      const email = document.getElementById("emailInput").value.trim();
      const code = document.getElementById("codeInput").value.trim();
      const errEl = document.getElementById("verifyError");
      errEl.textContent = "";

      if (!code || code !== generatedCode) {
        errEl.textContent = "Doğrulama kodu eşleşmedi.";
        return;
      }

      await fetch("/api/verify-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, profile: pendingProfile.name })
      });

      document.getElementById("activeProfileLabel").textContent = pendingProfile.name;
      document.getElementById("topAvatar").src = pendingProfile.avatar;
      document.getElementById("welcomeHeading").textContent = `Hoş Geldin, ${pendingProfile.name}`;
      document.getElementById("verifiedUserInfo").textContent = `Doğrulanan e-posta: ${email}`;

      verifyScreen.classList.remove("active");
      appScreen.classList.add("active");
      renderItems();
    }

    function showProfiles() {
      appScreen.classList.remove("active");
      profileScreen.classList.remove("hidden");
    }

    function openSupport() {
      if (SUPPORT_URL) {
        window.open(SUPPORT_URL, "_blank", "noopener,noreferrer");
      } else {
        alert("Destek bağlantısı henüz ayarlanmamış. SUPPORT_URL alanına kendi bağlantını ekleyebilirsin.");
      }
    }

    function renderItems() {
      const q = searchInput.value.trim().toLowerCase();
      const filtered = ITEMS.filter(item => {
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
      const item = ITEMS.find(x => x.id === id);
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

VERIFIED_USERS = []


@app.route("/")
def index():
    return render_template_string(
        HTML_TEMPLATE,
        items=CATALOG,
        avatar_url=AVATAR_SVG,
        guest_avatar_url=GUEST_AVATAR_SVG,
        support_url=SUPPORT_URL,
    )


@app.route("/api/send-code", methods=["POST"])
def api_send_code():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    if "@" not in email or "." not in email:
        return jsonify({"ok": False, "error": "Geçersiz e-posta adresi."}), 400
    code = f"{random.randint(100000, 999999)}"
    return jsonify({"ok": True, "code": code})


@app.route("/api/verify-code", methods=["POST"])
def api_verify_code():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    profile = (data.get("profile") or "Medusa").strip()
    if email and email not in VERIFIED_USERS:
        VERIFIED_USERS.append({"email": email, "profile": profile})
    return jsonify({"ok": True, "verified_count": len(VERIFIED_USERS)})


@app.route("/api/catalog")
def api_catalog():
    return jsonify({"count": len(CATALOG), "items": CATALOG})


@app.route("/health")
def health():
    return jsonify({"status": "ok", "count": len(CATALOG), "verified_users": len(VERIFIED_USERS)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
