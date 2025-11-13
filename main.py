from flask import Flask, redirect, Response
import requests, re, os

app = Flask(__name__)

def fetch_token_url():
    """Catcast player sayfasından güncel tokenli .m3u8 URL'si çek"""
    player_url = "https://catcast.tv/player/49918"
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://catcast.tv"}
    r = requests.get(player_url, headers=headers, timeout=10)
    if r.status_code != 200:
        raise Exception(f"Player sayfası {r.status_code} döndürdü")
    
    html = r.text
    # index.m3u8 veya chunklist.m3u8 içeren tokenli bağlantıyı yakala
    m = re.search(r'(https://[^\s"\']+?\.m3u8\?token=[A-Za-z0-9]+)', html)
    if not m:
        raise Exception("Tokenli m3u8 bağlantısı bulunamadı")
    return m.group(1)

@app.route('/')
def index():
    return "✅ IPTV yönlendirme aktif!<br>Oynatıcı linki: <a href='/live'>/live</a>"

@app.route('/live')
def live():
    try:
        token_url = fetch_token_url()
        return redirect(token_url, code=302)
    except Exception as e:
        return Response(f"❌ Token alınamadı: {e}", mimetype="text/plain")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
