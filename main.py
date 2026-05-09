import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from flask import Flask
import threading

# Render Web Service Setup
server = Flask(__name__)
@server.route('/')
def home(): return "Bot is live!"

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)

# AI Model ကို စိတ်ချရအောင် ပြန်ပြင်ထားခြင်း
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_text = update.message.text
    try:
        # AI ဆီက အဖြေတောင်းခြင်း
        response = model.generate_content(user_text)
        
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("AI က အဖြေမထုတ်ပေးနိုင်လို့ ဖြစ်နေပါတယ်။")

    except Exception as e:
        logging.error(f"AI Error: {e}")
        # ဘာ Error တက်လဲဆိုတာ Telegram မှာ တိုက်ရိုက်ပြခိုင်းခြင်း
        await update.message.reply_text(f"⚠️ AI မှာ Error တက်နေပါတယ်: {str(e)}")

def main():
    logging.basicConfig(level=logging.INFO)
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    port = int(os.environ.get("PORT", 10000))
    threading.Thread(target=lambda: server.run(host='0.0.0.0', port=port)).start()
    
    print("UKTY Bot is starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
