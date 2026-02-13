from telegram import Update, MessageEntity
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

def extract_text(message):
    # Ambil text atau caption
    content = message.text or message.caption or ""
    if not content:
        return ""

    entities = message.entities or message.caption_entities or []

    if not entities:
        return content.strip()

    result = []
    last_index = 0

    for entity in entities:
        if entity.type in [MessageEntity.URL, MessageEntity.TEXT_LINK]:
            result.append(content[last_index:entity.offset])
            last_index = entity.offset + entity.length

    result.append(content[last_index:])
    return "".join(result).strip()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    raw = message.text or message.caption or ""
    cleaned = extract_text(message)

    if not cleaned:
        await message.reply_text("❌ Tidak ada teks untuk diringkas.")
        return

    lower = raw.lower()
    if "instagram.com" in lower:
        platform = "📸 Instagram"
    elif "tiktok.com" in lower:
        platform = "🎵 TikTok"
    elif "x.com" in lower or "twitter.com" in lower:
        platform = "🐦 X (Twitter)"
    else:
        platform = "🔗 Konten"

    summary = cleaned.split(".")[0]

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

    app.add_handler(
        MessageHandler(
            filters.TEXT | filters.CAPTION,
            handle_message
        )
    )

    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
