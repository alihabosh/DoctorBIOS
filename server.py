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
    name = request.form.get('name')
    whatsapp = request.form.get('whatsapp')
    service = request.form.get('service_type')
    brand = request.form.get('brand')
    model = request.form.get('model')
    serial = request.form.get('serial')
    
    file = request.files.get('bios')
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        caption = f"💎 NEW ORDER - DOCTOR BIOS\n--------------------------\n👤 Client: {name}\n🛠 Service: {service}\n💻 Device: {brand} {model}\n🔢 SN: {serial}\n--------------------------\n💬 WA: https://wa.me/{whatsapp.replace('+', '')}"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        
        with open(filepath, 'rb') as f:
            requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"document": f})
        return "<h1 style='color:white; background:black; text-align:center;'>Success! Your request has been sent to Ali Haboush.</h1>"
    return "<h1>Error uploading file.</h1>"

if __name__ == "__main__":
    app.run(debug=True)