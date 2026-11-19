from flask import Flask, render_template_string
import json

app = Flask(__name__)

CATALOG = [
    {
        "id": 1,
        "title": "Stranger Things",
        "year": 2024,
        "rating": "9.1",
        "category": "Popüler Diziler",
        "poster": "https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg",
        "link": "https://vidsrc.me/embed/tv?tmdb=66732&ds_lang=tr",
        "overview": "Stranger Things oynatıcı ekranı."
    },
    {
        "id": 2,
        "title": "Wednesday",
        "year": 2024,
        "rating": "8.9",
        "category": "Popüler Diziler",
        "poster": "https://image.tmdb.org/t/p/w500/9PFonBhy4cQy7Jz20NpMygczOkv.jpg",
        "link": "https://vidsrc.me/embed/tv?tmdb=119051&ds_lang=tr",
        "overview": "Wednesday oynatıcı ekranı."
    },
    {
        "id": 3,
        "title": "Squid Game",
        "year": 2024,
        "rating": "8.7",
        "category": "Gündemdekiler",
        "poster": "https://image.tmdb.org/t/p/w500/dDlEmu3EZ0Pgg93K2SVNLCjCSvE.jpg",
        "link": "https://vidsrc.me/embed/tv?tmdb=93405&ds_lang=tr",
        "overview": "Squid Game oynatıcı ekranı."
    },
    {
        "id": 4,
        "title": "The Witcher",
        "year": 2024,
        "rating": "8.6",
        "category": "Popüler Diziler",
        "poster": "https://image.tmdb.org/t/p/w500/7vjaCdMw15FEbXyLQTVa04URsPm.jpg",
        "link": "https://vidsrc.me/embed/tv?tmdb=71912&ds_lang=tr",
        "overview": "The Witcher oynatıcı ekranı."
    },
    {
        "id": 5,
        "title": "Extraction 2",
        "year": 2023,
        "rating": "8.4",
        "category": "Netflix Orijinal Filmler",
        "poster": "https://image.tmdb.org/t/p/w500/wkPPggLUDauAoukxuvXIPq70Ssx.jpg",
        "link": "https://vidsrc.me/embed/movie?tmdb=697843&ds_lang=tr",
        "overview": "Extraction 2 oynatıcı ekranı."
    },
    {
        "id": 6,
        "title": "Dark",
        "year": 2020,
        "rating": "9.2",
        "category": "Popüler Diziler",
        "poster": "https://image.tmdb.org/t/p/w500/apbrbWs8M9lyOpJYU5WXrpFbk1Z.jpg",
        "link": "https://vidsrc.me/embed/tv?tmdb=70523&ds_lang=tr",
        "overview": "Dark oynatıcı ekranı."
    },
    {
        "id": 7,
        "title": "Arcane",
        "year": 2021,
        "rating": "9.4",
        "category": "Anime & Animasyon",
        "poster": "https://image.tmdb.org/t/p/w500/fqldf2t8ztc9aiwn3k6mlX3tvRT.jpg",
        "link": "https://vidsrc.me/embed/tv?tmdb=94605&ds_lang=tr",
        "overview": "Arcane oynatıcı ekranı."
    },
    {
        "id": 8,
        "title": "Our Planet",
        "year": 2019,
        "rating": "9.3",
        "category": "Belgeseller",
        "poster": "https://image.tmdb.org/t/p/w500/1XgmBoiiapwFMCKkG8tYqA5qN8S.jpg",
        "link": "https://vidsrc.me/embed/tv?tmdb=87108&ds_lang=tr",
        "overview": "Our Planet oynatıcı ekranı."
    },
    {
        "id": 9,
        "title": "La Casa de Papel",
        "year": 2021,
        "rating": "8.8",
        "category": "Gündemdekiler",
        "poster": "https://image.tmdb.org/t/p/w500/reEMJA1uzscCbkpeRJeTT2bjqUp.jpg",
        "link": "https://vidsrc.me/embed/tv?tmdb=71446&ds_lang=tr",
        "overview": "La Casa de Papel oynatıcı ekranı."
    },
    {
        "id": 10,
        "title": "The Gray Man",
        "year": 2022,
        "rating": "8.0",
        "category": "Netflix Orijinal Filmler",
        "poster": "https://image.tmdb.org/t/p/w500/8cXruOfGMhV8YQJaLnyN1v1meZr.jpg",
        "link": "https://vidsrc.me/embed/movie?tmdb=545611&ds_lang=tr",
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
        .modal-header { display: flex; justify-content: space-between; align-items: center; background: #0b0b0b; padding: 8px 12px; border-bottom: 1px solid #1f1f1f; height: 46px; flex-shrink: 0; gap: 8px; }
        .back-btn { background: var(--netflix-red); color: #fff; border: none; padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 6px; }
        .fs-btn { background: #222; color: #fff; border: 1px solid #3a3a3a; padding: 6px 10px; border-radius: 4px; font-size: 12px; cursor: pointer; display: flex; align-items: center; gap: 5px; }
        .modal-player-wrapper { flex: 1; width: 100%; height: calc(100dvh - 46px); background: #000; }
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
        <input type="text" id="searchInput" placeholder="Film veya dizi ara..." oninput="filterCatalog()">
    </div>

    <div class="hero-banner">
        <div class="hero-title">Stranger Things</div>
        <button class="hero-btn" onclick="openPlayer('https://vidsrc.me/embed/tv?tmdb=66732&ds_lang=tr', 'Stranger Things')"><i class="fa-solid fa-play"></i> Hemen İzle</button>
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
            <span style="font-size: 12px; color: #fff; font-weight: bold; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; text-align: center;" id="modalTitle">Oynatıcı</span>
            <button class="fs-btn" onclick="toggleFullscreen()"><i class="fa-solid fa-expand"></i> Tam Ekran</button>
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
        const allMovies = {{ catalog_json | safe }};
        let currentCategory = 'Tümü';
        let searchQuery = '';

        function render() {
            const grid = document.getElementById('movieGrid');
            grid.innerHTML = '';

            let filtered = allMovies.filter(m => {
                let matchCat = (currentCategory === 'Tümü' || m.category === currentCategory);
                let matchSearch = m.title.toLowerCase().includes(searchQuery.toLowerCase());
                return matchCat && matchSearch;
            });

            if(filtered.length === 0) {
                grid.innerHTML = '<div style="grid-column: span 5; text-align: center; color: #888; padding: 30px; font-size: 13px;">Aradığın içerik bulunamadı.</div>';
                return;
            }

            filtered.forEach(m => {
                const card = document.createElement('div');
                card.className = 'movie-card';
                card.onclick = () => openPlayer(m.link, m.title);
                card.innerHTML = `
                    <img src="${m.poster}" class="movie-poster" loading="lazy">
                    <div class="movie-info">${m.title}</div>
                `;
                grid.appendChild(card);
            });
        }

        function setCategory(cat, btn) {
            currentCategory = cat;
            document.querySelectorAll('.cat-chip').forEach(b => b.classList.remove('active'));
            if(btn) btn.classList.add('active');
            document.getElementById('sectionTitle').innerText = cat === 'Tümü' ? 'Arşivdeki İçerikler' : cat;
            render();
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
            render();
            window.scrollTo({top: 300, behavior: 'smooth'});
        }

        function toggleSearch() {
            const bar = document.getElementById('searchBar');
            bar.style.display = bar.style.display === 'block' ? 'none' : 'block';
            if(bar.style.display === 'block') document.getElementById('searchInput').focus();
        }

        function filterCatalog() {
            searchQuery = document.getElementById('searchInput').value;
            render();
        }

        function openPlayer(url, title) {
            document.getElementById('mediaFrame').src = url;
            document.getElementById('modalTitle').innerText = title;
            document.getElementById('mediaModal').style.display = 'flex';
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

        render();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, catalog_json=json.dumps(CATALOG, ensure_ascii=False))

if __name__ == '__main__':
    app.run(debug=True)
