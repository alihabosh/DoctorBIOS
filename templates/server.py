import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

app = Flask(__name__)

@app.route('/')
def home():
    return "DoctorBIOS Telegram Upload Service Running ✅"

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.document:
        file = await update.message.document.get_file()

        file_name = update.message.document.file_name
        save_path = f"uploads/{file_name}"

        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        await file.download_to_drive(save_path)

        await update.message.reply_text(
            f"✅ BIOS File Received:\n{file_name}"
        )

def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    application.run_polling()

if __name__ == "__main__":
    run_bot()