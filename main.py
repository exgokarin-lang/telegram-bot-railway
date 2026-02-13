from telegram import Update, MessageEntity
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

def get_all_text(message):
    # 1. text
    if message.text:
        return message.text.strip()

    # 2. caption
    if message.caption:
        return message.caption.strip()

    # 3. web page preview (INI YANG PALING SERING KELEWAT)
    if message.web_page:
        desc = message.web_page.description or ""
        title = message.web_page.title or ""
        combined = f"{title}. {desc}".strip()
        return combined

    return ""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    content = get_all_text(msg)

    if not content:
        await msg.reply_text("❌ Tidak ada teks untuk diringkas.")
        return

    lower = content.lower()

    if "instagram" in lower:
        platform = "📸 Instagram"
    elif "tiktok" in lower:
        platform = "🎵 TikTok"
    elif "x.com" in lower or "twitter" in lower:
        platform = "🐦 X (Twitter)"
    else:
        platform = "🔗 Berita"

    summary = content.split(".")[0]

    reply = (
        f"{platform} terdeteksi\n\n"
        f"📝 Ringkasan singkat:\n"
        f"{summary}"
    )

    await msg.reply_text(reply)

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("BOT_TOKEN belum diset")
        return

    app = ApplicationBuilder().token(token).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT | filters.CAPTION | filters.Entity("url"),
            handle_message
        )
    )

    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
