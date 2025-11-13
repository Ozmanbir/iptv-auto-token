import re
import requests
from flask import Flask, Response

app = Flask(__name__)

@app.route("/list.m3u")
def serve_m3u():
    try:
        # Catcast player sayfası
        url = "https://catcast.tv/player/49918"
        html = requests.get(url, timeout=10).text

        # Token yakalama
        match = re.search(r'token=([a-f0-9]{32})', html)
        if not match:
            return Response("# Token bulunamadı", mimetype="audio/mpegurl")

        token = match.group(1)
        stream_url = f"https://s.catcast.tv/content/49918/index.m3u8?token={token}"

        # M3U içeriği oluştur
        m3u_content = f"#EXTM3U\n#EXTINF:-1, tv-izle\n{stream_url}\n"
        return Response(m3u_content, mimetype="audio/mpegurl")

    except Exception as e:
        return Response(f"# Hata: {e}", mimetype="audio/mpegurl")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
