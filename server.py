from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():

    name = request.form.get("name")
    whatsapp = request.form.get("whatsapp")
    brand = request.form.get("brand")
    model = request.form.get("model")
    serial = request.form.get("serial")

    file = request.files.get("bios")

    if not file:
        return "No file uploaded"

    filename = secure_filename(file.filename)
    path = os.path.join("uploads", filename)
    file.save(path)

    message = f"""
📥 NEW BIOS JOB

👤 Name: {name}
📱 WhatsApp: {whatsapp}
💻 Brand: {brand}
📟 Model: {model}
🔢 Serial: {serial}
📎 File: {filename}
"""

    requests.get(
        f"https://api.telegram.org/botYOUR_BOT_TOKEN/sendMessage",
        params={
            "chat_id": "YOUR_CHAT_ID",
            "text": message
        }
    )

    return "Job Submitted Successfully ✅"

if __name__ == "__main__":
    app.run()