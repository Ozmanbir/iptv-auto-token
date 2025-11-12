from flask import Flask,redirect
import os
app=Flask(__name__)
@app.route('/')
def index():
 return redirect("https://catcast.tv/tv-zle",code=302)
if __name__=='__main__':
 port=int(os.environ.get('PORT',5000))
 app.run(host='0.0.0.0',port=port)
