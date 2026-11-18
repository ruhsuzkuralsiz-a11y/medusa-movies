import requests
from flask import Flask, render_template_string

app = Flask(__name__)

# Yeni ve güncel TMDB API Anahtarı
TMDB_API_KEY = "abdea525bebc9ce403ea266dc78f3555"

# Şık bir arayüz için basit HTML/CSS şablonu
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medusa Movies</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #141414; color: #fff; margin: 0; padding: 20px; }
        h1 { text-align: center; color: #e50914; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; }
        .movie-card { background: #1f1f1f; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.3); text-align: center; padding-bottom: 10px; }
        .movie-card img { width: 100%; height: auto; }
        .movie-card h3 { font-size: 14px; padding: 0 10px; margin: 10px 0 5px 0; }
        .movie-card p { font-size: 12px; color: #aaa; margin: 0; }
    </style>
</head>
<body>
    <h1>Medusa Movies - Popüler Filmler</h1>
    <div class="grid">
        {% for movie in movies %}
        <div class="movie-card">
            {% if movie.poster_path %}
            <img src="https://image.tmdb.org/t/p/w500{{ movie.poster_path }}" alt="{{ movie.title }}">
            {% else %}
            <img src="https://via.placeholder.com/500x750?text=Resim+Yok" alt="Resim Yok">
            {% endif %}
            <h3>{{ movie.title }}</h3>
            <p>⭐ {{ movie.vote_average }}</p>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=tr-TR&page=1"
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"TMDB API Hatası! Status Code: {response.status_code}, Cevap: {response.text}"
    
    data = response.json()
    movies = data.get('results', [])
    return render_template_string(HTML_TEMPLATE, movies=movies)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
