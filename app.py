import json
import os
import random
from flask import Flask, jsonify

app = Flask(__name__)

SUPPORT_URL = "https://www.instagram.com/ttlewiss21/"
SUPPORT_HANDLE = "@ttlewiss21"

CATALOG = [
    {
        "id": 1,
        "title": "Ornek Video 1",
        "category": "Filmler",
        "year": "2026",
        "note": "Dogrudan mp4 linki veya harici oynatici linki ekleyebilecegin ilk kart.",
        "media_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
    },
    {
        "id": 2,
        "title": "Ornek Video 2",
        "category": "Diziler",
        "year": "2026",
        "note": "Kendi ekleyecegin dizi veya film baglantisi icin hazir kart.",
        "media_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
    },
    {
        "id": 3,
        "title": "Harici Link Test Kartı",
        "category": "Animasyon",
        "year": "2026",
        "note": "Dis baglanti veya oynatici penceresi test karti.",
        "media_url": "",
    },
]

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
    .center.active {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }
    .logo { color: #e50914; font-weight: 900; font-size: 1.25rem; }
    .btn {
      background: #e50914;
      color: #fff;
      border: 0;
      border-radius: 8px;
      padding: 10px 16px;
      font-weight: 700;
      cursor: pointer;
      margin-top: 12px;
      text-decoration: none;
      display: inline-block;
    }
    header {
      position: sticky;
      top: 0;
      z-index: 20;
      background: rgba(20, 20, 20, 0.96);
      padding: 12px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      border-bottom: 1px solid #262626;
    }
    .cats { display: flex; gap: 10px; overflow-x: auto; }
    .cats button {
      background: none;
      border: 0;
      color: #b3b3b3;
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      white-space: nowrap;
    }
    .cats button.active { color: #ffffff; }
    .support-link {
      background: #e50914;
      color: #fff;
      text-decoration: none;
      border-radius: 6px;
      padding: 6px 10px;
      font-size: 0.78rem;
      font-weight: 700;
      white-space: nowrap;
    }
    .hero {
      margin: 14px 16px;
      padding: 16px;
      border-radius: 12px;
      background: linear-gradient(90deg, rgba(20,20,20,0.96) 25%, rgba(229,9,20,0.22) 100%), #1e1e22;
      border: 1px solid #2c2c32;
    }
    .hero h1 { font-size: 1.15rem; margin-bottom: 6px; }
    .hero p { font-size: 0.83rem; color: #d4d4d8; line-height: 1.45; }
    .search-box { padding: 0 16px 12px; }
    .search-box input, .box input {
      width: 100%;
      background: #1c1c20;
      border: 1px solid #34343c;
      color: #fff;
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 0.9rem;
    }
    .box input { margin-top: 10px; }
    .box {
      max-width: 420px;
      width: 100%;
      background: #1c1c1e;
      border: 1px solid #2e2e34;
      border-radius: 12px;
      padding: 20px;
      margin-top: 14px;
    }
    .section-title { padding: 4px 16px 10px; font-size: 1rem; font-weight: 700; }
    .grid {
      padding: 0 16px 32px;
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }
    .card {
      background: #1e1e22;
      border: 1px solid #2c2c32;
      border-radius: 10px;
      padding: 12px;
      min-height: 126px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      cursor: pointer;
    }
    .card-badge {
      font-size: 0.65rem;
      font-weight: 800;
      color: #f87171;
      text-transform: uppercase;
    }
    .card-title { font-size: 0.92rem; font-weight: 800; margin-top: 6px; }
    .card-year { font-size: 0.74rem; color: #a1a1aa; margin-top: 4px; }
    .modal {
      display: none;
      position: fixed;
      inset: 0;
      z-index: 50;
      background: rgba(0, 0, 0, 0.88);
      padding: 14px;
      align-items: center;
      justify-content: center;
    }
    .modal.open { display: flex; }
    .modal-box {
      width: 100%;
      max-width: 540px;
      max-height: 90vh;
      overflow-y: auto;
      background: #1c1c20;
      border: 1px solid #34343c;
      border-radius: 12px;
      padding: 16px;
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
    .player-area {
      margin-top: 12px;
      background: #0f0f12;
      border: 1px solid #2d2d35;
      border-radius: 10px;
      padding: 10px;
    }
    .player-area video,
    .player-area iframe {
      width: 100%;
      height: 230px;
      border: 0;
      border-radius: 8px;
      background: #000;
    }
    .ext-row {
      margin-top: 10px;
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
    }
    .ext-link {
      background: #2563eb;
      color: #fff;
      text-decoration: none;
      border-radius: 8px;
      padding: 8px 12px;
      font-size: 0.82rem;
      font-weight: 700;
    }
  </style>
</head>
<body>

  <div class="screen center active" id="pScreen">
    <div class="logo" style="font-size:1.7rem;">MEDUSAFILM</div>
    <h2 style="margin-top:12px;">Kim izliyor?</h2>
    <button class="btn" id="pickMedusa" type="button">Medusa</button>
    <button class="btn" id="pickGuest" type="button" style="background:#2563eb;">Misafir</button>
  </div>

  <div class="screen center" id="vScreen">
    <div class="box">
      <div class="logo">MEDUSAFILM</div>
      <h2 style="margin-top:8px;">E-Posta Dogrulama</h2>
      <input id="emailInp" type="email" placeholder="ornek@eposta.com" />
      <button class="btn" id="sendBtn" type="button" style="width:100%;">Kod Olustur</button>
      <div id="codeBox" style="margin-top:10px;color:#fbbf24;display:none;"></div>
      <div id="step2" style="display:none;">
        <input id="codeInp" type="text" placeholder="6 haneli kod" />
        <button class="btn" id="okBtn" type="button" style="width:100%;">Giris Yap</button>
      </div>
      <div id="errBox" style="margin-top:8px;color:#f87171;"></div>
    </div>
  </div>

  <div class="screen" id="aScreen">
    <header>
      <div class="logo">MEDUSAFILM</div>
      <div class="cats" id="catTabs">
        <button class="active" data-cat="" type="button">Tumu</button>
        <button data-cat="Diziler" type="button">Diziler</button>
        <button data-cat="Filmler" type="button">Filmler</button>
        <button data-cat="Animasyon" type="button">Animasyon</button>
      </div>
      <a class="support-link" href="__SUPPORT_URL__" target="_blank" rel="noopener noreferrer">Destek</a>
    </header>

    <section class="hero">
      <h1 id="welcomeText">Hos Geldin</h1>
      <p id="subText">Karta tiklayarak oynatici penceresini acabilir veya sag ustteki Destek butonu ile __HANDLE__ hesabina gecebilirsin.</p>
    </section>

    <div class="search-box">
      <input id="searchInp" type="text" placeholder="Icerik ara..." />
    </div>

    <div class="section-title" id="secTitle">Katalog</div>
    <div class="grid" id="grid"></div>
  </div>

  <div class="modal" id="playerModal">
    <div class="modal-box">
      <button class="close-btn" id="closeBtn" type="button">Kapat</button>
      <h3 id="mTitle"></h3>
      <p id="mMeta" style="font-size:0.8rem;color:#a1a1aa;margin-top:6px;"></p>
      <p id="mNote" style="font-size:0.86rem;color:#e4e4e7;margin-top:10px;line-height:1.45;"></p>
      <div class="player-area" id="playerArea"></div>
      <div class="ext-row" id="extRow"></div>
    </div>
  </div>

  <script>
    const ITEMS = __ITEMS_JSON__;
    const SUPPORT_URL = __SUPPORT_JSON__;
    const SUPPORT_HANDLE = __HANDLE_JSON__;

    let profileName = "Medusa";
    let codeVal = "";
    let activeCat = "";

    function openScreen(id) {
      ["pScreen", "vScreen", "aScreen"].forEach(function(s) {
        document.getElementById(s).classList.remove("active");
      });
      document.getElementById(id).classList.add("active");
    }

    function goVerify(name) {
      profileName = name;
      codeVal = "";
      document.getElementById("emailInp").value = "";
      document.getElementById("codeInp").value = "";
      document.getElementById("codeBox").style.display = "none";
      document.getElementById("step2").style.display = "none";
      document.getElementById("errBox").textContent = "";
      openScreen("vScreen");
    }

    document.getElementById("pickMedusa").addEventListener("click", function() { goVerify("Medusa"); });
    document.getElementById("pickGuest").addEventListener("click", function() { goVerify("Misafir"); });

    document.getElementById("sendBtn").addEventListener("click", async function() {
      const email = document.getElementById("emailInp").value.trim();
      const err = document.getElementById("errBox");
      err.textContent = "";
      if (!email || email.indexOf("@") === -1) {
        err.textContent = "Gecerli e-posta gir.";
        return;
      }
      const res = await fetch("/api/send-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email })
      });
      const data = await res.json();
      codeVal = String(data.code || "");
      const cb = document.getElementById("codeBox");
      cb.innerHTML = "Kod: <strong>" + codeVal + "</strong>";
      cb.style.display = "block";
      document.getElementById("step2").style.display = "block";
    });

    document.getElementById("okBtn").addEventListener("click", function() {
      const typed = document.getElementById("codeInp").value.trim();
      if (!typed || typed !== codeVal) {
        document.getElementById("errBox").textContent = "Kod hatali.";
        return;
      }
      document.getElementById("welcomeText").textContent = "Hos Geldin, " + profileName;
      document.getElementById("subText").textContent = "Destek hesabi: " + SUPPORT_HANDLE + " (" + SUPPORT_URL + ")";
      openScreen("aScreen");
      renderGrid();
    });

    function buildPlayerHtml(url) {
      if (!url) {
        return '<p style="font-size:0.84rem;color:#a1a1aa;">Bu kartta henuz baglanti yok. CATALOG icindeki media_url alanina link ekleyebilirsin.</p>';
      }
      const lower = url.toLowerCase();
      if (lower.indexOf(".mp4") !== -1 || lower.indexOf(".webm") !== -1 || lower.indexOf(".ogg") !== -1) {
        return '<video controls playsinline src="' + url + '"></video>';
      }
      return '<iframe src="' + url + '" allowfullscreen loading="lazy" referrerpolicy="no-referrer"></iframe>';
    }

    function openItemModal(item) {
      document.getElementById("mTitle").textContent = item.title;
      document.getElementById("mMeta").textContent = item.category + " · " + item.year;
      document.getElementById("mNote").textContent = item.note;
      document.getElementById("playerArea").innerHTML = buildPlayerHtml(item.media_url);

      const extRow = document.getElementById("extRow");
      if (item.media_url) {
        extRow.innerHTML = '<a class="ext-link" href="' + item.media_url + '" target="_blank" rel="noopener noreferrer">Baglantiyi Yeni Sekmede Ac</a>';
      } else {
        extRow.innerHTML = '<span style="font-size:0.78rem;color:#a1a1aa;">Harici baglanti tanimli degil.</span>';
      }
      document.getElementById("playerModal").classList.add("open");
    }

    function renderGrid() {
      const q = document.getElementById("searchInp").value.trim().toLowerCase();
      const filtered = ITEMS.filter(function(item) {
        const okCat = !activeCat || item.category === activeCat;
        const okQ = !q || item.title.toLowerCase().indexOf(q) !== -1;
        return okCat && okQ;
      });
      const grid = document.getElementById("grid");
      grid.innerHTML = filtered.map(function(item) {
        return '<div class="card" data-id="' + item.id + '">' +
          '<div><span class="card-badge">' + item.category + '</span>' +
          '<div class="card-title">' + item.title + '</div></div>' +
          '<div class="card-year">' + item.year + '</div>' +
          '</div>';
      }).join("");

      grid.querySelectorAll(".card").forEach(function(card) {
        card.addEventListener("click", function() {
          const item = ITEMS.find(function(x) { return x.id === Number(card.getAttribute("data-id")); });
          if (item) openItemModal(item);
        });
      });
    }

    document.getElementById("searchInp").addEventListener("input", renderGrid);

    document.querySelectorAll("#catTabs button").forEach(function(btn) {
      btn.addEventListener("click", function() {
        document.querySelectorAll("#catTabs button").forEach(function(b) { b.classList.remove("active"); });
        btn.classList.add("active");
        activeCat = btn.getAttribute("data-cat") || "";
        document.getElementById("secTitle").textContent = activeCat || "Katalog";
        renderGrid();
      });
    });

    document.getElementById("closeBtn").addEventListener("click", function() {
      document.getElementById("playerArea").innerHTML = "";
      document.getElementById("playerModal").classList.remove("open");
    });
  </script>
</body>
</html>"""


@app.route("/")
def index():
    return (
        HTML_TEMPLATE.replace("__SUPPORT_URL__", SUPPORT_URL)
        .replace("__SUPPORT_HANDLE__", SUPPORT_HANDLE)
        .replace("__ITEMS_JSON__", json.dumps(CATALOG))
        .replace("__SUPPORT_JSON__", json.dumps(SUPPORT_URL))
        .replace("__HANDLE_JSON__", json.dumps(SUPPORT_HANDLE))
    )


@app.route("/api/send-code", methods=["POST"])
def send_code():
    return jsonify({"ok": True, "code": f"{random.randint(100000, 999999)}"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
