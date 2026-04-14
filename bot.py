import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from config import BOT_TOKEN
from uploader import upload_to_pixeldrain

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me any file and I will give you a download link.")


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document or update.message.video or update.message.audio

    if not file:
        await update.message.reply_text("Send a valid file.")
        return

    file_obj = await context.bot.get_file(file.file_id)

    file_path = os.path.join(DOWNLOAD_DIR, file.file_name or f"{file.file_id}")

    await update.message.reply_text("Downloading...")

    await file_obj.download_to_drive(file_path)

    await update.message.reply_text("Uploading...")

    link = upload_to_pixeldrain(file_path)

    if link:
        await update.message.reply_text(f"Download Link:\n{link}")
    else:
        await update.message.reply_text("Upload failed")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO | filters.AUDIO, handle_file))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
