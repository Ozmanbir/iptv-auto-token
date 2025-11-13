from flask import Flask, redirect
import requests, re, os

app = Flask(__name__)

@app.route('/')
def index():
    return """
    ✅ Otomatik IPTV Token Sistemi Çalışıyor<br><br>
    Örnek Kullanım:<br>
    <a href='/live/49918'>Kanal 49918</a><br>
    <a href='/live/49324'>Kanal 49324</a><br><br>
    /live/<id> şeklinde istediğin Catcast ID'yi yaz.
    """

@app.route('/live/<channel_id>')
def live(channel_id):
    try:
        # Catcast'teki oynatıcı sayfasını çek
        page_url = f"https://catcast.tv/player/{channel_id}"
        r = requests.get(page_url, timeout=10)
        html = r.text

        # Token'i HTML içinde yakala (32 karakterlik hex token)
        match = re.search(r'token=[a-f0-9]{32}', html)
        if not match:
            return f"❌ Token bulunamadı (ID: {channel_id})", 404

        token = match.group(0)
        m3u8_url = f"https://s.catcast.tv/content/{channel_id}/index.m3u8?{token}"

        # Tokenli linke yönlendir
        return redirect(m3u8_url, code=302)

    except Exception as e:
        return f"❌ Hata oluştu: {e}", 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
