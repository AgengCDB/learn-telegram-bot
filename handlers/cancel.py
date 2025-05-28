from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

from custom_library.access import restricted

@restricted
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Survey canceled.")
    return ConversationHandler.END