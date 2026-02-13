from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

def extract_text_for_summary(text: str) -> str:
    lines = text.splitlines()

    # buang baris yang berisi link
    clean_lines = [line for line in lines if not line.startswith("http")]

    if not clean_lines:
        return "Tidak ada teks untuk diringkas."

    full_text = " ".join(clean_lines)

    # ambil kalimat pertama sebagai ringkasan
    summary = full_text.split(".")[0]
    return summary.strip()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    lower_text = text.lower()

    if "instagram.com" in lower_text:
        platform = "📸 Instagram"
    elif "tiktok.com" in lower_text:
        platform = "🎵 TikTok"
    elif "x.com" in lower_text or "twitter.com" in lower_text:
        platform = "🐦 X (Twitter)"
    else:
        platform = None

    if platform:
        summary = extract_text_for_summary(text)
        reply = (
            f"{platform} terdeteksi\n\n"
            f"📝 Ringkasan singkat:\n"
            f"{summary}"
        )
    else:
        reply = "❓ Pesan diterima, tapi tidak ada link IG / TikTok / X"

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
