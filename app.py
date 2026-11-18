import os
import requests
from flask import Flask, render_template_string

app = Flask(__name__)

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

@app.route("/")
def home():
    if not TMDB_API_KEY:
        return "Hata: TMDB API Key bulunamadı!"
    
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=tr-TR"
    response = requests.get(url)
    
    movies = []
    if response.status_code == 200:
        movies = response.json().get("results", [])
        
    html_code = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Medusa Movies - Film Akış Platformu</title>
        <style>
            body { background-color: #121212; color: #ffffff; font-family: Arial, sans-serif; margin: 0; padding: 0; }
            header { background: #1f1f1f; padding: 20px; text-align: center; font-size: 24px; font-weight: bold; color: #e50914; }
            .container { padding: 20px; max-width: 1200px; margin: auto; }
            .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 20px; }
            .movie-card { background: #1f1f1f; border-radius: 8px; overflow: hidden; text-align: center; padding-bottom: 10px; }
            .movie-card img { width: 100%; height: 225px; object-fit: cover; }
            .movie-title { font-size: 14px; padding: 10px; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        </style>
    </head>
    <body>
        <header>MEDUSA MOVIES</header>
        <div class="container">
            <h2>Popüler Filmler</h2>
            <div class="grid">
                {% for movie in movies %}
                <div class="movie-card">
                    <img src="https://image.tmdb.org/t/p/w500{{ movie.poster_path }}" alt="{{ movie.title }}">
                    <p class="movie-title">{{ movie.title }}</p>
                </div>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_code, movies=movies)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
  
