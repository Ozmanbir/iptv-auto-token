from flask import Flask
import requests
import os

app = Flask(__name__)

PLAYER_PAGE = "https://catcast.tv/tv-zle"

@app.route('/')
def index():
    return f"Token servisi aktif ✅<br>Sayfa: <a href='{PLAYER_PAGE}'>{PLAYER_PAGE}</a>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
