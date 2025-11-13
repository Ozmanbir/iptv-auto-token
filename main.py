from flask import Flask, Response, stream_with_context, request
import requests, os, time

app = Flask(__name__)

# Basit index
@app.route('/')
def index():
    return "✅ IPTV proxy aktif!<br>/live ve /live2"

def proxy_stream(url, extra_headers=None):
    """Uzak tokenli URL'i isteyip içeriği aynı şekilde stream ile dön."""
    headers = {
        "User-Agent": request.headers.get("User-Agent", "Mozilla/5.0"),
        # gerekirse Referer ekle (ör: catcast için)
        "Referer": "https://catcast.tv"
    }
    if extra_headers:
        headers.update(extra_headers)
    try:
        r = requests.get(url, headers=headers, stream=True, timeout=15)
    except Exception as e:
        return Response(f"Remote request failed: {e}", status=502, mimetype="text/plain")

    if r.status_code != 200:
        return Response(f"Remote returned {r.status_code}", status=502, mimetype="text/plain")

    # içerik tipi m3u8 için uygun content-type
    content_type = r.headers.get("Content-Type", "application/vnd.apple.mpegurl")
    return Response(stream_with_context(r.iter_content(chunk_size=1024)), content_type=content_type)

# 1. yayın (catcast örneği)
@app.route('/live')
def live():
    token_url = "https://s.catcast.tv/content/49918/index.m3u8?token=b13e2ae89c49fb4132e0622f19419604"
    # catcast için Referer gerekirse extra_headers içine koy (yukarısı zaten koyuyor)
    return proxy_stream(token_url)

# 2. yayın (diğer tokenli url)
@app.route('/live2')
def live2():
    token_url = "https://dc34a9483e0f144e9e.pages.dev/cefc8a875b06cc6da16ca7dd99157dee/DmodYM9CdSNPUZyc2x7VWd/5062/dc34a9483e0f144e9e.pages.dev/chunklist_hd.m3u8?verify=1763016750936~213.238.187.84~bd14cdaa057f57353a74ee68d0a7a394"
    # Eğer bu host özel header isterse buraya ekle:
    extra = {
        # "Referer": "https://dc34a9483e0f144e9e.pages.dev/",
        # "User-Agent": "Mozilla/5.0 (compatible)"
    }
    return proxy_stream(token_url, extra_headers=extra)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
