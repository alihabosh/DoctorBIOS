from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# البيانات المحدثة بناءً على صورك
BOT_TOKEN = "8399796732:AAEHZQ_9d9g1lCPPdMc6VCW3Jfjhma2vDMU"
CHAT_ID = "1420084231"

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
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

        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            caption = (
                f"💎 *NEW BIOS JOB RECEIVED*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 *Client:* {name}\n"
                f"📞 *WhatsApp:* {whatsapp}\n"
                f"💻 *Device:* {brand} {model}\n"
                f"🔢 *Serial:* {serial}\n"
                f"━━━━━━━━━━━━━━━━━━━━"
            )

            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            
            with open(filepath, 'rb') as doc:
                files = {'document': (filename, doc)}
                data = {'chat_id': CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}
                response = requests.post(url, data=data, files=files)

            if response.status_code == 200:
                # رسالة نجاح ترجعك للموقع
                return """
                <script>
                    alert('SUCCESS: File Sent to Lab! ✅');
                    window.location.href = '/';
                </script>
                """
            else:
                return f"Telegram Error: {response.text}"
                
        return redirect(url_for('index'))
    except Exception as e:
        return f"System Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)