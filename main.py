import requests
import re
from flask import Flask, jsonify

app = Flask(__name__)

# 🔹 CatCast sayfası (artık sabit)
PLAYER_PAGE = "https://catcast.tv/tv-zle"

@app.route("/")
def home():
    try:
        # Sayfayı indir
        response = requests.get(PLAYER_PAGE, timeout=10)
        response.raise_for_status()

        # Token içeren m3u8 bağlantısını bul
        match = re.search(r'(https://s\.catcast\.tv/content/.+?index\.m3u8\?token=[a-zA-Z0-9]+)', response.text)

        if match:
            stream_url = match.group(1)
            return jsonify({
                "status": "success",
                "stream_url": stream_url
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Yayın linki bulunamadı"
            })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
