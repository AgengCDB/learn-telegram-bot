# checkdbconn.py

import os
import psycopg2
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from decorator import restricted, cooldown

@restricted
@cooldown(m=10)
async def checkdbconn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        conn.close()
        await update.message.reply_text("✅ DB connected successfully!")
    except Exception as e:
        await update.message.reply_text(f"❌ Connection failed:\n{e}")

# Export handler
def checkdbconn_handler():
    return CommandHandler("checkdbconn", checkdbconn)
