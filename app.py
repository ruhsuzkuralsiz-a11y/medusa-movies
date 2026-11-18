from flask import Flask, render_template_string
import requests

app = Flask(__name__)

# TMDB Açık Film API Anahtarı (Dünyadaki tüm filmleri ve dizileri otomatik çeker)
TMDB_API_KEY = "c814436531362e9b1192e185f4702958"

@app.route('/')
def index():
    try:
        # Popüler filmleri ve dizileri otomatik olarak API'den çekiyoruz
        url = f"https://api.themoviedb.org/3/trending/all/day?api_key={TMDB_API_KEY}&language=tr-TR"
        response = requests.get(url)
        data = response.json()
        results = data.get('results', [])
    except:
        results = []

    movies_html = ""
    for item in results:
        title = item.get('title') or item.get('name') or 'Bilinmeyen'
        poster_path = item.get('poster_path')
        vote = round(item.get('vote_average', 0), 1)
        media_type = item.get('media_type', 'movie')
        tmdb_id = item.get('id')

        if poster_path:
            image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            image_url = "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=500"

        # İzleme linki otomatik oluşturuluyor
        watch_link = f"https://multiembed.mov/?video_id={tmdb_id}&tmdb=1"

        movies_html += f"""
        <a href="{watch_link}" class="movie-card">
            <img src="{image_url}" class="movie-poster">
            <div class="movie-info">
                <div class="movie-name">{title}</div>
                <div class="movie-rating">⭐ {vote} ({media_type.upper()})</div>
            </div>
        </a>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Medusa Movies - Canlı Yayın Film Sitesi</title>
        <style>
            body {{ background-color: #121212; color: #ffffff; font-family: Arial, sans-serif; margin: 0; padding-bottom: 70px; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 15px; background-color: #161616; border-bottom: 2px solid #e50914; }}
            .logo {{ color: #e50914; font-size: 20px; font-weight: bold; text-decoration: none; }}
            .section-title {{ padding: 15px; font-size: 16px; font-weight: bold; color: #fff; }}
            .movies-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 0 15px; }}
            .movie-card {{ background-color: #1a1a1a; border-radius: 8px; overflow: hidden; text-decoration: none; color: inherit; display: block; box-shadow: 0 4px 8px rgba(0,0,0,0.4); }}
            .movie-poster {{ width: 100%; height: 210px; object-fit: cover; background: #222; }}
            .movie-info {{ padding: 10px; }}
            .movie-name {{ font-size: 13px; font-weight: bold; margin-bottom: 4px; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
            .movie-rating {{ color: #f1c40f; font-size: 11px; font-weight: bold; }}
            .bottom-nav {{ position: fixed; bottom: 0; left: 0; width: 100%; background-color: #161616; display: flex; justify-content: space-around; padding: 10px 0; border-top: 1px solid #222; z-index: 999; }}
            .nav-item {{ color: #888; text-decoration: none; font-size: 11px; display: flex; flex-direction: column; align-items: center; gap: 3px; }}
            .nav-item.active {{ color: #fff; }}
        </style>
    </head>
    <body>
        <div class="header">
            <a href="/" class="logo">🔥 medusafilm</a>
        </div>
        <div class="section-title">Netflix, DC ve Trend İçerikler</div>
        <div class="movies-grid">
            {movies_html}
        </div>
        <div class="bottom-nav">
            <a href="/" class="nav-item active"><span>🏠</span> Anasayfa</a>
            <a href="/" class="nav-item"><span>🎞️</span> Filmler</a>
            <a href="/" class="nav-item"><span>✨</span> Keşfet</a>
            <a href="/" class="nav-item"><span>📺</span> Diziler</a>
            <a href="/" class="nav-item"><span>☰</span> Menu</a>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
        
