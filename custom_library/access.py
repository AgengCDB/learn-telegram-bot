# access.py
from functools import wraps

def load_allowed_users(file_path="D:\\GithubProject\\learn-telegram-bot\\.config\\allowed_users.txt"):
    try:
        with open(file_path, "r") as f:
            return [
                int(line.strip())
                for line in f
                if line.strip() and not line.strip().startswith("#")
            ]
    except FileNotFoundError:
        print("allowed_users.txt not found.")
        return []

ALLOWED_USERS = load_allowed_users()

def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ALLOWED_USERS:
            await update.message.reply_text("Access denied.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped
