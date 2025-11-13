from flask import Flask, Response
import requests, re, os, time

app = Flask(__name__)
PLAYER_PAGE = "https://catcast.tv/tv-zle"
TOKEN_FILE = "token.txt"
CACHE_SECONDS = 3600

def read_saved_token():
    try:
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    except:
        return ""

def save_token(t):
    try:
        with open(TOKEN_FILE, "w") as f:
            f.write(t)
    except:
        pass

last_token = read_saved_token()
last_check = 0

def fetch_token_once():
    global last_token, last_check
    now = time.time()
    if now - last_check < 5:  # çok sık istekleri engelle (aynı anda çok istek gelirse)
        return last_token
    try:
        r = requests.get(PLAYER_PAGE, timeout=10)
        html = r.text
        m = re.search(r'https://s\.catcast\.tv/content/\d+/index\.m3u8\?token=[a-zA-Z0-9]+', html)
        if m:
            last_token = m.group(0)
            save_token(last_token)
    except Exception as e:
        # hata olursa önceki token kullanılacak
        pass
    last_check = now
    return last_token

@app.route("/list.m3u")
def list_m3u():
    global last_token, last_check
    # Her istekte (eğer 1 saatten eskiyse) güncelle
    now = time.time()
    if not last_token or (now - last_check) > CACHE_SECONDS:
        fetch_token_once()
    if not last_token:
        # kesin fallback (çalışan sabit link yoksa kullanıcıya uyarı)
        m3u = "#EXTM3U\n#EXTINF:-1,Catcast TV (Token bulunamadı)\n"
    else:
        m3u = "#EXTM3U\n#EXTINF:-1 tvg-id=\"\" tvg-name=\"Catcast TV\" tvg-logo=\"https://catcast.tv/logo.png\" group-title=\"IPTV\",Catcast TV\n" + last_token + "\n"
    return Response(m3u, mimetype="text/plain; charset=utf-8", headers={"Cache-Control":"no-store, no-cache, must-revalidate, max-age=0"})

@app.route("/")
def index():
    return "✅ IPTV Token servisi aktif — liste: <a href='/list.m3u'>/list.m3u</a>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
