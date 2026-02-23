
from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "doctorbios_secret"

# 🔐 PUT YOUR DATA HERE
BOT_TOKEN = "doctorbios_upload_bot"
CHAT_ID = "1420084231"

def send_to_telegram(name, whatsapp, brand, model, serial, file):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    caption = f"""
🧑 Name: {name}
📱 WhatsApp: {whatsapp}
💻 Brand: {brand}
📟 Model: {model}
🔢 Serial: {serial}
"""
    files = {'document': (file.filename, file.stream, file.mimetype)}
    data = {'chat_id': CHAT_ID, 'caption': caption}
    r = requests.post(url, data=data, files=files)
    return r.ok

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    name = request.form.get("name")
    whatsapp = request.form.get("whatsapp")
    brand = request.form.get("brand")
    model = request.form.get("model")
    serial = request.form.get("serial")
    bios = request.files.get("bios")

    if bios:
        ok = send_to_telegram(name, whatsapp, brand, model, serial, bios)
        if ok:
            flash("Uploaded Successfully!")
        else:
            flash("Telegram Error! Check Token/ChatID")
    else:
        flash("No File Selected!")

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
