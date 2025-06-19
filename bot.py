import os
import json
from dotenv import load_dotenv

import logging

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
from functools import wraps

# Load .env file
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 📁 Allowed users file
def load_allowed_users(path=".config/allowed_users.txt"):
    try:
        with open(path, "r") as file:
            return set(int(line.strip()) for line in file if line.strip().isdigit())
    except FileNotFoundError:
        print("⚠️ allowed_users.txt not found.")
        return set()

ALLOWED_USERS = load_allowed_users()

# 💾 Persistent sign-in
SIGNED_IN_FILE = ".config/signed_in.json"

def save_signed_in():
    with open(SIGNED_IN_FILE, "w") as f:
        json.dump(list(SIGNED_IN_USERS), f)

def load_signed_in():
    if not os.path.exists(SIGNED_IN_FILE):
        # Create an empty file if it doesn't exist
        with open(SIGNED_IN_FILE, "w") as f:
            json.dump([], f)
        return set()

    try:
        with open(SIGNED_IN_FILE, "r") as f:
            return set(json.load(f))
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️ Failed to read {SIGNED_IN_FILE}: {e}")
        return set()

SIGNED_IN_USERS = load_signed_in()

# 🔐 Middleware check
def is_authenticated(user_id: int) -> bool:
    return user_id in SIGNED_IN_USERS and user_id in ALLOWED_USERS

# 🔐 Access control decorator
def restricted_command(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ALLOWED_USERS:
            await update.message.reply_text("❌ Access denied.")
            logging.warning(f"Access denied for user {user_id}")
            return
        if user_id not in SIGNED_IN_USERS:
            await update.message.reply_text("❌ Please use /start to sign in first.")
            logging.warning(f"User {user_id} attempted a command without signing in.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

# ✅ /start = sign in
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("❌ Access denied.")
        return
    SIGNED_IN_USERS.add(user_id)
    save_signed_in()
    logging.info(f"[SIGNED IN] User {user_id} has signed in.")
    await update.message.reply_text("✅ Signed in successfully! You may now use commands.")

# ❌ /stop = sign out
@restricted_command
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    SIGNED_IN_USERS.discard(user_id)
    save_signed_in()
    logging.info(f"[SIGNED OUT] User {user_id} has signed out.")
    await update.message.reply_text("👋 You've been signed out.")

@restricted_command
async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    print(f"[CHAT ID] User: {update.effective_user.id}, Chat: {chat.id}, Type: {chat.type}, Title: {chat.title}")
    await update.message.reply_text(f"🆔 Chat ID has been logged. (Chat Type: {chat.type})")

# 🟢 Example protected command
@restricted_command
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 Status: All systems operational.")

# 🚀 Run the bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("getchatid", get_chat_id))

    logging.debug("🔐 Very Private Bot Running...")
    app.run_polling()
