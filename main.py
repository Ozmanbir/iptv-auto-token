from flask import Flask, redirect, request
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ IPTV Otomatik Token Yönlendirme Aktif!<br>Örnek: /live/49918"

@app.route('/live/<int:channel_id>')
def get_live(channel_id):
    try:
        # Gerçek token’ı otomatik almak için örnek API isteği
        # (örnek link, senin yayına göre değişebilir)
        token_api = f"https://s.catcast.tv/content/{channel_id}/index.m3u8"
        r = requests.get(token_api, timeout=5)

        if r.status_code == 200:
            return redirect(token_api, code=302)
        else:
            return "❌ Token bulunamadı veya geçersiz yayın.", 404
    except Exception as e:
        return f"❌ Hata oluştu: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
