from flask import Flask, render_template_string

app = Flask(__name__)

MOVIES_DB = [
    {"id": 1, "title": "Stranger Things", "year": 2025, "rating": 8.7, "category": "Netflix Dizi", "quality": "4K", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg", "link": "https://vidsrc.me/embed/tv?imdb=tt4574334&language=tr", "trailer": "https://www.youtube.com/embed/b9EkMc79ZSU", "overview": "Hawkins kasabasında gizli deneyler ve doğaüstü olaylar."},
    {"id": 2, "title": "Wednesday", "year": 2024, "rating": 8.1, "category": "Netflix Dizi", "quality": "1080p", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/9PFonBhy4cQy7Jz20NpMygczOkv.jpg", "link": "https://vidsrc.me/embed/tv?imdb=tt13443470&language=tr", "trailer": "https://www.youtube.com/embed/Di310WS8nLk", "overview": "Nevermore Akademisi'nde gizemli olayları çözen Wednesday."},
    {"id": 3, "title": "Squid Game", "year": 2024, "rating": 8.0, "category": "Netflix Dizi", "quality": "4K", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/dDlEmu3EZ0Pgg93K2SVNLCjCSvE.jpg", "link": "https://vidsrc.me/embed/tv?imdb=tt10919420&language=tr", "trailer": "https://www.youtube.com/embed/oqxAJKy0ii4", "overview": "Ödül için ölümcül çocuk oyunları oynayan borç içindeki insanlar."},
    {"id": 4, "title": "The Witcher", "year": 2023, "rating": 8.0, "category": "Netflix Dizi", "quality": "4K", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/7vjaCdMw15FEbXyLQTVa04URsPm.jpg", "link": "https://vidsrc.me/embed/tv?imdb=tt5180504&language=tr", "trailer": "https://www.youtube.com/embed/ndl1W4ltcmg", "overview": "Rivyalı Geralt'ın canavarlarla dolu kıtasal maceraları."},
    {"id": 5, "title": "Money Heist (La Casa de Papel)", "year": 2021, "rating": 8.2, "category": "Netflix Dizi", "quality": "1080p", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/reEMJA1uzscCbkpeRJeTT2bjqUp.jpg", "link": "https://vidsrc.me/embed/tv?imdb=tt6468322&language=tr", "trailer": "https://www.youtube.com/embed/ZAXA1DV4dt0", "overview": "Profesör ve ekibinin devasa soygun planı."},
    {"id": 6, "title": "Dark", "year": 2020, "rating": 8.8, "category": "Netflix Dizi", "quality": "1080p", "lang": "Türkçe Dublaj", "poster": "https://image.tmdb.org/t/p/w500/apbrbWs8M9lyOpJYU5WXrpFbk1Z.jpg", "link": "https://vidsrc.me/embed/tv?imdb=tt5753856&language=tr", "trailer": "https://www.youtube.com/embed/rrwycJ08PSA", "overview": "Kasabada kaybolan çocuk ve dört ailenin zaman yolculuğu."}
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
        :root { --bg: #121212; --card: #1a1a1a; --accent: #e50914; --text: #ffffff; --muted: #aaa; --border: #2a2a2a; }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: var(--bg); color: var(--text); font-family: Arial, sans-serif; padding-bottom: 75px; }
        
        .header { background: #161616; padding: 12px 15px; border-bottom: 2px solid var(--accent); position: sticky; top: 0; z-index: 100; display: flex; align-items: center; justify-content: space-between; }
        .logo { color: var(--accent); font-size: 20px; font-weight: bold; text-decoration: none; display: flex; align-items: center; gap: 8px; }
        
        .search-container { padding: 10px 15px; background: #181818; }
        .search-box input { width: 100%; background: #222; border: 1px solid var(--border); padding: 9px 14px; border-radius: 20px; color: #fff; font-size: 14px; outline: none; }

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
        .btn { flex: 1; text-align: center; padding: 7px 0; border-radius: 4px; font-size: 11px; font-weight: bold; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 3px; cursor: pointer; border: none; }
        .watch-btn { background-color: var(--accent); color: white; }
        .trailer-btn { background-color: #333; color: #ddd; }

        /* Oynatıcı Modalı ve Geri Çıkma Tuşları */
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 2000; flex-direction: column; justify-content: space-between; }
        
        .modal-header { display: flex; justify-content: space-between; align-items: center; background: #161616; padding: 12px 15px; border-bottom: 1px solid var(--border); }
        .back-btn { background: var(--accent); color: white; border: none; padding: 8px 16px; border-radius: 20px; font-size: 13px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 6px; }
        
        .modal-player-wrapper { flex: 1; display: flex; align-items: center; justify-content: center; width: 100%; padding: 10px; }
        .iframe-container { position: relative; width: 100%; max-width: 900px; padding-bottom: 56.25%; height: 0; background: #000; border-radius: 8px; overflow: hidden; }
        .iframe-container iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; }
        
        .modal-footer-desc { background: #161616; padding: 12px 15px; font-size: 12px; color: var(--muted); border-top: 1px solid var(--border); text-align: center; }

        .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #161616; display: flex; justify-content: space-around; padding: 10px 0; border-top: 1px solid var(--border); z-index: 999; }
        .nav-item { color: var(--muted); text-decoration: none; font-size: 11px; display: flex; flex-direction: column; align-items: center; gap: 3px; }
        .nav-item.active { color: #fff; }
    </style>
</head>
<body>
    <div class="header">
        <a href="/" class="logo"><i class="fa-solid fa-fire"></i> medusafilm</a>
    </div>

    <div class="search-container">
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Film veya dizi ara..." oninput="filterMovies()">
        </div>
    </div>

    <div class="container">
        <div class="section-title">
            <span>Popüler İçerikler (Türkçe Dublaj)</span>
            <span id="countText" style="color:var(--accent);">0 içerik</span>
        </div>
        <div class="movies-grid" id="movieGrid"></div>
    </div>

    <!-- Tam Ekran Video Oynatıcı ve Geri Çıkma Paneli -->
    <div id="mediaModal" class="modal">
        <div class="modal-header">
            <button class="back-btn" onclick="closeModal()"><i class="fa-solid fa-arrow-left"></i> Geri Dön</button>
            <span style="font-size: 13px; color: #fff; font-weight: bold;" id="modalTitle">Medusa Oynatıcı</span>
            <div style="width: 70px;"></div> <!-- Dengeleme -->
        </div>
        <div class="modal-player-wrapper">
            <div class="iframe-container">
                <iframe id="mediaFrame" src="" allowfullscreen allow="autoplay"></iframe>
            </div>
        </div>
        <div class="modal-footer-desc" id="modalDesc"></div>
    </div>

    <div class="bottom-nav">
        <a href="/" class="nav-item active"><span>🏠</span> Anasayfa</a>
        <a href="/" class="nav-item"><span>📺</span> Diziler</a>
        <a href="/" class="nav-item"><span>🎬</span> Filmler</a>
        <a href="/" class="nav-item"><span>✨</span> Keşfet</a>
    </div>

    <script>
        const allMovies = {{ full_json | safe }};
        let searchQuery = '';

        function render() {
            const grid = document.getElementById('movieGrid');
            grid.innerHTML = '';

            let filtered = allMovies.filter(m => m.title.toLowerCase().includes(searchQuery.toLowerCase()));
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
                            <button class="btn watch-btn" onclick='openPlayer("${m.link}", "${m.title}", "${m.overview}")'><i class="fa-solid fa-play"></i> Türkçe İzle</button>
                            <button class="btn trailer-btn" onclick='openPlayer("${m.trailer}", "${m.title} (Fragman)", "${m.overview}")'><i class="fa-brands fa-youtube" style="color:#ff0000;"></i> Fragman</button>
                        </div>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        function filterMovies() {
            searchQuery = document.getElementById('searchInput').value;
            render();
        }

        function openPlayer(url, title, desc) {
            document.getElementById('mediaFrame').src = url;
            document.getElementById('modalTitle').innerText = title;
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
