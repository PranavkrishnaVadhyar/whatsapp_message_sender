from flask import Flask, render_template, request, redirect,url_for
from datetime import datetime
import pywhatkit
from threading import Timer


app = Flask (__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sms", methods=["POST","GET"])
def getnew_form():
    
    msg = request.form.get("message")
    phone = request.form.get("number")
    
    pywhatkit.sendwhatmsg (phone,msg,13,24,15,True,2)
    
    return redirect(url_for("/sms"))


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80)