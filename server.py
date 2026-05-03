from flask import Flask, render_template, request
import requests
import os
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

BOT_TOKEN = "8399796732:AAG897g1igybOwXMbsqabbNQlKKdGYPBHOI"
CHAT_ID = "1420084231"

if not os.path.exists("uploads"):
    os.makedirs("uploads")

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
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    caption = f"""
💎 New DoctorBIOS Job

👤 Name: {name}
📞 WhatsApp: {whatsapp}
💻 Brand: {brand}
📌 Model: {model}
🔢 Serial: {serial}
"""

    url = f"https://api.telegram.org/bot8399796732:AAG897g1igybOwXMbsqabbNQlKKdGYPBHOI/sendDocument"

    with open(filepath, 'rb') as f:
        requests.post(url,
        data={"chat_id": CHAT_ID, "caption": caption},
        files={"document": f})

    return render_template("index.html")

if __name__ == "__main__":
    app.run()