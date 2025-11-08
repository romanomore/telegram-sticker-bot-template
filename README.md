# Telegram Sticker Bot

A simple Telegram bot that automatically sends stickers when it detects specific phrases in messages.

## Features

- 🎯 Automatic sticker responses triggered by keywords
- 💬 Works in both private chats and groups
- ⚙️ Easy configuration through a phrase dictionary
- 🚀 Lightweight and fast

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Install Dependencies

```bash
pip install python-telegram-bot
```

## Setup

1. **Create your bot**
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Use `/newbot` command and follow instructions
   - Save the bot token you receive

2. **Configure the bot**
   - Create a `.env` file in the project root
   - Add your bot token: `TOKEN=your_bot_token_here`
   - Add your trigger phrases and sticker IDs to the `STICKERS` dictionary in the code
   - (Tip: Use the `handle_sticker` function in the code to find sticker IDs)

3. **Run and enjoy**
   - Start the bot
   - Add it to groups with friends or colleagues

## Usage

### Running the Bot

```bash
python sticker_bot.py
```
git
### Using Docker

```bash
docker-compose up -d
```

### Group Setup

To enable the bot in groups:
1. Message [@BotFather](https://t.me/BotFather)
2. Select your bot → `Bot Settings` → `Group Privacy`
3. **Disable** Privacy Mode
4. Add the bot to your desired group

## Example Configuration

```python
STICKERS = {
    'hello': 'CAACAgIAAxkBAAIC...',
    'goodbye': 'CAACAgIAAxkBAAID...'
}
```

When someone sends a message containing "hello", the bot will automatically reply with the corresponding sticker.

## Environment Variables

Create a `.env` file:

```env
TOKEN=your_bot_token_from_botfather
```

## Technologies

- Python 3.7+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library
- Docker & Docker Compose

## Project Structure

```
telegram-sticker-bot/
├── sticker_bot.py           # Main bot script
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yaml    # Docker Compose setup
└── README.md             # This file
```

## License

MIT

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ for the Telegram community**