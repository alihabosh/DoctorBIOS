from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

    with open(filepath, "rb") as f:
        requests.post(
            url,
            data={"chat_id": CHAT_ID},
            files={"document": f}
        )

    return "File Sent Successfully ✔"

if __name__ == "__main__":
    app.run()