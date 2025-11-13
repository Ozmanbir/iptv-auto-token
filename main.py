from flask import Flask, Response
import os, requests, re, time

app = Flask(__name__)
last_token = ""
last_check = 0

@app.route('/list.m3u')
def playlist():
    global last_token, last_check
    now = time.time()
    
    # 1 saatte bir yeniden çek
    if now - last_check > 3600 or not last_token:
        try:
            html = requests.get("https://catcast.tv/tv-zle", timeout=10).text
            m = re.search(r"https://s\.catcast\.tv/content/\d+/index\.m3u8\?token=[a-f0-9]+", html)
            if m:
                last_token = m.group(0)
                print(f"[+] Yeni token bulundu: {last_token}")
            else:
                print("[-] Token bulunamadı, eski kullanılıyor.")
        except Exception as e:
            print(f"[-] Hata: {e}")
        last_check = now

    if not last_token:
        last_token = "https://s.catcast.tv/content/49918/index.m3u8"

    m3u = (
        "#EXTM3U\n"
        "#EXTINF:-1 tvg-id=\"\" tvg-name=\"Catcast TV\" tvg-logo=\"https://catcast.tv/logo.png\" group-title=\"IPTV\",Catcast TV\n"
        f"{last_token}\n"
    )
    return Response(m3u, mimetype="audio/x-mpegurl", headers={
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"
    })

@app.route('/')
def index():
    return "✅ IPTV Token Yenileme Servisi Aktif<br><a href='/list.m3u'>📺 M3U Listesini Gör</a>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
