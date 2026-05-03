from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# بيانات البوت الخاصة بك
BOT_TOKEN = "8399796732:AAG897g1igybOwXMbsqabbNQlKKdGYPBHOI"
CHAT_ID = "1420084231"

if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    # استلام البيانات المطورة
    name = request.form['name']
    whatsapp = request.form['whatsapp']
    service = request.form['service_type']
    brand = request.form['brand']
    model = request.form['model']
    serial = request.form['serial']

    file = request.files['bios']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # رسالة تليجرام احترافية مع رابط واتساب
    caption = f"""
💎 DOCTOR BIOS - NEW JOB 🛠️
--------------------------
👤 Customer: {name}
🛠 Service: {service}
💻 Device: {brand} {model}
🔢 Serial: {serial}
--------------------------
💬 Chat with Customer: 
https://wa.me/{whatsapp.replace('+', '').replace(' ', '')}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

    with open(filepath, 'rb') as f:
        requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"document": f})

    return "<h1>تم استلام ملفك بنجاح! علي حبوش سيتواصل معك قريباً.</h1>"

if __name__ == "__main__":
    app.run()