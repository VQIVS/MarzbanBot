from telebot import TeleBot, types
from website.models import Configuration, ChannelAdmin
from bot.models import User
import os
import django
from bot.keyboard import *

configuration = Configuration.objects.all()
channel_admin = ChannelAdmin.objects.all()
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


@bot.message_handler(func=lambda message: message.text == 'اضافه کردن ایمیل')
def add_email(message):
    user_id = message.from_user.id
    address = str(user_id) + '@telegram.com'
    user, created = User.objects.get_or_create(user_id=str(user_id))
    user.primary_email = address
    user.save()
    bot.send_message(user_id, "لطفا ایمیل خود را به صورت صحیح وارد کنید")

@bot.message_handler(func=lambda message: message.text == '⭐️خرید سرویس')
def buy(message):
    user_id = message.from_user.id
    message_buy = "🛒 لطفاً یکی از پلن های زیر را برای خرید انتخاب کنید."
    bot.send_message(user_id, message_buy, reply_markup=products_keyboard)

@bot.message_handler(func=lambda message: message.text == "💬پشتیبانی")
def support(message):
    user_id = message.from_user.id
    support_id = ChannelAdmin.telegram_id
    support_message = ""
    bot.send_message(user_id, support_message)