from flask import Flask
import requests

app = Flask(__name__)

PLAYER_PAGE = "https://catcast.tv/tv-zle"

@app.route('/')
def index():
    return f"Token servisi aktif ✅<br>Sayfa: <a href='{PLAYER_PAGE}'>{PLAYER_PAGE}</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
