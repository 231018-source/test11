import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)
import uvicorn

# إنشاء تطبيق FastAPI
app = FastAPI()

# جلب التوكن من Render Environment Variables
TOKEN = os.getenv("BOT_TOKEN")

print("TOKEN =", TOKEN)

# رابط Render
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

# إنشاء تطبيق التلجرام
tg_app = Application.builder().token(TOKEN).build()


# أمر /start
async def start(update: Update, context):
    await update.message.reply_text(
        "أهلاً 👋\nالبوت يعمل بنجاح على Render 🚀"
    )


# الرد على الرسائل
async def handle_message(update: Update, context):
    text = (update.message.text or "").lower()

    if "مرحبا" in text or "اهلا" in text:
        await update.message.reply_text("أهلاً وسهلاً 👋")

    elif "كيف حالك" in text:
        await update.message.reply_text("أنا بخير 😊")

    elif "مين انت" in text or "من انت" in text:
        await update.message.reply_text("أنا بوت تلجرام 🤖")

    elif "شكرا" in text:
        await update.message.reply_text("العفو 🌸")

    else:
        await update.message.reply_text(
            f"أنت قلت:\n{text}"
        )


# إضافة المعالجات
tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)


# عند تشغيل السيرفر
@app.on_event("startup")
async def startup():
    await tg_app.initialize()
    await tg_app.start()

    webhook_url = f"{RENDER_EXTERNAL_URL}/webhook"

    await tg_app.bot.set_webhook(url=webhook_url)

    print(f"Webhook set to: {webhook_url}")


# استقبال رسائل التلجرام
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    update = Update.de_json(data, tg_app.bot)

    await tg_app.process_update(update)

    return {"ok": True}


# الصفحة الرئيسية
@app.get("/")
async def home():
    return {
        "status": "Bot is running successfully 🚀"
    }


# تشغيل السيرفر
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port
    )
