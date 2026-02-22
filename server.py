from flask import Flask, render_template, request, jsonify
import os
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID  = os.environ.get("TELEGRAM_CHAT_ID")

# ---------------- DMI Extract ----------------

def extract_dmi_info(path):

    with open(path,"rb") as f:
        data=f.read()

    model=None
    serial=None

    anchor=data.find(b"_SM_")

    if anchor==-1:
        return None,None

    for i in range(anchor,len(data)-4):

        if data[i]==0x01:

            length=data[i+1]
            strings_start=i+length

            end=data.find(b"\x00\x00",strings_start)
            strings=data[strings_start:end].split(b"\x00")

            if len(strings)>2:
                model=strings[1].decode(errors="ignore")
                serial=strings[2].decode(errors="ignore")
                break

    return model,serial

# ---------------- Telegram Send ----------------

def send_to_telegram(file_path,name,whatsapp,brand,model,serial):

    caption=f"""
New BIOS Job 📥

Name: {name}
WhatsApp: {whatsapp}
Brand: {brand}
Model: {model}
Serial: {serial}
"""

    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

    with open(file_path,"rb") as file:

        requests.post(
            url,
            data={
                "chat_id":CHAT_ID,
                "caption":caption
            },
            files={"document":file}
        )

# ---------------- Pages ----------------

@app.route('/')
def index():
    return render_template("index.html")

# ---------------- Detect DMI ----------------

@app.route('/detect_dmi',methods=['POST'])
def detect_dmi():

    file=request.files['bios']
    file.save("temp.bin")

    model,serial=extract_dmi_info("temp.bin")

    return jsonify({
        "model":model,
        "serial":serial
    })

# ---------------- Final Upload ----------------

@app.route('/submit_job',methods=['POST'])
def submit_job():

    name=request.form['name']
    whatsapp=request.form['whatsapp']
    brand=request.form['brand']
    model=request.form['model']
    serial=request.form['serial']

    bios=request.files['bios']

    filename=secure_filename(f"{serial}_{brand}.bin")
    filepath=os.path.join(app.config["UPLOAD_FOLDER"],filename)

    bios.save(filepath)

    send_to_telegram(filepath,name,whatsapp,brand,model,serial)

    return "Uploaded Successfully"

# ---------------- Run ----------------

if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)