import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# TMDB API Anahtarı
TMDB_API_KEY = "abdea525bebc9ce403ea266dc78f3555"

# Ana Sayfa ve Arama Şablonu
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medusa Movies</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #141414; color: #fff; margin: 0; padding: 20px; }
        h1 { text-align: center; color: #e50914; margin-bottom: 10px; }
        .search-box { text-align: center; margin-bottom: 30px; }
        .search-box input { padding: 10px; width: 60%; max-width: 400px; border-radius: 4px; border: none; font-size: 16px; }
        .search-box button { padding: 10px 20px; background-color: #e50914; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin-left: 5px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; }
        .movie-card { background: #1f1f1f; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.3); text-align: center; padding-bottom: 10px; text-decoration: none; color: inherit; display: block; transition: transform 0.2s; }
        .movie-card:hover { transform: scale(1.03); }
        .movie-card img { width: 100%; height: auto; }
        .movie-card h3 { font-size: 14px; padding: 0 10px; margin: 10px 0 5px 0; }
        .movie-card p { font-size: 12px; color: #aaa; margin: 0; }
    </style>
</head>
<body>
    <h1>Medusa Movies</h1>
    <div class="search-box">
        <form action="/" method="GET">
            <input type="text" name="q" placeholder="Film ara..." value="{{ query }}">
            <button type="submit">Ara</button>
        </form>
    </div>
    <div class="grid">
        {% for movie in movies %}
        <a href="/movie/{{ movie.id }}" class="movie-card">
            {% if movie.poster_path %}
            <img src="https://image.tmdb.org/t/p/w500{{ movie.poster_path }}" alt="{{ movie.title }}">
            {% else %}
            <img src="https://via.placeholder.com/500x750?text=Resim+Yok" alt="Resim Yok">
            {% endif %}
            <h3>{{ movie.title }}</h3>
            <p>⭐ {{ movie.vote_average }}</p>
        </a>
        {% endfor %}
    </div>
</body>
</html>
"""

# Film Detay Sayfası Şablonu
DETAIL_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name
    
