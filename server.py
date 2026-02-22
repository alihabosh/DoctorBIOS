import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 🔐 ضع التوكن والايدي في Environment Variables في Render
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


@app.route('/')
def home():
    return render_template("index.html")


# 🔍 Detect DMI (نسخة تجريبية حالياً)
@app.route('/detect_dmi', methods=['POST'])
def detect_dmi():
    file = request.files.get('bios')

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # هنا لاحقاً نضع كود استخراج DMI الحقيقي
    return jsonify({
        "model": "Detected_Model",
        "serial": "Detected_Serial"
    })


# 📤 إرسال الطلب إلى Telegram
@app.route('/submit_job', methods=['POST'])
def submit_job():

    name = request.form.get('name')
    whatsapp = request.form.get('whatsapp')
    brand = request.form.get('brand')
    model = request.form.get('model')
    serial = request.form.get('serial')
    bios = request.files.get('bios')

    if not bios:
        return "No BIOS file", 400

    caption = f"""
🆕 NEW BIOS JOB

👤 Name: {name}
📱 WhatsApp: {whatsapp}
🏷 Brand: {brand}
💻 Model: {model}
🔢 Serial: {serial}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

    files = {
        "document": (bios.filename, bios.stream)
    }

    data = {
        "chat_id": CHAT_ID,
        "caption": caption
    }

    response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        return "Job Submitted Successfully ✅"
    else:
        return "Telegram Error ❌", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)