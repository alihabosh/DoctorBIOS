from flask import Flask, request, render_template_string
import os
import requests

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"bin", "rom", "fd"}

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def send_to_telegram(file_path):

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram not configured")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"

    with open(file_path, "rb") as f:
        requests.post(
            url,
            data={"chat_id": TELEGRAM_CHAT_ID},
            files={"document": f}
        )


HTML_PAGE = """
<!doctype html>
<title>DoctorBIOS Upload</title>
<h2>Upload BIOS File</h2>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
<p>Allowed: .bin .rom .fd</p>
"""


@app.route("/upload", methods=["GET", "POST"])
def upload_file():

    if request.method == "POST":

        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]

        if file.filename == "":
            return "No selected file"

        if file and allowed_file(file.filename):

            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            send_to_telegram(filepath)

            return "BIOS Uploaded Successfully ✔️"

        else:
            return "Only BIOS files allowed!"

    return render_template_string(HTML_PAGE)


@app.route("/")
def home():
    return "DoctorBIOS Online ✔️"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
