from flask import Flask, render_template, request
import os
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

BOT_TOKEN = "8399796732:AAH07lP33r9C3ITFBEYV7I2hH7tcRYZsBzk"
CHAT_ID = "YOUR_CHAT_ID"

def send_to_telegram(file_path, name, whatsapp, brand, model, serial):
    caption = f"""
🆕 New BIOS Job Received

👤 Name: {name}
📱 WhatsApp: {whatsapp}
💻 Brand: {brand}
📦 Model: {model}
🔑 Serial: {serial}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

    with open(file_path, "rb") as file:
        response = requests.post(
            url,
            data={"chat_id": CHAT_ID, "caption": caption},
            files={"document": file}
        )
    return response.status_code

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
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    send_to_telegram(filepath, name, whatsapp, brand, model, serial)

    return "Uploaded Successfully ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)