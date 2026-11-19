import os
import json
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")

# Her içeriğin "dub_url" alanına Türkçe dublajlı video (.mp4 / .m3u8) veya embed linkini yazabilirsin.
CATALOG = [
    {"id": 27205, "media_type": "movie", "title": "Inception", "category": "Netflix Orijinal Filmler", "poster": "https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg", "glow": "#00e5ff", "dub_url": ""},
    {"id": 66732, "media_type": "tv", "title": "Stranger Things", "category": "Popüler Diziler", "poster": "https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg", "glow": "#ff1e2d", "dub_url": ""},
    {"id": 119051, "media_type": "tv", "title": "Wednesday", "category": "Popüler Diziler", "poster": "https://image.tmdb.org/t/p/w500/9PFonBhy4cQy7Jz20NpMygczOkv.jpg", "glow": "#a855f7", "dub_url": ""},
    {"id": 93405, "media_type": "tv", "title": "Squid Game", "category": "Gündemdekiler", "poster": "https://image.tmdb.org/t/p/w500/dDlEmu3EZ0Pgg93K2SVNLCjCSvE.jpg", "glow": "#ff2a85", "dub_url": ""},
    {"id": 71912, "media_type": "tv", "title": "The Witcher", "category": "Popüler Diziler", "poster": "https://image.tmdb.org/t/p/w500/7vjaCdMw15FEbXyLQTVa04URsPm.jpg", "glow": "#fbbf24", "dub_url": ""},
    {"id": 697843, "media_type": "movie", "title": "Extraction 2", "category": "Netflix Orijinal Filmler", "poster": "https://image.tmdb.org/t/p/w500/7gKI9hpEMcZuQPNgKrkDzJpbnNS.jpg", "glow": "#ff6a00", "dub_url": ""},
    {"id": 70523, "media_type": "tv", "title": "Dark", "category": "Popüler Diziler", "poster": "https://image.tmdb.org/t/p/w500/apbrbWs8M9lyOpJYU5WXrpFbk1Z.jpg", "glow": "#facc15", "dub_url": ""},
    {"id": 94605, "media_type": "tv", "title": "Arcane", "category": "Anime & Animasyon", "poster": "https://image.tmdb.org/t/p/w500/fqldf2t8ztc9aiwn3k6mlX3tvRT.jpg", "glow": "#00e5ff", "dub_url": ""},
    {"id": 87108, "media_type": "tv", "title": "Our Planet", "category": "Belgeseller", "poster": "https://image.tmdb.org/t/p/w500/1XgmBoiiapwFMCKkG8tYqA5qN8S.jpg", "glow": "#00ff88", "dub_url": ""},
    {"id": 71446, "media_type": "tv", "title": "La Casa de Papel", "category": "Gündemdekiler", "poster": "https://image.tmdb.org/t/p/w500/reEMJA1uzscCbkpeRJeTT2bjqUp.jpg", "glow": "#ff1744", "dub_url": ""},
    {"id": 545611, "media_type": "movie", "title": "The Gray Man", "category": "Netflix Orijinal Filmler", "poster": "https://image.tmdb.org/t/p/w500/8cXruOfGMhV8YQJaLnyN1v1meZr.jpg", "glow": "#2979ff", "dub_url": ""},
    {"id": 157336, "media_type": "movie", "title": "Interstellar", "category": "Netflix Orijinal Filmler", "poster": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg", "glow": "#3b82f6", "dub_url": ""}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>medusafilm</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --netflix-red: #E50914; --netflix-black: #09090b; --ambilight-color: #ff1e2d; }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: var(--netflix-black); color: #fff; font-family: Arial, sans-serif; padding-bottom: 75px; overflow-x: hidden; }
        .netflix-header { position: fixed; top: 0; left: 0; width: 100%; height: 60px; background: rgba(9, 9, 11, 0.9); display: flex; align-items: center; justify-content: space-between; padding: 0 20px; z-index: 1000; border-bottom: 1px solid var(--ambilight-color); }
        .netflix-logo { color: var(--netflix-red); font-size: 22px; font-weight: bold; text-decoration: none; font-family: Impact, sans-serif; }
        .search-icon-btn { background: none; border: none; color: #fff; font-size: 18px; cursor: pointer; }
        .search-bar-container { display: none; padding: 15px; background: rgba(9,9,11,0.96); position: fixed; top: 60px; left: 0; width: 100%; z-index: 999; border-bottom: 1px solid #222; }
        .search-bar-container input { width: 100%; background: #1c1c20; border: 1px solid #333; padding: 10px 15px; border-radius: 6px; color: #fff; outline: none; font-size: 14px; }
        .hero-banner { position: relative; width: 100%; height: 320px; background: url('https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg') center/cover no-repeat; display: flex; flex-direction: column; justify-content: flex-end; padding: 20px; text-align: center; margin-top: 60px; }
        .hero-title { font-size: 26px; font-weight: bold; margin-bottom: 10px; z-index: 2; }
        .hero-btn { background: #fff; color: #000; border: none; padding: 10px 26px; border-radius: 6px; font-size: 14px; font-weight: bold; cursor: pointer; z-index: 2; margin: 0 auto; display: flex; align-items: center; gap: 8px; }
        .netflix-categories { display: flex; gap: 10px; padding: 15px 20px; overflow-x: auto; white-space: nowrap; }
        .cat-chip { background: rgba(255,255,255,0.08); color: #fff; border: 1px solid rgba(255,255,255,0.15); padding: 6px 14px; border-radius: 20px; font-size: 12px; cursor: pointer; }
        .cat-chip.active { background: #fff; color: #000; font-weight: bold; }
        .section-box { padding: 10px 20px; }
        .row-header { font-size: 15px; font-weight: bold; margin-bottom: 12px; color: #e5e5e5; }
        .movies-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
        @media(min-width: 600px) { .movies-grid { grid-template-columns: repeat(5, 1fr); } }
        .movie-card { background: #16161a; border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; cursor: pointer; }
        .movie-poster { width: 100%; height: 150px; object-fit: cover; background: #1e1e24; display: block; }
        .poster-fallback { width: 100%; height: 150px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 10px; text-align: center; background: linear-gradient(155deg, #1e1e28, #0b0b0e); border-bottom: 2px solid var(--card-glow, #E50914); }
        .poster-fallback svg { width: 28px; height: 28px; margin-bottom: 6px; color: var(--card-glow, #E50914); }
        .poster-fallback span { font-size: 11px; font-weight: bold; color: #f3f4f6; line-height: 1.25; }
        .movie-info { padding: 8px; font-size: 11px; font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .modal { display: none; position: fixed; inset: 0; width: 100vw; height: 100dvh; background: #050507; z-index: 2000; flex-direction: column; }
        .modal-header { display: flex; justify-content: space-between; align-items: center; background: #0a0a0c; padding: 8px 12px; height: 48px; gap: 8px; }
        .back-btn { background: var(--netflix-red); color: #fff; border: none; padding: 6px 12px; border-radius: 4px; font-size: 11px; font-weight: bold; cursor: pointer; }
        .dub-badge { background: #16a34a; color: #fff; padding: 5px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; }
        .modal-player-wrapper { position: relative; flex: 1; width: 100%; height: calc(100dvh - 48px); background: #050507; display: flex; align-items: center; justify-content: center; }
        .modal-player-wrapper iframe, .modal-player-wrapper video { width: 100%; height: 100%; border: none; display: none; background: #000; }
        .empty-dub-box { display: none; text-align: center; padding: 24px; color: #d1d5db; font-size: 13px; max-width: 360px; line-height: 1.5; }
        .netflix-bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; height: 55px; background: rgba(12,12,15,0.94); display: flex; justify-content: space-around; align-items: center; border-top: 1px solid var(--ambilight-color); z-index: 1000; }
        .nav-link { color: #8c8c8c; font-size: 10px; display: flex; flex-direction: column; align-items: center; gap: 2px; cursor: pointer; background: none; border: none; }
        .nav-link.active { color: #fff; }
        .nav-link i { font-size: 16px; }
    </style>
</head>
<body>
    <div class="netflix-header">
        <a href="/" class="netflix-logo">MEDUSAFILM</a>
        <button class="search-icon-btn" onclick="toggleSearch()"><i class="fa-solid fa-magnifying-glass"></i></button>
    </div>

    <div class="search-bar-container" id="searchBar">
        <input type="text" id="searchInput" placeholder="Film veya dizi adı yaz..." oninput="handleSearchInput()">
    </div>

    <div class="hero-banner">
        <div class="hero-title">Stranger Things</div>
        <button class="hero-btn" onclick="openDubPlayer(66732, 'Stranger Things')"><i class="fa-solid fa-play"></i> Türkçe Dublaj İzle</button>
    </div>

    <div class="netflix-categories">
        <button class="cat-chip active" onclick="setCategory('Tümü', this)">Tümü</button>
        <button class="cat-chip" onclick="setCategory('Popüler Diziler', this)">Popüler Diziler</button>
        <button class="cat-chip" onclick="setCategory('Netflix Orijinal Filmler', this)">Filmler</button>
        <button class="cat-chip" onclick="setCategory('Gündemdekiler', this)">Gündemdekiler</button>
        <button class="cat-chip" onclick="setCategory('Belgeseller', this)">Belgeseller</button>
        <button class="cat-chip" onclick="setCategory('Anime & Animasyon', this)">Anime</button>
    </div>

    <div class="section-box">
        <div class="row-header" id="sectionTitle">Arşivdeki İçerikler</div>
        <div class="movies-grid" id="movieGrid"></div>
    </div>

    <div id="mediaModal" class="modal">
        <div class="modal-header">
            <button class="back-btn" onclick="closeModal()"><i class="fa-solid fa-arrow-left"></i> Geri</button>
            <span class="dub-badge" id="modalTitleBadge"><i class="fa-solid fa-volume-high"></i> Türkçe Dublaj</span>
        </div>
        <div class="modal-player-wrapper">
            <video id="dubVideo" controls autoplay playsinline></video>
            <iframe id="dubFrame" src="" allowfullscreen="true" allow="autoplay; fullscreen; encrypted-media"></iframe>
            <div id="emptyDubBox" class="empty-dub-box">
                <i class="fa-solid fa-circle-info" style="font-size: 26px; color: #E50914; margin-bottom: 10px;"></i><br>
                Bu içerik için henüz <strong>Türkçe dublaj</strong> kaynağı eklenmemiş. Katalogdaki <code>dub_url</code> alanına Türkçe dublajlı video veya oynatıcı linkini ekleyince burada çalar.
            </div>
        </div>
    </div>

    <div class="netflix-bottom-nav">
        <button class="nav-link active" onclick="navClick('Tümü', this)"><i class="fa-solid fa-house"></i><span>Ana Sayfa</span></button>
        <button class="nav-link" onclick="navClick('Popüler Diziler', this)"><i class="fa-solid fa-fire"></i><span>Popüler</span></button>
        <button class="nav-link" onclick="toggleSearch()"><i class="fa-solid fa-magnifying-glass"></i><span>Ara</span></button>
        <button class="nav-link" onclick="navClick('Anime & Animasyon', this)"><i class="fa-solid fa-bars"></i><span>Anime</span></button>
    </div>

    <script>
        const localMovies = {{ catalog_json | safe }};
        const SVG_FILM_ICON = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="2"/><line x1="7" y1="4" x2="7" y2="20"/><line x1="17" y1="4" x2="17" y2="20"/><line x1="3" y1="12" x2="21" y2="12"/></svg>`;

        let currentCategory = 'Tümü';
        let searchQuery = '';
        let searchTimer = null;

        function normalizeText(str) {
            return String(str || '').toLowerCase()
                .replace(/ı/g, 'i').replace(/İ/g, 'i').replace(/ğ/g, 'g')
                .replace(/ü/g, 'u').replace(/ş/g, 's').replace(/ö/g, 'o').replace(/ç/g, 'c').trim();
        }

        function createFallbackBox(titleText) {
            const div = document.createElement('div');
            div.className = 'poster-fallback';
            div.innerHTML = `${SVG_FILM_ICON}<span>${titleText}</span>`;
            return div;
        }

        function showCardFallback(imgEl) {
            if (!imgEl || !imgEl.parentElement) return;
            const titleEl = imgEl.parentElement.querySelector('.movie-info');
            imgEl.replaceWith(createFallbackBox(titleEl ? titleEl.textContent : 'İçerik'));
        }

        function renderCards(items, emptyMessage) {
            const grid = document.getElementById('movieGrid');
            grid.innerHTML = '';
            if (!items || items.length === 0) {
                grid.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; color: #9ca3af; padding: 30px; font-size: 13px;">${emptyMessage || 'İçerik bulunamadı.'}</div>`;
                return;
            }
            items.forEach(m => {
                const safeTitle = String(m.title || 'İçerik').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                const card = document.createElement('div');
                card.className = 'movie-card';
                card.style.setProperty('--card-glow', m.glow || '#E50914');
                card.onclick = () => openDubPlayer(m.id, m.title, m.dub_url || '');

                const infoDiv = document.createElement('div');
                infoDiv.className = 'movie-info';
                infoDiv.textContent = m.title || 'İçerik';

                if (m.poster) {
                    const img = document.createElement('img');
                    img.src = m.poster;
                    img.className = 'movie-poster';
                    img.loading = 'lazy';
                    img.onerror = function() { showCardFallback(this); };
                    card.appendChild(img);
                } else {
                    card.appendChild(createFallbackBox(safeTitle));
                }

                card.appendChild(infoDiv);
                grid.appendChild(card);
            });
        }

        function renderLocal() {
            const normQuery = normalizeText(searchQuery);
            const filtered = localMovies.filter(m => {
                const matchCat = (currentCategory === 'Tümü' || m.category === currentCategory);
                const matchSearch = !normQuery || normalizeText(m.title).includes(normQuery);
                return matchCat && matchSearch;
            });
            renderCards(filtered, 'Katalogda eşleşen içerik bulunamadı.');
        }

        function handleSearchInput() {
            searchQuery = document.getElementById('searchInput').value.trim();
            clearTimeout(searchTimer);

            if (!searchQuery) {
                document.getElementById('sectionTitle').innerText = currentCategory === 'Tümü' ? 'Arşivdeki İçerikler' : currentCategory;
                renderLocal();
                return;
            }

            const normQuery = normalizeText(searchQuery);
            const localMatches = localMovies.filter(m => normalizeText(m.title).includes(normQuery));
            document.getElementById('sectionTitle').innerText = `"${searchQuery}" Sonuçları`;
            renderCards(localMatches, `"${searchQuery}" için sonuç aranıyor...`);

            searchTimer = setTimeout(async () => {
                try {
                    const res = await fetch(`/api/search?q=${encodeURIComponent(searchQuery)}`);
                    if (!res.ok) return;
                    const data = await res.json();
                    const remote = Array.isArray(data.results) ? data.results : [];
                    const combined = [...localMatches];
                    const seenIds = new Set(localMatches.map(x => String(x.id)));
                    remote.forEach(item => {
                        if (item && item.id && !seenIds.has(String(item.id))) {
                            seenIds.add(String(item.id));
                            combined.push({ ...item, dub_url: '' });
                        }
                    });
                    document.getElementById('sectionTitle').innerText = `"${searchQuery}" Sonuçları (${combined.length})`;
                    renderCards(combined, `"${searchQuery}" için sonuç bulunamadı.`);
                } catch (e) {}
            }, 250);
        }

        function setCategory(cat, btn) {
            currentCategory = cat;
            document.querySelectorAll('.cat-chip').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            if (!searchQuery) {
                document.getElementById('sectionTitle').innerText = cat === 'Tümü' ? 'Arşivdeki İçerikler' : cat;
                renderLocal();
            }
        }

        function navClick(cat, btn) {
            document.querySelectorAll('.nav-link').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentCategory = cat;
            if (!searchQuery) renderLocal();
            window.scrollTo({top: 280, behavior: 'smooth'});
        }

        function toggleSearch() {
            const bar = document.getElementById('searchBar');
            bar.style.display = bar.style.display === 'block' ? 'none' : 'block';
            if (bar.style.display === 'block') document.getElementById('searchInput').focus();
        }

        function openDubPlayer(tmdbId, title, explicitDubUrl) {
            const found = localMovies.find(x => String(x.id) === String(tmdbId));
            const dubUrl = (explicitDubUrl || (found && found.dub_url) || '').trim();

            const videoEl = document.getElementById('dubVideo');
            const frameEl = document.getElementById('dubFrame');
            const emptyBox = document.getElementById('emptyDubBox');
            const badgeEl = document.getElementById('modalTitleBadge');

            badgeEl.innerHTML = `<i class="fa-solid fa-volume-high"></i> ${title || 'İçerik'} — Türkçe Dublaj`;
            document.getElementById('mediaModal').style.display = 'flex';

            videoEl.pause();
            videoEl.removeAttribute('src');
            videoEl.style.display = 'none';
            frameEl.src = '';
            frameEl.style.display = 'none';
            emptyBox.style.display = 'none';

            if (!dubUrl) {
                emptyBox.style.display = 'block';
                return;
            }

            if (/\.mp4($|\?)/i.test(dubUrl)) {
                videoEl.src = dubUrl;
                videoEl.style.display = 'block';
                videoEl.play().catch(() => {});
            } else {
                frameEl.src = dubUrl;
                frameEl.style.display = 'block';
            }
        }

        function closeModal() {
            const videoEl = document.getElementById('dubVideo');
            const frameEl = document.getElementById('dubFrame');
            videoEl.pause();
            videoEl.removeAttribute('src');
            videoEl.style.display = 'none';
            frameEl.src = '';
            frameEl.style.display = 'none';
            document.getElementById('emptyDubBox').style.display = 'none';
            document.getElementById('mediaModal').style.display = 'none';
        }

        renderLocal();
    </script>
</body>
</html>
"""

@app.route('/')
@app.route('/v2')
def index():
    return render_template_string(HTML_TEMPLATE, catalog_json=json.dumps(CATALOG, ensure_ascii=False))

@app.route('/api/search')
def api_search():
    q = request.args.get('q', '').strip()
    if not q or not TMDB_API_KEY:
        return jsonify({"results": []})

    try:
        r = requests.get(
            "https://api.themoviedb.org/3/search/multi",
            params={"api_key": TMDB_API_KEY, "query": q, "language": "tr-TR", "include_adult": "false"},
            timeout=6
        )
        r.raise_for_status()
        data = r.json()
        out = []
        for item in data.get("results", []):
            m_type = item.get("media_type")
            if m_type not in ("movi
