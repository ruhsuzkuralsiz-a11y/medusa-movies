import os
import requests
from flask import Flask, render_template_string

app = Flask(__name__)

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")


@app.route("/")
def home():
  if not TMDB_API_KEY:
    return "Hata: TMDB API Key bulunamadı!"

  url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=tr-TR&page=1"
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
            header { background: #1f1f1f; padding: 15px; text-align: center; font-size: 24px; font-weight: bold; color: #e50914; border-bottom: 2px solid #333; }
            .container { padding:
  
