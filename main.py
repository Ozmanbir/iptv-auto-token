from flask import Flask, redirect
import os

app = Flask(__name__)

@app.route('/')
def index():
    return """
    ✅ IPTV yönlendirme aktif!<br><br>
    🔹 <a href='/live'>/live</a><br>
    🔹 <a href='/live2'>/live2</a>
    """

# 1. yayın
@app.route('/live')
def live():
    token_url = "https://s.catcast.tv/content/49918/index.m3u8?token=b13e2ae89c49fb4132e0622f19419604"
    return redirect(token_url, code=302)

# 2. yayın
@app.route('/live2')
def live2():
    token_url = "https://dc34a9483e0f144e9e.pages.dev/cefc8a875b06cc6da16ca7dd99157dee/DmodYM9CdSNPUZyc2x7VWd/5062/dc34a9483e0f144e9e.pages.dev/chunklist_hd.m3u8?verify=1763016750936~213.238.187.84~bd14cdaa057f57353a74ee68d0a7a394"
    return redirect(token_url, code=302)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
