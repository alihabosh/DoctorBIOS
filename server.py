from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# بيانات البوت والدردشة الخاصة بك
BOT_TOKEN = "8399796732:AAG897g1igybOwXMbsqabbNQlKKdGYPBHOI"
CHAT_ID = "1420084231"

if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    try:
        name = request.form['name']
        whatsapp = request.form['whatsapp']
        brand = request.form['brand']
        model = request.form['model']
        serial = request.form['serial']

        file = request.files['bios']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            caption = f"💎 *New DoctorBIOS Job*\n\n👤 *Name:* {name}\n📞 *WhatsApp:* {whatsapp}\n💻 *Brand:* {brand}\n📌 *Model:* {model}\n🔢 *Serial:* {serial}"

            url = f"https://api.telegram.org/bot8399796732:AAG897g1igybOwXMbsqabbNQlKKdGYPBHOI/sendDocument"


            with open(filepath, 'rb') as f:
                requests.post(url, data={"chat_id": CHAT_ID, "caption": caption, "parse_mode": "Markdown"}, files={"document": f})

            return """
            <script>
                alert('SUCCESS: File Sent to Lab! ✅');
                window.location.href = '/';
            </script>
            """
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # تعديل المنفذ ليعمل على الاستضافات السحابية مثل Render
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))