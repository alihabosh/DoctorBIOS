from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "8399796732:AAH07lP33r9C3ITFBEYV7I2hH7tcRYZsBzk"
CHAT_ID = "8399796732"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit_job", methods=["POST"])
def submit_job():
    name = request.form["name"]
    whatsapp = request.form["whatsapp"]
    brand = request.form["brand"]
    model = request.form["model"]
    serial = request.form["serial"]
    bios = request.files["bios"]

    filepath = os.path.join(UPLOAD_FOLDER, bios.filename)
    bios.save(filepath)

    caption = f"""
🛠 New BIOS Job

👤 Name: {name}
📱 WhatsApp: {whatsapp}
💻 Brand: {brand}
📦 Model: {model}
🔢 Serial: {serial}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

    with open(filepath, "rb") as f:
        requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "caption": caption
            },
            files={
                "document": f
            }
        )

    return "BIOS Sent Successfully ✔"

if __name__ == "__main__":
    app.run()