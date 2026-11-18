from flask import Flask

app = Flask(__name__)

# En popüler Netflix, DC ve Marvel içerikleri (Anında ve hatasız yüklenir)
movies = [
    {
        "title": "The Batman",
        "rating": "8.5",
        "type": "DC / FİLM",
        "image": "https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpooo50r9T25onhq.jpg",
        "link": "https://multiembed.mov/?video_id=tt1877830"
    },
    {
        "title": "Stranger Things",
        "rating": "8.7",
        "type": "NETFLIX",
        "image": "https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg",
        "link": "https://multiembed.mov/?video_id=tt4574334"
    },
    {
        "title": "Spider-Man: No Way Home",
        "rating": "8.2",
        "type": "MARVEL",
        "image": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
        "link": "https://multiembed.mov/?video_id=tt10872600"
    },
    {
        "title": "Wednesday",
        "rating": "8.1",
        "type": "NETFLIX",
        "image": "https://image.tmdb.org/t/p/w500/9PFonBhy4cQy7Jz20NpMygczOkv.jpg",
        "link": "https://multiembed.mov/?video_id=tt13443470"
    },
    {
        "title": "Joker",
        "rating": "8.4",
        "type": "DC / FİLM",
        "image": "https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",
        "link": "https://multiembed.mov/?video_id=tt7286456"
    },
    {
        "title": "Avengers: Endgame",
        "rating": "8.4",
        "type": "MARVEL",
        "image": "
        
