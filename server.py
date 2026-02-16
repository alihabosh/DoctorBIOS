from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"bin", "rom", "fd", "cap"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024 * 1024  # 64MB limit


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return redirect(url_for("home"))

    file = request.files["file"]

    if file.filename == "":
        return redirect(url_for("home"))

    if not allowed_file(file.filename):
        return "Only BIOS files allowed!"

    filename = secure_filename(file.filename)

    # random rename to prevent overwrite or hacking
    import uuid
    ext = filename.rsplit(".", 1)[1]
    filename = str(uuid.uuid4()) + "." + ext

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run()
