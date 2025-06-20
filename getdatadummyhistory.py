# getdatadummyhistory.py
from datetime import datetime

from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters
from telegram import Update, InputFile
from telegram.ext import ContextTypes

import os
import pandas as pd
import psycopg2

from custom_library.print import print_rd
from decorator import restricted, cooldown

ASK_HOUR = 1

@restricted
@cooldown(m=30)
async def getdatadummyhistory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏱️ How many hours back? (max 48)")
    return ASK_HOUR

@restricted
async def receive_hour(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        hour = int(update.message.text.strip())
        if not (1 <= hour <= 48):
            await update.message.reply_text("⚠️ Please enter a number between 1 and 48.")
            return ASK_HOUR
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number.")
        return ASK_HOUR

    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

        df = pd.read_sql_query(f"""
            SELECT * FROM dummy_history
            WHERE time >= NOW() - INTERVAL '{hour} hours'
            ORDER BY time DESC
        """, conn)
        conn.close()
    except Exception as e:
        print_rd(e)
        await update.message.reply_text(f"❌ Database error: {e}")
        return ConversationHandler.END

    if df.empty:
        await update.message.reply_text("📭 No data available for that range.")
        return ConversationHandler.END

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dummy_history_{timestamp}.csv"
    file_path = f"temp/{filename}"

    # Save DataFrame to CSV
    df.to_csv(file_path, index=False)

    # Send as document
    with open(file_path, "rb") as f:
        await update.message.reply_document(InputFile(f, filename=filename))

    # Clean up
    os.remove(file_path)

    return ConversationHandler.END

@restricted
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END

# Export the handler
def getdatadummyhistory_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("getdatadummyhistory", getdatadummyhistory)],
        states={
            ASK_HOUR: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_hour)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
