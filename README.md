# Telegram Sticker Bot

A versatile Telegram bot that automatically sends stickers when it detects specific phrases in messages. Features multiple modes for personal chat management and silent operation in groups.

## ✨ Features

- 🎯 **Automatic sticker responses** triggered by keywords
- 💬 **Smart chat detection**: full functionality in private chats, silent mode in groups
- 🔄 **Multiple modes**: Text-to-Sticker and Sticker-ID lookup
- 📋 **Phrase management**: view all configured phrases
- 🎛️ **Interactive menu** with inline keyboard buttons
- ⚙️ **Easy configuration** through a phrase dictionary
- 🚀 **Lightweight and fast**
- 🐳 **Docker support** for easy deployment

## 🎮 How It Works

### In Private Chats
The bot provides a full-featured interactive menu:
- **Text to Sticker mode**: Send text and get matching stickers
- **Sticker to ID mode**: Send stickers to get their IDs for configuration
- **List Phrases**: View all configured phrases and stickers

### In Group Chats
The bot operates in **silent mode**:
- Only sends stickers when trigger phrases are detected
- No menu prompts or error messages
- Completely unobtrusive

## 📦 Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Install Dependencies
```bash
pip install python-telegram-bot
```

## 🚀 Setup

### 1. Create Your Bot
- Message [@BotFather](https://t.me/BotFather) on Telegram
- Use `/newbot` command and follow instructions
- Save the bot token you receive

### 2. Configure the Bot
Create a `.env` file in the project root:
```env
TOKEN=your_bot_token_from_botfather
```

Add your trigger phrases and sticker IDs to the `STICKERS` dictionary in `crying_bot.py`:
```python
STICKERS = {
    'hello': 'CAACAgIAAxkBAAIC...',
    'goodbye': 'CAACAgIAAxkBAAID...',
    'thanks': 'CAACAgIAAxkBAAIE...'
}
```

### 3. Get Sticker IDs

**Easy way** (using the bot itself):
1. Start your bot in Telegram
2. Send `/start` command
3. Select "🔍 Sticker to ID" mode
4. Send any sticker
5. Bot will reply with the sticker's ID
6. Copy and add to `STICKERS` dictionary

**Manual way** (using the code):
- Uncomment the `handle_sticker` function
- Send a sticker to your bot
- Check the console output for the sticker ID

## 🎯 Usage

### Running the Bot
```bash
python crying_bot.py
```

### Using Docker
```bash
docker-compose up -d
```

### Bot Commands

In private chats:
- `/start` - Open the main menu with mode selection

### Interactive Modes

**📝 Text to Sticker**
- Bot listens for configured phrases
- Automatically replies with matching stickers
- Works in both private chats and groups

**🔍 Sticker to ID**
- Send stickers to the bot
- Get their IDs for configuration
- Only works in private chats

**📋 List Phrases**
- View all configured trigger phrases
- See associated sticker IDs
- Check total number of phrases

### Group Setup

To enable the bot in groups:
1. Message [@BotFather](https://t.me/BotFather)
2. Select your bot → `Bot Settings` → `Group Privacy`
3. **Disable** Privacy Mode (so bot can read messages)
4. Add the bot to your desired group

The bot will automatically operate in silent mode - only sending stickers, never spam.

## 📝 Example Configuration
```python
STICKERS = {
    'hello': 'CAACAgIAAxkBAAIC...',
    'good morning': 'CAACAgIAAxkBAAID...',
    'thanks': 'CAACAgIAAxkBAAIE...',
    'lol': 'CAACAgIAAxkBAAIF...',
    'congrats': 'CAACAgIAAxkBAAIG...'
}
```

When someone sends a message containing "hello", the bot will automatically reply with the corresponding sticker.

## 🔧 Environment Variables

Create a `.env` file:
```env
TOKEN=your_bot_token_from_botfather
```

**Important**: Never commit your `.env` file to git! It's already included in `.gitignore`.

## 🐳 Docker Deployment

The bot includes Docker support for easy deployment:

### Using Docker Compose (Recommended)
```bash
# Start the bot
docker-compose up -d

# View logs
docker logs -f pythonx_v2

# Stop the bot
docker-compose down

# Restart after code changes
docker-compose up -d --build
```

### Using Docker directly
```bash
# Build the image
docker build -t sticker-bot .

# Run the container
docker run -d --name sticker-bot --env-file .env sticker-bot

# View logs
docker logs -f sticker-bot
```

## 🛠️ Technologies

- Python 3.7+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library (v20.0+)
- Docker & Docker Compose

## 📁 Project Structure
```
telegram-sticker-bot/
├── crying_bot.py           # Main bot script
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yaml    # Docker Compose setup
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 💡 Tips & Tricks

### Finding Sticker IDs
1. Use the bot's built-in "Sticker to ID" mode (easiest way)
2. Or enable the debug `handle_sticker` function in the code

### Adding Multiple Phrases for One Sticker
```python
STICKERS = {
    'hello': 'STICKER_ID_1',
    'hi': 'STICKER_ID_1',      # Same sticker
    'hey': 'STICKER_ID_1',     # for different phrases
}
```

### Case-Insensitive Matching
The bot automatically converts all text to lowercase for matching, so:
- "Hello", "HELLO", and "hello" all trigger the same sticker

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests
- Suggest improvements

## 📄 License

MIT License - feel free to use this bot for personal or commercial projects!

## 🆘 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the code comments for implementation details

## 🎉 Acknowledgments

 🚀 Built using the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library.

---

**Made with ❤️ for the Telegram community**