from flask import Flask, render_template_string, request, jsonify
import requests
import json

app = Flask(__name__)

TMDB_API_KEY = "Abdea525bebc9ce403ea266dc78f3555"

CATALOG = [
    {
        "id": 66732,
        "media_type": "tv",
        "title": "Stranger Things",
        "category": "Popüler Diziler",
        "poster": "https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg",
        "overview": "Stranger Things oynatıcı ekranı."
    },
    {
        "id": 119051,
        "media_type": "tv",
        "title": "Wednesday",
        "category": "Popüler Diziler",
        "poster": "https://image.tmdb.org/t/p/w500/9PFonBhy4cQy7Jz20NpMygczOkv.jpg",
        "overview": "Wednesday oynatıcı ekranı."
    },
    {
        "id": 93405,
        "media_type": "tv",
        "title": "Squid Game",
        "category": "Gündemdekiler",
        "poster": "https://image.tmdb.org/t/p/w500/dDlEmu3EZ0Pgg93K2SVNLCjCSvE.jpg",
        "overview": "Squid Game oynatıcı ekranı."
    },
    {
        "id": 71912,
        "media_type": "tv",
        "title": "The Witcher",
        "category": "Popüler Diziler",
        "poster": "https://image.tmdb.org/t/p/w500/7vjaCdMw15FEbXyLQTVa04URsPm.jpg",
        "overview": "The Witcher oynatıcı ekranı."
    },
    {
        "id": 697843,
        "media_type": "movie",
        "title": "Extraction 2",
        "category": "Netflix Orijinal Filmler",
        "poster": "https://image.tmdb.org/t/p/w500/wkPPggLUDauAoukxuvXIPq70Ssx.jpg",
        "overview": "Extraction 2 oynatıcı ekranı."
    },
    {
        "id": 70523,
        "media_type": "tv",
        "title": "Dark",
        "category": "Popüler Diziler",
        "poster": "https://image.tmdb.org/t/p/w500/apbrbWs8M9lyOpJYU5WXrpFbk1Z.jpg",
        "overview": "Dark oynatıcı ekranı."
    },
    {
        "id": 94605,
        "media_type": "tv",
        "title": "Arcane",
        "category": "Anime & Animasyon",
        "poster": "https://image.tmdb.org/t/p/w500/fqldf2t8ztc9aiwn3k6mlX3tvRT.jpg",
        "overview": "Arcane oynatıcı ekranı."
    },
    {
        "id": 87108,
        "media_type": "tv",
        "title": "Our Planet",
        "category": "Belgeseller",
        "poster": "https://image.tmdb.org/t/p/w500/1XgmBoiiapwFMCKkG8tYqA5qN8S.jpg",
        "overview": "Our Planet oynatıcı ekranı."
    },
    {
        "id": 71446,
        "media_type": "tv",
        "title": "La Casa de Papel",
        "category": "Gündemdekiler",
        "poster": "https://image.tmdb.org/t/p/w500/reEMJA1uzscCbkpeRJeTT2bjqUp.jpg",
        "overview": "La Casa de Papel oynatıcı ekranı."
    },
    {
        "id": 545611,
        "media_type": "movie",
        "title": "The Gray Man",
        "category": "Netflix Orijinal Filmler",
        "poster": "https://image.tmdb.org/t/p/w500/8cXruOfGMhV8YQJaLnyN1v1meZr.jpg",
        "overview": "The Gray Man oynatıcı ekranı."
    }
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
        :root { --netflix-red: #E50914; --netflix-black: #141414; }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: var(--netflix-black); color: #fff; font-family: Arial, sans-serif; padding-bottom: 70px; }

        .netflix-header { position: fixed; top: 0; left: 0; width: 100%; height: 60px; background: rgba(0,0,0,0.92); display: flex; align-items: center; justify-content: space-between; padding: 0 20px; z-index: 1000; }
        .netflix-logo { color: var(--netflix-red); font-size: 22px; font-weight: bold; text-decoration: none; font-family: Impact, sans-serif; }
        .search-icon-btn { background: none; border: none; color: #fff; font-size: 18px; cursor: pointer; }

        .search-bar-container { display: none; padding: 15px; background: #000; position: fixed; top: 60px; left: 0; width: 100%; z-index: 999; border-bottom: 1px solid #222; }
        .search-bar-container input { width: 100%; background: #222; border: 1px solid #444; padding: 10px 15px; border-radius: 4px; color: #fff; outline: none; font-size: 14px; }

        .hero-banner { position: relative; width: 100%; height: 350px; background: url('https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg') center/cover no-repeat; display: flex; flex-direction: column; justify-content: flex-end; padding: 20px; text-align: center; margin-top: 60px; }
        .hero-banner::after { content: ''; position: absolute; bottom: 0; left: 0; width: 100%; height: 120px; background: linear-gradient(to top, var(--netflix-black), transparent); }
        .hero-title { font-size: 26px; font-weight: bold; margin-bottom: 10px; z-index: 2; }
        .hero-btn { background: #fff; color: #000; border: none; padding: 10px 25px; border-radius: 4px; font-size: 14px; font-weight: bold; cursor: pointer; z-index: 2; margin: 0 auto; display: flex; align-items: center; gap: 8px; }

        .netflix-categories { display: flex; gap: 10px; padding: 15px 20px; overflow-x: auto; white-space: nowrap; scrollbar-width: none; background: var(--netflix-black); }
        .netflix-categories::-webkit-scrollbar { display: none; }
        .cat-chip { background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2); padding: 6px 14px; border-radius: 20px; font-size: 12px; cursor: pointer; }
        .cat-chip.active { background: #fff; color: #000; font-weight: bold; }

        .section-box { padding: 10px 20px; }
        .row-header { font-size: 15px; font-weight: bold; margin-bottom: 10px; color: #e5e5e5; }
        .movies-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
        @media(min-width: 600px) { .movies-grid { grid-template-columns: repeat(5, 1fr); } }

        .movie-card { background: #1f1f1f; border-radius: 4px; overflow: hidden; display: flex; flex-direction: column; cursor: pointer; }
        .movie-poster { width: 100%; height: 150px; object-fit: cover; background: #222; }
        .movie-info { padding: 8px; font-size: 11px; font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

        /* Tam Ekran / Geniş Oynatıcı Katmanı */
        .modal { display: none; position: fixed; inset: 0; width: 100vw; height: 100dvh; background: #000; z-index: 2000; flex-direction: column; }
        .modal-header { display: flex; justify-content: space-between; align-items: center; background: #0b0b0b; padding: 8px 12px; border-bottom: 1px solid #1f1f1f; height: 48px; flex-shrink: 0; gap: 6px; overflow-x: auto; }
        .back-btn { background: var(--netflix-red); color: #fff; border: none; padding: 6px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 5px; white-space: nowrap; }
        .srv-btn { background: #1e1e1e; color: #ccc; border: 1px solid #333; padding: 5px 8px; border-radius: 4px; font-size: 11px; cursor: pointer; white-space: nowrap; }
        .srv-btn.active { background: #fff; color: #000; font-weight: bold; border-color: #fff; }
        .fs-btn { background: #222; color: #fff; border: 1px solid #3a3a3a; padding: 6px 8px; border-radius: 4px; font-size: 11px; cursor: pointer; display: flex; align-items: center; gap: 4px; white-space: nowrap; }
        .modal-player-wrapper { flex: 1; width: 100%; height: calc(100dvh - 48px); background: #000; }
        .iframe-container { width: 100%; height: 100%; background: #000; }
        .iframe-container iframe { width: 100%; height: 100%; border: none; display: block; }

        .netflix-bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; height: 55px; background-color: rgba(18,18,18,0.95); display: flex; justify-content: space-around; align-items: center; border-top: 1px solid #222; z-index: 1000; }
        .nav-link { color: #8c8c8c; text-decoration: none; font-size: 10px; display: flex; flex-direction: column; align-items: center; gap: 2px; cursor: pointer; background: none; border: none; }
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
        <input type="text" id="searchInput" placeholder="Tüm film ve dizilerde ara..." oninput="handleSearchInput()">
    </div>

    <div class="hero-banner">
        <div class="hero-title">Stranger Things</div>
        <button class="hero-btn" onclick="openPlayer(66732, 'tv', 'Stranger Things')"><i class="fa-solid fa-play"></i> Hemen İzle</button>
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
            <button class="srv-btn active" id="srv1Btn" onclick="switchServer(1, this)">Sunucu 1</button>
            <button class="srv-btn" id="srv2Btn" onclick="switchServer(2, this)">Sunucu 2</button>
            <button class="srv-btn" id="srv3Btn" onclick="switchServer(3, this)">Sunucu 3</button>
            <button class="fs-btn" onclick="toggleFullscreen()"><i class="fa-solid fa-expand"></i></button>
        </div>
        <div class="modal-player-wrapper">
            <div class="iframe-container">
                <iframe id="mediaFrame" src="" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true" allow="autoplay; fullscreen; encrypted-media"></iframe>
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
        let currentCategory = 'Tümü';
        let searchQuery = '';
        let remoteResults = [];
        let searchTimer = null;

        let activeMediaId = null;
        let activeMediaType = 'movie';

        function buildServerUrl(srvNum, tmdbId, mediaType) {
            const typePath = mediaType === 'tv' ? 'tv' : 'movie';
            if (srvNum === 1) {
                return `https://vidsrc.me/embed/${typePath}?tmdb=${tmdbId}&ds_lang=tr`;
            } else if (srvNum === 2) {
                return `https://vidsrc.xyz/embed/${typePath}/${tmdbId}?ds_lang=tr`;
            } else {
                return `https://embed.su/embed/${typePath}/${tmdbId}`;
            }
        }

        function renderCards(items) {
            const grid = document.getElementById('movieGrid');
            grid.innerHTML = '';

            if (!items || items.length === 0) {
                grid.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; color: #888; padding: 30px; font-size: 13px;">Sonuç bulunamadı.</div>';
                return;
            }

            items.forEach(m => {
                const card = document.createElement('div');
                card.className = 'movie-card';
                card.onclick = () => openPlayer(m.id, m.media_type || 'movie', m.title);
                card.innerHTML = `
                    <img src="${m.poster}" class="movie-poster" loading="lazy">
                    <div class="movie-info">${m.title}</div>
                `;
                grid.appendChild(card);
            });
        }

        function renderLocal() {
            let filtered = localMovies.filter(m => {
                let matchCat = (currentCategory === 'Tümü' || m.category === currentCategory);
                let matchSearch = m.title.toLowerCase().includes(searchQuery.toLowerCase());
                return matchCat && matchSearch;
            });
            renderCards(filtered);
        }

        function handleSearchInput() {
            searchQuery = document.getElementById('searchInput').value.trim();
            clearTimeout(searchTimer);

            if (!searchQuery) {
                remoteResults = [];
                document.getElementById('sectionTitle').innerText = currentCategory === 'Tümü' ? 'Arşivdeki İçerikler' : currentCategory;
                renderLocal();
                return;
            }

            document.getElementById('sectionTitle').innerText = `"${searchQuery}" için aranıyor...`;
            searchTimer = setTimeout(async () => {
                try {
                    const res = await fetch(`/api/search?q=${encodeURIComponent(searchQuery)}`);
                    const data = await res.json();
                    remoteResults = data.results || [];
                    document.getElementById('sectionTitle').innerText = `"${searchQuery}" Arama Sonuçları`;
                    renderCards(remoteResults);
                } catch (e) {
                    renderLocal();
                }
            }, 350);
        }

        function setCategory(cat, btn) {
            currentCategory = cat;
            document.querySelectorAll('.cat-chip').forEach(b => b.classList.remove('active'));
            if(btn) btn.classList.add('active');
            if (!searchQuery) {
                document.getElementById('sectionTitle').innerText = cat === 'Tümü' ? 'Arşivdeki İçerikler' : cat;
                renderLocal();
            }
        }

        function navClick(cat, btn) {
            document.querySelectorAll('.nav-link').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            document.querySelectorAll('.cat-chip').forEach(chip => {
                if(chip.innerText === cat || (cat === 'Tümü' && chip.innerText === 'Tümü')) {
                    chip.click();
                } else {
                    chip.classList.remove('active');
                }
            });
            currentCategory = cat;
            if (!searchQuery) renderLocal();
            window.scrollTo({top: 300, behavior: 'smooth'});
        }

        function toggleSearch() {
            const bar = document.getElementById('searchBar');
            bar.style.display = bar.style.display === 'block' ? 'none' : 'block';
            if(bar.style.display === 'block') document.getElementById('searchInput').focus();
        }

        function openPlayer(tmdbId, mediaType, title) {
            activeMediaId = tmdbId;
            activeMediaType = mediaType || 'movie';
            document.querySelectorAll('.srv-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('srv1Btn').classList.add('active');
            document.getElementById('mediaFrame').src = buildServerUrl(1, activeMediaId, activeMediaType);
            document.getElementById('mediaModal').style.display = 'flex';
        }

        function switchServer(srvNum, btn) {
            if (!activeMediaId) return;
            document.querySelectorAll('.srv-btn').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            document.getElementById('mediaFrame').src = buildServerUrl(srvNum, activeMediaId, activeMediaType);
        }

        function toggleFullscreen() {
            const modal = document.getElementById('mediaModal');
            const fsEl = document.fullscreenElement || document.webkitFullscreenElement;
            if (!fsEl) {
                if (modal.requestFullscreen) {
                    modal.requestFullscreen().catch(() => {});
                } else if (modal.webkitRequestFullscreen) {
                    modal.webkitRequestFullscreen();
                }
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen().catch(() => {});
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen();
                }
            }
        }

        function closeModal() {
            document.getElementById('mediaFrame').src = '';
            document.getElementById('mediaModal').style.display = 'none';
            const fsEl = document.fullscreenElement || document.webkitFullscreenElement;
            if (fsEl) {
                if (document.exitFullscreen) {
                    document.exitFullscreen().catch(() => {});
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen();
                }
            }
        }

        renderLocal();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, catalog_json=json.dumps(CATALOG, ensure_ascii=False))

@app.route('/api/search')
def api_search():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify({"results": []})

    url = "https://api.themoviedb.org/3/search/multi"
    params = {
        "api_key": TMDB_API_KEY,
        "query": q,
        "language": "tr-TR",
        "include_adult": "false"
    }

    try:
        r = requests.get(url, params=params, timeout=8)
        data = r.json()
        out = []
        for item in data.get("results", []):
            m_type = item.get("media_type")
            if m_type not in ("movie", "tv"):
                continue
            poster_path = item.get("poster_path")
            if not poster_path:
                continue
            title = item.get("title") or item.get("name") or "İsimsiz"
            out.append({
                "id": item.get("id"),
                "media_type": m_type,
                "title": title,
                "poster": f"https://image.tmdb.org/t/p/w500{poster_path}"
            })
        return jsonify({"results": out})
    except Exception:
        return jsonify({"results": []})

if __name__ == '__main__':
    app.run(debug=True)
