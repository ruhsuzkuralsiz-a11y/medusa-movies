import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Kendi TMDB API anahtarını buraya ya da ortam değişkenine (TMDB_API_KEY) gir
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "BURAYA_TMDB_API_KEY_YAZ")
TMDB_BASE = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/w500"

# İsteğe bağlı özel kartlar
CUSTOM_ITEMS = []


def fetch_tmdb_movies(endpoint: str, page: int = 1):
    if not TMDB_API_KEY or TMDB_API_KEY == "BURAYA_TMDB_API_KEY_YAZ":
        return []
    try:
        resp = requests.get(
            f"{TMDB_BASE}/{endpoint}",
            params={
                "api_key": TMDB_API_KEY,
                "language": "tr-TR",
                "page": page,
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        movies = []
        for item in data.get("results", []):
            poster_path = item.get("poster_path")
            movies.append({
                "id": f"tmdb-{item.get('id')}",
                "tmdb_id": item.get("id"),
                "title": item.get("title") or item.get("name") or "İsimsiz Film",
                "year": (item.get("release_date") or "")[:4] or "—",
                "rating": round(float(item.get("vote_average") or 0), 1),
                "overview": item.get("overview") or "Bu film için henüz Türkçe özet eklenmemiş.",
                "poster": f"{IMG_BASE}{poster_path}" if poster_path else "",
                "category": "Vizyonda" if "now_playing" in endpoint else "Filmler",
                "source": "tmdb",
                "embed_url": None,
                "external_url": None,
            })
        return movies
    except Exception:
        return []


def fetch_archive_movies(query: str = "", rows: int = 24):
    # Internet Archive üzerinde kamu malı / açık arşiv video kayıtları
    q_parts = [
        'mediatype:(movies)',
        '(collection:(feature_films) OR collection:(opensource_movies) OR collection:(classic_tv) OR subject:("public domain"))',
    ]
    if query:
        safe_q = query.replace('"', "").strip()
        if safe_q:
            q_parts.append(f'({safe_q})')

    search_query = " AND ".join(q_parts)
    try:
        resp = requests.get(
            "https://archive.org/advancedsearch.php",
            params={
                "q": search_query,
                "fl[]": ["identifier", "title", "year", "description"],
                "sort[]": "downloads desc",
                "rows": rows,
                "page": 1,
                "output": "json",
            },
            timeout=12,
        )
        resp.raise_for_status()
        docs = resp.json().get("response", {}).get("docs", [])
        items = []
        for doc in docs:
            ident = doc.get("identifier")
            if not ident:
                continue
            desc = doc.get("description")
            if isinstance(desc, list):
                desc_text = " ".join(str(x) for x in desc if x)
            else:
                desc_text = str(desc or "")
            clean_desc = " ".join(desc_text.split())
            if not clean_desc:
                clean_desc = "Internet Archive açık arşiv kaydı."
            elif len(clean_desc) > 280:
                clean_desc = clean_desc[:277] + "..."

            year_val = doc.get("year")
            if isinstance(year_val, list):
                year_str = str(year_val[0])[:4] if year_val else "—"
            else:
                year_str = str(year_val)[:4] if year_val else "—"

            items.append({
                "id": f"ia-{ident}",
                "tmdb_id": None,
                "title": str(doc.get("title") or ident),
                "year": year_str or "—",
                "rating": "Arşiv",
                "overview": clean_desc,
                "poster": f"https://archive.org/services/img/{ident}",
                "category": "Açık Arşiv",
                "source": "archive",
                "embed_url": f"https://archive.org/embed/{ident}",
                "external_url": f"https://archive.org/details/{ident}",
            })
        return items
    except Exception:
        return []


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/movies")
def api_movies():
    category = request.args.get("category", "Tümü")
    query = request.args.get("q", "").strip()
    q_lower = query.lower()

    combined = []

    if category in ("Tümü", "Vizyonda", "Filmler"):
        now_playing = fetch_tmdb_movies("movie/now_playing", page=1)
        popular = fetch_tmdb_movies("movie/popular", page=1)
        seen_ids = set()

        for m in now_playing:
            if m["id"] not in seen_ids:
                seen_ids.add(m["id"])
                combined.append(m)

        for m in popular:
            if m["id"] not in seen_ids:
                seen_ids.add(m["id"])
                combined.append(m)

    if category in ("Tümü", "Açık Arşiv"):
        archive_rows = 12 if category == "Tümü" else 28
        archive_list = fetch_archive_movies(query=query, rows=archive_rows)
        combined.extend(archive_list)

    for item in CUSTOM_ITEMS:
        combined.append(item)

    if category == "Vizyonda":
        filtered = [m for m in combined if m["category"] == "Vizyonda"]
    elif category == "Filmler":
        filtered = [m for m in combined if m["category"] == "Filmler"]
    elif category == "Açık Arşiv":
        filtered = [m for m in combined if m["category"] == "Açık Arşiv"]
    else:
        filtered = combined

    if q_lower:
        filtered = [
            m for m in filtered
            if q_lower in str(m["title"]).lower() or q_lower in str(m["overview"]).lower()
        ]

    return jsonify({
        "movies": filtered,
        "has_api_key": bool(TMDB_API_KEY and TMDB_API_KEY != "BURAYA_TMDB_API_KEY_YAZ"),
    })


@app.route("/api/movie/<int:tmdb_id>/trailer")
def api_movie_trailer(tmdb_id: int):
    if not TMDB_API_KEY or TMDB_API_KEY == "BURAYA_TMDB_API_KEY_YAZ":
        return jsonify({"youtube_url": None, "embed_url": None})
    try:
        resp = requests.get(
            f"{TMDB_BASE}/movie/{tmdb_id}/videos",
            params={"api_key": TMDB_API_KEY, "language": "tr-TR"},
            timeout=10,
        )
        videos = resp.json().get("results", [])

        if not videos:
            resp_en = requests.get(
                f"{TMDB_BASE}/movie/{tmdb_id}/videos",
                params={"api_key": TMDB_API_KEY, "language": "en-US"},
                timeout=10,
            )
            videos = resp_en.json().get("results", [])

        for v in videos:
            if v.get("site") == "YouTube" and v.get("key"):
                return jsonify({
                    "youtube_url": f"https://www.youtube.com/watch?v={v['key']}",
                    "embed_url": f"https://www.youtube.com/embed/{v['key']}",
                })
    except Exception:
        pass
    return jsonify({"youtube_url": None, "embed_url": None})


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
      background: #0d0f14;
      color: #f3f4f6;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      min-height: 100vh;
    }
    header {
      position: sticky;
      top: 0;
      z-index: 20;
      background: rgba(13, 15, 20, 0.92);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid #1f2430;
      padding: 12px 16px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }
    .brand {
      font-size: 1.25rem;
      font-weight: 800;
      letter-spacing: 1px;
      background: linear-gradient(90deg, #f59e0b, #ef4444);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .tabs {
      display: flex;
      gap: 8px;
      overflow-x: auto;
    }
    .tab-btn {
      background: #181c26;
      color: #cbd5e1;
      border: 1px solid #262c3a;
      padding: 7px 14px;
      border-radius: 999px;
      cursor: pointer;
      font-size: 0.9rem;
      white-space: nowrap;
    }
    .tab-btn.active {
      background: #f59e0b;
      color: #111827;
      border-color: #f59e0b;
      font-weight: 700;
    }
    .support-btn {
      background: #22c55e;
      color: #08130b;
      text-decoration: none;
      padding: 7px 14px;
      border-radius: 999px;
      font-weight: 700;
      font-size: 0.9rem;
    }
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 18px 16px 40px;
    }
    .search-box {
      width: 100%;
      padding: 12px 14px;
      border-radius: 10px;
      border: 1px solid #262c3a;
      background: #151922;
      color: #f9fafb;
      font-size: 1rem;
      margin-bottom: 18px;
    }
    .notice {
      background: #1c1917;
      border: 1px solid #78350f;
      color: #fde68a;
      padding: 12px 14px;
      border-radius: 10px;
      margin-bottom: 16px;
      font-size: 0.92rem;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 14px;
    }
    @media (min-width: 768px) {
      .grid {
        grid-template-columns: repeat(4, 1fr);
        gap: 18px;
      }
    }
    .card {
      background: #151922;
      border: 1px solid #222836;
      border-radius: 12px;
      overflow: hidden;
      cursor: pointer;
      transition: transform 0.15s ease, border-color 0.15s ease;
      display: flex;
      flex-direction: column;
    }
    .card:hover {
      transform: translateY(-3px);
      border-color: #f59e0b;
    }
    .poster-wrap {
      position: relative;
      aspect-ratio: 2 / 3;
      background: #0f1218;
    }
    .poster-wrap img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
    .badge {
      position: absolute;
      top: 8px;
      left: 8px;
      background: rgba(245, 158, 11, 0.92);
      color: #111827;
      font-size: 0.72rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
    }
    .badge.archive {
      background: rgba(34, 197, 94, 0.92);
      color: #07140b;
    }
    .card-body {
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .card-title {
      font-size: 0.95rem;
      font-weight: 700;
      line-height: 1.3;
    }
    .card-meta {
      display: flex;
      justify-content: space-between;
      font-size: 0.82rem;
      color: #9ca3af;
    }
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.78);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 16px;
      z-index: 50;
    }
    .modal-backdrop.open {
      display: flex;
    }
    .modal {
      background: #151922;
      border: 1px solid #2c3446;
      border-radius: 14px;
      max-width: 720px;
      width: 100%;
      max-height: 90vh;
      overflow-y: auto;
      padding: 18px;
    }
    .modal-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }
    .close-btn {
      background: #242a38;
      color: #f3f4f6;
      border: none;
      border-radius: 8px;
      padding: 6px 12px;
      cursor: pointer;
      font-size: 0.95rem;
    }
    .video-box {
      width: 100%;
      aspect-ratio: 16 / 9;
      background: #0b0d12;
      border-radius: 10px;
      overflow: hidden;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #9ca3af;
      text-align: center;
      padding: 12px;
    }
    .video-box iframe {
      width: 100%;
      height: 100%;
      border: none;
    }
    .modal-overview {
      color: #d1d5db;
      line-height: 1.55;
      font-size: 0.95rem;
      margin-bottom: 14px;
    }
    .modal-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }
    .btn-link {
      background: #f59e0b;
      color: #111827;
      text-decoration: none;
      padding: 9px 14px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.9rem;
    }
  </style>
</head>
<body>
  <header>
    <div class="brand">MEDUSAFILM</div>
    <div class="tabs">
      <button class="tab-btn active" data-cat="Tümü">Tümü</button>
      <button class="tab-btn" data-cat="Vizyonda">Vizyonda</button>
      <button class="tab-btn" data-cat="Filmler">Filmler</button>
      <button class="tab-btn" data-cat="Açık Arşiv">Açık Arşiv</button>
    </div>
    <a class="support-btn" href="https://www.instagram.com/ttlewiss21/" target="_blank" rel="noopener">Destek</a>
  </header>

  <main class="container">
    <input id="searchInput" class="search-box" type="text" placeholder="Film adı veya açıklama ara..." />
    <div id="apiNotice" class="notice" style="display:none;">
      TMDB API anahtarı girilmediği için Vizyonda/Filmler listesi boş gelebilir; <b>Açık Arşiv</b> sekmesindeki filmleri yine de görebilirsin.
    </div>
    <div id="movieGrid" class="grid"></div>
  </main>

  <div id="movieModal" class="modal-backdrop">
    <div class="modal">
      <div class="modal-top">
        <h2 id="modalTitle">Film Başlığı</h2>
        <button id="closeModal" class="close-btn">Kapat</button>
      </div>
      <div id="modalMeta" style="color:#9ca3af; font-size:0.88rem; margin-bottom:12px;"></div>
      <div id="videoBox" class="video-box">Oynatıcı hazırlanıyor...</div>
      <p id="modalOverview" class="modal-overview"></p>
      <div class="modal-actions">
        <a id="extLink" class="btn-link" href="#" target="_blank" rel="noopener" style="display:none;">Kaynakta Aç</a>
      </div>
    </div>
  </div>

  <script>
    let currentCategory = "Tümü";
    let searchTimer = null;

    const grid = document.getElementById("movieGrid");
    const searchInput = document.getElementById("searchInput");
    const apiNotice = document.getElementById("apiNotice");
    const modal = document.getElementById("movieModal");
    const closeModal = document.getElementById("closeModal");
    const videoBox = document.getElementById("videoBox");
    const extLink = document.getElementById("extLink");

    async function loadMovies() {
      const q = encodeURIComponent(searchInput.value.trim());
      const cat = encodeURIComponent(currentCategory);
      grid.innerHTML = "<p style='color:#9ca3af;'>Yükleniyor...</p>";

      const res = await fetch(`/api/movies?category=${cat}&q=${q}`);
      const data = await res.json();

      apiNotice.style.display = (!data.has_api_key && currentCategory !== "Açık Arşiv") ? "block" : "none";

      if (!data.movies || data.movies.length === 0) {
        grid.innerHTML = "<p style='color:#9ca3af;'>Gösterilecek film bulunamadı.</p>";
        return;
      }

      grid.innerHTML = "";
      data.movies.forEach((m) => {
        const card = document.createElement("div");
        card.className = "card";
        let badgeHtml = "";
        if (m.category === "Vizyonda") {
          badgeHtml = `<span class="badge">VİZYONDA</span>`;
        } else if (m.category === "Açık Arşiv") {
          badgeHtml = `<span class="badge archive">AÇIK ARŞİV</span>`;
        }

        const ratingText = typeof m.rating === "number" ? `★ ${m.rating}` : m.rating;

        card.innerHTML = `
          <div class="poster-wrap">
            ${m.poster ? `<img src="${m.poster}" alt="${m.title}" loading="lazy" onerror="this.style.display='none'" />` : ""}
            ${badgeHtml}
          </div>
          <div class="card-body">
            <div class="card-title">${m.title}</div>
            <div class="card-meta">
              <span>${m.year}</span>
              <span>${ratingText}</span>
            </div>
          </div>
        `;
        card.addEventListener("click", () => openMovieModal(m));
        grid.appendChild(card);
      });
    }

    async function openMovieModal(movie) {
      document.getElementById("modalTitle").textContent = movie.title;
      const ratingText = typeof movie.rating === "number" ? `★ ${movie.rating}` : movie.rating;
      document.getElementById("modalMeta").textContent = `Yıl: ${movie.year}  •  ${ratingText}  •  ${movie.category}`;
      document.getElementById("modalOverview").textContent = movie.overview;
      videoBox.innerHTML = "Oynatıcı yükleniyor...";
      extLink.style.display = "none";
      modal.classList.add("open");

      if (movie.source === "archive" && movie.embed_url) {
        videoBox.innerHTML = `<iframe src="${movie.embed_url}" allowfullscreen></iframe>`;
        if (movie.external_url) {
          extLink.href = movie.external_url;
          extLink.textContent = "Archive.org Sayfasında Aç";
          extLink.style.display = "inline-block";
        }
      } else if (movie.source === "tmdb" && movie.tmdb_id) {
        const res = await fetch(`/api/movie/${movie.tmdb_id}/trailer`);
        const tData = await res.json();
        if (tData.embed_url) {
          videoBox.innerHTML = `<iframe src="${tData.embed_url}" allowfullscreen></iframe>`;
        } else {
          videoBox.innerHTML = "Bu film için gömülü fragman bulunamadı.";
        }
        if (tData.youtube_url) {
          extLink.href = tData.youtube_url;
          extLink.textContent = "YouTube'da Aç";
          extLink.style.display = "inline-block";
        }
      } else {
        videoBox.innerHTML = "Özel kart içeriği.";
      }
    }

    document.querySelectorAll(".tab-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        currentCategory = btn.dataset.cat;
        loadMovies();
      });
    });

    searchInput.addEventListener("input", () => {
      clearTimeout(searchTimer);
      searchTimer = setTimeout(loadMovies, 350);
    });

    closeModal.addEventListener("click", () => {
      modal.classList.remove("open");
      videoBox.innerHTML = "";
    });

    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.classList.remove("open");
        videoBox.innerHTML = "";
      }
    });

    loadMovies();
  </script>
</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
