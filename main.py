from flask import Flask, redirect, Response
import requests, re, os

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ IPTV Otomatik Jeton sistemi aktif!<br>Yayın linki: <a href='/live'>/live</a>"

@app.route('/live')
def live():
    try:
        # Catcast sayfasını al
        url = "https://catcast.tv/player/49918"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        html = r.text

        # m3u8 linkini bul (örnek: https://s.catcast.tv/content/49918/index.m3u8?token=xxxx)
        match = re.search(r'https://s\.catcast\.tv/content/49918/index\.m3u8\?token=[a-zA-Z0-9]+', html)
        if match:
            token_url = match.group(0)
            return redirect(token_url, code=302)
        else:
            return Response("❌ Token bulunamadı. Catcast sayfası yapısını kontrol et.", status=500)
    except Exception as e:
        return Response(f"⚠️ Hata: {e}", status=500)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
