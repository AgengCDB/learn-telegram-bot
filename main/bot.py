import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)

from handlers.survey import survey_conversation
from handlers.help import help_handler

from custom_library.access import restricted

# Load .env file
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Define /start handler
async def check_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    print("User ID:", user_id)
    await update.message.reply_text(f"Your user ID is {user_id}")
    
@restricted  # Optional: restrict to allowed users
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Hello, {update.effective_user.first_name}!")


# Main bot setup
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("checkid", check_id))
    app.add_handler(CommandHandler("hello", hello))
    
    app.add_handler(survey_conversation)
    app.add_handler(help_handler)

    print("Bot is running...")
    app.run_polling()
