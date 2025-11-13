from flask import Flask,Response
import requests,re,os
app=Flask(__name__)
PLAYER_PAGE="https://catcast.tv/tv-zle"
@app.route('/list.m3u')
def list_m3u():
    try:
        html=requests.get(PLAYER_PAGE,timeout=10).text
        match=re.search(r'https://s\.catcast\.tv/content/\d+/index\.m3u8\?token=[a-zA-Z0-9]+',html)
        if not match:
            return Response("#EXTM3U\n#EXTINF:-1,Catcast TV (Token bulunamadı)\n",mimetype='audio/x-mpegurl')
        m3u8_url=match.group(0)
        m3u_content=f"#EXTM3U\n#EXTINF:-1 tvg-id=\"\" tvg-name=\"Catcast TV\" tvg-logo=\"https://catcast.tv/logo.png\" group-title=\"IPTV\",Catcast TV\n{m3u8_url}\n"
        return Response(m3u_content,mimetype='audio/x-mpegurl')
    except Exception as e:
        return Response(f"#EXTM3U\n#EXTINF:-1,Catcast TV (Hata: {e})\n",mimetype='audio/x-mpegurl')
@app.route('/')
def index():
    return "✅IPTV M3U Token servisi aktif!<br>Liste:<a href='/list.m3u'>/list.m3u</a>"
if __name__=='__main__':
    port=int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port)
