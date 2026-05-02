from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# --- التوكن والآيدي الخاص بك (تم الدمج بنجاح) ---
BOT_TOKEN = "8399796732:AAG897g1igybOwXMbsqabbNQlKKdGYPBHOI"
CHAT_ID = "1420084231"
# ---------------------------------------------

if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.route('/')
def index():
    return render_template("index_4.html")

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # استلام البيانات من النموذج الجديد
        name = request.form.get('name')
        whatsapp = request.form.get('whatsapp')
        brand = request.form.get('brand')
        model = request.form.get('model')
        serial = request.form.get('serial')
        file = request.files.get('bios')

        if file and name:
            # حفظ الملف في مجلد uploads
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # تجهيز نص الرسالة
            caption = (f"💎 *New DoctorBIOS Job*\n\n"
                       f"👤 *Customer:* {name}\n"
                       f"📞 *WhatsApp:* {whatsapp}\n"
                       f"💻 *Brand:* {brand.upper()}\n"
                       f"📌 *Model:* {model}\n"
                       f"🔢 *Serial:* {serial}")

            # رابط الإرسال المباشر باستخدام التوكن المدمج
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

            with open(filepath, 'rb') as f:
                response = requests.post(url, data={
                    "chat_id": CHAT_ID, 
                    "caption": caption, 
                    "parse_mode": "Markdown"
                }, files={"document": f})

            if response.status_code == 200:
                return "<script>alert('SUCCESS: File Sent to Lab! ✅'); window.location.href = '/';</script>"
            return f"Telegram Error: {response.text}"
        
        return "Missing data! Please check all fields."
    except Exception as e:
        return f"System Error: {str(e)}"

if __name__ == "__main__":
    # تشغيل السيرفر على بورت 5000 (أو البورت الذي توفره الاستضافة)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)