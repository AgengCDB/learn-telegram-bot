import os
import psycopg2
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from telegram.constants import ParseMode

from decorator import restricted, cooldown

HELP_TEXT = """
🤖 *Available Commands*:

/status — Check system status
/getdatadummyhistory — Get dummy data from the last N hours
/checkdbconn - Check database connection
"""

@restricted
@cooldown(m=1)
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT, parse_mode=ParseMode.MARKDOWN)

# Export handler
def help_handler():
    return CommandHandler("help", help)