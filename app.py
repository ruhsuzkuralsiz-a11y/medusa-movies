import os
import random
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

AVATAR_SVG = "data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='12' fill='%23dc2626'/%3E%3Ccircle cx='50' cy='38' r='16' fill='%23ffffff'/%3E%3Cpath d='M22 84c2-16 14-26 28-26s26 10 28 26' fill='%23ffffff'/%3E%3C/svg%3E"

GUEST_AVATAR_SVG = "data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='12' fill='%232563eb'/%3E%3Ccircle cx='50' cy='38' r='16' fill='%23ffffff'/%3E%3Cpath d='M22 84c2-16 14-26 28-26s26 10 28 26' fill='%23ffffff'/%3E%3C/svg%3E"

SUPPORT_URL = ""
CATALOG = []
VERIFIED_USERS = []

HTML_TEMPLATE = """<!DOCTYPE html>
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
    .screen { display: none; min-height: 100vh; }
    .screen.active { display: block; }

    .profile-screen.active {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 24px;
      background: radial-gradient(circle at top, #261010 0%, #141414 65%);
    }
    .logo {
      color: #e50914;
      font-weight: 900;
      font-size: 1.25rem;
      letter-spacing: 1px;
    }
    .profile-title {
      font-size: 1.45rem;
      font-weight: 700;
      margin: 12px 0 22px;
      text-align: center;
    }
    .profiles {
      display: flex;
      gap: 22px;
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
    .profile-name { color: #cccccc; font-size: 0.92rem; font-weight: 600; }

    .verify-screen.active {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      background: radial-gradient(circle at top, #221012 0%, #141414 70%);
    }
    .verify-box {
      width: 100%;
      max-width: 420px;
      background: #1c1c1e;
      border: 1px solid #2e2e34;
      border-radius: 14px;
      padding: 22px 18px;
    }
    .verify-box h2 { font-size: 1.2rem; margin: 6px 0; }
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
      font-size: 0.84rem;
      color: #fbbf24;
      display: none;
    }
    .err-msg {
      margin-top: 8px;
      font-size: 0.82rem;
      color: #f87171;
      min-height: 18px;
    }

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
    .search-bar { padding: 0 16px 12px; }
    .search-bar input {
      width: 100%;
      background: #222222;
      border: 1px solid #363636;
      color: #fff;
      border-radius: 8px;
      padding: 9px 12px;
      font-size: 0.9rem;
    }
    .section-title { padding: 6px 16px 10px; font-size: 1rem; font-weight: 700; }
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
      padding: 0 16px 36px;
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

  <div class="screen profile-screen active" id="profileScreen">
    <div class="logo" style="font-size:1.6rem;">MEDUSAFILM</div>
    <div class="profile-title">Kim izliyor?</div>
    <div class="profiles">
      <div class="profile-card" data-name="Medusa" data-avatar="__AVATAR__">
        <img src="__AVATAR__" alt="Medusa" />
        <span class="profile-name">Medusa</span>
      </div>
      <div class="profile-card" data-name="Misafir" data-avatar="__GUEST_AVATAR__">
        <img src="__GUEST_AVATAR__" alt="Misafir" />
        <span class="profile-name">Misafir</span>
      </div>
    </div>
  </div>

  <div class="screen verify-screen" id="verifyScreen">
    <div class="verify-box">
      <div class="logo">MEDUSAFILM</div>
      <h2>E-Posta Dogrulama</h2>
      <p id="verifyDesc">Devam etmek icin e-posta adresini gir ve kodu onayla.</p>
      <input class="field" id="emailInput" type="email" placeholder="ornek@eposta.com" />
      <button class="btn-red" id="sendCodeBtn" type="button">Dogrulama Kodu Olustur</button>
      <div class="code-hint" id="codeHint"></div>
      <div id="codeStep" style="display:none;margin-top:12px;">
        <input class="field" id="codeInput" type="text" inputmode="numeric" maxlength="6" placeholder="6 haneli kod" />
        <button class="btn-red" id="verifyCodeBtn" type="button">Kodu Onayla ve Giris Yap</button>
      </div>
      <div class="err-msg" id="verifyError"></div>
      <button class="btn-ghost" id="backProfilesBtn" type="button">Profil Ekranina Don</button>
    </div>
  </div>

  <div class="screen app-screen" id="appScreen">
    <header>
      <div class="logo">MEDUSAFILM</div>
      <div class="nav-links" id="categoryTabs">
        <button class="active" data-cat="" type="button">Tumu</button>
        <button data-cat="Diziler" type="button">Diziler</button>
        <button data-cat="Filmler" type="button">Filmler</button>
        <button data-cat="Animasyon" type="button">Animasyon</button>
      </div>
      <div class="right-box">
        <button class="support-btn" id="supportBtn" type="button">Destek</button>
        <span id="activeProfileLabel" style="font-size:0.78rem;color:#ccc;">Medusa</span>
        <img class="top-avatar" id="topAvatar" src="__AVATAR__" alt="Profil" />
      </div>
    </header>

    <section class="hero">
      <div class="hero-badge">DOGRULANMIS GIRIS</div>
      <h1 id="welcomeHeading">Hos Geldin</h1>
      <p id="verifiedUserInfo">E-posta dogrulamasi aktif.</p>
    </section>

    <div class="search-bar">
      <input id="searchInput" type="text" placeholder="Ara..." />
    </div>

    <div class="section-title" id="sectionTitle">Katalog</div>
    <div class="empty-state" id="emptyState">Katalog su an bos (0 icerik).</div>
    <div class="grid" id="grid"></div>
  </div>

  <div class="modal" id="playerModal">
    <div class="modal-box">
      <button class="close-btn" id="closeModal" type="button">Kapat</button>
      <h3 id="modalTitle"></h3>
      <p id="modalMeta" style="font-size:0.8rem;color:#b3b3b3;margin-top:4px;"></p>
      <video id="videoPlayer" controls playsinline></video>
    </div>
  </div>

  <script>
    const ITEMS = __ITEMS_JSON__;
    const SUPPORT_URL = __SUPPORT_JSON__;

    let selectedCategory = "";
    let pendingProfile = { name: "Medusa", avatar: "__AVATAR__" };
    let generatedCode = "";

    const profileScreen = document.getElementById("profileScreen");
    const verifyScreen = document.getElementById("verifyScreen");
    const appScreen = document.getElementById("appScreen");

    function showScreen(target) {
      profileScreen.classList.remove("active");
      verifyScreen.classList.remove("active");
      appScreen.classList.remove("active");
      target.classList.add("active");
    }

    document.querySelectorAll(".profile-card").forEach(function(card) {
      card.addEventListener("click", function() {
        pendingProfile = {
          name: card.getAttribute("data-name") || "Medusa",
          avatar: card.getAttribute("data-avatar") || ""
        };
        generatedCode = "";
        document.getElementById("verifyDesc").textContent = '"' + pendingProfile.name + '" profili icin e-posta adresini gir.';
        document.getElementById("emailInput").value = "";
        document.getElementById("codeInput").value = "";
        document.getElementById("codeHint").style.display = "none";
        document.getElementById("codeStep").style.display = "none";
        document.getElementById("verifyError").textContent = "";
        showScreen(verifyScreen);
      });
    });

    document.getElementById("backProfilesBtn").addEventListener("click", function() {
      showScreen(profileScreen);
    });

    document.getElementById("topAvatar").addEventListener("click", function() {
      showScreen(profileScreen);
    });

    document.getElementById("sendCodeBtn").addEventListener("click", async function() {
      const email = document.getElementById("emailInput").value.trim();
      const errEl = document.getElementById("verifyError");
      errEl.textContent = "";

      if (!email || email.indexOf("@") === -1 || email.indexOf(".") === -1) {
        errEl.textContent = "Gecerli bir e-posta adresi gir.";
        return;
      }

      try {
        const res = await fetch("/api/send-code", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: email, profile: pendingProfile.name })
        });
        const data = await res.json();
        if (!data.ok) {
          errEl.textContent = data.error || "Kod olusturulamadi.";
          return;
        }
        generatedCode = String(data.code);
        const hint = document.getElementById("codeHint");
        hint.innerHTML = "Dogrulama Kodu: <strong>" + generatedCode + "</strong>";
        hint.style.display = "block";
        document.getElementById("codeStep").style.display = "block";
      } catch (e) {
        errEl.textContent = "Baglanti hatasi olustu.";
      }
    });

    document.getElementById("verifyCodeBtn").addEventListener("click", async function() {
      const email = document.getElementById("emailInput").value.trim();
      const code = document.getElementById("codeInput").value.trim();
      const errEl = document.getElementById("verifyError");
      errEl.textContent = "";

      if (!code || code !== generatedCode) {
        errEl.textContent = "Dogrulama kodu eslesmedi.";
        return;
      }

      try {
        await fetch("/api/verify-code", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: email, profile: pendingProfile.name })
        });
      } catch (e) {}

      document.getElementById("activeProfileLabel").textContent = pendingProfile.name;
      if (pendingProfile.avatar) {
        document.getElementById("topAvatar").src = pendingProfile.avatar;
      }
      document.getElementById("welcomeHeading").textContent = "Hos Geldin, " + pendingProfile.name;
      document.getElementById("verifiedUserInfo").textContent = "Dogrulanan e-posta: " + email;
      showScreen(appScreen);
      renderItems();
    });

    document.getElementById("supportBtn").addEventListener("click", function() {
      if (SUPPORT_URL) {
        window.open(SUPPORT_URL, "_blank", "noopener,noreferrer");
      } else {
        alert("Destek baglantisi henuz eklenmedi.");
      }
    });

    function renderItems() {
      const q = document.getElementById("searchInput").value.trim().toLowerCase();
      const grid = document.getElementById("grid");
      const emptyState = document.getElementById("emptyState");

      const filtered = ITEMS.filter(function(item) {
        const matchCat = !selectedCategory || item.category === selectedCategory;
        const matchQ = !q || (item.title || "").toLowerCase().indexOf(q) !== -1;
        return matchCat && matchQ;
      });

      if (filtered.length === 0) {
        grid.innerHTML = "";
        emptyState.style.display = "block";
        return;
      }

      emptyState.style.display = "none";
      grid.innerHTML = filtered.map(function(item) {
        return '<div class="card" data-id="' + item.id + '">' +
          '<img src="' + item.poster + '" alt="' + item.title + '" />' +
          '<div class="card-title">' + item.title + '</div>' +
          '</div>';
      }).join("");
    }

    document.getElementById("searchInput").addEventListener("input", renderItems);

    document.querySelectorAll("#categoryTabs button").forEach(function(btn) {
      btn.addEventListener("click", function() {
        document.querySelectorAll("#categoryTabs button").forEach(function(b) { b.classList.remove("active"); });
        btn.classList.add("active");
        selectedCategory = btn.getAttribute("data-cat") || "";
        document.getElementById("sectionTitle").textContent = selectedCategory || "Katalog";
        renderItems();
      });
    });

    document.getElementById("closeModal").addEventListener("click", function() {
      const vp = document.getElementById("videoPlayer");
      vp.pause();
      vp.removeAttribute("src");
      document.getElementById("playerModal").classList.remove("open");
    });
  </script>
</body>
</html>"""


def render_app():
    import json
    page = HTML_TEMPLATE.replace("__AVATAR__", AVATAR_SVG)
    page = page.replace("__GUEST_AVATAR__", GUEST_AVATAR_SVG)
    page = page.replace("__ITEMS_JSON__", json.dumps(CATALOG))
    page = page.replace("__SUPPORT_JSON__", json.dumps(SUPPORT_URL))
    return page


@app.route("/")
def index():
    return render_app()


@app.route("/api/send-code", methods=["POST"])
def api_send_code():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    if "@" not in email or "." not in email:
        return jsonify({"ok": False, "error": "Gecersiz e-posta adresi."}), 400
    code = f"{random.randint(100000, 999999)}"
    return jsonify({"ok": True, "code": code})


@app.route("/api/verify-code", methods=["POST"])
def api_verify_code():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    profile = (data.get("profile") or "Medusa").strip()
    if email and not any(u["email"] == email for u in VERIFIED_USERS):
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
