import random
import requests
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# İSTEĞE BAĞLI: Ücretsiz TMDB API anahtarınızı buraya yazarsanız yüzlerce güncel içerik otomatik çekilir.
# Boş bırakırsanız aşağıdaki zengin yerleşik katalog çalışır.
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
        "poster": "https://tmdb.org",
        "trailer_id": "b9EkMc79ZSU",
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
        "poster": "https://tmdb.org",
        "trailer_id": "ndl1W4ltcmg",
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
        "poster": "https://tmdb.org",
        "trailer_id": "aOC8E8z_ifw",
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
        "poster": "https://tmdb.org",
        "trailer_id": "nW948Va-l10",
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
        "poster": "https://tmdb.org",
        "trailer_id": "mqqft2x_Aa4",
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
        "poster": "https://tmdb.org",
        "trailer_id": "TcMBFSGVi1c",
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
        "poster": "https://tmdb.org",
        "trailer_id": "73_1biulkYk",
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
        "poster": "https://tmdb.org",
        "trailer_id": "cqGjhVJWtEg",
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
        "poster": "https://tmdb.org",
        "trailer_id": "LEjhY15eCx0",
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
        "poster": "https://tmdb.org",
        "trailer_id": "MGRm4IzK1SQ",
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
        "poster": "https://tmdb.org",
        "trailer_id": "4A_X-Dvl0ws",
        "overview": "Lanetli bir tılsımı yutan Yuji Itadori, lanetlerle savaşan büyücüler okuluna katılır.",
    },
    {
        "id": 112,
        "title": "Demon Slayer: Kimetsu no Yaiba",
        "year": 2025,
        "rating": 8.7,
        "category": "Anime",
        "quality": "4K UHD",
        "lang": "Türkçe Altyazı",
        "poster": "https://tmdb.org",
        "trailer_id": "VQGCKyvzIM4",
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
        "poster": "https://tmdb.org",
        "trailer_id": "Way9Dexny3w",
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
        "poster": "https://tmdb.org",
        "trailer_id": "uYPbbksJxIg",
        "overview": "Atom bombasının geliştirilme sürecinde başrol oynayan fizikçi J. Robert Oppenheimer'ın hikayesi.",
    },
    {
        "id": 115,
        "title": "Arcane",
        "year": 2025,
        "rating": 9.0,
        "category": "Netflix",
        "quality": "4K UHD",
        "lang": "Türkçe Dublaj & Altyazı",
        "poster": "https://tmdb.org",
        "trailer_id": "fXmAurh012s",
        "overview": "Ütopik Piltover ile yeraltı şehri Zaun arasındaki gerilim iki kız kardeşi karşı karşıya getirir.",
    },
    {
        "id": 116,
        "title": "Joker: İkili Delilik",
        "year": 2025,
        "rating": 7.4,
        "category": "Yeni Çıkanlar",
        "quality": "1080p",
        "lang": "Türkçe Dublaj",
        "poster": "https://tmdb.org",
        "trailer_id": "_OKAwz2MsJs",
        "overview": "Arkham Akıl Hastanesi'nde yargılanmayı bekleyen Arthur Fleck, gerçek aşkı ve içindeki müziği bulur.",
    },
]


def generate_hundreds_of_items():
    """Statik kataloğu çoğaltarak 200'den fazla içeriklik akıcı bir kütüphane oluşturur."""
    items = []
    categories = [
        "Netflix",
        "Disney+",
        "DC/Marvel",
        "Animasyon",
        "Anime",
        "Yeni Çıkanlar",
    ]
    years = [2022, 2023, 2024, 2025, 2026]
    suffixes = [
        "",
        " - Özel Bölüm",
        ": Yeniden Doğuş",
        " 2",
        ": Karanlık Yükseliş",
        ": Son Savaş",
        " (Director's Cut)",
        ": Yeni Çağ",
        ": Kayıp Efsane",
        ": Kırılma Noktası",
        ": Gölge Operasyonu",
        ": Sonsuzluk",
        ": Başlangıç",
        " III",
    ]

    idx = 1
    for suffix in suffixes:
        for base in BASE_CATALOG:
            item = base.copy()
            item["id"] = idx
            item["title"] = f"{base['title']}{suffix}"
            if suffix != "":
                item["category"] = random.choice(categories)
                item["year"] = random.choice(years)
                item["rating"] = round(random.uniform(7.1, 9.4), 1)
            items.append(item)
            idx += 1
    return items


def fetch_tmdb_catalog():
    """TMDB API anahtarı tanımlıysa gerçek verileri çeker, aksi halde yüzlerce statik içeriği döner."""
    if not TMDB_API_KEY:
        return generate_hundreds_of_items()

    catalog = []
    endpoints = [
        ("Yeni Çıkanlar", "movie/now_playing"),
        ("Netflix", "discover/tv?with_networks=213"),
        ("Disney+", "discover/tv?with_networks=2739"),
        ("DC/Marvel", "discover/movie?with_keywords=9715"),
        ("Animasyon", "discover/movie?with_genres=16"),
        ("Anime", "discover/tv?with_genres=16&with_original_language=ja"),
    ]

    try:
        for cat_name, path in endpoints:
            sep = "&" if "?" in path else "?"
            for page in:
                url = f"https://themoviedb.org{path}{sep}api_key={TMDB_API_KEY}&language=tr-TR&page={page}"
                res = requests.get(url, timeout=4).json()
                for m in res.get("results", []):
                    if not m.get("poster_path"):
                        continue
                    title = m.get("title") or m.get("name")
                    date = m.get("release_date") or m.get("first_air_date") or "2025"
