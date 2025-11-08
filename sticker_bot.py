from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import time
import threading
import os

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN not found in environments! Check file .env")

STICKERS = {
    'text': 'STICKER_ID'
}

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Hi! Write text, I will send the sticker.')

async def send_sticker(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    for phrase, sticker_id in STICKERS.items():
        if phrase in text:
            await update.message.reply_sticker(sticker_id)
            break  

# Function for search sticker ID
async def handle_sticker(update: Update, context: CallbackContext):
    sticker = update.message.sticker
    if sticker:
        await update.message.reply_text(f"Sticker ID: {sticker.file_id}")
    else:
        await update.message.reply_text("Can't find sticker")

def main():
    print("Launch...")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_sticker))
    application.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))
    print("Succes, waiting for stickers.")
    application.run_polling()

if __name__ == '__main__':
    main()