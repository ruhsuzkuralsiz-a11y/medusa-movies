import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# TMDB API Anahtarı
TMDB_API_KEY = "abdea525bebc9ce403ea266dc78f3555"

# Ana Sayfa Şablonu
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medusa Movies</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #121212; color: #fff; margin: 0; padding-bottom: 70px; }
        header { background: #1a1a1a; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #222; position: sticky; top: 0; z-index: 1000; }
        .logo { color: #ff3d00; font-size: 20px; font-weight: bold; text-decoration: none; display: flex; align-items: center; gap: 5px; }
        .logo span { color: #fff; }
        .search-container { padding: 15px 20px; background: #161616; text-align: center; }
        .search-container input { width: 100%; max-width: 600px; padding: 12px 15px; border-radius: 25px; border: none; background: #222; color: #fff; font-size: 15px; outline: none; }
        .section-title { padding: 15px 20px 5px 20px; font-size: 18px; font-weight: bold; color: #ddd; }
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; padding: 10px 15px; max-width: 1200px; margin: 0 auto; }
        @media(min-width: 768px) { .grid { grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 20px; padding: 20px; } }
        .movie-card { background: #1a1a1a; border-radius: 10px; overflow: hidden; text-decoration: none; color: inherit; display: flex; flex-direction: column; box-shadow: 0 4px 10px rgba(0,0,0,0.4); transition: transform 0.2s; }
        .movie-card:hover { transform: translateY(-3px); }
        .poster-wrapper { position: relative; width: 100%; padding-top: 150%; background: #222; }
        .poster-wrapper img { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; }
        .movie-info { padding: 10px; display: flex; flex-direction: column; gap: 4px; }
        .movie-title { font-size: 14px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin: 0; }
        .movie-meta { display: flex; justify-content: space-between; font-size: 12px; color: #aaa; }
        .rating { color: #f5c518; font-weight: bold; }
        
        nav.bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background: #181818; border-top: 1px solid #282828; display: flex; justify-content: space-around; padding: 10px 0; z-index: 1000; }
        nav.bottom-nav a { color: #aaa; text-decoration: none; font-size: 11px; display: flex; flex-direction: column; align-items: center; gap: 3px; }
        nav.bottom-nav a.active, nav.bottom-nav a:hover { color: #ff3d00; }
        nav.bottom-nav svg { width: 20px; height: 20px; fill: currentColor; }
    </style>
</head>
<body>
    <header>
        <a href="/" class="logo">🔥 Medusa<span>Movies</span></a>
    </header>

    <div class="search-container">
        <form action="/" method="GET">
            <input type="text" name="q" placeholder="Film ara (Örn: Avengers, Matrix...)" value="{{ query }}">
        </form>
    </div>

    <div class="section-title">Popüler Filmler</div>
    <div class="grid">
        {% for movie in movies %}
        <a href="/movie/{{ movie.id }}" class="movie-card">
            <div class="poster-wrapper">
                {% if movie.poster_path %}
                <img src="https://image.tmdb.org/t/p/w500{{ movie.poster_path }}" alt="{{ movie.title }}">
                {% else %}
                <img src="https://via.placeholder.com/500x750?text=Resim+Yok" alt="Resim Yok">
                {% endif %}
            </div>
            <div class="movie-info">
                <div class="movie-title">{{ movie.title }}</div>
                <div class="movie-meta">
                    <span>{{ movie.release_date[:4] if movie.release_date else '' }}</span>
                    <span class="rating">⭐ {{ "%.1f"|format(movie.vote_average) }}</span>
                </div>
            </div>
        </a>
        {% endfor %}
    </div>

    <nav class="bottom-nav">
        <a href="/" class="active">
            <svg viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
            Anasayfa
        </a>
        <a href="/">
            <svg viewBox="0 0 24 24"><path d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0-2-.9-2-2V4c0-1.1-.9-2-2-2zm0 14H8V4h12v12z"/></svg>
            Filmler
        </a>
        <a href="/">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10
            
