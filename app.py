from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Medusa Movies</title>
        <style>
            body { background-color: #121212; color: #fff; font-family: Arial, sans-serif; margin: 0; padding-bottom: 70px; }
            .header { display: flex; justify-content: space-between; align-items: center; padding: 12px 15px; background-color: #161616; border-bottom: 2px solid #e50914; }
            .logo { color: #e50914; font-size: 20px; font-weight: bold; text-decoration: none; }
            .section-title { padding: 15px; font-size: 15px; font-weight: bold; color: #fff; }
            .movies-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 0 15px; }
            .movie-card { background-color: #1a1a1a; border-radius: 8px; overflow: hidden; cursor: pointer; text-decoration: none; color: inherit; display: block; }
            .movie-poster { width: 100%; height: 210px; object-fit: cover; }
            .movie-info { padding: 10px; }
            .movie-name { font-size: 13px; font-weight: bold; margin-bottom: 4px; }
            .movie-rating { color: #f1c40f; font-size: 11px; font-weight: bold; }
            .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #161616; display: flex; justify-content: space-around; padding: 10px 0; border-top: 1px solid #222; }
            .nav-item { color: #888; text-decoration: none; font-size: 11px; display: flex; flex-direction: column; align-items: center; gap: 3px; }
            .nav-item.active { color: #fff; }
        </style>
    </head>
    <body>
        <div class="header">
            <a href="/" class="logo">🔥 medusafilm</a>
        </div>
        <div class="section-title">Popüler Filmler</div>
        <div class="movies-grid">
            <a href="https://multiembed.mov/?video_id=1263337" class="movie-card">
                <img src="https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=500" class="movie-poster">
                <div class="movie-info">
                    <div class="movie-name">Odyssey</div>
                    <div class="movie-rating">⭐ 8.0</div>
                </div>
            </a>
            <a href="
    
