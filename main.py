from flask import Flask, redirect
import requests, re, os

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ IPTV yönlendirme aktif!<br>Oynatıcı linki: <a href='/live'>/live</a>"

@app.route('/live')
def live():
    # Kaynak sayfadan tokenli linki çek
    source_url = "https://catcast.tv/player/49918"
    response = requests.get(source_url, timeout=10)
    match = re.search(r'https://s\.catcast\.tv/content/49918/index\.m3u8\?token=[a-zA-Z0-9]+', response.text)
    
    if match:
        token_url = match.group(0)
        return redirect(token_url, code=302)
    else:
        return "❌ Token bulunamadı", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
