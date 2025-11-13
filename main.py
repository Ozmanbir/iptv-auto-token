# main.py
from flask import Flask, Response
import requests, re, time, os

app = Flask(__name__)

# Basit bellek cache: (url -> (timestamp, m3u8_url))
CACHE = {}
CACHE_TTL = 30  # saniye, token sık değişiyorsa azalt veya artır

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

def find_m3u8_from_html(html):
    """
    HTML içinde s.catcast veya .m3u8 içeren tokenli URL'leri arar.
    Döner: tam url veya None
    """
    # Önce açıkça tokenli .m3u8 pattern'lerini yakala
    patterns = [
        r"https?://s\.catcast\.tv/[^\"'\s>]+?index\.m3u8\?[^\"'\s>]+",
        r"https?://[^\"'\s>]*\.m3u8\?[^\"'\s>]+",
        r"https?://[^\"'\s>]*\.m3u8"  # tokensiz bile varsa yakala
    ]
    for p in patterns:
        m = re.search(p, html)
        if m:
            return m.group(0)
    return None

def get_tokened_m3u8():
    """
    catcast.tv sayfasını çek ve içinden tokenli .m3u8 linkini bul.
    """
    # Örnek başlangıç sayfası (senin kanala özel url kullan)
    page_urls = [
        "https://catcast.tv/tv-zle",
        # alternatif: iframe/player id'si varsa onu da dene (örnek: /player/49918)
        # "https://catcast.tv/player/49918",
    ]

    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"}
    for url in page_urls:
        try:
            r = requests.get(url, headers=headers, timeout=10)
        except Exception:
            continue
        if r.status_code != 200:
            continue
        html = r.text

        # 1) Direkt HTML içinde m3u8 araması
        m3u8 = find_m3u8_from_html(html)
        if m3u8:
            return m3u8

        # 2) Bazen player iframe bulunur: <iframe src="/player/49918"> -> iframe src'e git
        iframe = re.search(r'<iframe[^>]+src=["\']([^"\']+)["\']', html)
        if iframe:
            src = iframe.group(1)
            # Eğer src relative ise tam url yap
            if src.startswith("/"):
                src = "https://catcast.tv" + src
            try:
                r2 = requests.get(src, headers=headers, timeout=10)
            except Exception:
                continue
            if r2.status_code != 200:
                continue
            m3u8 = find_m3u8_from_html(r2.text)
            if m3u8:
                return m3u8

        # 3) Bazen sayfa JS ile çekiyor; sayfada config veya JSON url olabilir
        # Basitçe "index.m3u8" içeren her şeyi yakaladık zaten.

    return None

@app.route('/list.m3u')
def playlist():
    cache_key = "catcast_tv_zle"
    now = time.time()
    # cache kontrol
    if cache_key in CACHE:
        ts, url = CACHE[cache_key]
        if now - ts < CACHE_TTL and url:
            m3u8_url = url
        else:
            m3u8_url = get_tokened_m3u8()
            CACHE[cache_key] = (now, m3u8_url)
    else:
        m3u8_url = get_tokened_m3u8()
        CACHE[cache_key] = (now, m3u8_url)

    if not m3u8_url:
        # token bulunamadıysa bilgi veren tek satırlık playlist
        m3u_content = "#EXTM3U\n#EXTINF:-1,Catcast TV (Token bulunamadı)\n"
    else:
        # m3u8_url doğrudan oynatılabilir link olmalı
        m3u_content = "#EXTM3U\n#EXTINF:-1 tvg-id=\"\" tvg-name=\"Catcast TV\" tvg-logo=\"https://catcast.tv/logo.png\" group-title=\"IPTV\",Catcast TV\n" + m3u8_url + "\n"

    return Response(m3u_content, mimetype='audio/x-mpegurl')

@app.route('/')
def index():
    return "✅ IPTV M3U servisi aktif! Liste: <a href='/list.m3u'>/list.m3u</a>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
