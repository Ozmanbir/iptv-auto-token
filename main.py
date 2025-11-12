# main.py
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

PLAYER_PAGE = os.getenv("PLAYER_PAGE", "https://catcast.tv/player/49918")
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", "120"))  # saniye
USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (compatible)")

app = Flask(__name__)

# in-memory store
_store = {"current_url": None, "last_checked": 0, "error": None}

def extract_m3u8_from_html(html: str) -> Optional[str]:
    """
    Basit heuristics: .m3u8?token=... geçen herhangi bir URL'i bul.
    """
    # 1) raw regex first
    m = re.search(r"https?://[^\s'\"<>]+\.m3u8\?[^'\"\s<>]+", html)
    if m:
        return m.group(0)
    # 2) try to scan script tags / source tags
    soup = BeautifulSoup(html, "html.parser")
    # look for source tags
    for tag in soup.find_all(["source","a","video"]):
        for attr in ("src","data-src","data-href","href"):
            v = tag.get(attr)
            if v and ".m3u8" in v:
                return v
    # 3) last attempt: search for s.catcast.tv content paths
    m2 = re.search(r"https?://s\.catcast\.tv/[^\s'\"<>]+\.m3u8\?[^'\"\s<>]+", html)
    if m2:
        return m2.group(0)
    return None

def refresh_loop():
    """
    sürekli arka plan döngüsü: PLAYER_PAGE içindeki .m3u8 linkini ayıklar
    """
    client = httpx.Client(timeout=20, headers={"User-Agent": USER_AGENT})
    while True:
        try:
            r = client.get(PLAYER_PAGE)
            r.raise_for_status()
            m3u8 = extract_m3u8_from_html(r.text)
            if m3u8:
                _store["current_url"] = m3u8
                _store["error"] = None
            else:
                _store["error"] = "m3u8 bulunamadi"
            _store["last_checked"] = int(time.time())
        except Exception as e:
            _store["error"] = str(e)
            # keep current_url if exists
        time.sleep(REFRESH_INTERVAL)

@app.route("/stream")
def stream_redirect():
    """Kullanıcıların video etiketinde kullanacağı endpoint"""
    url = _store.get("current_url")
    if not url:
        return jsonify({"error": "No stream available", "info": _store}), 503
    # direkt gerçek .m3u8'e yönlendir
    return redirect(url, code=302)

@app.route("/status")
def status():
    return jsonify(_store)

if __name__ == "__main__":
    # start background thread
    t = threading.Thread(target=refresh_loop, daemon=True)
    t.start()
    # run flask
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
