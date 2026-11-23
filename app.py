import os
from flask import Flask, render_template_string

app = Flask(__name__)

OVERLAY_HTML = r"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MEDUSA - Yayın Banner & Sesli Bildirim</title>
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

    .overlay-hidden .top-banner,
    .overlay-hidden .bottom-banner,
    .overlay-hidden .alert-strip {
      display: none !important;
    }

    /* ÜST BAR (TEK TUŞ KONTROLLER) */
    .top-controls {
      position: fixed;
      top: 6px;
      right: 6px;
      z-index: 60;
      display: flex;
      gap: 5px;
      align-items: center;
    }

    .ctrl-btn {
      background: rgba(15, 20, 17, 0.92);
      color: #39ff14;
      border: 1px solid rgba(57, 255, 20, 0.65);
      border-radius: 6px;
      padding: 4px 8px;
      font-size: 0.66rem;
      font-weight: 800;
      cursor: pointer;
      white-space: nowrap;
    }

    .ctrl-btn.live-btn {
      background: #39ff14;
      color: #000000;
      border-color: #39ff14;
    }

    .ctrl-btn.off-state {
      background: rgba(45, 14, 14, 0.94);
      color: #ff9e9e;
      border-color: rgba(255, 90, 90, 0.7);
    }

    /* ÜST BANNER */
    .top-banner {
      min-height: 60px;
      max-height: 13vh;
      background: linear-gradient(135deg, rgba(10, 14, 12, 0.94), rgba(18, 34, 24, 0.94));
      border-bottom: 2px solid #39ff14;
      box-shadow: 0 4px 16px rgba(57, 255, 20, 0.2);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 5px 12px;
      text-align: center;
    }

    .brand-title {
      font-size: clamp(1.1rem, 3.4vw, 1.75rem);
      font-weight: 900;
      letter-spacing: 3.5px;
      color: #39ff14;
      text-shadow: 0 0 12px rgba(57, 255, 20, 0.55);
      line-height: 1.05;
    }

    .sub-tag {
      margin-top: 2px;
      font-size: clamp(0.6rem, 1.4vw, 0.74rem);
      font-weight: 700;
      letter-spacing: 1.1px;
      color: #e6ffe6;
      background: rgba(57, 255, 20, 0.12);
      border: 1px solid rgba(57, 255, 20, 0.45);
      padding: 2px 10px;
      border-radius: 999px;
      white-space: nowrap;
    }

    .game-area {
      flex: 1;
      background: transparent;
      pointer-events: none;
    }

    .alert-strip {
      display: none;
      align-items: center;
      justify-content: center;
      gap: 6px;
      background: rgba(10, 20, 14, 0.96);
      border-top: 1px solid rgba(57, 255, 20, 0.55);
      padding: 4px 10px;
      font-size: clamp(0.66rem, 1.6vw, 0.78rem);
      font-weight: 700;
      color: #b7ffb0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .alert-strip.show {
      display: flex;
    }

    .bottom-banner {
      min-height: 72px;
      max-height: 16vh;
      background: linear-gradient(180deg, rgba(14, 18, 16, 0.95), rgba(8, 10, 9, 0.98));
      border-top: 2px solid #39ff14;
      box-shadow: 0 -4px 16px rgba(57, 255, 20, 0.18);
      padding: 6px 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }

    .bottom-left {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 2px;
      min-width: 0;
    }

    .channel-name {
      font-size: clamp(0.84rem, 2.4vw, 1.12rem);
      font-weight: 900;
      color: #ffffff;
      letter-spacing: 0.4px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .channel-name span {
      color: #39ff14;
    }

    .live-note {
      font-size: clamp(0.64rem, 1.6vw, 0.76rem);
      color: #b9c7bc;
      line-height: 1.2;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .action-list {
      display: flex;
      flex-direction: column;
      gap: 4px;
      width: auto;
      max-width: 145px;
      flex-shrink: 0;
    }

    .action-btn {
      background: rgba(24, 28, 26, 0.95);
      border: 1px solid rgba(57, 255, 20, 0.65);
      border-radius: 7px;
      padding: 4px 8px;
      font-size: clamp(0.6rem, 1.45vw, 0.72rem);
      font-weight: 800;
      color: #ffffff;
      text-transform: uppercase;
      letter-spacing: 0.4px;
      display: flex;
      align-items: center;
      gap: 5px;
      white-space: nowrap;
    }

    .dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #39ff14;
      box-shadow: 0 0 6px #39ff14;
      flex-shrink: 0;
    }

    @media (orientation: landscape) and (max-height: 500px) {
      .top-banner {
        min-height: 42px;
        max-height: 12vh;
        padding: 3px 10px;
      }
      .brand-title {
        font-size: 1rem;
        letter-spacing: 2.5px;
      }
      .sub-tag {
        font-size: 0.56rem;
        padding: 1px 8px;
        margin-top: 1px;
      }
      .bottom-banner {
        min-height: 50px;
        max-height: 15vh;
        padding: 4px 10px;
      }
      .action-list {
        flex-direction: row;
        max-width: none;
        gap: 5px;
      }
      .action-btn {
        padding: 3px 7px;
        font-size: 0.58rem;
      }
    }

    .panel {
      display: none;
      position: fixed;
      top: 34px;
      right: 6px;
      z-index: 60;
      width: 245px;
      max-height: 82vh;
      overflow-y: auto;
      background: rgba(12, 16, 14, 0.98);
      border: 1.5px solid #39ff14;
      border-radius: 10px;
      padding: 9px;
    }

    .panel.open {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .section-label {
      font-size: 0.64rem;
      font-weight: 800;
      color: #39ff14;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-top: 2px;
    }

    .panel input[type="text"] {
      width: 100%;
      padding: 5px 7px;
      border-radius: 6px;
      border: 1px solid rgba(57, 255, 20, 0.4);
      background: #080b09;
      color: #fff;
      font-size: 0.72rem;
    }

    .volume-row {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.68rem;
      color: #d7e5da;
    }

    .volume-row input[type="range"] {
      flex: 1;
      accent-color: #39ff14;
    }

    .btn-row {
      display: flex;
      gap: 5px;
      flex-wrap: wrap;
    }

    .panel button {
      flex: 1;
      padding: 5px 6px;
      border: none;
      border-radius: 6px;
      background: #39ff14;
      color: #000;
      font-weight: 800;
      font-size: 0.68rem;
      cursor: pointer;
      white-space: nowrap;
    }

    .panel button.secondary {
      background: #1a241e;
      color: #d8ffd4;
      border: 1px solid rgba(57, 255, 20, 0.45);
    }
  </style>
</head>
<body>
  <div class="top-controls">
    <button class="ctrl-btn live-btn" id="toggleOverlayBtn" onclick="toggleOverlayVisibility()">YAYINDA: AÇIK</button>
    <button class="ctrl-btn" onclick="togglePanel()">AYAR / SES</button>
  </div>

  <div class="panel" id="editPanel">
    <div class="section-label">Banner Metinleri</div>
    <input type="text" id="inTitle" value="MEDUSA" placeholder="Üst başlık" />
    <input type="text" id="inSub" value="CANLI YAYIN • İYİ SEYİRLER" placeholder="Alt etiket" />
    <input type="text" id="inChannel" value="@MEDUSA" placeholder="Kanal adı" />
    <input type="text" id="inNote" value="Desteğin için teşekkürler!" placeholder="Alt not" />
    <button onclick="applyBanner()">BANNER UYGULA</button>

    <div class="section-label">Ses & Okuma Ayarı</div>
    <div class="volume-row">
      <span>Ses:</span>
      <input type="range" id="volumeRange" min="0" max="100" value="85" oninput="updateVolumeLabel()" />
      <span id="volumeText">85%</span>
    </div>
    <input type="text" id="inPrefix" value="." placeholder="Yorum öneki (örn: .)" />

    <div class="section-label">Yorum / Takip / Hediye Test</div>
    <input type="text" id="inUser" value="Ahmet" placeholder="Kullanıcı adı" />
    <input type="text" id="inComment" value=".merhaba" placeholder="Yorum (örn: .merhaba)" />
    <div class="btn-row">
      <button onclick="handleSimulatedComment()">YORUM OKU</button>
      <button class="secondary" onclick="handleFollowEvent()">TAKİP</button>
      <button class="secondary" onclick="handleGiftEvent()">HEDİYE</button>
    </div>
  </div>

  <header class="top-banner">
    <div class="brand-title" id="outTitle">MEDUSA</div>
    <div class="sub-tag" id="outSub">CANLI YAYIN • İYİ SEYİRLER</div>
  </header>

  <main class="game-area"></main>

  <div class="alert-strip" id="alertStrip">
    <span class="dot"></span>
    <span id="alertText">Hazır</span>
  </div>

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
    let alertTimer = null;
    let overlayVisible = true;

    function toggleOverlayVisibility() {
      overlayVisible = !overlayVisible;
      document.body.classList.toggle('overlay-hidden', !overlayVisible);
      const btn = document.getElementById('toggleOverlayBtn');
      if (overlayVisible) {
        btn.textContent = 'YAYINDA: AÇIK';
        btn.classList.remove('off-state');
        btn.classList.add('live-btn');
      } else {
        btn.textContent = 'YAYINDA: GİZLİ';
        btn.classList.remove('live-btn');
        btn.classList.add('off-state');
      }
    }

    function togglePanel() {
      document.getElementById('editPanel').classList.toggle('open');
    }

    function updateVolumeLabel() {
      const val = document.getElementById('volumeRange').value;
      document.getElementById('volumeText').textContent = `${val}%`;
    }

    function getVolumeFloat() {
      const val = Number(document.getElementById('volumeRange').value || 85);
      return Math.max(0, Math.min(1, val / 100));
    }

    function speakText(text) {
      if (!('speechSynthesis' in window) || !text) return;
      window.speechSynthesis.cancel();
      const utter = new SpeechSynthesisUtterance(text);
      utter.lang = 'tr-TR';
      utter.volume = getVolumeFloat();
      utter.rate = 1.02;
      window.speechSynthesis.speak(utter);
    }

    function showAlertBanner(visualText, spokenText) {
      const strip = document.getElementById('alertStrip');
      const alertText = document.getElementById('alertText');
      alertText.textContent = visualText;
      strip.classList.add('show');

      if (alertTimer) clearTimeout(alertTimer);
      alertTimer = setTimeout(() => {
        strip.classList.remove('show');
      }, 4500);

      speakText(spokenText);
    }

    function applyBanner() {
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

    function handleSimulatedComment() {
      const user = document.getElementById('inUser').value.trim() || 'İzleyici';
      const comment = document.getElementById('inComment').value.trim();
      const prefix = document.getElementById('inPrefix').value.trim();

      if (!comment) return;

      if (prefix && !comment.startsWith(prefix)) {
        showAlertBanner(`Önek eşleşmedi (${prefix} ile başlamalı)`, '');
        return;
      }

      const cleanMsg = prefix ? comment.slice(prefix.length).trim() : comment;
      const finalSpeech = cleanMsg || comment;
      showAlertBanner(`${user}: ${comment}`, `${user} diyor ki: ${finalSpeech}`);
    }

    function handleFollowEvent() {
      const user = document.getElementById('inUser').value.trim() || 'Yeni Takipçi';
      showAlertBanner(`Yeni Takip: ${user} — Hoş geldiniz!`, `${user}, hoş geldiniz!`);
    }

    function handleGiftEvent(giftName = 'Gül', count = 1) {
      const user = document.getElementById('inUser').value.trim() || 'Bir İzleyici';
      const gName = document.getElementById('inComment').value.startsWith('.')
        ? 'Hediye'
        : (document.getElementById('inComment').value.trim() || giftName);
      showAlertBanner(`Hediye: ${user} (${count}x ${gName})`, `${user}, ${count} adet ${gName} hediye gönderdi, teşekkürler!`);
    }

    window.MedusaLiveEvents = {
      onComment: (user, text) => {
        document.getElementById('inUser').value = user;
        document.getElementById('inComment').value = text;
        handleSimulatedComment();
      },
      onFollow: (user) => {
        document.getElementById('inUser').value = user;
        handleFollowEvent();
      },
      onGift: (user, giftName, count = 1) => {
        document.getElementById('inUser').value = user;
        showAlertBanner(`Hediye: ${user} (${count}x ${giftName})`, `${user}, ${count} adet ${giftName} hediye gönderdi, teşekkürler!`);
      }
    };
  </script>
</body>
</html>"""

@app.route("/")
def home():
    return "MEDUSA Overlay Aktif. Banner için /overlay adresine git."

@app.route("/overlay")
def overlay():
    return render_template_string(OVERLAY_HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
