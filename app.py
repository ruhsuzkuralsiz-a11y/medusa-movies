import os
import random
from flask import Flask, jsonify, request

app = Flask(__name__)

INSTAGRAM_URL = "https://www.instagram.com/ttlewiss21/"
INSTAGRAM_HANDLE = "@ttlewiss21"

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
    .logo { color: #e50914; font-weight: 900; font-size: 1.3rem; }
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
      background: #1c1c1e;
      padding: 12px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #2c2c30;
    }
    .support-link {
      background: #e50914;
      color: #fff;
      text-decoration: none;
      border-radius: 6px;
      padding: 7px 12px;
      font-size: 0.85rem;
      font-weight: 700;
    }
    .box {
      max-width: 440px;
      width: 100%;
      background: #1c1c1e;
      border: 1px solid #2e2e34;
      border-radius: 12px;
      padding: 20px;
      margin-top: 14px;
    }
    .card-box {
      margin: 20px 16px;
      max-width: 480px;
      background: #1c1c1e;
      border: 1px solid #2e2e34;
      border-radius: 12px;
      padding: 18px;
    }
    .clickable-link {
      display: inline-block;
      margin-top: 10px;
      color: #f87171;
      font-weight: 700;
      text-decoration: underline;
      word-break: break-all;
    }
    .action-btn {
      display: inline-block;
      margin-top: 14px;
      background: #e50914;
      color: #fff;
      text-decoration: none;
      border-radius: 8px;
      padding: 10px 16px;
      font-weight: 700;
      font-size: 0.9rem;
    }
    input {
      width: 100%;
      background: #121214;
      border: 1px solid #35353d;
      color: #fff;
      border-radius: 8px;
      padding: 10px;
      margin-top: 10px;
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
      <a class="support-link" href="__IG_URL__" target="_blank" rel="noopener noreferrer">Destek</a>
    </header>

    <div class="card-box">
      <h1 id="welcomeText">Hos Geldin</h1>
      <p style="color:#d4d4d8;margin-top:8px;line-height:1.45;">
        Bana ulasmak, destek olmak veya topluluga katilmak icin asagidaki baglantiyi kullanabilirsin:
      </p>
      <a class="clickable-link" href="__IG_URL__" target="_blank" rel="noopener noreferrer">__IG_URL__</a>
      <div>
        <a class="action-btn" href="__IG_URL__" target="_blank" rel="noopener noreferrer">Instagram'a Git (__IG_HANDLE__)</a>
      </div>
    </div>
  </div>

  <script>
    const IG_URL = __IG_URL_JSON__;
    const IG_HANDLE = __IG_HANDLE_JSON__;
    let profileName = "Medusa";
    let codeVal = "";

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
      openScreen("aScreen");
    });
  </script>
</body>
</html>"""


@app.route("/")
def index():
    import json
    return (
        HTML_TEMPLATE.replace("__IG_URL__", INSTAGRAM_URL)
        .replace("__IG_HANDLE__", INSTAGRAM_HANDLE)
        .replace("__IG_URL_JSON__", json.dumps(INSTAGRAM_URL))
        .replace("__IG_HANDLE_JSON__", json.dumps(INSTAGRAM_HANDLE))
    )


@app.route("/api/send-code", methods=["POST"])
def send_code():
    return jsonify({"ok": True, "code": f"{random.randint(100000, 999999)}"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
