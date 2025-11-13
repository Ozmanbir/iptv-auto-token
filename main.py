from flask import Flask,Response
import os
app=Flask(__name__)
@app.route('/list.m3u')
def playlist():
    m3u_content="#EXTM3U\n#EXTINF:-1 tvg-id=\"\" tvg-name=\"Catcast TV\" tvg-logo=\"https://catcast.tv/logo.png\" group-title=\"IPTV\",Catcast TV\nhttps://catcast.tv/tv-zle\n"
    return Response(m3u_content,mimetype='audio/x-mpegurl')
@app.route('/')
def index():
    return "✅ IPTV M3U servisi aktif!<br>Liste: <a href='/list.m3u'>/list.m3u</a>"
if __name__=='__main__':
    port=int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port)
