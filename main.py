from flask import Flask, redirect
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ IPTV yönlendirme aktif!<br>Oynatıcı linki: <a href='/live'>/live</a>"

@app.route('/live')
def live():
    token_url = "https://s.catcast.tv/content/49918/index.m3u8?token=a04dd2e40849ea7db675bd8040f6e409"
    return redirect(token_url, code=302)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
