import uuid
from functools import wraps

from bot.models import BotUser
from telebot import TeleBot
from website.models import Configuration

from .keyboard import Keyboards

# Initializing settings
conf = Configuration.objects.first()
bot = TeleBot(conf.token)


def extract_user_id_from_caption(caption):
    try:
        parts = caption.split()
        if len(parts) < 2:
            raise ValueError("Caption does not contain user ID")

        user_id = int(parts[1])
        return user_id
    except (IndexError, ValueError) as e:
        print(f"Error extracting user ID: {e}")
        return None


def major_extract_user_id_from_caption(caption):
    try:
        parts = caption.split()
        user_index = parts.index("User")
        user_id = int(parts[user_index + 1])
        return user_id
    except (IndexError, ValueError, AttributeError) as e:
        print(f"Error extracting user ID: {e}")
        return None


def generate_user_id(length=32):
    unique_id = uuid.uuid4()
    return str(f"{conf.bot_name}_" + str(unique_id))[:length]


def rollback(query):
    user_id = query.message.chat.id
    msg_id = query.message.message_id
    bot.edit_message_text(
        chat_id=user_id,
        message_id=msg_id,
        text="❌ درخواست شما لغو شد.",
        reply_markup=None,
    )


def ban_check(bot):
    def decorator(handler_func):
        @wraps(handler_func)
        def wrapper(message, *args, **kwargs):
            user_id = (
                message.from_user.id
                if hasattr(message.from_user, "id")
                else message.chat.id
            )
            if BotUser.objects.filter(user_id=user_id, is_banned=True).exists():
                bot.send_message(user_id, "You are banned from using this bot.")
            else:
                return handler_func(message, *args, **kwargs)

        return wrapper

    return decorator


def bytes_to_gb(bytes_value):
    """
    Convert bytes to gigabytes.
    """
    return bytes_value / (1024**3)
