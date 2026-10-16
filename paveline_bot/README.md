# Paveline Bot

A production-quality, beginner-friendly Python bot that automatically generates personalised birthday wishes and birthday card images using free AI models, and delivers them on schedule or on demand.

## Features

- Generate personalized birthday wishes in multiple languages
- Create beautiful card images with Pillow
- Schedule automatic birthday wishes
- Telegram bot with inline buttons
- Free AI provider support (Gemini, Groq, OpenRouter, Ollama)
- Offline fallback templates
- SQLite database

## Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and configure
4. Run the bot: `python main.py`

## Getting API Keys

- **Telegram Bot**: Create via [@BotFather](https://t.me/BotFather) on Telegram
- **Google Gemini**: Get free key from [Google AI Studio](https://aistudio.google.com/apikey)
- **Groq**: Get free key from [Groq Console](https://console.groq.com/keys)
- **OpenRouter**: Get free key from [OpenRouter](https://openrouter.ai/keys)
- **Ollama**: Install locally from [ollama.ai](https://ollama.ai/)

## Supported Languages

- English
- Kiswahili
- French
- Spanish
- Arabic

## Commands

- `/start` - Start the bot
- `/help` - Show help
- `/wish <name>` - Generate a wish
- `/add` - Add a birthday
- `/list` - List upcoming birthdays
- `/remove` - Remove a birthday
- `/language` - Set language
- `/remind on|off` - Toggle reminders
- `/card` - Re-render with another design

## License

MIT
