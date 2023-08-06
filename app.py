from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import pywhatkit
import os
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = "static/files"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app_root = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sms", methods=["POST"])
def send_sms():
    msg = request.form.get("message")
    phone = "+91" + str(request.form.get("number"))
    hour = datetime.now().hour
    minute = datetime.now().minute
    pywhatkit.sendwhatmsg(phone, msg, hour, minute, 15, True, 2)
    flash("The message has been sent")
    return redirect(url_for("index"))

@app.route("/file", methods=["POST"])
def upload_file():
    target = os.path.join(app_root, app.config["UPLOAD_FOLDER"])
    msg = request.form.get("message")
    
    if not os.path.isdir(target):
        os.makedirs(target)
        
    if request.method == "POST":
        file = request.files["file"]
        file_name = secure_filename(file.filename)
        destination = os.path.join(target, file_name)
        file.save(destination)
        
        col_name = "phonenumber"
        
        # Use Pandas to parse the CSV file
        csvData = pd.read_csv(destination, names=[col_name], header=None)
        
        hour = datetime.now().hour
        minute = datetime.now().minute
        
        # Loop through the rows
        for i, row in csvData.iterrows():
            pywhatkit.sendwhatmsg("+91" + str(row[col_name]), msg, hour, minute, 15, True, 2)
    
    flash("The message has been sent")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.secret_key = "supersecretkey"
    app.run(host="0.0.0.0", port=80)
