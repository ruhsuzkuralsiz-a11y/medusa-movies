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
    
