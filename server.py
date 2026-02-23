from flask import Flask, render_template, request
import requests
import os
import random
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

BOT_TOKEN = "8399796732:AAEHZQ_9d9g1lCPPdMc6VCW3Jfjhma2vDMU"
CHAT_ID = "1420084231"

if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.route('/track<jobid>')
def track(jobid):
    return f"""
    <html>
    <head>
        <title>Track Job</title>
        <style>
            body {{
                background:#0f2027;
                color:white;
                text-align:center;
                font-family:Arial;
                padding-top:100px;
            }}
            .box {{
                background:#203a43;
                padding:30px;
                width:300px;
                margin:auto;
                border-radius:10px;
                box-shadow:0 0 15px gold;
            }}
        </style>
    </head>

    <body>
        <div class="box">
            <h2>Tracking Job ID</h2>
            <h1>{jobid}</h1>
            <p>Your BIOS file is under review 🔧</p>
            <p>We will contact you on WhatsApp soon 📞</p>
        </div>
    </body>
    </html>
    """

@app.route('/upload', methods=['POST'])
def upload():
    name = request.form['name']
    whatsapp = request.form['whatsapp']
    brand = request.form['brand']
    model = request.form['model']
    serial = request.form['serial']

    file = request.files['bios']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

# 🆔 Generate Job ID
    job_id = "DB-" + str(random.randint(1000,9999))

# 💾 Save Job
    jobs = load_jobs()
    jobs[job_id] = {
        "name": name,
        "status": "Under Repair"
    }
    save_jobs(jobs)

    caption = f"""
💎 New DoctorBIOS Job

👤 Name: {name}
📞 WhatsApp: {whatsapp}
💻 Brand: {brand}
📌 Model: {model}
🔢 Serial: {serial}
"""

    url = f"https://api.telegram.org/bot8399796732:AAEHzQ_9d9g1lCPPdMc6VCW3Jfjhma2vDMU/sendDocument"

    with open(filepath, 'rb') as f:
        requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"document": f})

    return f"""
    <h2>✅ Uploaded Successfully</h2>
    <p>Your Job ID: <b>{job_id}</b></p>
    <a href='/track'>Track Your Repair Status</a>
    """

if __name__ == "__main__":
    app.run(debug=True)