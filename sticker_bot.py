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
    raise ValueError("TOKEN not found in environment variables! Check your .env file")

STICKERS = {
    'hello': 'STICKER_ID',
    'goodbye': 'STICKER_ID_2',
    # Add your phrases here
}

# Dictionary to store user modes in private chats
user_modes = {}


def is_private_chat(update: Update) -> bool:
    """Check if the chat is private"""
    return update.effective_chat.type == 'private'


async def start(update: Update, context: CallbackContext):
    """
    /start command - shows main menu (only in private chats)
    """
    if not is_private_chat(update):
        # In groups, ignore /start or respond briefly
        await update.message.reply_text('👋 Hi! I will send stickers when I detect key phrases.')
        return
    
    keyboard = [
        [InlineKeyboardButton("📝 Text to Sticker", callback_data='text_to_sticker')],
        [InlineKeyboardButton("🔍 Sticker to ID", callback_data='sticker_to_id')],
        [InlineKeyboardButton("📋 List Phrases", callback_data='list_phrases')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        '👋 Hi! Choose a mode:\n\n'
        '📝 *Text to Sticker* - bot will send stickers when phrases are detected\n'
        '🔍 *Sticker to ID* - bot will return IDs of sent stickers\n'
        '📋 *List Phrases* - show all added phrases',
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def list_phrases(update: Update, context: CallbackContext):
    """
    Show list of all phrases and stickers
    """
    query = update.callback_query
    
    if not STICKERS:
        await query.edit_message_text('📋 Phrase list is empty!')
        return
    
    message = '📋 *List of phrases and stickers:*\n\n'
    for i, (phrase, sticker_id) in enumerate(STICKERS.items(), 1):
        # Shorten ID for readability
        short_id = sticker_id[:20] + '...' if len(sticker_id) > 20 else sticker_id
        message += f'{i}. `{phrase}` → `{short_id}`\n'
    
    message += f'\n*Total phrases: {len(STICKERS)}*\n\n'
    message += 'Use /start to return to the menu'
    
    await query.edit_message_text(message, parse_mode='Markdown')


async def button_handler(update: Update, context: CallbackContext):
    """
    Handle button clicks
    """
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    mode = query.data
    
    if mode == 'list_phrases':
        await list_phrases(update, context)
        return
    
    # Save selected mode for the user
    user_modes[user_id] = mode
    
    if mode == 'text_to_sticker':
        await query.edit_message_text(
            '📝 *Mode: Text to Sticker*\n\n'
            'Send text - I will search for matching stickers!\n\n'
            'Use /start to change mode',
            parse_mode='Markdown'
        )
    elif mode == 'sticker_to_id':
        await query.edit_message_text(
            '🔍 *Mode: Sticker to ID*\n\n'
            'Send me a sticker - I will return its ID!\n\n'
            'Use /start to change mode',
            parse_mode='Markdown'
        )


async def handle_text(update: Update, context: CallbackContext):
    """
    Handle text messages
    """
    # IN GROUPS: always search for phrases and send stickers (silent mode)
    if not is_private_chat(update):
        text = update.message.text.lower()
        for phrase, sticker_id in STICKERS.items():
            if phrase in text:
                await update.message.reply_sticker(sticker_id)
                break  # Send only one sticker
        return
    
    # IN PRIVATE CHATS: work with modes
    user_id = update.message.from_user.id
    mode = user_modes.get(user_id, None)
    
    # If mode is not selected
    if mode is None:
        await update.message.reply_text(
            'Please select a mode first using /start'
        )
        return
    
    # text_to_sticker mode
    if mode == 'text_to_sticker':
        text = update.message.text.lower()
        found = False
        for phrase, sticker_id in STICKERS.items():
            if phrase in text:
                await update.message.reply_sticker(sticker_id)
                found = True
                break
        
        if not found:
            await update.message.reply_text(
                '🤷 No matching sticker found for this phrase'
            )
    
    # sticker_to_id mode - ignore text
    elif mode == 'sticker_to_id':
        await update.message.reply_text(
            'In this mode I expect a sticker, not text. Please send a sticker!'
        )


async def handle_sticker(update: Update, context: CallbackContext):
    """
    Handle stickers
    """
    sticker = update.message.sticker
    
    # IN GROUPS: ignore stickers (silent mode)
    if not is_private_chat(update):
        return
    
    # IN PRIVATE CHATS: work with modes
    user_id = update.message.from_user.id
    mode = user_modes.get(user_id, None)
    
    # If mode is not selected
    if mode is None:
        await update.message.reply_text(
            'Please select a mode first using /start'
        )
        return
    
    # sticker_to_id mode - return ID
    if mode == 'sticker_to_id':
        await update.message.reply_text(
            f'🆔 *Sticker ID:*\n`{sticker.file_id}`\n\n'
            f'📋 Copy and add to STICKERS dictionary',
            parse_mode='Markdown'
        )
    
    # text_to_sticker mode - ignore sticker
    elif mode == 'text_to_sticker':
        await update.message.reply_text(
            'In this mode I respond only to text, not stickers.\n'
            'If you want to get a sticker ID, use /start and select "Sticker to ID"'
        )


def main():
    print("🚀 Starting bot...")
    
    application = Application.builder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))
    
    print("✅ Bot started and waiting for messages")
    application.run_polling()

if __name__ == '__main__':
    main()