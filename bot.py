import os
import json
from functools import wraps
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from custom_library.print import print_rd, print_gr, print_yl, print_bl

from decorator import restricted, cooldown

from getdatadummyhistory import getdatadummyhistory_handler
from checkdbconn import checkdbconn_handler
from help import help_handler

# Load environment
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_GROUP_IDS = set(map(int, os.getenv("ALLOWED_GROUP_IDS", "").split(",")))
ALLOWED_USER_IDS = set(map(int, os.getenv("ALLOWED_USER_IDS", "").split(",")))

# /status = check
@restricted
@cooldown(m=1)
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 Bot is active and you're signed in!")

from telegram import Update
from telegram.ext import ContextTypes

# Main
if __name__ == "__main__":
    print_bl(f"ALLOWED_GROUP_IDS = {ALLOWED_GROUP_IDS}")
    print_bl(f"ALLOWED_USER_IDS = {ALLOWED_USER_IDS}")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(help_handler())
    app.add_handler(CommandHandler("status", status))
    
    app.add_handler(getdatadummyhistory_handler())
    app.add_handler(checkdbconn_handler())

    print_bl("🤖 Bot is running...")
    app.run_polling()

    def broken()