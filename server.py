from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

BOT_TOKEN = "PUT_YOUR_BOT_TOKEN"
CHAT_ID = "PUT_YOUR_CHAT_ID"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/detect_dmi", methods=["POST"])
def detect_dmi():

    file = request.files["bios"]
    data = file.read()

    model = "Not Detected"
    serial = "Not Detected"

    try:
        text = data.decode(errors="ignore")

        if "Dell" in text:
            model="Dell Laptop"

        if "Lenovo" in text:
            model="Lenovo Laptop"

        if "SerialNumber" in text:
            idx=text.find("SerialNumber")
            serial=text[idx:idx+30]

    except:
        pass

    return jsonify({
        "model":model,
        "serial":serial
    })

@app.route("/submit_job", methods=["POST"])
def submit_job():

    name=request.form.get("name")
    whatsapp=request.form.get("whatsapp")
    brand=request.form.get("brand")
    model=request.form.get("model")
    serial=request.form.get("serial")
    bios=request.files.get("bios")

    filepath=os.path.join(UPLOAD_FOLDER,bios.filename)
    bios.save(filepath)

    message=f"""
💎 NEW BIOS JOB

👤 Name: {name}
📱 WhatsApp: {whatsapp}
🏷 Brand: {brand}
💻 Model: {model}
🔢 Serial: {serial}
"""

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id":CHAT_ID,
            "text":message
        }
    )

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
        data={"chat_id":CHAT_ID},
        files={"document":open(filepath,"rb")}
    )

    return "OK"

if __name__=="__main__":
    app.run()