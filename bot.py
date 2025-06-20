import os
import json
from functools import wraps
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from custom_library.print import print_rd, print_gr, print_yl, print_bl
from custom_library.load import load_signed_in
from custom_library.save import save_signed_in
from custom_library.persistent import SIGNED_IN_FILE, SIGNED_IN_USERS

from decorator import restricted, cooldown

from getdatadummyhistory import getdatadummyhistory_handler
from checkdbconn import checkdbconn_handler
from help import help_handler

# Load environment
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_GROUP_ID = int(os.getenv("ALLOWED_GROUP_ID"))
ALLOWED_USER_IDS = set(map(int, os.getenv("ALLOWED_USER_IDS", "").split(",")))

# /start = sign in
@restricted
@cooldown(s=30)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user_id = update.effective_user.id

    if chat.type not in ["group", "supergroup"] or chat.id != ALLOWED_GROUP_ID:
        return

    if user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text("❌ You're not allowed to use this bot.")
        print_rd(f"[DENIED] {user_id} not in allowed list.")
        return
    SIGNED_IN_USERS.add(user_id)
    save_signed_in(signed_in_file=SIGNED_IN_FILE, signed_in_users=SIGNED_IN_USERS)
    print_gr(f"[SIGN IN] {user_id} signed in.")
    await update.message.reply_text("✅ You are now signed in and may use the bot.")

# /stop = sign out
@restricted
@cooldown(s=30)
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    SIGNED_IN_USERS.discard(user_id)
    save_signed_in(signed_in_file=SIGNED_IN_FILE, signed_in_users=SIGNED_IN_USERS)
    print_gr(f"[SIGN OUT] {user_id} signed out.")
    await update.message.reply_text("👋 You have been signed out.")

# /status = check
@restricted
@cooldown(m=2)
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 Bot is active and you're signed in!")

from telegram import Update
from telegram.ext import ContextTypes

@cooldown(m=10)
async def print_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat = update.effective_chat
    chat_id = chat.id
    chat_type = chat.type

    print_bl(f"[INFO] User ID: {user_id} | Chat ID: {chat_id} | Chat Type: {chat_type}")

    await update.message.reply_text("✅ Success.")

# Main
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(help_handler())
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("printids", print_ids))
    
    app.add_handler(getdatadummyhistory_handler())
    app.add_handler(checkdbconn_handler())

    print_bl("🤖 Bot is running...")
    app.run_polling()
