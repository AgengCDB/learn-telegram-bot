import os
import json
from functools import wraps
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes

from custom_library.print import print_yl, print_rd
from custom_library.persistent import SIGNED_IN_USERS

# Load environment variables
load_dotenv()
ALLOWED_GROUP_ID = int(os.getenv("ALLOWED_GROUP_ID"))
ALLOWED_USER_IDS = set(map(int, os.getenv("ALLOWED_USER_IDS", "").split(",")))

# Cooldown file
COOLDOWN_FILE = ".config/cooldown.json"

def load_cooldowns():
    if not os.path.exists(COOLDOWN_FILE):
        return {}
    try:
        with open(COOLDOWN_FILE, "r") as f:
            raw = json.load(f)
            return {
                int(uid): {
                    cmd: datetime.fromisoformat(when)
                    for cmd, when in cmds.items()
                } for uid, cmds in raw.items()
            }
    except Exception as e:
        print_rd(f"[COOLDOWN] Failed to load: {e}")
        return {}

def save_cooldowns(data):
    try:
        with open(COOLDOWN_FILE, "w") as f:
            json.dump({
                str(uid): {
                    cmd: when.isoformat()
                    for cmd, when in cmds.items()
                } for uid, cmds in data.items()
            }, f, indent=2)
    except Exception as e:
        print_rd(f"[COOLDOWN] Failed to save: {e}")

# Global cooldown state
USER_COOLDOWNS = load_cooldowns()

# 🔒 Access Control Decorator
def restricted(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        chat = update.effective_chat
        user_id = update.effective_user.id

        if chat.type not in ["group", "supergroup"] or chat.id != ALLOWED_GROUP_ID:
            print_yl(f"[RESTRICTED] IGNORED {user_id} (wrong chat)")
            return

        if user_id not in ALLOWED_USER_IDS:
            await update.message.reply_text("❌ Access denied.")
            print_yl(f"[RESTRICTED] DENIED {user_id} not in allowed list.")
            return

        if user_id not in SIGNED_IN_USERS:
            await update.message.reply_text("❌ Please use /start to sign in first.")
            print_yl(f"[RESTRICTED] UNSIGNED {user_id} tried command.")
            return

        return await func(update, context, *args, **kwargs)

    return wrapper

# 🕒 Cooldown Decorator
def cooldown(h=0, m=0, s=0):
    cooldown_delta = timedelta(hours=h, minutes=m, seconds=s)

    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            user_id = update.effective_user.id
            func_name = func.__name__
            now = datetime.now()

            last_used = USER_COOLDOWNS.get(user_id, {}).get(func_name)
            if last_used and now < last_used:
                remaining = last_used - now
                remaining_str = str(remaining).split(".")[0]
                await update.message.reply_text(
                    f"⚠️ This command was used recently. Please wait {remaining_str} before trying again."
                )
                print_yl(f"""[COOLDOWN] {user_id} tried /{func_name} too soon.""")
                return

            if user_id not in USER_COOLDOWNS:
                USER_COOLDOWNS[user_id] = {}
            USER_COOLDOWNS[user_id][func_name] = now + cooldown_delta
            save_cooldowns(USER_COOLDOWNS)

            return await func(update, context, *args, **kwargs)

        return wrapper
    return decorator
