


import os
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# إعداد FastAPI
app = FastAPI()

# الحصول على الإعدادات من Render
TOKEN = "8392448718:AAGj7juwOmQz8f8UTP7xM48ysS-GTmxlyck"
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL") # رابط موقعك على رندر

# إنشاء تطبيق التلجرام (بدون تشغيل Polling)
tg_app = Application.builder().token(TOKEN).build()

# دالة الترحيب
async def start(update: Update, context):
    await update.message.reply_text("أهلاً بك! أنا أعمل الآن بنظام الـ Webhook السريع جداً 🚀")

# دالة الأسئلة والأجوبة
async def handle_message(update: Update, context):
    text = (update.message.text or "").lower()

    if "كيف حالك" in text:
        await update.message.reply_text("بخير 😊 شكراً لسؤالك")

    elif "مرحبا" in text or "اهلا" in text or "السلام" in text:
        await update.message.reply_text("أهلاً وسهلاً 👋")

    elif "من انت" in text or "مين انت" in text:
        await update.message.reply_text("أنا بوت بسيط أساعدك في الرد على الرسائل 🤖")

    elif "شكرا" in text or "thanks" in text:
        await update.message.reply_text("العفو 🌸")

    elif "باي" in text or "سلام" in text:
        await update.message.reply_text("مع السلامة 👋")

    else:
        await update.message.reply_text(f"لقد قلت: {update.message.text}")

# إضافة المعالجات
tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

@app.on_event("startup")
async def on_startup():
    """هذه الدالة تخبر تلجرام بمكان 'الجرس' (رابط الـ Webhook)"""
    webhook_url = f"{RENDER_EXTERNAL_URL}/webhook"
    await tg_app.bot.set_webhook(url=webhook_url)
    await tg_app.initialize()
    print(f"--- تم ضبط الـ Webhook بنجاح على الرابط: {webhook_url} ---")

@app.post("/webhook")
async def process_update(request: Request):
    """هذا هو 'الجرس' الذي يطرقه تلجرام عند وصول رسالة"""
    data = await request.json()
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return {"status": "ok"}

@app.get("/")
def home():
    return {"message": "البوت يعمل بنظام Webhook بنجاح!"}
