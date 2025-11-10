from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    filters, 
    CallbackContext
)
import os

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN not found in environments! Check file .env")

STICKERS = {
    'text': 'STICKER_ID'
}

# user_id: mode ('text_to_sticker' или 'sticker_to_id')
user_modes = {}


async def start(update: Update, context: CallbackContext):
    """
    Команда /start - показывает главное меню с выбором режима
    """
    keyboard = [
        [InlineKeyboardButton("📝 Text to Sticker", callback_data='text_to_sticker')],
        [InlineKeyboardButton("🔍 Sticker to ID", callback_data='sticker_to_id')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        '👋 Привет! Выбери режим работы:\n\n'
        '📝 *Text to Sticker* - пишешь фразу - бот отправлятет стикеры (отладка работы)\n'
        '🔍 *Sticker to ID* - бот будет возвращать ID отправленных стикеров',
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def button_handler(update: Update, context: CallbackContext):
    """
    Обработчик нажатий на кнопки
    """
    query = update.callback_query
    await query.answer()  # Убирает "часики" на кнопке
    
    user_id = query.from_user.id
    mode = query.data  # 'text_to_sticker' или 'sticker_to_id'
    
    # Сохраняем выбранный режим для пользователя
    user_modes[user_id] = mode
    
    if mode == 'text_to_sticker':
        await query.edit_message_text(
            '📝 *Режим: Text to Sticker*\n\n'
            'Отправляй текст - я буду искать подходящие стикеры!\n\n'
            'Для смены режима используй /start',
            parse_mode='Markdown'
        )
    elif mode == 'sticker_to_id':
        await query.edit_message_text(
            '🔍 *Режим: Sticker to ID*\n\n'
            'Отправь мне стикер - я верну его ID!\n\n'
            'Для смены режима используй /start',
            parse_mode='Markdown'
        )


async def handle_text(update: Update, context: CallbackContext):
    """
    Обработка текстовых сообщений - работает только в режиме text_to_sticker
    """
    user_id = update.message.from_user.id
    mode = user_modes.get(user_id, None)
    
    # Если режим не выбран, предлагаем выбрать
    if mode is None:
        await update.message.reply_text(
            'Сначала выбери режим работы через /start'
        )
        return
    
    # Если включен режим text_to_sticker
    if mode == 'text_to_sticker':
        text = update.message.text.lower()
        for phrase, sticker_id in STICKERS.items():
            if phrase in text:
                await update.message.reply_sticker(sticker_id)
                break
    
    # Если режим sticker_to_id, игнорируем текст (ждем стикер)
    elif mode == 'sticker_to_id':
        await update.message.reply_text(
            'В этом режиме я жду стикер, а не текст. Отправь стикер!'
        )


async def handle_sticker(update: Update, context: CallbackContext):
    """
    Обработка стикеров - работает только в режиме sticker_to_id
    """
    user_id = update.message.from_user.id
    mode = user_modes.get(user_id, None)
    
    sticker = update.message.sticker
    
    # Если режим не выбран
    if mode is None:
        await update.message.reply_text(
            'Сначала выбери режим работы через /start'
        )
        return
    
    # Если включен режим sticker_to_id
    if mode == 'sticker_to_id':
        await update.message.reply_text(
            f'🆔 *Sticker ID:*\n`{sticker.file_id}`\n\n'
            f'📋 Скопируй и добавь в словарь STICKERS',
            parse_mode='Markdown'
        )
    
    # Если режим text_to_sticker, игнорируем стикер
    elif mode == 'text_to_sticker':
        await update.message.reply_text(
            'В этом режиме я реагирую только на текст, а не на стикеры.'
        )


def main():
    print("🚀 Запуск бота...")
    
    application = Application.builder().token(TOKEN).build()
    
    # Обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))
    
    print("✅ Бот запущен и ожидает сообщений")
    application.run_polling()


if __name__ == '__main__':
    main()