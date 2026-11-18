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
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .container {
            width: 100%;
            max-width: 800px;
            padding: 15px;
        }
        .header-back {
            color: #ff4500;
            text-decoration: none;
            font-weight: bold;
            margin-bottom: 15px;
            display: inline-block;
        }
        /* Sunucu Seçim Butonları Alanı */
        .server-tabs {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 15px;
        }
        .server-btn {
            background-color: #1f1f1f;
            color: #fff;
            border: none;
            padding: 12px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            text-align: center;
            transition: 0.3s;
        }
        .server-btn.active {
            background-color: #ff4500;
            color: #fff;
        }
        .player-container {
            position: relative;
            width: 100%;
            background: #000;
            border-radius: 8px;
            overflow: hidden;
            aspect-ratio: 16/9;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .warning-text {
            color: #888;
            font-size: 13px;
            margin-top: 10px;
            text-align: center;
        }
        .movie-info {
            margin-top: 20px;
        }
        .movie-title {
            color: #ff4500;
            font-size: 24px;
            font-weight: bold;
        }
        .movie-meta {
            color: #f1c40f;
            font-size: 15px;
            margin-top: 5px;
        }
        .movie-overview {
            color: #ccc;
            font-size: 14px;
            line-height: 1.6;
            margin-top: 10px;
        }
    </style>
</head>
<body>

    <div class="container">
        <!-- Ana Sayfaya Dön Butonu -->
        <a href="/" class="header-back">← Ana Sayfaya Dön</a>

        <!-- Sunucu Seçenekleri (Server 1, Server 2, Multiembed, Fragman) -->
        <div class="server-tabs">
            <button class="server-btn active" onclick="changeServer('server1', this)">🎬 Server 1</button>
            <button class="server-btn" onclick="changeServer('server2', this)">⚡ Server 2</button>
            <button class="server-btn" onclick="changeServer('multiembed', this)">🔥 Multiembed</button>
            <button class="server-btn" onclick="changeServer('fragman', this)">🍿 Fragman</button>
        </div>

        <!-- Video Oynatıcı Alanı -->
        <div class="player-container">
            <iframe id="moviePlayer" src="" width="100%" height="100%" frameborder="0" allowfullscreen></iframe>
        </div>

        <div class="warning-text">
            * Server 1 hata verirse yukarıdan hemen Server 2 veya Multiembed'e geçiş yapabilirsin kanka.
        </div>

        <!-- Film Detayları -->
        <div class="movie-info">
            <div class="movie-title">Vahşinin Kalbi</div>
            <div class="movie-meta">
                <span>📅 2026-09-19</span> &nbsp;&nbsp;|&nbsp;&nbsp; <span>⭐️ 7.7 / 10</span>
            </div>
            <div class="movie-overview">
                <strong>Özet:</strong> Özel Kuvvetler subayı James Belmont, içinde bulunduğu uçağın Alaska'nın zorlu coğrafyasına düşmesi sonucu hayatta kalmayı başarır. Yanında sadece eğitimli savaş köpeği Odin bulunan Belmont; dondurucu soğuklar, vahşi doğa şartları ve sınırlı kaynaklarla karşı karşıya kalır. Medeniyetten tamamen uzakta mahsur kalan iki kişi, bir yandan bölgenin çetin iklim koşullarına ve yırtıcılara karşı direnirken...
            </div>
        </div>
    </div>

    <script>
        // Farklı sunucu kaynak linkleri (Film ID'sine göre dinamik bağlanabilir)
        const movieId = "{{ movie_id }}"; // Flask'ten gelen ID
        
        const servers = {
            "server1": "https://multiembed.mov/?video_id=" + movieId,
            "server2": "https://vidsrc.xyz/embed/movie?imdb=" + movieId,
            "multiembed": "https://multiembed.mov/?video_id=" + movieId + "&player=2",
            "fragman": "https://www.youtube.com/embed/dQw4w9WgXcQ" // Örnek fragman linki
        };

        // Sayfa açıldığında ilk server'ı yükle
        document.getElementById('moviePlayer').src = servers["server1"];

        function changeServer(serverName, buttonElement) {
            // Aktif buton stilini değiştir
            document.querySelectorAll('.server-btn').forEach(btn => btn.classList.remove('active'));
            buttonElement.classList.add('active');

            // Iframe kaynağını seçilen sunucuya göre güncelle
            document.getElementById('moviePlayer').src = servers[serverName];
        }
    </script>
</body>
</html>
