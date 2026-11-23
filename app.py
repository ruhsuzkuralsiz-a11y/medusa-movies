import json
import os
import random
from flask import Flask, jsonify, request

app = Flask(__name__)

SUPPORT_URL = "https://www.instagram.com/ttlewiss21/"
SUPPORT_HANDLE = "@ttlewiss21"

CATALOG = [
    {"id": 1, "title": "Stranger Things", "category": "Diziler", "year": "2016-2026", "note": "Bilim kurgu ve gerilim serisi.", "video_url": ""},
    {"id": 2, "title": "Wednesday", "category": "Diziler", "year": "2022-2026", "note": "Gizem ve karanlik komedi.", "video_url": ""},
    {"id": 3, "title": "Squid Game", "category": "Diziler", "year": "2021-2026", "note": "Hayatta kalma ve strateji.", "video_url": ""},
    {"id": 4, "title": "Dark", "category": "Diziler", "year": "2017-2020", "note": "Zaman dongusu ve gizem.", "video_url": ""},
    {"id": 5, "title": "Breaking Bad", "category": "Diziler", "year": "2008-2013", "note": "Dram ve sucluluk gerilimi.", "video_url": ""},
    {"id": 6, "title": "Peaky Blinders", "category": "Diziler", "year": "2013-2022", "note": "Donem dramasi ve aksiyon.", "video_url": ""},
    {"id": 7, "title": "Inception", "category": "Filmler", "year": "2010", "note": "Zihin ve ruya kurgusu.", "video_url": ""},
    {"id": 8, "title": "Interstellar", "category": "Filmler", "year": "2014", "note": "Uzay ve zaman yolculugu.", "video_url": ""},
    {"id": 9, "title": "The Matrix", "category": "Filmler", "year": "1999", "note": "Siber gerceklik klasigi.", "video_url": ""},
    {"id": 10, "title": "John Wick", "category": "Filmler", "year": "2014", "note": "Yuksek tempolu aksiyon.", "video_url": ""},
    {"id": 11, "title": "Dune", "category": "Filmler", "year": "2021", "note": "Col gezegeni ve buyuk evren.", "video_url": ""},
    {"id": 12, "title": "Fight Club", "category": "Filmler", "year": "1999", "note": "Psikolojik dram ve ters kose.", "video_url": ""},
    {"id": 13, "title": "Solo Leveling", "category": "Animasyon", "year": "2024-2026", "note": "Seviye atlama ve aksiyon.", "video_url": ""},
    {"id": 14, "title": "Attack on Titan", "category": "Animasyon", "year": "2013-2023", "note": "Dev savaslari ve dram.", "video_url": ""},
    {"id": 15, "title": "Jujutsu Kaisen", "category": "Animasyon", "year": "2020-2026", "note": "Lanetler ve ozel gucler.", "video_url": ""},
    {"id": 16, "title": "Arcane", "category": "Animasyon", "year": "2021-2024", "note": "Piltover ve Zaun hikayesi.", "video_url": ""},
    {"id": 17, "title": "Ben 10", "category": "Animasyon", "year": "2005-2021", "note": "Uzayli donusumleri ve macera.", "video_url": ""},
    {"id": 18, "title": "Rick and Morty", "category": "Animasyon", "year": "2013-2026", "note": "Boyutlar arasi bilim kurgu.", "video_url": ""},
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
    .logo { color: #e50914; font-weight: 900; font-size: 1.25rem; letter-spacing: 0.5px; }
    .btn {
      background: #e50914;
      color: #fff;
      border: 0;
      border-radius: 8px;
      padding: 10px 16px;
      font-weight: 700;
      cursor: pointer;
      margin-top: 12px;
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
    .hero h1 { font-size: 1.2rem; margin-bottom: 6px; }
    .hero p { font-size: 0.84rem; color: #d4d4d8; line-height: 1.45; }
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
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
    }
    .card {
      background: #1e1e22;
      border: 1px solid #2c2c32;
      border-radius: 10px;
      padding: 12px 10px;
      min-height: 126px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      cursor: pointer;
    }
    .card-badge {
      display: inline-block;
      font-size: 0.65rem;
      font-weight: 800;
      color: #f87171;
      text-transform: uppercase;
    }
    .card-title { font-size: 0.9rem; font-weight: 800; margin-top: 6px; }
    .card-year { font-size: 0.72rem; color: #a1a1aa; margin-top: 4px; }
    .empty {
      margin: 8px 16px;
      padding: 18px;
      border-radius: 10px;
      background: #1b1b1f;
      color: #b3b3b3;
      font-size: 0.86rem;
      text-align: center;
      display: none;
    }
    .modal {
      display: none;
      position: fixed;
      inset: 0;
      z-index: 50;
      background: rgba(0, 0, 0, 0.85);
      padding: 16px;
      align-items: center;
      justify-content: center;
    }
    .modal.open { display: flex; }
    .modal-box {
      width: 100%;
      max-width: 500px;
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
      <p id="subText">Katalogu inceleyebilir veya sag ustteki Destek butonu ile __HANDLE__ hesabina gecebilirsin.</p>
    </section>

    <div class="search-box">
      <input id="searchInp" type="text" placeholder="Icerik ara..." />
    </div>

    <div class="section-title" id="secTitle">Katalog</div>
    <div class="empty" id="emptyBox">Aramaya uygun icerik bulunamadi.</div>
    <div class="grid" id="grid"></div>
  </div>

  <div class="modal" id="infoModal">
    <div class="modal-box">
      <button class="close-btn" id="closeBtn" type="button">Kapat</button>
      <h3 id="mTitle"></h3>
      <p id="mMeta" style="font-size:0.8rem;color:#a1a1aa;margin-top:6px;"></p>
      <p id="mNote" style="font-size:0.88rem;color:#e4e4e7;margin-top:12px;line-height:1.45;"></p>
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

    function renderGrid() {
      const q = document.getElementById("searchInp").value.trim().toLowerCase();
      const filtered = ITEMS.filter(function(item) {
        const okCat = !activeCat || item.category === activeCat;
        const okQ = !q || item.title.toLowerCase().indexOf(q) !== -1;
        return okCat && okQ;
      });
      const grid = document.getElementById("grid");
      const empty = document.getElementById("emptyBox");
      if (filtered.length === 0) {
        grid.innerHTML = "";
        empty.style.display = "block";
        return;
      }
      empty.style.display = "none";
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
          if (!item) return;
          document.getElementById("mTitle").textContent = item.title;
          document.getElementById("mMeta").textContent = item.category + " · " + item.year;
          document.getElementById("mNote").textContent = item.note;
          document.getElementById("infoModal").classList.add("open");
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
      document.getElementById("infoModal").classList.remove("open");
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
