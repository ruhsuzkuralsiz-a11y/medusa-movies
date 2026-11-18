import random
import requests
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# İSTEĞE BAĞLI: Ücretsiz TMDB API anahtarınızı buraya yazarsanız yüzlerce güncel içerik otomatik çekilir.
TMDB_API_KEY = ""

# Yerleşik Zengin Film/Dizi Veritabanı
BASE_CATALOG = [
    {
        "id": 101,
        "title": "Stranger Things",
        "year": 2025,
        "rating": 8.7,
        "category": "Netflix",
        "quality": "4K UHD",
        "lang": "Türkçe Dublaj & Altyazı",
        "poster": "https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg",
        "trailer_id": "https://www.youtube.com/embed/b9EkMc79ZSU",
        "overview": "Hawkins kasabasında kaybolan bir çocuğun ardından gizli deneyler ve doğaüstü güçler ortaya çıkar.",
    },
    {
        "id": 102,
        "title": "The Witcher",
        "year": 2024,
        "rating": 8.1,
        "category": "Netflix",
        "quality": "1080p",
        "lang": "Türkçe Dublaj",
        "poster": "https://image.tmdb.org/t/p/w500/7vjaCdMw15FEbXyLQTVa04URsPm.jpg",
        "trailer_id": "https://www.youtube.com/embed/ndl1W4ltcmg",
        "overview": "Rivyalı Geralt, insanların yaratıklardan daha acımasız olabildiği bir dünyada kaderini arar.",
    },
    {
        "id": 103,
        "title": "The Mandalorian",
        "year": 2024,
        "rating": 8.7,
        "category": "Disney+",
        "quality": "4K UHD",
        "lang": "Türkçe Dublaj & Altyazı",
        "poster": "https://image.tmdb.org/t/p/w500/eU1i6eHXlzMOlqONkn1GhrSBExH.jpg",
        "trailer_id": "https://www.youtube.com/embed/aOC8E8z_ifw",
        "overview": "Galaksinin dış halkalarında yalnız bir ödül avcısının Grogu ile olan macerası.",
    },
    {
        "id": 104,
        "title": "Loki",
        "year": 2024,
        "rating": 8.2,
        "category": "Disney+",
        "quality": "1080p",
        "lang": "Türkçe Altyazı",
        "poster": "https://image.tmdb.org/t/p/w500/kEl2t3OhXc3ZbwwFBh1xu5CS6g6.jpg",
        "trailer_id": "https://www.youtube.com/embed/nW948Va-l10",
        "overview": "Zaman Değişim Otoritesi tarafından yakalanan Loki, çoklu evrenlerin kaderini değiştirir.",
    },
    {
        "id": 105,
        "title": "The Batman",
        "year": 2024,
        "rating": 7.8,
        "category": "DC/Marvel",
        "quality": "4K UHD",
        "lang": "Türkçe Dublaj & Altyazı",
        "poster": "https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpooo50r9T25onhq.jpg",
        "trailer_id": "https://www.youtube.com/embed/mqqft2x_V4g",
        "overview": "Gotham City'de yolsuzluğun kökünü kazımaya çalışan Batman, Riddler'ın bulmacalarıyla yüzleşir.",
    },
    {
        "id": 106,
        "title": "Avengers: Endgame",
        "year": 2023,
        "rating": 8.4,
        "category": "DC/Marvel",
        "quality": "4K UHD",
        "lang": "Türkçe Dublaj",
        "poster": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
        "trailer_id": "https://www.youtube.com/embed/TcMBFSGVi1c",
        "overview": "Thanos'un evrenin yarısını yok etmesinin ardından kalan kahramanlar son bir kez toplanır.",
    },
    {
        "id": 107,
        "title": "Deadpool & Wolverine",
        "year": 2025,
        "rating": 8.0,
        "category": "DC/Marvel",
        "quality": "4K UHD",
        "lang": "Türkçe Dublaj & Altyazı",
        "poster": "https://image.tmdb.org/t/p/w500/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg",
        "trailer_id": "https://www.youtube.com/embed/73_1biulkYk",
        "overview": "Wade Wilson ve isteksiz Wolverine, çoklu evreni kurtarmak için kaotik bir yolculuğa çıkar.",
    },
    {
        "id": 108,
        "title": "Spider-Man: Across the Spider-Verse",
        "year": 2024,
        "rating": 8.6,
        "category": "Animasyon",
        "quality": "4K UHD",
        "lang": "Türkçe Dublaj & Altyazı",
        "poster": "https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg",
        "trailer_id": "https://www.youtube.com/embed/cqGjhVJWtEg",
        "overview": "Miles Morales, çoklu evrenlerdeki Örümcek İnsanlar topluluğuyla karşı karşıya gelir.",
    },
    {
        "id": 109,
        "title": "Ters Yüz 2 (Inside Out 2)",
        "year": 2025,
        "rating": 7.9,
        "category": "Animasyon",
        "quality": "1080p",
        "lang": "Türkçe Dublaj",
        "poster": "https://image.tmdb.org/t/p/w500/vpnVM9B6NMmQpWeZvzLvDESb2QY.jpg",
        "trailer_id": "https://www.youtube.com/embed/LEjhY15eCx0",
        "overview": "Ergenliğe giren Riley'nin zihnindeki kontrol merkezine Kaygı başta olmak üzere yeni duygular katılır.",
    },
    {
        "id": 110,
        "title": "Attack on Titan",
        "year": 2024,
        "rating": 9.1,
        "category": "Anime",
        "quality": "1080p",
        "lang": "Türkçe Altyazı",
        "poster": "https://image.tmdb.org/t/p/w500/hTP1DtLGFamjfu8WqjmuQdP1sHk.jpg",
        "trailer_id": "https://www.youtube.com/embed/M_OauHnAFc4",
        "overview": "Devasa surların ardında yaşayan insanlık, insan yiyen Titanlara karşı ölüm kalım savaşı verir.",
    },
    {
        "id": 111,
        "title": "Jujutsu Kaisen",
        "year": 2025,
        "rating": 8.6,
        "category": "Anime",
        "quality": "1080p",
        "lang": "Türkçe Altyazı",
        "poster": "https://image.tmdb.org/t/p/w500/hUzeosd33nzE5MCNsZxCGEKTXaQ.jpg",
        "trailer_id": "https://www.youtube.com/embed/vHDdoSkKwXE",
        "overview": "Lanetli bir tılsımı yutan Yuji Itadori, lanetlerle savaşan büyücüler okuluna katılır.",
    },
    {
        "id": 112,
        "title": "Demon Slayer",
        "year": 2025,
        "rating": 8.7,
        "category": "Anime",
        "quality": "4K UHD",
        "lang": "Türkçe Altyazı",
        "poster": "https://image.tmdb.org/t/p/w500/xUfRZu2mi8bH6SzQj1Qylb0vqaA.jpg",
        "trailer_id": "https://www.youtube.com/embed/VQGCw1Bs4KA",
        "overview": "Ailesi iblisler tarafından katledilen Tanjiro, iblise dönüşen kız kardeşini kurtarmak için yola çıkar.",
    },
    {
        "id": 113,
        "title": "Dune: Çöl Gezegeni Bölüm İki",
        "year": 2025,
        "rating": 8.5,
        "category": "Yeni Çıkanlar",
        "quality": "4K UHD",
        "lang": "Türkçe Dublaj & Altyazı",
        "poster": "https://image.tmdb.org/t/p/w500/8b8R8l88Qje9dn9OE8PY05Nxl1X.jpg",
        "trailer_id": "https://www.youtube.com/embed/Way9Dexny3w",
        "overview": "Paul Atreides, ailesini yok eden komploculardan intikam almak için Fremenlerle birleşir.",
    },
    {
        "id": 114,
        "title": "Oppenheimer",
        "year": 2024,
        "rating": 8.3,
        "category": "Yeni Çıkanlar",
        "quality": "4K UHD",
        "lang": "Türkçe Dublaj & Altyazı",
        "poster": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
        "trailer_id": "https://www.youtube.com/embed/uYPbbksJxIg",
        "overview": "Atom bombasının geliştirilme sürecinde başrol oynayan fizikçi J. Robert Oppenheimer'ın hikayesi.",
    }
]

def generate_catalog():
    items = []
    categories = ["Netflix", "Disney+", "DC/Marvel", "Animasyon", "Anime", "Yeni Çıkanlar"]
    suffixes = ["", " - Sezon 2", ": Özel Seri", " (Director's Cut)"]
    idx = 1
    for suffix in suffixes:
        for base in BASE_CATALOG:
            item = base.copy()
            item["id"] = idx
            item["title"] = f"{base['title']}{suffix}" if suffix else base['title']
            if suffix:
                item["category"] = random.choice(categories)
                item["rating"] = round(random.uniform(7.2, 9.2), 1)
            item["link"] = f"https://multiembed.mov/?video_id=tt{1000000 + idx}&tmdb=1"
            items.append(item)
            idx += 1
    return items

MOVIES_DB = generate_catalog()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medusa Movies - Hdfilmcehennemi Tarzı</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-dark: #121212;
            --bg-elevated: #1a1a1a;
            --bg-card: #1e1e1e;
            --accent: #e50914;
            --text-main: #ffffff;
            --text-muted: #aaaaaa;
            --border: #2a2a2a;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: var(--bg-dark); color: var(--text-main); font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; padding-bottom: 75px; }
        
        /* HEADER & SEARCH */
        .header { background: var(--bg-elevated); padding: 12px 16px; border-bottom: 2px solid var(--accent); display: flex; flex-direction: column; gap: 10px; position: sticky; top: 0; z-index: 100; }
        .header-top { display: flex; justify-content: space-between; align-items: center; }
        .logo { color: var(--accent); font-size: 1.3rem; font-weight: 800; text-decoration: none; display: flex; align-items: center; gap: 6px; }
        .search-box { position: relative; width: 100%; }
        .search-box input { width: 100%; background: #262626; border: 1px solid var(--border); padding: 9px 14px 9px 38px; border-radius: 20px; color: #fff; font-size: 0.9rem; outline: none; }
        .search-box i { position: absolute; left: 13px; top: 50%; transform: translateY(-50%); color: var(--text-muted); font-size: 0.9rem; }

        /* KATEGORİ ÇUBUĞU */
        .filter-bar { display: flex; gap: 8px; padding: 10px 16px; background: #181818; overflow-x: auto; white-space: nowrap; scrollbar-width: none; border-bottom: 1px solid var(--border); }
        .filter-bar::-webkit-scrollbar { display: none; }
        .cat-pill { background: #262626; color: var(--text-muted); border: none; padding: 6px 14px; border-radius: 16px; font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: 0.2s; }
        .cat-pill.active { background: var(--accent); color: #fff; }

        /* İÇERİK ALANI */
        .container { padding: 12px 16px; }
        .section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; font-size: 0.95rem; font-weight: 700; color: #ddd; }
        
        .movie-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
        @media(min-width: 600px) { .movie-grid { grid-template-columns: repeat(4, 1fr); } }

        .movie-card { background: var(--bg-card); border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; border: 1px solid var(--border); box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        .poster-wrapper { position: relative; width: 100%; height: 210px; background: #000; overflow: hidden; }
        .poster-wrapper img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s; }
        .movie-card:hover img { transform: scale(1.03); }
        
        .badge-top-left { position: absolute; top: 6px; left: 6px; background: rgba(0,0,0,0.75); backdrop-filter: blur(4px); color: #f1c40f; padding: 2px 6px; font-size: 0.7rem; font-weight: bold; border-radius: 4px; display: flex; align-items: center; gap: 3px; }
        .badge-top-right { position: absolute; top: 6px; right: 6px; background: var(--accent); color: #fff; padding: 2px 5px; font-size: 0.65rem; font-weight: bold; border-radius: 4px; }
        .badge-bottom { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.9), transparent); padding: 8px 6px 4px; display: flex; justify-content: space-between; font-size: 0.68rem; color: #ccc; }

        .card-body { padding: 8px; display: flex; flex-direction: column; gap: 6px; flex-grow: 1; justify-content: space-between; }
        .movie-title { font-size: 0.85rem; font-weight: bold; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .movie-meta { font-size: 0.7rem; color: var(--text-muted); }
        
        .card-actions { display: flex; gap: 4px; margin-top: 4px; }
        .btn { flex: 1; padding: 6px 0; border: none; border-radius: 4px; font-size: 0.72rem; font-weight: bold; cursor: pointer; text-align: center; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 4px; }
        .btn-watch { background: var(--accent); color: #fff; }
        .btn-trailer { background: #2a2a2a; color: #ddd; }

        .load-more-wrap { text-align: center; margin: 20px 0; }
        .load-more-btn { background: #262626; color: #fff; border: 1px solid var(--border); padding: 10px 24px; border-radius: 20px; font-size: 0.85rem; font-weight: bold; cursor: pointer; }
        .load-more-btn:hover { background: var(--accent); border-color: var(--accent); }

        /* MODAL (FRAGMAN) */
        .modal { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.85); backdrop-filter: blur(5px); z-index: 1000; justify-content: center; align-items: center; padding: 15px; }
        .modal.open { display: flex; }
        .modal-content { background: var(--bg-elevated); width: 100%; max-width: 500px; border-radius: 10px; overflow: hidden; border: 1px solid var(--border); }
        .modal-header { display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: #181818; border-bottom: 1px solid var(--border); }
        .modal-title { font-size: 0.9rem; font-weight: bold; }
        .modal-close { background: none; border: none; color: #fff; font-size: 1.1rem; cursor: pointer; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: #333; }
        
        .video-container { position: relative; padding-bottom: 56.25%; height: 0; background: #000; }
        .video-container iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }
        .modal-info { padding: 12px; font-size: 0.8rem; color: var(--text-muted); line-height: 1.4; }

        /* ALT MENÜ */
        .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; height: 60px; background: #161616; border-top: 1px solid var(--border); display: flex; justify-content: space-around; align-items: center; z-index: 500; }
        .nav-item { background: none; border: none; color: var(--text-muted); display: flex; flex-direction: column; align-items: center; gap: 3px; font-size: 0.7rem; font-weight: 600; cursor: pointer; text-decoration: none; }
        .nav-item i { font-size: 1.1rem; }
        .nav-item.active, .nav-item:hover { color: var(--accent); }
    </style>
</head>
<body>

    <div class="header">
        <div class="header-top">
            <a href="/" class="logo"><i class="fa-solid fa-fire"></i> medusafilm</a>
        </div>
        <div class="search-box">
            <i class="fa-solid fa-search"></i>
            <input type="text" id="searchInput" placeholder="Film, dizi veya anime ara..." oninput="handleSearch()">
        </div>
    </div>

    <div class="filter-bar">
        <button class="cat-pill active" onclick="selectCategory('Tümü', this)">Tümü</button>
        <button class="cat-pill" onclick="selectCategory('Netflix', this)" data-cat="Netflix">Netflix</button>
        <button class="cat-pill" onclick="selectCategory('Disney+', this)" data-cat="Disney+">Disney+</button>
        <button class="cat-pill" onclick="selectCategory('DC/Marvel', this)" data-cat="DC/Marvel">DC / Marvel</button>
        <button class="cat-pill" onclick="selectCategory('Animasyon', this)" data-cat="Animasyon">Animasyon</button>
        <button class="cat-pill" onclick="selectCategory('Anime', this)" data-cat="Anime">Anime</button>
        <button class="cat-pill" onclick="selectCategory('Yeni Çıkanlar', this)" data-cat="Yeni Çıkanlar">Yeni Çıkanlar</button>
    </div>

    <div class="container">
        <div class="section-header">
            <span id="sectionTitle">Tüm Filmler ve Diziler</span>
            <span id="resultCount" style="color:var(--accent); font-size:0.8rem;">0 içerik</span>
        </div>

        <div class="movie-grid" id="movieGrid"></div>

        <div class="load-more-wrap" id="loadMoreWrap" style="display:none;">
            <button class="load-more-btn" onclick="loadMore()">Daha Fazla İçerik Göster</button>
        </div>
    </div>

    <!-- MODAL -->
    <div id="videoModal" class="modal" onclick="closeModalOnBg(event)">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title" id="modalMovieTitle">Film Başlığı</div>
                <button class="modal-close" onclick="closeModal()">&times;</button>
            </div>
            <div class="video-container">
                <iframe id="youtubePlayer" src="" allowfullscreen allow="autoplay"></iframe>
            </div>
            <div class="modal-info" id="modalOverview">Açıklama alanı...</div>
        </div>
    </div>

    <div class="bottom-nav">
        <a href="/" class="nav-item active" onclick="navAction('home', this); return false;"><i class="fa-solid fa-house"></i> Anasayfa</a>
        <a href="#" class="nav-item" onclick="navAction('trend', this); return false;"><i class="fa-solid fa-fire"></i> Trendler</a>
        <a href="#" class="nav-item" onclick="navAction('new', this); return false;"><i class="fa-solid fa-sparkles"></i> Yeni</a>
        <a href="#" class="nav-item" onclick="navAction('favorites', this); return false;"><i class="fa-solid fa-bookmark"></i> Listem</a>
    </div>

    <script>
        let currentCategory = 'Tümü';
        let currentSearch = '';
        let currentPage = 1;
        let onlyHighRated = false;
        let onlyFavorites = false;
        let favorites = JSON.parse(localStorage.getItem('hdf_favs') || '[]');

        async function fetchMovies(append = false) {
            if (!append) currentPage = 1;
            const params = new URLSearchParams({
                category: currentCategory,
                q: currentSearch,
                page: currentPage,
                trend: onlyHighRated ? '1' : '0'
            });
            const res = await fetch(`/api/movies?${params.toString()}`);
            const data = await res.json();
            let items = data.items;
            
            if (onlyFavorites) {
                items = items.filter(m => favorites.includes(m.id));
            }

            const grid = document.getElementById('movieGrid');
            if (!append) grid.innerHTML = '';
            
            document.getElementById('resultCount.innerText = `${onlyFavorites ? items.length : data.total} içerik`;

            items.forEach(movie => {
                const card = document.createElement('div');
                card.className = 'movie-card';
                card.innerHTML = `
                    <div class="poster-wrapper">
                        <img src="${movie.poster}" alt="${movie.title}" loading="lazy">
                        <div class="badge-top-left"><i class="fa-solid fa-star"></i> ${movie.rating}</div>
                        <div class="badge-top-right">${movie.quality}</div>
                        <div class="badge-bottom">
                            <span>${movie.year}</span>
                            <span>${movie.category}</span>
                        </div>
                    </div>
                    <div class="card-body">
                        <div>
                            <div class="movie-title" title="${movie.title}">${movie.title}</div>
                            <div class="movie-meta">${movie.lang}</div>
                        </div>
                        <div class="card-actions">
                            <a href="${movie.link}" class="btn btn-watch" target="_blank"><i class="fa-solid fa-play"></i> Türkçe İzle</a>
                            <button class="btn btn-trailer" onclick='openPlayer(${JSON.stringify(movie)})'><i class="fa-brands fa-yo
