from flask import Flask, request, render_template, redirect
import os
import requests

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

@app.route('/')
def index():
    return render_template("upload.html")

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            send_to_telegram(filepath)

            return redirect('/')
    return render_template("upload.html")

def send_to_telegram(filepath):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(filepath, 'rb') as f:
        requests.post(url, data={'chat_id': CHAT_ID}, files={'document': f})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
