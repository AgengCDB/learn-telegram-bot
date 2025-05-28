from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🛠 Available Commands:\n"
        "/start - Start the bot\n"
        "/checkid - Check ID\n"
        "/help - Show this help message\n"
        "/hello - Say hello\n"
        "/startsurvey - Begin a short survey\n"
        "/cancel - Cancel current operation"
    )
    await update.message.reply_text(help_text)
    
# Export the handler so it can be added in main.py
help_handler = CommandHandler("help", help_command)