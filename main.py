from flask import Flask,Response
import requests,re,os
app=Flask(__name__)
@app.route('/list.m3u')
def playlist():
    try:
        html=requests.get("https://catcast.tv/player/49918",timeout=10).text
        match=re.search(r"https://s\.catcast\.tv/content/\d+/index\.m3u8\?token=[a-z0-9]+",html)
        if match:
            stream=match.group(0)
        else:
            stream="https://catcast.tv/tv-zle"
        m3u="#EXTM3U\n#EXTINF:-1 tvg-name=\"Catcast TV\" group-title=\"IPTV\",Catcast TV\n"+stream+"\n"
        return Response(m3u,mimetype='audio/x-mpegurl')
    except Exception as e:
        return Response("#EXTM3U\n#EXTINF:-1,Error\nError:"+str(e)+"\n",mimetype='audio/x-mpegurl')
@app.route('/')
def index():
    return "✅ IPTV M3U aktif! <a href='/list.m3u'>Listeyi indir</a>"
if __name__=='__main__':
    port=int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port)
