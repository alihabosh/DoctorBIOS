from flask import Flask, render_template, request
import os
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(file_path, "rb") as file:
        response = requests.post(
            url,
            data={"chat_id": CHAT_ID},
            files={"document": file}
        )
    return response.status_code

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file selected"

    file = request.files['file']

    if file.filename == '':
        return "Empty filename"

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    send_to_telegram(filepath)

    return "BIOS Uploaded & Sent to Telegram Successfully ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
