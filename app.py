import os
import threading
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

YAYIN_KEY = os.environ.get("YAYIN_KEY", "")
_ylock = threading.Lock()
YAYIN = {
    "v": 0,
    "title": "MEDUSA • YAYIN",
    "stream": "",
    "alert": "",
    "alert_id": 0,
    "ttl": 8,
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/trending")
def api_trending():
    if not TMDB_API_KEY:
        return jsonify({"error": "TMDB_API_KEY tanımlı değil", "results": []}), 200
    try:
        r = requests.get(
            f"{TMDB_BASE_URL}/trending/all/week",
            params={"api_key": TMDB_API_KEY, "language": "tr-TR"},
            timeout=10,
        )
        r.raise_for_status()
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e), "results": []}), 500


@app.route("/api/search")
def api_search():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"results": []})
    if not TMDB_API_KEY:
        return jsonify({"error": "TMDB_API_KEY tanımlı değil", "results": []}), 200
    try:
        r = requests.get(
            f"{TMDB_BASE_URL}/search/multi",
            params={"api_key": TMDB_API_KEY, "language": "tr-TR", "query": q},
            timeout=10,
        )
        r.raise_for_status()
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e), "results": []}), 500


@app.route("/yayin")
def yayin():
    return render_template("yayin.html")


@app.route("/api/yayin/state", methods=["GET"])
def yayin_get():
    since = request.args.get("v", type=int)
    with _ylock:
        if since is not None and since == YAYIN["v"]:
            return jsonify({"v": YAYIN["v"], "changed": False})
        return jsonify({**YAYIN, "changed": True})


@app.route("/api/yayin/state", methods=["POST"])
def yayin_set():
    data = request.get_json(silent=True) or {}
    key = request.headers.get("X-Key", "") or data.get("key", "")
    if not YAYIN_KEY or key != YAYIN_KEY:
        return jsonify({"error": "yetkisiz"}), 403
    with _ylock:
        if "title" in data:
            YAYIN["title"] = str(data["title"])[:80]
        if "stream" in data:
            s = str(data["stream"]).strip()[:1000]
            YAYIN["stream"] = s if s.startswith(("http://", "https://")) or s == "" else ""
        if data.get("alert"):
            YAYIN["alert"] = str(data["alert"])[:200]
            YAYIN["ttl"] = max(2, min(int(data.get("ttl", 8)), 60))
            YAYIN["alert_id"] += 1
        if data.get("clear_alert"):
            YAYIN["alert"] = ""
            YAYIN["alert_id"] += 1
        YAYIN["v"] += 1
        return jsonify({**YAYIN, "changed": True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
