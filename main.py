from telegram import Update, MessageEntity
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

def extract_text_excluding_urls(message):
    text = message.text
    if not text:
        return ""

    if not message.entities:
        return text.strip()

    result = []
    last_index = 0

    for entity in message.entities:
        if entity.type in [MessageEntity.URL, MessageEntity.TEXT_LINK]:
            # ambil teks sebelum URL
            result.append(text[last_index:entity.offset])
            last_index = entity.offset + entity.length

    result.append(text[last_index:])
    cleaned = "".join(result).strip()

    return cleaned

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    full_text = message.text or ""

    cleaned_text = extract_text_excluding_urls(message)

    if not cleaned_text:
        await message.reply_text("❌ Tidak ada teks untuk diringkas.")
        return

    lower = full_text.lower()
    if "instagram.com" in lower:
        platform = "📸 Instagram"
    elif "tiktok.com" in lower:
        platform = "🎵 TikTok"
    elif "x.com" in lower or "twitter.com" in lower:
        platform = "🐦 X (Twitter)"
    else:
        platform = "🔗 Link"

    summary = cleaned_text.split(".")[0]

    reply = (
        f"{platform} terdeteksi\n\n"
        f"📝 Ringkasan singkat:\n"
        f"{summary}"
    )

    await message.reply_text(reply)

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
