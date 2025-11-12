import threading
import time
import re
import os
from typing import Optional
from flask import Flask, redirect, jsonify
import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# Catcast player sayfası
PLAYER_PAGE = "https://catcast.tv/player/49918"
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", 3600))  # saniye cinsinden (varsayılan: 1 saat)
USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

app = Flask(__name__)

# Bellekte saklanan mevcut m3u8 linki
_store = {"current_url": None, "last_checked": None}


def extract_m3u8_from_html(html: str) -> Optional[str]:
    """Sayfadan .m3u8 tokenli URL'yi bulur."""
    match = re.search(r'https://[^"\']+\.m3u8\?token=[^"\']+', html)
    if match:
        return match.group(0)
    return None


def fetch_new_token():
    """Yeni tokenli m3u8 URL’sini alır."""
    global _store
    headers = {"User-Agent": USER_AGENT}

    try:
        response = httpx.get(PLAYER_PAGE, headers=headers, timeout=20)
        response.raise_for_status()

        new_url = extract_m3u8_from_html(response.text)
        if new_url and new_url != _store["current_url"]:
            _store["current_url"] = new_url
            _store["last_checked"] = time.strftime("%Y-%m-%d %H:%M:%S")
            print("✅ Yeni tokenli link bulundu:", new_url)
        else:
            print("🔁 Token değişmemiş.")

    except Exception as e:
        print("❌ Hata:", e)


def auto_refresh():
    """Belirli aralıklarla tokeni yeniler."""
    while True:
        fetch_new_token()
        time.sleep(REFRESH_INTERVAL)


@app.route("/")
def home():
    if _store["current_url"]:
        return redirect(_store["current_url"])
    return jsonify({"status": "Hazır değil", "last_checked": _store["last_checked"]})


if __name__ == "__main__":
    threading.Thread(target=auto_refresh, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
