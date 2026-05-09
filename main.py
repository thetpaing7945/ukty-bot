import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from flask import Flask # Flask ထပ်ထည့်ထားပါတယ်

# Render Web Service အတွက် အသေးစား Server တစ်ခု ဆောက်ခြင်း
server = Flask(__name__)
@server.route('/')
def home(): return "Bot is running!"

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        response = model.generate_content(update.message.text)
        await update.message.reply_text(response.text)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Web Service အဖြစ် run ရန်
    import threading
    port = int(os.environ.get("PORT", 5000))
    threading.Thread(target=lambda: server.run(host='0.0.0.0', port=port)).start()
    
    app.run_polling()

if __name__ == '__main__':
    main()
