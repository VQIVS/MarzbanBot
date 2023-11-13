from sqlite3 import DatabaseError

from telebot import TeleBot
from website.models import Configuration, ChannelAdmin
from bot.models import User, Email
import os
import django
from bot.keyboard import keyboard, products_keyboard, tutorial_keyboard
from .utils.functions import is_valid_email

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
    support_id = channel_admin.telegram_id
    bot.send_message(user_id, support_id)

@bot.message_handler(func=lambda message: message.text == "اشتراک های من")
def subscriptions(message):
    user_id = message.from_user.id


@bot.message_handler(func=lambda message: is_valid_email(message.text))
def add_email(message):
    user_id = message.chat.id
    email = message.text
    try:
        user, created = User.objects.get_or_create(user_id=str(user_id))

        email_obj, created = Email.objects.get_or_create(address=email)
        user.emails.add(email_obj)

        message_save = f'کاربر {email} ثبت شد'
        bot.send_message(user_id, message_save)
    except DatabaseError:
        message_unsaved = 'ایمیل تکراری یا اشتباه است.'
        bot.send_message(user_id, message_unsaved)
@bot.message_handler(func=lambda message: message.text == "📚راهنما اتصال")
def tutorial(message):
    user_id = message.chat.id
    text = "برای آموزش ها عضو شوید"
    bot.send_message(user_id, text, reply_markup=tutorial_keyboard)