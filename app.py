from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
import pywhatkit
import os
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
import pandas as pd
from threading import Timer


app = Flask(__name__)

UPLOAD_FOLDER = "/static/files"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app_root = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sms", methods=["POST", "GET"])
def getnew_form():

    msg = request.form.get("message")
    phone = str(request.form.get("number"))
    hour = datetime.now().hour
    minute = datetime.now().minute
    pywhatkit.sendwhatmsg("+91" + phone, msg, 18, 59, 15, True, 2)
    flash("The message has been sent")
    return redirect(url_for("/sms"))


@app.route("/file", methods=["POST", "GET"])
def upload_file():
    target = os.path.join(app_root, UPLOAD_FOLDER)
    msg = request.form.get("message")
    if not os.path.isdir(target):
        os.makedirs(target)
    if request.method == "POST":
        file = request.files["file"]
        file_name = file.filename or ""
        destination = "/".join([target, file_name])
        file.save(destination)
        # CVS Column Names
        col_name = "phonenumber"
        msg = str(request.form.get("number"))
        hour = datetime.now().hour
        minute = datetime.now().minute
        # Use Pandas to parse the CSV file
        csvData = pd.read_csv(destination, names=col_name, header=None)
        # Loop through the Rows
        for i in csvData.iterrows():
            pywhatkit.sendwhatmsg("+91" + i, msg, hour, minute, 15, True, 2)
    flash("The message has been sent")
    return redirect(url_for("/file"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
