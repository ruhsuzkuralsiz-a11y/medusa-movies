from flask import Flask

app = Flask(__name__)

# Netflix, DC, Marvel, Anime ve Yeni Çıkanlar (Fragman ve Türkçe Dublaj Seçenekli)
movies = [
    {
        "title": "The Batman",
        "rating": "8.5",
        "category": "DC / FİLM",
        "image": "https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpooo50r9T25onhq.jpg",
        "link": "https://multiembed.mov/?video_id=tt1877830",
        "trailer": "https://www.youtube.com/embed/mqqft2x_V4g"
    },
    {
        "title": "Stranger Things (Yeni Sezon)",
        "rating": "8.7",
        "category": "NETFLIX",
        "image": "https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg",
        "link": "https://multiembed.mov/?video_id=tt4574334",
        "trailer": "https://www.youtube.com/embed/b9EkMc79ZSU"
    },
    {
        "title": "Attack on Titan (Final)",
        "rating": "9.1",
        "category": "ANİME",
        "image": "https://image.tmdb.org/t/p/w500/hTP1DtLGFamjfu8WqjmuQdP1sHk.jpg",
        "link": "https://multiembed.mov/?video_id=tt2560140",
        "trailer": "https://www.youtube.com/embed/M_OauHnAFc4"
    },
    {
        "title": "Deadpool & Wolverine (Yeni)",
        "rating": "8.3",
        "category": "MARVEL",
        "image": "https://image.tmdb.org/t/p/w500/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg",
        "link": "https://multiembed.mov/?video_id=tt6263850",
        "trailer": "https://www.youtube.com/embed/73_1biulkYk"
    },
    {
        "title": "Wednesday",
        "rating": "8.1",
        "category": "NETFLIX",
        "image": "https://image.tmdb.org/t/p/w500/9PFonBhy4cQy7Jz20NpMygczOkv.jpg",
        "link": "https://multiembed.mov/?video_id=tt13443470",
        "trailer": "https://www.youtube.com/embed/Di310WS8nLk"
    },
    {
        "title": "Demon Slayer",
        "rating": "8.8",
        "category": "ANİME",
        "image": "https://image.tmdb.org/t/p/w500/xUfRZu2mi8bH6SzQj1Qylb0vqaA.jpg",
        "link": "https://multiembed.mov/?video_id=tt9335498",
        "trailer": "https://www.youtube.com/embed/VQGCw1Bs4KA"
    }
]

@app.route('/')
def index():
    movies_html = ""
    for m in movies:
        movies_html += f"""
        <div class="movie-card">
            <img src="{m['image']}" class="movie-poster">
            <div class="movie-info">
                <div class="movie-name">{m['title']}</div>
                <div class="movie-meta">
                    <span class="movie-rating">⭐ {m['rating']}</span>
                    <span class="movie-cat">{m['category']}</span>
                </div>
                <div class="btn-group">
                    <a href="{m['link']}" class="btn watch-btn">🎬 Türkçe Dublaj</a>
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
        <title>Medusa Movies - Türkçe Dublaj & Fragmanlar</title>
        <style>
            body {{ background-color: #121212; color: #ffffff; font-family: Arial, sans-serif; margin: 0; padding-bottom: 70px; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 15px; background-color: #161616; border-bottom: 2px solid #e50914; }}
            .logo {{ color: #e50914; font-size: 20px; font-weight: bold; text-decoration: none; }}
            .filter-bar {{ display: flex; gap: 8px; padding: 12px 15px; overflow-x: auto; background: #181818; white-space: nowrap; }}
            .filter-btn {{ background: #222; color: #bbb; border: none; padding: 6px 14px; border-radius: 20px; font-size: 12px; cursor: pointer; text-decoration: none; }}
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
            .watch-api {{ background-color: #e50914; color: white; }}
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
        
        <div class="filter-bar">
            <a href="/" class="filter-btn active">Tümü</a>
            <a href="/" class="filter-btn">Netflix</a>
            <a href="/" class="filter-btn">DC / Marvel</a>
            <a href="/" class="filter-btn">Animeler</a>
            <a href="/" class="filter-btn">Yeni Çıkanlar</a>
        </div>

        <div class="section-title">Netflix, DC, Anime & Fragmanlar</div>
        
        <div class="movies-grid">
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

