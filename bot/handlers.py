from sqlite3 import DatabaseError

from telebot import TeleBot
from website.models import Configuration, ChannelAdmin
import os
import django
from bot.keyboard import keyboard

configuration = Configuration.objects.first()
channel_admin = ChannelAdmin.objects.get(pk=1)
token = configuration.token

bot = TeleBot(token)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


@bot.message_handler(['start'])
def start(message):
    user_id = message.from_user.id
    name = configuration.bot_name
    bot.send_message(user_id, f' خوش آمدید{name}سلام به ربات ', reply_markup=keyboard)
    text = "لطفا قبل از خرید با استفاده از دکمه اضافه کردن ایمیل , ایمیل خود را اضافه کنید و سپس اقدام به خرید بفرمایید"
    bot.send_message(user_id, text)

