<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medusa Movies</title>
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            padding-bottom: 70px;
        }
        /* Üst Header */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 15px;
            background-color: #161616;
            border-bottom: 2px solid #e50914;
        }
        .logo {
            color: #e50914;
            font-size: 20px;
            font-weight: bold;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .header-icons {
            display: flex;
            gap: 15px;
            font-size: 18px;
            cursor: pointer;
        }
        /* Bölüm Başlıkları */
        .section-title {
            padding: 15px 15px 10px 15px;
            font-size: 15px;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: #fff;
        }
        .section-title span {
            color: #888;
            font-size: 12px;
            cursor: pointer;
        }
        /* Yakında Gelecekler Yuvarlak Alanı (Hikaye Tarzı) */
        .upcoming-container {
            display: flex;
            overflow-x: auto;
            padding: 0 15px 10px 15px;
            gap: 12px;
            scrollbar-width: none;
        }
        .upcoming-container::-webkit-scrollbar {
            display: none;
        }
        .upcoming-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            flex-shrink: 0;
            width: 70px;
            text-align: center;
        }
        .upcoming-circle {
            width: 65px;
            height: 65px;
            border-radius: 50%;
            border: 2px solid #e50914;
            overflow: hidden;
            position: relative;
            background: #222;
        }
        .upcoming-circle img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .upcoming-date {
            position: absolute;
            bottom: 0;
            background: rgba(229, 9, 20, 0.9);
            color: white;
            font-size: 8px;
            width: 100%;
            text-align: center;
            font-weight: bold;
            padding: 1px 0;
        }
        .upcoming-name {
            font-size: 11px;
            margin-top: 5px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            width: 100%;
            color: #ccc;
        }
        /* Popüler Filmler Grid Tasarımı */
        .movies-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            padding: 0 15px;
        }
        .movie-card {
            background-color: #1a1a1a;
            border-radius: 8px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0,0,0,0.4);
            transition: transform 0.2s;
        }
        .movie-card:active {
            transform: scale(0.97);
        }
        .movie-poster-container {
            position: relative;
            width: 100%;
            height: 210px;
            background-color: #222;
        }
        .movie-poster {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .movie-badge-dub {
            position: absolute;
            bottom: 8px;
            left: 8px;
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid #e50914;
            color: white;
            font-size: 9px;
            padding: 2px 5px;
            border-radius: 4px;
            font-weight: bold;
        }
        .movie-info {
            padding: 10px;
        }
        .movie-name {
            font-size: 13px;
            font-weight: bold;
            color: #fff;
            margin-bottom: 4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .movie-meta-row {
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: #888;
        }
        .movie-rating {
            color: #f1c40f;
            font-weight: bold;
        }
        /* Sabit Alt Menü Çubuğu */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #161616;
            display: flex;
            justify-content: space-around;
            padding: 10px 0;
            border-top: 1px solid #222;
            z-index: 1000;
        }
        .nav-item {
            color: #888;
            text-decoration: none;
            font-size: 11px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 3px;
        }
        .nav-item.active {
            color: #ffffff;
        }
        .nav-item span {
            font-size: 18px;
        }
    </style>
</head>
<body>

    <!-- Ü
