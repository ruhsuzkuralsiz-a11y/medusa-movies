from flask import Flask, render_template_string

app = Flask(__name__)

# Kesintisiz çalışan, doğrudan video kaynaklı Netflix Arşivi
MOVIES_DB = [
    {"id": 1, "title": "Stranger Things", "year": 2025, "rating": 8.7, "category": "Netflix Dizi", "quality": "4K", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg", "link": "https://vidsrc.me/embed/tv?imdb=tt4574334", "trailer": "https://www.youtube.com/embed/b9EkMc79ZSU", "overview": "Hawkins kasabasında gizli deneyler ve doğaüstü olaylar."},
    {"id": 2, "title": "Wednesday", "year": 2024, "rating": 8.1, "category": "Netflix Dizi", "quality": "1080p", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/9PFonBhy4cQy7Jz20NpMygczOkv.jpg", "link": "https://vidsrc.me/embed/tv?imdb=tt13443470", "trailer": "https://www.youtube.com/embed/Di310WS8nLk", "overview": "Nevermore Akademisi'nde gizemli olayları çözen Wednesday."},
    {"id": 3, "title": "Squid Game", "year": 2024, "rating": 8.0, "category": "Netflix Dizi", "quality": "4K", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/dDlEmu3EZ0Pgg93K2SVNLCjCSvE.jpg", "link": "https://vidsrc.me/embed/tv?imdb=tt10919420", "trailer": "https://www.youtube.com/embed/oqxAJKy0ii4", "overview": "Ödül için ölümcül çocuk oyunları oynayan borç içindeki insanlar."},
    {"id": 4, "title": "The Witcher", "year": 2023, "rating": 8.0, "category": "Netflix Dizi", "quality": "4K", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/7vjaCdMw15FEbXyLQTVa04URsPm.jpg", "link": "https://vidsrc.me/embed/tv?imdb=tt5180504", "trailer": "https://www.youtube.com/embed/ndl1W4ltcmg", "overview": "Rivyalı Geralt'ın canavarlarla dolu kıtasal maceraları."},
    {"id": 5, "title": "Money Heist (La Casa de Papel)", "year": 2021, "rating": 8.2, "category": "Netflix Dizi", "quality": "1080p", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/reEMJA1uzscCbkpeRJeTT2bjqUp.jpg", "link": "https://vidsrc.me/embed/tv?imdb=tt6468322", "trailer": "https://www.youtube.com/embed/ZAXA1DV4dt0", "overview": "Profesör ve ekibinin devasa soygun planı."},
    {"id": 6, "title": "Dark", "year": 2020, "rating": 8.8, "category": "Netflix Dizi", "quality": "1080p", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/apbrbWs8M9lyOpJYU5WXrpFbk1Z.jpg", "link": "https://vidsrc.me/embed/tv?imdb=tt5753856", "trailer": "https://www.youtube.com/embed/rrwycJ08PSA", "overview": "Kasabada kaybolan çocuk ve dört ailenin zaman yolculuğu."},
    {"id": 7, "title": "Extraction 2", "year": 2023, "rating": 7.1, "category": "Netflix Film", "quality": "4K", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/7gKI9hpJcZUQzwsCUO2k8k5k20j.jpg", "link": "https://vidsrc.me/embed/movie?imdb=tt12261776", "trailer": "https://www.youtube.com/embed/Y2k_CCDiwEY", "overview": "Tyler Rake'in ölümcül yeni kurtarma operasyonu."},
    {"id": 8, "title": "The Gray Man", "year": 2022, "rating": 6.5, "category": "Netflix Film", "quality": "4K", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/8cXruOfGMhV8YQJaLnyN1v1meZr.jpg", "link": "https://vidsrc.me/embed/movie?imdb=tt1649418", "trailer": "https://www.youtube.com/embed/BmllggGO4pM", "overview": "CIA ajanının dünya çapındaki nefes kesen kaosu."},
    {"id": 9, "title": "Klaus", "year": 2019, "rating": 8.2, "category": "Animasyon & Çizgi Film", "quality": "1080p", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/qayga6VIBFrhkg2u7nKkNZytAXu.jpg", "link": "https://vidsrc.me/embed/movie?imdb=tt8722346", "trailer": "https://www.youtube.com/embed/taU60Otkuuk", "overview": "Bozuk bir postacının unutulmaz Noel masalı."},
    {"id": 10, "title": "Peaky Blinders", "year": 2022, "rating": 8.8, "category": "Netflix Dizi", "quality": "1080p", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/vUUqzWa2LnHIVqtrkvlVGBI9jHW.jpg", "link": "https://vidsrc.me/embed/tv?imdb=tt2442560", "trailer": "https://www.youtube.com/embed/oVzVdvGIC7U", "overview": "Birmingham'lı suç çetesinin destansı hikayesi."},
    {"id": 11, "title": "Breaking Bad", "year": 2013, "rating": 9.5, "category": "Netflix Dizi", "quality": "4K", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg", "link": "https://vidsrc.me/embed/tv?imdb=tt0903747", "trailer": "https://www.youtube.com/embed/HhesaQXLuRY", "overview": "Kimya öğretmeninin suç dünyasına geçişi."},
    {"id": 12, "title": "The Queen's Gambit", "year": 2020, "rating": 8.5, "category": "Netflix Dizi", "quality": "1080p", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/zU0htwkhNvBQdVSIKB9s6hgVeFK.jpg", "link": "https://vidsrc.me/embed/tv?imdb=tt10048342", "trailer": "https://www.youtube.com/embed/CDHgLTNAV5A", "overview": "Yetimhanede satranç dehası olan bir kızın hikayesi."}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medusa Movies - Kesintisiz İzle</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --bg: #121212; --card: #1a1a1a; --accent: #e50914; --text: #ffffff; --muted: #aaa; --border: #2a2a2a; }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: var(--bg); color: var(--text); font-family: Arial, sans-serif; padding-bottom: 75px; }
        .header { background: #161616; padding: 12px 15px; border-bottom: 2px solid var(--accent); position: sticky; top: 0; z-index: 100; }
        .header-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .logo { color: var(--accent); font-size: 20px; font-weight: bold; text-decoration: none; }
        .search-box input { width: 100%; background: #222; border: 1px solid var(--border); padding: 8px 12px; border-radius: 20px; color: #fff; font-size: 14px; outline: none; }
        
        .filter-bar { display: flex; gap: 8px; padding: 10px 15px; background: #181818; overflow-x: auto; white-space: nowrap; scrollbar-width: none; }
        .filter-bar::-webkit-scrollbar { display: none; }
        .filter-btn { background: #222; color: var(--muted); border: none; padding: 6px 14px; border-radius: 16px; font-size: 12px; cursor: pointer; }
        .filter-btn.active { background: var(--accent); color: #fff; font-weight: bold; }

        .container { padding: 12px 15px; }
        .section-title { font-size: 14px; font-weight: bold; margin-bottom: 10px; color: #ccc; display: flex; justify-content: space-between; }
        
        .movies-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        @media(min-width: 600px) { .movies-grid { grid-template-columns: repeat(4, 1fr); } }

        .movie-card { background-color: var(--card); border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; border: 1px solid var(--border); }
        .movie-poster { width: 100%; height: 200px; object-fit: cover; background: #222; }
        .movie-info { padding: 10px; display: flex; flex-direction: column; gap: 5px; }
        .movie-name { font-size: 13px; font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .movie-meta { display: flex; justify-content: space-between; font-size: 11px; color: var(--muted); }
        .movie-rating { color: #f1c40f; font-weight: bold; }
        
        .btn-group { display: flex; gap: 5px; margin-top: 5px; }
        .btn { flex: 1; text-align: center; padding: 6px 0; border-radius: 4px; font-size: 11px; font-weight: bold; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 3px; cursor: pointer; border: none; }
        .watch-btn { background-color: var(--accent); color: white; }
        .trailer-btn { background-color: #333; color: #ddd; }

        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.92); justify-content: center; align-items: center; z-index: 1000; padding: 10px; }
        .modal-content { width: 100%; max-width: 700px; position: relative; background: #161616; border-radius: 8px; overflow: hidden; border: 1px solid var(--border); }
        .close-btn { position: absolute; top: -35px; right: 0; color: #fff; font-size: 24px; cursor: pointer; background: none; border: none; }
        .iframe-container { position: relative; width: 100%; padding-bottom: 56.25%; height: 0; background: #000; }
        .iframe-container iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; }
        .modal-details { padding: 12px; font-size: 12px; color: var(--muted); }

        .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #161616; display: flex; justify-content: space-around; padding: 10px 0; border-top: 1px solid var(--border); z-index: 999; }
        .nav-item { color: var(--muted); text-decoration: none; font-size: 11px; display: flex; flex-direction: column; align-items: center; gap: 3px; }
        .nav-item.active { color: #fff; }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-top">
            <a href="/" class="logo">🔥 medusafilm (Kesintisiz)</a>
        </div>
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Film veya dizi ara..." oninput="filterMovies()">
        </div>
    </div>

    <div class="filter-bar">
        <button class="filter-btn active" onclick="setCategory('Tümü', this)">Tümü</button>
        <button class="filter-btn" onclick="setCategory('Netflix Dizi', this)">Netflix Dizileri</button>
        <button class="filter-btn" onclick="setCategory('Netflix Film', this)">Netflix Filmleri</button>
        <button class="filter-btn" onclick="setCategory('Animasyon & Çizgi Film', this)">Animasyon</button>
    </div>

    <div class="container">
        <div class="section-title">
            <span id="sectionTitle">Tüm İçerikler (Aktif İzle)</span>
            <span id="countText" style="color:var(--accent);">0 içerik</span>
        </div>
        <div class="movies-grid" id="movieGrid"></div>
    </div>

    <!-- Oynatıcı / Fragman Modalı -->
    <div id="mediaModal" class="modal">
        <div class="modal-content">
            <button class="close-btn" onclick="closeModal()">&times;</button>
            <div class="iframe-container">
                <iframe id="mediaFrame" src="" allowfullscreen allow="autoplay"></iframe>
            </div>
            <div class="modal-details" id="modalDesc"></div>
        </div>
    </div>

    <div class="bottom-nav">
        <a href="/" class="nav-item active"><span>🏠</span> Anasayfa</a>
        <a href="/" class="nav-item"><span>📺</span> Diziler</a>
        <a href="/" class="nav-item"><span>🎬</span> Filmler</a>
        <a href="/" class="nav-item"><span>✨</span> Keşfet</a>
    </div>

    <script>
        const allMovies = {{ full_json | safe }};
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

            document.getElementById('countText').innerText = filtered.length + ' içerik';
            
            filtered.forEach(m => {
                const card = document.createElement('div');
                card.className = 'movie-card';
                card.innerHTML = `
                    <img src="${m.poster}" class="movie-poster" loading="lazy">
                    <div class="movie-info">
                        <div class="movie-name" title="${m.title}">${m.title}</div>
                        <div class="movie-meta">
                            <span class="movie-rating">⭐ ${m.rating}</span>
                            <span style="color:#e50914; font-weight:bold;">${m.lang}</span>
                        </div>
                        <div class="btn-group">
                            <button class="btn watch-btn" onclick='openPlayer("${m.link}", "${m.overview}")'><i class="fa-solid fa-play"></i> Türkçe İzle</button>
                            <button class="btn trailer-btn" onclick='openPlayer("${m.trailer}", "${m.overview}")'><i class="fa-brands fa-youtube" style="color:#ff0000;"></i> Fragman</button>
                        </div>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        function setCategory(cat, btn) {
            currentCategory = cat;
            document.querySelectorAll('.filter-btn.active').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('sectionTitle').innerText = cat === 'Tümü' ? 'Tüm İçerikler (Aktif İzle)' : cat + ' Arşivi';
            render();
        }

        function filterMovies() {
            searchQuery = document.getElementById('searchInput').value;
            render();
        }

        function openPlayer(url, desc) {
            document.getElementById('mediaFrame').src = url;
            document.getElementById('modalDesc').innerText = desc;
            document.getElementById('mediaModal').style.display = 'flex';
        }

        function closeModal() {
            document.getElementById('mediaFrame').src = '';
            document.getElementById('mediaModal').style.display = 'none';
        }

        render();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    import json
    return render_template_string(HTML_TEMPLATE, full_json=json.dumps(MOVIES_DB))

if __name__ == '__main__':
    app.run(debug=True)
