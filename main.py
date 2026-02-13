from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "instagram.com" in text:
        reply = "📸 Link Instagram terdeteksi"
    elif "tiktok.com" in text:
        reply = "🎵 Link TikTok terdeteksi"
    elif "x.com" in text or "twitter.com" in text:
        reply = "🐦 Link X (Twitter) terdeteksi"
    else:
        reply = "❓ Pesan diterima, tapi bukan link IG / TikTok / X"

    await update.message.reply_text(reply)

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("BOT_TOKEN belum diset")
        return

    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
