from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)

from custom_library.access import restricted
from handlers.cancel import cancel

ASK_NAME, ASK_AGE = range(2)  # Conversation steps

@restricted
async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("What's your name?")
    return ASK_NAME

@restricted
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Great, how old are you?")
    return ASK_AGE

@restricted
async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age_text = update.message.text.strip()

    if not age_text.isdigit():
        await update.message.reply_text("❗ Please enter a valid number for your age.")
        return ASK_AGE

    age = int(age_text)
    if not (1 <= age <= 120):
        await update.message.reply_text("❗ Please enter an age between 1 and 120.")
        return ASK_AGE

    name = context.user_data["name"]
    await update.message.reply_text(f"✅ Thanks {name}, age {age} recorded!")
    return ConversationHandler.END

# This is what you import in main.py
survey_conversation = ConversationHandler(
    entry_points=[CommandHandler("startsurvey", start_survey)],
    states={
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
        ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)