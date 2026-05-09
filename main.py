import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Render ရဲ့ Environment Variables ထဲကနေ Key တွေကို ယူပါမယ်
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
သင်သည် 'UKTY (ဘာသာစုံစာသင်ဝိုင်း)' ၏ တရားဝင် Admin AI ဖြစ်သည်။ 
သင်တန်းအကြောင်း အချက်အလက်များ:
- သင်ကြားပေးသောအတန်းများ: G 10, G 11, G 12 (Grade 10, 11, 12)
- ဆရာမအရည်အချင်း: B.A (Eng), Dip in ELT ဘွဲ့ရ ဆရာမကိုယ်တိုင် သင်ကြားသည်။
- သင်ကြားသည့်ဘာသာရပ်: ဘာသာစုံ (အဓိက အင်္ဂလိပ်စာ အလေးပေးသည်)
- ပုံစံ: ယဉ်ကျေးပျူငှာစွာ ဖြေကြားပါ။ ကျောင်းသားများကို 'မောင်လေး/ညီမလေး' သို့မဟုတ် 'လူကြီးမင်း' ဟု သုံးနှုန်းနိုင်သည်။
- အဖြေများကို မြန်မာလိုပဲ ဖြေပါ။
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")

def main():
    logging.basicConfig(level=logging.INFO)
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found!")
        return

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
