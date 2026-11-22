import os
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

SAMPLE_VIDEO_1 = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
SAMPLE_VIDEO_2 = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4"
SAMPLE_VIDEO_3 = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4"
SAMPLE_VIDEO_4 = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"

POSTER_1 = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Big_buck_bunny_poster_big.jpg/480px-Big_buck_bunny_poster_big.jpg"
POSTER_2 = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Sintel_poster.jpg/480px-Sintel_poster.jpg"
POSTER_3 = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Tears_of_Steel_poster.jpg/480px-Tears_of_Steel_poster.jpg"
POSTER_4 = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Elephants_Dream_s5_both.jpg/480px-Elephants_Dream_s5_both.jpg"

CATALOG = [
    {"id": 101, "title": "Big Buck Bunny", "category": "Animasyon", "year": "2026", "quality": "1080p HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-01", "approved": True, "poster": POSTER_1, "glow": "#00e5ff", "video_url": SAMPLE_VIDEO_1},
    {"id": 102, "title": "Sintel Özel Seçki", "category": "Animasyon", "year": "2026", "quality": "1080p HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-02", "approved": True, "poster": POSTER_2, "glow": "#a855f7", "video_url": SAMPLE_VIDEO_2},
    {"id": 103, "title": "Tears of Steel", "category": "Filmler", "year": "2026", "quality": "4K / HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-03", "approved": True, "poster": POSTER_3, "glow": "#3b82f6", "video_url": SAMPLE_VIDEO_3},
    {"id": 104, "title": "Elephant's Dream Bölüm 1", "category": "Diziler", "year": "2026", "quality": "HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-04", "approved": True, "poster": POSTER_4, "glow": "#f59e0b", "video_url": SAMPLE_VIDEO_4},
    {"id": 105, "title": "Medusa Stüdyo Özel Yapım", "category": "Filmler", "year": "2026", "quality": "1080p HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-05", "approved": True, "poster": POSTER_1, "glow": "#ef4444", "video_url": SAMPLE_VIDEO_3},
    {"id": 106, "title": "Medusa Seri Arşivi", "category": "Diziler", "year": "2026", "quality": "1080p HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-06", "approved": True, "poster": POSTER_2, "glow": "#10b981", "video_url": SAMPLE_VIDEO_4},
    {"id": 107, "title": "Gece Vardiyası", "category": "Filmler", "year": "2026", "quality": "1080p HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-07", "approved": True, "poster": POSTER_3, "glow": "#06b6d4", "video_url": SAMPLE_VIDEO_3},
    {"id": 108, "title": "Kayıp Sinyal", "category": "Filmler", "year": "2026", "quality": "4K / HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-08", "approved": True, "poster": POSTER_1, "glow": "#ec4899", "video_url": SAMPLE_VIDEO_1},
    {"id": 109, "title": "Son Rota", "category": "Filmler", "year": "2026", "quality": "1080p HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-09", "approved": True, "poster": POSTER_2, "glow": "#f97316", "video_url": SAMPLE_VIDEO_2},
    {"id": 110, "title": "Çelik Şehir", "category": "Filmler", "year": "2026", "quality": "1080p HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-10", "approved": True, "poster": POSTER_3, "glow": "#8b5cf6", "video_url": SAMPLE_VIDEO_3},
    {"id": 111, "title": "Karanlık Koridor", "category": "Filmler", "year": "2026", "quality": "HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-11", "approved": True, "poster": POSTER_4, "glow": "#eab308", "video_url": SAMPLE_VIDEO_4},
    {"id": 112, "title": "Medusa Seçkisi: Final", "category": "Filmler", "year": "2026", "quality": "4K / HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-12", "approved": True, "poster": POSTER_1, "glow": "#22c55e", "video_url": SAMPLE_VIDEO_1},
    {"id": 113, "title": "Sıfır Noktası", "category": "Filmler", "year": "2026", "quality": "1080p HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-13", "approved": True, "poster": POSTER_2, "glow": "#38bdf8", "video_url": SAMPLE_VIDEO_2},
    {"id": 114, "title": "Gölgelerin İzinde", "category": "Filmler", "year": "2026", "quality": "4K / HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-14", "approved": True, "poster": POSTER_3, "glow": "#f43f5e", "video_url": SAMPLE_VIDEO_3},
    {"id": 115, "title": "Derin Dosya", "category": "Diziler", "year": "2026", "quality": "1080p HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-15", "approved": True, "poster": POSTER_4, "glow": "#a855f7", "video_url": SAMPLE_VIDEO_4},
    {"id": 116, "title": "Yıldız Tozu Seçkisi", "category": "Animasyon", "year": "2026", "quality": "1080p HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-16", "approved": True, "poster": POSTER_1, "glow": "#14b8a6", "video_url": SAMPLE_VIDEO_1},
    {"id": 117, "title": "Kızıl Ufuk", "category": "Filmler", "year": "2026", "quality": "1080p HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-17", "approved": True, "poster": POSTER_2, "glow": "#fb7185", "video_url": SAMPLE_VIDEO_2},
    {"id": 118, "title": "Buzul Kırığı", "category": "Filmler", "year": "2026", "quality": "4K / HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-18", "approved": True, "poster": POSTER_3, "glow": "#60a5fa", "video_url": SAMPLE_VIDEO_3},
    {"id": 119, "title": "Zaman Kasası", "category": "Filmler", "year": "2026", "quality": "1080p HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-19", "approved": True, "poster": POSTER_4, "glow": "#c084fc", "video_url": SAMPLE_VIDEO_4},
    {"id": 120, "title": "Medusa Gecesi: Özel", "category": "Filmler", "year": "2026", "quality": "4K / HD", "audio": "Onaylı Ses", "license_tag": "LISANS-ONAY-20", "approved": True, "poster": POSTER_1, "glow": "#34d399", "video_url": SAMPLE_VIDEO_1},
]

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
      background: #0b0b0e;
      color: #fff;
      font-family: system-ui, -apple-system, sans-serif;
      padding-bottom: 76px;
    }
    header {
      position: sticky;
      top: 0;
      z-index: 20;
      background: #121217;
      border-bottom: 1px solid #23232d;
      padding: 12px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }
    .brand {
      color: #ef4444;
      font-weight: 800;
      font-size: 1.1rem;
      letter-spacing: 0.5px;
    }
    .count {
      font-size: 0.8rem;
      color: #a1a1aa;
    }
    .toolbar {
      padding: 10px 14px;
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      background: #0e0e13;
      border-bottom: 1px solid #1e1e27;
    }
    input, select {
      background: #181820;
      color: #fff;
      border: 1px solid #2b2b38;
      border-radius: 8px;
      padding: 8px 10px;
      font-size: 0.9rem;
    }
    input { flex: 1; min-width: 150px; }
    .grid {
      padding: 12px;
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
    }
    .card {
      background: #15151c;
      border: 1px solid #242430;
      border-radius: 10px;
      overflow: hidden;
      cursor: pointer;
    }
    .card img {
      width: 100%;
      aspect-ratio: 2 / 3;
      object-fit: cover;
      display: block;
      background: #1e1e28;
    }
    .card-body {
      padding: 7px 8px;
    }
    .card-title {
      font-size: 0.82rem;
      font-weight: 700;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .card-meta {
      font-size: 0.7rem;
      color: #a1a1aa;
      margin-top: 2px;
    }
    .modal {
      display: none;
      position: fixed;
      inset: 0;
      z-index: 50;
      background: rgba(0, 0, 0, 0.88);
      padding: 16px;
      align-items: center;
      justify-content: center;
    }
    .modal.open { display: flex; }
    .modal-box {
      width: 100%;
      max-width: 540px;
      background: #15151d;
      border: 1px solid #2c2c3a;
      border-radius: 12px;
      padding: 14px;
    }
    video {
      width: 100%;
      max-height: 280px;
      border-radius: 8px;
      background: #000;
      margin-top: 10px;
    }
    .close-btn {
      float: right;
      background: #ef4444;
      color: #fff;
      border: 0;
      border-radius: 6px;
      padding: 5px 10px;
      font-weight: 700;
      cursor: pointer;
    }
    nav {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: #121217;
      border-top: 1px solid #23232d;
      display: flex;
      justify-content: space-around;
      padding: 8px 0;
    }
    nav button {
      background: none;
      border: 0;
      color: #a1a1aa;
      font-size: 0.78rem;
      cursor: pointer;
    }
    nav button.active { color: #fff; font-weight: 700; }
  </style>
</head>
<body>
  <header>
    <div class="brand">MEDUSAFILM</div>
    <div class="count" id="itemCount">{{ items|length }} İçerik</div>
  </header>

  <div class="toolbar">
    <input id="searchInput" type="text" placeholder="Film, dizi veya animasyon ara..." />
    <select id="categorySelect">
      <option value="">Tümü</option>
      <option value="Filmler">Filmler</option>
      <option value="Diziler">Diziler</option>
      <option value="Animasyon">Animasyon</option>
    </select>
  </div>

  <div class="grid" id="grid"></div>

  <div class="modal" id="playerModal">
    <div class="modal-box">
      <button class="close-btn" id="closeModal">Kapat</button>
      <h3 id="modalTitle"></h3>
      <p class="card-meta" id="modalMeta"></p>
      <video id="videoPlayer" controls playsinline></video>
    </div>
  </div>

  <nav>
    <button class="active" data-cat="">Ana Sayfa</button>
    <button data-cat="Filmler">Filmler</button>
    <button data-cat="Diziler">Diziler</button>
    <button data-cat="Animasyon">Animasyon</button>
  </nav>

  <script>
    const INITIAL_ITEMS = {{ items|tojson }};
    let currentItems = INITIAL_ITEMS;

    const grid = document.getElementById("grid");
    const countEl = document.getElementById("itemCount");
    const searchInput = document.getElementById("searchInput");
    const categorySelect = document.getElementById("categorySelect");
    const modal = document.getElementById("playerModal");
    const videoPlayer = document.getElementById("videoPlayer");

    function renderGrid(list) {
      countEl.textContent = `${list.length} İçerik`;
      grid.innerHTML = list.map(item => `
        <div class="card" onclick="openItem(${item.id})">
          <img src="${item.poster}" alt="${item.title}" loading="lazy" />
          <div class="card-body">
            <div class="card-title">${item.title}</div>
            <div class="card-meta">${item.category} · ${item.quality}</div>
          </div>
        </div>
      `).join("");
    }

    function openItem(id) {
      const item = currentItems.find(x => x.id === id);
      if (!item) return;
      document.getElementById("modalTitle").textContent = item.title;
      document.getElementById("modalMeta").textContent = `${item.category} · ${item.year} · ${item.quality} · ${item.license_tag}`;
      videoPlayer.src = item.video_url;
      modal.classList.add("open");
      videoPlayer.play().catch(() => {});
    }

    document.getElementById("closeModal").onclick = () => {
      videoPlayer.pause();
      videoPlayer.removeAttribute("src");
      modal.classList.remove("open");
    };

    async function filterCatalog() {
      const q = searchInput.value.trim();
      const cat = categorySelect.value;
      const params = new URLSearchParams();
      if (q) params.set("q", q);
      if (cat) params.set("category", cat);
      const res = await fetch(`/api/catalog?${params.toString()}`);
      const data = await res.json();
      currentItems = data.items || [];
      renderGrid(currentItems);
    }

    searchInput.addEventListener("input", filterCatalog);
    categorySelect.addEventListener("change", filterCatalog);

    document.querySelectorAll("nav button").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll("nav button").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        categorySelect.value = btn.dataset.cat;
        filterCatalog();
      });
    });

    renderGrid(currentItems);
  </script>
</body>
</html>
"""


def get_approved_catalog():
    return [item for item in CATALOG if item.get("approved")]


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, items=get_approved_catalog())


@app.route("/api/catalog")
def api_catalog():
    q = (request.args.get("q") or "").strip().lower()
    category = (request.args.get("category") or "").strip()
    items = get_approved_catalog()
    if category:
        items = [x for x in items if x.get("category") == category]
    if q:
        items = [x for x in items if q in x.get("title", "").lower() or q in x.get("category", "").lower()]
    return jsonify({"count": len(items), "items": items})


@app.route("/health")
def health():
    return jsonify({"status": "ok", "count": len(get_approved_catalog())})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
