@app.route('/upload', methods=['POST'])
def upload():
    # استلام البيانات الجديدة
    name = request.form['name']
    whatsapp = request.form['whatsapp']
    service = request.form['service_type'] # الخدمة المختارة
    brand = request.form['brand']
    model = request.form['model']
    serial = request.form['serial']

    file = request.files['bios']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # تنسيق الرسالة لتليجرام لتكون عملية أكثر
    caption = f"""
💎 DOCTOR BIOS - NEW JOB
--------------------------
🛠 Service: {service}
👤 Customer: {name}
💻 Device: {brand} {model}
🔢 Serial: {serial}
--------------------------
💬 Chat on WhatsApp: 
https://wa.me/{whatsapp.replace('+', '')}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    
    with open(filepath, 'rb') as f:
        requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"document": f})

    return "<h1>File Received! Ali Haboush will contact you soon.</h1>"