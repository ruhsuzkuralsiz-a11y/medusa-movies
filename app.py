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
        "glow": "#ff1e2d"
    },
    {
        "id": 119051,
        "media_type": "tv",
        "title": "Wednesday",
        "category": "Popüler Diziler",
        "poster": "https://image.tmdb.org/t/p/w500/9PFonBhy4cQy7Jz20NpMygczOkv.jpg",
        "glow": "#a855f7"
    },
    {
        "id": 93405,
        "media_type": "tv",
        "title": "Squid Game",
        "category": "Gündemdekiler",
        "poster": "https://image.tmdb.org/t/p/w500/dDlEmu3EZ0Pgg93K2SVNLCjCSvE.jpg",
        "glow": "#ff2a85"
    },
    {
        "id": 71912,
        "media_type": "tv",
        "title": "The Witcher",
        "category": "Popüler Diziler",
        "poster": "https://image.tmdb.org/t/p/w500/7vjaCdMw15FEbXyLQTVa04URsPm.jpg",
        "glow": "#fbbf24"
    },
    {
        "id": 697843,
        "media_type": "movie",
        "title": "Extraction 2",
        "category": "Netflix Orijinal Filmler",
        "poster": "https://image.tmdb.org/t/p/w500/7gKI9hpEMcZuQPNgKrkDzJpbnNS.jpg",
        "glow": "#ff6a00"
    },
    {
        "id": 70523,
        "media_type": "tv",
        "title": "Dark",
        "category": "Popüler Diziler",
        "poster": "https://image.tmdb.org/t/p/w500/apbrbWs8M9lyOpJYU5WXrpFbk1Z.jpg",
        "glow": "#facc15"
    },
    {
        "id": 94605,
        "media_type": "tv",
        "title": "Arcane",
        "category": "Anime & Animasyon",
        "poster": "https://image.tmdb.org/t/p/w500/fqldf2t8ztc9aiwn3k6mlX3tvRT.jpg",
        "glow": "#00e5ff"
    },
    {
        "id": 87108,
        "media_type": "tv",
        "title": "Our Planet",
        "category": "Belgeseller",
        "poster": "https://image.tmdb.org/t/p/w500/1XgmBoiiapwFMCKkG8tYqA5qN8S.jpg",
        "glow": "#00ff88"
    },
    {
        "id": 71446,
        "media_type": "tv",
        "title": "La Casa de Papel",
        "category": "Gündemdekiler",
        "poster": "https://image.tmdb.org/t/p/w500/reEMJA1uzscCbkpeRJeTT2bjqUp.jpg",
        "glow": "#ff1744"
    },
    {
        "id": 545611,
        "media_type": "movie",
        "title": "The Gray Man",
        "category": "Netflix Orijinal Filmler",
        "poster": "https://image.tmdb.org/t/p/w500/8cXruOfGMhV8YQJaLnyN1v1meZr.jpg",
        "glow": "#2979ff"
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
        :root {
            --netflix-red: #E50914;
            --netflix-black: #09090b;
            --ambilight-color: #ff1e2d;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--netflix-black);
            color: #fff;
            font-family: Arial, sans-serif;
            padding-bottom: 75px;
            overflow-x: hidden;
        }

        .ambient-bg {
            position: fixed;
            inset: -20%;
            pointer-events: none;
            z-index: 0;
            background:
                radial-gradient(circle at 50% 25%, var(--ambilight-color) 0%, transparent 45%),
                radial-gradient(circle at 20% 70%, var(--ambilight-color) 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, var(--ambilight-color) 0%, transparent 40%);
            opacity: 0.34;
            filter: blur(55px);
            transition: background 0.5s ease, opacity 0.4s ease;
        }

        .netflix-header {
            position: fixed; top: 0; left: 0; width: 100%; height: 60px;
            background: rgba(9, 9, 11, 0.85);
            backdrop-filter: blur(12px);
            display: flex; align-items: center; justify-content: space-between;
            padding: 0 20px; z-index: 1000;
            border-bottom: 1px solid var(--ambilight-color);
            box-shadow: 0 2px 24px -4px var(--ambilight-color);
            transition: border-color 0.4s ease, box-shadow 0.4s ease;
        }
        .netflix-logo {
            color: var(--netflix-red); font-size: 22px; font-weight: bold;
            text-decoration: none; font-family: Impact, sans-serif;
            text-shadow: 0 0 20px var(--ambilight-color);
        }
        .search-icon-btn { background: none; border: none; color: #fff; font-size: 18px; cursor: pointer; }

        .search-bar-container { display: none; padding: 15px; background: rgba(9,9,11,0.96); backdrop-filter: blur(10px); position: fixed; top: 60px; left: 0; width: 100%; z-index: 999; border-bottom: 1px solid #222; }
        .search-bar-container input { width: 100%; background: #1c1c20; border: 1px solid #333; padding: 10px 15px; border-radius: 6px; color: #fff; outline: none; font-size: 14px; }

        .hero-banner {
            position: relative; width: 100%; height: 350px;
            background: url('https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg') center/cover no-repeat;
            display: flex; flex-direction: column; justify-content: flex-end;
            padding: 20px; text-align: center; margin-top: 60px; z-index: 1;
            box-shadow: 0 0 65px -5px var(--ambilight-color);
        }
        .hero-banner::after { content: ''; position: absolute; bottom: 0; left: 0; width: 100%; height: 140px; background: linear-gradient(to top, var(--netflix-black), transparent); }
        .hero-title { font-size: 26px; font-weight: bold; margin-bottom: 10px; z-index: 2; text-shadow: 0 2px 14px rgba(0,0,0,0.9); }
        .hero-btn {
            background: #fff; color: #000; border: none; padding: 10px 26px; border-radius: 6px;
            font-size: 14px; font-weight: bold; cursor: pointer; z-index: 2; margin: 0 auto;
            display: flex; align-items: center; gap: 8px;
            box-shadow: 0 0 28px var(--ambilight-color);
        }

        .netflix-categories { position: relative; z-index: 1; display: flex; gap: 10px; padding: 15px 20px; overflow-x: auto; white-space: nowrap; scrollbar-width: none; }
        .netflix-categories::-webkit-scrollbar { display: none; }
        .cat-chip { background: rgba(255,255,255,0.08); color: #fff; border: 1px solid rgba(255,255,255,0.15); padding: 6px 14px; border-radius: 20px; font-size: 12px; cursor: pointer; }
        .cat-chip.active { background: #fff; color: #000; font-weight: bold; box-shadow: 0 0 18px var(--ambilight-color); }

        .section-box { position: relative; z-index: 1; padding: 10px 20px; }
        .row-header { font-size: 15px; font-weight: bold; margin-bottom: 12px; color: #e5e5e5; }
        .movies-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
        @media(min-width: 600px) { .movies-grid { grid-template-columns: repeat(5, 1fr); } }

        .movie-card {
            background: #16161a; border-radius: 8px; overflow: hidden;
            display: flex; flex-direction: column; cursor: pointer;
            border: 2px solid transparent;
            transition: transform 0.2s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        }
        .movie-card.active-glow, .movie-card:active {
            transform: scale(1.04);
            border-color: var(--card-glow, var(--ambilight-color));
            box-shadow: 0 0 28px var(--card-glow, var(--ambilight-color));
        }
        .movie-poster { width: 100%; height: 150px; object-fit: cover; background: #1e1e24; }
        .movie-info { padding: 8px; font-size: 11px; font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

        .modal {
            display: none; position: fixed; inset: 0; width: 100vw; height: 100dvh;
            background: #050507; z-index: 2000; flex-direction: column;
        }
        .modal-header {
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(10, 10, 12, 0.95); padding: 8px 12px;
            border-bottom: 2px solid var(--ambilight-color);
            box-shadow: 0 2px 20px var(--ambilight-color);
            height: 48px; flex-shrink: 0; gap: 8px; z-index: 3;
        }
        .back-btn { background: var(--netflix-red); color: #fff; border: none; padding: 6px 12px; border-radius: 4px; font-size: 11px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 5px; white-space: nowrap; }
        .modal-title { font-size: 12px; font-weight: bold; color: #fff; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; text-align: center; }
        .amb-btn {
            background: #1a1a1f; color: #fff;
            border: 1px solid var(--ambilight-color);
            box-shadow: 0 0 15px var(--ambilight-color);
            padding: 5px 9px; border-radius: 4px; font-size: 11px; cursor: pointer; white-space: nowrap;
        }
        .amb-btn.off { border-color: #333; box-shadow: none; color: #777; }
        .fs-btn { background: #1a1a1f; color: #fff; border: 1px solid #3a3a3a; padding: 6px 9px; border-radius: 4px; font-size: 11px; cursor: pointer; display: flex; align-items: center; gap: 4px; white-space: nowrap; }

        .modal-player-wrapper {
            position: relative; flex: 1; width: 100%; height: calc(100dvh - 48px);
            background: #050507; display: flex; align-items: center; justify-content: center;
            padding: 14px; overflow: hidden;
        }
        .player-ambilight-aura {
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at center, var(--ambilight-color) 0%, transparent 68%);
            filter: blur(42px);
            opacity: 0.65;
            pointer-events: none;
            animation: breatheGlow 3.6s ease-in-out infinite alternate;
        }
        .player-ambilight-aura.hidden { opacity: 0; animation: none; }

        @keyframes breatheGlow {
            0% { transform: scale(0.94); opacity: 0.48; }
            100% { transform: scale(1.06); opacity: 0.82; }
        }

        .iframe-container {
            position: relative; z-index: 2; width: 100%; height: 100%;
            background: #000; border-radius: 10px; overflow: hidden;
            border: 2px solid var(--ambilight-color);
            box-shadow: 0 0 45px var(--ambilight-color);
        }
        .iframe-container.no-glow { box-shadow: none; border: none; border-radius: 0; }
        .iframe-container iframe { width: 100%; height: 100%; border: none; display: block; }

        .netflix-bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; height: 55px; background-color: rgba(12,12,15,0.94); backdrop-filter: blur(10px); display: flex; justify-content: space-around; align-items: center; border-top: 1px solid var(--ambilight-color); box-shadow: 0 -2px 20px -4px var(--ambilight-color); z-index: 1000; }
        .nav-link { color: #8c8c8c; text-decoration: none; font-size: 10px; display: flex; flex-direction: column; align-items: center; gap: 2px; cursor: pointer; background: none; border: none; }
        .nav-link.active { color: #fff; }
        .nav-link i { font-size: 16px; }
    </style>
</head>
<body>
    <div class="ambient-bg" id="ambientBg"></div>

    <div class="netflix-header">
        <a href="/" class="netflix-logo">MEDUSAFILM</a>
        <button class="search-icon-btn" onclick="toggleSearch()"><i class="fa-solid fa-magnifying-glass"></i></button>
    </div>

    <div class="search-bar-container" id="searchBar">
        <input type="text" id="searchInput" placeholder="Film veya dizi adı yaz..." oninput="handleSearchInput()">
    </div>

    <div class="hero-banner" id="heroBanner">
        <div class="hero-title">Stranger Things</div>
        <button class="hero-btn" onclick="openPlayer(66732, 'tv', 'Stranger Things', '#ff1e2d')"><i class="fa-solid fa-play"></i> Hemen İzle</button>
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
            <span class="modal-title" id="modalTitle">Oynatıcı</span>
            <button class="amb-btn" id="ambToggleBtn" onclick="toggleAmbilight()"><i class="fa-solid fa-lightbulb"></i> LED</button>
            <button class="fs-btn" onclick="toggleFullscreen()"><i class="fa-solid fa-expand"></i></button>
        </div>
        <div class="modal-player-wrapper" id="playerWrapper">
            <div class="player-ambilight-aura" id="playerAura"></div>
            <div class="iframe-container" id="iframeBox">
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
        const dynamicPalette = ['#ff1e2d', '#a855f7', '#00e5ff', '#00ff88', '#fbbf24', '#ff2a85', '#2979ff'];
        const FALLBACK_POSTER = "https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg";

        let currentCategory = 'Tümü';
        let searchQuery = '';
        let searchTimer = null;
        let ambilightOn = true;

        function setAmbilightColor(hexColor) {
            if (!hexColor) return;
            document.documentElement.style.setProperty('--ambilight-color', hexColor);
        }

        function getColorForId(id, preset) {
            if (preset) return preset;
            const idx = Math.abs(Number(id) || 0) % dynamicPalette.length;
            return dynamicPalette[idx];
        }

        function buildPlayerUrl(tmdbId, mediaType) {
            const typePath = mediaType === 'tv' ? 'tv' : 'movie';
            return `https://vidsrc.me/embed/${typePath}?tmdb=${tmdbId}&ds_lang=tr`;
        }

        function highlightCard(cardEl, color) {
            document.querySelectorAll('.movie-card').forEach(c => c.classList.remove('active-glow'));
            if (cardEl) cardEl.classList.add('active-glow');
            setAmbilightColor(color);
        }

        function renderCards(items, emptyMessage) {
            const grid = document.getElementById('movieGrid');
            grid.innerHTML = '';

            if (!items || items.length === 0) {
                grid.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; color: #9ca3af; padding: 30px; font-size: 13px;">${emptyMessage || 'İçerik bulunamadı.'}</div>`;
                return;
            }

            items.forEach(m => {
                const cardColor = getColorForId(m.id, m.glow);
                const posterUrl = m.poster || FALLBACK_POSTER;
                const card = document.createElement('div');
                card.className = 'movie-card';
                card.style.setProperty('--card-glow', cardColor);

                card.onmouseenter = () => highlightCard(card, cardColor);
                card.ontouchstart = () => highlightCard(card, cardColor);
                card.onclick = () => openPlayer(m.id, m.media_type || 'movie', m.title, cardColor);

                card.innerHTML = `
                    <img src="${posterUrl}" class="movie-poster" loading="lazy" onerror="this.onerror=null; this.src='${FALLBACK_POSTER}';">
                    <div class="movie-info">${m.title}</div>
                `;
                grid.appendChild(card);
            });
        }

        function renderLocal() {
            let filtered = localMovies.filter(m => {
                let matchCat = (currentCategory === 'Tümü' || m.category === currentCategory);
                let matchSearch = !searchQuery || m.title.toLowerCase().includes(searchQuery.toLowerCase());
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

            const localMatches = localMovies.filter(m => m.title.toLowerCase().includes(searchQuery.toLowerCase()));
            if (localMatches.length > 0) {
                document.getElementById('sectionTitle').innerText = `"${searchQuery}" Sonuçları`;
                renderCards(localMatches);
            } else {
                document.getElementById('sectionTitle').innerText = `"${searchQuery}" aranıyor...`;
            }

            searchTimer = setTimeout(async () => {
                try {
                    const res = await fetch(`/api/search?q=${encodeURIComponent(searchQuery)}`);
                    const data = await res.json();
                    const remote = data.results || [];
                    const combined = [...localMatches];
                    const seenIds = new Set(localMatches.map(x => String(x.id)));

                    remote.forEach(item => {
                        if (!seenIds.has(String(item.id))) {
                            seenIds.add(String(item.id));
                            combined.push(item);
                        }
                    });

                    document.getElementById('sectionTitle').innerText = `"${searchQuery}" Sonuçları (${combined.length})`;
                    renderCards(combined, `"${searchQuery}" için sonuç bulunamadı. Yazımı kontrol edip tekrar deneyebilirsin.`);
                } catch (e) {
                    if (localMatches.length === 0) {
                        renderCards([], 'Arama servisine şu an ulaşılamıyor, tekrar dene.');
                    }
                }
            }, 300);
        }

        function setCategory(cat, btn) {
            currentCategory = cat;
            document.querySelectorAll('.cat-chip').forEach(b => b.classList.remove('active'));
            if(btn) btn.classList.add('active');
            if (!searchQuery) {
                document.getElementById('sectionTitle').innerText = cat === 'Tümü' ? 'Arşivdeki İçerikler' : cat;
           
