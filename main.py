from flask import Flask, redirect
import requests, re, os

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ IPTV yönlendirme aktif!<br>Oynatıcı linki: <a href='/live'>/live</a>"

@app.route('/live')
def live():
    try:
        # Catcast player sayfasını çek
        player_url = "https://catcast.tv/player/49918"
        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get(player_url, headers=headers, timeout=10).text

        # m3u8 linkini HTML içinden yakala
        match = re.search(r'(https://s\.catcast\.tv/content/\d+/index\.m3u8\?token=[a-zA-Z0-9]+)', html)
        if not match:
            return "❌ Token bulunamadı.", 500

        token_url = match.group(1)
        return redirect(token_url, code=302)

    except Exception as e:
        return f"⚠️ Hata: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
