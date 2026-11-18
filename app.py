from flask import Flask

app = Flask(__name__)

# Netflix, Disney+, DC, Marvel, Animasyon, Anime ve Yeni Çıkanlar Dev Arşivi
movies = [
    # NETFLIX
    {"title": "Stranger Things", "rating": "8.7", "category": "netflix", "cat_name": "NETFLIX", "image": "https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg", "link": "https://multiembed.mov/?video_id=tt4574334&tmdb=1", "trailer": "https://www.youtube.com/embed/b9EkMc79ZSU"},
    {"title": "Wednesday", "rating": "8.1", "category": "netflix", "cat_name": "NETFLIX", "image": "https://image.tmdb.org/t/p/w500/9PFonBhy4cQy7Jz20NpMygczOkv.jpg", "link": "https://multiembed.mov/?video_id=tt13443470&tmdb=1", "trailer": "https://www.youtube.com/embed/Di310WS8nLk"},
    {"title": "Extraction 2", "rating": "7.1", "category": "netflix", "cat_name": "NETFLIX", "image": "https://image.tmdb.org/t/p/w500/7gKI9hpJcZUQzwsCUO2k8k5k20j.jpg", "link": "https://multiembed.mov/?video_id=tt12261776&tmdb=1", "trailer": "https://www.youtube.com/embed/Y2k_CCDiwEY"},
    {"title": "The Witcher", "rating": "8.0", "category": "netflix", "cat_name": "NETFLIX", "image": "https://image.tmdb.org/t/p/w500/7vjaCdMw15FEbXyLQTVa04URsPm.jpg", "link": "https://multiembed.mov/?video_id=tt5180504&tmdb=1", "trailer": "https://www.youtube.com/embed/ndl1W4ltcmg"},
    {"title": "Money Heist", "rating": "8.2", "category": "netflix", "cat_name": "NETFLIX", "image": "https://image.tmdb.org/t/p/w500/reEMJA1uzscCbkpeRJeTT2bjqUp.jpg", "link": "https://multiembed.mov/?video_id=tt6468322&tmdb=1", "trailer": "https://www.youtube.com/embed/ZAXA1DV4dt0"},

    # DISNEY+
    {"title": "Loki", "rating": "8.2", "category": "disney", "cat_name": "DİSNEY+", "image": "https://image.tmdb.org/t/p/w500/kEl2t3OhXc3ZbwwFBh1xu5CS6g6.jpg", "link": "https://multiembed.mov/?video_id=tt9140554&tmdb=1", "trailer": "https://www.youtube.com/embed/nW948Va-l10"},
    {"title": "The Mandalorian", "rating": "8.7", "category": "disney", "cat_name": "DİSNEY+", "image": "https://image.tmdb.org/t/p/w500/eU1i6eHXlzMOlqONkn1GhrSBExH.jpg", "link": "https://multiembed.mov/?video_id=tt8111088&tmdb=1", "trailer": "https://www.youtube.com/embed/aOC8E8z_ifw"},
    {"title": "Cars", "rating": "7.2", "category": "disney", "cat_name": "DİSNEY+", "image": "https://image.tmdb.org/t/p/w500/qa6iEzPrgRZbxptqGTx04csg7qg.jpg", "link": "https://multiembed.mov/?video_id=tt0317219&tmdb=1", "trailer": "https://www.youtube.com/embed/SbXIu2T-_uk"},
    {"title": "Moana 2", "rating": "7.0", "category": "disney", "cat_name": "DİSNEY+", "image": "https://image.tmdb.org/t/p/w500/aHb1c9F7c2qW7n4J2G9B4XkR0P8.jpg", "link": "https://multiembed.mov/?video_id=tt13622976&tmdb=1", "trailer": "https://www.youtube.com/embed/hDZue5WpZ98"},

    # DC & MARVEL
    {"title": "The Batman", "rating": "8.5", "category": "dcmarvel", "cat_name": "DC / MARVEL", "image": "https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpooo50r9T25onhq.jpg", "link": "https://multiembed.mov/?video_id=tt1877830&tmdb=1", "trailer": "https://www.youtube.com/embed/mqqft2x_V4g"},
    {"title": "Deadpool & Wolverine", "rating": "8.3", "category": "dcmarvel", "cat_name": "DC / MARVEL", "image": "https://image.tmdb.org/t/p/w500/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg", "link": "https://multiembed.mov/?video_id=tt6263850&tmdb=1", "trailer": "https://www.youtube.com/embed/73_1biulkYk"},
    {"title": "Spider-Man: No Way Home", "rating": "8.2", "category": "dcmarvel", "cat_name": "DC / MARVEL", "image": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg", "link": "https://multiembed.mov/?video_id=tt10872600&tmdb=1", "trailer": "https://www.youtube.com/embed/JfVOs4VSpmA"},
    {"title": "Joker", "rating": "8.4", "category": "dcmarvel", "cat_name": "DC / MARVEL", "image": "https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg", "link": "https://multiembed.mov/?video_id=tt7286456&tmdb=1", "trailer": "https://www.youtube.com/embed/zAGVQLHvwOY"},

    # ANİMASYON
    {"title": "Spider-Man: Across the Spider-Verse", "rating": "8.4", "category": "animasyon", "cat_name": "ANİMASYON", "image": "https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg", "link": "https://multiembed.mov/?video_id=tt9362722&tmdb=1", "trailer": "https://www.youtube.com/embed/cqGjhVJWtEg"},
    {"title": "Kral Şakir: Mikroplar Savaşı", "rating": "7.5", "category": "animasyon", "cat_name": "ANİMASYON", "image": "https://image.tmdb.org/t/p/w500/w1vI3Ff8zD4GkE5Cj5z2H3k3d0s.jpg", "link": "https://multiembed.mov/?video_id=tt13243142&tmdb=1", "trailer": "https://www.youtube.com/embed/6i2b5S7Gj78"},
    {"title": "Inside Out 2", "rating": "7.8", "category": "animasyon", "cat_name": "ANİMASYON", "image": "https://image.tmdb.org/t/p/w500/vpnVM9B6NMmQpWeZvzLvDESb2QY.jpg", "link": "https://multiembed.mov/?video_id=tt22022452&tmdb=1", "trailer": "https://www.youtube.com/embed/LEjhY15eCx0"},

    # ANİME
    {"title": "Attack on Titan", "rating": "9.1", "category": "anime", "cat_name": "ANİME", "image": "https://image.tmdb.org/t/p/w500/hTP1DtLGFamjfu8WqjmuQdP1sHk.jpg", "link": "https://multiembed.mov/?video_id=tt2560140&tmdb=1", "trailer": "https://www.youtube.com/embed/M_OauHnAFc4"},
    {"title": "Demon Slayer", "rating": "8.8", "category": "anime", "cat_name": "ANİME", "image": "https://image.tmdb.org/t/p/w500/xUfRZu2mi8bH6SzQj1Qylb0vqaA.jpg", "link": "https://multiembed.mov/?video_id=tt9335498&tmdb=1", "trailer": "https://www.youtube.com/embed/VQGCw1Bs4KA"},
    {"title": "Death Note", "rating": "9.0", "category": "anime", "cat_name": "ANİME", "image": "https://image.tmdb.org/t/p/w500/iRl71SFVTn0wAPiFFbWpnBCabux.jpg", "link": "https://multiembed.mov/?video_id=tt0877057&tmdb=1", "trailer": "https://www.youtube.com/embed/NlJZ-YgShjo"},
    {"title": "Jujutsu Kaisen", "rating": "8.6", "category": "anime", "cat_name": "ANİME", "image": "https://image.tmdb.org/t/p/w500/hUzeosd33nzE5MCNsZxCGEKTXaQ.jpg", "link": "https://multiembed.mov/?video_id=tt12343534&tmdb=1", "trailer": "https://www.youtube.com/embed/vHDdoSkKwXE"},

    # YENİ ÇIKANLAR
    {"title": "Dune: Çöl Gezegeni Bölüm 2", "rating": "8.6", "category": "yeni", "cat_name": "YENİ ÇIKAN", "image": "https://image.tmdb.org/t/p/w500/8b8R8l88Qje9dn9OE8PY05Nxl1X.jpg", "link": "https://multiembed.mov/?video_id=tt15239678&tmdb=1", "trailer": "https://www.youtube.com/embed/Way9Dexny3w"},
    {"title": "Interstellar", "rating": "8.7", "category": "yeni", "cat_name": "YENİ ÇIKAN", "image": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg", "link": "https://multiembed.mov/?video_id=tt0816692&tmdb=1", "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E"},
    {"title": "Oppenheimer", "rating": "8.1", "category": "yeni", "cat_name": "YENİ ÇIKAN", "image": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg", "link": "https://multiembed.mov/?video_id=tt15398776&tmdb=1", "trailer": "https://www.youtube.com/embed/uYPbbksJxIg"}
]

@app.route('/')
def index():
    movies_html = ""
    for m in movies:
        movies_html += f"""
        <div class="movie-card" data-category="{m['category']}">
            <img src="{m['image']}" class="movie-poster" loading="lazy">
            <div class="movie-info">
                <div class="movie-name">{m['title']}</div>
                <div class="movie-meta">
                    <span class="movie-rating">⭐ {m['rating']}</span>
                    <span class="movie-cat">{m['cat_name']}</span>
                </div>
                <div class="btn-group">
                    <a href="{m['link']}" class="btn watch-btn" target="_blank">🎬 Türkçe İzle</a>
                    <a href="#" onclick="openModal('{m['trailer']}'); return false;" class="btn trailer-btn">🎥 Fragman</a>
                </div>
            </div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Medusa Movies - Reklamsız Film ve Dizi Arşivi</title>
        <style>
            body {{ background-color: #121212; color: #ffffff; font-family: Arial, sans-serif; margin: 0; padding-bottom: 70px; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 15px; background-color: #161616; border-bottom: 2px solid #e50914; }}
            .logo {{ color: #e50914; font-size: 20px; font-weight: bold; text-decoration: none; }}
            
            /* Kategori Filtre Çubuğu */
            .filter-bar {{ display: flex; gap: 8px; padding: 12px 15px; overflow-x: auto; background: #181818; white-space: nowrap; scrollbar-width: none; }}
            .filter-bar::-webkit-scrollbar {{ display: none; }}
            .filter-btn {{ background: #222; color: #bbb; border: none; padding: 7px 16px; border-radius: 20px; font-size: 12px; cursor: pointer; text-decoration: none; transition: 0.2s; }}
            .filter-btn.active {{ background: #e50914; color: #fff; font-weight: bold; }}
            
            .section-title {{ padding: 15px 15px 5px 15px; font-size: 15px; font-weight: bold; color: #fff; }}
            .movies-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 10px 15px; }}
            .movie-card {{ background-color: #1a1a1a; border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 8px rgba(0,0,0,0.4); }}
            .movie-poster {{ width: 100%; height: 200px; object-fit: cover; background: #222; }}
            .movie-info {{ padding: 10px; display: flex; flex-direction: column; gap: 6px; }}
            .movie-name {{ font-size: 13px; font-weight: bold; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
            .movie-meta {{ display: flex; justify-content: space-between; font-size: 11px; }}
            .movie-rating {{ color: #f1c40f; font-weight: bold; }}
            .movie-cat {{ color: #e50914; font-weight: bold; }}
            .btn-group {{ display: flex; gap: 5px; margin-top: 5px; }}
            .btn {{ flex: 1; text-align: center; padding: 6px 0; border-radius: 4px; font-size: 11px; font-weight: bold; text-decoration: none; }}
            .watch-btn {{ background-color: #e50914; color: white; }}
            .trailer-btn {{ background-color: #333; color: #ddd; }}
            
            /* Modal / Fragman Penceresi */
            .modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); justify-content: center; align-items: center; z-index: 1000; }}
            .modal-content {{ width: 90%; max-width: 500px; position: relative; }}
            .close-btn {{ position: absolute; top: -35px; right: 0; color: #fff; font-size: 24px; cursor: pointer; background: none; border: none; }}
            .iframe-container {{ position: relative; width: 100%; padding-bottom: 56.25%; height: 0; }}
            .iframe-container iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px; border: none; }}

            .bottom-nav {{ position: fixed; bottom: 0; left: 0; width: 100%; background-color: #161616; display: flex; justify-content: space-around; padding: 10px 0; border-top: 1px solid #222; z-index: 999; }}
            .nav-item {{ color: #888; text-decoration: none; font-size: 11px; display: flex; flex-direction: column; align-items: center; gap: 3px; }}
            .nav-item.active {{ color: #fff; }}
        </style>
    </head>
    <body>
        <div class="header">
            <a href="/" class="logo">🔥 medusafilm</a>
        </div>
        
        <!-- Üst Kategori Filtreleri -->
        <div class="filter-bar">
            <button class="filter-btn active" onclick="filterCategory('all', this)">Tümü</button>
            <button class="filter-btn" onclick="filterCategory('netflix', this)">Netflix</button>
            <button class="filter-btn" onclick="filterCategory('disney', this)">Disney+</button>
            <button class="filter-btn" onclick="filterCategory('dcmarvel', this)">DC / Marvel</button>
            <button class="filter-btn" onclick="filterCategory('animasyon', this)">Animasyon</button>
            <button class="filter-btn" onclick="filterCategory('anime', this)">Animeler</button>
            <button class="filter-btn" onclick="filterCategory('yeni', this)">Yeni Çıkanlar</button>
        </div>

        <div class="section-title">Popüler Filmler & Diziler</div>
        
        <div class="movies-grid" id="moviesGrid">
            {movies_html}
        </div>

        <!-- Fragman Modalı -->
        <div id="trailerModal" class="modal">
            <div class="modal-content">
                <button class="close-btn" onclick="closeModal()">&times;</button>
                <div class="iframe-container">
                    <iframe id="trailerFrame" src="" allowfullscreen></iframe>
                </div>
            </div>
        </div>

        <div class="bottom-nav">
            <a href="/" class="nav-item active"><span>🏠</span> Anasayfa</a>
            <a href="/" class="nav-item"><span>🎞️</span> Filmler</a>
            <a href="/" class="nav-item"><span>✨</span> Keşfet</a>
            <a href="/" class="nav-item"><span>📺</span> Diziler</a>
            <a href="/" class="nav-item"><span>☰</span> Menu</a>
        </div>

        <script>
            function filterCategory(cat, element) {{
                // Buton aktiflik değişimi
                document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
                element.classList.add('active');

                // Kartları filtreleme
                const cards = document.querySelectorAll('.movie-card');
                cards.forEach(card => {{
                    if (cat === 'all' || card.getAttribute('data-category') === cat) {{
                        card.style.display = 'flex';
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});
            }}

            function openModal(url) {{
                document.getElementById('trailerFrame').src = url;
                document.getElementById('trailerModal').style.display = 'flex';
            }}
            function closeModal() {{
                document.getElementById('trailerFrame').src = '';
                document.getElementById('trailerModal').style.display = 'none';
            }}
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
        
