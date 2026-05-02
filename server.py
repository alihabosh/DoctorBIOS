from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# إعداد المجلدات اللازمة
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- التوكن الجديد والآيدي الخاص بك ---
BOT_TOKEN = "8399796732:AAG897g1igybOwXMbsqabbNQlKKdGYPBHOI"
CHAT_ID = "1420084231"

@app.route('/')
def index():
    # استدعاء ملف الواجهة الأساسي
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    try:
        name = request.form.get('name')
        whatsapp = request.form.get('whatsapp')
        brand = request.form.get('brand')
        model = request.form.get('model')
        serial = request.form.get('serial')
        file = request.files.get('bios')

        if file and name:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # نص الرسالة المنسق لتليجرام
            caption = (f"💎 *New DoctorBIOS Job*\n\n"
                       f"👤 *Customer:* {name}\n"
                       f"📞 *WhatsApp:* {whatsapp}\n"
                       f"💻 *Brand:* {brand.upper() if brand else 'N/A'}\n"
                       f"📌 *Model:* {model}\n"
                       f"🔢 *Serial:* {serial}")

            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

            with open(filepath, 'rb') as f:
                response = requests.post(url, data={
                    "chat_id": CHAT_ID, 
                    "caption": caption, 
                    "parse_mode": "Markdown"
                }, files={"document": f})

            # تنظيف السيرفر من الملف بعد الإرسال
            if os.path.exists(filepath):
                os.remove(filepath)

            if response.status_code == 200:
                return "<script>alert('تم إرسال الملف بنجاح! ✅'); window.location.href = '/';</script>"
            return f"Telegram Error: {response.text}"
        
        return "الرجاء ملء جميع الحقول المطلوبة."
    except Exception as e:
        return f"خطأ في السيرفر: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)