from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"
CHAT_ID = "PUT_YOUR_CHAT_ID_HERE"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    name = request.form['name']
    whatsapp = request.form['whatsapp']
    brand = request.form['brand']
    model = request.form['model']
    serial = request.form['serial']
    file = request.files['bios']

    caption = f"""
📥 New BIOS Job Received!

👤 Name: {name}
📱 WhatsApp: {whatsapp}
💻 Brand: {brand}
📦 Model: {model}
🔑 Serial: {serial}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

    files = {
        "document": (file.filename, file.stream)
    }

    data = {
        "chat_id": CHAT_ID,
        "caption": caption
    }

    requests.post(url, data=data, files=files)

    return "BIOS File Sent Successfully ✅"

if __name__ == '__main__':
    app.run()