import os
import json
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

PLATFORM_CONFIG = {
    "site_name": "MEDUSAFILM",
    "license_code": "MEDUSA-PRO-2026-APPROVED",
    "license_status": "ONAYLI / AKTIF",
    "owner_approval": True
}

SAMPLE_VIDEO_1 = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
SAMPLE_VIDEO_2 = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4"
SAMPLE_VIDEO_3 = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4"
SAMPLE_VIDEO_4 = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"

CATALOG = [
    {
        "id": 101,
        "title": "Big Buck Bunny",
        "category": "Animasyon",
        "year": "2026",
        "quality": "1080p HD",
        "audio": "Onaylı Ses",
        "license_tag": "LISANS-ONAY-01",
        "approved": True,
        "poster": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Big_buck_bunny_poster_big.jpg/480px-Big_buck_bunny_poster_big.jpg",
        "glow": "#00e5ff",
        "video_url": SAMPLE_VIDEO_1
    },
    {
        "id": 102,
        "title": "Sintel Özel Seçki",
        "category": "Animasyon",
        "year": "2026",
        "quality": "1080p HD",
        "audio": "Onaylı Ses",
        "license_tag": "LISANS-ONAY-02",
        "approved": True,
        "poster": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Sintel_poster.jpg/480px-Sintel_poster.jpg",
        "glow": "#a855f7",
        "video_url": SAMPLE_VIDEO_2
    },
    {
        "id": 103,
        "title": "Tears of Steel",
        "category": "Filmler",
        "year": "2026",
        "quality": "4K / HD",
        "audio": "Onaylı Ses",
        "license_tag": "LISANS-ONAY-03",
        "approved": True,
        "poster": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Tears_of_Steel_poster.jpg/480px-Tears_of_Steel_poster.jpg",
        "glow": "#3b82f6",
        "video_url": SAMPLE_VIDEO_3
    },
    {
        "id": 104,
        "title": "Elephant's Dream Bölüm 1",
        "category": "Diziler",
        "year": "2026",
        "quality": "HD",
        "audio": "Onaylı Ses",
        "license_tag": "LISANS-ONAY-04",
        "approved": True,
        "poster": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Elephants_Dream_s5_both.jpg/480px-Elephants_Dream_s5_both.jpg",
        "glow": "#f59e0b",
        "video_url": SAMPLE_VIDEO_4
    },
    {
        "id": 105,
        "title": "Medusa Stüdyo Özel Yapım",
        "category": "Filmler",
        "year": "2026",
        "quality": "1080p HD",
        "audio": "Onaylı Ses",
        "license_tag": "LISANS-ONAY-05",
        "approved": True,
        "poster": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Big_buck_bunny_poster_big.jpg/480px-Big_buck_bunny_poster_big.jpg",
        "glow": "#ef4444",
        "video_url": SAMPLE_VIDEO_3
    },
    {
        "id": 106,
        "title": "Medusa Seri Arşivi",
        "category": "Diziler",
        "year": "2026",
        "quality": "1080p HD",
        "audio": "Onaylı Ses",
        "license_tag": "LISANS-ONAY-06",
        "approved": True,
        "poster": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Sintel_poster.jpg/480px-Sintel_poster.jpg",
        "glow": "#10b981",
        "video_url": SAMPLE_VIDEO_4
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>medusafilm — Lisanslı & Onaylı Platform</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --red: #E50914;
            --bg: #09090b;
            --card: #151519;
            --border: #27272a;
            --accent: #ff1e2d;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: var(--bg);
            color: #fff;
            font-family: Arial, sans-serif;
            padding-bottom: 78px;
            overflow-x: hidden;
        }
        .header {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 60px;
            background: rgba(9, 9, 11, 0.94);
            display: flex; align-items: center; justify-content: space-between;
            padding: 0 18px;
            z-index: 1000;
            border-bottom: 1px solid var(--accent);
        }
        .brand-group { display: flex; align-items: center; gap: 10px; }
        .logo {
            color: var(--red);
            font-size: 21px;
            font-weight: bold;
            text-decoration: none;
            font-family: Impact, sans-serif;
            letter-spacing: 0.5px;
        }
        .license-pill {
            background: rgba(22, 163, 74, 0.16);
            color: #4ade80;
            border: 1px solid rgba(74, 222, 128, 0.35);
            padding: 3px 8px;
            border-radius: 999px;
            font-size: 10px;
            font-weight: bold;
            cursor: pointer;
        }
        .icon-btn {
            background: none; border: none; color: #fff;
            font-size: 18px; cursor: pointer;
        }
        .search-bar {
            display: none;
            position: fixed;
            top: 60px; left: 0; width: 100%;
            padding: 12px 18px;
            background: rgba(9, 9, 11, 0.98);
            border-bottom: 1px solid var(--border);
            z-index: 999;
        }
        .search-bar input {
            width: 100%;
            background: #1c1c22;
            border: 1px solid #333;
            color: #fff;
            padding: 10px 14px;
            border-radius: 8px;
            font-size: 14px;
            outline: none;
        }
        .hero {
            margin-top: 60px;
            padding: 24px 18px;
            background: linear-gradient(155deg, rgba(229,9,20,0.22), rgba(9,9,11,0.96) 65%);
            border-bottom: 1px solid var(--border);
        }
        .hero-meta {
            display: flex; flex-wrap: wrap; gap: 8px;
            margin-bottom: 10px; font-size: 11px;
        }
        .tag {
            background: #1e1e24;
            border: 1px solid #32323a;
            padding: 4px 8px;
            border-radius: 5px;
            color: #e4e4e7;
        }
        .tag.ok {
            background: rgba(22, 163, 74, 0.18);
            border-color: rgba(74, 222, 128, 0.4);
            color: #86efac;
            font-weight: bold;
        }
        .hero-title { font-size: 24px; font-weight: bold; margin-bottom: 8px; }
        .hero-desc { font-size: 13px; color: #b4b4bc; margin-bottom: 14px; line-height: 1.45; }
        .hero-actions { display: flex; gap: 10px; flex-wrap: wrap; }
        .btn-primary {
            background: #fff; color: #000; border: none;
            padding: 10px 18px; border-radius: 6px;
            font-size: 13px; font-weight: bold; cursor: pointer;
            display: inline-flex; align-items: center; gap: 7px;
        }
        .btn-secondary {
            background: #1f1f26; color: #fff; border: 1px solid #383842;
            padding: 10px 14px; border-radius: 6px;
            font-size: 12px; font-weight: bold; cursor: pointer;
            display: inline-flex; align-items: center; gap: 7px;
        }
        .categories {
            display: flex; gap: 8px; padding: 14px 18px;
            overflow-x: auto; white-space: nowrap;
        }
        .cat-chip {
            background: rgba(255,255,255,0.08);
            color: #fff;
            border: 1px solid rgba(255,255,255,0.16);
            padding: 6px 14px; border-radius: 20px;
            font-size: 12px; cursor: pointer;
        }
        .cat-chip.active { background: #fff; color: #000; font-weight: bold; }
        .section { padding: 6px 18px 14px; }
        .section-title { font-size: 15px; font-weight: bold; margin-bottom: 12px; color: #f4f4f5; }
        .grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
        }
        @media(min-width: 640px) { .grid { grid-template-columns: repeat(5, 1fr); } }
        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
            display: flex; flex-direction: column;
            cursor: pointer;
        }
        .poster {
            width: 100%; height: 148px;
            object-fit: cover; background: #1e1e24; display: block;
        }
        .poster-fallback {
            width: 100%; height: 148px;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            padding: 10px; text-align: center;
            background: linear-gradient(155deg, #1e1e28, #0b0b0e);
            border-bottom: 2px solid var(--card-glow, var(--red));
        }
        .poster-fallback svg { width: 26px; height: 26px; margin-bottom: 6px; color: var(--card-glow, var(--red)); }
        .poster-fallback span { font-size: 11px; font-weight: bold; color: #f3f4f6; }
        .card-body { padding: 8px; }
        .card-title {
            font-size: 12px; font-weight: bold;
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
            margin-bottom: 4px;
        }
        .card-sub {
            font-size: 10px; color: #4ade80;
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
        }
        .modal {
            display: none; position: fixed; inset: 0;
            width: 100vw; height: 100dvh;
            background: #050507; z-index: 2000;
            flex-direction: column;
        }
        .modal-header {
            display: flex; align-items: center; justify-content: space-between;
            background: #0c0c10; border-bottom: 1px solid #222;
            padding: 8px 12px; height: 50px; gap: 8px;
        }
        .back-btn {
            background: var(--red); color: #fff; border: none;
            padding: 6px 12px; border-radius: 5px;
            font-size: 11px; font-weight: bold; cursor: pointer;
        }
        .modal-badge {
            background: #18181b; border: 1px solid #2e2e36;
            color: #4ade80; padding: 5px 10px; border-radius: 5px;
            font-size: 11px; font-weight: bold;
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
        }
        .player-wrap {
            flex: 1; width: 100%; height: calc(100dvh - 50px);
            display: flex; align-items: center; justify-content: center;
            background: #050507;
        }
        .player-wrap video { width: 100%; height: 100%; background: #000; }
        .info-panel {
            display: none; padding: 20px; max-width: 440px;
            background: #141418; border: 1px solid #2b2b33; border-radius: 10px;
            font-size: 13px; line-height: 1.6; color: #e4e4e7;
        }
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; width: 100%; height: 56px;
            background: rgba(12, 12, 15, 0.96);
            display: flex; justify-content: space-around; align-items: center;
            border-top: 1px solid var(--accent); z-index: 1000;
        }
        .nav-btn {
            background: none; border: none; color: #8c8c8c;
            font-size: 10px; display: flex; flex-direction: column; align-items: center; gap: 2px;
            cursor: pointer;
        }
        .nav-btn.active { color: #fff; }
        .nav-btn i { font-size: 16px; }
    </style>
</head>
<body>
    <header class="header">
        <div class="brand-group">
            <a href="/" class="logo">MEDUSAFILM</a>
            <button class="license-pill" onclick="openLicenseInfo()"><i class="fa-solid fa-shield-check"></i> ONAYLI</button>
        </div>
        <button class="icon-btn" onclick="toggleSearch()"><i class="fa-solid fa-magnifying-glass"></i></button>
    </header>

    <div class="search-bar" id="searchBar">
        <input type="text" id="searchInput" placeholder="Film, dizi veya animasyon ara..." oninput="handleSearch()">
    </div>

    <section class="hero">
        <div class="hero-meta">
            <span class="tag ok"><i class="fa-solid fa-check"></i> {{ config.license_status }}</span>
            <span class="tag">Kod: {{ config.license_code }}</span>
            <span class="tag">Tek Oynatıcı</span>
        </div>
        <div class="hero-title">Medusa Onaylı Yayın Merkezi</div>
        <div class="hero-desc">Kendi lisans anahtarın ve onay kaydınla çalışan film, dizi ve animasyon kataloğu tek ekranda.</div>
        <div class="hero-actions">
            <button class="btn-primary" onclick="openVideo('Big Buck Bunny', '{{ sample_video }}', 'LISANS-ONAY-01')">
                <i class="fa-solid fa-play"></i> Hemen Oynat
            </button>
            <button class="btn-secondary" onclick="openLicenseInfo()">
                <i class="fa-solid fa-certificate"></i> Lisans Detayı
            </button>
        </div>
    </section>

    <div class="categories">
        <button class="cat-chip active" onclick="setCategory('Tümü', this)">Tümü</button>
        <button class="cat-chip" onclick="setCategory('Filmler', this)">Filmler</button>
        <button class="cat-chip" onclick="setCategory('Diziler', this)">Diziler</button>
        <button class="cat-chip" onclick="setCategory('Animasyon', this)">Animasyon</button>
    </div>

    <section class="section">
        <div class="section-title" id="sectionTitle">Onaylı İçerik Kataloğu</div>
        <div class="grid" id="catalogGrid"></div>
    </section>

    <div class="modal" id="playerModal">
        <div class="modal-header">
            <button class="back-btn" onclick="closeModal()"><i class="fa-solid fa-arrow-left"></i> Geri</button>
            <span class="modal-badge" id="modalBadge">Onaylı Yayın</span>
        </div>
        <div class="player-wrap">
            <video id="videoPlayer" controls autoplay playsinline></video>
            <div class="info-panel" id="licensePanel">
                <div style="font-size: 16px; font-weight: bold; color: #4ade80; margin-bottom: 10px;">
                    <i class="fa-solid fa-shield-halved"></i> Platform Lisans & Onay Kaydı
                </div>
                <p><strong>Platform:</strong> {{ config.site_name }}</p>
                <p><strong>Lisans Kodu:</strong> {{ config.license_code }}</p>
                <p><strong>Durum:</strong> {{ config.license_status }}</p>
                <p style="margin-top: 10px; color: #a1a1aa;">
                    Katalogdaki içerikler onay bayrağı (<code>approved: True</code>) üzerinden kontrol edilir ve doğrudan oynatıcıya aktarılır.
                </p>
            </div>
        </div>
    </div>

    <nav class="bottom-nav">
        <button class="nav-btn active" onclick="navFilter('Tümü', this)"><i class="fa-solid fa-house"></i><span>Ana Sayfa</span></button>
        <button class="nav-btn" onclick="navFilter('Filmler', this)"><i class="fa-solid fa-film"></i><span>Filmler</span></button>
        <button class="nav-btn" onclick="navFilter('Diziler', this)"><i class="fa-solid fa-tv"></i><span>Diziler</span></button>
        <button class="nav-btn" onclick="navFilter('Animasyon', this)"><i class="fa-solid fa-wand-magic-sparkles"></i><span>Animasyon</span></button>
    </nav>

    <script>
        const ITEMS = {{ catalog_json | safe }};
        const DEFAULT_VIDEO = {{ sample_video_json | safe }};
        const SVG_ICON = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="2"/><line x1="7" y1="4" x2="7" y2="20"/><line x1="17" y1="4" x2="17" y2="20"/><line x1="3" y1="12" x2="21" y2="12"/></svg>`;

        let currentCat = 'Tümü';
        let queryText = '';

        function norm(s) {
            return String(s || '').toLowerCase()
                .replace(/ı/g, 'i').replace(/İ/g, 'i').replace(/ğ/g, 'g')
                .replace(/ü/g, 'u').replace(/ş/g, 's').replace(/ö/g, 'o').replace(/ç/g, 'c').trim();
        }

        function fallbackEl(title) {
            const d = document.createElement('div');
            d.className = 'poster-fallback';
            d.innerHTML = `${SVG_ICON}<span>${title}</span>`;
            return d;
        }

        function renderGrid() {
            const grid = document.getElementById('catalogGrid');
            grid.innerHTML = '';
            const q = norm(queryText);
            const list = ITEMS.filter(item => {
                if (!item.approved) return false;
                const catOk = (currentCat === 'Tümü' || item.category === currentCat);
                const qOk = !q || norm(item.title).includes(q) || norm(item.category).includes(q);
                return catOk && qOk;
            });

            if (list.length === 0) {
                grid.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; color: #9ca3af; padding: 28px; font-size: 13px;">Onaylı eşleşen içerik bulunamadı.</div>`;
                return;
            }

            list.forEach(item => {
                const card = document.createElement('div');
                card.className = 'card';
                card.style.setProperty('--card-glow', item.glow || '#E50914');
                card.onclick = () => openVideo(item.title, item.video_url || DEFAULT_VIDEO, item.license_tag || 'ONAYLI');

                const img = document.createElement('img');
                img.src = item.poster;
                img.className = 'poster';
                img.loading = 'lazy';
                img.onerror = function() { this.replaceWith(fallbackEl(item.title)); };

                const body = document.createElement('div');
                body.className = 'card-body';

                const title = document.createElement('div');
                title.className = 'card-title';
                title.textContent = item.title;

                const sub = document.createElement('div');
                sub.className = 'card-sub';
                sub.textContent = `${item.quality} • ${item.license_tag}`;

                body.appendChild(title);
                body.appendChild(sub);
                card.appendChild(img);
                card.appendChild(body);
                grid.appendChild(card);
            });
        }

        function setCategory(cat, btn) {
            currentCat = cat;
            document.querySelectorAll('.cat-chip').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            document.getElementById('sectionTitle').innerText = cat === 'Tümü' ? 'Onaylı İçerik Kataloğu' : `${cat} (Onaylı)`;
            renderGrid();
        }

        function navFilter(cat, btn) {
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            setCategory(cat, null);
            window.scrollTo({ top: 220, behavior: 'smooth' });
        }

        function toggleSearch() {
            const bar = document.getElementById('searchBar');
            bar.style.display = bar.style.display === 'block' ? 'none' : 'block';
            if (bar.style.display === 'block') document.getElementById('searchInput').focus();
        }

        function handleSearch() {
            queryText = document.getElementById('searchInput').value.trim();
            renderGrid();
        }

        function openVideo(title, url, tag) {
            const vid = document.getElementById('videoPlayer');
            const panel = document.getElementById('licensePanel');
            document.getElementById('modalBadge').textContent = `${title} • ${tag}`;
            document.getElementById('playerModal').style.display = 'flex';
            panel.style.display = 'none';
            vid.style.display = 'block';
            vid.src = url || DEFAULT_VIDEO;
    
