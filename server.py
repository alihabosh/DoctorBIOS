from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# البيانات الخاصة ببوت تليجرام
BOT_TOKEN = "8399796732:AAEHZQ_9d9g1lCPPdMc6VCW3Jfjhma2vDMU"
CHAT_ID = "1420084231"

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    # كود رفع الملف وإرساله للبوت
    file = request.files.get('bios')
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        caption = f"💎 NEW REQUEST\n👤 {request.form.get('name')}\n💻 {request.form.get('brand')} {request.form.get('model')}"
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                      data={"chat_id": CHAT_ID, "caption": caption}, files={"document": open(filepath, 'rb')})
    return "SENT SUCCESSFULLY ✅"

if __name__ == "__main__":
    app.run(debug=True)