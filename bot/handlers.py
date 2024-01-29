from sqlite3 import DatabaseError
from telebot import TeleBot
from website.models import Configuration, ChannelAdmin, Message
import os
import django
from bot.keyboard import keyboard

""" get the needle data from db """
configuration = Configuration.objects.first()
message_bot = Message.objects.first()
token = configuration.token
bot = TeleBot(token)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


@bot.message_handler(['start'])
def start(message):
    user_id = message.from_user.id
    text = message_bot.text
    bot.send_message(user_id, text, reply_markup=keyboard)


